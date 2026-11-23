"""order_preview's live-data checks: 상·하한가 and 주문가능/매도가능수량.

Only lookups (ka10001, kt00011, kt00018) are mocked; an error must withhold
the confirm token and no request may reach an order endpoint.
"""

from __future__ import annotations

import pytest

from kiwoom_client import AsyncKiwoomAPI
from kiwoom_client.mcp.orders.policy import OrderPolicy
from kiwoom_client.mcp.server import build_server
from tests.mcp_order_helpers import (
    BUY,
    mock_buyable,
    mock_holdings,
    mock_quote,
    mock_token,
    ok,
    order_requests,
)


@pytest.fixture
async def api(httpx_mock):
    mock_token(httpx_mock)
    api = AsyncKiwoomAPI("key", "secret", is_mock=True)
    await api.login()
    yield api
    await api.close()


@pytest.fixture
def app(api):
    app, _ = build_server(api, allow_live_orders=True, order_policy=OrderPolicy())
    return app


def _requested(httpx_mock, api_id: str) -> list:
    return [r for r in httpx_mock.get_requests() if r.headers.get("api-id") == api_id]


class TestPriceBand:
    async def test_inside_band_issues_a_token(self, httpx_mock, app):
        mock_quote(httpx_mock)
        mock_buyable(httpx_mock)
        result = await ok(app, "order_preview", BUY)
        assert result["errors"] == []
        assert result["confirm_token"]
        assert result["checks"]["upper_limit"] == 91000
        assert result["checks"]["lower_limit"] == 49000
        assert order_requests(httpx_mock) == []

    @pytest.mark.parametrize(
        ("price", "word"), [(91100, "상한가"), (48950, "하한가")]
    )
    async def test_outside_band_is_an_error_without_token(self, httpx_mock, app, price, word):
        mock_quote(httpx_mock)
        mock_buyable(httpx_mock)
        result = await ok(app, "order_preview", {**BUY, "ord_uv": price})
        assert any(word in e for e in result["errors"])
        assert "confirm_token" not in result
        assert order_requests(httpx_mock) == []

    @pytest.mark.parametrize(("price", "word"), [(90000, "상한가"), (49500, "하한가")])
    async def test_near_a_limit_is_a_warning(self, httpx_mock, app, price, word):
        mock_quote(httpx_mock)
        mock_buyable(httpx_mock)
        result = await ok(app, "order_preview", {**BUY, "ord_uv": price})
        assert result["errors"] == []
        assert any(word in w and "가깝" in w for w in result["warnings"])

    async def test_modify_is_checked_against_the_band(self, httpx_mock, app):
        mock_quote(httpx_mock)
        args = {"action": "modify", "order_no": "1", "stock": "005930", "qty": 1, "price": 95000}
        result = await ok(app, "order_preview", args)
        assert any("상한가" in e for e in result["errors"])
        assert _requested(httpx_mock, "kt00011") == []

    async def test_cancel_makes_no_lookup(self, httpx_mock, app):
        args = {"action": "cancel", "order_no": "1", "stock": "005930"}
        result = await ok(app, "order_preview", args)
        assert result["confirm_token"]
        assert httpx_mock.get_requests(url=None)[-1].url.path == "/oauth2/token"


class TestBuyable:
    async def test_more_than_orderable_is_an_error(self, httpx_mock, app):
        mock_quote(httpx_mock)
        mock_buyable(httpx_mock, allowed="5", cash_only="3")
        result = await ok(app, "order_preview", BUY)
        assert any("주문가능수량" in e for e in result["errors"])
        assert result["checks"]["orderable_qty"] == 5
        assert "confirm_token" not in result
        (req,) = _requested(httpx_mock, "kt00011")
        assert b'"uv":"70000"' in req.content.replace(b" ", b"")

    async def test_margin_beyond_cash_is_a_warning(self, httpx_mock, app):
        mock_quote(httpx_mock)
        mock_buyable(httpx_mock, allowed="100", cash_only="5")
        result = await ok(app, "order_preview", BUY)
        assert result["errors"] == []
        assert any("미수" in w for w in result["warnings"])

    async def test_market_buy_is_sized_at_the_upper_limit(self, httpx_mock, app):
        mock_quote(httpx_mock)
        mock_buyable(httpx_mock)
        await ok(app, "order_preview", {**BUY, "ord_uv": None, "price": "market"})
        (req,) = _requested(httpx_mock, "kt00011")
        assert b'"uv":"91000"' in req.content.replace(b" ", b"")

    async def test_unknown_rate_falls_back_to_cash_only(self, httpx_mock, app):
        mock_quote(httpx_mock)
        mock_buyable(httpx_mock, rate="", allowed="999", cash_only="4")
        result = await ok(app, "order_preview", BUY)
        assert result["checks"]["orderable_qty"] == 4
        assert result["errors"]


SELL = {**BUY, "side": "sell"}


class TestSellable:

    async def test_within_holdings(self, httpx_mock, app):
        mock_quote(httpx_mock)
        mock_holdings(httpx_mock)
        result = await ok(app, "order_preview", SELL)
        assert result["errors"] == []
        assert result["checks"]["sellable_qty"] == 20

    async def test_more_than_sellable_is_an_error(self, httpx_mock, app):
        mock_quote(httpx_mock)
        mock_holdings(httpx_mock)
        result = await ok(app, "order_preview", {**SELL, "ord_qty": 21})
        assert any("매도가능수량" in e for e in result["errors"])

    async def test_not_held_is_an_error(self, httpx_mock, app):
        mock_quote(httpx_mock)
        mock_holdings(httpx_mock, rows=[{"stk_cd": "A000660", "trde_able_qty": "1"}])
        result = await ok(app, "order_preview", SELL)
        assert any("보유" in e for e in result["errors"])


class TestLookupFailures:
    async def test_failed_lookups_are_warnings_not_passes(self, httpx_mock, app):
        httpx_mock.add_response(
            url="https://mockapi.kiwoom.com/api/dostk/stkinfo",
            json={"return_code": 1, "return_msg": "조회 실패"},
            is_reusable=True,
        )
        httpx_mock.add_response(
            url="https://mockapi.kiwoom.com/api/dostk/acnt",
            json={"return_code": 1, "return_msg": "조회 실패"},
            is_reusable=True,
        )
        result = await ok(app, "order_preview", BUY)
        assert result["errors"] == []
        assert sum("검사하지 못했습니다" in w for w in result["warnings"]) == 2

    async def test_without_connection_no_lookup_happens(self):
        app, _ = build_server(api=None, allow_live_orders=False)
        result = await ok(app, "order_preview", BUY)
        assert result["errors"] == [] and "checks" not in result
