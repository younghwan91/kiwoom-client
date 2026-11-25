---
seo_title: "kiwoom-client — Kiwoom REST API Python client and MCP server"
description: "Unofficial open-source Python client for the Kiwoom Securities REST API: 182 endpoints, real-time WebSocket, sync/async. No OCX — runs on macOS and Linux. MCP server built in."
hide:
  - navigation
  - toc
---

# kiwoom-client { .kc-sr-only }

<div class="kc-hero" markdown>

![kiwoom-client](images/brand/wordmark-light.svg#only-light)
![kiwoom-client](images/brand/wordmark-dark.svg#only-dark)

<p class="kc-tagline">The Kiwoom REST API, from Python and AI agents.</p>
<p class="kc-sub">An unofficial open-source Python client for the Kiwoom Securities REST API: 182 endpoints, condition search and real-time WebSocket. MCP server built in.</p>

[Quick start](#quick-start){ .md-button .md-button--primary }
[GitHub](https://github.com/younghwan91/kiwoom-client){ .md-button }
[PyPI](https://pypi.org/project/kiwoom-client/){ .md-button }

</div>

<div class="grid cards" markdown>

-   **Easy**

    ---

    `pip install`, add your app key and secret, done. Token issue, refresh before expiry, 401 reissue, per-TR rate
    limiting and pagination are handled for you. No COM/OCX, so it runs on Windows, macOS and Linux.

-   **AI-native**

    ---

    One command, `kiwoom-client-mcp`, gives Claude Code and Cursor all 182 REST endpoints and the 4 condition-search
    calls as MCP tools. `to_dataframe()` turns responses into numbers you can compute with.

-   **Live orders need your say-so**

    ---

    Against a live (실전투자) account the 12 order tools are **not even registered** until you set
    `KIWOOM_MCP_ALLOW_LIVE_ORDERS=true`. The agent never learns they exist.

</div>

## Quick start

```bash
pip install kiwoom-client
```

```python
from kiwoom_client import KiwoomAPI

api = KiwoomAPI(app_key="YOUR_APP_KEY", app_secret="YOUR_APP_SECRET", is_mock=True)  # True = mock trading

info = api.stock_info.basic_stock_info(stk_cd="005930")                   # Samsung Electronics
chart = api.chart.stock_daily_chart(stk_cd="005930", base_dt="20260326", upd_stkpc_tp="1")  # daily chart
print(info["stk_nm"])
```

Get an app key and secret at the [Kiwoom REST API portal](https://openapi.kiwoom.com) and start on the mock server
(`is_mock=True`).

!!! warning "The default is the live server"
    `KiwoomAPI(...)` defaults to `is_mock=False` (live). With live keys, `api.order.*` and `api.credit_order.*` place
    real orders. The MCP live-order guard covers the MCP server only, not direct Python calls.

## From an AI agent (MCP)

With [uv](https://docs.astral.sh/uv/) it starts in one line, no install:

```bash
uvx --from 'kiwoom-client[mcp]' kiwoom-client-mcp
```

Add it to Claude Code with `claude mcp add kiwoom -e KIWOOM_APP_KEY=YOUR_APP_KEY -e KIWOOM_APP_SECRET=YOUR_APP_SECRET -e KIWOOM_IS_MOCK=true -- uvx --from 'kiwoom-client[mcp]' kiwoom-client-mcp`. Claude Desktop, Cursor and Codex config is in [MCP server](mcp.md).

![Mock demo: an agent asks for quotes with get_quotes and drafts an order with order_preview](images/demo-mock.gif)

<small>**Mock demo** — the real MCP server wired to a fake Kiwoom server (made-up prices), with the tool calls replayed from a script. No order is sent. Replay it without keys from the repo root: `uv run --extra mcp python scripts/demo_mock_session.py`.</small>

## Where to next

| I want to | Go to |
|---|---|
| Read the full usage guide (sync/async, WebSocket, errors) | [README](https://github.com/younghwan91/kiwoom-client/blob/main/README.en.md) |
| Install and make a first call on macOS, Linux or a server | [macOS and Linux](macos-linux.md) |
| Look up an api_id or TR name among the 182 methods | [Endpoint reference](endpoints.md) |
| Connect it to Claude Code or Cursor | [MCP server](mcp.md) |
| Port OpenAPI+ / pykiwoom code to REST | [Migration table](migration-from-openapi-plus.md) |
| Compare with OpenAPI+, pykiwoom and other REST wrappers | [Why kiwoom-client](why.md) |
| Public projects built on it | [Showcase](showcase.md) |
| Kiwoom portal, MCP and public-data links | [Resources](resources.md) |
| Report a bug or ask for a feature | [GitHub Issues](https://github.com/younghwan91/kiwoom-client/issues) |

---

<small>kiwoom-client is an unofficial open-source project, not affiliated with or endorsed by Kiwoom Securities.
"Kiwoom" is a trademark of Kiwoom Securities Co., Ltd.; this project is only a client for its public REST API.</small>
