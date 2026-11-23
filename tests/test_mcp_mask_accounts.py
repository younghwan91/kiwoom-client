"""Account numbers in MCP tool responses are masked unless opted out."""

from __future__ import annotations

import asyncio

import pytest

from kiwoom_client import AsyncKiwoomAPI
from kiwoom_client.mcp import server as server_module
from kiwoom_client.mcp.masking import ENV_VAR, mask_from_env
from kiwoom_client.mcp.server import build_server
from tests.mcp_order_helpers import ACNT, mock_token, ok

ACCOUNT = "8012345611"
REPLY = {
    "return_code": 0,
    "acnt_no": ACCOUNT,
    "list": [{"acctNo": ACCOUNT, "stk_cd": "005930"}],
    "tot_evlt_amt": "000001000000",
}


@pytest.fixture
async def api(httpx_mock):
    mock_token(httpx_mock)
    httpx_mock.add_response(url=ACNT, json=REPLY, is_reusable=True)
    api = AsyncKiwoomAPI("key", "secret", is_mock=True)
    await api.login()
    yield api
    await api.close()


TOOL = "account_deposit_detail"


async def test_masked_by_default(api):
    app, _ = build_server(api, allow_live_orders=False)
    result = await ok(app, TOOL, {"params": {"qry_tp": "2"}})
    assert result["acnt_no"] == "******5611"
    assert result["list"][0]["acctNo"] == "******5611"
    assert result["list"][0]["stk_cd"] == "005930"
    assert result["tot_evlt_amt"] == "000001000000"


async def test_masked_through_call_tool_too(api):
    app, _ = build_server(api, allow_live_orders=False, mode="discovery")
    result = await ok(app, "call_tool", {"name": TOOL, "arguments": {"params": {"qry_tp": "2"}}})
    assert ACCOUNT not in str(result)


async def test_opt_out(api):
    app, _ = build_server(api, allow_live_orders=False, mask_accounts=False)
    result = await ok(app, TOOL, {"params": {"qry_tp": "2"}})
    assert result["acnt_no"] == ACCOUNT


@pytest.mark.parametrize(("value", "expected"), [(None, True), ("false", False), ("true", True)])
def test_env(value, expected):
    assert mask_from_env({} if value is None else {ENV_VAR: value}) is expected


def test_bad_env():
    with pytest.raises(ValueError, match=ENV_VAR):
        mask_from_env({ENV_VAR: "sometimes"})


def test_run_server_reads_the_env(monkeypatch):
    calls: list[dict] = []

    def fake_build_server(api, **kwargs):
        calls.append(kwargs)
        return object(), []

    monkeypatch.setattr(server_module, "build_server", fake_build_server)
    monkeypatch.setattr(asyncio, "run", lambda coro: coro.close())
    monkeypatch.setenv(ENV_VAR, "false")
    server_module.run_server(app_key="k", app_secret="s", is_mock=True)
    monkeypatch.delenv(ENV_VAR)
    server_module.run_server(app_key="k", app_secret="s", is_mock=True)
    assert [c["mask_accounts"] for c in calls] == [False, True]
