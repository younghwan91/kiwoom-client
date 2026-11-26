"""MCP server in demo mode: every smart-mode tool works offline and says it's synthetic."""

from __future__ import annotations

import pytest

from kiwoom_client.demo import DEMO_KEY, DEMO_NOTICE
from kiwoom_client.mcp import server as mcp_server
from kiwoom_client.mcp.condition_search_session import ConditionSearchSession
from kiwoom_client.mcp.modes import SMART
from kiwoom_client.mcp.orders.tools import TOOL_NAMES as ORDER_TOOL_NAMES
from tests.demo_support import no_network  # noqa: F401
from tests.intent_support import call

pytestmark = pytest.mark.usefixtures("no_network")

#: Tools whose example needs more than the registry example to be useful here.
EXTRA_CALLS = {
    "watch": {"stocks": ["005930"], "seconds": 1},
    "get_orders": {"status": "filled"},
    "order_preview": {"side": "buy", "stock": "삼성전자", "qty": 1, "price": "market"},
}


@pytest.fixture
async def demo_app(monkeypatch):
    for name in ("KIWOOM_MCP_READ_ONLY", "KIWOOM_MCP_AUDIT_LOG", "KIWOOM_MCP_ALLOW_LIVE_ORDERS"):
        monkeypatch.delenv(name, raising=False)
    api, allow_orders, policy = mcp_server.client_and_order_settings(
        app_key="", app_secret="", is_mock=False, demo=True
    )
    session = ConditionSearchSession(connect=lambda: mcp_server._connect_condition_search(api))
    app, _ = mcp_server.build_server(
        api, allow_live_orders=allow_orders, session=session, mode=SMART,
        order_policy=policy, demo=True,
    )  # fmt: skip
    try:
        yield app, api, allow_orders, policy
    finally:
        await session.close()
        await api.close()


async def test_settings_are_paper_orders_without_the_real_audit_log(demo_app):
    _app, api, allow_orders, policy = demo_app
    assert api.is_demo and allow_orders and policy.audit_log is None


async def test_instructions_tell_the_agent_it_is_a_demo(demo_app):
    app = demo_app[0]
    assert "데모 모드" in app.instructions and "가상 데이터" in app.instructions


async def test_every_smart_tool_answers_with_the_marker(demo_app):
    app = demo_app[0]
    listed = await app.get_request_handler("tools/list").handler(None, None)
    names = {t.name for t in listed.tools}
    local = {t.name: t for t in mcp_server._local_tools(allow_live_orders=True)}
    assert {"place_order", "get_portfolio", "watch", "condition_search_run"} <= names
    for name in sorted(names & set(local)):
        if name in ORDER_TOOL_NAMES:
            continue  # need a confirm token: test_order_flow
        arguments = EXTRA_CALLS.get(name, local[name].example or {})
        is_error, payload = await call(app, name, arguments)
        assert not is_error, f"{name}: {payload}"
        assert payload[DEMO_KEY] == DEMO_NOTICE, name
    # meta tools reach the raw TR tools too
    is_error, payload = await call(
        app, "call_tool", {"name": "stock_info_basic_stock_info", "arguments": {"stk_cd": "005930"}}
    )
    assert not is_error and payload[DEMO_KEY] == DEMO_NOTICE


async def test_portfolio_is_the_demo_account(demo_app):
    app = demo_app[0]
    _, portfolio = await call(app, "get_portfolio", {})
    names = [h["name"] for h in portfolio["holdings"]]
    assert "삼성전자" in names and portfolio["account"].endswith("0001")
    assert portfolio["totals"]["total_assets"] > 0


async def test_order_flow_with_the_confirm_token_is_a_paper_trade(demo_app):
    app, api, _, _ = demo_app
    args = {"side": "buy", "stock": "삼성전자", "qty": 2, "price": "market"}
    _, preview = await call(app, "order_preview", args)
    assert preview["errors"] == [] and preview["confirm_token"]
    is_error, _ = await call(app, "place_order", args)
    assert is_error  # no token, no order
    is_error, sent = await call(
        app, "place_order", {**args, "confirm_token": preview["confirm_token"]}
    )
    assert not is_error and sent["sent"] is True and sent[DEMO_KEY] == DEMO_NOTICE
    assert api.demo_backend.book.orders[-1].filled_qty == 2
    _, orders = await call(app, "get_orders", {"status": "filled"})
    assert orders["orders"][0]["code"] == "005930"


async def test_errors_are_prefixed(demo_app):
    app = demo_app[0]
    is_error, text = await call(app, "stock_snapshot", {"stk_cd": "999999"})
    assert is_error and text.startswith("[데모]")


async def test_read_only_still_removes_order_tools(monkeypatch):
    monkeypatch.setenv("KIWOOM_MCP_READ_ONLY", "true")
    api, allow_orders, _ = mcp_server.client_and_order_settings(
        app_key="", app_secret="", is_mock=False, demo=True
    )
    await api.close()
    assert not allow_orders
