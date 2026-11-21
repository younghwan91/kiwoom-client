"""Tests for MCP tool annotations (title / readOnlyHint / destructiveHint ...)."""

from __future__ import annotations

from mcp import types

from kiwoom_client.mcp.annotations import (
    LIVE_ORDER_TITLE_PREFIX,
    tool_annotations,
    tool_title,
)
from kiwoom_client.mcp.server import build_server
from kiwoom_client.mcp.tools import discover_rest_tools


def _spec(name: str):
    return next(s for s in discover_rest_tools() if s.tool_name == name)


async def _listed_tools(*, allow_live_orders: bool) -> dict[str, types.Tool]:
    app, _specs = build_server(api=None, allow_live_orders=allow_live_orders)
    handler = app.get_request_handler("tools/list").handler
    result = await handler(None, types.PaginatedRequestParams())
    return {tool.name: tool for tool in result.tools}


class TestToolAnnotations:
    def test_every_order_tool_is_destructive_and_not_read_only(self):
        for spec in discover_rest_tools():
            if not spec.guarded:
                continue
            ann = tool_annotations(spec)
            assert ann.read_only_hint is False, spec.tool_name
            assert ann.destructive_hint is True, spec.tool_name
            assert ann.idempotent_hint is False, spec.tool_name
            assert ann.open_world_hint is True, spec.tool_name

    def test_every_lookup_tool_is_read_only(self):
        for spec in discover_rest_tools():
            if spec.guarded:
                continue
            ann = tool_annotations(spec)
            assert ann.read_only_hint is True, spec.tool_name
            assert ann.open_world_hint is True, spec.tool_name

    def test_title_is_first_docstring_line(self):
        spec = _spec("stock_info_basic_stock_info")
        assert tool_title(spec) == "종목기본정보요청 (Basic Stock Info)"

    def test_order_titles_are_prefixed(self):
        spec = _spec("order_buy_order")
        title = tool_title(spec)
        assert title.startswith(LIVE_ORDER_TITLE_PREFIX)
        assert "실계좌" not in title  # 경고 문단은 description 에만


class TestListedToolsCarryAnnotations:
    async def test_all_listed_tools_have_title_and_annotations(self):
        tools = await _listed_tools(allow_live_orders=True)
        for tool in tools.values():
            assert tool.title, tool.name
            assert tool.annotations is not None, tool.name
            assert tool.annotations.title == tool.title

    async def test_listed_order_tool_is_destructive(self):
        tools = await _listed_tools(allow_live_orders=True)
        ann = tools["order_buy_order"].annotations
        assert ann.destructive_hint is True
        assert ann.read_only_hint is False

    async def test_condition_search_hints(self):
        tools = await _listed_tools(allow_live_orders=False)
        assert tools["condition_search_condition_list"].annotations.read_only_hint is True
        assert tools["condition_search_condition_search"].annotations.read_only_hint is True
        realtime = tools["condition_search_condition_search_realtime"].annotations
        assert realtime.read_only_hint is False
        assert realtime.destructive_hint is False

    async def test_wire_format_uses_camel_case_hints(self):
        tools = await _listed_tools(allow_live_orders=True)
        dumped = tools["order_buy_order"].model_dump(by_alias=True, exclude_none=True)
        assert dumped["annotations"]["destructiveHint"] is True
        assert dumped["annotations"]["readOnlyHint"] is False
