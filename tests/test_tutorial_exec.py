"""docs/tutorials/: run each page's python blocks, top to bottom, on the demo backend.

The tutorials promise "paste the blocks into one file and run it with no key".
Here the blocks run in one namespace exactly like that, with the network
blocked, so a renamed method or a changed demo frame breaks the build instead
of the reader. ``SECONDS`` is shortened so the real-time step takes a moment.
Blocks marked ``<!-- docs-test: no-exec -->`` (the real-account swap) are skipped.
"""

from __future__ import annotations

import re
import textwrap
from pathlib import Path

import pytest

from tests.demo_support import no_network  # noqa: F401

TUTORIALS = Path(__file__).resolve().parents[1] / "docs" / "tutorials"
PAGES = sorted(TUTORIALS.glob("*.md"))
_NO_EXEC = {"<!-- docs-test: no-exec -->", "<!-- docs-test: skip -->"}
_FENCE = re.compile(r"^```(\w*)\s*$")


def python_blocks(page: Path) -> list[str]:
    lines = page.read_text(encoding="utf-8").splitlines()
    blocks, i = [], 0
    while i < len(lines):
        m = _FENCE.match(lines[i])
        if not m or not m.group(1):
            i += 1
            continue
        j = i + 1
        while not lines[j].startswith("```"):
            j += 1
        if m.group(1) == "python" and (i == 0 or lines[i - 1].strip() not in _NO_EXEC):
            blocks.append(textwrap.dedent("\n".join(lines[i + 1 : j])))
        i = j + 1
    return blocks


def test_tutorials_exist():
    names = {p.name for p in PAGES}
    assert {"condition-alert-bot.md", "condition-alert-bot.en.md"} <= names


@pytest.mark.usefixtures("no_network")
@pytest.mark.parametrize("page", PAGES, ids=lambda p: p.name)
def test_blocks_run_on_the_demo_backend(page, capsys):
    code = "\n\n".join(python_blocks(page))
    assert "KiwoomAPI.demo()" in code
    assert "api.order." not in code and "credit_order" not in code  # the bots never order
    code, n = re.subn(r"^SECONDS = \d+", "SECONDS = 2", code, flags=re.M)
    assert n == 1
    namespace: dict = {"__name__": "__tutorial__"}
    exec(compile(code, str(page), "exec"), namespace)
    api = namespace["api"]
    assert api.is_demo
    assert api.demo_backend.book.orders == []  # nothing reached even the paper account
    out = capsys.readouterr().out
    assert re.search(r"\(\d{6}\) [\d,]+", out), out  # at least one stock came back
