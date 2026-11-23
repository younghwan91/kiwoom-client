"""Tests for discovery mode (search_tools / describe_tool / call_tool)."""

from __future__ import annotations

import json

import pytest
from mcp import types

from kiwoom_client import AsyncKiwoomAPI
from kiwoom_client.mcp import cli
from kiwoom_client.mcp.discovery import CALL_TOOL, DESCRIBE_TOOL, META_TOOL_NAMES, SEARCH_TOOLS
from kiwoom_client.mcp.modes import ENV_VAR, discovery_from_env
from kiwoom_client.mcp.server import build_server


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


async def _list(app) -> dict[str, types.Tool]:
    result = await app.get_request_handler("tools/list").handler(
        None, types.PaginatedRequestParams()
    )
    return {t.name: t for t in result.tools}


async def _call(app, name, arguments=None) -> types.CallToolResult:
    return await app.get_request_handler("tools/call").handler(
        None, types.CallToolRequestParams(name=name, arguments=arguments or {})
    )


def _json(result: types.CallToolResult):
    assert result.is_error is False, result.content[0].text
    return json.loads(result.content[0].text)


class TestMode:
    def test_env(self):
        assert discovery_from_env({ENV_VAR: "Discovery"}) is True
        assert discovery_from_env({ENV_VAR: "full"}) is False
        assert discovery_from_env({}) is False

    async def test_build_server_default_lists_every_tool_and_no_meta_tools(self):
        app, specs = build_server(api=None, allow_live_orders=False)
        listed = await _list(app)
        assert {s.tool_name for s in specs} <= set(listed)
        assert not META_TOOL_NAMES & set(listed)

    async def test_discovery_lists_only_the_meta_tools(self):
        app, _specs = build_server(api=None, allow_live_orders=True, discovery=True)
        assert set(await _list(app)) == META_TOOL_NAMES

    async def test_catalog_tools_are_not_directly_callable(self):
        app, _specs = build_server(api=None, allow_live_orders=True, discovery=True)
        result = await _call(app, "order_preview", {"side": "buy"})
        assert result.is_error is True
        assert "call_tool" in result.content[0].text


class TestSearchAndDescribe:
    async def test_no_query_summarises_toolsets(self):
        app, _specs = build_server(api=None, allow_live_orders=False, discovery=True)
        summary = _json(await _call(app, SEARCH_TOOLS))
        assert summary["toolsets"]["account"] > 0
        assert "order" in summary["toolsets"]  # order_preview 만
        assert "credit_order" not in summary["toolsets"]

    async def test_keyword_search_matches_korean_docstrings(self):
        app, _specs = build_server(api=None, allow_live_orders=False, discovery=True)
        found = _json(await _call(app, SEARCH_TOOLS, {"query": "종목기본정보"}))
        assert found["tools"][0]["name"] == "stock_info_basic_stock_info"
        assert found["tools"][0]["read_only"] is True

    async def test_search_by_toolset_and_limit(self):
        app, _specs = build_server(api=None, allow_live_orders=False, discovery=True)
        found = _json(await _call(app, SEARCH_TOOLS, {"toolset": "chart", "limit": 3}))
        assert len(found["tools"]) == 3
        assert found["truncated"] is True
        assert all(t["toolset"] == "chart" for t in found["tools"])

    async def test_describe_returns_schema_and_annotations(self):
        app, _specs = build_server(api=None, allow_live_orders=False, discovery=True)
        detail = _json(await _call(app, DESCRIBE_TOOL, {"name": "order_preview"}))
        assert {"side", "stock", "stk_cd", "qty", "price"} <= set(
            detail["inputSchema"]["properties"]
        )
        assert detail["annotations"]["readOnlyHint"] is True
        assert detail["toolset"] == "order"

    async def test_call_tool_annotation_reflects_whether_orders_are_reachable(self):
        for allow, destructive in ((False, False), (True, True)):
            app, _specs = build_server(api=None, allow_live_orders=allow, discovery=True)
            ann = (await _list(app))[CALL_TOOL].annotations
            assert ann.destructive_hint is destructive


class TestCallTool:
    async def test_runs_a_rest_tool(self, httpx_mock, api):
        httpx_mock.add_response(
            url="https://mockapi.kiwoom.com/api/dostk/stkinfo",
            json={"return_code": 0, "return_msg": "OK", "stk_cd": "005930"},
        )
        app, _specs = build_server(api, allow_live_orders=False, discovery=True)
        result = _json(
            await _call(
                app,
                CALL_TOOL,
                {
                    "name": "stock_info_basic_stock_info",
                    "arguments": {"params": {"stk_cd": "005930"}},
                },
            )
        )
        assert result["stk_cd"] == "005930"

    async def test_runs_a_local_tool(self):
        app, _specs = build_server(api=None, allow_live_orders=False, discovery=True)
        args = {"side": "buy", "stk_cd": "005930", "ord_qty": 1, "ord_uv": 70050}
        result = _json(await _call(app, CALL_TOOL, {"name": "order_preview", "arguments": args}))
        assert result["sent"] is False

    async def test_cannot_call_meta_tools_recursively(self):
        app, _specs = build_server(api=None, allow_live_orders=True, discovery=True)
        result = await _call(app, CALL_TOOL, {"name": CALL_TOOL, "arguments": {}})
        assert result.is_error is True


class TestGuardInDiscoveryMode:
    """call_tool must never reach a tool normal mode would not expose."""

    @pytest.mark.parametrize(
        "name",
        [
            "order_buy_order",
            "order_sell_order",
            "order_modify_order",
            "order_cancel_order",
            "order_gold_spot_buy_order",
            "credit_order_margin_buy_order",
        ],
    )
    async def test_guarded_order_tools_are_unknown_without_opt_in(self, httpx_mock, api, name):
        # httpx_mock has no order endpoint registered: any request would fail loudly.
        app, _specs = build_server(api, allow_live_orders=False, discovery=True)
        args = {"params": {"dmst_stex_tp": "KRX", "stk_cd": "005930", "ord_qty": "1"}}
        result = await _call(app, CALL_TOOL, {"name": name, "arguments": args})
        assert result.is_error is True
        assert "Unknown tool" in result.content[0].text
        assert not [r for r in httpx_mock.get_requests() if "/ordr" in str(r.url)]

    async def test_order_tools_are_not_searchable_or_describable_without_opt_in(self):
        app, _specs = build_server(api=None, allow_live_orders=False, discovery=True)
        found = _json(await _call(app, SEARCH_TOOLS, {"query": "매수주문"}))
        assert found["tools"] == []
        described = await _call(app, DESCRIBE_TOOL, {"name": "order_buy_order"})
        assert described.is_error is True

    async def test_toolset_filter_applies_to_call_tool(self):
        app, _specs = build_server(
            api=None, allow_live_orders=True, discovery=True, toolsets={"chart"}
        )
        result = await _call(
            app, CALL_TOOL, {"name": "stock_info_basic_stock_info", "arguments": {}}
        )
        assert result.is_error is True
        assert "Unknown tool" in result.content[0].text


class TestCliDiscoveryFlag:
    def test_flag_and_env_turn_it_on(self, monkeypatch):
        calls = []
        import kiwoom_client.mcp.server as server

        monkeypatch.setattr(server, "run_server", lambda **kw: calls.append(kw))
        monkeypatch.setenv("KIWOOM_APP_KEY", "k")
        monkeypatch.setenv("KIWOOM_APP_SECRET", "s")
        monkeypatch.delenv(ENV_VAR, raising=False)
        cli.main(["--discovery"])
        monkeypatch.setenv(ENV_VAR, "discovery")
        cli.main([])
        monkeypatch.delenv(ENV_VAR)
        cli.main([])
        assert [c["mode"] for c in calls] == ["discovery", "discovery", "smart"]

    def test_config_snippet_can_enable_it(self, capsys):
        cli.main(["config", "cursor", "--discovery"])
        env = json.loads(capsys.readouterr().out)["mcpServers"]["kiwoom"]["env"]
        assert env[ENV_VAR] == "discovery"
