"""``kiwoom-client-mcp --demo`` / ``KIWOOM_MCP_DEMO``: no key needed, keys ignored."""

from __future__ import annotations

import json

import pytest

from kiwoom_client.mcp import cli
from kiwoom_client.mcp import server as mcp_server
from kiwoom_client.mcp.client_config import APP_KEY_PLACEHOLDER, CLIENTS, render


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


@pytest.mark.parametrize("client", CLIENTS)
def test_demo_snippets_need_no_key(client):
    snippet = render(client, demo=True)
    assert "--demo" in snippet.body and APP_KEY_PLACEHOLDER not in snippet.body
    assert "KIWOOM_APP_KEY" not in snippet.body and "가상 데이터" in snippet.note
    if snippet.body.lstrip().startswith("{"):
        json.loads(snippet.body)
    if client == "codex":
        tomllib = pytest.importorskip("tomllib")
        tomllib.loads(snippet.body)


def test_config_demo_flag(capsys):
    cli.main(["config", "claude-code", "--demo"])
    out = capsys.readouterr().out
    assert (
        out == "claude mcp add kiwoom -- uvx --from 'kiwoom-client[mcp]' kiwoom-client-mcp --demo\n"
    )


def test_config_demo_excludes_live():
    with pytest.raises(SystemExit):
        cli.main(["config", "cursor", "--demo", "--live"])


def test_auto_is_demo_only_without_keys(captured_run, monkeypatch):
    monkeypatch.setenv("KIWOOM_MCP_DEMO", "auto")
    cli.main([])
    monkeypatch.setenv("KIWOOM_APP_KEY", "k")
    monkeypatch.setenv("KIWOOM_APP_SECRET", "s")
    cli.main([])
    assert captured_run[0]["demo"] is True and "demo" not in captured_run[1]


def test_doctor_in_demo_needs_no_key_and_never_checks_auth():
    from kiwoom_client.mcp.doctor import Overrides, diagnose

    def no_token(*args, **kwargs):
        raise AssertionError("demo doctor must not issue a token")

    report = diagnose(env={}, flags=Overrides(demo=True), check_auth=True, issue_token=no_token)
    text = report.render()
    assert not report.failed and "데모 모드" in text and "주문 도구: 등록 (데모" in text
    auto = diagnose(env={"KIWOOM_MCP_DEMO": "auto"}, issue_token=no_token)
    assert not auto.failed and "데모 모드" in auto.render()
    keyed = diagnose(
        env={"KIWOOM_MCP_DEMO": "auto", "KIWOOM_APP_KEY": "k", "KIWOOM_APP_SECRET": "s"}
    )
    assert "데모 모드" not in keyed.render()
