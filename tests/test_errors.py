"""Tests for the exception hierarchy: narrower types, unchanged behaviour."""

from __future__ import annotations

import httpx
import pytest

import kiwoom_client
from kiwoom_client import errors
from kiwoom_client.auth import KiwoomAuth, KiwoomAuthError
from kiwoom_client.base import AsyncBaseClient, BaseClient, KiwoomAPIError
from kiwoom_client.errors import (
    KiwoomError,
    KiwoomRateLimitError,
    KiwoomRequestError,
    KiwoomServerMismatchError,
    KiwoomStockNotFoundError,
    KiwoomTokenError,
    KiwoomUnsupportedError,
    KiwoomWebSocketError,
    api_error_class,
    parse_error_code,
)

URL = "https://mockapi.kiwoom.com/api/dostk/stkinfo"


def _client(**kwargs) -> BaseClient:
    client = BaseClient("k", "s", is_mock=True, rate_limit=None, retry_backoff=0, **kwargs)
    client.access_token = "t"
    return client


class TestHierarchy:
    def test_everything_is_a_kiwoom_error(self):
        for cls in (KiwoomAPIError, KiwoomAuthError, KiwoomWebSocketError):
            assert issubclass(cls, KiwoomError)
            assert issubclass(cls, Exception)

    @pytest.mark.parametrize(
        "cls",
        [KiwoomTokenError, KiwoomServerMismatchError, KiwoomRateLimitError,
         KiwoomRequestError, KiwoomStockNotFoundError, KiwoomUnsupportedError],
    )
    def test_subclasses_are_api_errors(self, cls):
        assert issubclass(cls, KiwoomAPIError)

    def test_mismatch_is_a_token_error(self):
        assert issubclass(KiwoomServerMismatchError, KiwoomTokenError)

    def test_not_found_is_a_request_error(self):
        assert issubclass(KiwoomStockNotFoundError, KiwoomRequestError)

    def test_same_objects_everywhere(self):
        assert errors.KiwoomAPIError is kiwoom_client.KiwoomAPIError
        assert errors.KiwoomAuthError is kiwoom_client.KiwoomAuthError
        assert kiwoom_client.base.KiwoomAPIError.__module__ == "kiwoom_client.base"
        for name in errors.__all__:
            if name[0].isupper():
                assert getattr(kiwoom_client, name) is getattr(errors, name)


class TestParseErrorCode:
    @pytest.mark.parametrize(
        ("message", "expected"),
        [
            ("인증에 실패했습니다[8005:Token이 유효하지 않습니다]", 8005),
            ("[ 1902 : 종목 정보가 없습니다]", 1902),
            ("허용된 요청 개수를 초과하였습니다", None),
            ("[2000] something", None),
            (None, None),
            (3, None),
        ],
    )
    def test_parse(self, message, expected):
        assert parse_error_code(message) == expected


class TestClassification:
    @pytest.mark.parametrize(
        ("return_code", "message", "cls"),
        [
            (3, "인증에 실패했습니다[8005:Token이 유효하지 않습니다]", KiwoomTokenError),
            (3, "인증에 실패했습니다", KiwoomTokenError),
            (3, "[8031:투자구분(실전/모의)이 달라서 Token를 사용할수가 없습니다]",
             KiwoomServerMismatchError),
            (1, "[8030:투자구분(실전/모의)이 달라서 Appkey를 사용할수가 없습니다]",
             KiwoomServerMismatchError),
            (5, "허용된 요청 개수를 초과하였습니다", KiwoomRateLimitError),
            (1, "[1700:허용된 API 요청 개수를 초과하였습니다]", KiwoomRateLimitError),
            (1, "[1511:필수 입력 값에 값이 존재하지 않습니다]", KiwoomRequestError),
            (1, "[1902:종목 정보가 없습니다]", KiwoomStockNotFoundError),
            (1, "[8104:모의투자에서 지원하지 않는 API 입니다.]", KiwoomUnsupportedError),
            (1, "주문가능금액을 확인하세요", KiwoomAPIError),
            (2, "[1999:예기치 못한 에러]", KiwoomAPIError),
            ("3", "string return_code", KiwoomAPIError),
        ],
    )
    def test_api_error_class(self, return_code, message, cls):
        assert api_error_class(return_code, message) is cls


class TestRaisedFromRequest:
    def test_attributes_and_str_unchanged(self, httpx_mock):
        payload = {"return_code": 1, "return_msg": "[1902:종목 정보가 없습니다]"}
        httpx_mock.add_response(url=URL, json=payload)
        with _client() as client, pytest.raises(KiwoomAPIError) as info:
            client.request("/api/dostk/stkinfo", "ka10001", {"stk_cd": "999999"})
        exc = info.value
        assert type(exc) is KiwoomStockNotFoundError
        assert exc.code == 1
        assert exc.message == "[1902:종목 정보가 없습니다]"
        assert exc.error_code == 1902
        assert exc.response["return_msg"] == payload["return_msg"]
        assert str(exc) == "[1] [1902:종목 정보가 없습니다]"

    def test_unknown_stays_plain(self, httpx_mock):
        httpx_mock.add_response(url=URL, json={"return_code": 20, "return_msg": "거부"})
        with _client() as client, pytest.raises(KiwoomAPIError) as info:
            client.request("/api/dostk/stkinfo", "ka10001")
        assert type(info.value) is KiwoomAPIError
        assert info.value.error_code is None

    def test_token_error_without_provider_is_not_retried(self, httpx_mock):
        httpx_mock.add_response(
            url=URL, json={"return_code": 3, "return_msg": "인증에 실패했습니다[8005:Token]"}
        )
        with _client() as client, pytest.raises(KiwoomTokenError):
            client.request("/api/dostk/stkinfo", "ka10001")
        assert len(httpx_mock.get_requests()) == 1

    def test_rate_limit_after_retries(self, httpx_mock):
        for _ in range(3):
            httpx_mock.add_response(
                url=URL, json={"return_code": 5, "return_msg": "허용된 요청 개수를 초과"}
            )
        with _client(max_retries=2) as client, pytest.raises(KiwoomRateLimitError):
            client.request("/api/dostk/stkinfo", "ka10001")
        assert len(httpx_mock.get_requests()) == 3  # retry behaviour unchanged

    def test_http_429_still_raises_httpx(self, httpx_mock):
        httpx_mock.add_response(url=URL, status_code=429)
        with _client(max_retries=0) as client, pytest.raises(httpx.HTTPStatusError):
            client.request("/api/dostk/stkinfo", "ka10001")

    async def test_async_raises_the_same_subclass(self, httpx_mock):
        httpx_mock.add_response(
            url=URL, json={"return_code": 1, "return_msg": "[8104:모의투자 미지원]"}
        )
        async with AsyncBaseClient("k", "s", is_mock=True, rate_limit=None) as client:
            client.access_token = "t"
            with pytest.raises(KiwoomUnsupportedError):
                await client.request("/api/dostk/stkinfo", "ka10001")


def test_auth_error_is_kiwoom_error(httpx_mock):
    httpx_mock.add_response(
        url="https://mockapi.kiwoom.com/oauth2/token", json={"return_code": 1, "return_msg": "x"}
    )
    with KiwoomAuth("k", "s", "https://mockapi.kiwoom.com") as auth:
        with pytest.raises(KiwoomError):
            auth.issue_token()
