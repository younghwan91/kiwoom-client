"""생성 문서(scripts/gen_docs.py)가 코드와 어긋나지 않았는지 본다.

엔드포인트를 더하거나 docstring 이름을 바꿨다면 ``python scripts/gen_docs.py`` 를 돌려
생성 파일을 같이 커밋하면 된다.
"""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

import pytest

from kiwoom_client._registry import MODULE_NAMES
from kiwoom_client.mcp.tools import GUARDED_MODULES, discover_rest_tools

ROOT = Path(__file__).resolve().parent.parent


def _load_gen_docs():
    spec = importlib.util.spec_from_file_location("gen_docs", ROOT / "scripts" / "gen_docs.py")
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    sys.modules["gen_docs"] = module
    spec.loader.exec_module(module)
    return module


gen_docs = _load_gen_docs()


@pytest.mark.parametrize("rel", sorted(gen_docs.TARGETS))
def test_generated_file_is_up_to_date(rel):
    path = ROOT / rel
    assert path.exists(), f"{rel} 가 없습니다 — python scripts/gen_docs.py"
    assert path.read_text(encoding="utf-8") == gen_docs.TARGETS[rel](), (
        f"{rel} 가 코드와 어긋났습니다 — python scripts/gen_docs.py 로 다시 생성해 커밋하세요"
    )


def test_catalog_matches_mcp_discovery():
    """문서의 엔드포인트 목록 = MCP 서버가 노출하는 REST 도구 목록."""
    documented = {ep.tool for ep in gen_docs.rest_endpoints()}
    exposed = {spec.tool_name for spec in discover_rest_tools()}
    assert documented == exposed


def test_api_ids_are_unique_and_well_formed():
    ids = [ep.api_id for ep in gen_docs.rest_endpoints()]
    assert len(ids) == len(set(ids))
    assert all(len(i) == 7 and i[:2] in {"ka", "kt"} and i[2:].isdigit() for i in ids)


def test_every_endpoint_has_korean_and_english_name():
    """docstring 첫 줄은 ``"한글명 (English Name)"`` 꼴이어야 표에 두 이름이 다 들어간다."""
    bad = [ep.call for ep in gen_docs.rest_endpoints() if not ep.name_ko or not ep.name_en]
    bad += [c.call for c in gen_docs.ws_calls() if not c.name_ko or not c.name_en]
    assert not bad, f"docstring 첫 줄이 '한글명 (English)' 꼴이 아닙니다: {bad}"


def test_order_modules_match_mcp_guard():
    """문서가 ⚠️ 를 다는 모듈 = MCP 실주문 가드가 막는 모듈."""
    assert gen_docs.ORDER_MODULES == GUARDED_MODULES


def test_every_module_has_a_title():
    assert set(MODULE_NAMES) <= set(gen_docs.MODULE_TITLES)


def test_check_mode_reports_clean_tree(capsys):
    assert gen_docs.main(["--check"]) == 0
    assert capsys.readouterr().out == ""


def test_llms_txt_links_point_to_files_in_the_repo():
    local = [t for _, t, _, _ in gen_docs.LLMS_LINKS if "://" not in t]
    missing = [t for t in local if not (ROOT / t).exists()]
    assert not missing, f"llms.txt 가 없는 파일을 가리킵니다: {missing}"


def test_llms_txt_follows_llmstxt_format():
    """llmstxt.org: H1 제목 → 인용(>) 요약 → H2 섹션의 '- [이름](url): 설명' 목록."""
    lines = (ROOT / "llms.txt").read_text(encoding="utf-8").splitlines()
    assert lines[0] == "# kiwoom-client"
    assert next(line for line in lines[1:] if line.strip()).startswith("> ")
    sections = [line for line in lines if line.startswith("## ")]
    assert sections and sections[-1] == "## Optional"
    after_first_h2 = lines[lines.index(sections[0]):]
    links = [line for line in after_first_h2 if line.startswith("- ")]
    assert links and all(line.startswith("- [") and "](" in line for line in links)


def test_llms_full_signatures_do_not_leak_typevars():
    text = (ROOT / "llms-full.txt").read_text(encoding="utf-8")
    assert "_SyncT" not in text and "_AsyncT" not in text


def _frontmatter(path):
    text = path.read_text(encoding="utf-8")
    assert text.startswith("---\n"), f"{path}: 첫 줄이 YAML 프론트매터가 아닙니다"
    front = text.split("---\n", 2)[1]
    out = {}
    for line in front.splitlines():
        key, _, value = line.partition(":")
        out[key.strip()] = value.strip()
    return out


def test_skill_frontmatter_follows_agent_skills_spec():
    """agentskills 규격: name 은 디렉터리 이름과 같은 소문자·숫자·하이픈 64자 이내,
    description 은 1024자 이내. 본문은 500줄 아래로(긴 표는 endpoints.md 로)."""
    skill = ROOT / "skills" / "kiwoom-client" / "SKILL.md"
    meta = _frontmatter(skill)
    assert meta["name"] == skill.parent.name
    name = meta["name"]
    assert len(name) <= 64 and all(c.islower() or c.isdigit() or c == "-" for c in name)
    assert 0 < len(meta["description"]) <= 1024
    assert len(skill.read_text(encoding="utf-8").splitlines()) < 500


def test_plugin_manifests_point_at_the_skill():
    import json

    market = json.loads((ROOT / ".claude-plugin" / "marketplace.json").read_text(encoding="utf-8"))
    plugin = json.loads((ROOT / ".claude-plugin" / "plugin.json").read_text(encoding="utf-8"))
    assert market["name"] and market["owner"]["name"]
    entry = next(p for p in market["plugins"] if p["name"] == plugin["name"])
    assert entry["source"] == "./"  # 레포 루트가 플러그인 — skills/ 를 자동으로 찾는다
    assert (ROOT / "skills" / plugin["name"] / "SKILL.md").exists()
    assert "version" not in plugin  # 버전을 적으면 설치한 사람이 그 버전에 묶인다
