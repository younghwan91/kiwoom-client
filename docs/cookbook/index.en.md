---
seo_title: "Kiwoom REST API Python examples (cookbook)"
description: "Ready-to-run Python examples for the Kiwoom REST API: daily bars as a DataFrame, account summary, pagination, rate limits, asyncio, real-time trades, condition search, mock orders."
---

# Cookbook

Common tasks as code you can run right away. Every example uses **mock trading** (`is_mock=True`) and reads the keys
from the `KIWOOM_APP_KEY` · `KIWOOM_APP_SECRET` environment variables (`KiwoomAPI.from_env`).

```bash
pip install 'kiwoom-client[pandas]'
export KIWOOM_APP_KEY=...  KIWOOM_APP_SECRET=...   # a mock-trading key
```

| Recipe | Uses |
|---|---|
| [Daily bars as a DataFrame](daily-chart.md) | `ka10081`, `to_dataframe()` |
| [Paging through a continuation query](pagination.md) | `cont_yn`·`next_key`, `request_all()` |
| [Account balance and valuation summary](account-summary.md) | `kt00018`, `kt00001` |
| [Concurrent queries with asyncio](async-concurrency.md) | `AsyncKiwoomAPI`, `asyncio.gather` |
| [Tick-aligned limit orders, mock trading](limit-order.md) | `round_to_tick()`·`add_ticks()`, `kt10000`–`kt10003` |
| [Real-time trades and order book over WebSocket](realtime-trades.md) | `0B`·`0D`, `ws.on()`·`ws.subscribe()` |
| [Condition search results in real time](condition-search-realtime.md) | `CNSRLST`·`CNSRREQ`·`CNSRCLR` |
| [Handling rate limits (429)](rate-limits.md) | `rate_limit`·`max_retries`, `KiwoomRateLimitError` |

New here? Start with the [condition-search alert bot in 10 minutes](../tutorials/condition-alert-bot.md), which runs right away on demo data with no key.

To find the TR you need, see the [endpoint reference](../endpoints.md); for fields, the
[field reference](../reference/index.md). Wrong request field names can be caught before sending with
`KiwoomAPI.from_env(is_mock=True, validate_params="warn")`.

> The tests **actually run** the REST examples on these pages against fake responses built from Kiwoom's official spec
> (`tests/test_cookbook_exec.py`). WebSocket examples are checked for syntax and names only.
