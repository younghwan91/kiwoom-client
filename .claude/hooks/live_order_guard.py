#!/usr/bin/env python3
"""PreToolUse(Bash) 가드 — 에이전트가 실계좌로 주문·토큰 폐기를 실행하지 못하게 한다.

왜: 이 PC 에 있는 키움 키(~/git/quant-airflow/.env)는 실전투자용이고, 같은 앱키로 데몬이 돈다.
`KiwoomAPI(...)` 기본값은 `is_mock=False`(실서버)라 키를 불러 `api.order.buy_order(...)` 를 부르면
그대로 실주문이 나간다. 라이브러리 가드(`KIWOOM_MCP_ALLOW_LIVE_ORDERS`)는 MCP 경로에만 있다.

막는 것: 코드를 실행하는 Bash 명령 중, 명령 본문이나 명령이 가리키는 .py 파일에
  (1) 주문 식별자(buy/sell/modify/cancel 주문 메서드, kt10000~kt10009, /api/dostk/(crd)ordr) 또는
      토큰 폐기(logout(, revoke_token, /oauth2/revoke) 가 있고
  (2) 키를 불러오는 흔적(.env·--env-file·KIWOOM_APP_KEY) 이 있는 경우.
그리고 MCP 실주문 opt-in(KIWOOM_MCP_ALLOW_LIVE_ORDERS=true) 을 켜는 명령.
pytest 단위 테스트(pytest-httpx 목)는 키를 불러오지 않으니 걸리지 않는다.

bypass 모드에서도 PreToolUse 의 deny 는 먹힌다. 오류가 나면 조용히 통과한다.
"""

from __future__ import annotations

import json
import os
import re
import sys

ORDER = re.compile(
    r"\b(?:(?:gold_spot_|margin_)?(?:buy|sell|modify|cancel)_order)\b"
    r"|\bkt1000[0-9]\b|/api/dostk/(?:crd)?ordr\b"
    r"|\blogout\s*\(|\brevoke_token\b|/oauth2/revoke\b"
)
CREDS = re.compile(r"\.env\b|--env-file|KIWOOM_APP_KEY|KIWOOM_APP_SECRET")
EXECS = re.compile(r"\b(?:python3?|ipython|uv\s+run|uvx|pytest|kiwoom-client-mcp|curl|wget|http|httpie)\b")
# opt-in 을 '켜는' 위치만: 명령 앞 환경변수 대입이나 export. grep 패턴·커밋 메시지·문서 heredoc 은 아님.
MCP_LIVE = re.compile(r"(?:^|[;&|\n(]\s*|\bexport\s+|\benv\s+)(?:[A-Za-z_]\w*=\S*\s+)*KIWOOM_MCP_ALLOW_LIVE_ORDERS=['\"]?true", re.I)
HEREDOC = re.compile(r"<<-?\s*(['\"]?)(\w+)\1[^\n]*\n(.*?)\n\2(?:\n|$)", re.S)
PYFILE = re.compile(r"(?:^|[\s'\"=])([\w./~-]+\.py)\b")

HOW = (
    " 실주문·토큰 폐기는 사용자만 한다 — 명령을 보여주고 사용자가 직접 `! <명령>` 으로 실행하게 하라."
    " 개발·검증은 pytest-httpx 목(단위 테스트)이나 조회 전용 스모크(주문 제외)로."
)


def deny(reason: str) -> None:
    print(json.dumps({"hookSpecificOutput": {
        "hookEventName": "PreToolUse",
        "permissionDecision": "deny",
        "permissionDecisionReason": "[kiwoom live-order guard] " + reason + HOW,
    }}, ensure_ascii=False))
    sys.exit(0)


def strip_docs(cmd: str) -> str:
    """따옴표 안 글자와 파일에 쓰는 heredoc 본문을 지운다 — 명령이 아니라 글이다."""
    cmd = HEREDOC.sub(lambda m: "" if not re.search(r"\b(?:bash|sh|python3?|uv\s+run)\b[^\n]*$", cmd[: m.start()].split("\n")[-1]) else m.group(0), cmd)
    return re.sub(r"'[^']*'|\"[^\"]*\"", "''", cmd)


def script_text(cmd: str, cwd: str) -> str:
    """명령이 가리키는 .py 파일 내용. 상대 경로는 cwd 와 명령 안의 `cd <dir>` 기준 둘 다로 푼다."""
    bases = [cwd] + [os.path.join(cwd, os.path.expanduser(d)) for d in re.findall(r"\bcd\s+([^\s;&|]+)", cmd)]
    out = []
    for m in PYFILE.finditer(cmd):
        rel = os.path.expanduser(m.group(1))
        for base in ([""] if os.path.isabs(rel) else bases):
            p = os.path.join(base, rel)
            try:
                if os.path.isfile(p) and os.path.getsize(p) < 2_000_000:
                    with open(p, encoding="utf-8", errors="ignore") as f:
                        out.append(f.read())
                    break
            except OSError:
                pass
    return "\n".join(out)


def main() -> None:
    data = json.load(sys.stdin)
    if data.get("tool_name") != "Bash":
        return
    cmd = (data.get("tool_input") or {}).get("command") or ""
    if MCP_LIVE.search(strip_docs(cmd)):
        deny("MCP 실주문 opt-in(KIWOOM_MCP_ALLOW_LIVE_ORDERS=true)을 켜는 명령.")
    if not EXECS.search(cmd):
        return
    cwd = data.get("cwd") or os.getcwd()
    text = cmd + "\n" + script_text(cmd, cwd)
    m = ORDER.search(text)
    if m and CREDS.search(text):
        deny(f"실계좌 키를 불러 주문/토큰 폐기({m.group(0)})를 실행할 수 있는 명령.")


if __name__ == "__main__":
    try:
        main()
    except SystemExit:
        raise
    except Exception:
        pass
