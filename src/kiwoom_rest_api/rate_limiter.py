"""Token-bucket rate limiter for Kiwoom REST API."""
import threading
import time


class RateLimiter:
    """Token-bucket rate limiter.

    Args:
        rate: Maximum requests per second.
    """

    def __init__(self, rate: float) -> None:
        self.rate = rate
        self._tokens = rate
        self._last_refill = time.monotonic()
        self._lock = threading.Lock()

    def acquire(self) -> None:
        """Acquire a token, blocking until one is available."""
        with self._lock:
            now = time.monotonic()
            elapsed = now - self._last_refill
            self._tokens = min(self.rate, self._tokens + elapsed * self.rate)
            self._last_refill = now

            if self._tokens < 1:
                sleep_time = (1 - self._tokens) / self.rate
                time.sleep(sleep_time)
                self._tokens = 0
                self._last_refill = time.monotonic()
            else:
                self._tokens -= 1
