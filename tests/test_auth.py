"""Tests for OAuth authentication."""

import pytest

from kiwoom_rest_api.auth import KiwoomAuth


class TestKiwoomAuth:
    def test_issue_token(self, httpx_mock):
        httpx_mock.add_response(
            url="https://mockapi.kiwoom.com/oauth2/token",
            json={"token": "abc123", "token_type": "Bearer", "expires_in": 86400},
        )
        auth = KiwoomAuth("key", "secret", "https://mockapi.kiwoom.com")
        result = auth.issue_token()
        assert result["token"] == "abc123"
        assert result["token_type"] == "Bearer"
        auth.close()

    def test_revoke_token(self, httpx_mock):
        httpx_mock.add_response(
            url="https://mockapi.kiwoom.com/oauth2/revoke",
            json={"return_code": 0, "return_msg": "OK"},
        )
        auth = KiwoomAuth("key", "secret", "https://mockapi.kiwoom.com")
        result = auth.revoke_token("abc123")
        assert result["return_code"] == 0
        auth.close()
