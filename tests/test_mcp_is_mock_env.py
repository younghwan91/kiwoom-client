"""KIWOOM_IS_MOCK must mean the same thing to the MCP server as to from_env().

Before: the server compared with ``== "true"``, so ``1``/``yes`` and typos like
``ture`` silently connected to the **live** server while ``KiwoomAPI.from_env``
read ``1``/``yes`` as mock. Now both use ``kiwoom_client._env.parse_bool``.
"""

from __future__ import annotations

import pytest

from kiwoom_client._env import resolve_credentials
from kiwoom_client.mcp import cli
from kiwoom_client.mcp.cli import resolve_is_mock


@pytest.fixture
def captured_run(monkeypatch):
    calls: list[dict] = []
    import kiwoom_client.mcp.server as server

    monkeypatch.setattr(server, "run_server", lambda **kw: calls.append(kw))
    monkeypatch.setenv("KIWOOM_APP_KEY", "k")
    monkeypatch.setenv("KIWOOM_APP_SECRET", "s")
    for name in ("KIWOOM_MCP_TOOLSETS", "KIWOOM_MCP_MODE", "KIWOOM_MCP_MAX_ROWS"):
        monkeypatch.delenv(name, raising=False)
    return calls


@pytest.mark.parametrize(
    ("value", "expected"),
    [
        ("true", True),
        ("TRUE", True),
        ("1", True),
        ("yes", True),
        ("on", True),
        ("false", False),
        ("0", False),
        ("no", False),
        ("", False),
        ("  ", False),
    ],
)
def test_values_parse_like_from_env(value, expected):
    assert resolve_is_mock(flag=False, env={"KIWOOM_IS_MOCK": value}) is expected
    if value.strip():
        creds = resolve_credentials(
            environ={"KIWOOM_APP_KEY": "k", "KIWOOM_APP_SECRET": "s", "KIWOOM_IS_MOCK": value}
        )
        assert creds.is_mock is expected


def test_unset_means_live_as_before():
    assert resolve_is_mock(flag=False, env={}) is False


@pytest.mark.parametrize("value", ["ture", "mock", "2", "t rue"])
def test_unknown_value_is_rejected_not_treated_as_live(value):
    with pytest.raises(ValueError, match="KIWOOM_IS_MOCK"):
        resolve_is_mock(flag=False, env={"KIWOOM_IS_MOCK": value})


def test_mock_flag_wins_over_env():
    assert resolve_is_mock(flag=True, env={"KIWOOM_IS_MOCK": "false"}) is True


def test_server_refuses_to_start_on_unknown_value(monkeypatch, capsys, captured_run):
    monkeypatch.setenv("KIWOOM_IS_MOCK", "ture")
    with pytest.raises(SystemExit) as exc:
        cli.main([])
    assert exc.value.code == 1
    assert "KIWOOM_IS_MOCK" in capsys.readouterr().err
    assert captured_run == []  # 서버를 띄우지 않았다 — 실전으로 떨어지지 않음


@pytest.mark.parametrize("value", ["1", "yes"])
def test_server_starts_in_mock_for_truthy_values(monkeypatch, captured_run, value):
    monkeypatch.setenv("KIWOOM_IS_MOCK", value)
    cli.main([])
    assert captured_run[0]["is_mock"] is True
