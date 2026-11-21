"""자주 쓰는 TR 의 응답 TypedDict (``src/kiwoom_client/spec/responses.py``) 를 카탈로그로 만든다.

실행 (레포 루트):

    uv run python scripts/build_response_types.py          # 다시 쓴다
    uv run python scripts/build_response_types.py --check  # 다르면 1 (tests/test_response_types.py)

TR 을 더하려면 ``SELECTED`` 에 api_id 를 넣고 다시 돌린다. 클래스 이름은 메서드 이름에서 온다
(``stock_daily_chart`` → ``StockDailyChartResponse``, 목록 한 줄은 ``StockDailyChartItem``).
"""

from __future__ import annotations

import argparse
import keyword
import sys
from pathlib import Path

from kiwoom_client import spec

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "src" / "kiwoom_client" / "spec" / "responses.py"

#: 실사용(예제·소비자 코드)에서 가장 많이 부르는 TR.
SELECTED = (
    "ka10001",  # 주식기본정보
    "ka10004",  # 주식호가
    "ka10080",  # 분봉
    "ka10081",  # 일봉
    "ka10030",  # 당일거래량상위
    "kt00001",  # 예수금상세
    "kt00004",  # 계좌평가현황
    "kt00018",  # 계좌평가잔고내역
    "ka10075",  # 미체결
    "kt10000",  # 매수주문 (매도·정정·취소 응답도 같은 모양)
)

HEADER = '''"""자주 쓰는 TR 의 응답 TypedDict — ``cast`` 해서 IDE 자동완성·mypy 를 받는다.

자동 생성 — 고치지 말 것. ``scripts/build_response_types.py`` 가 TR 카탈로그로 만든다.

엔드포인트 메서드의 반환 타입은 그대로 ``dict[str, Any]`` 다 (응답에 필드가 빠지거나 더해질 수
있어서). 필요한 곳에서만 좁혀 쓴다::

    from typing import cast
    from kiwoom_client.spec.responses import StockDailyChartResponse

    resp = cast(StockDailyChartResponse, api.chart.stock_daily_chart(stk_cd="005930"))
    for bar in resp.get("stk_dt_pole_chart_qry", []):
        bar["cur_prc"]   # str — 숫자는 kiwoom_client.to_number() 로

모든 키는 선택(``total=False``)이고 값은 키움이 보내는 그대로 문자열이다
(``return_code`` 만 정수). 키 이름이 숫자로 시작하는 필드가 있어 함수형 문법을 쓴다.
"""

from __future__ import annotations

from typing import TypedDict
'''


def _camel(name: str) -> str:
    return "".join(part.capitalize() for part in name.split("_"))


def _typed_dict(name: str, doc: str, fields: list[tuple[str, str, str]]) -> str:
    """키가 모두 식별자면 클래스 문법(독스트링 포함), 아니면 함수형 문법 (ruff UP013)."""
    q = '"""'
    if all(fid.isidentifier() and not keyword.iskeyword(fid) for fid, _, _ in fields):
        body = "".join(f"    {fid}: {ftype}\n    {q}{label}{q}\n" for fid, ftype, label in fields)
        return f"class {name}(TypedDict, total=False):\n    {q}{doc}{q}\n\n{body}\n\n"
    body = "".join(f'        "{fid}": {ftype},  # {label}\n' for fid, ftype, label in fields)
    head = f'# {doc}\n{name} = TypedDict(\n    "{name}",\n    {{\n'
    return f"{head}{body}    }},\n    total=False,\n)\n\n\n"


def render() -> str:
    out = [HEADER, "\n"]
    exported: list[str] = []
    for api_id in SELECTED:
        tr = spec.get(api_id)
        where = spec.method_for(api_id)
        assert where is not None, api_id
        base = _camel(where[1])
        lists = [f for f in tr.response if f.type == "list"]
        if len(lists) > 1:
            raise SystemExit(f"{api_id}: 목록이 둘 이상 — 이름 규칙을 넓힐 것")
        item_name = f"{base}Item"
        if lists:
            children = [(f.id, "str", f.name) for f in tr.response if f.parent == lists[0].id]
            doc = f"{api_id} {tr.name} — ``{lists[0].id}`` 목록의 한 줄."
            out.append(_typed_dict(item_name, doc, children))
            exported.append(item_name)
        name = f"{base}Response"
        fields = [
            ("return_code", "int", "결과코드 (0 = 정상)"),
            ("return_msg", "str", "결과메시지"),
        ]
        for f in tr.response:
            if f.parent is None:
                ftype = f"list[{item_name}]" if f.type == "list" else "str"
                fields.append((f.id, ftype, f.name))
        doc = f"{api_id} {tr.name} — ``api.{where[0]}.{where[1]}()`` 응답."
        out.append(_typed_dict(name, doc, fields))
        exported.append(name)
    out.append("__all__ = [\n" + "".join(f'    "{n}",\n' for n in sorted(exported)) + "]\n")
    return "".join(out)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args(argv)
    text = render()
    current = OUT.read_text(encoding="utf-8") if OUT.exists() else None
    if args.check:
        if current != text:
            print("responses.py 가 카탈로그와 다르다 — build_response_types.py", file=sys.stderr)
            return 1
        return 0
    OUT.write_text(text, encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
