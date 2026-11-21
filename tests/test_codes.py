"""Tests for the coded-value enums in kiwoom_client.codes."""

from __future__ import annotations

import json

import pytest

import kiwoom_client
from kiwoom_client.codes import (
    AdjustedPrice,
    Exchange,
    Market,
    OrderType,
    PriceChangeSign,
    QueryExchange,
    StockListMarket,
    exchange_stock_code,
)

ALL_ENUMS = (
    AdjustedPrice, Exchange, Market, OrderType, PriceChangeSign, QueryExchange, StockListMarket,
)


class TestWireValues:
    """Values copied from Kiwoom's official spec — a change here is a bug."""

    def test_exchange(self):
        assert [e.value for e in Exchange] == ["KRX", "NXT", "SOR"]

    def test_order_type(self):
        assert {e.name: e.value for e in OrderType} == {
            "LIMIT": "0", "MARKET": "3", "CONDITIONAL_LIMIT": "5", "BEST_LIMIT": "6",
            "FIRST_LIMIT": "7", "LIMIT_IOC": "10", "MARKET_IOC": "13", "BEST_IOC": "16",
            "LIMIT_FOK": "20", "MARKET_FOK": "23", "BEST_FOK": "26", "STOP_LIMIT": "28",
            "MID_PRICE": "29", "MID_PRICE_IOC": "30", "MID_PRICE_FOK": "31",
            "PRE_MARKET": "61", "AFTER_HOURS_SINGLE": "62", "POST_MARKET": "81",
        }

    def test_query_exchange(self):
        assert (QueryExchange.KRX, QueryExchange.NXT, QueryExchange.ALL) == ("1", "2", "3")

    def test_market(self):
        assert (Market.ALL, Market.KOSPI, Market.KOSDAQ) == ("000", "001", "101")

    def test_stock_list_market(self):
        assert StockListMarket.KOSPI == "0"
        assert StockListMarket.KOSDAQ == "10"
        assert StockListMarket.ETF == "8"
        assert len(StockListMarket) == 16

    def test_adjusted_price_and_sign(self):
        assert (AdjustedPrice.RAW, AdjustedPrice.ADJUSTED) == ("0", "1")
        assert [s.value for s in PriceChangeSign] == ["1", "2", "3", "4", "5"]

    @pytest.mark.parametrize("enum", ALL_ENUMS)
    def test_values_are_unique(self, enum):
        values = [member.value for member in enum]
        assert len(values) == len(set(values))


class TestStrBehaviour:
    @pytest.mark.parametrize("enum", ALL_ENUMS)
    def test_str_and_format_are_the_raw_code(self, enum):
        for member in enum:
            assert isinstance(member, str)
            assert str(member) == member.value
            assert f"{member}" == member.value
            assert f"{member:>4}" == f"{member.value:>4}"

    def test_json_serialises_to_raw_code(self):
        body = {"trde_tp": OrderType.MARKET, "dmst_stex_tp": Exchange.KRX}
        assert json.dumps(body) == '{"trde_tp": "3", "dmst_stex_tp": "KRX"}'

    def test_lookup_by_value(self):
        assert OrderType("3") is OrderType.MARKET
        assert PriceChangeSign("5") is PriceChangeSign.DOWN

    def test_reaches_the_wire(self, httpx_mock):
        from kiwoom_client.base import BaseClient

        httpx_mock.add_response(json={"return_code": 0})
        with BaseClient("k", "s", is_mock=True, rate_limit=None) as client:
            client.access_token = "t"
            client.request("/api/dostk/stkinfo", "ka10099", {"mrkt_tp": StockListMarket.KOSDAQ})
        assert json.loads(httpx_mock.get_requests()[0].content) == {"mrkt_tp": "10"}


class TestExchangeStockCode:
    @pytest.mark.parametrize(
        ("exchange", "expected"),
        [(Exchange.KRX, "039490"), (Exchange.NXT, "039490_NX"), (Exchange.SOR, "039490_AL"),
         ("NXT", "039490_NX")],
    )
    def test_suffixes(self, exchange, expected):
        assert exchange_stock_code("039490", exchange) == expected

    def test_replaces_existing_suffix(self):
        assert exchange_stock_code("039490_NX", Exchange.KRX) == "039490"
        assert exchange_stock_code("039490_AL", Exchange.NXT) == "039490_NX"

    def test_unknown_exchange(self):
        with pytest.raises(ValueError):
            exchange_stock_code("005930", "NYSE")


def test_top_level_exports():
    assert kiwoom_client.OrderType is OrderType
    assert kiwoom_client.Exchange is Exchange
