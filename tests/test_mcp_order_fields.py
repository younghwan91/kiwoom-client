"""Order tools accept only the TR catalog's request fields; lookups are unchanged."""

from __future__ import annotations

import json

import pytest

from kiwoom_client import AsyncKiwoomAPI, spec
from kiwoom_client.mcp.orders.fields import order_tool_names, unknown_fields
from kiwoom_client.mcp.orders.policy import OrderPolicy
from kiwoom_client.mcp.server import build_server
from kiwoom_client.mcp.tools import discover_rest_tools
from tests.mcp_order_helpers import (
    BUY_PARAMS,
    listed,
    mock_lookups,
    mock_orders,
    mock_token,
    ok,
    order_requests,
    refused,
)

LAX = OrderPolicy(require_confirm=False)


class TestCatalog:
    def test_every_order_tool_is_described_by_the_catalog(self):
        guarded = {s.tool_name for s in discover_rest_tools() if s.guarded}
        assert order_tool_names() == guarded
        for name in guarded:
            assert unknown_fields(name, []) == [], name

    def test_known_and_unknown(self):
        assert unknown_fields("order_buy_order", BUY_PARAMS) == []
        assert unknown_fields("order_buy_order", {**BUY_PARAMS, "acnt_no": "1"}) == ["acnt_no"]
        assert unknown_fields("order_cancel_order", {"ord_qty": "1"}) == ["ord_qty"]
        assert unknown_fields("account_deposit_detail", {}) is None


@pytest.fixture
async def api(httpx_mock):
    mock_token(httpx_mock)
    mock_orders(httpx_mock)
    mock_lookups(httpx_mock)
    api = AsyncKiwoomAPI("key", "secret", is_mock=True)
    await api.login()
    yield api
    await api.close()


class TestOrderTools:
    @pytest.mark.parametrize(
        "arguments",
        [
            {"params": {**BUY_PARAMS, "acnt_no": "1234"}},
            {"params": {**BUY_PARAMS, "mdfy_uv": "1"}},  # a field of another TR
            {"params": {**BUY_PARAMS, "injected": ""}},  # empty value would still be sent
            {"params": BUY_PARAMS, "extra_top_level": "x"},  # flat keys join the body
        ],
    )
    async def test_unknown_field_sends_nothing(self, httpx_mock, api, arguments):
        app, _ = build_server(api, allow_live_orders=True, order_policy=LAX)
        text = await refused(app, "order_buy_order", arguments)
        assert "받지 않는 필드" in text
        assert order_requests(httpx_mock) == []

    async def test_catalog_fields_only_are_sent(self, httpx_mock, api):
        app, _ = build_server(api, allow_live_orders=True, order_policy=LAX)
        await ok(app, "order_buy_order", {"params": {**BUY_PARAMS, "cond_uv": ""}})
        assert len(order_requests(httpx_mock)) == 1

    async def test_credit_order_too(self, httpx_mock, api):
        app, _ = build_server(api, allow_live_orders=True, order_policy=LAX)
        await refused(app, "credit_order_margin_buy_order", {"params": {**BUY_PARAMS, "x": "1"}})
        assert order_requests(httpx_mock) == []

    async def test_preview_tool_mode_reports_unknown_fields_and_withholds_token(self, api):
        app, _ = build_server(api, allow_live_orders=True)
        result = await ok(
            app, "order_preview", {"tool": "order_buy_order", "params": {**BUY_PARAMS, "x": "1"}}
        )
        assert any("받지 않는 필드" in e for e in result["errors"])
        assert "confirm_token" not in result

    async def test_schema_is_closed_for_order_tools_only(self, api):
        app, _ = build_server(api, allow_live_orders=True)
        tools = await listed(app)
        assert tools["order_buy_order"].input_schema["properties"]["params"][
            "additionalProperties"
        ] is False
        assert tools["stock_info_basic_stock_info"].input_schema["properties"]["params"][
            "additionalProperties"
        ] is True


class TestLookupsUnchanged:
    async def test_lookup_still_forwards_unknown_keys(self, httpx_mock, api):
        app, _ = build_server(api, allow_live_orders=False)
        params = {"stk_cd": "005930", "something_new": "1"}
        await ok(app, "stock_info_basic_stock_info", {"params": params})
        (req,) = [r for r in httpx_mock.get_requests() if r.headers.get("api-id") == "ka10001"]
        assert json.loads(req.content) == params

    def test_catalog_has_the_lookup(self):
        assert spec.for_method("stock_info", "basic_stock_info").api_id == "ka10001"
