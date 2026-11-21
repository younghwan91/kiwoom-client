"""docs/troubleshooting(.en).md 의 "코드 → 예외 클래스" 가 라이브러리의 실제 매핑과 같은지 본다.

문서가 "1902 는 KiwoomStockNotFoundError" 라고 적었는데 코드가 다른 클래스를 내면, 그 문서를 보고 쓴
``except`` 는 아무것도 잡지 못한다.
"""

from __future__ import annotations

import re
from pathlib import Path

import pytest

from kiwoom_client import errors

ROOT = Path(__file__).resolve().parent.parent
PAGES = [ROOT / "docs" / "troubleshooting.md", ROOT / "docs" / "troubleshooting.en.md"]

# 표 한 줄: | 1901 · 1902 · 1903 | 뜻 | `KiwoomStockNotFoundError` | ... |
_ROW = re.compile(r"^\|\s*(?P<codes>\d{4}(?:\s*·\s*\d{4})*)\s*\|[^|]*\|\s*`(?P<cls>Kiwoom\w+)`")
# 제목·목록: ... — 8030 / 8031 ... `KiwoomServerMismatchError`
_HEADING = re.compile(r"(?P<codes>\b\d{4}(?:\s*/\s*\d{4})*)\b")


def documented_pairs(page: Path) -> list[tuple[int, str]]:
    pairs: list[tuple[int, str]] = []
    lines = page.read_text(encoding="utf-8").splitlines()
    for i, line in enumerate(lines):
        m = _ROW.match(line)
        if m:
            pairs += [(int(c), m.group("cls")) for c in re.findall(r"\d{4}", m.group("codes"))]
            continue
        if line.startswith("### ") and _HEADING.search(line):
            # 제목 다음 첫 문단에 처음 나오는 예외 클래스가 그 코드의 클래스다.
            codes = [int(c) for c in re.findall(r"\b\d{4}\b", line)]
            for follow in lines[i + 1 : i + 6]:
                if follow.startswith("#"):
                    break
                cls = re.search(r"`(Kiwoom\w+Error)`", follow)
                if cls:
                    pairs += [(c, cls.group(1)) for c in codes]
                    break
        bullet = re.match(r"^- \*\*(?P<code>\d{4})\*\*.*`(?P<cls>Kiwoom\w+Error)`", line)
        if bullet:
            pairs.append((int(bullet.group("code")), bullet.group("cls")))
    return pairs


@pytest.mark.parametrize("page", PAGES, ids=lambda p: p.name)
def test_documented_error_classes_match_the_library(page):
    pairs = documented_pairs(page)
    assert len(pairs) >= 10, "표·제목에서 코드를 거의 못 찾았다 — 파서가 문서 모양과 어긋났다"
    wrong = []
    for code, name in pairs:
        expected = getattr(errors, name)
        actual = errors.api_error_class(0, f"[{code}:문서 검사]")
        if actual is not expected:
            wrong.append(f"{code}: 문서 {name}, 코드 {actual.__name__}")
    assert not wrong, f"{page.name}: 문서의 예외 클래스가 실제와 다르다 — {wrong}"
