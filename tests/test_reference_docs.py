"""docs/reference (scripts/gen_reference.py) — 모든 REST 메서드가 레퍼런스에 있고 링크가 닿는지."""

from __future__ import annotations

import re
from pathlib import Path

from kiwoom_client import spec

ROOT = Path(__file__).resolve().parent.parent
DOCS = ROOT / "docs"


def _anchors(path: Path) -> set[str]:
    return set(re.findall(r'<a id="([^"]+)"></a>', path.read_text(encoding="utf-8")))


def test_every_rest_method_has_a_reference_section():
    for (module, method), api_id in spec.endpoint_index().items():
        page = DOCS / "reference" / f"{module}.md"
        assert api_id.lower() in _anchors(page), f"{module}.{method} ({api_id})"
        assert f"`{method}()`" in page.read_text(encoding="utf-8")


def test_endpoint_table_links_resolve():
    text = (DOCS / "endpoints.md").read_text(encoding="utf-8")
    links = re.findall(r"\]\((reference/[a-z_]+\.md)#([a-z0-9]+)\)", text)
    assert len({api_id for _, api_id in links}) == len(set(spec.endpoint_index().values()))
    for rel, anchor in links:
        assert anchor in _anchors(DOCS / rel), f"{rel}#{anchor}"


def test_required_fields_are_marked():
    text = (DOCS / "reference" / "order.md").read_text(encoding="utf-8")
    assert "| `trde_tp` | 매매구분 | Y | 2 |" in text
    assert "api.order.buy_order(dmst_stex_tp=..., stk_cd=..., ord_qty=..., trde_tp=...)" in text
