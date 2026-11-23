"""The "Saving context" table in docs/mcp.md(·en) matches the real tools/list.

Tool definitions change with every intent tool, so the documented sizes
drift. Counts may be off by a couple of tools and sizes ("약 7.5 K") by 20 %, so
adding one intent tool doesn't fail; more than that means the table is stale.
"""

from __future__ import annotations

import json
import re
from pathlib import Path

import pytest
from mcp import types

from kiwoom_client.mcp.server import build_server

DOCS = Path(__file__).resolve().parents[1] / "docs"
SECTIONS = {"mcp.md": "## 컨텍스트 줄이기", "mcp.en.md": "## Saving context"}
TOLERANCE = 0.20
COUNT_SLACK = 2


def _settings(cell: str) -> dict:
    """Map the table's first column (e.g. "`--full --toolsets market,chart,account`")."""
    kwargs: dict = {"mode": "smart"}
    if "--full" in cell:
        kwargs["mode"] = "full"
    if "--discovery" in cell:
        kwargs["mode"] = "discovery"
    match = re.search(r"--toolsets ([a-z_,]+)", cell)
    if match:
        kwargs["toolsets"] = frozenset(match.group(1).split(","))
    return kwargs


def _rows(page: str) -> list[tuple[str, int, float]]:
    text = (DOCS / page).read_text(encoding="utf-8")
    start = text.index(SECTIONS[page])
    section = text[start : text.index("\n## ", start + 1)]
    rows = []
    for line in section.splitlines():
        cells = [c.strip() for c in line.strip("|").split("|")]
        if len(cells) == 3 and cells[1].isdigit():
            size = re.search(r"([\d.]+)\s*K", cells[2])
            assert size, line
            rows.append((cells[0], int(cells[1]), float(size.group(1)) * 1000))
    return rows


async def _measure(**kwargs) -> tuple[int, int]:
    app, _specs = build_server(api=None, allow_live_orders=False, **kwargs)
    result = await app.get_request_handler("tools/list").handler(
        None, types.PaginatedRequestParams()
    )
    dumped = [t.model_dump(mode="json", by_alias=True, exclude_none=True) for t in result.tools]
    return len(dumped), len(json.dumps(dumped, ensure_ascii=False))


@pytest.mark.parametrize("page", sorted(SECTIONS))
async def test_table_matches_tools_list(page):
    rows = _rows(page)
    assert len(rows) >= 3
    for setting, count, size in rows:
        real_count, real_size = await _measure(**_settings(setting))
        hint = f"docs/{page} '{SECTIONS[page]}' 표의 {setting} 행을 고치세요"
        assert abs(count - real_count) <= COUNT_SLACK, f"{hint}: 도구 {real_count}개"
        assert abs(size - real_size) <= TOLERANCE * real_size, f"{hint}: {real_size} 글자"
