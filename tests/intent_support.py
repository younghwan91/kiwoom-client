"""Shared fakes for the intent tool tests (not collected: no ``test_`` prefix)."""

from __future__ import annotations

import json
from contextlib import asynccontextmanager

from mcp import types

from kiwoom_client import AsyncKiwoomAPI

BASE = "https://mockapi.kiwoom.com"
STKINFO = f"{BASE}/api/dostk/stkinfo"
ACNT = f"{BASE}/api/dostk/acnt"

LISTING = [
    {"code": "005930", "name": "삼성전자", "marketName": "거래소"},
    {"code": "005935", "name": "삼성전자우", "marketName": "거래소"},
    {"code": "028260", "name": "삼성물산", "marketName": "거래소"},
    {"code": "035720", "name": "카카오", "marketName": "거래소"},
    {"code": "293490", "name": "카카오게임즈", "marketName": "코스닥"},
]


@asynccontextmanager
async def mock_api(httpx_mock):
    """A logged-in AsyncKiwoomAPI against the (mocked) paper-trading server."""
    httpx_mock.add_response(
        url=f"{BASE}/oauth2/token",
        json={"token": "test_token", "token_type": "Bearer", "expires_in": 86400},
    )
    api = AsyncKiwoomAPI("key", "secret", is_mock=True)
    await api.login()
    try:
        yield api
    finally:
        await api.close()


def mock_listing(httpx_mock, rows=LISTING):
    """ka10099: KOSPI returns ``rows``, KOSDAQ/ETF are empty."""
    httpx_mock.add_response(
        url=STKINFO,
        match_json={"mrkt_tp": "0"},
        json={"return_code": 0, "list": rows},
        is_reusable=True,
    )
    for market in ("10", "8"):
        httpx_mock.add_response(
            url=STKINFO,
            match_json={"mrkt_tp": market},
            json={"return_code": 0, "list": []},
            is_reusable=True,
        )


async def call(app, name, arguments):
    """``(is_error, payload)`` — payload is the decoded JSON, or the error text."""
    result = await app.get_request_handler("tools/call").handler(
        None, types.CallToolRequestParams(name=name, arguments=arguments)
    )
    text = result.content[0].text
    return result.is_error, (text if result.is_error else json.loads(text))
