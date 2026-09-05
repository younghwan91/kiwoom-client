"""Token-bucket rate limiters for Kiwoom REST API.

Kiwoom enforces request limits **independently per TR (api_id)**: empirically
about a burst of 2 with ~1 request/second sustained refill, returning HTTP 429
(`return_code=5`, "허용된 요청 개수를 초과하였습니다") when exceeded. A single
global limiter would needlessly throttle calls that target different TRs, so
``PerKeyRateLimiter`` keeps an independent bucket per key.
"""

from __future__ import annotations

import asyncio
import threading
import time


class RateLimiter:
    """Token-bucket rate limiter.

    Args:
        rate: Token refill rate in tokens/second (== max sustained req/s).
        capacity: Maximum tokens, i.e. burst size. Defaults to ``rate``.
    """

    def __init__(self, rate: float, capacity: float | None = None) -> None:
        self.rate = rate
        self.capacity = float(capacity) if capacity is not None else float(rate)
        self._tokens = self.capacity
        self._last_refill = time.monotonic()
        self._lock = threading.Lock()

    def acquire(self) -> None:
        """Acquire a token, blocking until one is available."""
        with self._lock:
            now = time.monotonic()
            elapsed = now - self._last_refill
            self._tokens = min(self.capacity, self._tokens + elapsed * self.rate)
            self._last_refill = now

            if self._tokens < 1:
                sleep_time = (1 - self._tokens) / self.rate
                time.sleep(sleep_time)
                self._tokens = 0
                self._last_refill = time.monotonic()
            else:
                self._tokens -= 1


class PerKeyRateLimiter:
    """Maintains an independent :class:`RateLimiter` bucket per key.

    Mirrors Kiwoom's per-TR (api_id) limiting so that calls to different
    endpoints do not throttle one another.

    Args:
        rate: Token refill rate in tokens/second, applied per key.
        capacity: Burst size per key. Defaults to ``rate``.
    """

    def __init__(self, rate: float, capacity: float | None = None) -> None:
        self.rate = rate
        self.capacity = capacity
        self._buckets: dict[str, RateLimiter] = {}
        self._lock = threading.Lock()

    def acquire(self, key: str) -> None:
        """Acquire a token for ``key``, blocking until one is available."""
        with self._lock:
            bucket = self._buckets.get(key)
            if bucket is None:
                bucket = RateLimiter(self.rate, self.capacity)
                self._buckets[key] = bucket
        # Sleep (if needed) outside the manager lock; each bucket self-locks.
        bucket.acquire()


class AsyncRateLimiter:
    """Token-bucket rate limiter for asyncio.

    Same algorithm as :class:`RateLimiter`, but it yields to the event loop
    while waiting instead of blocking the thread.

    Args:
        rate: Token refill rate in tokens/second (== max sustained req/s).
        capacity: Maximum tokens, i.e. burst size. Defaults to ``rate``.
    """

    def __init__(self, rate: float, capacity: float | None = None) -> None:
        self.rate = rate
        self.capacity = float(capacity) if capacity is not None else float(rate)
        self._tokens = self.capacity
        self._last_refill = time.monotonic()
        self._lock = asyncio.Lock()

    async def acquire(self) -> None:
        """Acquire a token, awaiting until one is available."""
        async with self._lock:
            now = time.monotonic()
            elapsed = now - self._last_refill
            self._tokens = min(self.capacity, self._tokens + elapsed * self.rate)
            self._last_refill = now

            if self._tokens < 1:
                sleep_time = (1 - self._tokens) / self.rate
                await asyncio.sleep(sleep_time)
                self._tokens = 0
                self._last_refill = time.monotonic()
            else:
                self._tokens -= 1


class AsyncPerKeyRateLimiter:
    """Maintains an independent :class:`AsyncRateLimiter` bucket per key.

    Args:
        rate: Token refill rate in tokens/second, applied per key.
        capacity: Burst size per key. Defaults to ``rate``.
    """

    def __init__(self, rate: float, capacity: float | None = None) -> None:
        self.rate = rate
        self.capacity = capacity
        self._buckets: dict[str, AsyncRateLimiter] = {}
        self._lock = asyncio.Lock()

    async def acquire(self, key: str) -> None:
        """Acquire a token for ``key``, awaiting until one is available."""
        async with self._lock:
            bucket = self._buckets.get(key)
            if bucket is None:
                bucket = AsyncRateLimiter(self.rate, self.capacity)
                self._buckets[key] = bucket
        # Await (if needed) outside the manager lock; each bucket self-locks.
        await bucket.acquire()
