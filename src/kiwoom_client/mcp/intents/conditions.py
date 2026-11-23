"""``condition_search_run`` — run a saved condition (조건검색식) by name or number.

The raw condition tools need two calls and a ``seq`` the person never sees
(they know the name they gave the condition in 영웅문4). This lists the
conditions (CNSRLST, ka10171), picks the one meant, runs it once (CNSRREQ,
ka10172, ``search_type=0``) following ``cont_yn``/``next_key`` up to
``count`` rows, and returns codes, names and prices as numbers.
"""

from __future__ import annotations

from typing import Any

from kiwoom_client.base import KiwoomAPIError
from kiwoom_client.domestic.condition_search import ConditionSearch
from kiwoom_client.mcp.intents.limits import count_schema, row_count
from kiwoom_client.mcp.intents.normalize import num, pct, pick, price, stock_code, text
from kiwoom_client.mcp.intents.registry import IntentContext, read_only_tool, register
from kiwoom_client.mcp.local_tools import LocalTool

SOURCE = "ka10172 조건검색 요청 일반 (CNSRREQ)"
DEFAULT_COUNT = 50
MAX_COUNT = 300
MAX_PAGES = 10

#: CNSRREQ ``data`` row → result row (field ids from the ka10172 spec).
ROW_FIELDS: dict[str, tuple[str, Any]] = {
    "code": ("9001", stock_code),
    "name": ("302", text),
    "price": ("10", price),
    "change": ("11", num),
    "change_pct": ("12", pct),
    "volume": ("13", price),
    "open": ("16", price),
    "high": ("17", price),
    "low": ("18", price),
}


def _fold(value: Any) -> str:
    return "".join(str(value).split()).casefold()


def parse_condition_list(reply: dict[str, Any]) -> list[dict[str, str]]:
    """CNSRLST ``data`` — ``[["0", "조건1"], ...]`` or ``[{"seq", "name"}]`` — as dicts."""
    out = []
    for entry in reply.get("data") or []:
        if isinstance(entry, dict):
            seq, name = entry.get("seq"), entry.get("name")
        elif isinstance(entry, (list, tuple)) and len(entry) >= 2:
            seq, name = entry[0], entry[1]
        else:
            continue
        if seq not in (None, ""):
            out.append({"seq": str(seq).strip(), "name": str(name or "").strip()})
    return out


def pick_condition(conditions: list[dict[str, str]], query: Any) -> dict[str, str]:
    """By exact seq, then exact name, then a single partial name match.

    Raises:
        ValueError: no condition saved, none matches, or several match.
    """
    wanted = str(query if query is not None else "").strip()
    if not wanted:
        raise ValueError("name_or_seq(조건식 이름 또는 번호)이 필요합니다")
    if not conditions:
        raise ValueError("저장된 조건검색식이 없습니다 — 영웅문4에서 조건식을 만들어 저장하세요")
    for matches in (
        [c for c in conditions if c["seq"] == wanted],
        [c for c in conditions if _fold(c["name"]) == _fold(wanted)],
        [c for c in conditions if _fold(wanted) in _fold(c["name"])],
    ):
        if len(matches) == 1:
            return matches[0]
        if len(matches) > 1:
            listed = ", ".join(f"{c['seq']}:{c['name']}" for c in matches[:10])
            raise ValueError(f"'{wanted}' 에 맞는 조건식이 여러 개입니다 — 번호로 다시: {listed}")
    listed = ", ".join(f"{c['seq']}:{c['name']}" for c in conditions[:20])
    raise ValueError(f"'{wanted}' 조건식을 찾지 못했습니다. 저장된 조건식: {listed}")


def _check(reply: dict[str, Any] | None, trnm: str) -> dict[str, Any]:
    if reply is None:
        raise ValueError(f"{trnm} 응답이 없습니다")
    code = reply.get("return_code", 0)
    if str(code) not in ("0", ""):
        raise KiwoomAPIError(int(num(code) or -1), str(reply.get("return_msg") or trnm), reply)
    return reply


async def condition_search_run(
    session: Any, name_or_seq: Any, *, count: Any = None
) -> dict[str, Any]:
    if session is None:
        raise ValueError("이 서버에는 WebSocket 세션이 없어 조건검색을 할 수 없습니다")
    want = row_count(count, default=DEFAULT_COUNT, maximum=MAX_COUNT)
    builder = ConditionSearch()
    conditions = parse_condition_list(
        _check(await session.request(builder.condition_list()), "CNSRLST")
    )
    chosen = pick_condition(conditions, name_or_seq)

    rows: list[dict[str, Any]] = []
    cont_yn, next_key = "N", ""
    more = False
    for _ in range(MAX_PAGES):
        payload = builder.condition_search(
            seq=chosen["seq"], search_type="0", stex_tp="K", cont_yn=cont_yn, next_key=next_key
        )
        reply = _check(await session.request(payload), "CNSRREQ")
        rows.extend(pick(r, ROW_FIELDS) for r in reply.get("data") or [] if isinstance(r, dict))
        next_key = str(reply.get("next_key") or "")
        more = str(reply.get("cont_yn") or "N").upper() == "Y" and bool(next_key)
        if len(rows) >= want or not more:
            break
        cont_yn = "Y"
    return {
        "condition": chosen,
        "source": SOURCE,
        "count": min(len(rows), want),
        "more_available": more or len(rows) > want,
        "rows": rows[:want],
    }


@register
def condition_tools(context: IntentContext) -> list[LocalTool]:
    async def handler(_api: Any, arguments: dict[str, Any]) -> dict[str, Any]:
        return await condition_search_run(
            context.session, arguments.get("name_or_seq"), count=arguments.get("count")
        )

    return [
        read_only_tool(
            name="condition_search_run",
            title="조건검색 실행 (이름으로)",
            description=(
                "영웅문4에 저장한 조건검색식을 이름(일부도 가능) 또는 번호로 한 번 실행해 걸린 "
                "종목의 코드·이름·현재가·등락률·거래량을 돌려준다(CNSRLST → CNSRREQ, WebSocket). "
                "목록조회·seq 확인을 따로 하지 않아도 된다. 실시간 등록은 하지 않는다."
            ),
            properties={
                "name_or_seq": {
                    "type": "string",
                    "description": "조건식 이름 또는 번호 (예: '급등주', '3')",
                },
                "count": count_schema(DEFAULT_COUNT, MAX_COUNT),
            },
            required=("name_or_seq",),
            toolset="condition_search",
            handler=handler,
            example={"name_or_seq": "급등주"},
        )
    ]
