"""Demo paper trading: orders fill or rest in memory, nothing is sent anywhere."""

from __future__ import annotations

from datetime import date

import pytest

from kiwoom_client import KiwoomAPI
from kiwoom_client.base import KiwoomAPIError
from kiwoom_client.demo import DEMO_BASE_URL, DEMO_KEY, DemoBackend
from kiwoom_client.demo.paper import STARTING_CASH, STARTING_HOLDINGS
from kiwoom_client.tick_size import tick_size
from tests.demo_support import no_network  # noqa: F401

pytestmark = pytest.mark.usefixtures("no_network")


@pytest.fixture
def demo():
    backend = DemoBackend(today=date(2026, 11, 27))
    api = backend.attach(KiwoomAPI("k", "s", base_url=DEMO_BASE_URL, rate_limit=None))
    with api:
        yield api, backend


def _holding(api, code):
    bal = api.account.evaluation_balance_detail(qry_tp="1", dmst_stex_tp="KRX")
    rows = [r for r in bal["acnt_evlt_remn_indv_tot"] if r["stk_cd"].endswith(code)]
    return rows[0] if rows else None


def _cash(api):
    return int(api.account.deposit_detail(qry_tp="3")["ord_alow_amt"])


def test_market_buy_fills_at_the_current_price(demo):
    api, backend = demo
    price = backend.market.price("000660")
    result = api.order.buy_order(dmst_stex_tp="KRX", stk_cd="000660", ord_qty="3", trde_tp="3")
    assert result["ord_no"] and result[DEMO_KEY] and "전송하지 않음" in result["return_msg"]
    held = _holding(api, "000660")
    assert int(held["rmnd_qty"]) == STARTING_HOLDINGS["000660"][0] + 3
    assert _cash(api) == STARTING_CASH - 3 * price - int(3 * price * 0.00015)
    filled = api.account.filled_orders(qry_tp="0", sell_tp="0", stex_tp="0")["cntr"]
    assert filled[0]["ord_no"] == result["ord_no"] and filled[0]["cntr_qty"] == "3"


def test_limit_below_the_price_rests_then_cancel_frees_the_cash(demo):
    api, backend = demo
    price = backend.market.price("005930")
    low = price - 5 * int(tick_size(price))
    order = api.order.buy_order(
        dmst_stex_tp="KRX", stk_cd="005930", ord_qty="10", ord_uv=str(low), trde_tp="0"
    )
    open_ = api.account.unfilled_orders(all_stk_tp="0", trde_tp="0", stex_tp="0")["oso"]
    assert [o["ord_no"] for o in open_] == [order["ord_no"]] and open_[0]["oso_qty"] == "10"
    assert _cash(api) < STARTING_CASH  # reserved
    api.order.cancel_order(
        dmst_stex_tp="KRX", orig_ord_no=order["ord_no"], stk_cd="005930", cncl_qty="0"
    )
    assert api.account.unfilled_orders(all_stk_tp="0", trde_tp="0", stex_tp="0")["oso"] == []
    assert _cash(api) == STARTING_CASH


def test_modify_to_a_marketable_price_fills(demo):
    api, backend = demo
    price = backend.market.price("035420")
    high = price + 3 * int(tick_size(price))
    order = api.order.sell_order(
        dmst_stex_tp="KRX", stk_cd="035420", ord_qty="5", ord_uv=str(high), trde_tp="0"
    )
    assert int(_holding(api, "035420")["trde_able_qty"]) == STARTING_HOLDINGS["035420"][0] - 5
    new = api.order.modify_order(
        dmst_stex_tp="KRX", orig_ord_no=order["ord_no"], stk_cd="035420",
        mdfy_qty="5", mdfy_uv=str(price),
    )  # fmt: skip
    assert new["base_orig_ord_no"] == order["ord_no"]
    assert int(_holding(api, "035420")["rmnd_qty"]) == STARTING_HOLDINGS["035420"][0] - 5
    assert api.account.unfilled_orders(all_stk_tp="0", trde_tp="0", stex_tp="0")["oso"] == []


@pytest.mark.parametrize(
    ("call", "message"),
    [
        (lambda api: api.order.buy_order(dmst_stex_tp="KRX", stk_cd="005930", ord_qty="100000",
                                         trde_tp="3"), "주문가능금액"),
        (lambda api: api.order.sell_order(dmst_stex_tp="KRX", stk_cd="005380", ord_qty="1",
                                          trde_tp="3"), "매도가능수량"),
        (lambda api: api.order.buy_order(dmst_stex_tp="KRX", stk_cd="005930", ord_qty="1",
                                         ord_uv="71550", trde_tp="0"), "호가단위"),
        (lambda api: api.order.buy_order(dmst_stex_tp="KRX", stk_cd="005930", ord_qty="1",
                                         ord_uv="10", trde_tp="0"), "하한가"),
        (lambda api: api.order.cancel_order(dmst_stex_tp="KRX", orig_ord_no="9999",
                                            stk_cd="005930", cncl_qty="0"), "원주문번호"),
        (lambda api: api.credit_order.margin_buy_order(dmst_stex_tp="KRX", stk_cd="005930",
                                                       ord_qty="1", trde_tp="3", crd_deal_tp="33"),
         "지원하지 않습니다"),
    ],
)  # fmt: skip
def test_refusals_change_nothing(demo, call, message):
    api, backend = demo
    before = (backend.account.cash, dict(backend.account.holdings), len(backend.book.orders))
    with pytest.raises(KiwoomAPIError, match=message):
        call(api)
    after = (backend.account.cash, dict(backend.account.holdings), len(backend.book.orders))
    assert after == before


def test_each_backend_has_its_own_account():
    a, b = DemoBackend(), DemoBackend()
    a.account.cash -= 1
    assert b.account.cash == STARTING_CASH
