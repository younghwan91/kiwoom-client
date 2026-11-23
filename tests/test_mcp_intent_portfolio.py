"""get_portfolio: holdings with weights, cash, totals; account number masked."""

from __future__ import annotations

import json

import pytest

from kiwoom_client import spec
from kiwoom_client.mcp.intents.portfolio import (
    CASH_FIELDS,
    HOLDING_FIELDS,
    HOLDINGS_KEY,
    TOTAL_FIELDS,
    build_portfolio,
)
from kiwoom_client.mcp.server import build_server

from .intent_support import ACNT, call, mock_api


@pytest.fixture
async def api(httpx_mock):
    async with mock_api(httpx_mock) as client:
        yield client


def _holding(code, name, qty, avg, cur, pnl, rate):
    return {
        "stk_cd": f"A{code}", "stk_nm": name, "rmnd_qty": f"{qty:015d}",
        "trde_able_qty": f"{qty:015d}", "pur_pric": f"{avg:015d}", "cur_prc": f"{cur:012d}",
        "pur_amt": f"{qty * avg:015d}", "evlt_amt": f"{qty * cur:015d}",
        "evltv_prft": f"{pnl:+015d}", "prft_rt": rate,
    }  # fmt: skip


def test_fields_exist_in_the_catalog():
    kt00018 = {f.id for f in spec.get("kt00018").response}
    assert HOLDINGS_KEY in kt00018
    assert {s for s, _ in {**HOLDING_FIELDS, **TOTAL_FIELDS}.values()} <= kt00018
    kt00001 = {f.id for f in spec.get("kt00001").response}
    assert {s for s, _ in CASH_FIELDS.values()} <= kt00001
    assert "acctNo" in {f.id for f in spec.get("ka00001").response}


def test_build_portfolio_weights():
    holdings = [
        _holding("005930", "삼성전자", 10, 60000, 70000, 100000, "16.67"),
        _holding("000660", "SK하이닉스", 2, 200000, 150000, -100000, "-25.00"),
        _holding("035720", "카카오", 0, 0, 0, 0, "0"),  # 다 판 종목은 뺀다
    ]
    out = build_portfolio({"tot_prft_rt": "0.00"}, holdings, {"d2_entra": "000000000700000"})
    codes = [h["code"] for h in out["holdings"]]
    assert codes == ["005930", "000660"]  # 평가금액 큰 순
    samsung = out["holdings"][0]
    assert samsung["value"] == 700000 and samsung["pnl"] == 100000
    # 총자산 = 주식 700,000 + 300,000 + 현금 700,000 = 1,700,000
    assert out["totals"]["total_assets"] == 1700000
    assert samsung["weight_pct"] == round(700000 / 1700000 * 100, 2)
    assert samsung["stock_weight_pct"] == 70.0
    assert out["totals"]["cash_weight_pct"] == round(700000 / 1700000 * 100, 2)
    assert out["holdings"][1]["return_pct"] == -25.0
    assert out["account"] is None


async def test_get_portfolio_masks_account_and_pages(httpx_mock, api):
    httpx_mock.add_response(
        url=ACNT,
        match_headers={"api-id": "kt00018", "cont-yn": "N"},
        json={
            "return_code": 0, "tot_pur_amt": "000000001000000", "tot_evlt_amt": "000000001000000",
            "tot_evlt_pl": "000000000000000", "tot_prft_rt": "0.00",
            HOLDINGS_KEY: [_holding("005930", "삼성전자", 10, 70000, 70000, 0, "0.00")],
        },
        headers={"cont-yn": "Y", "next-key": "p2"},
    )  # fmt: skip
    httpx_mock.add_response(
        url=ACNT,
        match_headers={"api-id": "kt00018", "cont-yn": "Y"},
        json={
            "return_code": 0,
            HOLDINGS_KEY: [_holding("000660", "SK하이닉스", 2, 150000, 150000, 0, "0")],
        },
    )
    httpx_mock.add_response(
        url=ACNT,
        match_headers={"api-id": "kt00001"},
        json={"return_code": 0, "d2_entra": "000000000500000", "ord_alow_amt": "000000000500000"},
    )
    httpx_mock.add_response(
        url=ACNT,
        match_headers={"api-id": "ka00001"},
        json={"return_code": 0, "acctNo": "1234567890"},
    )
    app, _specs = build_server(api, allow_live_orders=False)
    is_error, out = await call(app, "get_portfolio", {})
    assert is_error is False, out
    assert out["account"] == "******7890"
    assert "1234567890" not in json.dumps(out)
    assert out["holdings_count"] == 2
    assert out["totals"]["total_assets"] == 700000 + 300000 + 500000
    assert out["totals"]["orderable_cash"] == 500000
    kt00018 = json.loads(
        httpx_mock.get_requests(url=ACNT, match_headers={"api-id": "kt00018"})[0].content
    )
    assert kt00018 == {"qry_tp": "1", "dmst_stex_tp": "KRX"}


async def test_bad_exchange(api):
    app, _specs = build_server(api, allow_live_orders=False)
    is_error, _text = await call(app, "get_portfolio", {"dmst_stex_tp": "NYSE"})
    assert is_error is True
