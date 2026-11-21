"""Kiwoom order code values the MCP helpers need to understand.

The codes are the members of :class:`kiwoom_client.codes.OrderType` /
:class:`~kiwoom_client.codes.StockListMarket`; the short Korean labels are this
package's own (the TR catalog keeps no code lists — see ``spec/SOURCE.md``).
Tests check that every enum member has a label and vice versa. The price
classification below is this package's own reading of those codes. The
official guide is authoritative: https://openapi.kiwoom.com
"""

from __future__ import annotations

from kiwoom_client.codes import OrderType, StockListMarket

#: 매매구분 (``trde_tp``) for stock orders (kt10000-kt10003), code → 한글명.
TRADE_TYPES: dict[str, str] = {
    OrderType.LIMIT.value: "보통",
    OrderType.MARKET.value: "시장가",
    OrderType.CONDITIONAL_LIMIT.value: "조건부지정가",
    OrderType.POST_MARKET.value: "장마감후시간외",
    OrderType.PRE_MARKET.value: "장시작전시간외",
    OrderType.AFTER_HOURS_SINGLE.value: "시간외단일가",
    OrderType.BEST_LIMIT.value: "최유리지정가",
    OrderType.FIRST_LIMIT.value: "최우선지정가",
    OrderType.LIMIT_IOC.value: "보통(IOC)",
    OrderType.MARKET_IOC.value: "시장가(IOC)",
    OrderType.BEST_IOC.value: "최유리(IOC)",
    OrderType.LIMIT_FOK.value: "보통(FOK)",
    OrderType.MARKET_FOK.value: "시장가(FOK)",
    OrderType.BEST_FOK.value: "최유리(FOK)",
    OrderType.STOP_LIMIT.value: "스톱지정가",
    OrderType.MID_PRICE.value: "중간가",
    OrderType.MID_PRICE_IOC.value: "중간가(IOC)",
    OrderType.MID_PRICE_FOK.value: "중간가(FOK)",
}

#: 시장구분 (``mrkt_tp``) for 종목정보 리스트 (ka10099), code → 한글명.
STOCK_LIST_MARKETS: dict[str, str] = {
    StockListMarket.KOSPI.value: "코스피",
    StockListMarket.KOSDAQ.value: "코스닥",
    StockListMarket.K_OTC.value: "K-OTC",
    StockListMarket.KONEX.value: "코넥스",
    StockListMarket.ETN.value: "ETN",
    StockListMarket.LOSS_LIMITED_ETN.value: "손실제한 ETN",
    StockListMarket.GOLD_SPOT.value: "금현물",
    StockListMarket.VOLATILITY_ETN.value: "변동성 ETN",
    StockListMarket.INFRA_FUND.value: "인프라투융자",
    StockListMarket.ELW.value: "ELW",
    StockListMarket.MUTUAL_FUND.value: "뮤추얼펀드",
    StockListMarket.WARRANT.value: "신주인수권",
    StockListMarket.REIT.value: "리츠종목",
    StockListMarket.WARRANT_CERTIFICATE.value: "신주인수권증서",
    StockListMarket.ETF.value: "ETF",
    StockListMarket.HIGH_YIELD_FUND.value: "하이일드펀드",
}

#: trde_tp values that carry a limit price in ``ord_uv``.
LIMIT_PRICE_TRADE_TYPES: frozenset[str] = frozenset({"0", "5", "10", "20", "28", "62"})

#: trde_tp values priced by the exchange — ``ord_uv`` is left empty.
NO_PRICE_TRADE_TYPES: frozenset[str] = frozenset(
    {"3", "13", "23", "6", "16", "26", "7", "61", "81"}
)

#: 국내거래소구분 (``dmst_stex_tp``), code → 이름.
EXCHANGES: dict[str, str] = {
    "KRX": "한국거래소",
    "NXT": "넥스트트레이드",
    "SOR": "최선주문집행(SOR)",
}
