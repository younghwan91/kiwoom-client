"""scripts/mkdocs_hooks.py — llms.txt 복사, hreflang·canonical·sitemap 정리."""

from __future__ import annotations

import importlib.util
from pathlib import Path

_ROOT = Path(__file__).resolve().parent.parent
_SCRIPT = _ROOT / "scripts" / "mkdocs_hooks.py"


def _load():
    spec = importlib.util.spec_from_file_location("mkdocs_hooks", _SCRIPT)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_post_build_copies_llms_files_to_site_root(tmp_path):
    hooks = _load()
    hooks.on_post_build({"site_dir": str(tmp_path)})
    for name in hooks.SITE_ROOT_FILES:
        assert (tmp_path / name).read_bytes() == (_ROOT / name).read_bytes()


def test_mkdocs_config_registers_the_hook():
    assert "  - scripts/mkdocs_hooks.py" in (_ROOT / "mkdocs.yml").read_text(encoding="utf-8")


# --- hreflang · canonical · sitemap ---------------------------------------------------------------

_SITE = "https://example.org/kc/"


def test_src_to_url_follows_use_directory_urls():
    hooks = _load()
    assert hooks.src_to_url("index.md") == ""
    assert hooks.src_to_url("why.md") == "why/"
    assert hooks.src_to_url("cookbook/index.md") == "cookbook/"
    assert hooks.src_to_url("cookbook/daily-chart.md") == "cookbook/daily-chart/"


def test_has_translation_and_untranslated_urls(tmp_path):
    hooks = _load()
    for name in (
        "index.md",
        "index.en.md",
        "why.md",
        "why.en.md",
        "cookbook/index.md",
        "cookbook/a.md",
    ):
        (tmp_path / name).parent.mkdir(parents=True, exist_ok=True)
        (tmp_path / name).write_text("# x\n", encoding="utf-8")
    assert hooks.has_translation("why.md", tmp_path)
    assert hooks.has_translation("why.en.md", tmp_path)
    assert not hooks.has_translation("cookbook/a.md", tmp_path)
    assert hooks.untranslated_urls(tmp_path) == ["cookbook/a/", "cookbook/"]


_HEAD = (
    "<html><head>\n<title>t</title>\n"
    '          <link rel="alternate" href="./" hreflang="ko">\n'
    '          <link rel="alternate" href="../en/why/" hreflang="en">\n'
    '</head><body><a href="./" hreflang="ko" class="md-select__link">한국어</a></body></html>'
)


def test_rewrite_alternates_makes_absolute_and_adds_x_default():
    out = _load().rewrite_alternates(_HEAD, _SITE + "why/", translated=True)
    head = out.split("</head>")[0]
    assert '<link rel="alternate" hreflang="ko" href="https://example.org/kc/why/">' in head
    assert '<link rel="alternate" hreflang="en" href="https://example.org/kc/en/why/">' in head
    assert '<link rel="alternate" hreflang="x-default" href="https://example.org/kc/why/">' in head
    assert 'href="../en/why/"' not in head
    assert 'class="md-select__link"' in out  # 언어 전환 메뉴는 그대로


def test_rewrite_alternates_drops_hreflang_when_untranslated():
    out = _load().rewrite_alternates(_HEAD, _SITE + "why/", translated=False)
    assert "hreflang" not in out.split("</head>")[0]
    assert 'hreflang="ko" class="md-select__link"' in out


def test_rewrite_alternates_fails_loudly_if_material_format_changes():
    import pytest

    hooks = _load()
    with pytest.raises(hooks.PluginError):
        hooks.rewrite_alternates("<html><head></head></html>", _SITE, translated=True)


def _url(loc: str, alts: dict[str, str]) -> str:
    links = "".join(
        f'\n        <xhtml:link rel="alternate" hreflang="{k}" href="{v}"/>'
        for k, v in alts.items()
    )
    loc_line = f"\n        <loc>{loc}</loc>\n        <changefreq>daily</changefreq>"
    return f"\n    <url>{loc_line}{links}\n    </url>"


def test_rewrite_sitemap_drops_en_copies_and_adds_x_default():
    hooks = _load()
    ko = {"ko": _SITE + "why/", "en": _SITE + "en/why/"}
    a = {"ko": _SITE + "a/", "en": _SITE + "en/a/"}
    xml = (
        '<?xml version="1.0"?>\n<urlset>'
        + _url(_SITE + "why/", ko)
        + _url(_SITE + "a/", a)
        + _url(_SITE + "en/why/", ko)
        + _url(_SITE + "en/a/", a)
        + "\n</urlset>"
    )
    out = hooks.rewrite_sitemap(xml, _SITE, ["a/"])
    assert f"<loc>{_SITE}en/a/</loc>" not in out
    assert f'href="{_SITE}en/a/"' not in out
    assert out.count("<url>") == 3
    assert out.count('hreflang="x-default"') == 2  # why 쌍에만
    assert hooks.rewrite_sitemap(out, _SITE, ["a/"]) == out  # 멱등 (언어마다 다시 돈다)


def test_i18n_languages_match_hook_constants():
    hooks = _load()
    cfg = (_ROOT / "mkdocs.yml").read_text(encoding="utf-8")
    assert f"- locale: {hooks.DEFAULT_LANG}\n          name: 한국어\n          default: true" in cfg
    assert f"- locale: {hooks.OTHER_LANG}\n" in cfg
    assert "docs_structure: suffix" in cfg
