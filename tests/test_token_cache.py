"""Tests for the opt-in on-disk token cache (``token_cache=``).

A token issued by one process is reused by the next one that points at the same
file, so short-lived scripts and the ``kiwoom`` CLI do not ask Kiwoom for a new
token on every run. All HTTP is mocked.
"""

from __future__ import annotations

import json
import os
import sys
import time

import pytest

from kiwoom_client import AsyncKiwoomAPI, KiwoomAPI
from kiwoom_client.auth import AsyncKiwoomAuth, KiwoomAuth

BASE = "https://mockapi.kiwoom.com"
TOKEN_URL = f"{BASE}/oauth2/token"
REVOKE_URL = f"{BASE}/oauth2/revoke"


def _token_reply(token: str, seconds: float = 86400) -> dict[str, object]:
    return {"token": token, "token_type": "Bearer", "expires_in": seconds, "return_code": 0}


def _token_requests(httpx_mock) -> int:
    return sum(1 for r in httpx_mock.get_requests() if r.url.path == "/oauth2/token")


class TestSyncTokenCache:
    def test_second_process_reuses_cached_token(self, httpx_mock, tmp_path):
        cache = tmp_path / "token.json"
        httpx_mock.add_response(url=TOKEN_URL, json=_token_reply("first"))

        with KiwoomAuth("key", "secret", BASE, token_cache=cache) as auth:
            assert auth.get_valid_token() == "first"
        # A new object (a new process) with the same file does not reissue.
        with KiwoomAuth("key", "secret", BASE, token_cache=cache) as auth:
            assert auth.get_valid_token() == "first"

        assert _token_requests(httpx_mock) == 1

    def test_file_holds_no_secret_and_is_private(self, httpx_mock, tmp_path):
        cache = tmp_path / "token.json"
        httpx_mock.add_response(url=TOKEN_URL, json=_token_reply("tok"))
        with KiwoomAuth("my-app-key", "my-secret", BASE, token_cache=cache) as auth:
            auth.get_valid_token()

        text = cache.read_text(encoding="utf-8")
        assert "my-app-key" not in text
        assert "my-secret" not in text
        assert "tok" in text
        if sys.platform != "win32":
            assert (cache.stat().st_mode & 0o777) == 0o600

    def test_expiring_cached_token_is_reissued(self, httpx_mock, tmp_path):
        cache = tmp_path / "token.json"
        httpx_mock.add_response(url=TOKEN_URL, json=_token_reply("old", seconds=30))
        httpx_mock.add_response(url=TOKEN_URL, json=_token_reply("new"))

        with KiwoomAuth("key", "secret", BASE, token_cache=cache) as auth:
            assert auth.get_valid_token() == "old"
        # 30 s left is inside the default 60 s margin: the cached one is not used.
        with KiwoomAuth("key", "secret", BASE, token_cache=cache) as auth:
            assert auth.get_valid_token() == "new"
        with KiwoomAuth("key", "secret", BASE, token_cache=cache) as auth:
            assert auth.get_valid_token() == "new"

        assert _token_requests(httpx_mock) == 2

    def test_entries_are_per_app_key_and_server(self, httpx_mock, tmp_path):
        cache = tmp_path / "token.json"
        httpx_mock.add_response(url=TOKEN_URL, json=_token_reply("for-a"))
        httpx_mock.add_response(url=TOKEN_URL, json=_token_reply("for-b"))

        with KiwoomAuth("key-a", "secret", BASE, token_cache=cache) as auth:
            assert auth.get_valid_token() == "for-a"
        with KiwoomAuth("key-b", "secret", BASE, token_cache=cache) as auth:
            assert auth.get_valid_token() == "for-b"
        with KiwoomAuth("key-a", "secret", BASE, token_cache=cache) as auth:
            assert auth.get_valid_token() == "for-a"

        assert _token_requests(httpx_mock) == 2

    def test_refresh_replaces_cached_token(self, httpx_mock, tmp_path):
        cache = tmp_path / "token.json"
        httpx_mock.add_response(url=TOKEN_URL, json=_token_reply("one"))
        httpx_mock.add_response(url=TOKEN_URL, json=_token_reply("two"))

        with KiwoomAuth("key", "secret", BASE, token_cache=cache) as auth:
            auth.get_valid_token()
            assert auth.refresh_token() == "two"
        with KiwoomAuth("key", "secret", BASE, token_cache=cache) as auth:
            assert auth.get_valid_token() == "two"

    def test_revoke_drops_cached_token(self, httpx_mock, tmp_path):
        cache = tmp_path / "token.json"
        httpx_mock.add_response(url=TOKEN_URL, json=_token_reply("gone"))
        httpx_mock.add_response(url=REVOKE_URL, json={"return_code": 0})
        httpx_mock.add_response(url=TOKEN_URL, json=_token_reply("fresh"))

        with KiwoomAuth("key", "secret", BASE, token_cache=cache) as auth:
            auth.revoke_token(auth.get_valid_token())
        with KiwoomAuth("key", "secret", BASE, token_cache=cache) as auth:
            assert auth.get_valid_token() == "fresh"

    def test_unknown_expiry_is_not_persisted(self, httpx_mock, tmp_path):
        cache = tmp_path / "token.json"
        httpx_mock.add_response(url=TOKEN_URL, json={"token": "no-expiry", "return_code": 0})
        httpx_mock.add_response(url=TOKEN_URL, json=_token_reply("next"))

        with KiwoomAuth("key", "secret", BASE, token_cache=cache) as auth:
            assert auth.get_valid_token() == "no-expiry"
        # Without an expiry we cannot tell later whether it is still good.
        with KiwoomAuth("key", "secret", BASE, token_cache=cache) as auth:
            assert auth.get_valid_token() == "next"

    @pytest.mark.parametrize(
        "garbage", ["", "{not json", "[]", '{"x": 1}', '{"v": 1, "tokens": []}']
    )
    def test_corrupt_file_is_ignored(self, httpx_mock, tmp_path, garbage):
        cache = tmp_path / "token.json"
        cache.write_text(garbage, encoding="utf-8")
        httpx_mock.add_response(url=TOKEN_URL, json=_token_reply("ok"))

        with KiwoomAuth("key", "secret", BASE, token_cache=cache) as auth:
            assert auth.get_valid_token() == "ok"
        assert json.loads(cache.read_text(encoding="utf-8"))["v"] == 1

    def test_unwritable_location_does_not_break_requests(self, httpx_mock, tmp_path):
        blocker = tmp_path / "a-file"
        blocker.write_text("x", encoding="utf-8")
        httpx_mock.add_response(url=TOKEN_URL, json=_token_reply("still-works"))

        # The parent "directory" is a regular file, so saving must fail quietly.
        with KiwoomAuth("key", "secret", BASE, token_cache=blocker / "token.json") as auth:
            assert auth.get_valid_token() == "still-works"

    def test_creates_parent_directory(self, httpx_mock, tmp_path):
        cache = tmp_path / "nested" / "dir" / "token.json"
        httpx_mock.add_response(url=TOKEN_URL, json=_token_reply("tok"))
        with KiwoomAuth("key", "secret", BASE, token_cache=cache) as auth:
            auth.get_valid_token()
        assert cache.exists()

    def test_without_token_cache_nothing_is_written(self, httpx_mock, tmp_path, monkeypatch):
        monkeypatch.chdir(tmp_path)
        httpx_mock.add_response(url=TOKEN_URL, json=_token_reply("tok"))
        with KiwoomAuth("key", "secret", BASE) as auth:
            auth.get_valid_token()
        assert os.listdir(tmp_path) == []

    def test_expired_entries_are_pruned(self, httpx_mock, tmp_path):
        cache = tmp_path / "token.json"
        stale = {"v": 1, "tokens": {"deadbeef": {"token": "t", "expires_at": time.time() - 10}}}
        cache.write_text(json.dumps(stale), encoding="utf-8")
        httpx_mock.add_response(url=TOKEN_URL, json=_token_reply("tok"))

        with KiwoomAuth("key", "secret", BASE, token_cache=cache) as auth:
            auth.get_valid_token()
        assert "deadbeef" not in json.loads(cache.read_text(encoding="utf-8"))["tokens"]


class TestFacade:
    def test_kiwoom_api_token_cache(self, httpx_mock, tmp_path):
        cache = tmp_path / "token.json"
        httpx_mock.add_response(url=TOKEN_URL, json=_token_reply("shared"))
        httpx_mock.add_response(
            url=f"{BASE}/api/dostk/stkinfo",
            json={"return_code": 0, "stk_cd": "005930"},
            is_reusable=True,
        )
        for _ in range(2):
            with KiwoomAPI("key", "secret", is_mock=True, token_cache=cache) as api:
                api.stock_info.basic_stock_info(stk_cd="005930")
        assert _token_requests(httpx_mock) == 1

    def test_from_env_reads_kiwoom_token_cache(self, httpx_mock, tmp_path, monkeypatch):
        cache = tmp_path / "token.json"
        monkeypatch.setenv("KIWOOM_APP_KEY", "key")
        monkeypatch.setenv("KIWOOM_APP_SECRET", "secret")
        monkeypatch.setenv("KIWOOM_IS_MOCK", "true")
        monkeypatch.setenv("KIWOOM_TOKEN_CACHE", str(cache))
        httpx_mock.add_response(url=TOKEN_URL, json=_token_reply("env"))

        with KiwoomAPI.from_env() as api:
            api.login()
        assert cache.exists()

    def test_from_env_explicit_argument_wins(self, httpx_mock, tmp_path, monkeypatch):
        monkeypatch.setenv("KIWOOM_APP_KEY", "key")
        monkeypatch.setenv("KIWOOM_APP_SECRET", "secret")
        monkeypatch.setenv("KIWOOM_IS_MOCK", "true")
        monkeypatch.setenv("KIWOOM_TOKEN_CACHE", str(tmp_path / "from-env.json"))
        httpx_mock.add_response(url=TOKEN_URL, json=_token_reply("arg"))

        with KiwoomAPI.from_env(token_cache=tmp_path / "from-arg.json") as api:
            api.login()
        assert (tmp_path / "from-arg.json").exists()
        assert not (tmp_path / "from-env.json").exists()


class TestAsyncTokenCache:
    async def test_async_reuses_and_shares_with_sync(self, httpx_mock, tmp_path):
        cache = tmp_path / "token.json"
        httpx_mock.add_response(url=TOKEN_URL, json=_token_reply("async-tok"))

        async with AsyncKiwoomAuth("key", "secret", BASE, token_cache=cache) as auth:
            assert await auth.get_valid_token() == "async-tok"
        async with AsyncKiwoomAuth("key", "secret", BASE, token_cache=cache) as auth:
            assert await auth.get_valid_token() == "async-tok"
        # The sync client reads the same file format.
        with KiwoomAuth("key", "secret", BASE, token_cache=cache) as auth:
            assert auth.get_valid_token() == "async-tok"
        assert _token_requests(httpx_mock) == 1

    async def test_async_facade(self, httpx_mock, tmp_path):
        cache = tmp_path / "token.json"
        httpx_mock.add_response(url=TOKEN_URL, json=_token_reply("a"))
        httpx_mock.add_response(
            url=f"{BASE}/api/dostk/stkinfo",
            json={"return_code": 0, "stk_cd": "005930"},
            is_reusable=True,
        )
        for _ in range(2):
            async with AsyncKiwoomAPI("key", "secret", is_mock=True, token_cache=cache) as api:
                await api.stock_info.basic_stock_info(stk_cd="005930")
        assert _token_requests(httpx_mock) == 1
