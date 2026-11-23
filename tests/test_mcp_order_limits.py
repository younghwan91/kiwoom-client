"""Order limits and the stock allowlist, enforced in order_preview and again
right before sending. Every refusal must leave the order endpoints untouched."""

from __future__ import annotations

from datetime import date, datetime

import pytest

from kiwoom_client import AsyncKiwoomAPI
from kiwoom_client.mcp.orders.gate import OrderCall, OrderGate, order_facts
from kiwoom_client.mcp.orders.policy import (
    ALLOWED_STOCKS_ENV,
    DAILY_ORDER_LIMIT_ENV,
    MAX_ORDER_AMOUNT_ENV,
    MAX_ORDER_QTY_ENV,
    OrderPolicy,
)
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

CANCEL_PARAMS = {"dmst_stex_tp": "KRX", "orig_ord_no": "1", "stk_cd": "005930", "cncl_qty": "0"}


class TestPolicyFromEnv:
    def test_unset_means_no_limit(self):
        policy = OrderPolicy.from_env(is_mock=False, env={})
        assert policy.max_order_amount is None
        assert policy.max_order_qty is None
        assert policy.allowed_stocks is None
        assert policy.daily_order_limit is None

    def test_values(self):
        policy = OrderPolicy.from_env(
            is_mock=False,
            env={
                MAX_ORDER_AMOUNT_ENV: "1,000,000",
                MAX_ORDER_QTY_ENV: "50",
                ALLOWED_STOCKS_ENV: " 005930, 000660 ,,",
                DAILY_ORDER_LIMIT_ENV: "20",
            },
        )
        assert policy.max_order_amount == 1_000_000
        assert policy.max_order_qty == 50
        assert policy.allowed_stocks == {"005930", "000660"}
        assert policy.daily_order_limit == 20

    @pytest.mark.parametrize(
        ("name", "value"),
        [
            (MAX_ORDER_AMOUNT_ENV, "lots"),
            (MAX_ORDER_QTY_ENV, "0"),
            (MAX_ORDER_QTY_ENV, "-5"),
            (DAILY_ORDER_LIMIT_ENV, "1.5"),
            (ALLOWED_STOCKS_ENV, " , "),
        ],
    )
    def test_bad_value_refuses_to_start(self, name, value):
        with pytest.raises(ValueError, match=name):
            OrderPolicy.from_env(is_mock=False, env={name: value})


class TestFacts:
    def test_reads_each_kind(self):
        assert order_facts(OrderCall("order_buy_order", BUY_PARAMS)).qty == 10
        modify = order_facts(
            OrderCall("credit_order_margin_modify_order", {"stk_cd": "005930", "mdfy_qty": "3",
                                                           "mdfy_uv": "1000"})
        )  # fmt: skip
        assert (modify.kind, modify.qty, modify.price) == ("modify", 3, 1000)
        assert order_facts(OrderCall("order_cancel_order", CANCEL_PARAMS)).kind == "cancel"


@pytest.fixture
async def api(httpx_mock):
    mock_token(httpx_mock)
    mock_orders(httpx_mock)
    mock_lookups(httpx_mock)  # quote: 상한가 91,000 / 하한가 49,000
    api = AsyncKiwoomAPI("key", "secret", is_mock=True)
    await api.login()
    yield api
    await api.close()


def _app(api, **limits):
    # require_confirm=False isolates the limits: nothing but them can refuse.
    policy = OrderPolicy(require_confirm=False, **limits)
    app, _ = build_server(api, allow_live_orders=True, order_policy=policy)
    return app


class TestEnforcedBeforeSending:
    @pytest.mark.parametrize(
        ("limits", "word"),
        [
            ({"max_order_qty": 9}, "KIWOOM_MCP_MAX_ORDER_QTY"),
            ({"max_order_amount": 699_999}, "KIWOOM_MCP_MAX_ORDER_AMOUNT"),
            ({"allowed_stocks": frozenset({"000660"})}, "KIWOOM_MCP_ALLOWED_STOCKS"),
        ],
    )
    async def test_raw_tool_over_limit_sends_nothing(self, httpx_mock, api, limits, word):
        app = _app(api, **limits)
        assert word in await refused(app, "order_buy_order", {"params": BUY_PARAMS})
        assert order_requests(httpx_mock) == []

    async def test_at_the_limit_is_allowed(self, httpx_mock, api):
        app = _app(api, max_order_qty=10, max_order_amount=700_000,
                   allowed_stocks=frozenset({"005930"}))  # fmt: skip
        await ok(app, "order_buy_order", {"params": BUY_PARAMS})
        assert len(order_requests(httpx_mock)) == 1

    async def test_unset_limits_change_nothing(self, httpx_mock, api):
        app = _app(api)
        await ok(app, "order_buy_order", {"params": {**BUY_PARAMS, "ord_qty": "100000"}})
        assert len(order_requests(httpx_mock)) == 1

    async def test_market_order_amount_is_bounded_at_the_upper_limit(self, httpx_mock, api):
        market = {**BUY_PARAMS, "ord_uv": "", "trde_tp": "3"}
        app = _app(api, max_order_amount=10 * 91_000 - 1)
        assert "상한가" in await refused(app, "order_buy_order", {"params": market})
        assert order_requests(httpx_mock) == []
        app = _app(api, max_order_amount=10 * 91_000)
        await ok(app, "order_buy_order", {"params": market})

    async def test_market_order_without_a_quote_is_refused_when_amount_is_limited(self):
        gate = OrderGate(OrderPolicy(max_order_amount=1))
        market = OrderCall("order_buy_order", {**BUY_PARAMS, "ord_uv": "", "trde_tp": "3"})
        assert any("추정하지 못해" in p for p in await gate.problems(market))

    async def test_discovery_route_is_limited_too(self, httpx_mock, api):
        policy = OrderPolicy(require_confirm=False, max_order_qty=1)
        app, _ = build_server(api, allow_live_orders=True, mode="discovery", order_policy=policy)
        inner = {"name": "order_buy_order", "arguments": {"params": BUY_PARAMS}}
        await refused(app, "call_tool", inner)
        assert order_requests(httpx_mock) == []

    async def test_cancel_ignores_size_limits_but_not_the_allowlist(self, httpx_mock, api):
        app = _app(api, max_order_qty=1, max_order_amount=1)
        await ok(app, "order_cancel_order", {"params": CANCEL_PARAMS})
        app = _app(api, allowed_stocks=frozenset({"000660"}))
        await refused(app, "order_cancel_order", {"params": CANCEL_PARAMS})
        assert len(order_requests(httpx_mock)) == 1


class TestDailyLimit:
    async def test_counts_every_send_and_refuses_after_the_limit(self, httpx_mock, api):
        app = _app(api, daily_order_limit=2)
        await ok(app, "order_buy_order", {"params": BUY_PARAMS})
        await ok(app, "order_cancel_order", {"params": CANCEL_PARAMS})
        text = await refused(app, "order_buy_order", {"params": BUY_PARAMS})
        assert "KIWOOM_MCP_DAILY_ORDER_LIMIT" in text
        assert len(order_requests(httpx_mock)) == 2

    async def test_refusals_do_not_count(self, httpx_mock, api):
        app = _app(api, daily_order_limit=1, max_order_qty=1)
        await refused(app, "order_buy_order", {"params": BUY_PARAMS})
        await ok(app, "order_buy_order", {"params": {**BUY_PARAMS, "ord_qty": "1"}})

    async def test_resets_on_a_new_day(self):
        today = [date(2026, 11, 24)]
        gate = OrderGate(
            OrderPolicy(require_confirm=False, daily_order_limit=1),
            now=lambda: datetime.combine(today[0], datetime.min.time()),
        )
        call = OrderCall("order_buy_order", BUY_PARAMS)

        async def sender():
            return {}

        await gate.send(call, None, require_token=False, sender=sender)
        assert await gate.problems(call)  # limit reached today
        today[0] = date(2026, 11, 25)
        assert await gate.problems(call) == []


class TestPreview:
    async def test_limit_errors_withhold_the_token(self, httpx_mock, api):
        app = _app(api, max_order_qty=5)
        result = await ok(app, "order_preview", BUY)
        assert any("KIWOOM_MCP_MAX_ORDER_QTY" in e for e in result["errors"])
        assert "confirm_token" not in result

    async def test_place_order_cannot_get_past_the_allowlist(self, httpx_mock, api):
        policy = OrderPolicy(allowed_stocks=frozenset({"000660"}))
        app, _ = build_server(api, allow_live_orders=True, order_policy=policy)
        args = {"stock": "005930", "side": "buy", "qty": 10, "price": 70000}
        preview = await ok(app, "order_preview", args)
        assert preview["errors"] and "confirm_token" not in preview
        await refused(app, "place_order", {**args, "confirm_token": "1.2.3"})
        assert order_requests(httpx_mock) == []

    async def test_token_issued_before_a_limit_still_meets_the_send_check(self, httpx_mock, api):
        """The limits are re-checked at send time, not trusted from the preview."""
        app, _ = build_server(
            api, allow_live_orders=True, order_policy=OrderPolicy(daily_order_limit=1)
        )
        first = await ok(app, "order_preview", BUY)
        second = await ok(app, "order_preview", BUY)
        await ok(
            app, "order_buy_order", {"params": BUY_PARAMS, "confirm_token": first["confirm_token"]}
        )
        await refused(
            app, "order_buy_order", {"params": BUY_PARAMS, "confirm_token": second["confirm_token"]}
        )
        assert len(order_requests(httpx_mock)) == 1
