"""rebalance_plan: pure quantity maths, and the tool path that never sends an order."""

from __future__ import annotations

import pytest

from kiwoom_client.mcp.intents.portfolio import HOLDINGS_KEY
from kiwoom_client.mcp.intents.rebalance import Position, normalize_weights, plan_rebalance
from kiwoom_client.mcp.server import build_server
from kiwoom_client.tick_size import is_on_tick

from .intent_support import ACNT, BASE, STKINFO, call, mock_api, mock_listing

ORDER_PATHS = ("/api/dostk/ordr", "/api/dostk/crdordr")


@pytest.fixture
async def api(httpx_mock):
    async with mock_api(httpx_mock) as client:
        yield client


SAMSUNG = Position("005930", "삼성전자", qty=100, sellable_qty=100, price=70000)
HYNIX = Position("000660", "SK하이닉스", qty=0, sellable_qty=0, price=0)


class TestWeights:
    def test_fractions_and_percents(self):
        assert normalize_weights({"a": 0.5, "b": 0.25}) == ({"a": 0.5, "b": 0.25}, 0.0)
        assert normalize_weights({"a": 50, "b": "25%"}) == ({"a": 0.5, "b": 0.25}, 0.0)

    def test_cash_key(self):
        stocks, cash = normalize_weights({"삼성전자": 60, "현금": 40})
        assert stocks == {"삼성전자": 0.6} and cash == 0.4

    @pytest.mark.parametrize(
        "raw", [{"a": 0.7, "b": 0.4}, {"a": -0.1}, {"a": "x"}, {}, {"현금": 1}, ["a"]]
    )
    def test_rejects(self, raw):
        with pytest.raises(ValueError):
            normalize_weights(raw)


class TestPlan:
    def test_sell_down_and_buy_new_with_whole_shares(self):
        # investable = 100*70,000 + 3,000,000 = 10,000,000
        plan = plan_rebalance(
            [SAMSUNG], 3_000_000, {"005930": 0.5, "000660": 0.3}, {"000660": 180_500}
        )
        sell, buy = plan.orders
        assert (sell["action"], sell["code"], sell["qty"]) == ("sell", "005930", 29)
        assert sell["target_qty"] == 71  # floor(5,000,000 / 70,000)
        assert (buy["action"], buy["code"], buy["qty"]) == ("buy", "000660", 16)
        assert buy["price"] == 180_500 and is_on_tick(buy["price"])
        assert plan.summary["buy_amount"] <= 3_000_000 + plan.summary["sell_amount"]
        assert plan.basis["investable"] == 10_000_000
        assert buy["order_preview_args"] == {
            "action": "new", "side": "buy", "stock": "000660", "qty": 16, "price": 180_500,
            "trde_tp": "0", "dmst_stex_tp": "KRX",
        }  # fmt: skip

    def test_off_tick_prices_round_buy_down_and_sell_up(self):
        held = Position("111111", None, qty=10, sellable_qty=10, price=70_050)
        plan = plan_rebalance([held], 0, {"111111": 0.0, "222222": 0.5}, {"222222": 70_050})
        sell = next(r for r in plan.orders if r["action"] == "sell")
        buy = next(r for r in plan.orders if r["action"] == "buy")
        assert sell["price"] == 70_100 and buy["price"] == 70_000

    def test_holdings_outside_targets_are_left_alone(self):
        other = Position("035720", "카카오", qty=10, sellable_qty=10, price=40_000)
        plan = plan_rebalance([SAMSUNG, other], 0, {"005930": 1.0}, {})
        assert all(r["code"] != "035720" for r in plan.orders)
        assert plan.basis["untouched"] == ["035720"]
        assert plan.basis["investable"] == 7_000_000

    def test_sell_unlisted_sells_them(self):
        other = Position("035720", "카카오", qty=10, sellable_qty=10, price=40_000)
        plan = plan_rebalance([SAMSUNG, other], 0, {"005930": 1.0}, {}, sell_unlisted=True)
        (sell,) = [r for r in plan.orders if r["action"] == "sell"]
        assert (sell["code"], sell["qty"]) == ("035720", 10)

    def test_sell_is_capped_at_sellable_and_buys_are_trimmed_to_cash(self):
        locked = Position("005930", "삼성전자", qty=100, sellable_qty=0, price=70_000)
        plan = plan_rebalance(
            [locked], 100_000, {"005930": 0.2, "000660": 0.5}, {"000660": 100_000}
        )
        assert [r["action"] for r in plan.orders] == ["buy"]
        assert plan.orders[0]["qty"] == 1  # 현금 100,000 원으로 1주만
        assert plan.summary["cash_after_estimate"] >= 0
        assert any("매도가능" in w for w in plan.warnings)
        assert any("줄였습니다" in w for w in plan.warnings)

    def test_cash_buffer_is_kept(self):
        plan = plan_rebalance(
            [], 1_000_000, {"000660": 1.0}, {"000660": 100_000}, cash_buffer=300_000
        )
        assert plan.orders[0]["qty"] == 7
        assert plan.summary["cash_after_estimate"] >= 300_000

    def test_nothing_to_invest_and_unknown_price(self):
        with pytest.raises(ValueError):
            plan_rebalance([], 0, {"000660": 1.0}, {"000660": 1000})
        with pytest.raises(ValueError, match="현재가"):
            plan_rebalance([], 1000, {"000660": 1.0}, {})


def _mock_account(httpx_mock):
    holding = {
        "stk_cd": "A005930", "stk_nm": "삼성전자", "rmnd_qty": "000000000000100",
        "trde_able_qty": "000000000000100", "cur_prc": "000000070000",
        "evlt_amt": "000000007000000", "pur_pric": "000000060000",
    }  # fmt: skip
    httpx_mock.add_response(
        url=ACNT,
        match_headers={"api-id": "kt00018"},
        json={"return_code": 0, HOLDINGS_KEY: [holding]},
    )
    httpx_mock.add_response(
        url=ACNT,
        match_headers={"api-id": "kt00001"},
        json={"return_code": 0, "d2_entra": "000000003000000"},
    )
    httpx_mock.add_response(
        url=ACNT,
        match_headers={"api-id": "ka00001"},
        json={"return_code": 0, "acctNo": "9876543210"},
    )
    httpx_mock.add_response(
        url=STKINFO,
        match_headers={"api-id": "ka10095"},
        json={"return_code": 0, "atn_stk_infr": [
            {"stk_cd": "005930", "stk_nm": "삼성전자", "cur_prc": "-70000"},
            {"stk_cd": "000660", "stk_nm": "SK하이닉스", "cur_prc": "+180500"},
        ]},
    )  # fmt: skip


async def test_tool_plans_without_sending_and_previews_accept_the_args(httpx_mock, api):
    mock_listing(httpx_mock)
    _mock_account(httpx_mock)
    # order_preview's own live checks (price limits, orderable qty) get an empty OK.
    httpx_mock.add_response(json={"return_code": 0}, is_reusable=True, is_optional=True)
    app, _specs = build_server(api, allow_live_orders=False)
    args = {"targets": {"삼성전자": 50, "000660": 30}}
    is_error, out = await call(app, "rebalance_plan", args)
    assert is_error is False, out
    assert out["sent"] is False
    assert out["account"] == "******3210"
    assert [(r["action"], r["code"]) for r in out["orders"]] == [
        ("sell", "005930"),
        ("buy", "000660"),
    ]
    for row in out["orders"]:
        is_error, preview = await call(app, "order_preview", row["order_preview_args"])
        assert is_error is False, preview
        assert preview["sent"] is False
        assert preview["params"]["ord_qty"] == str(row["qty"])
    sent = [r.url.path for r in httpx_mock.get_requests() if r.url.path in ORDER_PATHS]
    assert sent == []
    assert str(httpx_mock.get_requests()[0].url).startswith(BASE)


async def test_unresolvable_target_is_an_error(httpx_mock, api):
    mock_listing(httpx_mock)
    app, _specs = build_server(api, allow_live_orders=False)
    is_error, text = await call(app, "rebalance_plan", {"targets": {"삼성": 0.5}})
    assert is_error is True and "후보" in text
