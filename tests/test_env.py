"""Tests for KiwoomAPI.from_env() and the small .env reader behind it."""

from __future__ import annotations

import logging

import pytest

from kiwoom_client import AsyncKiwoomAPI, KiwoomAPI
from kiwoom_client._env import parse_bool, read_env_file, resolve_credentials

VARS = ("KIWOOM_APP_KEY", "KIWOOM_APP_SECRET", "KIWOOM_IS_MOCK")


@pytest.fixture(autouse=True)
def _clean_env(monkeypatch):
    for name in VARS:
        monkeypatch.delenv(name, raising=False)


class TestReadEnvFile:
    def test_parses_common_forms(self, tmp_path):
        path = tmp_path / ".env"
        path.write_text(
            "# comment\n"
            "\n"
            "KIWOOM_APP_KEY=plain\n"
            'KIWOOM_APP_SECRET="quoted value"\n'
            "export KIWOOM_IS_MOCK='true'\n"
            "TRAILING=abc # note\n"
            "HASH_IN_QUOTES=\"a # b\"\n"
            "EMPTY=\n"
            "not a pair\n",
            encoding="utf-8",
        )
        assert read_env_file(path) == {
            "KIWOOM_APP_KEY": "plain",
            "KIWOOM_APP_SECRET": "quoted value",
            "KIWOOM_IS_MOCK": "true",
            "TRAILING": "abc",
            "HASH_IN_QUOTES": "a # b",
            "EMPTY": "",
        }

    def test_bom_is_ignored(self, tmp_path):
        path = tmp_path / ".env"
        path.write_bytes("﻿KIWOOM_APP_KEY=k\n".encode())
        assert read_env_file(path) == {"KIWOOM_APP_KEY": "k"}

    def test_missing_file_raises(self, tmp_path):
        with pytest.raises(FileNotFoundError):
            read_env_file(tmp_path / "nope.env")


class TestParseBool:
    @pytest.mark.parametrize("value", ["true", "TRUE", " True ", "1", "yes", "y", "on"])
    def test_true(self, value):
        assert parse_bool(value) is True

    @pytest.mark.parametrize("value", ["false", "False", "0", "no", "n", "off"])
    def test_false(self, value):
        assert parse_bool(value) is False

    @pytest.mark.parametrize("value", ["", "mock", "ture", "2"])
    def test_garbage_raises(self, value):
        with pytest.raises(ValueError, match="KIWOOM_IS_MOCK"):
            parse_bool(value)


class TestResolveCredentials:
    def test_from_environ(self):
        creds = resolve_credentials(
            environ={"KIWOOM_APP_KEY": "k", "KIWOOM_APP_SECRET": "s", "KIWOOM_IS_MOCK": "1"}
        )
        assert creds == ("k", "s", True)

    def test_environ_wins_over_file(self, tmp_path):
        path = tmp_path / ".env"
        path.write_text(
            "KIWOOM_APP_KEY=file_key\nKIWOOM_APP_SECRET=file_secret\nKIWOOM_IS_MOCK=false\n",
            encoding="utf-8",
        )
        creds = resolve_credentials(
            path, environ={"KIWOOM_APP_KEY": "env_key", "KIWOOM_IS_MOCK": "true"}
        )
        assert creds == ("env_key", "file_secret", True)

    def test_blank_environ_falls_back_to_file(self, tmp_path):
        path = tmp_path / ".env"
        path.write_text("KIWOOM_APP_KEY=file_key\nKIWOOM_APP_SECRET=s\n", encoding="utf-8")
        creds = resolve_credentials(path, is_mock=True, environ={"KIWOOM_APP_KEY": "  "})
        assert creds.app_key == "file_key"

    def test_explicit_is_mock_wins(self):
        creds = resolve_credentials(
            is_mock=False,
            environ={"KIWOOM_APP_KEY": "k", "KIWOOM_APP_SECRET": "s", "KIWOOM_IS_MOCK": "true"},
        )
        assert creds.is_mock is False

    def test_missing_key_names_both_sources(self, tmp_path):
        path = tmp_path / "creds.env"
        path.write_text("KIWOOM_APP_SECRET=s\n", encoding="utf-8")
        with pytest.raises(ValueError, match=r"KIWOOM_APP_KEY .*creds\.env"):
            resolve_credentials(path, environ={})

    def test_missing_both(self):
        with pytest.raises(ValueError, match="KIWOOM_APP_KEY, KIWOOM_APP_SECRET"):
            resolve_credentials(environ={})

    def test_unset_is_mock_means_live_with_warning(self, caplog):
        with caplog.at_level(logging.WARNING, logger="kiwoom_client"):
            creds = resolve_credentials(
                environ={"KIWOOM_APP_KEY": "k", "KIWOOM_APP_SECRET": "s"}
            )
        assert creds.is_mock is False  # same default as KiwoomAPI() and the MCP server
        assert "실전투자" in caplog.text

    def test_set_is_mock_does_not_warn(self, caplog):
        with caplog.at_level(logging.WARNING, logger="kiwoom_client"):
            resolve_credentials(
                environ={"KIWOOM_APP_KEY": "k", "KIWOOM_APP_SECRET": "s", "KIWOOM_IS_MOCK": "no"}
            )
        assert caplog.text == ""

    def test_invalid_is_mock_raises(self):
        with pytest.raises(ValueError):
            resolve_credentials(
                environ={"KIWOOM_APP_KEY": "k", "KIWOOM_APP_SECRET": "s", "KIWOOM_IS_MOCK": "x"}
            )


class TestFromEnv:
    def test_sync_mock_from_environ(self, monkeypatch):
        monkeypatch.setenv("KIWOOM_APP_KEY", "k")
        monkeypatch.setenv("KIWOOM_APP_SECRET", "s")
        monkeypatch.setenv("KIWOOM_IS_MOCK", "true")
        with KiwoomAPI.from_env() as api:
            assert api._base_client.base_url == "https://mockapi.kiwoom.com"
            assert api._base_client.app_key == "k"
            assert api._auth.app_secret == "s"

    def test_sync_from_file_with_kwargs(self, tmp_path):
        path = tmp_path / ".env"
        path.write_text(
            "KIWOOM_APP_KEY=k\nKIWOOM_APP_SECRET=s\nKIWOOM_IS_MOCK=true\n", encoding="utf-8"
        )
        with KiwoomAPI.from_env(path, rate_limit=None, max_retries=7) as api:
            assert api._base_client._rate_limiter is None
            assert api._base_client._max_retries == 7
            assert api._is_mock is True

    def test_sync_default_is_live(self, monkeypatch):
        monkeypatch.setenv("KIWOOM_APP_KEY", "k")
        monkeypatch.setenv("KIWOOM_APP_SECRET", "s")
        with KiwoomAPI.from_env() as api:
            assert api._base_client.base_url == "https://api.kiwoom.com"

    def test_subclass_is_preserved(self, monkeypatch):
        class MyAPI(KiwoomAPI):
            pass

        monkeypatch.setenv("KIWOOM_APP_KEY", "k")
        monkeypatch.setenv("KIWOOM_APP_SECRET", "s")
        with MyAPI.from_env(is_mock=True) as api:
            assert isinstance(api, MyAPI)

    async def test_async(self, monkeypatch):
        monkeypatch.setenv("KIWOOM_APP_KEY", "k")
        monkeypatch.setenv("KIWOOM_APP_SECRET", "s")
        monkeypatch.setenv("KIWOOM_IS_MOCK", "1")
        async with AsyncKiwoomAPI.from_env() as api:
            assert isinstance(api, AsyncKiwoomAPI)
            assert api._base_client.base_url == "https://mockapi.kiwoom.com"

    def test_missing_credentials_raise(self):
        with pytest.raises(ValueError):
            KiwoomAPI.from_env()
