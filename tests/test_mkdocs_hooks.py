"""scripts/mkdocs_hooks.py — llms.txt 를 사이트 루트에 싣는 훅."""

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
