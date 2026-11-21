---
seo_title: "Kiwoom Securities API on macOS and Linux — Python over REST, no OCX"
description: "Kiwoom OpenAPI+ (OCX) is Windows-only; the Kiwoom REST API runs on macOS, Linux and servers. App keys, pip install, a first quote, daily bars as a DataFrame, real-time trades."
---

# Kiwoom Securities API on macOS and Linux

Kiwoom's **OpenAPI+** is a Windows COM/OCX control, so it does not run on macOS or Linux and was tied to 32-bit Python
for years. The Kiwoom **REST API** is HTTPS (JSON) plus WebSocket, so the OS does not matter. This page walks through
macOS or Linux from install to your first call. For how the two compare see [Why kiwoom-client](why.md); to port
OpenAPI+ code see [Migrating from OpenAPI+ / pykiwoom](migration-from-openapi-plus.md).

| You need | Notes |
|---|---|
| A Kiwoom Securities account | Required to apply for API access |
| App key and secret | Apply on the [Kiwoom REST API portal](https://openapi.kiwoom.com). **Mock and live keys are separate** |
| Python 3.10+ (64-bit) | System Python, Homebrew, pyenv or uv — any works |
| Windows, OCX, a login window | Not needed |

## 1. Install

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install 'kiwoom-client[pandas]'   # with DataFrame helpers; plain kiwoom-client otherwise
```

With uv: `uv add 'kiwoom-client[pandas]'`.

## 2. Keys in environment variables

Keep keys out of your code — use environment variables or a `.env` file. The MCP server reads the same names.

```bash
export KIWOOM_APP_KEY=your_app_key
export KIWOOM_APP_SECRET=your_app_secret
export KIWOOM_IS_MOCK=true          # for a mock-trading key
```

!!! warning "The default is the live server"
    If `is_mock` is not set anywhere you connect to the **live trading server**. Pass `is_mock=True` explicitly at first.
    A mock key against the live server (or the reverse) is rejected (8030/8031 — see [Troubleshooting](troubleshooting.md)).

## 3. First call

```python
from kiwoom_client import KiwoomAPI

api = KiwoomAPI.from_env(is_mock=True)   # tokens are issued and refreshed for you

info = api.stock_info.basic_stock_info(stk_cd="005930")   # ka10001 basic stock info
print(info["stk_nm"], info["cur_prc"])
```

To look up a code by name, `api.stock_code("삼성전자")`. All 182 TRs are listed by api_id, Korean name and method in
the [endpoint reference](endpoints.md).

Or check from the command line (read-only — there are no order commands):

```bash
kiwoom quote 005930 --mock
kiwoom chart 005930 --daily -n 5 --mock
```

## 4. Daily bars as a DataFrame

```python
from kiwoom_client import to_ohlcv

resp = api.chart.stock_daily_chart(stk_cd="005930", base_dt="20260327", upd_stkpc_tp="1")
df = to_ohlcv(resp)   # open/high/low/close/volume, date index, oldest first
print(df.tail())
```

TRs that do not fit in one response continue via `cont-yn`/`next-key` — see the
[pagination recipe](cookbook/pagination.md).

## 5. Real-time trades (WebSocket)

```python
import asyncio

from kiwoom_client import KiwoomAPI


async def main():
    api = KiwoomAPI.from_env(is_mock=True)
    ws = api.create_websocket()
    await ws.connect()                                   # through LOGIN
    ws.on("0B", lambda d: print(d["item"], d["values"].get("10")))   # 10 = current price
    await ws.subscribe("0B", "005930")
    await ws.listen()                                    # handles PING, reconnect, resubscribe


asyncio.run(main())
```

More in the [real-time recipe](cookbook/realtime-trades.md).

## 6. Running on a server (cron, systemd, Docker)

There is no login window, so it runs as is on a headless Linux server or in a container. Pass keys as environment
variables.

```bash
docker run --rm --env-file .env python:3.12-slim \
  sh -c "pip install -q kiwoom-client && kiwoom quote 005930 --mock"
```

- **A token only works from the IP that received it.** Reusing a token on another server, or an outgoing IP that
  changes behind NAT, gives error 8010 — let each process get its own token ([Troubleshooting](troubleshooting.md)).
- Rate limits are per TR. The default rate limiter keeps you under them and retries on 429
  — [rate-limit recipe](cookbook/rate-limits.md) (Korean).
- With a live key, `api.order.*` and `api.credit_order.*` place real orders. Run automated trading on a mock account
  first — [tick-aligned limit orders](cookbook/limit-order.md).

## Next

- From AI agents: [MCP server](mcp.md) — Claude Code and Cursor look up quotes and your account
- Stuck: [Troubleshooting](troubleshooting.md) · [FAQ](faq.md)
