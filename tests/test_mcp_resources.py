"""Tests for MCP resources (guide, tool index, code tables, TR template) and prompts."""

from __future__ import annotations

import json
import re

import pytest
from mcp import types

from kiwoom_client import spec
from kiwoom_client.codes import OrderType, StockListMarket
from kiwoom_client.mcp.codes import (
    LIMIT_PRICE_TRADE_TYPES,
    NO_PRICE_TRADE_TYPES,
    STOCK_LIST_MARKETS,
    TRADE_TYPES,
)
from kiwoom_client.mcp.resources import (
    GUIDE_URI,
    INSTRUCTIONS,
    MARKETS_URI,
    TOOLS_URI,
    TR_URI_TEMPLATE,
    TRADE_TYPES_URI,
)
from kiwoom_client.mcp.server import build_server


def _handler(app, method):
    return app.get_request_handler(method).handler


async def _read(app, uri: str) -> types.TextResourceContents:
    result = await _handler(app, "resources/read")(None, types.ReadResourceRequestParams(uri=uri))
    (content,) = result.contents
    return content


async def _prompt(app, name: str, arguments: dict[str, str] | None = None) -> str:
    result = await _handler(app, "prompts/get")(
        None, types.GetPromptRequestParams(name=name, arguments=arguments)
    )
    return result.messages[0].content.text


async def _tool_names(app) -> set[str]:
    listed = await _handler(app, "tools/list")(None, types.PaginatedRequestParams())
    return {t.name for t in listed.tools}


class TestCodes:
    def test_trade_types_match_the_enum(self):
        assert {m.value for m in OrderType} == set(TRADE_TYPES)
        assert TRADE_TYPES["3"] == "시장가"

    def test_stock_list_markets_match_the_enum(self):
        assert {m.value for m in StockListMarket} == set(STOCK_LIST_MARKETS)
        assert STOCK_LIST_MARKETS["10"] == "코스닥"

    def test_price_classes_only_use_known_codes_and_do_not_overlap(self):
        assert set(TRADE_TYPES) >= LIMIT_PRICE_TRADE_TYPES | NO_PRICE_TRADE_TYPES
        assert not LIMIT_PRICE_TRADE_TYPES & NO_PRICE_TRADE_TYPES


class TestResources:
    async def test_list_and_templates(self):
        app, _specs = build_server(api=None, allow_live_orders=False)
        listed = await _handler(app, "resources/list")(None, types.PaginatedRequestParams())
        assert {str(r.uri) for r in listed.resources} == {
            GUIDE_URI,
            TOOLS_URI,
            TRADE_TYPES_URI,
            MARKETS_URI,
        }
        templates = await _handler(app, "resources/templates/list")(
            None, types.PaginatedRequestParams()
        )
        assert [t.uri_template for t in templates.resource_templates] == [TR_URI_TEMPLATE]

    async def test_capabilities_advertise_resources_and_prompts(self):
        app, _specs = build_server(api=None, allow_live_orders=False)
        caps = app.create_initialization_options().capabilities
        assert caps.resources is not None
        assert caps.prompts is not None
        assert caps.tools is not None

    async def test_guide_is_markdown_and_states_the_order_rule(self):
        app, _specs = build_server(api=None, allow_live_orders=False)
        guide = await _read(app, GUIDE_URI)
        assert guide.mime_type == "text/markdown"
        assert "order_preview" in guide.text
        assert "KIWOOM_MCP_ALLOW_LIVE_ORDERS" in guide.text

    async def test_tool_index_follows_the_guard(self):
        for allow in (False, True):
            app, _specs = build_server(api=None, allow_live_orders=allow)
            index = json.loads((await _read(app, TOOLS_URI)).text)
            names = {item["name"] for item in index}
            assert names == await _tool_names(app)
            assert ("order_buy_order" in names) is allow
        basic = next(i for i in index if i["name"] == "stock_info_basic_stock_info")
        assert basic["api_id"] == "ka10001"
        assert basic["read_only"] is True

    async def test_tool_index_in_discovery_mode_lists_the_catalog_not_meta_tools(self):
        app, _specs = build_server(api=None, allow_live_orders=False, discovery=True)
        names = {item["name"] for item in json.loads((await _read(app, TOOLS_URI)).text)}
        assert "stock_info_basic_stock_info" in names
        assert "call_tool" not in names
        assert "order_buy_order" not in names

    async def test_code_tables(self):
        app, _specs = build_server(api=None, allow_live_orders=False)
        trade = json.loads((await _read(app, TRADE_TYPES_URI)).text)
        assert trade["trde_tp"]["0"] == "보통"
        assert set(trade["dmst_stex_tp"]) == {"KRX", "NXT", "SOR"}
        markets = json.loads((await _read(app, MARKETS_URI)).text)
        assert markets["mrkt_tp"]["10"] == "코스닥"

    async def test_tr_template(self):
        app, _specs = build_server(api=None, allow_live_orders=False)
        detail = json.loads((await _read(app, "kiwoom://tr/ka10001")).text)
        assert detail["api_id"] == "ka10001"
        assert detail["request"][0]["id"] == "stk_cd"
        assert any(f["id"] == "cur_prc" for f in detail["response"])

    @pytest.mark.parametrize("uri", ["kiwoom://tr/nope", "kiwoom://nothing"])
    async def test_unknown_uri_raises(self, uri):
        app, _specs = build_server(api=None, allow_live_orders=False)
        with pytest.raises(ValueError, match="Unknown resource"):
            await _read(app, uri)


class TestInstructions:
    def test_flow_intent_tools_then_search_then_confirmed_orders(self):
        text = INSTRUCTIONS
        for word in ("stock_search", "search_tools", "call_tool", "order_preview", "확인"):
            assert word in text, word
        assert text.index("stock_search") < text.index("search_tools") < text.index("order_preview")
        assert "confirm_token" in text
        assert "kiwoom://guide" in text

    def test_stays_short(self):
        # Clients put this in front of the model on every session.
        assert len(INSTRUCTIONS) < 500

    async def test_named_tools_exist_in_the_smart_listing(self):
        app, _specs = build_server(api=None, allow_live_orders=False, mode="smart")
        listed = await _tool_names(app)
        named = set(re.findall(r"\b[a-z]+(?:_[a-z]+)+\b", INSTRUCTIONS)) - {
            "max_rows",
            "confirm_token",
        }
        assert named <= listed


class TestPrompts:
    async def test_list(self):
        app, _specs = build_server(api=None, allow_live_orders=False)
        listed = await _handler(app, "prompts/list")(None, types.PaginatedRequestParams())
        assert {p.name for p in listed.prompts} == {
            "analyze_stock",
            "review_account",
            "market_today",
            "rebalance",
            "order_checklist",
        }

    async def test_analyze_stock_mentions_the_stock(self):
        app, _specs = build_server(api=None, allow_live_orders=False)
        text = await _prompt(app, "analyze_stock", {"stock": "삼성전자"})
        assert "삼성전자" in text
        assert "stock_search" in text

    async def test_order_checklist_requires_preview_and_confirmation(self):
        app, _specs = build_server(api=None, allow_live_orders=False)
        text = await _prompt(app, "order_checklist", {"request": "삼성전자 1주 매수"})
        assert "order_preview" in text
        assert "확인" in text

    async def test_market_today_focus_is_optional(self):
        app, _specs = build_server(api=None, allow_live_orders=False)
        plain = await _prompt(app, "market_today")
        focused = await _prompt(app, "market_today", {"focus": "반도체"})
        assert "반도체" not in plain and "반도체" in focused
        assert "주문" in plain  # 조회만 한다는 문구

    async def test_rebalance_previews_and_waits_for_confirmation(self):
        app, _specs = build_server(api=None, allow_live_orders=False)
        text = await _prompt(app, "rebalance", {"target": "삼성전자 30%, 현금 70%"})
        assert "삼성전자 30%" in text
        assert "order_preview" in text
        assert "확인" in text
        assert "confirm_token" in text

    async def test_order_prompts_point_to_the_confirm_token(self):
        app, _specs = build_server(api=None, allow_live_orders=False)
        text = await _prompt(app, "order_checklist", {"request": "x"})
        assert "confirm_token" in text

    @pytest.mark.parametrize(
        ("name", "arguments"), [("analyze_stock", {}), ("rebalance", {}), ("order_checklist", {})]
    )
    async def test_required_argument_missing(self, name, arguments):
        app, _specs = build_server(api=None, allow_live_orders=False)
        with pytest.raises(ValueError):
            await _prompt(app, name, arguments)

    async def test_unknown_prompt(self):
        app, _specs = build_server(api=None, allow_live_orders=False)
        with pytest.raises(ValueError, match="Unknown prompt"):
            await _prompt(app, "nope")

    async def test_every_tool_a_prompt_names_exists(self):
        """Prompts name tools in prose — catch a rename before an agent does."""
        app, _specs = build_server(api=None, allow_live_orders=False)
        exposed = await _tool_names(app)
        texts = [
            await _prompt(app, "analyze_stock", {"stock": "x"}),
            await _prompt(app, "review_account"),
            await _prompt(app, "market_today"),
            await _prompt(app, "rebalance", {"target": "x"}),
            await _prompt(app, "order_checklist", {"request": "x"}),
            (await _read(app, GUIDE_URI)).text,
        ]
        mentioned = set()
        for text in texts:
            mentioned |= set(re.findall(r"\b[a-z]+(?:_[a-z0-9]+)+\b", text))
        tool_like = {m for m in mentioned if m in exposed or m.split("_")[0] in {
            "stock", "chart", "account", "order", "market", "ranking", "sector",
            "foreign",
        }}  # fmt: skip
        non_tools = {"order_tools_enabled", "max_rows", "next_key", "cont_yn"}
        assert tool_like - non_tools <= exposed

    def test_tr_template_matches_catalog_ids(self):
        assert spec.get("ka10099").request_field("mrkt_tp") is not None
