"""scripts/check_site_seo.py(사이트 OG·Twitter·JSON-LD 검사기)와 overrides/main.html 의 사실 값."""

from __future__ import annotations

import importlib.util
import json
import re
import struct
from pathlib import Path

_ROOT = Path(__file__).resolve().parent.parent


def _load():
    spec = importlib.util.spec_from_file_location(
        "check_site_seo", _ROOT / "scripts" / "check_site_seo.py"
    )
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


_GOOD_META = """
<meta name="description" content="d">
<link rel="canonical" href="https://example.org/x/">
<meta property="og:title" content="t">
<meta property="og:description" content="d">
<meta property="og:url" content="https://example.org/x/">
<meta property="og:image" content="https://example.org/i.png">
<meta property="og:locale" content="ko_KR">
<meta name="twitter:card" content="summary_large_image">
"""

_JSONLD = {
    "@context": "https://schema.org",
    "@graph": [
        {
            "@type": "SoftwareSourceCode",
            "name": "n",
            "description": "d",
            "codeRepository": "https://github.com/x/y",
            "programmingLanguage": {"@type": "ComputerLanguage", "name": "Python"},
            "license": "https://opensource.org/licenses/MIT",
        },
        {
            "@type": "SoftwareApplication",
            "name": "n",
            "description": "d",
            "applicationCategory": "FinanceApplication",
            "offers": {"@type": "Offer", "price": "0"},
            "license": "https://opensource.org/licenses/MIT",
        },
    ],
}


def _page(head: str) -> str:
    return f"<!doctype html><html><head>{head}</head><body><p>본문</p></body></html>"


def test_good_page_passes():
    assert _load().check_page("why/index.html", _page(_GOOD_META)) == []


def test_missing_og_and_relative_image_are_reported():
    head = _GOOD_META.replace('<meta property="og:title" content="t">', "").replace(
        "https://example.org/i.png", "images/i.png"
    )
    problems = _load().check_page("why/index.html", _page(head))
    assert any("og:title" in p for p in problems)
    assert any("og:image" in p for p in problems)


def test_og_url_must_match_canonical():
    head = _GOOD_META.replace(
        'og:url" content="https://example.org/x/"', 'og:url" content="https://example.org/y/"'
    )
    assert any("og:url" in p for p in _load().check_page("why/index.html", _page(head)))


def test_home_needs_jsonld_and_other_pages_must_not_have_it():
    mod = _load()
    script = f'<script type="application/ld+json">{json.dumps(_JSONLD)}</script>'
    assert mod.check_page("index.html", _page(_GOOD_META + script)) == []
    assert any("JSON-LD" in p for p in mod.check_page("index.html", _page(_GOOD_META)))
    assert any("JSON-LD" in p for p in mod.check_page("why/index.html", _page(_GOOD_META + script)))


def test_check_site_walks_html_and_skips_404(tmp_path):
    mod = _load()
    (tmp_path / "index.html").write_text(_page(_GOOD_META), encoding="utf-8")  # 홈인데 JSON-LD 없음
    (tmp_path / "404.html").write_text("<html><head></head></html>", encoding="utf-8")
    bad = mod.check_site(tmp_path)
    assert list(bad) == ["index.html"]


def test_template_facts_match_pyproject_and_image():
    """overrides/main.html 이 적는 라이선스·이미지 크기가 실제와 같다."""
    template = (_ROOT / "overrides" / "main.html").read_text(encoding="utf-8")
    pyproject = (_ROOT / "pyproject.toml").read_text(
        encoding="utf-8"
    )  # tomllib 은 3.11+ 라 정규식으로
    assert re.search(r'^license = "MIT"$', pyproject, re.M) and "licenses/MIT" in template
    assert (
        re.search(r'^requires-python = ">=3.10"$', pyproject, re.M) and "Python 3.10+" in template
    )
    png = (_ROOT / "docs" / "images" / "social-preview.png").read_bytes()
    width, height = struct.unpack(">II", png[16:24])
    assert f'og:image:width" content="{width}"' in template
    assert f'og:image:height" content="{height}"' in template


def test_mkdocs_uses_the_overrides_dir_and_ci_runs_the_checker():
    assert "  custom_dir: overrides" in (_ROOT / "mkdocs.yml").read_text(encoding="utf-8")
    for wf in ("ci.yml", "docs-deploy.yml"):
        assert "scripts/check_site_seo.py site" in (_ROOT / ".github" / "workflows" / wf).read_text(
            encoding="utf-8"
        )


def test_hreflang_must_be_absolute_and_complete():
    mod = _load()
    rel = (
        '<link rel="alternate" hreflang="ko" href="./">'
        '<link rel="alternate" hreflang="en" href="../en/x/">'
    )
    problems = mod.check_page("x/index.html", _page(_GOOD_META + rel))
    assert any("x-default" in p or "세트" in p for p in problems)
    assert any("절대 URL" in p for p in problems)
    good = (
        '<link rel="alternate" hreflang="ko" href="https://example.org/x/">'
        '<link rel="alternate" hreflang="en" href="https://example.org/en/x/">'
        '<link rel="alternate" hreflang="x-default" href="https://example.org/x/">'
    )
    assert mod.check_page("x/index.html", _page(_GOOD_META + good)) == []


def test_sitemap_must_not_list_pages_canonicalised_elsewhere():
    mod = _load()
    root = "https://example.org/"
    canonicals = {"index.html": root, "x/index.html": root + "x/", "en/x/index.html": root + "x/"}
    ok = f"<urlset><url><loc>{root}</loc></url><url><loc>{root}x/</loc></url></urlset>"
    assert mod.check_sitemap(ok, root, canonicals) == []
    bad = ok.replace(
        "</urlset>", f"<url><loc>{root}en/x/</loc></url><url><loc>{root}x/</loc></url></urlset>"
    )
    problems = mod.check_sitemap(bad, root, canonicals)
    assert any("두 번" in p for p in problems)
    assert any("canonical" in p for p in problems)


# --- 페이지별 검색 제목·설명 (front matter) -------------------------------------

#: 검색 의도가 분명한 주요 페이지 — 한국어판과(있으면) 영어판 모두
#: seo_title·description 이 있어야 한다.
KEY_PAGES = (
    "index",
    "why",
    "migration-from-openapi-plus",
    "mcp",
    "faq",
    "troubleshooting",
    "cookbook/index",
    "ai-tools",
    "convenience",
    "resources",
    "showcase",
)


def _front_matter(path: Path) -> dict[str, str]:
    """``key: "value"`` 꼴 줄만 읽는다.

    값은 JSON 문자열 — 콜론이 들어가도 YAML 이 안 깨지게 따옴표로 감싼다.
    """
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        return {}
    out = {}
    for line in text[4:].split("\n---\n", 1)[0].splitlines():
        key, sep, value = line.partition(": ")
        if sep and value.startswith('"'):
            out[key] = json.loads(value)
    return out


def _key_page_files() -> list[Path]:
    docs = _ROOT / "docs"
    files = []
    for stem in KEY_PAGES:
        files.append(docs / f"{stem}.md")
        if (docs / f"{stem}.en.md").is_file():
            files.append(docs / f"{stem}.en.md")
    return files


def test_key_pages_have_search_title_and_description():
    for path in _key_page_files():
        fm = _front_matter(path)
        rel = path.relative_to(_ROOT)
        assert 20 <= len(fm.get("seo_title", "")) <= 80, f"{rel}: seo_title 20~80자"
        assert 50 <= len(fm.get("description", "")) <= 180, f"{rel}: description 50~180자"


def test_english_pages_have_english_meta():
    for path in _key_page_files():
        if path.name.endswith(".en.md"):
            fm = _front_matter(path)
            assert not re.search(r"[가-힣]", fm["seo_title"] + fm["description"]), path.name
