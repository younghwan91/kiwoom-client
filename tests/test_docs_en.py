"""영어판 문서의 "(Korean)" 표시가 실제와 맞는지 본다.

영어판(``docs/**/*.en.md``, ``README_EN.md``)은 아직 번역이 없는 페이지로 링크할 때
"(Korean)" 을 붙인다. 그 페이지에 ``.en.md`` 가 생기면 표시를 지워야 한다 — 남아 있으면
영어 독자가 있는 번역을 건너뛴다.
"""

from __future__ import annotations

import re
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
DOCS = ROOT / "docs"
SITE = "https://younghwan91.github.io/kiwoom-client/en/"

#: ``[text](target)`` 와 바로 뒤의 `` (Korean)``.
_LINK = re.compile(
    r"\[(?P<text>[^\]]*)\]\((?P<target>[^)\s#]+)(?:#[^)]*)?\)(?P<after>\s*\(Korean\))?"
)


def _english_pages() -> list[Path]:
    pages = sorted(p for p in DOCS.rglob("*.en.md") if "superpowers" not in p.parts)
    return [ROOT / "README_EN.md", *pages]


def _translated(page: Path, target: str) -> bool | None:
    """링크 대상에 영어판이 있으면 True, 없으면 False, 사이트 문서 링크가 아니면 None."""
    if target.startswith(SITE):
        stem = target[len(SITE):].strip("/")
        if not stem:
            candidates = [DOCS / "index.en.md"]
        else:
            candidates = [DOCS / f"{stem}.en.md", DOCS / stem / "index.en.md"]
    elif target.endswith(".md") and "://" not in target:
        src = (page.parent / target).resolve()
        candidates = [src.with_name(src.name[: -len(".md")] + ".en.md")]
    else:
        return None
    return any(c.is_file() for c in candidates)


def _korean_marked_links(page: Path) -> list[tuple[str, bool | None]]:
    out = []
    for m in _LINK.finditer(page.read_text(encoding="utf-8")):
        if "(Korean)" in m.group("text") or m.group("after"):
            out.append((m.group("target"), _translated(page, m.group("target"))))
    return out


@pytest.mark.parametrize("page", _english_pages(), ids=lambda p: p.relative_to(ROOT).as_posix())
def test_korean_marker_only_on_untranslated_pages(page: Path) -> None:
    stale = [target for target, translated in _korean_marked_links(page) if translated]
    assert not stale, f"{page.name}: 영어판이 생긴 페이지에 '(Korean)' 표시가 남아 있다 — {stale}"


def test_marker_detection_works() -> None:
    """검사가 헛돌지 않게: 상대 경로·사이트 절대 URL 링크를 둘 다 알아본다.

    외부 사이트(키움 문서 등)에 붙은 "(Korean)" 은 검사 대상이 아니다(None).
    """
    page = DOCS / "x.en.md"
    assert _translated(page, "migration-from-openapi-plus.md") is True
    assert _translated(page, "endpoints.md") is False
    assert _translated(page, SITE + "migration-from-openapi-plus/") is True
    assert _translated(page, SITE) is True
    assert _translated(page, "https://openapi.kiwoom.com/guide/apiguide") is None
    marked = [t for p in _english_pages() for t in _korean_marked_links(p)]
    assert any(translated is not None for _, translated in marked), "'(Korean)' 표시를 못 찾음"
