"""Tests for OAuth authentication."""

import json

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

        # 요청 바디 필드명 검증: 키움 API 는 'secretkey' 를 기대한다 (regression guard)
        body = json.loads(httpx_mock.get_requests()[0].content)
        assert body == {
            "grant_type": "client_credentials",
            "appkey": "key",
            "secretkey": "secret",
        }
        auth.close()

    def test_revoke_token(self, httpx_mock):
        httpx_mock.add_response(
            url="https://mockapi.kiwoom.com/oauth2/revoke",
            json={"return_code": 0, "return_msg": "OK"},
        )
        auth = KiwoomAuth("key", "secret", "https://mockapi.kiwoom.com")
        result = auth.revoke_token("abc123")
        assert result["return_code"] == 0

        body = json.loads(httpx_mock.get_requests()[0].content)
        assert body == {"appkey": "key", "secretkey": "secret", "token": "abc123"}
        auth.close()
