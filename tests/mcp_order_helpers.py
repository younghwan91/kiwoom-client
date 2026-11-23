"""Shared fixtures for the MCP order-safety tests (pytest-httpx mocks only)."""

from __future__ import annotations

import json
from typing import Any

from mcp import types

BASE = "https://mockapi.kiwoom.com"
ORDR = f"{BASE}/api/dostk/ordr"
CRDORDR = f"{BASE}/api/dostk/crdordr"
STKINFO = f"{BASE}/api/dostk/stkinfo"
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
