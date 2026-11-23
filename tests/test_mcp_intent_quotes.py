"""get_quotes: many stocks in one ka10095 call, per-stock errors."""

from __future__ import annotations

import json

import pytest

from kiwoom_client.mcp.intents.quotes import MAX_STOCKS, parse_stock_list
from kiwoom_client.mcp.server import build_server

from .intent_support import STKINFO, call, mock_api, mock_listing


@pytest.fixture
async def api(httpx_mock):
    async with mock_api(httpx_mock) as client:
        yield client


def _row(code, name, cur, flu):
    return {
        "stk_cd": code, "stk_nm": name, "cur_prc": cur, "pred_pre": "-1,000",
        "flu_rt": flu, "trde_qty": "1,234,567", "trde_prica": "86000", "mac": "4170000",
        "open_pric": "+70500", "high_pric": "+71000", "low_pric": "-69000",
    }  # fmt: skip


def test_parse_stock_list():
    assert parse_stock_list("삼성전자, 000660 ,") == ["삼성전자", "000660"]
    assert parse_stock_list(["a", " ", "b"]) == ["a", "b"]
    assert parse_stock_list(None) == []


async def test_one_request_for_all_and_partial_failure(httpx_mock, api):
    mock_listing(httpx_mock)
    httpx_mock.add_response(
        url=STKINFO,
        match_headers={"api-id": "ka10095"},
        json={
            "return_code": 0,
            "atn_stk_infr": [
                _row("005930", "삼성전자", "-69000", "-1.43"),
                _row("000660", "SK하이닉스", "+180000", "+2.10"),
            ],
        },
    )
    app, _specs = build_server(api, allow_live_orders=False)
    stocks = ["삼성전자", "000660", "없는회사", "123450", "005930"]
    is_error, out = await call(app, "get_quotes", {"stocks": stocks})
    assert is_error is False, out
    first, second, missing, absent, again = out["quotes"]
    assert first["code"] == "005930" and first["price"] == 69000
    assert first["change"] == -1000 and first["change_pct"] == -1.43
    assert first["volume"] == 1234567
    assert first["market_cap_100m_krw"] == 4170000
    assert second["name"] == "SK하이닉스"
    assert "error" in missing and missing["query"] == "없는회사"
    assert absent == {
        "query": "123450",
        "code": "123450",
        "error": "키움 응답에 이 종목이 없습니다",
    }
    assert again["code"] == "005930"
    assert out["failed"] == 2
    (request,) = httpx_mock.get_requests(url=STKINFO, match_headers={"api-id": "ka10095"})
    assert json.loads(request.content) == {"stk_cd": "005930|000660|123450"}


async def test_too_many_stocks_is_an_error(api):
    app, _specs = build_server(api, allow_live_orders=False)
    codes = [f"{i:06d}" for i in range(MAX_STOCKS + 1)]
    is_error, text = await call(app, "get_quotes", {"stocks": codes})
    assert is_error is True and "20" in text


async def test_empty_is_an_error(api):
    app, _specs = build_server(api, allow_live_orders=False)
    is_error, _text = await call(app, "get_quotes", {"stocks": []})
    assert is_error is True
