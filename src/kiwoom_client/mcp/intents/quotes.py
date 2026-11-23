"""``get_quotes`` — current price, change, volume and market cap for many stocks.

One ka10095 (관심종목정보요청) call takes up to 20 codes joined by ``|``, so
a watchlist costs one request instead of one per stock. Names are resolved
first; a name that can't be resolved, or a code Kiwoom doesn't return,
becomes an ``error`` entry for that stock while the others still answer.
"""

from __future__ import annotations

from collections.abc import Sequence
from typing import Any

from kiwoom_client.mcp.intents.normalize import num, pct, pick, price, stock_code, text
from kiwoom_client.mcp.intents.registry import IntentContext, read_only_tool, register
from kiwoom_client.mcp.intents.resolve import resolve_stock
from kiwoom_client.mcp.local_tools import LocalTool

MAX_STOCKS = 20
SOURCE = "ka10095 관심종목정보요청"

#: ka10095 ``atn_stk_infr`` row → quote. Units per the Kiwoom spec:
#: 거래대금 백만원, 시가총액 억원.
QUOTE_FIELDS: dict[str, tuple[str, Any]] = {
    "name": ("stk_nm", text),
    "price": ("cur_prc", price),
    "change": ("pred_pre", num),
    "change_pct": ("flu_rt", pct),
    "volume": ("trde_qty", price),
    "trade_value_million_krw": ("trde_prica", num),
    "market_cap_100m_krw": ("mac", num),
    "open": ("open_pric", price),
    "high": ("high_pric", price),
    "low": ("low_pric", price),
    "base_price": ("base_pric", price),
    "upper_limit": ("upl_pric", price),
    "lower_limit": ("lst_pric", price),
}


def parse_stock_list(value: Any) -> list[str]:
    """``["삼성전자", "000660"]`` or ``"삼성전자, 000660"`` → list of non-blank strings."""
    if value is None:
        return []
    items = value.split(",") if isinstance(value, str) else list(value)
    return [str(item).strip() for item in items if str(item).strip()]


async def fetch_quotes(api: Any, codes: Sequence[str]) -> dict[str, dict[str, Any]]:
    """Quotes for ``codes`` (at most :data:`MAX_STOCKS`), keyed by plain code.

    Codes Kiwoom doesn't return are simply absent from the result.
    """
    unique = list(dict.fromkeys(codes))
    if not unique:
        return {}
    if len(unique) > MAX_STOCKS:
        raise ValueError(f"한 번에 {MAX_STOCKS}종목까지 조회합니다 (받은 수: {len(unique)})")
    resp = await api.stock_info.watchlist_stock_info(stk_cd="|".join(unique))
    quotes: dict[str, dict[str, Any]] = {}
    for row in resp.get("atn_stk_infr") or []:
        if not isinstance(row, dict):
            continue
        code = stock_code(row.get("stk_cd"))
        if code:
            quotes[code] = {"code": code, **pick(row, QUOTE_FIELDS)}
    return quotes


async def get_quotes(api: Any, stocks: Any) -> dict[str, Any]:
    queries = parse_stock_list(stocks)
    if not queries:
        raise ValueError("stocks(종목명 또는 코드 목록)이 필요합니다")
    if len(queries) > MAX_STOCKS:
        raise ValueError(f"한 번에 {MAX_STOCKS}종목까지 조회합니다 (받은 수: {len(queries)})")

    # Sequential on purpose: the first name lookup fills the listing cache,
    # the rest reuse it instead of each fetching the listing again.
    resolved: list[tuple[str, str | None, str | None]] = []  # (query, code, error)
    for query in queries:
        try:
            stock = await resolve_stock(api, query)
        except ValueError as exc:
            resolved.append((query, None, str(exc)))
        else:
            resolved.append((query, stock.code, None))

    quotes = await fetch_quotes(api, [code for _, code, _ in resolved if code])
    rows: list[dict[str, Any]] = []
    for query, code, error in resolved:
        if code is None:
            rows.append({"query": query, "error": error})
        elif code in quotes:
            rows.append(quotes[code])
        else:
            rows.append({"query": query, "code": code, "error": "키움 응답에 이 종목이 없습니다"})
    failed = sum(1 for row in rows if "error" in row)
    return {"source": SOURCE, "requested": len(queries), "failed": failed, "quotes": rows}


@register
def quote_tools(_context: IntentContext) -> list[LocalTool]:
    async def handler(api: Any, arguments: dict[str, Any]) -> dict[str, Any]:
        return await get_quotes(api, arguments.get("stocks"))

    return [
        read_only_tool(
            name="get_quotes",
            title="여러 종목 시세 한 번에",
            description=(
                f"여러 종목(최대 {MAX_STOCKS}개)의 현재가·전일대비·등락률·거래량·"
                "거래대금(백만원)·시가총액(억원)·시고저를 요청 한 번으로 돌려준다(ka10095). "
                "관심종목·보유종목 시세를 한꺼번에 볼 때 쓴다. 찾지 못한 종목은 그 종목만 "
                "error 로 표시한다."
            ),
            properties={
                "stocks": {
                    "type": "array",
                    "items": {"type": "string"},
                    "maxItems": MAX_STOCKS,
                    "description": "종목명 또는 종목코드 목록 (예: ['삼성전자', '000660'])",
                }
            },
            required=("stocks",),
            toolset="stock_info",
            handler=handler,
            example={"stocks": ["삼성전자", "000660"]},
        )
    ]
