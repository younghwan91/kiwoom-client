"""Regression bundle for the order-safety layers behind the opt-in guard.

Every blocking condition — no confirm token, a limit, the allowlist, the
field allowlist, a duplicate, the daily cap, read-only mode — is tried on
every route an agent has to an order: the raw TR tool called directly (full
mode), through ``call_tool`` (discovery and smart modes), and the high-level
``place_order``. Each must leave the order endpoints without a single new
request. A positive control proves the same routes do send when nothing
blocks, so the zero counts are not vacuous.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from typing import Any

import pytest

from kiwoom_client import AsyncKiwoomAPI
from kiwoom_client.mcp.guard import READ_ONLY_ENV, order_tools_allowed
from kiwoom_client.mcp.orders.policy import OrderPolicy
from kiwoom_client.mcp.server import build_server
from tests.mcp_order_helpers import (
    BUY_PARAMS,
    call,
    mock_lookups,
    mock_orders,
    mock_token,
    order_requests,
)

PLACE_ARGS = {"stock": "005930", "side": "buy", "qty": 10, "price": 70000}

#: (mode, how the tool is reached)
ROUTES = [
    pytest.param("full", "direct", id="full-direct"),
    pytest.param("discovery", "call_tool", id="discovery-call_tool"),
    pytest.param("smart", "call_tool", id="smart-call_tool"),
]
TOOLS = [
    pytest.param("order_buy_order", id="raw-tr"),
    pytest.param("place_order", id="place_order"),
]


@dataclass
class Scenario:
    policy: OrderPolicy = field(default_factory=OrderPolicy)
    params: dict[str, Any] = field(default_factory=lambda: dict(BUY_PARAMS))
    read_only: bool = False
    #: orders sent first, untouched by the check under test (dup/daily)
    warm_up: int = 0
    #: whether to pass the token the preview gives (None if it gives none)
    with_token: bool = True
    #: the refusal must name this — proves the intended check fired
    reason: str = ""


SCENARIOS = {
    "no-token": Scenario(with_token=False, reason="confirm_token 이 없습니다"),
    "forged-token": Scenario(with_token=False, reason="맞지 않습니다"),
    "over-qty": Scenario(policy=OrderPolicy(max_order_qty=9), reason="MAX_ORDER_QTY"),
    "over-amount": Scenario(
        policy=OrderPolicy(max_order_amount=699_999), reason="MAX_ORDER_AMOUNT"
    ),
    "outside-allowlist": Scenario(
        policy=OrderPolicy(allowed_stocks=frozenset({"000660"})), reason="ALLOWED_STOCKS"
    ),
    "unknown-field": Scenario(params={**BUY_PARAMS, "injected": "1"}, reason="받지 않는"),
    "duplicate": Scenario(warm_up=1, reason="중복"),
    "daily-cap": Scenario(
        policy=OrderPolicy(daily_order_limit=1), warm_up=1, reason="DAILY_ORDER_LIMIT"
    ),
    "read-only": Scenario(read_only=True, reason="Unknown tool"),
}


@pytest.fixture
async def api(httpx_mock):
    mock_token(httpx_mock)
    mock_orders(httpx_mock)
    mock_lookups(httpx_mock)
    api = AsyncKiwoomAPI("key", "secret", is_mock=True)
    await api.login()
    yield api
    await api.close()


async def _reach(app, route: str, name: str, arguments: dict[str, Any]):
    if route == "direct":
        return await call(app, name, arguments)
    return await call(app, "call_tool", {"name": name, "arguments": arguments})


def _arguments(tool: str, params: dict[str, Any]) -> dict[str, Any]:
    if tool == "order_buy_order":
        return {"params": params}
    extra = {k: v for k, v in params.items() if k not in BUY_PARAMS}  # injected keys
    return {**PLACE_ARGS, **extra}


def _preview_arguments(tool: str, params: dict[str, Any]) -> dict[str, Any]:
    if tool == "order_buy_order":
        return {"tool": "order_buy_order", "params": params}
    return dict(PLACE_ARGS)


async def _token(app, route: str, tool: str, params: dict[str, Any]) -> str | None:
    result = await _reach(app, route, "order_preview", _preview_arguments(tool, params))
    if result.is_error:
        return None
    return json.loads(result.content[0].text).get("confirm_token")


async def _send_ok(app, route, tool, params) -> None:
    token = await _token(app, route, tool, params)
    args = {**_arguments(tool, params), "confirm_token": token}
    result = await _reach(app, route, tool, args)
    assert result.is_error is False, result.content[0].text


@pytest.mark.parametrize(("mode", "route"), ROUTES)
@pytest.mark.parametrize("tool", TOOLS)
@pytest.mark.parametrize("name", list(SCENARIOS))
async def test_blocked_order_never_reaches_kiwoom(httpx_mock, api, mode, route, tool, name):
    scenario = SCENARIOS[name]
    allow = order_tools_allowed(
        is_mock=True, env={READ_ONLY_ENV: "true"} if scenario.read_only else {}
    )
    app, _ = build_server(api, allow_live_orders=allow, mode=mode, order_policy=scenario.policy)

    for _ in range(scenario.warm_up):
        await _send_ok(app, route, tool, BUY_PARAMS)
    before = len(order_requests(httpx_mock))
    assert before == scenario.warm_up

    token = await _token(app, route, tool, scenario.params) if scenario.with_token else None
    if name == "forged-token":
        token = "9999999999.0000000000000000.deadbeef"
    args = _arguments(tool, scenario.params)
    if token is not None:
        args["confirm_token"] = token
    result = await _reach(app, route, tool, args)

    assert result.is_error is True, (name, result.content[0].text)
    assert scenario.reason in result.content[0].text, (name, result.content[0].text)
    assert len(order_requests(httpx_mock)) == before, name


@pytest.mark.parametrize(("mode", "route"), ROUTES)
@pytest.mark.parametrize("tool", TOOLS)
async def test_positive_control_sends_exactly_once(httpx_mock, api, mode, route, tool):
    app, _ = build_server(api, allow_live_orders=True, mode=mode, order_policy=OrderPolicy())
    await _send_ok(app, route, tool, BUY_PARAMS)
    assert len(order_requests(httpx_mock)) == 1
