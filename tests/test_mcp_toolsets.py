"""Tests for the KIWOOM_MCP_TOOLSETS filter."""

from __future__ import annotations

import pytest
from mcp import types

from kiwoom_client.mcp.server import build_server
from kiwoom_client.mcp.toolsets import ENV_VAR, TOOLSET_NAMES, parse_toolsets, toolsets_from_env


class TestParseToolsets:
    @pytest.mark.parametrize("value", [None, "", "  ", ",", "all", "ALL"])
    def test_unset_or_all_means_every_toolset(self, value):
        assert parse_toolsets(value) is None

    def test_comma_separated_names_are_trimmed_and_lowercased(self):
        assert parse_toolsets(" Market, chart ,account") == {"market", "chart", "account"}

    def test_unknown_name_is_rejected_with_the_valid_list(self):
        with pytest.raises(ValueError, match="nope") as exc:
            parse_toolsets("market,nope")
        assert "stock_info" in str(exc.value)

    def test_every_module_is_a_toolset(self):
        assert parse_toolsets(",".join(TOOLSET_NAMES)) == set(TOOLSET_NAMES)

    def test_reads_env(self):
        assert toolsets_from_env({ENV_VAR: "chart"}) == {"chart"}
        assert toolsets_from_env({}) is None


class TestBuildServerToolsets:
    def test_default_registers_every_module(self):
        _app, specs = build_server(api=None, allow_live_orders=True)
        assert {s.module_name for s in specs} == set(TOOLSET_NAMES)

    def test_filter_keeps_only_named_modules(self):
        _app, specs = build_server(api=None, allow_live_orders=False, toolsets={"market", "chart"})
        assert specs
        assert {s.module_name for s in specs} == {"market", "chart"}

    def test_condition_search_is_a_toolset_too(self):
        _app, specs = build_server(api=None, allow_live_orders=False, toolsets={"chart"})
        assert not any(s.module_name == "condition_search" for s in specs)

    def test_naming_order_cannot_bypass_the_live_order_guard(self):
        _app, specs = build_server(
            api=None, allow_live_orders=False, toolsets={"order", "credit_order", "account"}
        )
        assert not any(s.guarded for s in specs)
        assert {s.module_name for s in specs} == {"account"}

    def test_order_toolset_with_opt_in_exposes_order_tools(self):
        _app, specs = build_server(api=None, allow_live_orders=True, toolsets={"order"})
        assert specs and all(s.module_name == "order" for s in specs)

    async def test_filtered_out_tool_is_neither_listed_nor_callable(self):
        app, _specs = build_server(api=object(), allow_live_orders=True, toolsets={"chart"})
        listed = await app.get_request_handler("tools/list").handler(
            None, types.PaginatedRequestParams()
        )
        assert "stock_info_basic_stock_info" not in {t.name for t in listed.tools}
        result = await app.get_request_handler("tools/call").handler(
            None,
            types.CallToolRequestParams(name="stock_info_basic_stock_info", arguments={}),
        )
        assert result.is_error is True
        assert "Unknown tool" in result.content[0].text
