"""Named constants for Kiwoom's coded request/response fields.

Kiwoom encodes options as short strings — ``trde_tp="3"`` is a market order,
``stex_tp="3"`` means "KRX+NXT combined", ``mrkt_tp="101"`` is KOSDAQ — and the
same field name means different things in different TRs. These enums give the
common ones a name so a typo becomes an ``AttributeError`` instead of a
rejected (or worse, accepted) order.

Every member is a ``str``, so it can be passed straight into any endpoint::

    from kiwoom_client.codes import Exchange, OrderType

    api.order.buy_order(
        dmst_stex_tp=Exchange.KRX, stk_cd="005930", ord_qty="10",
        ord_uv="70000", trde_tp=OrderType.LIMIT,
    )

Only values stated in Kiwoom's official API spec are included, and each enum
lists the TRs it was checked against. A field whose codes differ per TR
(``mrkt_tp`` comes in at least five dialects) gets one enum per dialect.

Sources:
    - 키움 REST API 가이드: https://openapi.kiwoom.com/guide/apiguide
    - 키움 공식 스펙 번들:
      https://github.com/Kiwoom-Securities/Kiwoom-REST-API (``kiwoom/_data/kiwoom_api_spec.json``)
"""

from __future__ import annotations

from enum import Enum

__all__ = [
    "AdjustedPrice",
    "Exchange",
    "Market",
    "OrderType",
    "PriceChangeSign",
    "QueryExchange",
    "StockListMarket",
    "exchange_stock_code",
]


class _Code(str, Enum):
    """``str`` mix-in Enum whose ``str()``/``format()`` is the raw code.

    Python 3.12 changed ``format()`` on mixed-in enums to print
    ``ClassName.MEMBER``; pinning ``__str__`` keeps ``f"{code}"`` equal to the
    wire value on every supported version.
    """

    def __str__(self) -> str:
        return str(self.value)

    def __format__(self, format_spec: str) -> str:
        return format(str(self.value), format_spec)


class Exchange(_Code):
    """국내거래소구분 ``dmst_stex_tp`` for orders.

    Checked against kt10000-kt10003 (주문) and kt10006-kt10009 (신용주문).
    Account TRs such as kt00004/kt00018 accept only ``KRX``/``NXT``; history
    TRs (kt00007, kt00009) additionally take ``"%"`` for all exchanges.
    The mock server supports ``KRX`` only.
    """

    KRX = "KRX"
    """한국거래소."""
    NXT = "NXT"
    """넥스트트레이드."""
    SOR = "SOR"
    """최선주문집행 (Smart Order Routing)."""


class OrderType(_Code):
    """매매구분 ``trde_tp`` for stock orders.

    Checked against kt10000 (매수), kt10001 (매도), kt10006 (신용 매수),
    kt10007 (신용 매도). Other TRs reuse the name ``trde_tp`` for unrelated
    codes (e.g. 순매수/순매도 in ranking TRs) — don't pass these there.
    """

    LIMIT = "0"
    """보통 (지정가)."""
    MARKET = "3"
    """시장가."""
    CONDITIONAL_LIMIT = "5"
    """조건부지정가."""
    BEST_LIMIT = "6"
    """최유리지정가."""
    FIRST_LIMIT = "7"
    """최우선지정가."""
    LIMIT_IOC = "10"
    """보통 (IOC)."""
    MARKET_IOC = "13"
    """시장가 (IOC)."""
    BEST_IOC = "16"
    """최유리 (IOC)."""
    LIMIT_FOK = "20"
    """보통 (FOK)."""
    MARKET_FOK = "23"
    """시장가 (FOK)."""
    BEST_FOK = "26"
    """최유리 (FOK)."""
    STOP_LIMIT = "28"
    """스톱지정가 (``cond_uv`` 에 조건단가)."""
    MID_PRICE = "29"
    """중간가."""
    MID_PRICE_IOC = "30"
    """중간가 (IOC)."""
    MID_PRICE_FOK = "31"
    """중간가 (FOK)."""
    PRE_MARKET = "61"
    """장시작전시간외."""
    AFTER_HOURS_SINGLE = "62"
    """시간외단일가."""
    POST_MARKET = "81"
    """장마감후시간외."""


class QueryExchange(_Code):
    """거래소구분 ``stex_tp`` for market-data queries.

    The ``1:KRX, 2:NXT, 3:통합`` dialect used by ~45 query TRs (ranking,
    stock-info and sector TRs such as ka10016-ka10037, ka10051, ka20002).
    A few TRs (ka10075, ka10076, ka10085) use ``0`` for 통합 instead — check
    the TR's spec before using this enum there.
    """

    KRX = "1"
    NXT = "2"
    ALL = "3"
    """통합 (KRX + NXT)."""


class Market(_Code):
    """시장구분 ``mrkt_tp`` in the ``000/001/101`` dialect.

    Used by most ranking and stock-info TRs (e.g. ka10016-ka10018,
    ka10023-ka10028, ka10054, ka10098). Some of those (ka10020-ka10022,
    ka10044, ka10058, ka10069) accept only ``KOSPI``/``KOSDAQ``. Sector TRs
    (ka20001…), program-trading TRs (ka90003…) and ka10099 use other codes —
    see :class:`StockListMarket` for the last one.
    """

    ALL = "000"
    KOSPI = "001"
    KOSDAQ = "101"


class StockListMarket(_Code):
    """시장구분 ``mrkt_tp`` for 종목정보 리스트 (ka10099, ``stock_info_list``)."""

    KOSPI = "0"
    KOSDAQ = "10"
    K_OTC = "30"
    KONEX = "50"
    ETN = "60"
    LOSS_LIMITED_ETN = "70"
    """손실제한 ETN."""
    GOLD_SPOT = "80"
    """금현물."""
    VOLATILITY_ETN = "90"
    """변동성 ETN."""
    INFRA_FUND = "2"
    """인프라투융자."""
    ELW = "3"
    MUTUAL_FUND = "4"
    """뮤추얼펀드."""
    WARRANT = "5"
    """신주인수권."""
    REIT = "6"
    """리츠종목."""
    WARRANT_CERTIFICATE = "7"
    """신주인수권증서."""
    ETF = "8"
    HIGH_YIELD_FUND = "9"
    """하이일드펀드."""


class AdjustedPrice(_Code):
    """수정주가구분 ``upd_stkpc_tp`` for chart TRs (ka10079-ka10083, ka10094)."""

    RAW = "0"
    """수정주가 미적용."""
    ADJUSTED = "1"
    """수정주가 적용."""


class PriceChangeSign(_Code):
    """전일대비기호 ``pred_pre_sig`` in responses (46+ TRs)."""

    UPPER_LIMIT = "1"
    """상한가."""
    UP = "2"
    """상승."""
    UNCHANGED = "3"
    """보합."""
    LOWER_LIMIT = "4"
    """하한가."""
    DOWN = "5"
    """하락."""


_EXCHANGE_SUFFIX = {Exchange.KRX: "", Exchange.NXT: "_NX", Exchange.SOR: "_AL"}


def exchange_stock_code(stk_cd: str, exchange: Exchange | str) -> str:
    """Return the exchange-specific ``stk_cd`` that quote/chart TRs expect.

    Kiwoom's spec: ``KRX:039490, NXT:039490_NX, SOR:039490_AL``. Any existing
    suffix on ``stk_cd`` is replaced.

    >>> exchange_stock_code("005930", Exchange.NXT)
    '005930_NX'

    Raises:
        ValueError: If ``exchange`` is not KRX, NXT or SOR.
    """
    base = stk_cd.split("_", 1)[0]
    return base + _EXCHANGE_SUFFIX[Exchange(exchange)]
