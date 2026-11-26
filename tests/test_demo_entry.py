"""``KiwoomAPI.demo()`` / ``AsyncKiwoomAPI.demo()`` — the whole client on the demo backend."""

from __future__ import annotations

import asyncio

import pytest

from kiwoom_client import AsyncKiwoomAPI, KiwoomAPI
from kiwoom_client.demo import DEMO_KEY, DemoBackend, DemoWebSocket
from tests.demo_support import no_network  # noqa: F401

pytestmark = pytest.mark.usefixtures("no_network")


def test_sync_demo_client_does_everything_offline():
    with KiwoomAPI.demo() as api:
        assert api.is_demo and isinstance(api.demo_backend, DemoBackend)
        assert "server='demo'" in repr(api)
        info = api.stock_info.basic_stock_info(stk_cd=api.stock_code("삼성전자"))
        assert info[DEMO_KEY] and info["stk_nm"] == "삼성전자"
        order = api.order.buy_order(dmst_stex_tp="KRX", stk_cd="005930", ord_qty="1", trde_tp="3")
        assert order["ord_no"]
        assert api.demo_backend.book.orders[0].filled_qty == 1
        assert isinstance(api.create_websocket(), DemoWebSocket)
        api.logout()  # revokes nothing real: the fake server answers


def test_real_clients_are_not_demo():
    api = KiwoomAPI("key", "secret")
    try:
        assert not api.is_demo and api.demo_backend is None
    finally:
        api.close()


def test_seed_is_passed_through():
    with KiwoomAPI.demo(seed=1) as a, KiwoomAPI.demo(seed=2) as b:
        assert a.demo_backend.market.seed == 1
        chart = {"stk_cd": "005930", "base_dt": "20261127", "upd_stkpc_tp": "1"}
        rows_a = a.chart.stock_daily_chart(**chart)["stk_dt_pole_chart_qry"]
        rows_b = b.chart.stock_daily_chart(**chart)["stk_dt_pole_chart_qry"]
        assert [r["cur_prc"] for r in rows_a[:20]] != [r["cur_prc"] for r in rows_b[:20]]


async def test_async_demo_client_and_websocket():
    async with AsyncKiwoomAPI.demo() as api:
        assert api.is_demo
        quotes, balance = await asyncio.gather(
            api.stock_info.watchlist_stock_info(stk_cd="005930|035720"),
            api.account.evaluation_balance_detail(qry_tp="1", dmst_stex_tp="KRX"),
        )
        assert len(quotes["atn_stk_infr"]) == 2 and balance["acnt_evlt_remn_indv_tot"]
        ws = await api.create_websocket()
        got: list[dict] = []
        ws.on("0B", got.append)
        async with ws:
            task = asyncio.create_task(ws.listen())
            await ws.subscribe("0B", "005930")
            await asyncio.sleep(0.35)
        await asyncio.wait_for(task, 1)
        assert got and got[0]["item"] == "005930"
