"""Tests for MCP server tool assembly and dispatch."""

from __future__ import annotations

import pytest
from mcp import types

from kiwoom_client import AsyncKiwoomAPI
from kiwoom_client.base import KiwoomAPIError
from kiwoom_client.mcp.server import build_server, dispatch_tool
from kiwoom_client.mcp.tools import discover_rest_tools


@pytest.fixture
async def api(httpx_mock):
    httpx_mock.add_response(
        url="https://mockapi.kiwoom.com/oauth2/token",
        json={"token": "test_token", "token_type": "Bearer", "expires_in": 86400},
    )
    api = AsyncKiwoomAPI("key", "secret", is_mock=True)
    await api.login()
    yield api
    await api.close()


class TestBuildServer:
    def test_mock_registers_guarded_tools(self):
        _app, specs = build_server(api=None, allow_live_orders=True)
        names = {s.tool_name for s in specs}
        assert "order_buy_order" in names

    def test_live_without_opt_in_excludes_guarded_tools(self):
        _app, specs = build_server(api=None, allow_live_orders=False)
        names = {s.tool_name for s in specs}
        assert "order_buy_order" not in names
        assert "credit_order_margin_buy_order" not in names
        # 조회성 도구는 그대로 남는다
        assert "stock_info_basic_stock_info" in names

    def test_condition_search_tools_are_always_present(self):
        for allow in (True, False):
            _app, specs = build_server(api=None, allow_live_orders=allow)
            names = {s.tool_name for s in specs}
            assert {"condition_search_condition_list", "condition_search_condition_search",
                    "condition_search_condition_search_realtime",
                    "condition_search_condition_search_cancel"} <= names

    def test_tool_count_matches_discovery_when_allowed(self):
        _app, specs = build_server(api=None, allow_live_orders=True)
        rest_specs = [s for s in specs if not s.tool_name.startswith("condition_search_")]
        assert len(rest_specs) == len(discover_rest_tools())


class TestDispatchToolRest:
    async def test_forwards_params_to_the_underlying_method(self, httpx_mock, api):
        httpx_mock.add_response(
            url="https://mockapi.kiwoom.com/api/dostk/stkinfo",
            json={"return_code": 0, "return_msg": "OK", "stk_cd": "005930"},
        )
        specs = {s.tool_name: s for s in discover_rest_tools()}
        result = await dispatch_tool(
            api=api,
            session=None,
            spec_by_name=specs,
            name="stock_info_basic_stock_info",
            arguments={"params": {"stk_cd": "005930"}},
        )
        assert result["return_code"] == 0
        assert result["stk_cd"] == "005930"

    async def test_propagates_kiwoom_api_errors(self, httpx_mock, api):
        httpx_mock.add_response(
            url="https://mockapi.kiwoom.com/api/dostk/stkinfo",
            status_code=200,
            json={"return_code": 4, "return_msg": "종목코드 오류"},
        )
        specs = {s.tool_name: s for s in discover_rest_tools()}
        with pytest.raises(KiwoomAPIError):
            await dispatch_tool(
                api=api,
                session=None,
                spec_by_name=specs,
                name="stock_info_basic_stock_info",
                arguments={"params": {"stk_cd": "BAD"}},
            )

    async def test_unknown_tool_name_raises_value_error(self, api):
        with pytest.raises(ValueError, match="Unknown tool"):
            await dispatch_tool(
                api=api, session=None, spec_by_name={}, name="nope", arguments={}
            )


class TestRegisteredHandlers:
    """Exercises the tools/list and tools/call handlers build_server wires up."""

    async def test_list_tools_returns_the_filtered_specs(self):
        app, specs = build_server(api=None, allow_live_orders=False)
        handler = app.get_request_handler("tools/list").handler
        result = await handler(None, types.PaginatedRequestParams())
        assert isinstance(result, types.ListToolsResult)
        assert {t.name for t in result.tools} == {s.tool_name for s in specs}
        assert "order_buy_order" not in {t.name for t in result.tools}

    async def test_call_tool_returns_the_dispatch_result_as_text(self, httpx_mock, api):
        httpx_mock.add_response(
            url="https://mockapi.kiwoom.com/api/dostk/stkinfo",
            json={"return_code": 0, "return_msg": "OK", "stk_cd": "005930"},
        )
        app, _specs = build_server(api, allow_live_orders=True)
        handler = app.get_request_handler("tools/call").handler
        result = await handler(
            None,
            types.CallToolRequestParams(
                name="stock_info_basic_stock_info", arguments={"params": {"stk_cd": "005930"}}
            ),
        )
        assert isinstance(result, types.CallToolResult)
        assert result.is_error is False
        assert "005930" in result.content[0].text

    async def test_call_tool_returns_kiwoom_api_error_as_call_tool_result(self, httpx_mock, api):
        httpx_mock.add_response(
            url="https://mockapi.kiwoom.com/api/dostk/stkinfo",
            status_code=200,
            json={"return_code": 4, "return_msg": "종목코드 오류"},
        )
        app, _specs = build_server(api, allow_live_orders=True)
        handler = app.get_request_handler("tools/call").handler
        result = await handler(
            None,
            types.CallToolRequestParams(
                name="stock_info_basic_stock_info", arguments={"params": {"stk_cd": "BAD"}}
            ),
        )
        assert isinstance(result, types.CallToolResult)
        assert result.is_error is True
        assert "종목코드 오류" in result.content[0].text

    async def test_call_tool_returns_unknown_tool_error_as_call_tool_result(self, api):
        app, _specs = build_server(api, allow_live_orders=True)
        handler = app.get_request_handler("tools/call").handler
        result = await handler(None, types.CallToolRequestParams(name="nope", arguments={}))
        assert isinstance(result, types.CallToolResult)
        assert result.is_error is True
        assert "Unknown tool" in result.content[0].text
