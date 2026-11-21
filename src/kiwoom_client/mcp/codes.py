"""Kiwoom order code values the MCP helpers need to understand.

Facts only (code → meaning), collected from the Kiwoom REST API guide for
주식 매수/매도주문 (kt10000/kt10001). Kiwoom can add or retire codes; the
official guide is authoritative: https://openapi.kiwoom.com
"""

from __future__ import annotations

#: 매매구분 (``trde_tp``) for stock orders.
TRADE_TYPES: dict[str, str] = {
    "0": "보통(지정가)",
    "3": "시장가",
    "5": "조건부지정가",
    "6": "최유리지정가",
    "7": "최우선지정가",
    "10": "보통(IOC)",
    "13": "시장가(IOC)",
    "16": "최유리(IOC)",
    "20": "보통(FOK)",
    "23": "시장가(FOK)",
    "26": "최유리(FOK)",
    "28": "스톱지정가",
    "29": "중간가",
    "30": "중간가(IOC)",
    "31": "중간가(FOK)",
    "61": "장시작전시간외",
    "62": "시간외단일가",
    "81": "장마감후시간외",
}

#: trde_tp values that carry a limit price in ``ord_uv``.
LIMIT_PRICE_TRADE_TYPES: frozenset[str] = frozenset({"0", "5", "10", "20", "28", "62"})

#: trde_tp values priced by the exchange — ``ord_uv`` is left empty.
NO_PRICE_TRADE_TYPES: frozenset[str] = frozenset(
    {"3", "13", "23", "6", "16", "26", "7", "61", "81"}
)

#: 국내거래소구분 (``dmst_stex_tp``).
EXCHANGES: dict[str, str] = {
    "KRX": "한국거래소",
    "NXT": "넥스트트레이드",
    "SOR": "최선주문집행(SOR)",
}
