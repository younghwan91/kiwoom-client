"""Packaging checks for the MCP server: extra pin, registry manifest, uvx-style launch."""

from __future__ import annotations

import json
import re
from importlib.metadata import version
from pathlib import Path

from kiwoom_client.mcp.guard import ENV_VAR as LIVE_ORDERS_ENV_VAR

ROOT = Path(__file__).resolve().parent.parent
PYPROJECT = (ROOT / "pyproject.toml").read_text(encoding="utf-8")
SERVER_JSON = json.loads((ROOT / "server.json").read_text(encoding="utf-8"))


def _project_version() -> str:
    match = re.search(r'^version = "([^"]+)"', PYPROJECT, re.M)
    assert match
    return match.group(1)


class TestMcpExtra:
    def test_extra_requires_mcp_2(self):
        # The server uses the mcp 2.x lowlevel API (ServerRequestContext,
        # add_request_handler); 1.x fails at import.
        assert '"mcp>=2.0,<3"' in PYPROJECT

    def test_installed_mcp_matches_the_pin(self):
        assert version("mcp").split(".")[0] == "2"

    def test_console_script_points_at_the_cli(self):
        assert 'kiwoom-client-mcp = "kiwoom_client.mcp.cli:main"' in PYPROJECT


class TestServerJson:
    def test_versions_track_pyproject(self):
        project = _project_version()
        (package,) = SERVER_JSON["packages"]
        assert SERVER_JSON["version"] == project
        assert package["version"] == project
        assert package["runtimeArguments"][0]["value"] == f"kiwoom-client[mcp]=={project}"

    def test_package_is_this_pypi_project_over_stdio(self):
        (package,) = SERVER_JSON["packages"]
        assert package["registryType"] == "pypi"
        assert package["identifier"] == "kiwoom-client"
        assert package["transport"] == {"type": "stdio"}

    def test_keys_are_secret_and_defaults_are_safe(self):
        (package,) = SERVER_JSON["packages"]
        env = {item["name"]: item for item in package["environmentVariables"]}
        assert env["KIWOOM_APP_KEY"]["isSecret"] is True
        assert env["KIWOOM_APP_SECRET"]["isSecret"] is True
        assert env["KIWOOM_IS_MOCK"]["default"] == "true"
        # Live orders stay a deliberate, manual opt-in — never a registry form field.
        assert LIVE_ORDERS_ENV_VAR not in env

    def test_description_fits_the_registry_limit(self):
        assert len(SERVER_JSON["description"]) <= 100

    def test_name_matches_the_github_namespace(self):
        assert SERVER_JSON["name"] == "io.github.younghwan91/kiwoom-client"
        assert SERVER_JSON["repository"]["url"].endswith("/younghwan91/kiwoom-client")


class TestServerMetadata:
    def test_initialize_reports_version_and_instructions(self):
        from kiwoom_client import __version__
        from kiwoom_client.mcp.server import build_server

        app, _specs = build_server(api=None, allow_live_orders=False)
        options = app.create_initialization_options()
        assert options.server_version == __version__
        assert "order_preview" in (options.instructions or "")
        assert "kiwoom://guide" in (options.instructions or "")


def test_readme_carries_the_registry_ownership_marker():
    # The MCP registry verifies PyPI ownership by finding this string in the
    # package README (pyproject readme = README.md).
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    assert f"mcp-name: {SERVER_JSON['name']}" in readme
