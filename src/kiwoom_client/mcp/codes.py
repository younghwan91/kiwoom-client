"""Kiwoom order code values the MCP helpers need to understand.

Code → meaning comes from the TR catalog (:mod:`kiwoom_client.spec`, built
from Kiwoom's official spec) so there is one source of truth; the same values
are named in :class:`kiwoom_client.codes.OrderType`. The price classification
below is this package's own reading of those codes. The official guide is
authoritative: https://openapi.kiwoom.com
"""

from __future__ import annotations

from kiwoom_client import spec

#: TR whose ``trde_tp``/``dmst_stex_tp`` codes stock orders use (주식 매수주문).
_ORDER_TR = "kt10000"


def _catalog_codes(api_id: str, field_id: str) -> dict[str, str]:
    field = spec.get(api_id).request_field(field_id)
    return dict(field.codes) if field is not None else {}


#: 매매구분 (``trde_tp``) for stock orders, code → 한글명.
TRADE_TYPES: dict[str, str] = _catalog_codes(_ORDER_TR, "trde_tp")

#: trde_tp values that carry a limit price in ``ord_uv``.
LIMIT_PRICE_TRADE_TYPES: frozenset[str] = frozenset({"0", "5", "10", "20", "28", "62"})

#: trde_tp values priced by the exchange — ``ord_uv`` is left empty.
NO_PRICE_TRADE_TYPES: frozenset[str] = frozenset(
    {"3", "13", "23", "6", "16", "26", "7", "61", "81"}
)

#: 국내거래소구분 (``dmst_stex_tp``). The catalog lists these only as text
#: ("KRX,NXT,SOR"), so the names are spelled out here.
EXCHANGES: dict[str, str] = {
    "KRX": "한국거래소",
    "NXT": "넥스트트레이드",
    "SOR": "최선주문집행(SOR)",
}
