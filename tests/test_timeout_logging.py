"""Tests for the opt-in timeout option and DEBUG request tracing."""

from __future__ import annotations

import logging

import httpx
import pytest

from kiwoom_client import AsyncKiwoomAPI, KiwoomAPI
from kiwoom_client.auth import AsyncKiwoomAuth, KiwoomAuth
from kiwoom_client.base import AsyncBaseClient, BaseClient

KEY = "PSappkey0123456789ABCDEFkeyTAIL"
SECRET = "secretvalue-0123456789-abcdefghij"
TOKEN = "tokenvalue-ZZZZ-0123456789"
ACCOUNT = "8112345611"
BASE = "https://mockapi.kiwoom.com"
URL = f"{BASE}/api/dostk/acnt"


class TestTimeout:
    def test_default_is_30s_everywhere(self):
        with KiwoomAPI(KEY, SECRET, is_mock=True) as api:
            assert api._base_client._client.timeout == httpx.Timeout(30.0)
            assert api._auth._client.timeout == httpx.Timeout(30.0)
        with BaseClient(KEY, SECRET) as client:
            assert client._client.timeout == httpx.Timeout(30.0)
        with KiwoomAuth(KEY, SECRET, BASE) as auth:
            assert auth._client.timeout == httpx.Timeout(30.0)

    def test_facade_passes_timeout_through(self):
        with KiwoomAPI(KEY, SECRET, is_mock=True, timeout=5.0) as api:
            assert api._base_client._client.timeout == httpx.Timeout(5.0)
            assert api._auth._client.timeout == httpx.Timeout(5.0)

    def test_httpx_timeout_object(self):
        custom = httpx.Timeout(10.0, connect=2.0)
        with BaseClient(KEY, SECRET, timeout=custom) as client:
            assert client._client.timeout == custom

    async def test_async(self):
        async with AsyncKiwoomAPI(KEY, SECRET, is_mock=True, timeout=7.0) as api:
            assert api._base_client._client.timeout == httpx.Timeout(7.0)
            assert api._auth._client.timeout == httpx.Timeout(7.0)
        async with AsyncBaseClient(KEY, SECRET) as client:
            assert client._client.timeout == httpx.Timeout(30.0)
        async with AsyncKiwoomAuth(KEY, SECRET, BASE, timeout=3.0) as auth:
            assert auth._client.timeout == httpx.Timeout(3.0)

    def test_timeout_is_keyword_only(self):
        with pytest.raises(TypeError):
            BaseClient(KEY, SECRET, None, False, 1.0, 2, 3, 1.1, None, 5.0)  # type: ignore[misc]

    def test_from_env_forwards_timeout(self, monkeypatch):
        monkeypatch.setenv("KIWOOM_APP_KEY", KEY)
        monkeypatch.setenv("KIWOOM_APP_SECRET", SECRET)
        with KiwoomAPI.from_env(is_mock=True, timeout=4.0) as api:
            assert api._base_client._client.timeout == httpx.Timeout(4.0)


def _client(**kwargs) -> BaseClient:
    client = BaseClient(KEY, SECRET, is_mock=True, rate_limit=None, retry_backoff=0, **kwargs)
    client.access_token = TOKEN
    return client


class TestDebugLogging:
    def test_traces_status_and_return_code_without_secrets(self, httpx_mock, caplog):
        httpx_mock.add_response(url=URL, status_code=429)
        httpx_mock.add_response(url=URL, json={"return_code": 0, "acnt_no": ACCOUNT})
        with caplog.at_level(logging.DEBUG, logger="kiwoom_client"), _client() as client:
            client.request("/api/dostk/acnt", "kt00004", {"acnt_no": ACCOUNT})
        text = caplog.text
        assert "kt00004 /api/dostk/acnt -> HTTP 429 (attempt 1)" in text
        assert "rate-limited (HTTP 429)" in text
        assert "kt00004 /api/dostk/acnt -> HTTP 200 (attempt 2)" in text
        assert "kt00004 return_code=0" in text
        for secret in (TOKEN, SECRET, KEY, ACCOUNT, "Bearer"):
            assert secret not in text

    def test_token_refresh_is_traced(self, httpx_mock, caplog):
        class Provider:
            def get_valid_token(self) -> str:
                return TOKEN

            def refresh_token(self) -> str:
                return TOKEN

        httpx_mock.add_response(url=URL, json={"return_code": 3, "return_msg": "인증 실패"})
        httpx_mock.add_response(url=URL, json={"return_code": 0})
        with caplog.at_level(logging.DEBUG, logger="kiwoom_client"):
            with BaseClient(KEY, SECRET, is_mock=True, rate_limit=None,
                            token_provider=Provider()) as client:
                client.request("/api/dostk/acnt", "kt00004")
        assert "token rejected (return_code 3), reissuing" in caplog.text
        assert TOKEN not in caplog.text

    def test_silent_at_default_level(self, httpx_mock, caplog):
        httpx_mock.add_response(url=URL, json={"return_code": 0})
        with caplog.at_level(logging.WARNING), _client() as client:
            client.request("/api/dostk/acnt", "kt00004")
        assert caplog.text == ""

    async def test_async_traces(self, httpx_mock, caplog):
        httpx_mock.add_response(url=URL, json={"return_code": 5, "return_msg": "초과"})
        httpx_mock.add_response(url=URL, json={"return_code": 0})
        with caplog.at_level(logging.DEBUG, logger="kiwoom_client"):
            async with AsyncBaseClient(KEY, SECRET, is_mock=True, rate_limit=None,
                                       retry_backoff=0) as client:
                client.access_token = TOKEN
                await client.request("/api/dostk/acnt", "kt00004", {"acnt_no": ACCOUNT})
        assert "rate-limited (return_code 5)" in caplog.text
        assert ACCOUNT not in caplog.text and TOKEN not in caplog.text
