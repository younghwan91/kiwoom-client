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
