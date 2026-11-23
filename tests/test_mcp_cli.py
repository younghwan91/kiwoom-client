"""Tests for the kiwoom-client-mcp command line (no server is started)."""

from __future__ import annotations

import json
import subprocess
import sys

import pytest

from kiwoom_client import __version__
from kiwoom_client.mcp import cli
from kiwoom_client.mcp.client_config import (
    APP_KEY_PLACEHOLDER,
    CLIENTS,
    SERVER_NAME,
    render,
)
from kiwoom_client.mcp.guard import ENV_VAR as LIVE_ORDERS_ENV_VAR


@pytest.fixture
def no_keys(monkeypatch):
    for name in ("KIWOOM_APP_KEY", "KIWOOM_APP_SECRET", "KIWOOM_IS_MOCK", "KIWOOM_MCP_TOOLSETS",
                 "KIWOOM_MCP_MODE", "KIWOOM_MCP_MAX_ROWS"):
        monkeypatch.delenv(name, raising=False)


@pytest.fixture
def captured_run(monkeypatch):
    """Replace run_server so main() can be exercised without stdio or network."""
    calls: list[dict] = []
    import kiwoom_client.mcp.server as server

    monkeypatch.setattr(server, "run_server", lambda **kw: calls.append(kw))
    return calls


class TestHelpAndVersion:
    def test_version(self, capsys, no_keys):
        with pytest.raises(SystemExit) as exc:
            cli.main(["--version"])
        assert exc.value.code == 0
        assert __version__ in capsys.readouterr().out

    def test_help_mentions_guard_and_toolsets_without_keys(self, capsys, no_keys):
        with pytest.raises(SystemExit) as exc:
            cli.main(["--help"])
        assert exc.value.code == 0
        out = capsys.readouterr().out
        assert LIVE_ORDERS_ENV_VAR in out
        assert "--toolsets" in out
        assert "stock_info" in out

    def test_module_entry_point_runs(self):
        proc = subprocess.run(
            [sys.executable, "-m", "kiwoom_client.mcp", "--version"],
            capture_output=True,
            text=True,
            check=True,
        )
        assert __version__ in proc.stdout


#: Runs the CLI with the ``mcp`` package made unimportable, as after a plain
#: ``pip install kiwoom-client`` (no ``[mcp]`` extra).
_WITHOUT_MCP = (
    "import sys; sys.modules['mcp'] = None; "
    "from kiwoom_client.mcp.cli import main; main(sys.argv[1:])"
)


class TestWithoutMcpExtra:
    def test_help_and_config_work_without_the_mcp_package(self):
        for argv in (["--help"], ["config", "claude-desktop"]):
            proc = subprocess.run(
                [sys.executable, "-c", _WITHOUT_MCP, *argv], capture_output=True, text=True
            )
            assert proc.returncode == 0, proc.stderr
            assert proc.stdout

    def test_serving_without_the_mcp_package_explains_the_extra(self):
        env = {"KIWOOM_APP_KEY": "k", "KIWOOM_APP_SECRET": "s", "PATH": ""}
        proc = subprocess.run(
            [sys.executable, "-c", _WITHOUT_MCP], capture_output=True, text=True, env=env
        )
        assert proc.returncode == 1
        assert "kiwoom-client[mcp]" in proc.stderr


class TestServe:
    def test_missing_keys_exit_with_hint(self, capsys, no_keys, captured_run):
        with pytest.raises(SystemExit) as exc:
            cli.main([])
        assert exc.value.code == 1
        assert "config claude-code" in capsys.readouterr().err
        assert captured_run == []

    def test_defaults_to_live_and_all_toolsets(self, monkeypatch, no_keys, captured_run):
        monkeypatch.setenv("KIWOOM_APP_KEY", "k")
        monkeypatch.setenv("KIWOOM_APP_SECRET", "s")
        cli.main([])
        assert captured_run == [
            {
                "app_key": "k",
                "app_secret": "s",
                "is_mock": False,
                "toolsets": None,
                "mode": "smart",
                "max_rows": None,
            }
        ]

    def test_mock_flag_and_toolsets_flag(self, monkeypatch, no_keys, captured_run):
        monkeypatch.setenv("KIWOOM_APP_KEY", "k")
        monkeypatch.setenv("KIWOOM_APP_SECRET", "s")
        monkeypatch.setenv("KIWOOM_MCP_TOOLSETS", "account")
        cli.main(["--mock", "--toolsets", "market,chart"])
        (call,) = captured_run
        assert call["is_mock"] is True
        assert call["toolsets"] == {"market", "chart"}

    def test_explicit_all_overrides_env(self, monkeypatch, no_keys, captured_run):
        monkeypatch.setenv("KIWOOM_APP_KEY", "k")
        monkeypatch.setenv("KIWOOM_APP_SECRET", "s")
        monkeypatch.setenv("KIWOOM_MCP_TOOLSETS", "account")
        cli.main(["--toolsets", "all"])
        assert captured_run[0]["toolsets"] is None

    def test_env_toolsets_used_when_flag_absent(self, monkeypatch, no_keys, captured_run):
        monkeypatch.setenv("KIWOOM_APP_KEY", "k")
        monkeypatch.setenv("KIWOOM_APP_SECRET", "s")
        monkeypatch.setenv("KIWOOM_MCP_TOOLSETS", "account")
        cli.main([])
        assert captured_run[0]["toolsets"] == {"account"}

    def test_bad_toolset_flag_is_a_usage_error(self, capsys, no_keys, captured_run):
        with pytest.raises(SystemExit) as exc:
            cli.main(["--toolsets", "nope"])
        assert exc.value.code == 2
        assert "nope" in capsys.readouterr().err

    def test_bad_toolset_env_exits(self, monkeypatch, capsys, no_keys, captured_run):
        monkeypatch.setenv("KIWOOM_APP_KEY", "k")
        monkeypatch.setenv("KIWOOM_APP_SECRET", "s")
        monkeypatch.setenv("KIWOOM_MCP_TOOLSETS", "nope")
        with pytest.raises(SystemExit) as exc:
            cli.main([])
        assert exc.value.code == 1
        assert captured_run == []

    def test_there_is_no_flag_that_enables_live_orders(self):
        help_text = cli.build_parser().format_help()
        assert "--allow-live-orders" not in help_text


class TestConfigSnippets:
    @pytest.mark.parametrize("client", CLIENTS)
    def test_snippets_use_placeholders_and_never_enable_live_orders(self, client):
        for mock in (True, False):
            body = render(client, mock=mock).body
            assert APP_KEY_PLACEHOLDER in body
            assert LIVE_ORDERS_ENV_VAR not in body

    @pytest.mark.parametrize("client", ["claude-desktop", "cursor"])
    def test_json_snippets_are_valid_json(self, client):
        config = json.loads(render(client, toolsets=["market", "chart"]).body)
        server = config["mcpServers"][SERVER_NAME]
        assert server["command"] == "uvx"
        assert server["args"] == ["--from", "kiwoom-client[mcp]", "kiwoom-client-mcp"]
        assert server["env"]["KIWOOM_IS_MOCK"] == "true"
        assert server["env"]["KIWOOM_MCP_TOOLSETS"] == "market,chart"

    def test_codex_snippet_is_valid_toml(self):
        tomllib = pytest.importorskip("tomllib")  # Python 3.11+
        config = tomllib.loads(render("codex", mock=False, launcher="installed").body)
        server = config["mcp_servers"][SERVER_NAME]
        assert server["command"] == "kiwoom-client-mcp"
        assert server["args"] == []
        assert server["env"]["KIWOOM_IS_MOCK"] == "false"

    def test_claude_code_snippet_is_one_command(self):
        body = render("claude-code").body
        assert body.startswith(f"claude mcp add {SERVER_NAME} ")
        assert "-e KIWOOM_APP_KEY=YOUR_APP_KEY" in body
        assert body.rstrip().endswith("-- uvx --from 'kiwoom-client[mcp]' kiwoom-client-mcp")

    def test_config_command_prints_body_to_stdout_and_note_to_stderr(self, capsys, no_keys):
        cli.main(["config", "cursor", "--live", "--toolsets", "chart"])
        captured = capsys.readouterr()
        config = json.loads(captured.out)
        assert config["mcpServers"][SERVER_NAME]["env"]["KIWOOM_IS_MOCK"] == "false"
        assert "mcp.json" in captured.err
