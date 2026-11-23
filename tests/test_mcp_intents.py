"""Tests for the intent tool skeleton: registry, normalisation, stock resolution."""

from __future__ import annotations

import pytest
from mcp import types

from kiwoom_client.mcp.intents import intent_tools
from kiwoom_client.mcp.intents import registry as intent_registry
from kiwoom_client.mcp.intents.limits import row_count
from kiwoom_client.mcp.intents.normalize import (
    date,
    mask_account,
    num,
    pct,
    pick,
    price,
    stock_code,
)
from kiwoom_client.mcp.intents.resolve import AmbiguousStock, StockNotFound, resolve_stock
from kiwoom_client.mcp.server import build_server
from kiwoom_client.mcp.tools import discover_rest_tools

from .intent_support import STKINFO, call, mock_api, mock_listing


@pytest.fixture
async def api(httpx_mock):
    async with mock_api(httpx_mock) as client:
        yield client


class TestNormalize:
    @pytest.mark.parametrize(
        ("raw", "expected"),
        [
            ("+70000", 70000),
            ("-1,200", -1200),
            ("000000070000", 70000),
            ("-00000001200", -1200),
            ("+1.25", 1.25),
            ("12.50%", 12.5),
            ("", None),
            ("  ", None),
            ("abc", None),
            (None, None),
            (5, 5),
        ],
    )
    def test_num(self, raw, expected):
        assert num(raw) == expected

    def test_price_drops_direction_sign(self):
        assert price("-70000") == 70000
        assert price("+000070000") == 70000
        assert price("") is None

    def test_pct_is_float(self):
        assert pct("-0.50") == -0.5
        assert isinstance(pct("3"), float)

    @pytest.mark.parametrize(
        ("raw", "expected"),
        [
            ("20261124", "2026-11-24"),
            ("202611241530", "2026-11-24T15:30"),
            ("20261124153000", "2026-11-24T15:30:00"),
            ("153000", "15:30:00"),
            ("15:30:00", "15:30:00"),
            ("", None),
        ],
    )
    def test_date(self, raw, expected):
        assert date(raw) == expected

    def test_stock_code_strips_prefix_and_suffix(self):
        assert stock_code("A005930") == "005930"
        assert stock_code("005930_NX") == "005930"
        assert stock_code("005930") == "005930"

    def test_mask_account_keeps_last_four(self):
        assert mask_account("1234567890") == "******7890"
        assert mask_account("") is None

    def test_pick_skips_absent_fields(self):
        row = pick({"cur_prc": "-100"}, {"price": ("cur_prc", price), "volume": ("trde_qty", num)})
        assert row == {"price": 100}

    def test_row_count_clamps(self):
        assert row_count(None, default=20) == 20
        assert row_count("5") == 5
        assert row_count(0) == 1
        assert row_count(10_000, maximum=100) == 100
        with pytest.raises(ValueError):
            row_count("many")


class TestResolve:
    async def test_code_needs_no_request(self, httpx_mock, api):
        assert (await resolve_stock(api, "005930")).code == "005930"
        assert (await resolve_stock(api, "a005930")).code == "005930"
        assert not httpx_mock.get_requests(url=STKINFO)

    async def test_exact_name_beats_prefix(self, httpx_mock, api):
        mock_listing(httpx_mock)
        stock = await resolve_stock(api, "삼성전자")
        assert (stock.code, stock.name) == ("005930", "삼성전자")
        assert (await resolve_stock(api, "카카오")).code == "035720"

    async def test_single_partial_match_is_accepted(self, httpx_mock, api):
        mock_listing(httpx_mock)
        assert (await resolve_stock(api, "카카오게임")).code == "293490"

    async def test_ambiguous_name_lists_candidates(self, httpx_mock, api):
        mock_listing(httpx_mock)
        with pytest.raises(AmbiguousStock) as info:
            await resolve_stock(api, "삼성")
        codes = [c["code"] for c in info.value.candidates]
        assert set(codes) == {"005930", "005935", "028260"}
        assert "삼성전자(005930)" in str(info.value)

    async def test_unknown_name(self, httpx_mock, api):
        mock_listing(httpx_mock)
        with pytest.raises(StockNotFound):
            await resolve_stock(api, "없는회사")

    async def test_blank(self, api):
        with pytest.raises(ValueError):
            await resolve_stock(api, " ")


class TestRegistry:
    def test_every_intent_tool_is_read_only(self):
        for tool in intent_tools():
            assert tool.annotations.read_only_hint is True, tool.name
            assert tool.annotations.destructive_hint is False, tool.name

    def test_names_do_not_collide_with_rest_tools(self):
        rest = {s.tool_name for s in discover_rest_tools()}
        assert not {t.name for t in intent_tools()} & rest

    def test_descriptions_carry_an_example(self):
        for tool in intent_tools():
            assert "예:" in tool.description, tool.name

    def test_duplicate_names_are_rejected(self, monkeypatch):
        factories = list(intent_registry._FACTORIES)
        monkeypatch.setattr(intent_registry, "_FACTORIES", factories + factories[:1])
        with pytest.raises(RuntimeError, match="겹칩니다"):
            intent_registry.build_intent_tools()

    async def test_server_lists_intent_tools(self):
        app, _specs = build_server(api=None, allow_live_orders=False)
        listed = await app.get_request_handler("tools/list").handler(
            None, types.PaginatedRequestParams()
        )
        names = {t.name for t in listed.tools}
        assert {t.name for t in intent_tools()} <= names


class TestSnapshotByName:
    async def test_stock_name_resolves_and_prices_lose_direction_sign(self, httpx_mock, api):
        mock_listing(httpx_mock)
        httpx_mock.add_response(
            url=STKINFO,
            match_json={"stk_cd": "005930"},
            json={
                "return_code": 0,
                "stk_cd": "005930",
                "stk_nm": "삼성전자",
                "cur_prc": "-69,000",
                "pred_pre": "-1,000",
                "flu_rt": "-1.43",
            },
        )
        app, _specs = build_server(api, allow_live_orders=False)
        is_error, out = await call(app, "stock_snapshot", {"stock": "삼성전자"})
        assert is_error is False, out
        assert out["cur_prc"] == 69000  # 하락 부호는 가격이 아니다
        assert out["pred_pre"] == -1000  # 전일대비는 부호를 유지
        assert out["flu_rt"] == -1.43

    async def test_ambiguous_name_is_a_tool_error(self, httpx_mock, api):
        mock_listing(httpx_mock)
        app, _specs = build_server(api, allow_live_orders=False)
        is_error, text = await call(app, "stock_snapshot", {"stock": "삼성"})
        assert is_error is True
        assert "후보" in text

    async def test_neither_argument_is_an_error(self, api):
        app, _specs = build_server(api, allow_live_orders=False)
        is_error, _text = await call(app, "stock_snapshot", {})
        assert is_error is True


class TestDocs:
    """Every intent tool appears in the MCP page's tool table, in both languages."""

    @pytest.mark.parametrize("page", ["docs/mcp.md", "docs/mcp.en.md"])
    def test_tool_table_lists_every_intent_tool(self, page):
        from pathlib import Path

        text = (Path(__file__).resolve().parent.parent / page).read_text(encoding="utf-8")
        missing = [t.name for t in intent_tools() if f"`{t.name}`" not in text]
        assert not missing, f"{page} 도구 표에 없음: {missing}"
