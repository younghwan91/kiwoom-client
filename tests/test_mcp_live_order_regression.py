"""Regression bundle: without the opt-in, no path exposes or reaches an order tool.

The live-order guard drops order/credit_order tools at registration. Every
feature added on top of the plain tool list — toolset filter, listing modes
(full/smart/discovery), helper tools, resources — must see only what the guard
left. This file walks every path in every server configuration and fails if an order tool is
listed, searchable, describable, callable, or if any request reaches an order
endpoint. A positive control proves the checks would notice a leak.
"""

from __future__ import annotations

import asyncio
import json

import pytest
from mcp import types

from kiwoom_client import AsyncKiwoomAPI
from kiwoom_client.mcp import server as server_module
from kiwoom_client.mcp.guard import ENV_VAR as LIVE_ORDERS_ENV_VAR
from kiwoom_client.mcp.intents import intent_tools
from kiwoom_client.mcp.modes import FULL, MODES
from kiwoom_client.mcp.orders.tools import TOOL_NAMES as HIGH_LEVEL_ORDER_TOOLS
from kiwoom_client.mcp.server import build_server
from kiwoom_client.mcp.tools import GUARDED_MODULES, discover_rest_tools
from kiwoom_client.mcp.toolsets import TOOLSET_NAMES

BASE = "https://mockapi.kiwoom.com"
ORDER_PATHS = ("/api/dostk/ordr", "/api/dostk/crdordr")

#: Raw TR order tools plus the high-level ones (place_order ...) built on them.
GUARDED_NAMES = sorted(
    {s.tool_name for s in discover_rest_tools() if s.guarded} | HIGH_LEVEL_ORDER_TOOLS
)

TOOLSET_CHOICES = [
    None,
    frozenset({"order"}),
    frozenset({"credit_order"}),
    frozenset(GUARDED_MODULES),
    frozenset(TOOLSET_NAMES),
]
CONFIGS = [
    pytest.param(mode, toolsets, id=f"mode={mode}-toolsets={sorted(toolsets or [])}")
    for mode in MODES
    for toolsets in TOOLSET_CHOICES
]

ORDER_ARGS = {"params": {"dmst_stex_tp": "KRX", "stk_cd": "005930", "ord_qty": "1", "trde_tp": "3"}}


@pytest.fixture
async def api(httpx_mock):
    httpx_mock.add_response(
        url=f"{BASE}/oauth2/token",
        json={"token": "test_token", "token_type": "Bearer", "expires_in": 86400},
    )
    api = AsyncKiwoomAPI("key", "secret", is_mock=True)
    await api.login()
    yield api
    await api.close()


def _order_requests(httpx_mock) -> list[str]:
    return [str(r.url) for r in httpx_mock.get_requests() if r.url.path in ORDER_PATHS]


async def _list(app) -> list[types.Tool]:
    result = await app.get_request_handler("tools/list").handler(
        None, types.PaginatedRequestParams()
    )
    return result.tools


async def _call(app, name: str, arguments: dict) -> types.CallToolResult:
    return await app.get_request_handler("tools/call").handler(
        None, types.CallToolRequestParams(name=name, arguments=arguments)
    )


async def _tool_index(app) -> set[str]:
    result = await app.get_request_handler("resources/read").handler(
        None, types.ReadResourceRequestParams(uri="kiwoom://tools")
    )
    return {item["name"] for item in json.loads(result.contents[0].text)}


async def _reachable_names(app, *, meta: bool) -> set[str]:
    """Every tool name an agent could learn about through any path."""
    names = {t.name for t in await _list(app)} | await _tool_index(app)
    if meta:
        found = await _call(app, "search_tools", {"limit": 50})
        summary = json.loads(found.content[0].text)
        for toolset in summary["toolsets"]:
            page = json.loads(
                (await _call(app, "search_tools", {"toolset": toolset, "limit": 50}))
                .content[0]
                .text
            )
            names |= {t["name"] for t in page["tools"]}
    return names


@pytest.mark.parametrize(("mode", "toolsets"), CONFIGS)
class TestNoOrderToolWithoutOptIn:
    async def test_not_listed_indexed_or_searchable(self, mode, toolsets):
        app, specs = build_server(api=None, allow_live_orders=False, mode=mode, toolsets=toolsets)
        assert not any(spec.guarded for spec in specs)
        assert not set(GUARDED_NAMES) & await _reachable_names(app, meta=mode != FULL)
        for tool in await _list(app):
            ann = tool.annotations
            if tool.name != "call_tool":
                assert not (ann and ann.destructive_hint), tool.name
        if mode != FULL:
            for name in GUARDED_NAMES:
                described = await _call(app, "describe_tool", {"name": name})
                assert described.is_error is True, name

    async def test_not_callable_by_any_route(self, httpx_mock, api, mode, toolsets):
        app, _specs = build_server(api, allow_live_orders=False, mode=mode, toolsets=toolsets)
        for name in GUARDED_NAMES:
            direct = await _call(app, name, ORDER_ARGS)
            assert direct.is_error is True, name
            if mode != FULL:
                meta = await _call(app, "call_tool", {"name": name, "arguments": ORDER_ARGS})
                assert meta.is_error is True, name
                assert "Unknown tool" in meta.content[0].text
        assert _order_requests(httpx_mock) == []


class TestHelperAndLocalToolsNeverOrder:
    async def test_every_local_tool_stays_off_order_endpoints(self, httpx_mock, api):
        httpx_mock.add_response(
            url=f"{BASE}/api/dostk/stkinfo",
            json={"return_code": 0, "list": [{"code": "005930", "name": "삼성전자"}]},
            is_reusable=True,
        )
        httpx_mock.add_response(
            url=f"{BASE}/api/dostk/acnt", json={"return_code": 0}, is_reusable=True
        )
        # Any other lookup endpoint an intent tool uses answers an empty OK. Order
        # endpoints would answer too — the assertion at the end is what catches them.
        httpx_mock.add_response(json={"return_code": 0}, is_reusable=True, is_optional=True)
        app, specs = build_server(api, allow_live_orders=False)
        rest_names = {s.tool_name for s in specs}
        local = [t for t in await _list(app) if t.name not in rest_names]
        assert {t.name for t in local} >= {"order_preview", "stock_search", "account_summary"}
        sample_args = {
            "order_preview": {"side": "buy", "stk_cd": "005930", "ord_qty": 1, "ord_uv": 70000},
            # every intent tool, called with the example shown in its description
            **{tool.name: tool.example for tool in intent_tools() if tool.example is not None},
        }
        for tool in local:
            result = await _call(app, tool.name, sample_args.get(tool.name, {}))
            assert result.is_error is False, (tool.name, result.content[0].text)
        assert _order_requests(httpx_mock) == []

    async def test_order_preview_says_orders_are_off(self):
        app, _specs = build_server(api=None, allow_live_orders=False)
        args = {"side": "buy", "stk_cd": "005930", "ord_qty": 1, "ord_uv": 70000}
        preview = json.loads((await _call(app, "order_preview", args)).content[0].text)
        assert preview["sent"] is False
        assert preview["order_tools_enabled"] is False


class TestPositiveControl:
    """With the opt-in the same checks find the order tools — they are not vacuous."""

    @pytest.mark.parametrize("mode", ["discovery", "smart"])
    async def test_opt_in_exposes_order_tools_everywhere(self, mode):
        app, _specs = build_server(api=None, allow_live_orders=True, mode=mode)
        assert set(GUARDED_NAMES) <= await _reachable_names(app, meta=True)
        listed = {t.name: t for t in await _list(app)}
        assert listed["call_tool"].annotations.destructive_hint is True


class TestRunServerWiring:
    """run_server must derive the guard from is_mock + env, not from any other option."""

    @pytest.fixture
    def captured(self, monkeypatch):
        calls: list[dict] = []

        def fake_build_server(api, **kwargs):
            calls.append(kwargs)
            return object(), []

        def fake_run(coro):
            coro.close()

        monkeypatch.setattr(server_module, "build_server", fake_build_server)
        monkeypatch.setattr(asyncio, "run", fake_run)
        return calls

    @pytest.mark.parametrize(
        ("is_mock", "env_value", "expected"),
        [
            (False, None, False),
            (False, "false", False),
            (False, "1", False),
            (False, "true", True),
            (True, None, True),
        ],
    )
    def test_guard_decision(self, monkeypatch, captured, is_mock, env_value, expected):
        if env_value is None:
            monkeypatch.delenv(LIVE_ORDERS_ENV_VAR, raising=False)
        else:
            monkeypatch.setenv(LIVE_ORDERS_ENV_VAR, env_value)
        server_module.run_server(
            app_key="k",
            app_secret="s",
            is_mock=is_mock,
            toolsets=frozenset(GUARDED_MODULES),
            discovery=True,
            max_rows=5,
        )
        assert captured[0]["allow_live_orders"] is expected
