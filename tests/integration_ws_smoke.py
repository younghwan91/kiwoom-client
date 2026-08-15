#!/usr/bin/env python3
"""실서버 대상 프로토콜 검증 하네스 — 라이브러리의 가정이 맞는지 확인한다.

단위 테스트는 전부 mock 이라 "우리가 이해한 프로토콜대로 코드가 동작한다"까지만
증명한다. 이 스크립트는 그 이해 자체가 맞는지를 실서버에 물어본다.

검증 항목:
    1. 토큰 응답의 만료 필드가 expires_dt 인지 expires_in 인지
    2. 만료·무효 토큰에 API 가 401 을 주는지, 200 + return_code 를 주는지
       (401 이 아니면 BaseClient 의 자동 재발급이 트리거되지 않는다)
    3. WebSocket LOGIN 핸드셰이크 응답 구조
    4. 서버 PING 프레임 구조
    5. REG(실시간 등록) 응답 구조
    6. REAL 프레임의 항목 필드명 (item / values) — 장중에만 확인 가능
    2b. 위 신호로 자동 재발급이 실제로 도는지 (실서버 자가복구)

사용법:
    python tests/integration_ws_smoke.py                    # 모의투자, .env
    python tests/integration_ws_smoke.py --prod             # 실서버
    python tests/integration_ws_smoke.py --env-file PATH    # 다른 .env
    python tests/integration_ws_smoke.py --listen 60        # 수신 대기 60초

비밀값은 출력하지 않는다. 토큰은 앞뒤 일부만 마스킹해 보여준다.
"""

from __future__ import annotations

import argparse
import asyncio
import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))

import httpx  # noqa: E402

from kiwoom_rest_api import KiwoomAPI  # noqa: E402
from kiwoom_rest_api.auth import KiwoomAuth, KiwoomAuthError  # noqa: E402
from kiwoom_rest_api.base import BaseClient  # noqa: E402
from kiwoom_rest_api.websocket import KiwoomWebSocket  # noqa: E402

PROD = "https://api.kiwoom.com"
MOCK = "https://mockapi.kiwoom.com"
PROD_WS = "wss://api.kiwoom.com:10000/api/dostk/websocket"
MOCK_WS = "wss://mockapi.kiwoom.com:10000/api/dostk/websocket"

# 검증 결과 누적: (항목, 결론, 판정)
results: list[tuple[str, str, str]] = []


def record(item: str, finding: str, verdict: str) -> None:
    results.append((item, finding, verdict))
    icon = {"OK": "✅", "MISMATCH": "❌", "UNKNOWN": "❔"}.get(verdict, "•")
    print(f"  {icon} {finding}")


def mask(token: str | None) -> str:
    if not token:
        return "(없음)"
    return f"{token[:6]}…{token[-4:]} (len={len(token)})" if len(token) > 12 else "(짧음)"


def load_env(path: Path) -> tuple[str, str]:
    if not path.is_file():
        sys.exit(f"❌ .env 를 찾을 수 없습니다: {path}")
    values: dict[str, str] = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        k, _, v = line.partition("=")
        values[k.strip()] = v.strip().strip('"').strip("'")
    key = values.get("KIWOOM_APP_KEY", "")
    secret = values.get("KIWOOM_APP_SECRET", "")
    if not key or not secret:
        sys.exit(f"❌ {path} 에 KIWOOM_APP_KEY / KIWOOM_APP_SECRET 이 없습니다")
    return key, secret


def dump(
    label: str, payload: Any, redact_keys: tuple[str, ...] = ("token", "access_token")
) -> None:
    """구조 확인용 덤프. 토큰류는 마스킹."""
    if isinstance(payload, dict):
        shown = {k: (mask(v) if k in redact_keys and isinstance(v, str) else v)
                 for k, v in payload.items()}
    else:
        shown = payload
    print(f"    {label}: {json.dumps(shown, ensure_ascii=False)[:600]}")


# --- 1. 토큰 발급 응답 구조 ---------------------------------------------------

def check_token_response(auth: KiwoomAuth) -> str:
    print("\n[1] 토큰 발급 응답 구조")
    try:
        data = auth.issue_token()
    except KiwoomAuthError as exc:
        record("토큰 발급", f"발급 실패: {exc}", "MISMATCH")
        sys.exit("토큰을 못 받아 이후 검증을 진행할 수 없습니다.")

    dump("응답 전체", data)
    print(f"    응답 키: {sorted(data)}")

    has_dt, has_in = "expires_dt" in data, "expires_in" in data
    if has_dt:
        record("만료 필드", f"expires_dt 사용 — 값 {data['expires_dt']!r}", "OK")
    if has_in:
        record("만료 필드", f"expires_in 사용 — 값 {data['expires_in']!r}", "OK")
    if not (has_dt or has_in):
        record("만료 필드", f"둘 다 없음! 실제 키: {sorted(data)} "
                          "→ 선제 갱신이 동작하지 않고 401 경로에만 의존한다", "MISMATCH")

    if auth.expires_at is not None:
        import time
        left = auth.expires_at - time.time()
        record("만료 파싱", f"파싱 성공 — 약 {left/3600:.1f}시간 후 만료", "OK")
    else:
        record("만료 파싱", "파싱 실패 (expires_at=None) → 선제 갱신 비활성", "MISMATCH")

    token_key = "token" if "token" in data else "access_token" if "access_token" in data else None
    record("토큰 키", f"{token_key!r} 사용 — {mask(auth.token)}",
           "OK" if token_key else "MISMATCH")
    return auth.token or ""


# --- 2. 무효 토큰에 대한 응답 -------------------------------------------------

def check_invalid_token(base_url: str) -> None:
    print("\n[2] 무효 토큰 요청 시 응답 (자동 재발급 트리거 조건)")
    with httpx.Client(base_url=base_url, timeout=30.0) as client:
        resp = client.post(
            "/api/dostk/stkinfo",
            headers={
                "Content-Type": "application/json;charset=UTF-8",
                "api-id": "ka10001",
                "authorization": "Bearer invalid-token-for-protocol-check",
            },
            json={"stk_cd": "005930"},
        )
    print(f"    HTTP status: {resp.status_code}")
    try:
        body = resp.json()
        dump("body", body)
        rc = body.get("return_code")
    except ValueError:
        body, rc = None, None
        print(f"    body(raw): {resp.text[:200]!r}")

    # 서버가 뭘 주는지는 서버의 사실이다. 물어야 할 건 라이브러리가 그걸
    # 인증 실패로 알아보느냐다.
    handled = (
        resp.status_code in BaseClient.TOKEN_ERROR_STATUSES
        or rc in BaseClient.TOKEN_ERROR_RETURN_CODES
    )
    record("무효 토큰 신호",
           f"서버 응답 = HTTP {resp.status_code} / return_code={rc}. "
           f"라이브러리 인식: statuses={BaseClient.TOKEN_ERROR_STATUSES}, "
           f"return_codes={sorted(BaseClient.TOKEN_ERROR_RETURN_CODES)} → "
           f"{'인식함' if handled else '인식 못함 (자동 재발급이 트리거되지 않는다)'}",
           "OK" if handled else "MISMATCH")


def check_live_self_heal(key: str, secret: str, base_url: str) -> None:
    """실서버 상대로 자동 재발급이 실제로 도는지 확인한다.

    만료를 기다릴 수 없으니 캐시된 토큰만 손상시킨다. 만료 시각은 그대로 두어
    선제 갱신이 개입하지 못하게 하고, 오직 응답 기반 재발급 경로만 태운다.
    """
    print("\n[2b] 실서버 자동 재발급 (토큰 손상 후 자가복구)")
    api = KiwoomAPI(key, secret, base_url=base_url)
    try:
        api.login()
        before = api._auth.token
        # 만료 시각은 유효한 채로 토큰 값만 망가뜨린다 → 선제 갱신 우회
        api._auth._token = "deliberately-broken-token"
        print(f"    토큰 손상 후 조회 시도 (before={mask(before)})")

        result = api.stock_info.basic_stock_info(stk_cd="005930")
        after = api._auth.token

        if result.get("return_code") == 0 and after not in (None, "deliberately-broken-token"):
            record("자가복구",
                   f"손상된 토큰으로 요청 → 자동 재발급 후 성공 "
                   f"(종목명={result.get('stk_nm')!r}, 새 토큰={mask(after)})", "OK")
        else:
            record("자가복구", f"복구 실패 — 응답={str(result)[:120]}", "MISMATCH")
    except Exception as exc:
        record("자가복구", f"복구 실패 — {type(exc).__name__}: {exc}", "MISMATCH")
    finally:
        api.close()


# --- 3~6. WebSocket 프로토콜 --------------------------------------------------

async def check_websocket(token: str, ws_url: str, codes: list[str], listen_s: int) -> None:
    print(f"\n[3~6] WebSocket 프로토콜 ({ws_url})")
    frames: list[dict[str, Any]] = []
    ws = KiwoomWebSocket(token, ws_url=ws_url)

    # 모든 프레임을 원본 그대로 모은다.
    ws.on_message(frames.append)

    try:
        await ws.connect()
    except Exception as exc:
        record("WS LOGIN", f"연결/로그인 실패: {type(exc).__name__}: {exc}", "MISMATCH")
        return
    record("WS LOGIN", "LOGIN 핸드셰이크 성공 (return_code=0)", "OK")

    listener = asyncio.create_task(ws.listen())
    await ws.subscribe(["0B", "0D"], codes)
    print(f"    REG 전송: type=['0B','0D'] item={codes}")
    print(f"    {listen_s}초 동안 수신 대기…")

    try:
        await asyncio.wait_for(asyncio.shield(listener), timeout=listen_s)
    except asyncio.TimeoutError:
        pass
    finally:
        await ws.disconnect()
        listener.cancel()

    # --- 수집한 프레임 분석 ---
    by_trnm: dict[str, list[dict]] = {}
    for f in frames:
        by_trnm.setdefault(str(f.get("trnm")), []).append(f)

    print(f"\n    수신 프레임 {len(frames)}건: "
          f"{ {k: len(v) for k, v in by_trnm.items()} }")
    for trnm, items in by_trnm.items():
        dump(f"{trnm} 샘플", items[0])

    # REG 응답
    if "REG" in by_trnm:
        rc = by_trnm["REG"][0].get("return_code")
        record("WS REG", f"REG 응답 수신 (return_code={rc})",
               "OK" if rc in (0, "0") else "MISMATCH")
    else:
        record("WS REG", "REG 응답 프레임이 오지 않음", "UNKNOWN")

    # PING — listen() 이 내부에서 처리하므로 on_message 로도 보인다
    if "PING" in by_trnm:
        record("WS PING", f"PING 수신 확인 — 필드 {sorted(by_trnm['PING'][0])}", "OK")
    else:
        record("WS PING", f"{listen_s}초 안에 PING 미수신 (주기가 더 길 수 있음)", "UNKNOWN")

    # REAL — 핵심 검증
    if "REAL" in by_trnm:
        sample = by_trnm["REAL"][0]
        data = sample.get("data")
        record("WS REAL", f"REAL 프레임 수신 — 최상위 키 {sorted(sample)}", "OK")
        if isinstance(data, list) and data and isinstance(data[0], dict):
            entry_keys = sorted(data[0])
            print(f"    REAL data[0] 키: {entry_keys}")
            dump("REAL data[0] 원본", data[0], redact_keys=())
            for field in ("type", "item", "values"):
                record(f"REAL.{field}",
                       f"{'존재' if field in data[0] else '없음'} — 라이브러리 가정과 "
                       f"{'일치' if field in data[0] else '불일치'}",
                       "OK" if field in data[0] else "MISMATCH")
        else:
            record("WS REAL", f"data 가 dict 리스트가 아님: {type(data).__name__}", "MISMATCH")
    else:
        record("WS REAL",
               "REAL 프레임 미수신 — 장 마감 시간이면 정상. "
               "item/values 필드명은 장중 재실행으로만 확정 가능",
               "UNKNOWN")


def main() -> None:
    ap = argparse.ArgumentParser(description="키움 실서버 프로토콜 검증")
    ap.add_argument("--prod", action="store_true", help="실서버 사용 (기본: 모의투자)")
    ap.add_argument("--env-file", default=str(ROOT / ".env"), help=".env 경로")
    ap.add_argument("--listen", type=int, default=30, help="WebSocket 수신 대기 초")
    ap.add_argument("--codes", default="005930,000660", help="구독 종목코드 (쉼표 구분)")
    args = ap.parse_args()

    base_url = PROD if args.prod else MOCK
    ws_url = PROD_WS if args.prod else MOCK_WS
    key, secret = load_env(Path(args.env_file))

    print("=" * 72)
    print(f"키움 프로토콜 검증 — {'실서버' if args.prod else '모의투자'} ({base_url})")
    print(f".env: {args.env_file}")
    print("=" * 72)

    auth = KiwoomAuth(key, secret, base_url)
    try:
        token = check_token_response(auth)
        check_invalid_token(base_url)
        check_live_self_heal(key, secret, base_url)
        asyncio.run(check_websocket(token, ws_url, args.codes.split(","), args.listen))
    finally:
        auth.close()

    print("\n" + "=" * 72)
    print("요약")
    print("=" * 72)
    counts = {"OK": 0, "MISMATCH": 0, "UNKNOWN": 0}
    for item, finding, verdict in results:
        counts[verdict] = counts.get(verdict, 0) + 1
        icon = {"OK": "✅", "MISMATCH": "❌", "UNKNOWN": "❔"}.get(verdict, "•")
        print(f"{icon} [{item}] {finding}")
    print(f"\n일치 {counts['OK']} / 불일치 {counts['MISMATCH']} / 미확정 {counts['UNKNOWN']}")
    if counts["MISMATCH"]:
        print("\n❌ 불일치 항목이 있습니다 — 라이브러리 수정이 필요합니다.")
        sys.exit(1)


if __name__ == "__main__":
    main()
