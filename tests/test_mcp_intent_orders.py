"""get_orders / get_buying_power: lookups only, normalised rows, cancel preview args."""

from __future__ import annotations

import json

import pytest

from kiwoom_client import spec
from kiwoom_client.mcp.intents import orders as orders_module
from kiwoom_client.mcp.server import build_server

from .intent_support import ACNT, call, mock_api


@pytest.fixture
async def api(httpx_mock):
    async with mock_api(httpx_mock) as client:
        yield client


@pytest.mark.parametrize(
    ("api_id", "key", "fields"),
    [
        ("ka10075", "oso", orders_module._OPEN_FIELDS),
        ("ka10076", "cntr", orders_module._FILLED_FIELDS),
        ("kt00007", "acnt_ord_cntr_prps_dtl", orders_module._HISTORY_FIELDS),
    ],
)
def test_fields_exist_in_the_catalog(api_id, key, fields):
    ids = {f.id for f in spec.get(api_id).response}
    assert key in ids
    assert {source for source, _ in fields.values()} <= ids


def test_buying_power_fields_exist_in_the_catalog():
    kt00011 = {f.id for f in spec.get("kt00011").response}
    for rate in orders_module._MARGIN_RATES:
        assert {f"profa_{rate}ord_alow_amt", f"profa_{rate}ord_alowq"} <= kt00011
    assert {"aplc_rt", "stk_profa_rt", "profa_rt", "min_ord_alow_amt", "min_ord_alowq"} <= kt00011
    kt00001 = {f.id for f in spec.get("kt00001").response}
    assert {s for s, _ in orders_module._ACCOUNT_CASH_FIELDS.values()} <= kt00001
    assert {f"{r}stk_ord_alow_amt" for r in ("20", "30", "40", "100")} <= kt00001


OPEN_ORDER = {
    "acnt_no": "1234567890", "ord_no": "0012345", "stk_cd": "005930", "stk_nm": "삼성전자",
    "io_tp_nm": "+매수", "trde_tp": "보통", "ord_stt": "접수", "ord_qty": "10",
    "ord_pric": "70000", "oso_qty": "7", "cntr_qty": "3", "cntr_pric": "70000",
    "cur_prc": "-69900", "tm": "093015", "orig_ord_no": "0000000", "stex_tp_txt": "KRX",
    "sor_yn": "N",
}  # fmt: skip


async def test_open_orders_today(httpx_mock, api):
    httpx_mock.add_response(
        url=ACNT, match_headers={"api-id": "ka10075"}, json={"return_code": 0, "oso": [OPEN_ORDER]}
    )
    app, _specs = build_server(api, allow_live_orders=False)
    is_error, out = await call(app, "get_orders", {})
    assert is_error is False, out
    (row,) = out["orders"]
    assert row["order_no"] == "0012345" and row["side"] == "buy"
    assert (row["qty"], row["open_qty"], row["filled_qty"]) == (10, 7, 3)
    assert row["current_price"] == 69900 and row["time"] == "09:30:15"
    assert row["original_order_no"] is None
    assert "acnt_no" not in json.dumps(row)  # 계좌번호는 내보내지 않는다
    assert row["cancel_preview_args"] == {
        "action": "cancel", "stock": "005930", "order_no": "0012345", "qty": "all",
        "dmst_stex_tp": "KRX",
    }  # fmt: skip
    body = json.loads(httpx_mock.get_requests(url=ACNT)[0].content)
    assert body == {"all_stk_tp": "0", "trde_tp": "0", "stex_tp": "0"}


async def test_cancel_args_work_in_order_preview(httpx_mock, api):
    httpx_mock.add_response(
        url=ACNT, match_headers={"api-id": "ka10075"}, json={"return_code": 0, "oso": [OPEN_ORDER]}
    )
    app, _specs = build_server(api, allow_live_orders=False)
    _err, out = await call(app, "get_orders", {"status": "open"})
    is_error, preview = await call(app, "order_preview", out["orders"][0]["cancel_preview_args"])
    assert is_error is False, preview
    assert preview["sent"] is False
    assert preview["params"]["orig_ord_no"] == "0012345"
    assert preview["params"]["cncl_qty"] == "0"


async def test_filled_today_for_one_stock(httpx_mock, api):
    httpx_mock.add_response(
        url=ACNT,
        match_headers={"api-id": "ka10076"},
        json={"return_code": 0, "cntr": [{
            "ord_no": "0012346", "stk_cd": "005930", "stk_nm": "삼성전자", "io_tp_nm": "-매도",
            "ord_qty": "5", "cntr_qty": "5", "cntr_pric": "71000", "tdy_trde_cmsn": "120",
            "tdy_trde_tax": "640", "ord_tm": "101500", "oso_qty": "0",
        }]},
    )  # fmt: skip
    app, _specs = build_server(api, allow_live_orders=False)
    is_error, out = await call(app, "get_orders", {"status": "filled", "stock": "005930"})
    assert is_error is False, out
    (row,) = out["orders"]
    assert row["side"] == "sell" and row["filled_price"] == 71000 and row["tax"] == 640
    assert "cancel_preview_args" not in row
    body = json.loads(httpx_mock.get_requests(url=ACNT)[0].content)
    assert body == {"qry_tp": "1", "sell_tp": "0", "stex_tp": "0", "stk_cd": "005930"}


async def test_another_day_uses_kt00007(httpx_mock, api):
    httpx_mock.add_response(
        url=ACNT,
        match_headers={"api-id": "kt00007"},
        json={"return_code": 0, "acnt_ord_cntr_prps_dtl": [{
            "ord_no": "0000077", "stk_cd": "A005930", "stk_nm": "삼성전자", "io_tp_nm": "현금매수",
            "ord_qty": "0000000010", "ord_uv": "0000070000", "cntr_qty": "0000000010",
            "cntr_uv": "0000069900", "ord_remnq": "0000000000", "ord_tm": "09:01:02",
        }]},
    )  # fmt: skip
    app, _specs = build_server(api, allow_live_orders=False)
    args = {"status": "filled", "date": "2025-01-02"}
    is_error, out = await call(app, "get_orders", args)
    assert is_error is False, out
    (row,) = out["orders"]
    assert row["code"] == "005930" and row["filled_price"] == 69900 and row["qty"] == 10
    assert out["date"] == "2025-01-02"
    body = json.loads(httpx_mock.get_requests(url=ACNT)[0].content)
    assert body["ord_dt"] == "20250102" and body["qry_tp"] == "4"


async def test_bad_status(api):
    app, _specs = build_server(api, allow_live_orders=False)
    is_error, _text = await call(app, "get_orders", {"status": "cancelled"})
    assert is_error is True


async def test_buying_power_for_a_stock(httpx_mock, api):
    httpx_mock.add_response(
        url=ACNT,
        match_headers={"api-id": "kt00011"},
        json={
            "return_code": 0, "stk_profa_rt": "20%", "profa_rt": "40%", "aplc_rt": "40%",
            "profa_40ord_alow_amt": "000002800000", "profa_40ord_alowq": "000000000040",
            "profa_100ord_alow_amt": "000001120000", "profa_100ord_alowq": "000000000016",
            "min_ord_alow_amt": "000001120000", "min_ord_alowq": "000000000016",
            "entr": "000001120000", "ord_alowa": "000001120000",
        },
    )  # fmt: skip
    app, _specs = build_server(api, allow_live_orders=False)
    args = {"stock": "005930", "price": 70000}
    is_error, out = await call(app, "get_buying_power", args)
    assert is_error is False, out
    assert out["applied_margin_rate_pct"] == 40.0
    assert out["orderable"] == {"amount": 2800000, "qty": 40}
    assert out["cash_only"] == {"amount": 1120000, "qty": 16}
    assert out["by_margin_rate"]["100"]["qty"] == 16
    body = json.loads(httpx_mock.get_requests(url=ACNT)[0].content)
    assert body == {"stk_cd": "005930", "uv": "70000"}


async def test_buying_power_for_the_account(httpx_mock, api):
    httpx_mock.add_response(
        url=ACNT,
        match_headers={"api-id": "kt00001"},
        json={
            "return_code": 0, "entr": "000000001000000", "d2_entra": "000000000900000",
            "ord_alow_amt": "000000000850000", "pymn_alow_amt": "000000000800000",
            "100stk_ord_alow_amt": "000000000850000",
        },
    )  # fmt: skip
    app, _specs = build_server(api, allow_live_orders=False)
    is_error, out = await call(app, "get_buying_power", {})
    assert is_error is False, out
    assert (out["deposit"], out["d2_estimated_deposit"]) == (1000000, 900000)
    assert out["orderable_amount"] == 850000
    assert out["orderable_amount_by_stock_margin_rate"] == {"100": 850000}
    body = json.loads(httpx_mock.get_requests(url=ACNT)[0].content)
    assert body == {"qry_tp": "3"}


async def test_buying_power_bad_price(api):
    app, _specs = build_server(api, allow_live_orders=False)
    is_error, _text = await call(app, "get_buying_power", {"stock": "005930", "price": -1})
    assert is_error is True
