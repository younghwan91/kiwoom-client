"""The same order sent again within the duplicate window is refused, unsent."""

from __future__ import annotations

import pytest

from kiwoom_client import AsyncKiwoomAPI
from kiwoom_client.mcp.orders.gate import OrderCall, OrderGate
from kiwoom_client.mcp.orders.policy import DUPLICATE_WINDOW_ENV, OrderPolicy
from kiwoom_client.mcp.server import build_server
from tests.mcp_order_helpers import (
    BUY,
    BUY_PARAMS,
    mock_lookups,
    mock_orders,
    mock_token,
    ok,
    order_requests,
    refused,
)


class Clock:
    def __init__(self) -> None:
        self.now = 100.0

    def __call__(self) -> float:
        return self.now


async def _sender():
    return {"return_code": 0}


class TestGate:
    async def test_same_order_within_the_window_is_refused(self):
        clock = Clock()
        gate = OrderGate(OrderPolicy(require_confirm=False), monotonic=clock)
        call = OrderCall("order_buy_order", BUY_PARAMS)
        await gate.send(call, None, require_token=False, sender=_sender)
        clock.now += 9.9
        with pytest.raises(ValueError, match="중복"):
            await gate.send(call, None, require_token=False, sender=_sender)
        clock.now += 0.1
        await gate.send(call, None, require_token=False, sender=_sender)

    async def test_normalised_equal_orders_count_as_the_same(self):
        gate = OrderGate(OrderPolicy(require_confirm=False), monotonic=Clock())
        await gate.send(OrderCall("order_buy_order", BUY_PARAMS), None,
                        require_token=False, sender=_sender)  # fmt: skip
        same = {**BUY_PARAMS, "ord_qty": 10, "cond_uv": ""}
        with pytest.raises(ValueError, match="중복"):
            await gate.send(OrderCall("order_buy_order", same), None,
                            require_token=False, sender=_sender)  # fmt: skip

    @pytest.mark.parametrize(
        ("tool", "change"),
        [
            ("order_buy_order", {"ord_qty": "11"}),
            ("order_sell_order", {}),
            ("credit_order_margin_buy_order", {}),
        ],
    )
    async def test_a_different_order_is_not_a_duplicate(self, tool, change):
        gate = OrderGate(OrderPolicy(require_confirm=False), monotonic=Clock())
        await gate.send(OrderCall("order_buy_order", BUY_PARAMS), None,
                        require_token=False, sender=_sender)  # fmt: skip
        await gate.send(OrderCall(tool, {**BUY_PARAMS, **change}), None,
                        require_token=False, sender=_sender)  # fmt: skip

    async def test_zero_turns_it_off(self):
        gate = OrderGate(OrderPolicy(require_confirm=False, duplicate_window=0))
        call = OrderCall("order_buy_order", BUY_PARAMS)
        await gate.send(call, None, require_token=False, sender=_sender)
        await gate.send(call, None, require_token=False, sender=_sender)

    async def test_a_refused_order_is_not_remembered(self):
        gate = OrderGate(OrderPolicy(require_confirm=False, max_order_qty=1), monotonic=Clock())
        call = OrderCall("order_buy_order", BUY_PARAMS)
        with pytest.raises(ValueError, match="MAX_ORDER_QTY"):
            await gate.send(call, None, require_token=False, sender=_sender)
        assert gate.duplicate_of_recent(call) is None


class TestPolicy:
    def test_default_is_ten_seconds(self):
        assert OrderPolicy.from_env(is_mock=True, env={}).duplicate_window == 10
        assert OrderPolicy.from_env(is_mock=False, env={}).duplicate_window == 10

    def test_env(self):
        env = {DUPLICATE_WINDOW_ENV: "30"}
        assert OrderPolicy.from_env(is_mock=False, env=env).duplicate_window == 30
        env = {DUPLICATE_WINDOW_ENV: "0"}
        assert OrderPolicy.from_env(is_mock=False, env=env).duplicate_window == 0

    @pytest.mark.parametrize("value", ["-1", "ten", "1.5"])
    def test_bad_value(self, value):
        with pytest.raises(ValueError, match=DUPLICATE_WINDOW_ENV):
            OrderPolicy.from_env(is_mock=False, env={DUPLICATE_WINDOW_ENV: value})


@pytest.fixture
async def api(httpx_mock):
    mock_token(httpx_mock)
    mock_orders(httpx_mock)
    mock_lookups(httpx_mock)
    api = AsyncKiwoomAPI("key", "secret", is_mock=True)
    await api.login()
    yield api
    await api.close()


class TestThroughTheServer:
    async def test_second_preview_and_token_cannot_resend_the_same_order(self, httpx_mock, api):
        app, _ = build_server(api, allow_live_orders=True, order_policy=OrderPolicy())
        args = {"stock": "005930", "side": "buy", "qty": 10, "price": 70000}
        first = await ok(app, "order_preview", args)
        await ok(app, "place_order", {**args, "confirm_token": first["confirm_token"]})
        second = await ok(app, "order_preview", args)
        assert any("중복" in w for w in second["warnings"])
        text = await refused(app, "place_order", {**args, "confirm_token": second["confirm_token"]})
        assert "중복" in text
        assert len(order_requests(httpx_mock)) == 1

    async def test_raw_tool_without_confirm_is_deduplicated_too(self, httpx_mock, api):
        policy = OrderPolicy(require_confirm=False)
        app, _ = build_server(api, allow_live_orders=True, order_policy=policy)
        await ok(app, "order_buy_order", {"params": BUY_PARAMS})
        await refused(app, "order_buy_order", {"params": BUY_PARAMS})
        await refused(app, "order_buy_order", BUY_PARAMS)  # flat arguments, same body
        assert len(order_requests(httpx_mock)) == 1

    async def test_preview_alone_never_counts_as_a_send(self, httpx_mock, api):
        policy = OrderPolicy(require_confirm=False)
        app, _ = build_server(api, allow_live_orders=True, order_policy=policy)
        await ok(app, "order_preview", BUY)
        await ok(app, "order_buy_order", {"params": BUY_PARAMS})
