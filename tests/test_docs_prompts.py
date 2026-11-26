"""docs/prompts.md(·en): every question names only tools that exist, and orders stop at a preview.

The page is meant to be pasted into an agent as-is, so a renamed or removed tool
would quietly send people to something that is not there.
"""

from __future__ import annotations

import re
from pathlib import Path

import pytest
from mcp import types

from kiwoom_client.mcp.server import build_server

DOCS = Path(__file__).resolve().parents[1] / "docs"
PAGES = {"prompts.md": "- 도구:", "prompts.en.md": "- Tools:"}
ORDER_TOOLS = {"place_order", "modify_order", "cancel_order"}
_ITEM = re.compile(r"^### \d+\. ", re.M)
_TEXT_BLOCK = re.compile(r"```text\n(.*?)\n```", re.S)
_NAME = re.compile(r"`([a-z_]+)`")


def _items(page: str) -> list[tuple[str, list[str]]]:
    """(prompt text, tool names in order) for each numbered item."""
    text = (DOCS / page).read_text(encoding="utf-8")
    chunks = _ITEM.split(text)[1:]
    out = []
    for chunk in chunks:
        block = _TEXT_BLOCK.search(chunk)
        assert block, chunk[:80]
        tools_line = next(line for line in chunk.splitlines() if line.startswith(PAGES[page]))
        out.append((block.group(1), _NAME.findall(tools_line)))
    return out


async def _all_tool_names() -> set[str]:
    # Order tools exist only with the opt-in (or on paper trading); the page says so.
    app, _specs = build_server(api=None, allow_live_orders=True, mode="full")
    result = await app.get_request_handler("tools/list").handler(
        None, types.PaginatedRequestParams()
    )
    return {tool.name for tool in result.tools} | {"search_tools", "describe_tool", "call_tool"}


@pytest.mark.parametrize("page", sorted(PAGES))
async def test_every_named_tool_exists(page):
    items = _items(page)
    assert 15 <= len(items) <= 20
    known = await _all_tool_names()
    for _prompt, tools in items:
        assert tools
        assert set(tools) <= known, set(tools) - known


@pytest.mark.parametrize("page", sorted(PAGES))
def test_orders_go_through_a_preview_first(page):
    for prompt, tools in _items(page):
        sends = [i for i, name in enumerate(tools) if name in ORDER_TOOLS]
        if sends:
            assert "order_preview" in tools[: sends[0]], prompt


@pytest.mark.parametrize("page", sorted(PAGES))
def test_prompts_ask_for_lookups_not_picks(page):
    for prompt, _tools in _items(page):
        assert not re.search(r"추천|recommend", prompt, re.I), prompt


def test_both_languages_list_the_same_tools():
    ko, en = (_items(page) for page in sorted(PAGES))
    assert [tools for _p, tools in ko] == [tools for _p, tools in en]
