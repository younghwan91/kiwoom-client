"""``kiwoom-client-mcp --demo`` / ``KIWOOM_MCP_DEMO``: no key needed, keys ignored."""

from __future__ import annotations

import pytest

from kiwoom_client.mcp import cli
from kiwoom_client.mcp import server as mcp_server


@pytest.fixture
def captured_run(monkeypatch):
    calls: list[dict] = []
    monkeypatch.setattr(mcp_server, "run_server", lambda **kw: calls.append(kw))
    for name in (
        "KIWOOM_APP_KEY",
        "KIWOOM_APP_SECRET",
        "KIWOOM_IS_MOCK",
        "KIWOOM_MCP_DEMO",
        "KIWOOM_MCP_TOOLSETS",
        "KIWOOM_MCP_MODE",
        "KIWOOM_MCP_MAX_ROWS",
    ):
        monkeypatch.delenv(name, raising=False)  # fmt: skip
    return calls


def test_cli_demo_needs_no_key(captured_run, capsys):
    cli.main(["--demo"])
    assert captured_run[0]["demo"] is True and captured_run[0]["app_key"] == ""
    assert capsys.readouterr().err == ""


def test_cli_demo_from_env(captured_run, monkeypatch):
    monkeypatch.setenv("KIWOOM_MCP_DEMO", "true")
    cli.main([])
    assert captured_run[0]["demo"] is True


def test_cli_demo_wins_over_keys_and_warns(captured_run, monkeypatch, capsys):
    monkeypatch.setenv("KIWOOM_APP_KEY", "real-key")
    monkeypatch.setenv("KIWOOM_APP_SECRET", "real-secret")
    cli.main(["--demo"])
    assert captured_run[0]["app_key"] == "" and captured_run[0]["demo"] is True
    assert "쓰지 않습니다" in capsys.readouterr().err


def test_cli_bad_demo_env_exits(captured_run, monkeypatch):
    monkeypatch.setenv("KIWOOM_MCP_DEMO", "maybe")
    with pytest.raises(SystemExit):
        cli.main([])
    assert captured_run == []


def test_missing_keys_hint_mentions_demo(captured_run, capsys):
    with pytest.raises(SystemExit):
        cli.main([])
    assert "--demo" in capsys.readouterr().err


def test_real_mode_does_not_pass_demo(captured_run, monkeypatch):
    monkeypatch.setenv("KIWOOM_APP_KEY", "k")
    monkeypatch.setenv("KIWOOM_APP_SECRET", "s")
    cli.main([])
    assert "demo" not in captured_run[0]
