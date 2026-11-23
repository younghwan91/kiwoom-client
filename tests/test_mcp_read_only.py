"""KIWOOM_MCP_READ_ONLY=true: no order tool is registered, mock trading included."""

from __future__ import annotations

import asyncio

import pytest

from kiwoom_client.mcp import server as server_module
from kiwoom_client.mcp.guard import (
    ENV_VAR as LIVE_ORDERS_ENV_VAR,
)
from kiwoom_client.mcp.guard import (
    READ_ONLY_ENV,
    order_tools_allowed,
    read_only,
)
from kiwoom_client.mcp.server import build_server
from tests.mcp_order_helpers import ok


class TestParsing:
    @pytest.mark.parametrize(
        ("value", "expected"),
        [(None, False), ("", False), ("true", True), ("1", True), ("false", False)],
    )
    def test_values(self, value, expected):
        env = {} if value is None else {READ_ONLY_ENV: value}
        assert read_only(env) is expected

    def test_bad_value_refuses(self):
        with pytest.raises(ValueError, match=READ_ONLY_ENV):
            read_only({READ_ONLY_ENV: "yes please"})


@pytest.mark.parametrize("is_mock", [True, False])
@pytest.mark.parametrize("opt_in", [None, "true"])
def test_read_only_beats_mock_and_opt_in(is_mock, opt_in):
    env = {READ_ONLY_ENV: "true"}
    if opt_in:
        env[LIVE_ORDERS_ENV_VAR] = opt_in
    assert order_tools_allowed(is_mock=is_mock, env=env) is False


@pytest.mark.parametrize(
    ("is_mock", "opt_in", "expected"),
    [(True, None, True), (False, None, False), (False, "true", True)],
)
def test_without_read_only_it_is_the_old_guard(is_mock, opt_in, expected):
    env = {} if opt_in is None else {LIVE_ORDERS_ENV_VAR: opt_in}
    assert order_tools_allowed(is_mock=is_mock, env=env) is expected


class TestRunServerWiring:
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

    @pytest.mark.parametrize("is_mock", [True, False])
    def test_no_order_tools(self, monkeypatch, captured, is_mock):
        monkeypatch.setenv(READ_ONLY_ENV, "true")
        monkeypatch.setenv(LIVE_ORDERS_ENV_VAR, "true")
        server_module.run_server(app_key="k", app_secret="s", is_mock=is_mock)
        assert captured[0]["allow_live_orders"] is False


async def test_preview_names_read_only_as_a_reason():
    app, _ = build_server(api=None, allow_live_orders=False)
    preview = await ok(
        app, "order_preview", {"side": "buy", "stk_cd": "005930", "ord_qty": 1, "ord_uv": 70000}
    )
    assert preview["order_tools_enabled"] is False
    assert "confirm_token" not in preview
    assert any(READ_ONLY_ENV in w for w in preview["warnings"])
