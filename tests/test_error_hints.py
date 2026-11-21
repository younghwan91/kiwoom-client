"""Tests for the advice ("힌트") attached to API and auth errors.

Hints only add text: the exception type, ``code``/``message``/``response`` and
the first line of ``str(exc)`` are what they were before.
"""

from __future__ import annotations

import pytest

from kiwoom_client._errors import describe_server, error_hint
from kiwoom_client.auth import AsyncKiwoomAuth, KiwoomAuth, KiwoomAuthError
from kiwoom_client.base import BaseClient, KiwoomAPIError
from kiwoom_client.errors import KiwoomServerMismatchError, KiwoomTokenError

PROD = "https://api.kiwoom.com"
MOCK = "https://mockapi.kiwoom.com"
MISMATCH_TOKEN = (
    "인증에 실패했습니다[8031:투자구분(실전/모의)이 달라서 Token를 사용할수가 없습니다]"
)
BAD_KEY = "[8002:App Key와 Secret Key 검증에 실패했습니다]"
MISMATCH_KEY = "[8030:투자구분(실전/모의)이 달라서 Appkey를 사용할수가 없습니다]"


class TestErrorHint:
    def test_describe_server(self):
        assert "모의투자" in describe_server(MOCK)
        assert "실전투자" in describe_server(PROD)
        assert describe_server("https://proxy.local") == "https://proxy.local"
        assert describe_server(None) is None

    def test_mismatch_points_to_the_other_server(self):
        assert "is_mock=True" in error_hint(8030, base_url=PROD)
        assert "is_mock=False" in error_hint(8031, base_url=MOCK)
        assert "is_mock" in error_hint(8030)

    @pytest.mark.parametrize(
        ("error_code", "return_code", "needle"),
        [
            (8001, None, "앱키"),
            (8002, None, "앱키"),
            (8010, None, "IP"),
            (8104, None, "모의투자"),
            (1700, None, "rate_limit"),
            (None, 5, "rate_limit"),
            (1902, None, "_NX"),
            (8005, None, "토큰"),
            (None, 3, "토큰"),
        ],
    )
    def test_known_codes(self, error_code, return_code, needle):
        assert needle in error_hint(error_code, return_code)

    @pytest.mark.parametrize(("error_code", "return_code"), [(None, None), (1999, 1), (None, 20)])
    def test_unknown_codes_have_no_hint(self, error_code, return_code):
        assert error_hint(error_code, return_code) is None


def _request(httpx_mock, base_url: str, payload: dict) -> KiwoomAPIError:
    httpx_mock.add_response(url=f"{base_url}/api/dostk/stkinfo", json=payload)
    with BaseClient("k", "s", base_url=base_url, rate_limit=None) as client:
        client.access_token = "t"
        with pytest.raises(KiwoomAPIError) as info:
            client.request("/api/dostk/stkinfo", "ka10001")
    return info.value


class TestApiErrorHints:
    def test_mismatch_on_live_server(self, httpx_mock):
        exc = _request(httpx_mock, PROD, {"return_code": 3, "return_msg": MISMATCH_TOKEN})
        assert type(exc) is KiwoomServerMismatchError
        assert exc.message == MISMATCH_TOKEN  # raw, untouched
        assert str(exc).splitlines()[0] == f"[3] {MISMATCH_TOKEN}"
        assert "is_mock=True" in exc.hint
        assert "힌트" in str(exc) and "실전투자 서버" in str(exc)

    def test_mismatch_on_mock_server(self, httpx_mock):
        exc = _request(httpx_mock, MOCK, {"return_code": 3, "return_msg": MISMATCH_TOKEN})
        assert "is_mock=False" in exc.hint

    def test_token_error_hint(self, httpx_mock):
        exc = _request(httpx_mock, MOCK, {"return_code": 3, "return_msg": "인증에 실패했습니다"})
        assert type(exc) is KiwoomTokenError
        assert exc.hint is not None

    def test_unknown_error_is_byte_for_byte_unchanged(self, httpx_mock):
        exc = _request(httpx_mock, MOCK, {"return_code": 20, "return_msg": "주문가능금액 부족"})
        assert exc.hint is None
        assert str(exc) == "[20] 주문가능금액 부족"
        assert exc.args == ("[20] 주문가능금액 부족",)

    def test_direct_construction_has_no_hint(self):
        exc = KiwoomAPIError(1, "x")
        assert exc.hint is None
        assert str(exc) == "[1] x"


class TestAuthErrorHints:
    def test_construction_is_backwards_compatible(self):
        assert str(KiwoomAuthError("plain")) == "plain"
        assert KiwoomAuthError().args == ()
        assert KiwoomAuthError("a", "b").args == ("a", "b")
        assert KiwoomAuthError("plain").hint is None

    def test_hint_is_appended(self):
        exc = KiwoomAuthError("토큰 발급 실패: x", hint="do y")
        assert str(exc) == "토큰 발급 실패: x\n  힌트: do y"
        assert exc.hint == "do y"

    def test_token_response_with_mismatch_on_live(self, httpx_mock):
        httpx_mock.add_response(
            url=f"{PROD}/oauth2/token", json={"return_code": 1, "return_msg": MISMATCH_KEY}
        )
        with KiwoomAuth("k", "s", PROD) as auth, pytest.raises(KiwoomAuthError) as info:
            auth.issue_token()
        exc = info.value
        assert str(exc).splitlines()[0] == f"토큰 발급 실패: {MISMATCH_KEY}"
        assert exc.error_code == 8030
        assert "is_mock=True" in exc.hint

    def test_token_response_without_code_has_no_hint(self, httpx_mock):
        httpx_mock.add_response(url=f"{MOCK}/oauth2/token", json={"return_msg": "알 수 없음"})
        with KiwoomAuth("k", "s", MOCK) as auth, pytest.raises(KiwoomAuthError) as info:
            auth.issue_token()
        assert str(info.value) == "토큰 발급 실패: 알 수 없음"

    def test_http_error_body_is_surfaced(self, httpx_mock):
        httpx_mock.add_response(
            url=f"{MOCK}/oauth2/token",
            status_code=400,
            json={"return_code": 1, "return_msg": BAD_KEY},
        )
        with KiwoomAuth("k", "s", MOCK) as auth, pytest.raises(KiwoomAuthError) as info:
            auth.issue_token()
        exc = info.value
        assert str(exc).startswith("토큰 발급 요청 실패: ")
        assert "8002" in str(exc)
        assert exc.error_code == 8002
        assert "모의투자 서버" in exc.hint

    def test_http_error_without_json_is_unchanged(self, httpx_mock):
        httpx_mock.add_response(url=f"{MOCK}/oauth2/token", status_code=500, text="oops")
        with KiwoomAuth("k", "s", MOCK) as auth, pytest.raises(KiwoomAuthError) as info:
            auth.issue_token()
        assert str(info.value).startswith("토큰 발급 요청 실패: ")
        assert info.value.hint is None
        assert "힌트" not in str(info.value)

    async def test_async_token_response(self, httpx_mock):
        httpx_mock.add_response(
            url=f"{MOCK}/oauth2/token", json={"return_code": 1, "return_msg": MISMATCH_KEY}
        )
        async with AsyncKiwoomAuth("k", "s", MOCK) as auth:
            with pytest.raises(KiwoomAuthError) as info:
                await auth.issue_token()
        assert "is_mock=False" in info.value.hint
