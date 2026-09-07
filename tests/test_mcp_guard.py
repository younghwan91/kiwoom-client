"""Tests for the live-order opt-in guard."""

from __future__ import annotations

from kiwoom_client.mcp.guard import ENV_VAR, live_orders_allowed


class TestLiveOrdersAllowed:
    def test_mock_is_always_allowed_even_without_env(self):
        assert live_orders_allowed(is_mock=True, env={}) is True

    def test_live_without_env_is_blocked(self):
        assert live_orders_allowed(is_mock=False, env={}) is False

    def test_live_with_env_true_is_allowed(self):
        assert live_orders_allowed(is_mock=False, env={ENV_VAR: "true"}) is True

    def test_env_value_is_case_insensitive(self):
        assert live_orders_allowed(is_mock=False, env={ENV_VAR: "TRUE"}) is True

    def test_live_with_env_false_is_blocked(self):
        assert live_orders_allowed(is_mock=False, env={ENV_VAR: "false"}) is False

    def test_live_with_unrelated_env_value_is_blocked(self):
        assert live_orders_allowed(is_mock=False, env={ENV_VAR: "1"}) is False

    def test_env_defaults_to_os_environ(self, monkeypatch):
        monkeypatch.delenv(ENV_VAR, raising=False)
        assert live_orders_allowed(is_mock=False) is False
        monkeypatch.setenv(ENV_VAR, "true")
        assert live_orders_allowed(is_mock=False) is True
