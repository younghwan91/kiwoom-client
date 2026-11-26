"""The demo backend (kiwoom_client.demo): a fake Kiwoom REST server in the process.

Every test runs with the network blocked (``no_network``): demo mode must never
reach the real server, the paper-trading server or DNS.
"""

from __future__ import annotations

import json
from datetime import date

import httpx
import pytest

from kiwoom_client import AsyncKiwoomAPI, KiwoomAPI, spec
from kiwoom_client.base import KiwoomStockNotFoundError
from kiwoom_client.demo import DEMO_BASE_URL, DEMO_KEY, DEMO_NOTICE, UNIVERSE, DemoBackend
from kiwoom_client.demo.backend import ORDER_API_IDS
from kiwoom_client.tick_size import is_on_tick
from tests.demo_support import NetworkBlocked, no_network  # noqa: F401

pytestmark = pytest.mark.usefixtures("no_network")

FRIDAY = date(2026, 11, 27)


def _api(backend: DemoBackend | None = None) -> KiwoomAPI:
    api = KiwoomAPI("demo-key", "demo-secret", base_url=DEMO_BASE_URL, rate_limit=None)
    return (backend or DemoBackend(today=FRIDAY)).attach(api)


def _post(backend: DemoBackend, api_id: str, body: dict, *, url: str | None = None) -> dict:
    tr = spec.get(api_id)
    request = httpx.Request(
        "POST",
        f"{DEMO_BASE_URL}{url or tr.url}",
        headers={"api-id": api_id},
        content=json.dumps(body).encode(),
    )
    return backend.handle(request).json()


def _body(tr: spec.TRSpec) -> dict:
    """A request body naming a demo stock wherever the TR takes a stock code."""
    body = {}
    for f in tr.request_fields:
        if f.id == "stk_cd" or "종목코드" in f.name:
            body[f.id] = "005930"
        elif "일자" in f.name or f.id.endswith("_dt") or f.id == "dt":
            body[f.id] = "20261127"
        else:
            body[f.id] = "0"
    return body


def test_guard_really_blocks_the_network():
    with pytest.raises((NetworkBlocked, httpx.ConnectError)):
        httpx.get("https://api.kiwoom.com/")


REST_IDS = [a for a in spec.api_ids() if spec.get(a).transport == "rest"]


@pytest.mark.parametrize("api_id", REST_IDS)
def test_every_rest_tr_answers_with_catalog_fields(api_id):
    backend = DemoBackend(today=FRIDAY)
    tr = spec.get(api_id)
    data = _post(backend, api_id, _body(tr))
    assert data[DEMO_KEY] == DEMO_NOTICE
    if api_id in ORDER_API_IDS:
        assert data["return_code"] != 0  # ord_qty "0" is refused; credit/gold always are
        return
    assert data["return_code"] == 0, data
    for f in tr.response:
        if f.parent is None:
            assert f.id in data, f"{api_id}: {f.id} missing"
    lists = [f.id for f in tr.response if f.parent is None and f.type == "list"]
    children = {f.parent: set() for f in tr.response if f.parent}
    for f in tr.response:
        if f.parent:
            children[f.parent].add(f.id)
    for key in lists:
        for row in data[key]:
            assert set(row) == children.get(key, set(row)), f"{api_id}.{key}"


def test_unknown_api_id_and_unknown_stock_are_errors():
    backend = DemoBackend(today=FRIDAY)
    request = httpx.Request(
        "POST", f"{DEMO_BASE_URL}/api/dostk/stkinfo", headers={"api-id": "ka99999"}
    )
    assert backend.handle(request).json()["return_code"] != 0
    with _api(backend) as api, pytest.raises(KiwoomStockNotFoundError):
        api.stock_info.basic_stock_info(stk_cd="999999")


def test_token_flow_and_quote_through_the_real_client():
    with _api() as api:
        api.login()
        info = api.stock_info.basic_stock_info(stk_cd="005930")
    assert info["stk_nm"] == "삼성전자" and info[DEMO_KEY] == DEMO_NOTICE
    price = abs(int(info["cur_prc"]))
    upper, lower = abs(int(info["upl_pric"])), abs(int(info["lst_pric"]))
    assert lower < price < upper and is_on_tick(price)


def test_same_seed_same_data_other_seed_other_data():
    def close(seed):
        backend = DemoBackend(seed=seed, today=FRIDAY)
        rows = _post(backend, "ka10081", {"stk_cd": "000660", "base_dt": "20261127"})
        return [r["cur_prc"] for r in rows["stk_dt_pole_chart_qry"][:30]]

    assert close(1) == close(1)
    assert close(1) != close(2)


def test_daily_chart_is_business_days_newest_first_and_pages():
    with _api() as api:
        rows = api._base_client.request_all(
            "/api/dostk/chart", "ka10081",
            {"stk_cd": "005930", "base_dt": "20261127", "upd_stkpc_tp": "1"},
            data_key="stk_dt_pole_chart_qry",
        )  # fmt: skip
    assert len(rows) == 600  # more than one page: continuation is followed
    dates = [r["dt"] for r in rows]
    assert dates[0] == "20261127" and dates == sorted(dates, reverse=True)
    for r in rows:
        assert date(int(r["dt"][:4]), int(r["dt"][4:6]), int(r["dt"][6:])).weekday() < 5
        o, h, lo, c = (int(r[k]) for k in ("open_pric", "high_pric", "low_pric", "cur_prc"))
        assert lo <= min(o, c) and max(o, c) <= h
        assert all(is_on_tick(p) for p in (o, h, lo, c))


def test_weekend_maps_to_the_previous_friday():
    backend = DemoBackend(today=date(2026, 11, 29))  # Sunday
    rows = _post(backend, "ka10081", {"stk_cd": "005930", "base_dt": "20261129"})
    assert rows["stk_dt_pole_chart_qry"][0]["dt"] == "20261127"


def test_minute_chart_covers_the_session_and_aggregates():
    backend = DemoBackend(today=FRIDAY)
    one = _post(backend, "ka10080", {"stk_cd": "005930", "tic_scope": "1"})[
        "stk_min_pole_chart_qry"
    ]
    five = _post(backend, "ka10080", {"stk_cd": "005930", "tic_scope": "5"})[
        "stk_min_pole_chart_qry"
    ]
    assert one[-1]["cntr_tm"] == "20261127090000" and one[0]["cntr_tm"] == "20261127152900"
    assert len(five) == 78
    daily = _post(backend, "ka10081", {"stk_cd": "005930", "base_dt": "20261127"})
    today = daily["stk_dt_pole_chart_qry"][0]
    assert one[0]["cur_prc"] == today["cur_prc"]  # the session closes where the daily bar does


def test_listing_and_search_use_real_names():
    with _api() as api:
        assert api.stock_code("삼성전자") == "005930"
        assert api.stock_code("에코프로") == "086520"
        names = [s["name"] for s in api.find_stock("삼성")]
    assert "삼성전자" in names and "삼성SDI" in names
    assert len(UNIVERSE) >= 15


def test_rankings_are_sorted_and_filtered_by_market():
    backend = DemoBackend(today=FRIDAY)
    gainers = _post(backend, "ka10027", {"mrkt_tp": "000", "sort_tp": "1"})["pred_pre_flu_rt_upper"]
    rates = [float(r["flu_rt"]) for r in gainers]
    assert rates and rates == sorted(rates, reverse=True) and all(x > 0 for x in rates)
    kosdaq = _post(backend, "ka10030", {"mrkt_tp": "101"})["tdy_trde_qty_upper"]
    assert {r["stk_cd"] for r in kosdaq} <= {s.code for s in UNIVERSE if s.market == "10"}


def test_investor_flow_nets_to_zero():
    backend = DemoBackend(today=FRIDAY)
    rows = _post(backend, "ka10059", {"stk_cd": "005930", "dt": "20261127", "amt_qty_tp": "1"})
    for row in rows["stk_invsr_orgn"]:
        total = sum(int(row[k]) for k in ("ind_invsr", "frgnr_invsr", "orgn", "etc_corp"))
        assert abs(total) <= 3  # rounding only


def test_account_balance_adds_up():
    with _api() as api:
        bal = api.account.evaluation_balance_detail(qry_tp="1", dmst_stex_tp="KRX")
        cash = api.account.deposit_detail(qry_tp="3")
        acct = api.account.account_number_inquiry()
    holdings = bal["acnt_evlt_remn_indv_tot"]
    assert holdings and int(bal["tot_evlt_amt"]) == sum(int(h["evlt_amt"]) for h in holdings)
    assert int(bal["prsm_dpst_aset_amt"]) == int(bal["tot_evlt_amt"]) + int(cash["entr"])
    assert acct["acctNo"].startswith("DEMO")


async def test_async_client_shares_the_same_backend():
    backend = DemoBackend(today=FRIDAY)
    api = backend.attach(
        AsyncKiwoomAPI("demo-key", "demo-secret", base_url=DEMO_BASE_URL, rate_limit=None)
    )
    async with api:
        quotes = await api.stock_info.watchlist_stock_info(stk_cd="005930|000660")
        code = await api.stock_code("SK하이닉스")
    assert [q["stk_cd"] for q in quotes["atn_stk_infr"]] == ["005930", "000660"]
    assert code == "000660"
    assert "ka10095" in backend.requests
