"""Tests for the network-free order_preview tool."""

from __future__ import annotations

import json
import socket

import httpx
import pytest
from mcp import types

from kiwoom_client.mcp.order_preview import TOOL_NAME, preview_order
from kiwoom_client.mcp.server import build_server


def _preview(**arguments):
    return preview_order(arguments, order_tools_enabled=True)


class TestPreviewOrder:
    def test_valid_limit_buy_is_passed_through(self):
        result = _preview(side="buy", stk_cd="005930", ord_qty=10, ord_uv=70000)
        assert result["sent"] is False
        assert result["would_call"] == "order_buy_order"
        assert result["params"] == {
            "dmst_stex_tp": "KRX",
            "stk_cd": "005930",
            "ord_qty": "10",
            "ord_uv": "70000",
            "trde_tp": "0",
        }
        assert result["estimated_amount"] == 700000
        assert result["price"]["changed"] is False
        assert result["warnings"] == []

    def test_buy_price_is_rounded_down_to_tick(self):
        result = _preview(side="buy", stk_cd="005930", ord_qty="3", ord_uv="70050")
        assert result["params"]["ord_uv"] == "70000"
        assert result["price"] == {
            "requested": "70050",
            "adjusted": "70000",
            "tick_size": "100",
            "changed": True,
        }
        assert any("내림" in w for w in result["warnings"])

    def test_sell_price_is_rounded_up_to_tick(self):
        result = _preview(side="sell", stk_cd="005930", ord_qty=1, ord_uv=70050)
        assert result["params"]["ord_uv"] == "70100"
        assert result["would_call"] == "order_sell_order"

    def test_sell_round_up_crosses_band_edge_to_a_valid_tick(self):
        result = _preview(side="sell", stk_cd="000000", ord_qty=1, ord_uv=4997)
        assert result["params"]["ord_uv"] == "5000"

    def test_market_order_drops_price(self):
        result = _preview(side="buy", stk_cd="005930", ord_qty=1, ord_uv=70000, trde_tp="3")
        assert result["params"]["ord_uv"] == ""
        assert result["estimated_amount"] is None
        assert result["price"] is None
        assert any("단가를 쓰지 않습니다" in w for w in result["warnings"])

    def test_limit_order_without_price_is_rejected(self):
        with pytest.raises(ValueError, match="ord_uv"):
            _preview(side="buy", stk_cd="005930", ord_qty=1)

    @pytest.mark.parametrize("qty", [0, -1, "1.5", "abc", None])
    def test_bad_quantity_is_rejected(self, qty):
        with pytest.raises(ValueError, match="ord_qty"):
            _preview(side="buy", stk_cd="005930", ord_qty=qty, ord_uv=1000)

    def test_bad_side_is_rejected(self):
        with pytest.raises(ValueError, match="side"):
            _preview(side="short", stk_cd="005930", ord_qty=1, ord_uv=1000)

    def test_soft_problems_become_warnings(self):
        result = _preview(
            side="buy", stk_cd="5930", ord_qty=1, ord_uv=1000, trde_tp="99", dmst_stex_tp="NYSE"
        )
        assert len(result["warnings"]) == 3

    def test_reports_when_order_tools_are_not_registered(self):
        result = preview_order(
            {"side": "buy", "stk_cd": "005930", "ord_qty": 1, "ord_uv": 1000},
            order_tools_enabled=False,
        )
        assert result["order_tools_enabled"] is False
        assert any("KIWOOM_MCP_ALLOW_LIVE_ORDERS" in w for w in result["warnings"])


@pytest.fixture
def no_network(monkeypatch):
    """Any attempt to open a socket or send an httpx request fails the test."""

    def _blocked(*_args, **_kwargs):
        raise AssertionError("order_preview must not touch the network")

    monkeypatch.setattr(socket.socket, "connect", _blocked)
    monkeypatch.setattr(httpx.AsyncClient, "send", _blocked)
    monkeypatch.setattr(httpx.Client, "send", _blocked)


class TestOrderPreviewTool:
    async def _call(self, app, arguments):
        handler = app.get_request_handler("tools/call").handler
        return await handler(None, types.CallToolRequestParams(name=TOOL_NAME, arguments=arguments))

    async def test_listed_even_without_live_order_opt_in(self):
        app, _specs = build_server(api=None, allow_live_orders=False)
        listed = await app.get_request_handler("tools/list").handler(
            None, types.PaginatedRequestParams()
        )
        tools = {t.name: t for t in listed.tools}
        assert TOOL_NAME in tools
        assert "order_buy_order" not in tools
        assert tools[TOOL_NAME].annotations.read_only_hint is True

    async def test_call_makes_no_network_request(self, no_network):
        # api=None: the tool has no client to call even if it wanted to.
        app, _specs = build_server(api=None, allow_live_orders=False)
        result = await self._call(
            app, {"side": "buy", "stk_cd": "005930", "ord_qty": 1, "ord_uv": 70050}
        )
        assert result.is_error is False
        payload = json.loads(result.content[0].text)
        assert payload["sent"] is False
        assert payload["params"]["ord_uv"] == "70000"
        assert payload["order_tools_enabled"] is False

    async def test_invalid_input_is_a_tool_error(self, no_network):
        app, _specs = build_server(api=None, allow_live_orders=True)
        result = await self._call(app, {"side": "buy", "stk_cd": "005930", "ord_qty": 0})
        assert result.is_error is True

    async def test_follows_the_order_toolset(self):
        for toolsets, expected in (({"order"}, True), ({"market"}, False)):
            app, _specs = build_server(api=None, allow_live_orders=False, toolsets=toolsets)
            listed = await app.get_request_handler("tools/list").handler(
                None, types.PaginatedRequestParams()
            )
            assert (TOOL_NAME in {t.name for t in listed.tools}) is expected
