"""Tests for the asyncio client."""

from __future__ import annotations

import asyncio
import time

import httpx
import pytest

from kiwoom_rest_api import AsyncKiwoomAPI
from kiwoom_rest_api.auth import AsyncKiwoomAuth, KiwoomAuthError
from kiwoom_rest_api.base import AsyncBaseClient, KiwoomAPIError
from kiwoom_rest_api.rate_limiter import AsyncPerKeyRateLimiter

BASE = "https://mockapi.kiwoom.com"
TOKEN_URL = f"{BASE}/oauth2/token"
API_URL = f"{BASE}/api/dostk/stkinfo"


class TestAsyncRateLimiter:
    async def test_burst_then_throttle(self):
        limiter = AsyncPerKeyRateLimiter(rate=100.0, capacity=2)
        start = time.monotonic()
        for _ in range(4):
            await limiter.acquire("ka10001")
        elapsed = time.monotonic() - start
        # 2 burst free, 2 more at 100/s → 최소 ~0.02s
        assert elapsed >= 0.015

    async def test_keys_are_independent(self):
        limiter = AsyncPerKeyRateLimiter(rate=1.0, capacity=1)
        start = time.monotonic()
        await limiter.acquire("ka10001")
        await limiter.acquire("ka10002")
        assert time.monotonic() - start < 0.1, "다른 TR 은 서로 막지 않는다"

    async def test_does_not_block_the_event_loop(self):
        """대기 중에도 다른 코루틴이 돌아야 한다 (time.sleep 이면 실패)."""
        limiter = AsyncPerKeyRateLimiter(rate=20.0, capacity=1)
        await limiter.acquire("k")
        ticks = 0

        async def ticker():
            nonlocal ticks
            for _ in range(5):
                await asyncio.sleep(0.005)
                ticks += 1

        await asyncio.gather(limiter.acquire("k"), ticker())
        assert ticks == 5


class TestAsyncAuth:
    async def test_issue_and_cache(self, httpx_mock):
        httpx_mock.add_response(url=TOKEN_URL, json={"token": "t1", "expires_in": 3600})
        async with AsyncKiwoomAuth("key", "secret", BASE) as auth:
            assert await auth.get_valid_token() == "t1"
            assert await auth.get_valid_token() == "t1"
        assert len(httpx_mock.get_requests()) == 1

    async def test_reissues_near_expiry(self, httpx_mock):
        httpx_mock.add_response(url=TOKEN_URL, json={"token": "t1", "expires_in": 30})
        httpx_mock.add_response(url=TOKEN_URL, json={"token": "t2", "expires_in": 3600})
        async with AsyncKiwoomAuth("key", "secret", BASE, expiry_margin=60.0) as auth:
            assert await auth.get_valid_token() == "t1"
            assert await auth.get_valid_token() == "t2"

    async def test_refresh_forces_reissue(self, httpx_mock):
        httpx_mock.add_response(url=TOKEN_URL, json={"token": "t1", "expires_in": 3600})
        httpx_mock.add_response(url=TOKEN_URL, json={"token": "t2", "expires_in": 3600})
        async with AsyncKiwoomAuth("key", "secret", BASE) as auth:
            await auth.get_valid_token()
            assert await auth.refresh_token() == "t2"

    async def test_missing_token_raises(self, httpx_mock):
        httpx_mock.add_response(url=TOKEN_URL, json={"return_msg": "bad key"})
        async with AsyncKiwoomAuth("key", "secret", BASE) as auth:
            with pytest.raises(KiwoomAuthError):
                await auth.issue_token()

    async def test_concurrent_callers_issue_once(self, httpx_mock):
        """동시 요청이 몰려도 토큰 발급은 한 번뿐이어야 한다."""
        httpx_mock.add_response(url=TOKEN_URL, json={"token": "t1", "expires_in": 3600})
        async with AsyncKiwoomAuth("key", "secret", BASE) as auth:
            tokens = await asyncio.gather(*(auth.get_valid_token() for _ in range(10)))
        assert tokens == ["t1"] * 10
        assert len(httpx_mock.get_requests()) == 1


class TestAsyncBaseClient:
    async def test_request_success(self, httpx_mock):
        httpx_mock.add_response(url=API_URL, json={"return_code": 0, "stk_nm": "삼성전자"})
        async with AsyncBaseClient("key", "secret", is_mock=True) as client:
            client.access_token = "token"
            result = await client.request("/api/dostk/stkinfo", "ka10001", {"stk_cd": "005930"})
        assert result["stk_nm"] == "삼성전자"

    async def test_api_error(self, httpx_mock):
        httpx_mock.add_response(url=API_URL, json={"return_code": -100, "return_msg": "Invalid"})
        async with AsyncBaseClient("key", "secret", is_mock=True) as client:
            with pytest.raises(KiwoomAPIError) as exc:
                await client.request("/api/dostk/stkinfo", "ka10001")
        assert exc.value.code == -100

    async def test_retries_on_429(self, httpx_mock):
        httpx_mock.add_response(url=API_URL, status_code=429, json={})
        httpx_mock.add_response(url=API_URL, json={"return_code": 0, "ok": 1})
        async with AsyncBaseClient(
            "key", "secret", is_mock=True, retry_backoff=0.01
        ) as client:
            result = await client.request("/api/dostk/stkinfo", "ka10001")
        assert result["ok"] == 1
        assert len(httpx_mock.get_requests()) == 2

    async def test_401_refreshes_token_once(self, httpx_mock):
        httpx_mock.add_response(url=TOKEN_URL, json={"token": "t1", "expires_in": 3600})
        httpx_mock.add_response(url=API_URL, status_code=401, json={})
        httpx_mock.add_response(url=TOKEN_URL, json={"token": "t2", "expires_in": 3600})
        httpx_mock.add_response(url=API_URL, json={"return_code": 0, "ok": 1})
        async with AsyncKiwoomAuth("key", "secret", BASE) as auth:
            async with AsyncBaseClient(
                "key", "secret", is_mock=True, token_provider=auth, retry_backoff=0.01
            ) as client:
                result = await client.request("/api/dostk/stkinfo", "ka10001")
        assert result["ok"] == 1
        api_reqs = [r for r in httpx_mock.get_requests() if "stkinfo" in str(r.url)]
        assert api_reqs[-1].headers["authorization"] == "Bearer t2"

    async def test_401_without_provider_raises(self, httpx_mock):
        httpx_mock.add_response(url=API_URL, status_code=401, json={})
        async with AsyncBaseClient(
            "key", "secret", is_mock=True, retry_backoff=0.01
        ) as client:
            client.access_token = "manual"
            with pytest.raises(httpx.HTTPStatusError):
                await client.request("/api/dostk/stkinfo", "ka10001")
        assert len(httpx_mock.get_requests()) == 1

    async def test_request_all_paginates(self, httpx_mock):
        httpx_mock.add_response(
            url=f"{BASE}/api/dostk/acnt",
            json={"return_code": 0, "items": [{"n": "A"}], "cont_yn": "Y", "next_key": "p2"},
        )
        httpx_mock.add_response(
            url=f"{BASE}/api/dostk/acnt",
            json={"return_code": 0, "items": [{"n": "B"}], "cont_yn": "N", "next_key": ""},
        )
        async with AsyncBaseClient("key", "secret", is_mock=True) as client:
            client.access_token = "token"
            result = await client.request_all("/api/dostk/acnt", "ka10076", data_key="items")
        assert [r["n"] for r in result] == ["A", "B"]


class TestAsyncKiwoomAPI:
    async def test_module_call_is_awaitable(self, httpx_mock):
        httpx_mock.add_response(url=TOKEN_URL, json={"token": "t1", "expires_in": 3600})
        httpx_mock.add_response(url=API_URL, json={"return_code": 0, "stk_nm": "삼성전자"})
        async with AsyncKiwoomAPI("key", "secret", is_mock=True) as api:
            result = await api.stock_info.basic_stock_info(stk_cd="005930")
        assert result["stk_nm"] == "삼성전자"

    async def test_concurrent_calls_to_different_trs(self, httpx_mock):
        """서로 다른 TR 은 동시에 나가야 한다 — async 를 만든 이유."""
        httpx_mock.add_response(url=TOKEN_URL, json={"token": "t1", "expires_in": 3600})
        httpx_mock.add_response(url=API_URL, json={"return_code": 0, "ok": 1})
        httpx_mock.add_response(
            url=f"{BASE}/api/dostk/chart", json={"return_code": 0, "ok": 2}
        )
        async with AsyncKiwoomAPI("key", "secret", is_mock=True) as api:
            start = time.monotonic()
            a, b = await asyncio.gather(
                api.stock_info.basic_stock_info(stk_cd="005930"),
                api.chart.stock_daily_chart(stk_cd="005930"),
            )
            elapsed = time.monotonic() - start
        assert a["ok"] == 1 and b["ok"] == 2
        assert elapsed < 1.0, "서로 다른 TR 이 직렬화되면 안 된다"

    async def test_login_and_logout(self, httpx_mock):
        httpx_mock.add_response(url=TOKEN_URL, json={"token": "t1", "expires_in": 3600})
        httpx_mock.add_response(url=f"{BASE}/oauth2/revoke", json={"return_code": 0})
        async with AsyncKiwoomAPI("key", "secret", is_mock=True) as api:
            await api.login()
            result = await api.logout()
        assert result["return_code"] == 0

    async def test_logout_without_token_raises(self):
        async with AsyncKiwoomAPI("key", "secret", is_mock=True) as api:
            with pytest.raises(RuntimeError):
                await api.logout()

    async def test_all_modules_are_exposed(self):
        """sync 와 같은 엔드포인트 모듈 집합을 갖는다."""
        from kiwoom_rest_api import KiwoomAPI
        from kiwoom_rest_api._registry import MODULE_NAMES

        api = AsyncKiwoomAPI("key", "secret", is_mock=True)
        try:
            for name in MODULE_NAMES:
                assert hasattr(KiwoomAPI, name), f"sync 에 {name} 없음"
                assert getattr(api, name) is not None
                # 같은 인스턴스를 재사용한다 (lazy 캐시)
                assert getattr(api, name) is getattr(api, name)
        finally:
            await api.close()
