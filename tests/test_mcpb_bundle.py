"""The Claude Desktop bundle (mcpb/) stays consistent with the package.

No node, no network: packing and the official ``mcpb validate`` run in CI
(``python scripts/build_mcpb.py``). These tests pin what the schema can't —
versions, env var names, defaults and the live-order rule.
"""

from __future__ import annotations

import importlib.util
import json
import re
import subprocess
import sys
from pathlib import Path

import pytest
from mcp import types

from kiwoom_client import __version__
from kiwoom_client._env import ENV_IS_MOCK
from kiwoom_client.mcp import cli
from kiwoom_client.mcp import server as server_module
from kiwoom_client.mcp.guard import ENV_VAR as LIVE_ORDERS_ENV_VAR
from kiwoom_client.mcp.modes import DEFAULT_MODE, MODES
from kiwoom_client.mcp.modes import ENV_VAR as MODE_ENV_VAR
from kiwoom_client.mcp.server import build_server
from kiwoom_client.mcp.toolsets import ENV_VAR as TOOLSETS_ENV_VAR

ROOT = Path(__file__).resolve().parents[1]
BUNDLE = ROOT / "mcpb"


def _load_script():
    spec = importlib.util.spec_from_file_location("build_mcpb", ROOT / "scripts" / "build_mcpb.py")
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


build_mcpb = _load_script()
MANIFEST = json.loads((BUNDLE / "manifest.json").read_text(encoding="utf-8"))
ENV = MANIFEST["server"]["mcp_config"]["env"]
USER_CONFIG = MANIFEST["user_config"]


def test_sources_pass_the_build_checks():
    assert build_mcpb.check_sources() == []


def test_versions_match_the_package():
    assert MANIFEST["version"] == __version__ == build_mcpb.package_version()
    assert build_mcpb.bundle_version() == (__version__, __version__)


def test_uv_server_type_from_manifest_0_4():
    assert MANIFEST["manifest_version"] == "0.4"
    server = MANIFEST["server"]
    assert server["type"] == "uv"
    assert (BUNDLE / server["entry_point"]).is_file()
    args = server["mcp_config"]["args"]
    assert server["mcp_config"]["command"] == "uv"
    assert "${__dirname}" in args and server["entry_point"] in args
    assert not (BUNDLE / "server" / "lib").exists() and not (BUNDLE / "server" / "venv").exists()


def test_runs_everywhere_the_package_runs():
    compat = MANIFEST["compatibility"]
    assert set(compat["platforms"]) == {"darwin", "win32", "linux"}
    pyproject = (ROOT / "pyproject.toml").read_text(encoding="utf-8")
    requires = re.search(r'^requires-python\s*=\s*"([^"]+)"', pyproject, re.MULTILINE)
    assert requires and compat["runtimes"]["python"] == requires.group(1)


def test_env_uses_the_package_variable_names():
    assert set(ENV) == {
        "KIWOOM_APP_KEY",
        "KIWOOM_APP_SECRET",
        ENV_IS_MOCK,
        MODE_ENV_VAR,
        TOOLSETS_ENV_VAR,
    }


def test_keys_are_sensitive_and_required():
    for key in ("app_key", "app_secret"):
        assert USER_CONFIG[key]["type"] == "string"
        assert USER_CONFIG[key]["sensitive"] is True
        assert USER_CONFIG[key]["required"] is True


def test_defaults_are_mock_and_smart():
    assert USER_CONFIG["is_mock"] == {**USER_CONFIG["is_mock"], "type": "boolean", "default": True}
    assert USER_CONFIG["mode"]["default"] == DEFAULT_MODE
    for mode in MODES:
        assert mode in USER_CONFIG["mode"]["description"]
    assert USER_CONFIG["toolsets"]["default"] == ""


def test_never_enables_live_orders():
    assert LIVE_ORDERS_ENV_VAR in build_mcpb.FORBIDDEN_ENV
    for path in BUNDLE.rglob("*"):
        if path.is_file():
            assert LIVE_ORDERS_ENV_VAR not in path.read_text(encoding="utf-8", errors="ignore")


def test_check_sources_catches_a_live_order_opt_in(tmp_path):
    bundle = tmp_path / "mcpb"
    build_mcpb.stage(bundle)
    manifest = json.loads((bundle / "manifest.json").read_text(encoding="utf-8"))
    manifest["server"]["mcp_config"]["env"][LIVE_ORDERS_ENV_VAR] = "true"
    manifest["version"] = "9.9.9"
    (bundle / "manifest.json").write_text(json.dumps(manifest), encoding="utf-8")
    problems = build_mcpb.check_sources(bundle=bundle)
    assert any(LIVE_ORDERS_ENV_VAR in p for p in problems)
    assert any("9.9.9" in p for p in problems)


async def test_declared_tools_exist_in_the_default_listing():
    app, _specs = build_server(api=None, allow_live_orders=False, mode=DEFAULT_MODE)
    result = await app.get_request_handler("tools/list").handler(
        None, types.PaginatedRequestParams()
    )
    listed = {tool.name for tool in result.tools}
    assert {tool["name"] for tool in MANIFEST["tools"]} <= listed
    assert MANIFEST["tools_generated"] is True


@pytest.mark.parametrize(
    ("is_mock", "mode", "toolsets", "expected"),
    [
        ("true", "smart", "", (True, "smart", None)),
        ("false", "", "", (False, "smart", None)),
        ("true", "full", "market,chart", (True, "full", {"market", "chart"})),
    ],
)
def test_cli_reads_values_as_the_host_substitutes_them(
    monkeypatch, is_mock, mode, toolsets, expected
):
    """Claude Desktop puts user_config values into env as strings."""
    calls: list[dict] = []
    monkeypatch.setattr(server_module, "run_server", lambda **kw: calls.append(kw))
    values = {"app_key": "k", "app_secret": "s", "is_mock": is_mock, "mode": mode}
    values["toolsets"] = toolsets
    for name, template in ENV.items():
        key = re.fullmatch(r"\$\{user_config\.(\w+)\}", template)
        assert key, template
        monkeypatch.setenv(name, values[key.group(1)])
    cli.main([])
    (call,) = calls
    assert (call["is_mock"], call["mode"], call["toolsets"]) == expected


def test_entry_point_runs_the_cli():
    proc = subprocess.run(
        [sys.executable, str(BUNDLE / MANIFEST["server"]["entry_point"]), "--version"],
        capture_output=True,
        text=True,
        check=True,
    )
    assert __version__ in proc.stdout
