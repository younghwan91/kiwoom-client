"""scripts/indexnow.py — 배포 뒤 IndexNow 에 보낼 URL 고르기 (네트워크 없음)."""

from __future__ import annotations

import importlib.util
import re
from pathlib import Path

_ROOT = Path(__file__).resolve().parent.parent
_SITE = "https://younghwan91.github.io/kiwoom-client/"


def _load():
    spec = importlib.util.spec_from_file_location("indexnow", _ROOT / "scripts" / "indexnow.py")
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_key_file_is_published_with_the_key_as_content():
    mod = _load()
    assert re.fullmatch(r"[0-9a-f]{32}", mod.KEY)
    key_file = _ROOT / "docs" / f"{mod.KEY}.txt"
    assert key_file.read_text(encoding="utf-8").strip() == mod.KEY
    assert mod.key_location() == f"{_SITE}{mod.KEY}.txt"


def test_site_url_matches_mkdocs():
    mod = _load()
    assert f"site_url: {mod.SITE_URL}\n" in (_ROOT / "mkdocs.yml").read_text(encoding="utf-8")


def test_doc_url_maps_sources_to_site_urls():
    mod = _load()
    assert mod.doc_url("docs/index.md") == _SITE
    assert mod.doc_url("docs/index.en.md") == _SITE + "en/"
    assert mod.doc_url("docs/why.md") == _SITE + "why/"
    assert mod.doc_url("docs/why.en.md") == _SITE + "en/why/"
    assert mod.doc_url("docs/cookbook/index.md") == _SITE + "cookbook/"
    assert mod.doc_url("docs/cookbook/daily-chart.md") == _SITE + "cookbook/daily-chart/"
    assert mod.doc_url("src/kiwoom_client/api.py") is None
    assert mod.doc_url("docs/images/x.png") is None


_SITEMAP = [_SITE, _SITE + "why/", _SITE + "en/why/", _SITE + "cookbook/daily-chart/"]


def test_select_only_changed_pages_that_are_in_the_sitemap():
    mod = _load()
    changed = ["docs/why.en.md", "docs/cookbook/daily-chart.md", "README.md", "src/x.py"]
    assert mod.select_urls(changed, _SITEMAP) == [
        _SITE + "en/why/",
        _SITE + "cookbook/daily-chart/",
    ]
    # 영어판이 없는 페이지의 /en/ 사본은 sitemap 에 없으므로 보내지 않는다
    assert mod.select_urls(["docs/cookbook/daily-chart.en.md"], _SITEMAP) == []
    assert mod.select_urls(["CHANGELOG.md"], _SITEMAP) == []


def test_site_wide_changes_or_unknown_diff_send_everything():
    mod = _load()
    assert mod.select_urls(None, _SITEMAP) == _SITEMAP
    assert mod.select_urls(["overrides/main.html"], _SITEMAP) == _SITEMAP
    assert mod.select_urls(["mkdocs.yml"], _SITEMAP) == _SITEMAP


def test_payload_follows_the_protocol():
    mod = _load()
    body = mod.payload([_SITE])
    assert body == {
        "host": "younghwan91.github.io",
        "key": mod.KEY,
        "keyLocation": f"{_SITE}{mod.KEY}.txt",
        "urlList": [_SITE],
    }


def test_new_branch_push_means_send_everything():
    mod = _load()
    assert mod.changed_files("0" * 40, "HEAD") is None
    assert mod.changed_files("", "HEAD") is None


def test_sitemap_urls():
    xml = f"<urlset><url><loc>{_SITE}</loc></url><url><loc>{_SITE}why/</loc></url></urlset>"
    assert _load().sitemap_urls(xml) == [_SITE, _SITE + "why/"]


def test_deploy_workflow_runs_indexnow_after_deploy_without_failing_it():
    wf = (_ROOT / ".github" / "workflows" / "docs-deploy.yml").read_text(encoding="utf-8")
    job = wf.split("  indexnow:", 1)[1]
    assert "needs: deploy" in job
    assert "continue-on-error: true" in job
    assert "python3 scripts/indexnow.py" in job
