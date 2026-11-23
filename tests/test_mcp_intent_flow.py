"""investor_flow: ka10059 net buying per investor group, oldest day first."""

from __future__ import annotations

import json

import pytest

from kiwoom_client import spec
from kiwoom_client.mcp.intents.flow import _ROW_FIELDS, KEY, summarize_flow
from kiwoom_client.mcp.server import build_server

from .intent_support import STKINFO, call, mock_api


@pytest.fixture
async def api(httpx_mock):
    async with mock_api(httpx_mock) as client:
        yield client


def _day(dt, foreign, inst, ind):
    return {
        "dt": dt, "cur_prc": "-69000", "pred_pre": "-500", "frgnr_invsr": foreign,
        "orgn": inst, "ind_invsr": ind, "penfnd_etc": "+10",
    }  # fmt: skip


def test_fields_exist_in_the_catalog():
    tr = spec.get("ka10059")
    ids = {f.id for f in tr.response}
    assert KEY in ids
    assert {source for source, _ in _ROW_FIELDS.values()} <= ids
    assert set(tr.required_fields) <= {"dt", "stk_cd", "amt_qty_tp", "trde_tp", "unit_tp"}


def test_summary_counts_days():
    rows = [{"date": "a", "foreign": 10}, {"date": "b", "foreign": -3}, {"date": "c", "foreign": 5}]
    s = summarize_flow(rows)
    assert s["foreign"] == {"net_total": 12, "buy_days": 2, "sell_days": 1}
    assert (s["from"], s["to"], s["days"]) == ("a", "c", 3)


async def test_pages_and_orders_rows(httpx_mock, api):
    httpx_mock.add_response(
        url=STKINFO,
        match_headers={"api-id": "ka10059", "cont-yn": "N"},
        json={"return_code": 0, KEY: [_day("20261124", "+1,200", "-300", "-900")]},
        headers={"cont-yn": "Y", "next-key": "n2"},
    )
    httpx_mock.add_response(
        url=STKINFO,
        match_headers={"api-id": "ka10059", "cont-yn": "Y"},
        json={"return_code": 0, KEY: [_day("20261121", "-200", "+100", "+100")]},
    )
    app, _specs = build_server(api, allow_live_orders=False)
    args = {"stock": "005930", "days": 5, "end_date": "2026-11-24"}
    is_error, out = await call(app, "investor_flow", args)
    assert is_error is False, out
    assert [r["date"] for r in out["rows"]] == ["2026-11-21", "2026-11-24"]
    latest = out["rows"][-1]
    assert (latest["foreign"], latest["institution"], latest["individual"]) == (1200, -300, -900)
    assert latest["close"] == 69000
    assert out["summary"]["foreign"]["net_total"] == 1000
    assert out["unit"] == "million_krw"
    body = json.loads(httpx_mock.get_requests(url=STKINFO)[0].content)
    assert body == {
        "dt": "20261124", "stk_cd": "005930", "amt_qty_tp": "1", "trde_tp": "0", "unit_tp": "1",
    }  # fmt: skip


async def test_quantity_unit(httpx_mock, api):
    httpx_mock.add_response(url=STKINFO, json={"return_code": 0})
    app, _specs = build_server(api, allow_live_orders=False)
    args = {"stock": "005930", "unit": "quantity"}
    is_error, out = await call(app, "investor_flow", args)
    assert is_error is False, out
    assert out["unit"] == "shares" and out["rows"] == []
    body = json.loads(httpx_mock.get_requests(url=STKINFO)[0].content)
    assert (body["amt_qty_tp"], body["unit_tp"]) == ("2", "1")


async def test_bad_unit(api):
    app, _specs = build_server(api, allow_live_orders=False)
    is_error, _text = await call(app, "investor_flow", {"stock": "005930", "unit": "won"})
    assert is_error is True
