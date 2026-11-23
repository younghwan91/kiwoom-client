"""market_movers: ranking TRs behind one readable tool."""

from __future__ import annotations

import json

import pytest

from kiwoom_client import spec
from kiwoom_client.mcp.intents.movers import KINDS, MARKETS
from kiwoom_client.mcp.server import build_server

from .intent_support import BASE, call, mock_api

RKINFO = f"{BASE}/api/dostk/rkinfo"


@pytest.fixture
async def api(httpx_mock):
    async with mock_api(httpx_mock) as client:
        yield client


def test_request_codes_cover_every_required_field():
    """Each kind fills every required request field of its TR (catalog check)."""
    for kind in KINDS.values():
        tr = spec.for_method("ranking", kind.method)
        sent = {"mrkt_tp", *kind.params}
        assert set(tr.required_fields) <= sent, (kind.method, set(tr.required_fields) - sent)
        response_ids = {f.id for f in tr.response}
        assert kind.key in response_ids
        assert {source for source, _ in kind.fields.values()} <= response_ids, kind.method


GAINER = {
    "stk_cd": "293490", "stk_nm": "카카오게임즈", "cur_prc": "+26000", "pred_pre": "+6000",
    "flu_rt": "+30.00", "now_trde_qty": "5,000,000", "cntr_str": "150.25",
}  # fmt: skip
OTHER = {"stk_cd": "000001", "stk_nm": "B", "cur_prc": "+1000", "flu_rt": "+25.00"}


async def test_gainers_on_kosdaq(httpx_mock, api):
    httpx_mock.add_response(
        url=RKINFO,
        match_headers={"api-id": "ka10027"},
        json={
            "return_code": 0,
            "pred_pre_flu_rt_upper": [GAINER, OTHER],
        },
    )
    app, _specs = build_server(api, allow_live_orders=False)
    args = {"kind": "gainers", "market": "kosdaq", "count": 1}
    is_error, out = await call(app, "market_movers", args)
    assert is_error is False, out
    assert out["count"] == 1
    row = out["rows"][0]
    assert row == {
        "rank": 1, "code": "293490", "name": "카카오게임즈", "price": 26000, "change": 6000,
        "change_pct": 30.0, "volume": 5000000, "strength_pct": 150.25,
    }  # fmt: skip
    body = json.loads(httpx_mock.get_requests(url=RKINFO)[0].content)
    assert body["mrkt_tp"] == MARKETS["kosdaq"] and body["sort_tp"] == "1"


async def test_losers_sort_by_fall(httpx_mock, api):
    httpx_mock.add_response(url=RKINFO, json={"return_code": 0, "pred_pre_flu_rt_upper": []})
    app, _specs = build_server(api, allow_live_orders=False)
    is_error, out = await call(app, "market_movers", {"kind": "losers"})
    assert is_error is False and out["rows"] == []
    body = json.loads(httpx_mock.get_requests(url=RKINFO)[0].content)
    assert body["sort_tp"] == "3" and body["mrkt_tp"] == "000"


@pytest.mark.parametrize("kind", ["volume", "value", "volume_spike"])
async def test_other_kinds_call_their_tr(httpx_mock, api, kind):
    spec_kind = KINDS[kind]
    api_id = spec.for_method("ranking", spec_kind.method).api_id
    httpx_mock.add_response(
        url=RKINFO,
        match_headers={"api-id": api_id},
        json={"return_code": 0, spec_kind.key: [{"stk_cd": "005930", "cur_prc": "-69000"}]},
    )
    app, _specs = build_server(api, allow_live_orders=False)
    is_error, out = await call(app, "market_movers", {"kind": kind})
    assert is_error is False, out
    assert out["rows"][0]["price"] == 69000


@pytest.mark.parametrize("args", [{"kind": "hot"}, {"market": "nyse"}])
async def test_bad_arguments(api, args):
    app, _specs = build_server(api, allow_live_orders=False)
    is_error, _text = await call(app, "market_movers", args)
    assert is_error is True
