# Handling rate limits (429)

The Kiwoom REST API limits the number of calls **separately for each TR (api_id)**. Go over it and you get HTTP `429`
with `{"return_code": 5, "return_msg": "허용된 요청 개수를 초과하였습니다"}` ("the allowed number of requests was
exceeded" — measured by this library). Kiwoom's official error codes include `1700` (API request count exceeded) ·
`1701` (total request count exceeded) · `1702` (group request count exceeded).

## What the library already does

| Mechanism | Default | Argument to change it |
|---|---|---|
| Per-TR token bucket — waits before sending | 1 per second, burst 2 | `rate_limit=`, `rate_burst=` (`rate_limit=None` turns it off) |
| On 429 · `return_code` 5, wait and send again | 3 times, 1.1 s × attempt number | `max_retries=`, `retry_backoff=` |

So within one process you usually do not need to do anything. Different TRs do not block each other; only repeating the
same TR slows down to 1 per second.

```python
from kiwoom_client import KiwoomAPI

api = KiwoomAPI.from_env(is_mock=True)                                   # defaults
api = KiwoomAPI.from_env(is_mock=True, rate_limit=0.5, rate_burst=1)     # slower (several processes sharing)
api = KiwoomAPI.from_env(is_mock=True, max_retries=5, retry_backoff=2.0)  # more persistent
```

## When it still overflows

If it still overflows after all retries are used up, an exception is raised. Which one depends on the signal the
request was rejected with.

```python
import httpx

from kiwoom_client import KiwoomAPI, KiwoomRateLimitError

api = KiwoomAPI.from_env(is_mock=True)

try:
    info = api.stock_info.basic_stock_info(stk_cd="005930")
except KiwoomRateLimitError as e:          # return_code 5 / 1700·1701·1702
    print("rate limit exceeded:", e.error_code, e.message)
except httpx.HTTPStatusError as e:         # still HTTP 429 after retries
    if e.response.status_code != 429:
        raise
    print("HTTP 429 — try again shortly")
```

## Several processes or programs on the same app key

The rate limiter counts **only within a process**. If several programs run with the same app key (a collection batch
plus a trading bot, say), together they can exceed the limit.

- Programs that call the same TR should split `rate_limit` between them (with two, `0.5` each).
- If you can, gather the queries into one process and have the others use its results.
- To see what was retried and how many times, turn `logging.getLogger("kiwoom_client")` up to DEBUG.

```python
import logging

logging.basicConfig(level=logging.INFO)
logging.getLogger("kiwoom_client").setLevel(logging.DEBUG)
```

## Making fewer calls in the first place

- A **continuation query** (연속조회) repeats the same TR, so it runs at 1 per second. Stop at the date you need —
  [pagination](pagination.md).
- **Many stocks**: instead of calling the same TR per stock, look for TRs that return many stocks at once (rankings
  `api.ranking.*`, sectors, condition search).
- **asyncio**: different TRs go out concurrently, so sending them together is faster —
  [concurrent queries with asyncio](async-concurrency.md).
- **Real time**: for values you watch continuously, do not poll REST repeatedly; receive them over the WebSocket —
  [real-time trades](realtime-trades.md).
