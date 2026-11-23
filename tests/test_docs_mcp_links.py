"""문서 사이트 안에서 MCP 설명은 ``docs/mcp.md`` 한 곳으로 보낸다.

예전엔 docs/ 페이지가 README 의 "MCP 서버로 사용하기" 절로 링크했다. MCP 페이지가 생긴 뒤에도
그 링크가 남아 사이트 밖(GitHub README)으로 튕겨 나갔다 — 다시 생기지 않게 막는다.
"""

from __future__ import annotations

import re
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
PAGES = [
    p
    for p in sorted((ROOT / "docs").rglob("*.md"))
    if "superpowers" not in p.relative_to(ROOT).parts
]

_README_MCP = re.compile(
    r"\]\(https://github\.com/younghwan91/kiwoom-client"
    r"(?:/blob/main/README(?:\.en|_EN)?\.md)?#(?:mcp-서버로-사용하기|using-as-an-mcp-server)\)"
)


@pytest.mark.parametrize("page", PAGES, ids=lambda p: p.relative_to(ROOT).as_posix())
def test_docs_link_to_mcp_page_not_readme_section(page: Path) -> None:
    hits = _README_MCP.findall(page.read_text(encoding="utf-8"))
    assert not hits, f"{page.name}: README 의 MCP 절 대신 [MCP 서버](mcp.md) 로 링크하세요"


def test_mcp_pages_exist() -> None:
    assert (ROOT / "docs" / "mcp.md").exists()
    assert (ROOT / "docs" / "mcp.en.md").exists()
