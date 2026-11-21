"""Tests for the high-level helper tools (stock_search, stock_snapshot, account_summary)."""

from __future__ import annotations

import json

import pytest
from mcp import types

from kiwoom_client import AsyncKiwoomAPI
from kiwoom_client.mcp.helpers import helper_tools
from kiwoom_client.mcp.server import build_server
from kiwoom_client.mcp.tools import discover_rest_tools

BASE = "https://mockapi.kiwoom.com"
STKINFO = f"{BASE}/api/dostk/stkinfo"
ACNT = f"{BASE}/api/dostk/acnt"

KOSPI = [
    {"code": "005930", "name": "삼성전자", "marketName": "거래소", "upName": "전기전자"},
    {"code": "005935", "name": "삼성전자우", "marketName": "거래소", "upName": "전기전자"},
    {"code": "028260", "name": "삼성물산", "marketName": "거래소", "upName": "유통"},
]
KOSDAQ = [{"code": "035720", "name": "카카오게임즈", "marketName": "코스닥", "upName": "IT"}]


@pytest.fixture
async def api(httpx_mock):
    httpx_mock.add_response(
        url=f"{BASE}/oauth2/token",
        json={"token": "test_token", "token_type": "Bearer", "expires_in": 86400},
    )
    api = AsyncKiwoomAPI("key", "secret", is_mock=True)
    await api.login()
    yield api
    await api.close()


def _mock_lists(httpx_mock):
    for market, rows in (("0", KOSPI), ("10", KOSDAQ)):
        httpx_mock.add_response(
            url=STKINFO,
            match_json={"mrkt_tp": market},
            json={"return_code": 0, "return_msg": "OK", "list": rows},
            is_reusable=True,
        )


async def _call(app, name, arguments):
    result = await app.get_request_handler("tools/call").handler(
        None, types.CallToolRequestParams(name=name, arguments=arguments)
    )
    assert result.is_error is False, result.content[0].text
    return json.loads(result.content[0].text)


class TestRegistration:
    def test_names_do_not_collide_with_rest_tools(self):
        rest = {s.tool_name for s in discover_rest_tools()}
        assert not {t.name for t in helper_tools()} & rest

    def test_all_helpers_are_read_only(self):
        for tool in helper_tools():
            assert tool.annotations.read_only_hint is True, tool.name
            assert not tool.annotations.destructive_hint

    async def test_helpers_follow_their_toolsets(self):
        app, _specs = build_server(api=None, allow_live_orders=False, toolsets={"account"})
        listed = await app.get_request_handler("tools/list").handler(
            None, types.PaginatedRequestParams()
        )
        names = {t.name for t in listed.tools}
        assert "account_summary" in names
        assert "stock_search" not in names


class TestStockSearch:
    async def test_exact_name_ranks_first_and_list_is_cached(self, httpx_mock, api):
        _mock_lists(httpx_mock)
        app, _specs = build_server(api, allow_live_orders=False)
        args = {"query": "삼성전자", "markets": ["0", "10"]}
        out = await _call(app, "stock_search", args)
        assert [r["code"] for r in out["results"]] == ["005930", "005935"]
        await _call(app, "stock_search", {"query": "카카오", "markets": ["0", "10"]})
        # 두 번째 검색은 캐시를 쓴다: 시장별 리스트 요청은 한 번씩만
        assert len(httpx_mock.get_requests(url=STKINFO)) == 2

    async def test_code_and_spaces(self, httpx_mock, api):
        _mock_lists(httpx_mock)
        app, _specs = build_server(api, allow_live_orders=False)
        by_code = await _call(app, "stock_search", {"query": "028260", "markets": ["0"]})
        assert by_code["results"][0]["name"] == "삼성물산"
        spaced = await _call(app, "stock_search", {"query": "카카오 게임즈", "markets": ["10"]})
        assert spaced["results"][0]["code"] == "035720"

    async def test_follows_continuation(self, httpx_mock, api):
        httpx_mock.add_response(
            url=STKINFO,
            match_headers={"cont-yn": "N"},
            json={"return_code": 0, "list": KOSPI[:1]},
            headers={"cont-yn": "Y", "next-key": "k2"},
        )
        httpx_mock.add_response(
            url=STKINFO,
            match_headers={"cont-yn": "Y", "next-key": "k2"},
            json={"return_code": 0, "list": KOSPI[1:]},
        )
        app, _specs = build_server(api, allow_live_orders=False)
        out = await _call(app, "stock_search", {"query": "삼성", "markets": ["0"]})
        assert len(out["results"]) == 3

    async def test_empty_query_is_an_error(self, api):
        app, _specs = build_server(api, allow_live_orders=False)
        result = await app.get_request_handler("tools/call").handler(
            None, types.CallToolRequestParams(name="stock_search", arguments={"query": " "})
        )
        assert result.is_error is True


class TestSnapshotAndAccount:
    async def test_snapshot_picks_and_normalises(self, httpx_mock, api):
        httpx_mock.add_response(
            url=STKINFO,
            match_json={"stk_cd": "005930"},
            json={
                "return_code": 0,
                "return_msg": "OK",
                "stk_cd": "005930",
                "stk_nm": "삼성전자",
                "cur_prc": "+70,000",
                "flu_rt": "-1.25",
                "per": "12.3",
                "unrelated_field": "x",
            },
        )
        app, _specs = build_server(api, allow_live_orders=False)
        out = await _call(app, "stock_snapshot", {"stk_cd": "005930"})
        assert out["stk_cd"] == "005930"
        assert out["cur_prc"] == 70000
        assert out["flu_rt"] == -1.25
        assert "unrelated_field" not in out

    async def test_account_summary_sends_a_lookup_only(self, httpx_mock, api):
        httpx_mock.add_response(
            url=ACNT,
            match_json={"qry_tp": "1", "dmst_stex_tp": "KRX"},
            json={
                "return_code": 0,
                "tot_pur_amt": "000001000000",
                "tot_evlt_amt": "000001100000",
                "tot_prft_rt": "10.00",
                "acnt_evlt_remn_indv_tot": [
                    {"stk_cd": "A005930", "stk_nm": "삼성전자", "rmnd_qty": "10", "prft_rt": "10.0"}
                ],
            },
        )
        app, _specs = build_server(api, allow_live_orders=False)
        out = await _call(app, "account_summary", {})
        assert out["holdings_count"] == 1
        assert out["holdings"][0]["rmnd_qty"] == 10
        assert out["totals"]["tot_prft_rt"] == 10.0
        assert out["totals"]["tot_pur_amt"] == 1000000  # 0 채움 금액도 숫자로
        assert out["holdings"][0]["stk_cd"] == "A005930"
        (request,) = httpx_mock.get_requests(url=ACNT)
        assert request.headers["api-id"] == "kt00018"
        # 주문 엔드포인트로는 아무것도 가지 않는다
        assert not httpx_mock.get_requests(url=f"{BASE}/api/dostk/ordr")
