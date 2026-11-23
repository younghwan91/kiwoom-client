"""``market_movers`` — today's top stocks by volume, gain, loss, value or volume spike.

One readable call over the ranking TRs, with request codes filled in from
the Kiwoom spec (KRX, 관리종목 제외, no price/volume floor unless noted):

- ``volume``       ka10030 당일거래량상위 (sort 1 거래량)
- ``gainers``      ka10027 전일대비등락률상위 (sort 1 상승률)
- ``losers``       ka10027 전일대비등락률상위 (sort 3 하락률)
- ``value``        ka10032 거래대금상위
- ``volume_spike`` ka10023 거래량급증 (전일 대비 급증률, 1만주 이상)
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from kiwoom_client.mcp.intents.common import fetch_rows
from kiwoom_client.mcp.intents.limits import count_schema, row_count
from kiwoom_client.mcp.intents.normalize import num, pct, pick, price, stock_code, text
from kiwoom_client.mcp.intents.registry import IntentContext, read_only_tool, register
from kiwoom_client.mcp.local_tools import LocalTool

#: market argument → ranking mrkt_tp
MARKETS: dict[str, str] = {"all": "000", "kospi": "001", "kosdaq": "101"}

#: ranking stex_tp: 1 KRX.
_KRX = "1"

_COMMON: dict[str, tuple[str, Any]] = {
    "code": ("stk_cd", stock_code),
    "name": ("stk_nm", text),
    "price": ("cur_prc", price),
    "change": ("pred_pre", num),
    "change_pct": ("flu_rt", pct),
}


@dataclass(frozen=True)
class Kind:
    method: str
    source: str
    key: str
    params: dict[str, str]
    fields: dict[str, tuple[str, Any]]


KINDS: dict[str, Kind] = {
    "volume": Kind(
        method="top_volume_today",
        source="ka10030 당일거래량상위요청",
        key="tdy_trde_qty_upper",
        params={
            "sort_tp": "1", "mang_stk_incls": "1", "crd_tp": "0", "trde_qty_tp": "0",
            "pric_tp": "0", "trde_prica_tp": "0", "mrkt_open_tp": "0", "stex_tp": _KRX,
        },
        fields={
            **_COMMON,
            "volume": ("trde_qty", price),
            "volume_vs_prev_day_pct": ("pred_rt", pct),
            "turnover_pct": ("trde_tern_rt", pct),
            "trade_value_million_krw": ("trde_amt", num),
        },
    ),
    "gainers": Kind(
        method="top_change_rate",
        source="ka10027 전일대비등락률상위요청 (상승률)",
        key="pred_pre_flu_rt_upper",
        params={
            "sort_tp": "1", "trde_qty_cnd": "0000", "stk_cnd": "1", "crd_cnd": "0",
            "updown_incls": "1", "pric_cnd": "0", "trde_prica_cnd": "0", "stex_tp": _KRX,
        },
        fields={**_COMMON, "volume": ("now_trde_qty", price), "strength_pct": ("cntr_str", pct)},
    ),
    "losers": Kind(
        method="top_change_rate",
        source="ka10027 전일대비등락률상위요청 (하락률)",
        key="pred_pre_flu_rt_upper",
        params={
            "sort_tp": "3", "trde_qty_cnd": "0000", "stk_cnd": "1", "crd_cnd": "0",
            "updown_incls": "1", "pric_cnd": "0", "trde_prica_cnd": "0", "stex_tp": _KRX,
        },
        fields={**_COMMON, "volume": ("now_trde_qty", price), "strength_pct": ("cntr_str", pct)},
    ),
    "value": Kind(
        method="top_trading_value",
        source="ka10032 거래대금상위요청",
        key="trde_prica_upper",
        params={"mang_stk_incls": "0", "stex_tp": _KRX},
        fields={
            **_COMMON,
            "trade_value_million_krw": ("trde_prica", num),
            "volume": ("now_trde_qty", price),
            "prev_day_volume": ("pred_trde_qty", price),
            "prev_day_rank": ("pred_rank", num),
        },
    ),
    "volume_spike": Kind(
        method="sudden_volume_increase",
        source="ka10023 거래량급증요청 (전일 대비 급증률)",
        key="trde_qty_sdnin",
        params={
            "sort_tp": "2", "tm_tp": "2", "trde_qty_tp": "10", "stk_cnd": "1",
            "pric_tp": "0", "stex_tp": _KRX,
        },
        fields={
            **_COMMON,
            "volume": ("now_trde_qty", price),
            "prev_volume": ("prev_trde_qty", price),
            "spike_qty": ("sdnin_qty", num),
            "spike_pct": ("sdnin_rt", pct),
        },
    ),
}  # fmt: skip

DEFAULT_COUNT = 20
MAX_COUNT = 100


async def market_movers(
    api: Any, kind: str = "volume", market: str = "all", count: Any = None
) -> dict[str, Any]:
    kind = str(kind or "volume").strip().lower()
    market = str(market or "all").strip().lower()
    if kind not in KINDS:
        raise ValueError(f"kind 는 {', '.join(KINDS)} 중 하나여야 합니다: {kind!r}")
    if market not in MARKETS:
        raise ValueError(f"market 은 {', '.join(MARKETS)} 중 하나여야 합니다: {market!r}")
    want = row_count(count, default=DEFAULT_COUNT, maximum=MAX_COUNT)
    spec = KINDS[kind]
    method = getattr(api.ranking, spec.method)
    params = {"mrkt_tp": MARKETS[market], **spec.params}
    _first, records = await fetch_rows(method, spec.key, params, want=want, max_pages=3)
    rows = [{"rank": i, **pick(r, spec.fields)} for i, r in enumerate(records[:want], start=1)]
    return {"kind": kind, "market": market, "source": spec.source, "count": len(rows), "rows": rows}


@register
def mover_tools(_context: IntentContext) -> list[LocalTool]:
    async def handler(api: Any, arguments: dict[str, Any]) -> dict[str, Any]:
        return await market_movers(
            api,
            kind=str(arguments.get("kind") or "volume"),
            market=str(arguments.get("market") or "all"),
            count=arguments.get("count"),
        )

    return [
        read_only_tool(
            name="market_movers",
            title="오늘의 상위 종목 (거래량·상승·하락·거래대금·급증)",
            description=(
                "오늘 시장의 상위 종목을 순위·현재가·등락률·거래량과 함께 돌려준다. kind: volume "
                "거래량, gainers 상승률, losers 하락률, value 거래대금, volume_spike 전일 대비 "
                "거래량 급증률. 'KRX, 관리종목 제외' 기준. '오늘 뭐가 많이 올랐어?' 같은 "
                "질문에 쓴다."
            ),
            properties={
                "kind": {"type": "string", "enum": list(KINDS), "default": "volume"},
                "market": {"type": "string", "enum": list(MARKETS), "default": "all"},
                "count": count_schema(DEFAULT_COUNT, MAX_COUNT),
            },
            toolset="ranking",
            handler=handler,
            example={"kind": "gainers", "market": "kosdaq", "count": 10},
        )
    ]
