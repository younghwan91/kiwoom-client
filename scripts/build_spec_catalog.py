"""키움 공식 REST API 명세에서 TR 카탈로그(``src/kiwoom_client/spec/catalog.json``)를 만든다.

원천: 키움증권 공식 GitHub 저장소 ``Kiwoom-Securities/Kiwoom-REST-API`` 의
``kiwoom/_data/kiwoom_api_spec.json`` (키움 REST API 포털 https://openapi.kiwoom.com 의
"API 명세서 다운로드"와 같은 내용, 공식 kwcli·kiwoom-spec-mcp 가 번들하는 파일).
원본 파일은 레포에 넣지 않는다 — 여기서 사실 정보(필드 ID·한글명·타입·길이·필수 여부·
필드 설명·코드값)만 뽑아 카탈로그로 다시 쓴다. 개요 문장·요청/응답 예제·오류 메시지는 버린다.

재현 (레포 루트, 네트워크 필요 — 키움 API 서버가 아니라 GitHub 에서 문서 파일만 받는다):

    uv run python scripts/build_spec_catalog.py --download            # SOURCE_COMMIT 고정본
    uv run python scripts/build_spec_catalog.py --source path/to/kiwoom_api_spec.json

새 명세로 올릴 때는 ``SOURCE_COMMIT`` 을 공식 저장소의 새 커밋으로 바꾸고 다시 돌린 뒤
``git diff src/kiwoom_client/spec/catalog.json`` 을 검토한다.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
import urllib.request
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "src" / "kiwoom_client" / "spec" / "catalog.json"
SUPPLEMENT = Path(__file__).resolve().parent / "spec_supplement.json"

SOURCE_REPO = "Kiwoom-Securities/Kiwoom-REST-API"
SOURCE_PATH = "kiwoom/_data/kiwoom_api_spec.json"
#: 공식 저장소 main 의 고정 커밋 (2026-11-05 push). 올릴 때 여기만 바꾼다.
SOURCE_COMMIT = "c7a3d25449ed4b4238bef378780c41103c67b9e9"

#: 카탈로그에 넣는 메뉴 최상위 구분. 미국주식은 이 라이브러리가 감싸지 않아 뺀다.
MARKETS = ("국내주식", "OAuth 인증")

SCHEMA_VERSION = 1

_TYPES = {"string": "string", "list": "list", "list<map>": "list", "object": "object", "": "string"}

# "0:보통 , 3:시장가" · "Y:연속조회요청,N:연속조회미요청" · "1:KRX, 2:NXT 3.통합" 꼴의 코드값.
# 코드는 영숫자 1~6자, 앞은 줄머리·쉼표·공백·괄호, 뒤는 ':' (전각 포함) 또는 "3.통합" 의 '.'.
_CODE = re.compile(
    r"(?:^|(?<=[\s,(/]))(?:([A-Za-z0-9%]{1,6})\s*[:\uff1a]\s*|(\d{1,2})\.(?=[가-힣]))"
)
# "코스피:0, 코스닥:1" · "당일 : 1, 전일 : 2" 처럼 뜻이 앞에 오는 꼴.
_REVERSED = re.compile(r"^\s*([^:,]+?)\s*:\s*([A-Za-z0-9]{1,12})\s*$")
# "KRX:039490,NXT:039490_NX" 처럼 뜻 자리에 예시값만 있으면 코드표가 아니다.
_EXAMPLE_ONLY = re.compile(r"^[0-9A-Z_]+\)?$")


def parse_codes(desc: str) -> dict[str, str]:
    """필드 설명에서 ``코드: 뜻`` 목록을 뽑는다.

    휴리스틱이라 틀릴 수 있다 — 원문 ``desc`` 를 같이 남기고, 검증은 코드값을 강제하지 않는다.
    """
    text = desc.replace("\n", " ").strip()
    tokens = [t for t in (x.strip() for x in text.split(",")) if t]
    code_first = re.match(r"^[A-Za-z0-9]{1,6}\s*:", text)
    if tokens and not code_first and all(_REVERSED.match(t) for t in tokens):
        reversed_codes: dict[str, str] = {}
        for t in tokens:
            m = _REVERSED.match(t)
            assert m is not None
            reversed_codes.setdefault(m.group(2), m.group(1))
        return reversed_codes
    matches = list(_CODE.finditer(text))
    # 코드 하나짜리는 설명 전체가 "코드:뜻" 일 때만 (예: "0:조건검색", "K:KRX").
    if not matches or (len(matches) == 1 and matches[0].start() != 0):
        return {}
    codes: dict[str, str] = {}
    for i, m in enumerate(matches):
        end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
        label = text[m.end():end].strip().strip(",").strip()
        code = m.group(1) or m.group(2)
        # 시각("09:00")처럼 보이는 것은 코드값이 아니다.
        if not label or (re.fullmatch(r"\d{2}", code) and re.match(r"\d{2}\b", label)):
            return {}
        codes.setdefault(code, label)
    if all(_EXAMPLE_ONLY.match(v) for v in codes.values()):
        return {}
    return codes


def _clean(text: str) -> str:
    return re.sub(r"[ \t]*\n[ \t]*", "\n", text).strip()


def _length(raw: str) -> int | None:
    raw = (raw or "").strip()
    return int(raw) if raw.isdigit() else None


def convert_fields(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """명세의 body 행 목록 → 카탈로그 필드 목록 (LIST 자식은 ``parent`` 로 잇는다)."""
    out: list[dict[str, Any]] = []
    parents: dict[int, str] = {}
    for row in rows:
        if row.get("is_section"):
            continue
        field_id = row["element"].strip()
        depth = int(row.get("depth") or 0)
        ftype = _TYPES.get(row.get("type", "").strip().lower(), "string")
        field: dict[str, Any] = {"id": field_id, "name": row.get("한글명", "").strip()}
        field["type"] = ftype
        length = _length(row.get("length", ""))
        if length is not None:
            field["length"] = length
        field["required"] = row.get("required", "").strip().upper() == "Y"
        desc = _clean(row.get("description", ""))
        if desc:
            field["desc"] = desc
            codes = parse_codes(desc)
            if codes:
                field["codes"] = codes
        if depth > 0 and depth - 1 in parents:
            field["parent"] = parents[depth - 1]
        if ftype == "list":
            parents[depth] = field_id
        out.append(field)
    return out


def _menu(path: str) -> list[str]:
    # "국내주식 > 종목정보 > 주식기본정보요청(ka10001)" → ["국내주식", "종목정보"]
    return [p.strip() for p in path.split(">")][:-1]


def convert(spec: dict[str, Any]) -> dict[str, dict[str, Any]]:
    trs: dict[str, dict[str, Any]] = {}
    for entry in spec["apis"].values():
        meta = entry["meta"]
        menu = _menu(meta.get("메뉴 위치", ""))
        if not menu or menu[0] not in MARKETS:
            continue
        api_id = meta["API ID"].strip()
        url = meta.get("URL", "").strip()
        trs[api_id] = {
            "api_id": api_id,
            "name": meta.get("API 명", "").strip(),
            "menu": menu,
            "method": meta.get("Method", "POST").strip(),
            "url": url,
            "transport": "websocket" if url.endswith("/websocket") else "rest",
            "source": "official",
            "request": convert_fields(entry.get("request", {}).get("body", [])),
            "response": convert_fields(entry.get("response", {}).get("body", [])),
        }
    return trs


def load_source(args: argparse.Namespace) -> dict[str, Any]:
    if args.source:
        return json.loads(Path(args.source).read_text(encoding="utf-8"))
    url = f"https://raw.githubusercontent.com/{SOURCE_REPO}/{SOURCE_COMMIT}/{SOURCE_PATH}"
    with urllib.request.urlopen(url, timeout=60) as resp:
        return json.loads(resp.read().decode("utf-8"))


def build(spec: dict[str, Any]) -> dict[str, Any]:
    trs = convert(spec)
    supplement = json.loads(SUPPLEMENT.read_text(encoding="utf-8"))
    for api_id, tr in supplement["trs"].items():
        if api_id in trs:
            raise SystemExit(f"{api_id} 는 이제 공식 명세에 있다 — spec_supplement.json 에서 뺄 것")
        trs[api_id] = tr
    return {
        "schema_version": SCHEMA_VERSION,
        "source": {
            "repository": f"https://github.com/{SOURCE_REPO}",
            "path": SOURCE_PATH,
            "commit": SOURCE_COMMIT,
            "portal": "https://openapi.kiwoom.com",
        },
        "trs": dict(sorted(trs.items())),
    }


def render(catalog: dict[str, Any]) -> str:
    # TR 하나가 한 줄 — diff 를 TR 단위로 읽을 수 있고 파일도 작다.
    lines = ["{"]
    lines.append(f'"schema_version": {catalog["schema_version"]},')
    lines.append(f'"source": {json.dumps(catalog["source"], ensure_ascii=False)},')
    lines.append('"trs": {')
    items = list(catalog["trs"].items())
    for i, (api_id, tr) in enumerate(items):
        comma = "," if i + 1 < len(items) else ""
        body = json.dumps(tr, ensure_ascii=False, separators=(",", ":"))
        lines.append(f"{json.dumps(api_id)}: {body}{comma}")
    lines.append("}")
    lines.append("}")
    return "\n".join(lines) + "\n"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--source", help="이미 받아 둔 kiwoom_api_spec.json 경로")
    group.add_argument("--download", action="store_true", help="SOURCE_COMMIT 고정본을 받는다")
    parser.add_argument("--out", default=str(OUT))
    args = parser.parse_args(argv)

    catalog = build(load_source(args))
    Path(args.out).write_text(render(catalog), encoding="utf-8")
    n_fields = sum(len(t["request"]) + len(t["response"]) for t in catalog["trs"].values())
    print(f"{len(catalog['trs'])} TR, 필드 {n_fields}개 → {args.out}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
