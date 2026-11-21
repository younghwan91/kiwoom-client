# Concurrent queries with asyncio

`AsyncKiwoomAPI` has the same methods as `KiwoomAPI`; you just put `await` in front of the call. The gain comes when you
send **different TRs** at the same time. Kiwoom's rate limits are per TR (api_id), so the library queues each TR
separately too.

| Sent at the same time | Time taken (default rate limiter: 1 request per second per TR, burst 2) |
|---|---|
| 3 different TRs | One round trip — they do not wait for each other |
| The same TR 10 times (10 stocks) | About 8 seconds — the first 2 go at once, the rest at 1 per second |

## Different TRs at once

```python
import asyncio

from kiwoom_client import AsyncKiwoomAPI, to_dataframe


async def main():
    async with AsyncKiwoomAPI.from_env(is_mock=True) as api:
        info, quote, daily = await asyncio.gather(
            api.stock_info.basic_stock_info(stk_cd="005930"),   # ka10001
            api.market.stock_quote(stk_cd="005930"),            # ka10004
            api.chart.stock_daily_chart(stk_cd="005930", base_dt="20260326", upd_stkpc_tp="1"),
        )
    print(info["stk_nm"], "ask1", quote["sel_fpr_bid"], "bid1", quote["buy_fpr_bid"])
    print(to_dataframe(daily).head())


asyncio.run(main())
```

## Many stocks — the same TR waits its turn

If you call the same TR for several stocks, the library orders the calls so they stay within that one TR's limit
(1 per second), even when you bundle them with `gather`. That is faster than getting 429s and retrying, and your code
can stay as it is.

```python
import asyncio

from kiwoom_client import AsyncKiwoomAPI, KiwoomAPIError

CODES = ["005930", "000660", "035420", "005380", "051910"]


async def main():
    async with AsyncKiwoomAPI.from_env(is_mock=True) as api:
        results = await asyncio.gather(
            *(api.stock_info.basic_stock_info(stk_cd=code) for code in CODES),
            return_exceptions=True,  # if one stock fails, still get the rest
        )
    for code, res in zip(CODES, results):
        if isinstance(res, KiwoomAPIError):
            print(code, "failed:", res)
        elif isinstance(res, BaseException):
            raise res
        else:
            print(code, res["stk_nm"], res["cur_prc"])


asyncio.run(main())
```

- Jobs that call the same TR many times (looping over every stock and so on) do not get faster unless you can change
  the TR. In that case look for TRs that return many stocks at once (rankings, sectors, condition search), or use data
  you fetched beforehand.
- When several **processes** call the same TR with the same app key, each process counts separately, so together they
  can exceed the limit — [handling rate limits](rate-limits.md).
- Use `AsyncKiwoomAPI` with `async with`, or call `await api.close()` at the end.
