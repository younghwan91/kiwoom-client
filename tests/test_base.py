"""Tests for base client, auth, and pagination."""

from unittest.mock import MagicMock, patch

import httpx
import pytest

from kiwoom_rest_api.base import BaseClient, KiwoomAPIError


class TestBaseClient:
    def test_init_default_prod(self):
        client = BaseClient("key", "secret")
        assert client.base_url == "https://api.kiwoom.com"
        client.close()

    def test_init_mock(self):
        client = BaseClient("key", "secret", is_mock=True)
        assert client.base_url == "https://mockapi.kiwoom.com"
        client.close()

    def test_init_custom_url(self):
        client = BaseClient("key", "secret", base_url="https://custom.api.com")
        assert client.base_url == "https://custom.api.com"
        client.close()

    def test_access_token_property(self):
        client = BaseClient("key", "secret")
        assert client.access_token is None
        client.access_token = "test_token"
        assert client.access_token == "test_token"
        client.close()

    def test_build_headers(self):
        client = BaseClient("key", "secret")
        client.access_token = "my_token"
        headers = client._build_headers("ka10001", "N", "")
        assert headers["api-id"] == "ka10001"
        assert headers["cont-yn"] == "N"
        assert headers["authorization"] == "Bearer my_token"
        assert headers["Content-Type"] == "application/json;charset=UTF-8"
        client.close()

    def test_build_headers_no_token(self):
        client = BaseClient("key", "secret")
        headers = client._build_headers("ka10001")
        assert "authorization" not in headers
        client.close()

    def test_context_manager(self):
        with BaseClient("key", "secret") as client:
            assert client.base_url == "https://api.kiwoom.com"

    def test_request_success(self, httpx_mock):
        httpx_mock.add_response(
            url="https://mockapi.kiwoom.com/api/dostk/stkinfo",
            json={"return_code": 0, "return_msg": "OK", "stk_nm": "삼성전자"},
        )
        with BaseClient("key", "secret", is_mock=True) as client:
            client.access_token = "token"
            result = client.request("/api/dostk/stkinfo", "ka10001", {"stk_cd": "005930"})
            assert result["stk_nm"] == "삼성전자"
            assert result["return_code"] == 0

    def test_request_api_error(self, httpx_mock):
        httpx_mock.add_response(
            url="https://mockapi.kiwoom.com/api/dostk/stkinfo",
            json={"return_code": -100, "return_msg": "Invalid token"},
        )
        with BaseClient("key", "secret", is_mock=True) as client:
            client.access_token = "bad_token"
            with pytest.raises(KiwoomAPIError) as exc_info:
                client.request("/api/dostk/stkinfo", "ka10001", {"stk_cd": "005930"})
            assert exc_info.value.code == -100
            assert "Invalid token" in str(exc_info.value)

    def test_request_all_pagination(self, httpx_mock):
        # First page
        httpx_mock.add_response(
            url="https://mockapi.kiwoom.com/api/dostk/acnt",
            json={
                "return_code": 0,
                "items": [{"name": "A"}, {"name": "B"}],
                "cont_yn": "Y",
                "next_key": "page2",
            },
        )
        # Second page
        httpx_mock.add_response(
            url="https://mockapi.kiwoom.com/api/dostk/acnt",
            json={
                "return_code": 0,
                "items": [{"name": "C"}],
                "cont_yn": "N",
                "next_key": "",
            },
        )
        with BaseClient("key", "secret", is_mock=True) as client:
            client.access_token = "token"
            result = client.request_all("/api/dostk/acnt", "ka10076", data_key="items")
            assert len(result) == 3
            assert result[0]["name"] == "A"
            assert result[2]["name"] == "C"
