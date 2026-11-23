"""Two-step orders: order_preview issues a confirm_token, order tools redeem it.

Every refusal must leave the order endpoints untouched (pytest-httpx records
every request; nothing here reaches a real server).
"""

from __future__ import annotations

import pytest

from kiwoom_client import AsyncKiwoomAPI
from kiwoom_client.mcp.order_preview import preview_any
from kiwoom_client.mcp.orders.confirm import ConfirmError, ConfirmTokens
from kiwoom_client.mcp.orders.policy import REQUIRE_CONFIRM_ENV, OrderPolicy
from kiwoom_client.mcp.orders.tools import TOOL_NAMES
from kiwoom_client.mcp.server import build_server
from tests.mcp_order_helpers import (
    BUY,
    BUY_PARAMS,
    listed,
    mock_orders,
    mock_stock_lists,
    mock_token,
    ok,
    order_requests,
    refused,
    sent_bodies,
)

STRICT = OrderPolicy(require_confirm=True)
LAX = OrderPolicy(require_confirm=False)


class Clock:
    def __init__(self) -> None:
        self.now = 1_000_000.0

    def __call__(self) -> float:
        return self.now


class TestConfirmTokens:
    def test_round_trip(self):
        tokens = ConfirmTokens()
        token = tokens.issue("order_buy_order", BUY_PARAMS)
        tokens.redeem(token, "order_buy_order", BUY_PARAMS)

    def test_token_does_not_contain_the_parameters(self):
        token = ConfirmTokens().issue("order_buy_order", BUY_PARAMS)
        assert "005930" not in token and "70000" not in token

    def test_normalisation_ignores_types_whitespace_and_empty_fields(self):
        tokens = ConfirmTokens()
        token = tokens.issue("order_buy_order", {**BUY_PARAMS, "cond_uv": ""})
        same = {**BUY_PARAMS, "ord_qty": 10, "stk_cd": " 005930 "}
        tokens.redeem(token, "order_buy_order", same)

    @pytest.mark.parametrize(
        ("tool", "change"),
        [
            ("order_buy_order", {"ord_qty": "11"}),
            ("order_buy_order", {"ord_uv": "70100"}),
            ("order_buy_order", {"stk_cd": "000660"}),
            ("order_buy_order", {"trde_tp": "3"}),
            ("order_buy_order", {"cond_uv": "1"}),
            ("order_sell_order", {}),
        ],
    )
    def test_any_change_is_refused(self, tool, change):
        tokens = ConfirmTokens()
        token = tokens.issue("order_buy_order", BUY_PARAMS)
        with pytest.raises(ConfirmError, match="맞지 않습니다"):
            tokens.check(token, tool, {**BUY_PARAMS, **change})

    def test_single_use(self):
        tokens = ConfirmTokens()
        token = tokens.issue("order_buy_order", BUY_PARAMS)
        tokens.redeem(token, "order_buy_order", BUY_PARAMS)
        with pytest.raises(ConfirmError, match="이미 쓴"):
            tokens.check(token, "order_buy_order", BUY_PARAMS)

    def test_check_alone_does_not_use_up_the_token(self):
        tokens = ConfirmTokens()
        token = tokens.issue("order_buy_order", BUY_PARAMS)
        tokens.check(token, "order_buy_order", BUY_PARAMS)
        tokens.redeem(token, "order_buy_order", BUY_PARAMS)

    def test_expiry(self):
        clock = Clock()
        tokens = ConfirmTokens(ttl=120, clock=clock)
        token = tokens.issue("order_buy_order", BUY_PARAMS)
        clock.now += 121
        with pytest.raises(ConfirmError, match="만료"):
            tokens.check(token, "order_buy_order", BUY_PARAMS)

    def test_edited_expiry_breaks_the_mac(self):
        clock = Clock()
        tokens = ConfirmTokens(ttl=120, clock=clock)
        expires, nonce, mac = tokens.issue("order_buy_order", BUY_PARAMS).split(".")
        clock.now += 121
        forged = f"{int(expires) + 3600}.{nonce}.{mac}"
        with pytest.raises(ConfirmError, match="맞지 않습니다"):
            tokens.check(forged, "order_buy_order", BUY_PARAMS)

    def test_another_process_cannot_redeem(self):
        token = ConfirmTokens().issue("order_buy_order", BUY_PARAMS)
        with pytest.raises(ConfirmError, match="맞지 않습니다"):
            ConfirmTokens().check(token, "order_buy_order", BUY_PARAMS)

    @pytest.mark.parametrize("token", ["", None, "abc", "1.2", "x.y.z", 123])
    def test_missing_or_malformed(self, token):
        with pytest.raises(ConfirmError):
            ConfirmTokens().check(token, "order_buy_order", BUY_PARAMS)


class TestPolicyFromEnv:
    @pytest.mark.parametrize(
        ("is_mock", "value", "expected"),
        [
            (False, None, True),
            (True, None, False),
            (False, "false", False),
            (True, "true", True),
            (False, "", True),
        ],
    )
    def test_require_confirm(self, is_mock, value, expected):
        env = {} if value is None else {REQUIRE_CONFIRM_ENV: value}
        assert OrderPolicy.from_env(is_mock=is_mock, env=env).require_confirm is expected

    def test_bad_value_refuses_to_start(self):
        with pytest.raises(ValueError, match=REQUIRE_CONFIRM_ENV):
            OrderPolicy.from_env(is_mock=False, env={REQUIRE_CONFIRM_ENV: "maybe"})

    def test_build_server_default_is_strict(self):
        assert OrderPolicy().require_confirm is True


@pytest.fixture
async def api(httpx_mock):
    mock_token(httpx_mock)
    mock_orders(httpx_mock)
    api = AsyncKiwoomAPI("key", "secret", is_mock=True)
    await api.login()
    yield api
    await api.close()


async def _preview(app, arguments):
    return await ok(app, "order_preview", arguments)


class TestRawTrTools:
    async def test_preview_issues_a_token_only_when_orders_exist(self, api):
        on, _ = build_server(api, allow_live_orders=True, order_policy=STRICT)
        off, _ = build_server(api, allow_live_orders=False, order_policy=STRICT)
        assert (await _preview(on, BUY))["confirm_token"]
        assert (await _preview(on, BUY))["confirm_expires_in"] == 120
        assert "confirm_token" not in await _preview(off, BUY)

    async def test_schema_has_the_token_argument(self, api):
        app, _ = build_server(api, allow_live_orders=True, order_policy=STRICT)
        tools = await listed(app)
        assert "confirm_token" in tools["order_buy_order"].input_schema["properties"]
        assert "confirm_token" in tools["credit_order_margin_buy_order"].input_schema["properties"]

    async def test_without_token_nothing_is_sent(self, httpx_mock, api):
        app, _ = build_server(api, allow_live_orders=True, order_policy=STRICT)
        text = await refused(app, "order_buy_order", {"params": BUY_PARAMS})
        assert "confirm_token" in text
        assert order_requests(httpx_mock) == []

    async def test_with_token_sends_once_and_never_forwards_it(self, httpx_mock, api):
        app, _ = build_server(api, allow_live_orders=True, order_policy=STRICT)
        preview = await _preview(app, BUY)
        args = {"params": preview["params"], "confirm_token": preview["confirm_token"]}
        await ok(app, "order_buy_order", args)
        assert sent_bodies(httpx_mock) == [BUY_PARAMS]
        await refused(app, "order_buy_order", args)
        assert len(order_requests(httpx_mock)) == 1

    async def test_token_inside_params_is_also_accepted_and_stripped(self, httpx_mock, api):
        app, _ = build_server(api, allow_live_orders=True, order_policy=STRICT)
        preview = await _preview(app, BUY)
        params = {**preview["params"], "confirm_token": preview["confirm_token"]}
        await ok(app, "order_buy_order", {"params": params})
        assert sent_bodies(httpx_mock) == [BUY_PARAMS]

    async def test_changed_params_are_refused(self, httpx_mock, api):
        app, _ = build_server(api, allow_live_orders=True, order_policy=STRICT)
        preview = await _preview(app, BUY)
        bigger = {**preview["params"], "ord_qty": "100"}
        await refused(
            app, "order_buy_order", {"params": bigger, "confirm_token": preview["confirm_token"]}
        )
        await refused(
            app,
            "order_sell_order",
            {"params": preview["params"], "confirm_token": preview["confirm_token"]},
        )
        assert order_requests(httpx_mock) == []

    async def test_discovery_call_tool_is_gated_too(self, httpx_mock, api):
        app, _ = build_server(api, allow_live_orders=True, discovery=True, order_policy=STRICT)
        inner = {"name": "order_buy_order", "arguments": {"params": BUY_PARAMS}}
        await refused(app, "call_tool", inner)
        assert order_requests(httpx_mock) == []

    async def test_credit_order_token_via_tool_mode(self, httpx_mock, api):
        app, _ = build_server(api, allow_live_orders=True, order_policy=STRICT)
        await refused(app, "credit_order_margin_buy_order", {"params": BUY_PARAMS})
        preview = await _preview(
            app, {"tool": "credit_order_margin_buy_order", "params": BUY_PARAMS}
        )
        assert preview["estimated_amount"] == 700000
        await ok(
            app,
            "credit_order_margin_buy_order",
            {"params": BUY_PARAMS, "confirm_token": preview["confirm_token"]},
        )
        assert sent_bodies(httpx_mock) == [BUY_PARAMS]

    async def test_tool_mode_checks_required_fields_and_tool_name(self, api):
        app, _ = build_server(api, allow_live_orders=True, order_policy=STRICT)
        await refused(app, "order_preview", {"tool": "order_buy_order", "params": {"stk_cd": "1"}})
        await refused(app, "order_preview", {"tool": "account_deposit_detail", "params": {}})

    async def test_lax_policy_sends_without_token_but_still_checks_a_given_one(
        self, httpx_mock, api
    ):
        app, _ = build_server(api, allow_live_orders=True, order_policy=LAX)
        await ok(app, "order_buy_order", {"params": BUY_PARAMS})
        await refused(app, "order_buy_order", {"params": BUY_PARAMS, "confirm_token": "1.2.3"})
        assert len(order_requests(httpx_mock)) == 1

    async def test_default_build_server_policy_requires_a_token(self, httpx_mock, api):
        app, _ = build_server(api, allow_live_orders=True)
        await refused(app, "order_buy_order", {"params": BUY_PARAMS})
        assert order_requests(httpx_mock) == []


class TestHighLevelTools:
    async def test_registered_only_with_the_opt_in(self, api):
        off, _ = build_server(api, allow_live_orders=False)
        on, _ = build_server(api, allow_live_orders=True)
        assert not TOOL_NAMES & set(await listed(off))
        tools = await listed(on)
        assert set(tools) >= TOOL_NAMES
        for name in TOOL_NAMES:
            ann = tools[name].annotations
            assert ann.destructive_hint is True and ann.read_only_hint is False
            assert "confirm_token" in tools[name].input_schema["required"]

    async def test_place_order_by_name(self, httpx_mock, api):
        mock_stock_lists(httpx_mock)
        # Even the lax policy does not relax the high-level tools.
        app, _ = build_server(api, allow_live_orders=True, order_policy=LAX)
        args = {"stock": "삼성전자", "side": "buy", "qty": 10, "price": 70050}
        await refused(app, "place_order", args)
        preview = await _preview(app, args)
        assert preview["params"] == BUY_PARAMS
        sent = await ok(app, "place_order", {**args, "confirm_token": preview["confirm_token"]})
        assert sent["sent"] is True and sent["tool"] == "order_buy_order"
        assert sent_bodies(httpx_mock) == [BUY_PARAMS]

    async def test_preview_token_fits_the_raw_tool_too(self, httpx_mock, api):
        app, _ = build_server(api, allow_live_orders=True, order_policy=STRICT)
        market_sell = {"side": "sell", "stock": "005930", "qty": 1, "price": "market"}
        preview = await _preview(app, market_sell)
        assert preview["params"]["trde_tp"] == "3" and preview["params"]["ord_uv"] == ""
        await ok(
            app,
            "order_sell_order",
            {"params": preview["params"], "confirm_token": preview["confirm_token"]},
        )
        assert sent_bodies(httpx_mock)[0]["trde_tp"] == "3"

    async def test_changed_argument_is_refused(self, httpx_mock, api):
        app, _ = build_server(api, allow_live_orders=True)
        args = {"stock": "005930", "side": "buy", "qty": 10, "price": 70000}
        token = (await _preview(app, args))["confirm_token"]
        await refused(app, "place_order", {**args, "qty": 11, "confirm_token": token})
        await refused(app, "place_order", {**args, "side": "sell", "confirm_token": token})
        assert order_requests(httpx_mock) == []

    async def test_cancel_all(self, httpx_mock, api):
        app, _ = build_server(api, allow_live_orders=True)
        args = {"order_no": "0000123", "stock": "005930"}
        preview = await _preview(app, {**args, "action": "cancel", "qty": "all"})
        await ok(app, "cancel_order", {**args, "confirm_token": preview["confirm_token"]})
        assert sent_bodies(httpx_mock) == [
            {"dmst_stex_tp": "KRX", "orig_ord_no": "0000123", "stk_cd": "005930", "cncl_qty": "0"}
        ]

    async def test_modify(self, httpx_mock, api):
        app, _ = build_server(api, allow_live_orders=True)
        args = {"order_no": "0000123", "stock": "005930", "qty": 5, "price": 69900}
        preview = await _preview(app, {**args, "action": "modify"})
        await ok(app, "modify_order", {**args, "confirm_token": preview["confirm_token"]})
        assert sent_bodies(httpx_mock)[0]["mdfy_uv"] == "69900"

    async def test_modify_off_tick_needs_a_side(self, api):
        app, _ = build_server(api, allow_live_orders=True)
        args = {"action": "modify", "order_no": "1", "stock": "005930", "qty": 1, "price": 69950}
        assert "호가단위" in await refused(app, "order_preview", args)
        snapped = await _preview(app, {**args, "side": "sell"})
        assert snapped["params"]["mdfy_uv"] == "70000"


class TestPreviewModes:
    def test_market_price_alias(self):
        result = preview_any(
            {"side": "buy", "stock": "005930", "qty": 1, "price": "market"},
            order_tools_enabled=True,
        )
        assert result["params"]["trde_tp"] == "3"

    def test_market_with_a_limit_trade_type_is_an_error(self):
        with pytest.raises(ValueError, match="market"):
            preview_any(
                {"side": "buy", "stock": "005930", "qty": 1, "price": "market", "trde_tp": "0"},
                order_tools_enabled=True,
            )

    def test_unknown_action(self):
        with pytest.raises(ValueError, match="action"):
            preview_any({"action": "short"}, order_tools_enabled=True)

    async def test_name_needs_a_connection(self):
        app, _ = build_server(api=None, allow_live_orders=False)
        text = await refused(app, "order_preview", {"side": "buy", "stock": "삼성전자", "qty": 1})
        assert "종목코드" in text
