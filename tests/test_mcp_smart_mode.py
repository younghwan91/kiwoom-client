"""Tests for the listing modes — smart (default), full, discovery."""

from __future__ import annotations

import asyncio
import json

import pytest
from mcp import types

from kiwoom_client import AsyncKiwoomAPI
from kiwoom_client.mcp import cli
from kiwoom_client.mcp import server as server_module
from kiwoom_client.mcp.discovery import META_TOOL_NAMES
from kiwoom_client.mcp.local_tools import LocalTool
from kiwoom_client.mcp.modes import (
    DEFAULT_MODE,
    ENV_VAR,
    MODES,
    SMART,
    mode_from_env,
    parse_mode,
)
from kiwoom_client.mcp.server import _local_tools, build_server

BASE = "https://mockapi.kiwoom.com"

#: tools/list of the smart default must stay small enough to leave on. The
#: budget leaves room for more intent tools; full mode is ~220 K characters.
SMART_LIST_BUDGET = 40_000


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


async def _list(app) -> list[types.Tool]:
    result = await app.get_request_handler("tools/list").handler(
        None, types.PaginatedRequestParams()
    )
    return result.tools


async def _call(app, name, arguments=None) -> types.CallToolResult:
    return await app.get_request_handler("tools/call").handler(
        None, types.CallToolRequestParams(name=name, arguments=arguments or {})
    )


def _json(result: types.CallToolResult):
    assert result.is_error is False, result.content[0].text
    return json.loads(result.content[0].text)


def _size(tools: list[types.Tool]) -> int:
    dumped = [t.model_dump(mode="json", by_alias=True, exclude_none=True) for t in tools]
    return len(json.dumps(dumped, ensure_ascii=False))


class TestParse:
    def test_default_is_smart(self):
        assert DEFAULT_MODE == SMART == MODES[0]
        assert parse_mode(None) == parse_mode("") == parse_mode("  ") == "smart"
        assert mode_from_env({}) == "smart"

    def test_case_and_space_insensitive(self):
        assert parse_mode(" Full ") == "full"
        assert mode_from_env({ENV_VAR: "DISCOVERY"}) == "discovery"

    def test_unknown_value_raises(self):
        with pytest.raises(ValueError, match="smart, full, discovery"):
            parse_mode("all")

    def test_build_server_rejects_unknown_mode(self):
        with pytest.raises(ValueError, match="unknown mode"):
            build_server(api=None, allow_live_orders=False, mode="tiny")


class TestSmartListing:
    async def test_lists_local_tools_and_meta_tools_only(self):
        app, specs = build_server(api=None, allow_live_orders=False, mode="smart")
        listed = {t.name for t in await _list(app)}
        local = {t.name for t in _local_tools(allow_live_orders=False)}
        assert listed == local | META_TOOL_NAMES
        assert not listed & {s.tool_name for s in specs}

    async def test_new_local_tool_is_listed_automatically(self, monkeypatch):
        """An intent tool added to the registration point shows up with no other change."""
        extra = LocalTool(
            name="fake_intent",
            title="가짜 의도 도구",
            description="테스트용",
            input_schema={"type": "object", "properties": {}},
            annotations=types.ToolAnnotations(read_only_hint=True),
            toolset="market",
            handler=lambda _api, _args: asyncio.sleep(0, result={"ok": True}),
        )
        original = server_module._local_tools
        monkeypatch.setattr(server_module, "_local_tools", lambda **kw: [*original(**kw), extra])
        app, _specs = build_server(api=None, allow_live_orders=False, mode="smart")
        assert "fake_intent" in {t.name for t in await _list(app)}
        assert _json(await _call(app, "fake_intent")) == {"ok": True}
        found = _json(await _call(app, "search_tools", {"query": "가짜 의도"}))
        assert [t["name"] for t in found["tools"]] == ["fake_intent"]

    async def test_stays_within_budget(self):
        for allow in (False, True):
            app, _specs = build_server(api=None, allow_live_orders=allow, mode="smart")
            assert _size(await _list(app)) < SMART_LIST_BUDGET

    async def test_is_far_smaller_than_full(self):
        smart, _ = build_server(api=None, allow_live_orders=False, mode="smart")
        full, _ = build_server(api=None, allow_live_orders=False, mode="full")
        assert _size(await _list(smart)) * 5 < _size(await _list(full))


class TestSmartCalls:
    async def test_local_tool_is_called_directly(self):
        app, _specs = build_server(api=None, allow_live_orders=False, mode="smart")
        args = {"side": "buy", "stk_cd": "005930", "ord_qty": 1, "ord_uv": 70010}
        preview = _json(await _call(app, "order_preview", args))
        assert preview["sent"] is False

    async def test_tr_tool_runs_through_call_tool(self, httpx_mock, api):
        httpx_mock.add_response(
            url=f"{BASE}/api/dostk/stkinfo",
            json={"return_code": 0, "stk_cd": "005930", "stk_nm": "삼성전자"},
        )
        app, _specs = build_server(api, allow_live_orders=False, mode="smart")
        result = _json(
            await _call(
                app,
                "call_tool",
                {
                    "name": "stock_info_basic_stock_info",
                    "arguments": {"params": {"stk_cd": "005930"}},
                },
            )
        )
        assert result["stk_nm"] == "삼성전자"

    async def test_tr_tool_is_not_called_directly(self):
        app, _specs = build_server(api=None, allow_live_orders=False, mode="smart")
        result = await _call(app, "stock_info_basic_stock_info", {"params": {"stk_cd": "005930"}})
        assert result.is_error is True
        assert "call_tool" in result.content[0].text


class TestToolsetFilterAppliesFirst:
    async def test_smart_lists_only_local_tools_of_chosen_toolsets(self):
        app, _specs = build_server(
            api=None, allow_live_orders=False, mode="smart", toolsets=frozenset({"chart"})
        )
        listed = {t.name for t in await _list(app)}
        assert listed == META_TOOL_NAMES  # every current local tool is in another toolset
        summary = _json(await _call(app, "search_tools"))
        assert set(summary["toolsets"]) == {"chart"}

    async def test_smart_keeps_local_tools_in_chosen_toolsets(self):
        app, _specs = build_server(
            api=None, allow_live_orders=False, mode="smart", toolsets=frozenset({"stock_info"})
        )
        listed = {t.name for t in await _list(app)}
        assert {"stock_search", "stock_snapshot"} <= listed
        assert "account_summary" not in listed


class TestCli:
    @pytest.fixture
    def calls(self, monkeypatch):
        calls: list[dict] = []
        monkeypatch.setattr(server_module, "run_server", lambda **kw: calls.append(kw))
        monkeypatch.setenv("KIWOOM_APP_KEY", "k")
        monkeypatch.setenv("KIWOOM_APP_SECRET", "s")
        monkeypatch.delenv(ENV_VAR, raising=False)
        return calls

    def test_flags_and_env(self, monkeypatch, calls):
        cli.main([])
        cli.main(["--full"])
        cli.main(["--discovery"])
        monkeypatch.setenv(ENV_VAR, "full")
        cli.main([])
        cli.main(["--discovery"])  # the flag beats the environment
        assert [c["mode"] for c in calls] == ["smart", "full", "discovery", "full", "discovery"]

    def test_full_and_discovery_are_exclusive(self, calls):
        with pytest.raises(SystemExit) as exc:
            cli.main(["--full", "--discovery"])
        assert exc.value.code == 2
        assert calls == []

    def test_bad_env_value_exits(self, monkeypatch, capsys, calls):
        monkeypatch.setenv(ENV_VAR, "everything")
        with pytest.raises(SystemExit) as exc:
            cli.main([])
        assert exc.value.code == 1
        assert ENV_VAR in capsys.readouterr().err
        assert calls == []

    def test_config_snippet_mode(self, capsys):
        cli.main(["config", "cursor"])
        env = json.loads(capsys.readouterr().out)["mcpServers"]["kiwoom"]["env"]
        assert ENV_VAR not in env  # server default (smart)
        cli.main(["config", "cursor", "--full"])
        env = json.loads(capsys.readouterr().out)["mcpServers"]["kiwoom"]["env"]
        assert env[ENV_VAR] == "full"


class TestRunServerDefault:
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

    def test_defaults_to_smart(self, captured):
        server_module.run_server(app_key="k", app_secret="s", is_mock=True)
        server_module.run_server(app_key="k", app_secret="s", is_mock=True, discovery=True)
        server_module.run_server(app_key="k", app_secret="s", is_mock=True, mode="full")
        assert [c["mode"] for c in captured] == ["smart", "discovery", "full"]
