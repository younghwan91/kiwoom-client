"""Tests for ``kiwoom-client-mcp doctor`` — no network unless --check-auth (mocked here)."""

from __future__ import annotations

import subprocess
import sys

import pytest

from kiwoom_client.mcp import cli, doctor
from kiwoom_client.mcp.doctor import ENV_VARS, Overrides, diagnose

MOCK_TOKEN_URL = "https://mockapi.kiwoom.com/oauth2/token"
SECRET = "SECRET-VALUE-do-not-print"


@pytest.fixture
def clean_env(monkeypatch):
    for name in ENV_VARS:
        monkeypatch.delenv(name, raising=False)


def _run(capsys, argv) -> tuple[int, str]:
    with pytest.raises(SystemExit) as exc:
        cli.main(argv)
    return int(exc.value.code or 0), capsys.readouterr().out


class TestOffline:
    def test_without_keys_reports_and_fails(self, capsys, clean_env, httpx_mock):
        code, out = _run(capsys, ["doctor"])
        assert code == 1
        assert "KIWOOM_APP_KEY: 없음" in out
        assert "tools/list: 도구" in out
        assert "네트워크 호출 없음" in out
        assert httpx_mock.get_requests() == []

    def test_never_prints_values(self, capsys, clean_env, monkeypatch, httpx_mock):
        monkeypatch.setenv("KIWOOM_APP_KEY", SECRET)
        monkeypatch.setenv("KIWOOM_APP_SECRET", SECRET + "-2")
        monkeypatch.setenv("KIWOOM_IS_MOCK", "true")
        code, out = _run(capsys, ["doctor"])
        assert code == 0
        assert SECRET not in out
        assert "KIWOOM_APP_KEY: 설정됨" in out
        assert "모의투자" in out
        assert httpx_mock.get_requests() == []

    def test_tool_count_matches_the_server_listing(self, capsys, clean_env, monkeypatch):
        monkeypatch.setenv("KIWOOM_APP_KEY", "k")
        monkeypatch.setenv("KIWOOM_APP_SECRET", "s")
        smart = diagnose(env={"KIWOOM_APP_KEY": "k", "KIWOOM_APP_SECRET": "s"})
        full = diagnose(
            env={"KIWOOM_APP_KEY": "k", "KIWOOM_APP_SECRET": "s"}, flags=Overrides(mode="full")
        )

        def count(report) -> int:
            (line,) = [t for _lvl, t in report.lines if t.startswith("tools/list")]
            return int(line.split("도구 ")[1].split("개")[0])

        assert count(smart) < 20 < count(full)

    @pytest.mark.parametrize(
        ("env", "needle"),
        [
            ({"KIWOOM_IS_MOCK": "ture"}, "KIWOOM_IS_MOCK"),
            ({"KIWOOM_MCP_MODE": "everything"}, "KIWOOM_MCP_MODE"),
            ({"KIWOOM_MCP_TOOLSETS": "nope"}, "toolset"),
            ({"KIWOOM_MCP_MAX_ROWS": "-1"}, "KIWOOM_MCP_MAX_ROWS"),
        ],
    )
    def test_bad_values_are_errors(self, env, needle):
        report = diagnose(env={"KIWOOM_APP_KEY": "k", "KIWOOM_APP_SECRET": "s", **env})
        assert report.failed
        assert any(level == "error" and needle in text for level, text in report.lines)

    def test_guard_states(self):
        keys = {"KIWOOM_APP_KEY": "k", "KIWOOM_APP_SECRET": "s"}
        live = diagnose(env=keys)
        assert any("등록 안 됨" in text for _lvl, text in live.lines)
        opted = diagnose(env={**keys, "KIWOOM_MCP_ALLOW_LIVE_ORDERS": "true"})
        assert any(lvl == "warn" and "실제 주문" in text for lvl, text in opted.lines)
        mock = diagnose(env={**keys, "KIWOOM_IS_MOCK": "true"})
        assert any("모의투자 — 실제 체결 없음" in text for _lvl, text in mock.lines)

    def test_read_only_wins_over_mock_and_opt_in(self):
        keys = {"KIWOOM_APP_KEY": "k", "KIWOOM_APP_SECRET": "s", "KIWOOM_MCP_READ_ONLY": "true"}
        for extra in ({"KIWOOM_IS_MOCK": "true"}, {"KIWOOM_MCP_ALLOW_LIVE_ORDERS": "true"}):
            report = diagnose(env={**keys, **extra})
            assert any("읽기 전용" in text for _lvl, text in report.lines)
            assert not any("실제 주문" in text for _lvl, text in report.lines)

    def test_bad_read_only_value_is_an_error(self):
        keys = {"KIWOOM_APP_KEY": "k", "KIWOOM_APP_SECRET": "s", "KIWOOM_MCP_READ_ONLY": "maybe"}
        report = diagnose(env=keys)
        assert any(lvl == "error" and "KIWOOM_MCP_READ_ONLY" in t for lvl, t in report.lines)

    def test_server_flags_apply(self, capsys, clean_env, monkeypatch):
        monkeypatch.setenv("KIWOOM_APP_KEY", "k")
        monkeypatch.setenv("KIWOOM_APP_SECRET", "s")
        monkeypatch.setenv("KIWOOM_MCP_TOOLSETS", "chart")
        _code, out = _run(capsys, ["--mock", "--full", "--toolsets", "all", "doctor"])
        assert "모의투자" in out
        assert "모드: full · toolset: 전부" in out

    def test_wrong_mcp_major_is_an_error(self, monkeypatch):
        monkeypatch.setattr(doctor, "_mcp_version", lambda: "1.9.4")
        report = diagnose(env={"KIWOOM_APP_KEY": "k", "KIWOOM_APP_SECRET": "s"})
        assert report.failed
        assert not any(text.startswith("tools/list") for _lvl, text in report.lines)

    def test_works_without_the_mcp_package(self):
        script = (
            "import sys; sys.modules['mcp'] = None; "
            "import importlib.metadata as m; real = m.version; "
            "m.version = lambda n: (_ for _ in ()).throw(m.PackageNotFoundError(n)) "
            "if n == 'mcp' else real(n); "
            "from kiwoom_client.mcp.cli import main; main(['doctor'])"
        )
        env = {"KIWOOM_APP_KEY": "k", "KIWOOM_APP_SECRET": "s", "PATH": ""}
        proc = subprocess.run(
            [sys.executable, "-c", script], capture_output=True, text=True, env=env
        )
        assert proc.returncode == 1, proc.stderr
        assert "mcp 패키지 없음" in proc.stdout


class TestCheckAuth:
    def test_issues_one_token_and_never_revokes(self, capsys, clean_env, monkeypatch, httpx_mock):
        httpx_mock.add_response(
            url=MOCK_TOKEN_URL,
            json={"token": "t", "token_type": "Bearer", "expires_in": 86400, "return_code": 0},
        )
        monkeypatch.setenv("KIWOOM_APP_KEY", "k")
        monkeypatch.setenv("KIWOOM_APP_SECRET", "s")
        code, out = _run(capsys, ["--mock", "doctor", "--check-auth"])
        assert code == 0, out
        assert "토큰 발급 성공" in out
        assert [r.url.path for r in httpx_mock.get_requests()] == ["/oauth2/token"]

    def test_failure_is_an_error(self, capsys, clean_env, monkeypatch, httpx_mock):
        httpx_mock.add_response(
            url=MOCK_TOKEN_URL, status_code=401, json={"return_code": 3, "return_msg": "bad key"}
        )
        monkeypatch.setenv("KIWOOM_APP_KEY", "k")
        monkeypatch.setenv("KIWOOM_APP_SECRET", "s")
        code, out = _run(capsys, ["--mock", "doctor", "--check-auth"])
        assert code == 1
        assert "토큰 발급 실패" in out

    def test_without_keys_makes_no_request(self, capsys, clean_env, httpx_mock):
        code, out = _run(capsys, ["doctor", "--check-auth"])
        assert code == 1
        assert "확인할 수 없습니다" in out
        assert httpx_mock.get_requests() == []
