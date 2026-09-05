"""Tests for the token-bucket rate limiter."""
import time

from kiwoom_client.base import BaseClient
from kiwoom_client.rate_limiter import PerKeyRateLimiter, RateLimiter


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


def test_capacity_separate_from_rate():
    """capacity controls burst independently of refill rate."""
    # rate 1/s, burst 2: two acquires instant, third must wait ~1s.
    limiter = RateLimiter(1, capacity=2)
    start = time.monotonic()
    limiter.acquire()
    limiter.acquire()
    mid = time.monotonic() - start
    assert mid < 0.5, f"first 2 (burst) should be instant, got {mid:.3f}s"
    limiter.acquire()
    elapsed = time.monotonic() - start
    assert elapsed >= 1.0, f"3rd should wait for refill, got {elapsed:.3f}s"


def test_per_key_buckets_are_independent():
    """Exhausting one key's bucket must not throttle a different key."""
    limiter = PerKeyRateLimiter(rate=1, capacity=2)
    # Drain key A's burst (2 tokens).
    limiter.acquire("ka10001")
    limiter.acquire("ka10001")
    # Key B is fresh: its first 2 acquires should be instant.
    start = time.monotonic()
    limiter.acquire("ka10004")
    limiter.acquire("ka10004")
    elapsed = time.monotonic() - start
    assert elapsed < 0.5, f"independent key should not be throttled, got {elapsed:.3f}s"


def test_base_client_default_rate_limiter_is_per_key():
    """BaseClient enables a per-TR limiter by default (matches Kiwoom's model)."""
    client = BaseClient(app_key="test_key", app_secret="test_secret")
    assert isinstance(client._rate_limiter, PerKeyRateLimiter)
    assert client._rate_limiter.rate == BaseClient.DEFAULT_RATE_LIMIT
    assert client._rate_limiter.capacity == BaseClient.DEFAULT_RATE_BURST
    client.close()


def test_base_client_accepts_rate_limit():
    """BaseClient should accept an explicit rate_limit as a per-TR limiter."""
    client = BaseClient(app_key="test_key", app_secret="test_secret", rate_limit=5.0)
    assert isinstance(client._rate_limiter, PerKeyRateLimiter)
    assert client._rate_limiter.rate == 5.0
    client.close()


def test_base_client_rate_limit_none_disables():
    """BaseClient with rate_limit=None should have no rate limiter."""
    client = BaseClient(app_key="test_key", app_secret="test_secret", rate_limit=None)
    assert client._rate_limiter is None
    client.close()
