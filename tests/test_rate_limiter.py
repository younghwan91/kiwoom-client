"""Tests for the token-bucket rate limiter."""
import time

import pytest

from kiwoom_rest_api.base import BaseClient
from kiwoom_rest_api.rate_limiter import RateLimiter


def test_rate_limiter_throttles():
    """RateLimiter(5) with 11 rapid acquire() calls should take >= 1.0 second.

    The bucket starts full (5 tokens). The first 5 calls consume them instantly.
    The next 5 calls must wait for tokens to refill at 5/s, taking ~1.0s total.
    11 calls total = 5 free + 5 waited = >= 1.0s elapsed.
    """
    limiter = RateLimiter(5)
    start = time.monotonic()
    for _ in range(11):
        limiter.acquire()
    elapsed = time.monotonic() - start
    assert elapsed >= 1.0, f"Expected >= 1.0s, got {elapsed:.3f}s"


def test_rate_limiter_no_throttle_within_budget():
    """RateLimiter(10) with 5 rapid acquire() calls should finish quickly."""
    limiter = RateLimiter(10)
    start = time.monotonic()
    for _ in range(5):
        limiter.acquire()
    elapsed = time.monotonic() - start
    assert elapsed < 1.0, f"Expected < 1.0s, got {elapsed:.3f}s"


def test_base_client_accepts_rate_limit():
    """BaseClient should accept rate_limit parameter without error."""
    client = BaseClient(
        app_key="test_key",
        app_secret="test_secret",
        rate_limit=5.0,
    )
    assert client._rate_limiter is not None
    assert isinstance(client._rate_limiter, RateLimiter)
    client.close()


def test_base_client_no_rate_limit():
    """BaseClient without rate_limit should have no rate limiter."""
    client = BaseClient(
        app_key="test_key",
        app_secret="test_secret",
    )
    assert client._rate_limiter is None
    client.close()


def test_base_client_rate_limit_none_explicit():
    """BaseClient with rate_limit=None should have no rate limiter."""
    client = BaseClient(
        app_key="test_key",
        app_secret="test_secret",
        rate_limit=None,
    )
    assert client._rate_limiter is None
    client.close()
