"""README 의 링크·이미지가 PyPI 에서도 살아 있는지 본다 — 네트워크 없이 문자열만 검사한다.

PyPI 는 pyproject 의 ``readme = "README.md"`` 를 프로젝트 페이지로 그대로 보여 주는데, 레포 기준
상대 경로(``docs/images/hero-light.png``, ``CONTRIBUTING.md``)는 pypi.org 기준으로 풀려서 깨진다.
그래서 README 두 벌은 레포 안 파일을 절대 URL(raw.githubusercontent.com / github.com/.../blob/main)
로만 가리킨다. 같은 문서 안 앵커(``#빠른-시작``)는 괜찮다.
"""

from __future__ import annotations

import re
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
READMES = ["README.md", "README.en.md"]

_MD_LINK = re.compile(r"\]\(([^)\s]+)\)")
_HTML_SRC = re.compile(r'\b(?:src|srcset|href)="([^"]+)"')
_ALLOWED = ("http://", "https://", "#", "mailto:")


@pytest.mark.parametrize("name", READMES)
def test_readme_has_no_repo_relative_links(name: str) -> None:
    text = (ROOT / name).read_text(encoding="utf-8")
    targets = _MD_LINK.findall(text) + _HTML_SRC.findall(text)
    relative = [t for t in targets if not t.startswith(_ALLOWED)]
    assert not relative, (
        f"{name}: PyPI 에서 깨지는 상대 경로 {relative} — "
        "https://raw.githubusercontent.com/younghwan91/kiwoom-client/main/... (이미지) 또는 "
        "https://github.com/younghwan91/kiwoom-client/blob/main/... (파일) 로 바꾸세요"
    )


@pytest.mark.parametrize("name", READMES)
def test_readme_in_page_anchors_exist(name: str) -> None:
    """``(#앵커)`` 링크가 실제 제목을 가리키는지 (GitHub 식 slug)."""
    text = (ROOT / name).read_text(encoding="utf-8")
    body = re.sub(r"```.*?```", "", text, flags=re.S)
    slugs = set()
    for title in re.findall(r"^#{1,6}\s+(.+?)\s*$", body, flags=re.M):
        slug = re.sub(r"[^\w\- ]", "", title.strip().lower()).replace(" ", "-")
        slugs.add(slug)
    anchors = [t[1:] for t in _MD_LINK.findall(body) if t.startswith("#")]
    missing = [a for a in anchors if a not in slugs]
    assert not missing, f"{name}: 없는 제목을 가리키는 앵커 {missing}"
