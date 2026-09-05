"""Tests for automatic access-token refresh.

키움 토큰은 만료된다. 장시간 도는 봇이 401 로 죽지 않도록
KiwoomAuth 가 만료를 추적하고 BaseClient 가 401 에서 재발급을 트리거한다.
"""

from __future__ import annotations

import time

import httpx
import pytest

from kiwoom_client.auth import KiwoomAuth, KiwoomAuthError
from kiwoom_client.base import BaseClient, KiwoomAPIError

BASE = "https://mockapi.kiwoom.com"
TOKEN_URL = f"{BASE}/oauth2/token"
API_URL = f"{BASE}/api/dostk/stkinfo"


def _future_dt(seconds: int) -> str:
    """seconds 초 뒤를 키움 형식(yyyyMMddHHmmss)으로."""
    return time.strftime("%Y%m%d%H%M%S", time.localtime(time.time() + seconds))


class TestExpiryParsing:
    def test_expires_dt_is_parsed(self, httpx_mock):
        httpx_mock.add_response(
            url=TOKEN_URL, json={"token": "t1", "expires_dt": _future_dt(3600)}
        )
        with KiwoomAuth("key", "secret", BASE) as auth:
            auth.issue_token()
            assert auth.expires_at is not None
            assert 3500 < auth.expires_at - time.time() < 3700

    def test_expires_in_is_parsed(self, httpx_mock):
        httpx_mock.add_response(
            url=TOKEN_URL, json={"token": "t1", "expires_in": 7200}
        )
        with KiwoomAuth("key", "secret", BASE) as auth:
            auth.issue_token()
            assert auth.expires_at is not None
            assert 7100 < auth.expires_at - time.time() < 7300

    def test_no_expiry_field_leaves_expiry_unknown(self, httpx_mock):
        """만료 정보가 없으면 선제 갱신은 하지 않고 401 경로에 맡긴다."""
        httpx_mock.add_response(url=TOKEN_URL, json={"token": "t1"})
        with KiwoomAuth("key", "secret", BASE) as auth:
            auth.issue_token()
            assert auth.expires_at is None

    def test_malformed_expires_dt_is_ignored(self, httpx_mock):
        httpx_mock.add_response(
            url=TOKEN_URL, json={"token": "t1", "expires_dt": "not-a-date"}
        )
        with KiwoomAuth("key", "secret", BASE) as auth:
            auth.issue_token()
            assert auth.expires_at is None

    def test_access_token_alias_is_accepted(self, httpx_mock):
        httpx_mock.add_response(
            url=TOKEN_URL, json={"access_token": "t1", "expires_in": 100}
        )
        with KiwoomAuth("key", "secret", BASE) as auth:
            assert auth.issue_token()["access_token"] == "t1"
            assert auth.token == "t1"

    def test_missing_token_raises(self, httpx_mock):
        httpx_mock.add_response(url=TOKEN_URL, json={"return_code": 3, "return_msg": "bad key"})
        with KiwoomAuth("key", "secret", BASE) as auth:
            with pytest.raises(KiwoomAuthError) as exc:
                auth.issue_token()
            assert "bad key" in str(exc.value)

    def test_http_error_raises_auth_error(self, httpx_mock):
        httpx_mock.add_response(url=TOKEN_URL, status_code=500, text="boom")
        with KiwoomAuth("key", "secret", BASE) as auth:
            with pytest.raises(KiwoomAuthError):
                auth.issue_token()


class TestGetValidToken:
    def test_issues_on_first_call(self, httpx_mock):
        httpx_mock.add_response(url=TOKEN_URL, json={"token": "t1", "expires_in": 3600})
        with KiwoomAuth("key", "secret", BASE) as auth:
            assert auth.get_valid_token() == "t1"
        assert len(httpx_mock.get_requests()) == 1

    def test_reuses_valid_token(self, httpx_mock):
        httpx_mock.add_response(url=TOKEN_URL, json={"token": "t1", "expires_in": 3600})
        with KiwoomAuth("key", "secret", BASE) as auth:
            assert auth.get_valid_token() == "t1"
            assert auth.get_valid_token() == "t1"
        assert len(httpx_mock.get_requests()) == 1, "유효한 토큰은 재발급하지 않는다"

    def test_reissues_when_near_expiry(self, httpx_mock):
        """만료 여유(expiry_margin) 안으로 들어오면 선제 재발급."""
        httpx_mock.add_response(url=TOKEN_URL, json={"token": "t1", "expires_in": 30})
        httpx_mock.add_response(url=TOKEN_URL, json={"token": "t2", "expires_in": 3600})
        with KiwoomAuth("key", "secret", BASE, expiry_margin=60.0) as auth:
            assert auth.get_valid_token() == "t1"  # 첫 발급
            assert auth.get_valid_token() == "t2"  # 30s < 60s margin → 재발급
        assert len(httpx_mock.get_requests()) == 2

    def test_unknown_expiry_is_not_preemptively_refreshed(self, httpx_mock):
        httpx_mock.add_response(url=TOKEN_URL, json={"token": "t1"})
        with KiwoomAuth("key", "secret", BASE) as auth:
            assert auth.get_valid_token() == "t1"
            assert auth.get_valid_token() == "t1"
        assert len(httpx_mock.get_requests()) == 1

    def test_refresh_token_forces_reissue(self, httpx_mock):
        httpx_mock.add_response(url=TOKEN_URL, json={"token": "t1", "expires_in": 3600})
        httpx_mock.add_response(url=TOKEN_URL, json={"token": "t2", "expires_in": 3600})
        with KiwoomAuth("key", "secret", BASE) as auth:
            assert auth.get_valid_token() == "t1"
            assert auth.refresh_token() == "t2", "유효해도 강제 재발급"
            assert auth.get_valid_token() == "t2"
        assert len(httpx_mock.get_requests()) == 2

    def test_revoke_clears_cached_token(self, httpx_mock):
        httpx_mock.add_response(url=TOKEN_URL, json={"token": "t1", "expires_in": 3600})
        httpx_mock.add_response(url=f"{BASE}/oauth2/revoke", json={"return_code": 0})
        with KiwoomAuth("key", "secret", BASE) as auth:
            auth.get_valid_token()
            auth.revoke_token("t1")
            assert auth.token is None
            assert auth.expires_at is None


class _FakeProvider:
    """BaseClient 가 요구하는 TokenProvider 프로토콜의 최소 구현."""

    def __init__(self, tokens: list[str]) -> None:
        self._tokens = tokens
        self._i = 0
        self.refresh_calls = 0

    def get_valid_token(self) -> str:
        return self._tokens[self._i]

    def refresh_token(self) -> str:
        self.refresh_calls += 1
        self._i = min(self._i + 1, len(self._tokens) - 1)
        return self._tokens[self._i]


class TestBaseClientTokenProvider:
    def test_provider_supplies_authorization_header(self, httpx_mock):
        httpx_mock.add_response(url=API_URL, json={"return_code": 0, "ok": 1})
        provider = _FakeProvider(["tok-A"])
        with BaseClient("key", "secret", is_mock=True, token_provider=provider) as client:
            client.request("/api/dostk/stkinfo", "ka10001")
        req = httpx_mock.get_requests()[0]
        assert req.headers["authorization"] == "Bearer tok-A"

    def test_401_triggers_refresh_and_retry(self, httpx_mock):
        httpx_mock.add_response(url=API_URL, status_code=401, json={"return_msg": "expired"})
        httpx_mock.add_response(url=API_URL, json={"return_code": 0, "stk_nm": "삼성전자"})
        provider = _FakeProvider(["stale", "fresh"])
        with BaseClient(
            "key", "secret", is_mock=True, token_provider=provider, retry_backoff=0.01
        ) as client:
            result = client.request("/api/dostk/stkinfo", "ka10001")
        assert result["stk_nm"] == "삼성전자"
        assert provider.refresh_calls == 1
        reqs = httpx_mock.get_requests()
        assert len(reqs) == 2
        assert reqs[0].headers["authorization"] == "Bearer stale"
        assert reqs[1].headers["authorization"] == "Bearer fresh", "재시도는 새 토큰으로"

    def test_401_refresh_happens_only_once_per_request(self, httpx_mock):
        """재발급 후에도 401 이면 무한루프 대신 에러를 올린다."""
        httpx_mock.add_response(url=API_URL, status_code=401, json={})
        httpx_mock.add_response(url=API_URL, status_code=401, json={})
        provider = _FakeProvider(["a", "b"])
        with BaseClient(
            "key", "secret", is_mock=True, token_provider=provider, retry_backoff=0.01
        ) as client:
            with pytest.raises(httpx.HTTPStatusError):
                client.request("/api/dostk/stkinfo", "ka10001")
        assert provider.refresh_calls == 1
        assert len(httpx_mock.get_requests()) == 2, "재발급은 요청당 1회뿐"

    def test_401_without_provider_raises(self, httpx_mock):
        """수동 토큰 사용자는 기존대로 401 을 그대로 받는다 (하위호환)."""
        httpx_mock.add_response(url=API_URL, status_code=401, json={})
        with BaseClient("key", "secret", is_mock=True, retry_backoff=0.01) as client:
            client.access_token = "manual"
            with pytest.raises(httpx.HTTPStatusError):
                client.request("/api/dostk/stkinfo", "ka10001")
        assert len(httpx_mock.get_requests()) == 1, "provider 없으면 재발급 시도 없음"

    def test_manual_token_still_works(self, httpx_mock):
        """token_provider 를 안 넘기면 기존 access_token 경로 그대로."""
        httpx_mock.add_response(url=API_URL, json={"return_code": 0, "ok": 1})
        with BaseClient("key", "secret", is_mock=True) as client:
            client.access_token = "manual"
            client.request("/api/dostk/stkinfo", "ka10001")
        assert httpx_mock.get_requests()[0].headers["authorization"] == "Bearer manual"

    def test_provider_token_refreshed_between_429_retries(self, httpx_mock):
        """429 재시도 때도 헤더를 새로 만들어야 만료 토큰을 재사용하지 않는다."""
        httpx_mock.add_response(url=API_URL, status_code=429, json={})
        httpx_mock.add_response(url=API_URL, json={"return_code": 0, "ok": 1})
        provider = _FakeProvider(["tok-A"])
        with BaseClient(
            "key", "secret", is_mock=True, token_provider=provider, retry_backoff=0.01
        ) as client:
            client.request("/api/dostk/stkinfo", "ka10001")
        reqs = httpx_mock.get_requests()
        assert len(reqs) == 2
        assert all(r.headers["authorization"] == "Bearer tok-A" for r in reqs)


class TestKiwoomAPIWiring:
    def test_login_wires_provider_and_reuses_token(self, httpx_mock):
        from kiwoom_client import KiwoomAPI

        httpx_mock.add_response(url=TOKEN_URL, json={"token": "t1", "expires_in": 3600})
        httpx_mock.add_response(url=API_URL, json={"return_code": 0, "stk_nm": "삼성전자"})
        with KiwoomAPI("key", "secret", is_mock=True) as api:
            api.login()
            result = api.stock_info.basic_stock_info(stk_cd="005930")
        assert result["stk_nm"] == "삼성전자"
        api_req = next(r for r in httpx_mock.get_requests() if "stkinfo" in str(r.url))
        assert api_req.headers["authorization"] == "Bearer t1"

    def test_api_recovers_from_expired_token(self, httpx_mock):
        from kiwoom_client import KiwoomAPI

        httpx_mock.add_response(url=TOKEN_URL, json={"token": "t1", "expires_in": 3600})
        httpx_mock.add_response(url=API_URL, status_code=401, json={})
        httpx_mock.add_response(url=TOKEN_URL, json={"token": "t2", "expires_in": 3600})
        httpx_mock.add_response(url=API_URL, json={"return_code": 0, "stk_nm": "삼성전자"})
        with KiwoomAPI("key", "secret", is_mock=True, retry_backoff=0.01) as api:
            api.login()
            result = api.stock_info.basic_stock_info(stk_cd="005930")
        assert result["stk_nm"] == "삼성전자"
        last = [r for r in httpx_mock.get_requests() if "stkinfo" in str(r.url)][-1]
        assert last.headers["authorization"] == "Bearer t2"

    def test_auto_login_on_first_request(self, httpx_mock):
        """login() 을 안 불러도 첫 요청에서 토큰을 발급한다."""
        from kiwoom_client import KiwoomAPI

        httpx_mock.add_response(url=TOKEN_URL, json={"token": "t1", "expires_in": 3600})
        httpx_mock.add_response(url=API_URL, json={"return_code": 0, "stk_nm": "삼성전자"})
        with KiwoomAPI("key", "secret", is_mock=True) as api:
            result = api.stock_info.basic_stock_info(stk_cd="005930")
        assert result["stk_nm"] == "삼성전자"


class TestVersion:
    def test_version_matches_installed_metadata(self):
        from importlib.metadata import version

        import kiwoom_client

        assert kiwoom_client.__version__ == version("kiwoom-client")

    def test_version_is_not_hardcoded_stale(self):
        import kiwoom_client

        assert kiwoom_client.__version__ != "0.1.0"


class TestReturnCodeTokenError:
    """키움은 만료 토큰에 401 이 아니라 200 + return_code 3 을 준다.

    실서버 확인 (2026-08-15, api.kiwoom.com):
        HTTP 200, {"return_code": 3,
                   "return_msg": "인증에 실패했습니다[8005:Token이 유효하지 않습니다]"}
    401 만 보고 있으면 자동 재발급이 영원히 트리거되지 않는다.
    """

    def test_return_code_3_triggers_refresh_and_retry(self, httpx_mock):
        httpx_mock.add_response(
            url=API_URL,
            json={
                "return_code": 3,
                "return_msg": "인증에 실패했습니다[8005:Token이 유효하지 않습니다]",
            },
        )
        httpx_mock.add_response(url=API_URL, json={"return_code": 0, "stk_nm": "삼성전자"})
        provider = _FakeProvider(["stale", "fresh"])
        with BaseClient(
            "key", "secret", is_mock=True, token_provider=provider, retry_backoff=0.01
        ) as client:
            result = client.request("/api/dostk/stkinfo", "ka10001")
        assert result["stk_nm"] == "삼성전자"
        assert provider.refresh_calls == 1
        reqs = httpx_mock.get_requests()
        assert reqs[1].headers["authorization"] == "Bearer fresh", "재시도는 새 토큰으로"

    def test_refreshes_only_once_then_raises(self, httpx_mock):
        for _ in range(2):
            httpx_mock.add_response(
                url=API_URL, json={"return_code": 3, "return_msg": "인증에 실패했습니다"}
            )
        provider = _FakeProvider(["a", "b"])
        with BaseClient(
            "key", "secret", is_mock=True, token_provider=provider, retry_backoff=0.01
        ) as client:
            with pytest.raises(KiwoomAPIError) as exc:
                client.request("/api/dostk/stkinfo", "ka10001")
        assert exc.value.code == 3
        assert provider.refresh_calls == 1

    def test_without_provider_raises_immediately(self, httpx_mock):
        """수동 토큰 사용자는 기존대로 KiwoomAPIError 를 받는다."""
        httpx_mock.add_response(url=API_URL, json={"return_code": 3, "return_msg": "인증 실패"})
        with BaseClient("key", "secret", is_mock=True, retry_backoff=0.01) as client:
            client.access_token = "manual"
            with pytest.raises(KiwoomAPIError):
                client.request("/api/dostk/stkinfo", "ka10001")
        assert len(httpx_mock.get_requests()) == 1

    def test_other_error_codes_do_not_refresh(self, httpx_mock):
        """인증과 무관한 오류는 재발급 없이 그대로 올린다."""
        httpx_mock.add_response(url=API_URL, json={"return_code": -100, "return_msg": "입력 오류"})
        provider = _FakeProvider(["a", "b"])
        with BaseClient(
            "key", "secret", is_mock=True, token_provider=provider, retry_backoff=0.01
        ) as client:
            with pytest.raises(KiwoomAPIError):
                client.request("/api/dostk/stkinfo", "ka10001")
        assert provider.refresh_calls == 0
