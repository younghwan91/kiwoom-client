---
seo_title: "Kiwoom MCP server — quotes and account lookups from Claude and Cursor"
description: "kiwoom-client-mcp gives Claude Code, Claude Desktop, Cursor and Codex Kiwoom REST API tools: quotes, charts, rankings, your account. Live order tools stay off until you opt in."
---

# MCP server

`kiwoom-client-mcp` exposes the Kiwoom REST API as MCP (Model Context Protocol) tools. Agents such as Claude Code, Claude Desktop, Cursor and Codex can look up quotes, charts, rankings and your account directly. On a live account the order tools are **not even registered** until you turn them on yourself.

## What to ask

Common requests in the default (smart) mode and the tools the agent calls. No api_id or field names needed; name a stock by its name or code.

| Ask | Tools used | Calls |
|---|---|---|
| "What's Samsung Electronics trading at? PER?" | `stock_snapshot` | 1 |
| "Quotes for Samsung Electronics, SK hynix and NAVER" | `get_quotes` (up to 20 stocks) | 1 |
| "Show my balance and returns" | `account_summary` | 1 |
| "Daily chart trend for SK hynix" | `get_chart` (day/week/month/minute, with moving averages and period return) | 1 |
| "What's EcoPro's ticker?" | `stock_search` | 1 |
| "Stocks with a volume spike today" | `search_tools` → `describe_tool` → `call_tool` (`ranking_sudden_volume_increase`) | 3 |
| "Foreign investors' trading in Samsung Electronics" | `search_tools` → `describe_tool` → `call_tool` (`foreign_institution_foreign_trading_trend`) | 3 |
| "Buy 10 Samsung Electronics at 70,000" | `order_preview` → user confirms → `place_order` (`confirm_token`) | 2 |
| "Cancel my unfilled order" | `call_tool` (`account_unfilled_orders`, plus 2 calls to find its name and input) → `order_preview` → user confirms → `cancel_order` | 3–5 |

- More one-call intent tools are being added; the current list is under [Tools](#tools).
- Order tools (`place_order` and the rest) exist on paper trading, or on a live account only with `KIWOOM_MCP_ALLOW_LIVE_ORDERS=true` ([Live-order guard](#live-order-guard)).
- 19 questions to paste as-is, with what each returns, are in the [prompt library](prompts.md).
- The prompts `review_account`, `analyze_stock`, `market_today`, `rebalance` and `order_checklist` give the agent these steps in one go ([Resources and prompts](#resources-and-prompts)).

## Install

The quickest way is to run it with [uv](https://docs.astral.sh/uv/), with nothing installed:

```bash
uvx --from 'kiwoom-client[mcp]' kiwoom-client-mcp --help
```

You can also install it with pip. You need the `[mcp]` extra (`mcp>=2.0`):

```bash
pip install 'kiwoom-client[mcp]'
kiwoom-client-mcp --version
```

Get an app key and secret from the [Kiwoom REST API portal](https://openapi.kiwoom.com). Start with a paper-trading (모의투자) key. Paper and live keys are different, and using one against the other server fails with error 8030.

## Add it to your client

### Claude Desktop: one-click bundle (.mcpb)

Download `kiwoom-client-<version>.mcpb` from [GitHub Releases](https://github.com/younghwan91/kiwoom-client/releases) and double-click it, or drop it on Claude Desktop's Settings → Extensions screen (bundles are attached from the release after 0.5.0). The install screen asks for:

| Field | Default | Notes |
|---|---|---|
| App key, app secret | — | masked and kept in secure storage |
| Paper-trading server | on | off = lookups on the live server. This bundle cannot turn on live order tools |
| Tool listing mode | `smart` | `full` or `discovery` (see "Saving context") |
| Modules to expose | empty (all) | e.g. `market,chart,account` |

The bundle carries no server code: on first run uv installs `kiwoom-client[mcp]` from PyPI at the bundle's version. To build one yourself run `python scripts/build_mcpb.py` (needs Node.js; validates and packs with the official `@anthropic-ai/mcpb` CLI).

### Config snippets

The `config` command prints a ready-to-paste snippet for each client. Keys come out as `YOUR_APP_KEY` placeholders and the default is paper trading. The command needs no keys and no network.

```bash
kiwoom-client-mcp config claude-code      # a `claude mcp add` command
kiwoom-client-mcp config claude-desktop   # JSON to merge into claude_desktop_config.json
kiwoom-client-mcp config cursor           # ~/.cursor/mcp.json or .cursor/mcp.json
kiwoom-client-mcp config codex            # ~/.codex/config.toml
kiwoom-client-mcp config vscode           # VS Code (GitHub Copilot) .mcp.json or ~/.copilot/mcp-config.json
kiwoom-client-mcp config gemini-cli       # ~/.gemini/settings.json
```

The snippet goes to stdout and the "where to put it" note goes to stderr, so `> mcp.json` saves valid JSON. The options are:

| Option | Effect |
|---|---|
| `--live` | `KIWOOM_IS_MOCK=false` (lookups on the live server). Order tools stay off |
| `--toolsets market,chart` | expose only these modules |
| `--full` | list every TR tool (see "Saving context" below) |
| `--discovery` | expose only three meta tools |
| `--launcher installed` | use `kiwoom-client-mcp` from PATH instead of `uvx` |

## Environment variables and options

| Env var | CLI | Meaning | Default |
|---|---|---|---|
| `KIWOOM_APP_KEY`, `KIWOOM_APP_SECRET` | — | App key and secret (required to serve) | — |
| `KIWOOM_IS_MOCK` | `--mock` | paper-trading server. Accepts true/false, 1/0, yes/no; anything else is an error | `false` (live) |
| `KIWOOM_MCP_TOOLSETS` | `--toolsets` | modules to expose, comma-separated. `all` = every module | all |
| `KIWOOM_MCP_MODE` | `--full`, `--discovery` | `smart`, `full` or `discovery` (see "Saving context") | `smart` |
| `KIWOOM_MCP_MAX_ROWS` | `--max-rows` | default row limit for list responses | no limit |
| `KIWOOM_MCP_ALLOW_LIVE_ORDERS` | (none) | expose order tools on a live account | `false` |
| `KIWOOM_MCP_READ_ONLY` | (none) | `true` registers no order tool at all, paper trading included | `false` |
| `KIWOOM_MCP_MASK_ACCOUNTS` | (none) | `false` returns account numbers unmasked in responses | `true` (last 4 only) |
| `KIWOOM_MCP_REQUIRE_CONFIRM` | (none) | require a `confirm_token` on the TR order tools (`order_*`, `credit_order_*`) | `true` live, `false` paper |
| `KIWOOM_MCP_MAX_ORDER_AMOUNT` | (none) | largest amount of one new order or change, KRW | no limit |
| `KIWOOM_MCP_MAX_ORDER_QTY` | (none) | largest quantity of one new order or change, shares | no limit |
| `KIWOOM_MCP_ALLOWED_STOCKS` | (none) | stock codes orders may name, comma-separated | no limit |
| `KIWOOM_MCP_DAILY_ORDER_LIMIT` | (none) | orders this server process may send per day (KST) | no limit |
| `KIWOOM_MCP_DUPLICATE_WINDOW` | (none) | refuse the exact same order sent again within this many seconds. `0` = off | `10` |
| `KIWOOM_MCP_AUDIT_LOG` | (none) | order audit log (JSONL) path. `off` = off | `~/.kiwoom-client/mcp-audit.jsonl` |

CLI options win over environment variables. The live-order opt-in deliberately has no CLI option.

Toolset names are the endpoint module names: `account`, `stock_info`, `market`, `chart`, `order`, `credit_order`, `ranking`, `sector`, `foreign_institution`, `short_selling`, `slb`, `theme`, `condition_search`, `elw`, `etf`.

## Live-order guard

- When `KIWOOM_IS_MOCK=false` (live) and `KIWOOM_MCP_ALLOW_LIVE_ORDERS` is not `true`, the server **does not register** the order tools (8 `order_*`, 4 `credit_order_*`, `place_order`/`modify_order`/`cancel_order`). They do not appear in the tool list, `call_tool`, `search_tools` or `kiwoom://tools`.
- The toolset filter, the listing modes (smart, full, discovery) and the helper tools only ever see what the guard left. Picking `--toolsets order` does not bring order tools back without the opt-in. A regression test (`tests/test_mcp_live_order_regression.py`) pins this.
- Paper trading (`KIWOOM_IS_MOCK=true`) has no real fills, so the order tools are always available there.
- With `KIWOOM_MCP_READ_ONLY=true` no order tool (`order_*`, `credit_order_*`, `place_order` ...) is registered, on paper trading or with the opt-in alike — for agents that should only look. `order_preview` stays but issues no token.
- The guard exists only on the MCP server path. Using `KiwoomAPI`/`AsyncKiwoomAPI` from Python is not gated.

Order tools carry the `destructiveHint=true` annotation so clients can ask before running them. Lookup tools carry `readOnlyHint=true`.

### Server-enforced safeguards at a glance

All of these are enforced inside the MCP server; nothing a model puts in a tool call turns them off. They apply top to bottom, and any one of them stops the order before a request is sent.

| Safeguard | Stops | Where | Setting |
|---|---|---|---|
| Live-order opt-in guard | order tools on a live account | tool registration at start | `KIWOOM_MCP_ALLOW_LIVE_ORDERS` (off by default) |
| Read-only mode | every order tool, paper trading included | tool registration at start | `KIWOOM_MCP_READ_ONLY` |
| Preview checks | prices outside the daily band, more than the buyable/sellable quantity | `order_preview` (errors → no token) | always (with a connection) |
| Order field allowlist | request fields the catalog doesn't list; arguments outside a high-level tool's schema | preview + right before sending | always |
| Limits, allowed stocks, daily cap | large orders, unlisted stocks, runaway loops | preview + right before sending | `KIWOOM_MCP_MAX_ORDER_AMOUNT` etc. (no limit by default) |
| Duplicate window | the same order sent again in quick succession | right before sending | `KIWOOM_MCP_DUPLICATE_WINDOW` (10 s) |
| Confirmation token | orders sent without a preview and confirmation, or changed after it | right before sending | always for `place_order` etc.; `KIWOOM_MCP_REQUIRE_CONFIRM` for TR tools (on for live by default) |
| Audit log | (records) previews, refusals, sends, failures | preview + around sending | `KIWOOM_MCP_AUDIT_LOG` |
| Account-number masking | account numbers in responses | every tool response | `KIWOOM_MCP_MASK_ACCOUNTS` (on by default) |

A regression test (`tests/test_mcp_order_safety_regression.py`) checks that every combination — direct call, `call_tool`, smart mode, `place_order` × no token, forged token, over a limit, outside the allowlist, unknown field, duplicate, daily cap, read-only — sends zero requests to the order endpoints.

### Order preview: `order_preview`

`order_preview` sends nothing. Apart from a stock-list lookup (ka10099) when you give a name, it makes no network call. It returns:

- the price snapped to the tick size (down for a buy, up for a sell)
- field checks
- the estimated amount
- warnings
- the exact `params` to hand to the order tool
- on a server with order tools, a `confirm_token` valid for that one order

New orders and changes are checked once more with lookup TRs. Problems come back as `errors` (the order can't go through) and `warnings` (close to a limit, or not checked); the looked-up values are in `checks`. With any `errors`, no token is issued.

| Check | Lookup TR | error | warning |
|---|---|---|---|
| Upper/lower price limit | ka10001 `upl_pric`, `lst_pric` | price outside the band | price within 2% of a limit |
| Buyable quantity | kt00011, quantity at the applied margin rate (`aplc_rt`) | more than the buyable quantity | more than the cash-only quantity (`min_ord_alowq`), or 90% or more of the buyable quantity |
| Sellable quantity | kt00018 `trde_able_qty` | more than the sellable quantity, or a stock not held | not on the first page of holdings |

A market buy is sized at the upper limit price. A failed lookup is never treated as a pass: it leaves a "not checked" warning. Cancels make no lookup.

The stock can be `stock` (a name or a code) or `stk_cd`; quantity and price can be `qty`/`price` (`"market"` = market order) or the TR field names (`ord_qty`/`ord_uv`). With `action="modify"` or `"cancel"` and an `order_no` it previews a change or a cancel; with `tool` (e.g. `credit_order_margin_buy_order`) and `params` it previews that TR tool.

`order_tools_enabled` says whether this server has order tools at all. An agent should show the preview to the user and place an order only after explicit confirmation. The server's `instructions` and the `order_checklist` and `rebalance` prompts describe that sequence.

### Confirmation tokens (two-step orders)

The server makes the `confirm_token`: an HMAC, under a random secret created when the process starts, over the previewed order's TR tool name and its normalised request fields. The token does not contain the order. An order tool refuses the order, **sending nothing**, when

- there is no token,
- anything differs from the preview (stock, quantity, price, trade type ...),
- 120 seconds have passed,
- the token was already used, or
- the token came from before a server restart.

`place_order`, `modify_order` and `cancel_order` always require a token. The TR order tools (`order_*`, `credit_order_*`) follow `KIWOOM_MCP_REQUIRE_CONFIRM`: `true` by default on a live account, `false` on paper trading. A token that is given is checked even where none is required. These checks run **after** the live-order opt-in guard; without the opt-in the order tools are still not registered at all.

### Limits and allowed stocks

Set any of the four variables above and the server enforces it. `order_preview` puts a breach in `errors` and issues no token, and the check runs again right before sending: a breach is refused and nothing is sent. The send-time check does not trust the preview.

- The amount is price × quantity. A market order is valued at the upper price limit (ka10001); if that lookup fails, the amount limit can't be checked and the order is refused.
- Cancels skip the quantity and amount limits. The allowed stocks and the daily count apply to cancels too.
- The daily count is the orders (new, change, cancel) this process sent to Kiwoom. Refused attempts don't count; a restart or a new day (KST) starts from zero.
- Unset means no limit (the previous behaviour).

### Order field allowlist

The order tools (`order_*`, `credit_order_*`) accept only the TR catalog's request fields in `params` (and as flat top-level fields). Any other key — even with an empty value — refuses the order, unsent, so a field slipped in by prompt injection can't change what is sent. Their input schema's `params` is `additionalProperties: false`. Lookup tools still forward fields the catalog doesn't list, as before.

### Duplicate orders

An order with the same TR tool and request fields as one just sent is refused, unsent, if it arrives within `KIWOOM_MCP_DUPLICATE_WINDOW` (default 10 s) — even with a fresh token from a new preview. This stops a retry loop, or an instruction handled twice, from placing the same order twice. The preview warns in that case; refused orders are not remembered.

### Account numbers in responses

In every tool response, account-number fields (the TR catalog fields named 계좌번호: `acnt_no`, `acctNo`, `acnt_print` ...) keep only their last 4 characters, so account numbers don't end up in chat transcripts or agent logs. Set `KIWOOM_MCP_MASK_ACCOUNTS=false` to get them as Kiwoom sends them.

### Audit log

The server appends every order attempt, one JSON object per line, to `KIWOOM_MCP_AUDIT_LOG` (default `~/.kiwoom-client/mcp-audit.jsonl`; `off` turns it off).

| `event` | When | Main fields |
|---|---|---|
| `preview` | `order_preview` built an order | `tool`, `params`, `errors`, `warnings` (count), `token_issued` |
| `rejected` | the server refused it; nothing sent | `via` (tool called), `tool`, `params`, `reasons`, `token_given` |
| `sent` | it went to Kiwoom | `via`, `tool`, `params`, `result` (`return_code`, `return_msg`, `ord_no`) |
| `failed` | it went to Kiwoom and the call raised | `via`, `tool`, `params`, `error` |

App key, secret, access token and `confirm_token` are never written; account-number fields keep only their last 4 characters. The file is created `0600` in a `0700` directory. If the log can't be written, the order is neither blocked nor changed; the server logs a warning.

## Tools

| Kind | Name | Notes |
|---|---|---|
| Intent tools | `stock_search` | find a stock by name or code (ka10099, cached) |
| | `stock_snapshot` | price, change, market cap, PER/PBR and more in one call (ka10001). Takes a stock name too |
| | `account_summary` | account totals, P&L and holdings (kt00018) |
| | `get_chart` | day/week/month/minute OHLCV (oldest first) + period return, high/low, average volume, 5/20 moving averages. Follows pages up to `count` (ka10081/82/83/80) |
| | `get_quotes` | price, change, volume, trade value and market cap for up to 20 stocks in one request (ka10095). Unresolved stocks get a per-stock error |
| | `market_movers` | today's top stocks: `kind` = volume, gainers, losers, value (trade value), volume_spike; `market` = all, kospi, kosdaq (ka10030/10027/10032/10023) |
| | `investor_flow` | daily net buying by individuals, foreigners, institutions (and pension funds etc.) with period totals and buy/sell day counts; amount (million KRW) or shares (ka10059) |
| | `get_orders` | open or filled orders. Today via ka10075/ka10076, other days via kt00007. Open rows carry `cancel_preview_args` for `order_preview` |
| | `get_buying_power` | how many shares/how much for a stock at a price (by margin rate and cash-only, kt00011); without a stock, deposit, D+2, orderable and withdrawable amounts (kt00001) |
| | `get_portfolio` | holdings with qty, average price, value, P&L, return and weight (of total assets and of stocks), plus cash (D+2), orderable cash and total assets. Account number masked (kt00018+kt00001+ka00001) |
| | `rebalance_plan` | whole-share quantities and tick-valid prices to reach target weights (`{"005930": 0.5}`) from current holdings and prices. Sells first, buys within cash. **Sends nothing** — each row carries `order_preview_args` |
| | `watch` | collects live trades (0B) for up to 60 s and returns last price, high/low, buy/sell volume and tick count per stock; returns at once when `until` (e.g. `{"stock": "005930", "above": 72000}`) is hit. WebSocket |
| | `condition_search_run` | runs a saved condition (영웅문4) once by name (partial) or number and returns the matching stocks with code, name, price, change % and volume (CNSRLST→CNSRREQ, WebSocket) |
| | `order_preview` | preview of an order, change or cancel, never sent. Issues a `confirm_token` |
| Orders (opt-in) | `place_order`, `modify_order`, `cancel_order` | order, change or cancel by stock name, quantity and price (or `"market"`). `confirm_token` required |
| TR tools | `<module>_<method>` | e.g. `stock_info_basic_stock_info`, `chart_stock_daily_chart`. [Full list](endpoints.md) |
| Condition search | 4 `condition_search_*` tools | WebSocket. Real-time registration returns the first reply only |

Intent tools answer one thing a person asks in one call, with no api_id or field names. They take a stock as a name (`"삼성전자"`) or a code (`"005930"`); a name that matches several stocks returns an error listing the candidates. Numbers come back without signs-as-direction, commas or zero padding, and lists are cut to a default row count. All of them are read-only (`readOnlyHint=true`).

TR tools take Kiwoom request fields, as strings, under `params`. Each tool's input schema lists the field names, whether they are required and what they mean, from the TR catalog.

```json
{"params": {"stk_cd": "005930"}}
```

To fetch the next page, pass the response's `cont-yn`/`next-key` back as `cont_yn="Y"` and `next_key`.

## Saving context

Every tool definition lands in the agent's context. So the default mode (`smart`) lists only the helper tools and three meta tools, and the agent finds the other TR tools through the meta tools. The size of `tools/list` by setting (measured on the live server with the guard on):

| Setting | Tools | `tools/list` size (characters) |
|---|---|---|
| default `smart` | 17 | about 12.8 K |
| `--discovery` | 3 | about 1.4 K |
| `--full` | 188 | about 228 K |
| `--full --toolsets market,chart,account` | 86 | about 102 K |

(Each TR tool's input schema lists its request field IDs and Korean names, which makes them large. Paper trading adds the order tools. The smart count grows as helper tools are added. A test checks these numbers against the real list; `kiwoom-client-mcp doctor` shows the values for your own setup.)

- **Smart mode (default)**: call the helper tools (`stock_search`, `stock_snapshot`, `account_summary`, `order_preview`, ...) directly; reach any other TR with `search_tools` (keyword or toolset search) → `describe_tool` (input schema) → `call_tool` (run).
- **Full mode**: `--full` or `KIWOOM_MCP_MODE=full`. The default up to 0.5.x: every TR tool is listed. Switch back to it if your client struggles with the meta tools or an existing setup calls TR tools by name.
- **Discovery mode**: only the three meta tools. Helper tools are called through `call_tool` too.
- **Toolsets**: turn on only the modules you use. Applies in every mode.
- **`max_rows`**: pass `max_rows` to any lookup tool to keep only the first N rows of each list in the response. Set a server-wide default with `--max-rows`. A cut response carries `"_truncated": {"<key>": {"total": 300, "returned": 20}}`.

## Resources and prompts

| URI | Content |
|---|---|
| `kiwoom://guide` | usage rules for agents |
| `kiwoom://tools` | the tools exposed right now (name, toolset, read-only, api_id) |
| `kiwoom://codes/trade-types` | order type `trde_tp` and exchange `dmst_stex_tp` codes |
| `kiwoom://codes/markets` | market codes `mrkt_tp` (ka10099) |
| `kiwoom://tr/{api_id}` | request and response fields of one TR (e.g. `kiwoom://tr/ka10001`) |

The server's `instructions` steer the agent: helper tools first, then `search_tools`, and orders only after a preview and the user's confirmation. There are five prompts:

- `review_account()`: check balances (P&L, unfilled orders, deposit), lookups only
- `analyze_stock(stock)`: analyse one stock (price, metrics, daily chart, flows), lookups only
- `market_today(focus?)`: today's market (sector indices, top value/movers, foreign and institutional flows), lookups only
- `rebalance(target)`: compare target weights with holdings, build an order plan and previews, never order before the user confirms
- `order_checklist(request)`: build a preview and never order before the user confirms

## Troubleshooting

Start with `doctor`. It does not start the server, needs no keys and makes no network call. It shows whether each environment variable is set, never its value.

```bash
kiwoom-client-mcp doctor                  # Python/mcp versions, which env vars are set, server, mode, guard, tools/list size
kiwoom-client-mcp --mock doctor           # server options go before doctor (resolved exactly as when serving)
kiwoom-client-mcp doctor --check-auth     # issue one token to check the keys (one request to Kiwoom, never revoked)
```

It exits with code 1 and `[err]` lines when something is wrong.

| Symptom | Cause and fix |
|---|---|
| `KIWOOM_APP_KEY and KIWOOM_APP_SECRET ... must be set` | put the keys in the client config's `env` |
| `MCP 서버에는 mcp 패키지가 필요합니다` | installed without the `[mcp]` extra. Use `pip install 'kiwoom-client[mcp]'` or `uvx --from 'kiwoom-client[mcp]' ...` |
| `ImportError: ServerRequestContext` | an old `mcp` 1.x is installed. Run `pip install -U 'mcp>=2.0,<3'` |
| `KIWOOM_IS_MOCK=... 를 해석할 수 없습니다` | use true/false (or 1/0, yes/no) |
| error 8030/8031 | the paper/live key does not match `KIWOOM_IS_MOCK` |
| no order tools | intended (live server without the opt-in). Test on paper trading, or see "Live-order guard" above |
