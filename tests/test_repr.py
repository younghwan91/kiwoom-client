"""Reprs must help debugging without ever leaking the secret or a token."""

from __future__ import annotations

import pytest

from kiwoom_client import AsyncKiwoomAPI, KiwoomAPI
from kiwoom_client._redact import mask_secret, server_label, token_state
from kiwoom_client.auth import AsyncKiwoomAuth, KiwoomAuth
from kiwoom_client.base import AsyncBaseClient, BaseClient
from kiwoom_client.websocket import KiwoomWebSocket

KEY = "PSappkey0123456789ABCDEFkeyTAIL"
SECRET = "secretvalue-0123456789-abcdefghij"
TOKEN = "tokenvalue-ZZZZ-0123456789"
MOCK = "https://mockapi.kiwoom.com"


def assert_clean(text: str) -> None:
    assert SECRET not in text
    assert TOKEN not in text
    assert KEY not in text
    # no meaningful fragment of the secret/token either
    for needle in (SECRET[:8], SECRET[-6:], TOKEN[:8], TOKEN[-6:]):
        assert needle not in text


class TestMaskSecret:
    def test_values(self):
        assert mask_secret(KEY) == "****TAIL"
        assert mask_secret(KEY, 0) == "****"
        assert mask_secret("short") == "****"
        assert mask_secret("") == "''"
        assert mask_secret(None) == "None"

    def test_token_state_and_server(self):
        assert token_state(TOKEN) == "set"
        assert token_state(None) == "none"
        assert server_label(MOCK) == "mock"
        assert server_label("https://api.kiwoom.com") == "live"
        assert server_label("http://localhost:8080") == "custom"


class TestReprs:
    def test_sync_facade(self):
        with KiwoomAPI(KEY, SECRET, is_mock=True) as api:
            api._auth._token = TOKEN
            api._base_client.access_token = TOKEN
            for obj in (api, api._base_client, api._auth):
                text = repr(obj)
                assert_clean(text)
                assert "****TAIL" in text
            assert repr(api) == (
                "KiwoomAPI(server='mock', base_url='https://mockapi.kiwoom.com', "
                "app_key='****TAIL', token='set')"
            )
            assert "access_token='set'" in repr(api._base_client)
            assert "token='set'" in repr(api._auth)

    def test_live_default_shows_live(self):
        with KiwoomAPI(KEY, SECRET) as api:
            assert "server='live'" in repr(api)
            assert "token='none'" in repr(api)

    async def test_async_facade(self):
        async with AsyncKiwoomAPI(KEY, SECRET, is_mock=True) as api:
            api._auth._token = TOKEN
            for obj in (api, api._base_client, api._auth):
                assert_clean(repr(obj))
            assert repr(api).startswith("AsyncKiwoomAPI(server='mock'")

    def test_standalone_clients(self):
        with BaseClient(KEY, SECRET, is_mock=True) as client:
            client.access_token = TOKEN
            assert_clean(repr(client))
            assert_clean(str(client))
        with KiwoomAuth(KEY, SECRET, MOCK) as auth:
            assert_clean(repr(auth))

    async def test_async_standalone(self):
        async with AsyncBaseClient(KEY, SECRET, is_mock=True) as client:
            assert_clean(repr(client))
        async with AsyncKiwoomAuth(KEY, SECRET, MOCK) as auth:
            assert_clean(repr(auth))

    def test_websocket(self):
        ws = KiwoomWebSocket(TOKEN, is_mock=True)
        text = repr(ws)
        assert_clean(text)
        assert "connected=False" in text and "subscriptions=0" in text

    @pytest.mark.parametrize("fmt", [repr, str, lambda o: f"{o!r}", lambda o: f"{o}"])
    def test_every_formatting_path(self, fmt):
        with KiwoomAPI(KEY, SECRET, is_mock=True) as api:
            api._auth._token = TOKEN
            assert_clean(fmt(api))
