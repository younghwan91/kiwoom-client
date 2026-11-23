"""Shared fixtures for the MCP order-safety tests (pytest-httpx mocks only)."""

from __future__ import annotations

import json
from typing import Any

from mcp import types

BASE = "https://mockapi.kiwoom.com"
ORDR = f"{BASE}/api/dostk/ordr"
CRDORDR = f"{BASE}/api/dostk/crdordr"
STKINFO = f"{BASE}/api/dostk/stkinfo"
ACNT = f"{BASE}/api/dostk/acnt"
ORDER_PATHS = ("/api/dostk/ordr", "/api/dostk/crdordr")

KOSPI = [
    {"code": "005930", "name": "삼성전자", "marketName": "거래소", "upName": "전기전자"},
    {"code": "005935", "name": "삼성전자우", "marketName": "거래소", "upName": "전기전자"},
]

BUY = {"side": "buy", "stk_cd": "005930", "ord_qty": 10, "ord_uv": 70000}
BUY_PARAMS = {
    "dmst_stex_tp": "KRX",
    "stk_cd": "005930",
    "ord_qty": "10",
    "ord_uv": "70000",
    "trde_tp": "0",
}


def mock_token(httpx_mock) -> None:
    httpx_mock.add_response(
        url=f"{BASE}/oauth2/token",
        json={"token": "test_token", "token_type": "Bearer", "expires_in": 86400},
    )


def mock_orders(httpx_mock) -> None:
    for url in (ORDR, CRDORDR):
        httpx_mock.add_response(
            url=url,
            json={"return_code": 0, "return_msg": "OK", "ord_no": "0000123"},
            is_reusable=True,
            is_optional=True,
        )


def mock_stock_lists(httpx_mock) -> None:
    for market, rows in (("0", KOSPI), ("10", [])):
        httpx_mock.add_response(
            url=STKINFO,
            match_json={"mrkt_tp": market},
            json={"return_code": 0, "return_msg": "OK", "list": rows},
            is_reusable=True,
            is_optional=True,
        )


def mock_quote(httpx_mock, *, upper="+91000", lower="-49000", current="70000") -> None:
    """ka10001 for the preview's 상·하한가 check."""
    httpx_mock.add_response(
        url=STKINFO,
        match_headers={"api-id": "ka10001"},
        json={
            "return_code": 0,
            "stk_cd": "005930",
            "upl_pric": upper,
            "lst_pric": lower,
            "cur_prc": current,
        },
        is_reusable=True,
        is_optional=True,
    )


def mock_buyable(httpx_mock, *, rate="40", allowed="100", cash_only="50", cash="3500000") -> None:
    """kt00011 for the preview's 주문가능수량 check."""
    httpx_mock.add_response(
        url=ACNT,
        match_headers={"api-id": "kt00011"},
        json={
            "return_code": 0,
            "aplc_rt": rate,
            f"profa_{rate}ord_alowq": allowed,
            "min_ord_alowq": cash_only,
            "ord_alowa": cash,
        },
        is_reusable=True,
        is_optional=True,
    )


def mock_holdings(httpx_mock, rows=None) -> None:
    """kt00018 for the preview's 매도가능수량 check."""
    if rows is None:
        rows = [{"stk_cd": "A005930", "rmnd_qty": "000000000020", "trde_able_qty": "000000000020"}]
    httpx_mock.add_response(
        url=ACNT,
        match_headers={"api-id": "kt00018"},
        json={"return_code": 0, "acnt_evlt_remn_indv_tot": rows},
        is_reusable=True,
        is_optional=True,
    )


def mock_lookups(httpx_mock) -> None:
    """Every lookup order_preview may make, with generous limits."""
    mock_quote(httpx_mock)
    mock_buyable(httpx_mock)
    mock_holdings(httpx_mock)


def order_requests(httpx_mock) -> list[Any]:
    return [r for r in httpx_mock.get_requests() if r.url.path in ORDER_PATHS]


def sent_bodies(httpx_mock) -> list[dict[str, Any]]:
    return [json.loads(r.content) for r in order_requests(httpx_mock)]


async def call(app, name: str, arguments: dict[str, Any]) -> types.CallToolResult:
    return await app.get_request_handler("tools/call").handler(
        None, types.CallToolRequestParams(name=name, arguments=arguments)
    )


async def ok(app, name: str, arguments: dict[str, Any]) -> Any:
    result = await call(app, name, arguments)
    assert result.is_error is False, result.content[0].text
    return json.loads(result.content[0].text)


async def refused(app, name: str, arguments: dict[str, Any]) -> str:
    result = await call(app, name, arguments)
    assert result.is_error is True, result.content[0].text
    return result.content[0].text


async def listed(app) -> dict[str, types.Tool]:
    result = await app.get_request_handler("tools/list").handler(
        None, types.PaginatedRequestParams()
    )
    return {t.name: t for t in result.tools}
