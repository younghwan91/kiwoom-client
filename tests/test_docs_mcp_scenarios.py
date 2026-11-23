"""The "what to ask" table in docs/mcp.md(·en) names only tools that exist."""

from __future__ import annotations

import re
from pathlib import Path

import pytest
from mcp import types

from kiwoom_client.mcp.server import build_server

DOCS = Path(__file__).resolve().parents[1] / "docs"
SECTIONS = {"mcp.md": "## 무엇을 물어보면 되나", "mcp.en.md": "## What to ask"}
NOT_TOOLS = {"confirm_token", "KIWOOM_MCP_ALLOW_LIVE_ORDERS"}


def _table_rows(page: str) -> list[list[str]]:
    text = (DOCS / page).read_text(encoding="utf-8")
    start = text.index(SECTIONS[page])
    section = text[start : text.index("\n## ", start + 1)]
    rows = [line for line in section.splitlines() if line.startswith("| ")]
    return [[cell.strip() for cell in row.strip("|").split("|")] for row in rows[1:]]


async def _all_tool_names() -> set[str]:
    # Order tools exist only with the opt-in (or on paper trading); the docs say so.
    app, _specs = build_server(api=None, allow_live_orders=True, mode="full")
    result = await app.get_request_handler("tools/list").handler(
        None, types.PaginatedRequestParams()
    )
    return {tool.name for tool in result.tools} | {"search_tools", "describe_tool", "call_tool"}


@pytest.mark.parametrize("page", sorted(SECTIONS))
async def test_every_named_tool_exists(page):
    rows = _table_rows(page)
    assert len(rows) >= 5
    known = await _all_tool_names()
    for _ask, tools, calls in rows:
        named = set(re.findall(r"`([a-z_]+)`", tools)) - NOT_TOOLS
        assert named, tools
        assert named <= known, named - known
        assert re.fullmatch(r"\d+(\u2013\d+)?", calls), calls


def test_both_languages_have_the_same_rows():
    ko, en = (_table_rows(page) for page in ("mcp.md", "mcp.en.md"))
    assert [row[1] for row in ko] != []

    def names(cell: str) -> set[str]:
        return set(re.findall(r"`([a-z_]+)`", cell))

    assert [names(r[1]) for r in ko] == [names(r[1]) for r in en]
    assert [r[2] for r in ko] == [r[2] for r in en]
