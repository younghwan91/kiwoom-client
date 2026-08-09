[한국어](README.md) | [English](README_EN.md)

# kiwoom-rest-api — Python wrapper for Kiwoom Securities REST API

[![PyPI version](https://img.shields.io/pypi/v/kiwoom-client)](https://pypi.org/project/kiwoom-client/)
[![Downloads](https://img.shields.io/pypi/dm/kiwoom-client)](https://pypi.org/project/kiwoom-client/)
[![CI](https://github.com/younghwan91/kiwoom-rest-api/actions/workflows/ci.yml/badge.svg)](https://github.com/younghwan91/kiwoom-rest-api/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/github/license/younghwan91/kiwoom-rest-api)](https://github.com/younghwan91/kiwoom-rest-api/blob/main/LICENSE)
[![Python](https://img.shields.io/pypi/pyversions/kiwoom-rest-api)](https://pypi.org/project/kiwoom-rest-api/)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-younghwan--chae-0A66C2?logo=linkedin&logoColor=white)](https://www.linkedin.com/in/younghwan-chae/)

> A modern Python wrapper for the **Kiwoom Securities REST API** — a cross-platform replacement for the legacy
> Kiwoom OpenAPI+ (OCX/COM). Automate Korean stock (KOSPI/KOSDAQ) trading, quotes, and real-time WebSocket
> data on Windows, macOS, and Linux. 207 endpoints · 19 real-time data types · mock & live trading.

A Python wrapper for [Kiwoom Securities](https://www.kiwoom.com/) REST API, covering all domestic stock endpoints.
Unlike the legacy OpenAPI+ (OCX/COM) or `pykiwoom`, it has no 32-bit/Windows-only constraints and runs in headless server environments.

## Why this library?

- **Cross-platform**: REST-based — works on Windows, macOS, Linux, and server environments. No COM/OCX dependency.
- **Auto token management**: Call `login()` once and all subsequent requests are authenticated automatically.
- **Auto pagination**: `request_all()` handles continuation queries in a single call.
- **Built-in rate limiter**: Token-bucket rate limiting to stay within API limits.
- **Full coverage**: 207 REST endpoints for Korean domestic stocks + 19 real-time WebSocket data types.

## Installation

```bash
pip install kiwoom-client
```

Or with [uv](https://docs.astral.sh/uv/):

```bash
uv add kiwoom-client
```

## Prerequisites

1. Sign up at the [Kiwoom REST API Portal](https://openapi.kiwoom.com).
2. Apply for API access to get your `app_key` and `app_secret`.
3. See [`.env.example`](.env.example) for environment variable setup.
4. Start with the **mock trading server** (`is_mock=True`) before switching to live trading.

## Quick Start

```python
from kiwoom_rest_api import KiwoomAPI

# Connect to mock trading server
api = KiwoomAPI(
    app_key="YOUR_APP_KEY",
    app_secret="YOUR_APP_SECRET",
    is_mock=True,
)

# Login (required before any API call)
api.login()

# Get stock info for Samsung Electronics (005930)
info = api.stock_info.basic_stock_info(stk_cd="005930")

# Get daily chart
chart = api.chart.stock_daily_chart(stk_cd="005930", base_dt="20260326")

# Place a buy order
result = api.order.buy_order(
    dmst_stex_tp="01",
    stk_cd="005930",
    ord_qty=10,
    trde_tp="00",
    ord_uv=70000,
)

# Logout
api.logout()
```

## Real-time WebSocket

```python
import asyncio
from kiwoom_rest_api import KiwoomAPI

api = KiwoomAPI(app_key="YOUR_KEY", app_secret="YOUR_SECRET")
api.login()

ws = api.create_websocket()

async def main():
    await ws.connect()
    ws.on("0B", lambda data: print(f"Trade: {data}"))
    await ws.subscribe("0B", ["005930", "000660"])
    await ws.listen()

asyncio.run(main())
```

## API Categories

| Category | Module | Endpoints |
|----------|--------|-----------|
| Account | `api.account` | 33 |
| Stock Info | `api.stock_info` | 31 |
| Market Data | `api.market` | 25 |
| Charts | `api.chart` | 21 |
| Rankings | `api.ranking` | 23 |
| Orders | `api.order` | 8 |
| Credit Orders | `api.credit_order` | 4 |
| Sectors | `api.sector` | 6 |
| Foreign/Institutional | `api.foreign_institution` | 4 |
| Short Selling | `api.short_selling` | 1 |
| Stock Lending (SLB) | `api.slb` | 4 |
| Themes | `api.theme` | 2 |
| Condition Search | `api.condition_search` | 4 |
| ELW | `api.elw` | 11 |
| ETF | `api.etf` | 9 |
| Real-time WebSocket | `api.create_websocket()` | 19 types |

For the full endpoint reference with method names and API IDs, see the [Korean README](README.md).

## Error Handling

```python
from kiwoom_rest_api.base import KiwoomAPIError

try:
    result = api.order.buy_order(stk_cd="005930", ord_qty=10, ord_uv=70000)
except KiwoomAPIError as e:
    print(f"Code: {e.code}, Message: {e.message}")
```

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for development setup and guidelines.

## License

MIT

---

## ⭐ Found this useful?

If this library helped you, please **[⭐ Star it](https://github.com/younghwan91/kiwoom-rest-api)** — it boosts discoverability so more developers can find it.

- 🐛 Bugs & questions → [Issues](https://github.com/younghwan91/kiwoom-rest-api/issues)
- 🔧 Improvements → PRs welcome ([CONTRIBUTING](CONTRIBUTING.md))
- 📈 [Follow](https://github.com/younghwan91) for new endpoints & release updates

## Related projects — Korean equity quant stack

This library is one piece of an open-source **Korean equity quant stack**, spanning market-data, fundamentals & news APIs, a collection pipeline, and alpha research.

| Project | What it is |
|---|---|
| **[krx-fundamentals-api](https://github.com/younghwan91/krx-fundamentals-api)** | Korean corporate fundamentals REST API — financials, ratios, dividends, screening (DART + KRX + Naver) |
| **[krx-news-rest-api](https://github.com/younghwan91/krx-news-rest-api)** | Korean stock news & disclosure REST API (FastAPI + Redis) |
| **[kr-quant-airflow](https://github.com/younghwan91/kr-quant-airflow)** | Airflow pipeline collecting Korean market data into TimescaleDB |
| **[kr-quant](https://github.com/younghwan91/kr-quant)** | KOSPI/KOSDAQ alpha research with enforced walk-forward & random negative-control guardrails |
| **[opt_portfolio](https://github.com/younghwan91/opt_portfolio)** | VAA-based tactical asset-allocation backtest & management system |
| **[automated-stock-trading-systems](https://github.com/younghwan91/automated-stock-trading-systems)** | Backtester for Bensdorp's 7 non-correlated trading systems (educational reimplementation) |
| **[quantbox-engine](https://github.com/younghwan91/quantbox-engine)** | Crypto-futures backtest & execution engine — zero lookahead, backtest↔live parity |

## Author

**Younghwan Chae** · [GitHub @younghwan91](https://github.com/younghwan91) · [LinkedIn](https://www.linkedin.com/in/younghwan-chae/)

See the full open-source quant stack on my [profile](https://github.com/younghwan91).
