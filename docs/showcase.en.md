---
seo_title: "Projects using kiwoom-client"
description: "Public projects that run on kiwoom-client every day — a data pipeline, a quant core and trading daemons — and how they use the Kiwoom REST API."
---

# Showcase

Public projects that run on kiwoom-client. They run every day, so they double as examples of the library in use.

| Project | What it does | Where kiwoom-client is used |
|---|---|---|
| [quant-airflow](https://github.com/younghwan91/quant-airflow) | Airflow pipeline loading Korean market data (prices, flows, earnings) into TimescaleDB | Daily collection DAGs fetch prices, investor flows, margin and short-sale data |
| [krx-quant-core](https://github.com/younghwan91/krx-quant-core) | Shared core for KRX quant systems: ticks, price limits, cost model, order guard | Uses `tick_size`/`round_to_tick` as the source of truth and fails if its backtest tick table drifts |
| [daytrade-it](https://github.com/younghwan91/daytrade-it) | Day-trading research system: disclosure risk gate, Kiwoom broker adapter, MCP tools | The Kiwoom broker adapter calls quotes, account and orders through `KiwoomAPI` |
| [scalp-it](https://github.com/younghwan91/scalp-it) | Scalping strategy validation framework plus intraday tick and quote collection | The Kiwoom adapter queries through `KiwoomAPI`; `tick_size` for tick math |

<small>All of the above are public repositories by this library's author: research and personal trading code, not
investment advice. Descriptions summarise each repository's own description and code as of 2026-11.</small>

## Add your project

If a **public** project of yours uses kiwoom-client, open a PR adding one row to this page.

```markdown
| [Project](https://github.com/<user>/<repo>) | What it does (one line) | Where kiwoom-client is used (e.g. real-time fills, condition-search alert bot) |
```

- Public repositories and pages only. No account numbers, keys or P&L screenshots.
- No investment advice or return claims: just what the code does.
