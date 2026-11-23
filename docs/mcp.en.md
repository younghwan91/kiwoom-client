---
seo_title: "Kiwoom MCP server — quotes and account lookups from Claude and Cursor"
description: "kiwoom-client-mcp gives Claude Code, Claude Desktop, Cursor and Codex Kiwoom REST API tools: quotes, charts, rankings, your account. Live order tools stay off until you opt in."
---

# MCP server

`kiwoom-client-mcp` exposes the Kiwoom REST API as MCP (Model Context Protocol) tools. Agents such as Claude Code, Claude Desktop, Cursor and Codex can look up quotes, charts, rankings and your account directly. On a live account the order tools are **not even registered** until you turn them on yourself.

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
| `KIWOOM_MCP_REQUIRE_CONFIRM` | (none) | require a `confirm_token` on the TR order tools (`order_*`, `credit_order_*`) | `true` live, `false` paper |

CLI options win over environment variables. The live-order opt-in deliberately has no CLI option.

Toolset names are the endpoint module names: `account`, `stock_info`, `market`, `chart`, `order`, `credit_order`, `ranking`, `sector`, `foreign_institution`, `short_selling`, `slb`, `theme`, `condition_search`, `elw`, `etf`.

## Live-order guard

- When `KIWOOM_IS_MOCK=false` (live) and `KIWOOM_MCP_ALLOW_LIVE_ORDERS` is not `true`, the server **does not register** the order tools (8 `order_*`, 4 `credit_order_*`, `place_order`/`modify_order`/`cancel_order`). They do not appear in the tool list, `call_tool`, `search_tools` or `kiwoom://tools`.
- The toolset filter, the listing modes (smart, full, discovery) and the helper tools only ever see what the guard left. Picking `--toolsets order` does not bring order tools back without the opt-in. A regression test (`tests/test_mcp_live_order_regression.py`) pins this.
- Paper trading (`KIWOOM_IS_MOCK=true`) has no real fills, so the order tools are always available there.
- The guard exists only on the MCP server path. Using `KiwoomAPI`/`AsyncKiwoomAPI` from Python is not gated.

Order tools carry the `destructiveHint=true` annotation so clients can ask before running them. Lookup tools carry `readOnlyHint=true`.

### Order preview: `order_preview`

`order_preview` sends nothing. Apart from a stock-list lookup (ka10099) when you give a name, it makes no network call. It returns:

- the price snapped to the tick size (down for a buy, up for a sell)
- field checks
- the estimated amount
- warnings
- the exact `params` to hand to the order tool
- on a server with order tools, a `confirm_token` valid for that one order

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

## Tools

| Kind | Name | Notes |
|---|---|---|
| Intent tools | `stock_search` | find a stock by name or code (ka10099, cached) |
| | `stock_snapshot` | price, change, market cap, PER/PBR and more in one call (ka10001). Takes a stock name too |
| | `account_summary` | account totals, P&L and holdings (kt00018) |
| | `get_chart` | day/week/month/minute OHLCV (oldest first) + period return, high/low, average volume, 5/20 moving averages. Follows pages up to `count` (ka10081/82/83/80) |
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
| default `smart` | 7 | about 3.9 K |
| `--discovery` | 3 | about 1.4 K |
| `--full` | 178 | about 219 K |
| `--full --toolsets market,chart,account` | 80 | about 97 K |

(Each TR tool's input schema lists its request field IDs and Korean names, which makes them large. Paper trading adds the order tools. The smart count grows as helper tools are added.)

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

| Symptom | Cause and fix |
|---|---|
| `KIWOOM_APP_KEY and KIWOOM_APP_SECRET ... must be set` | put the keys in the client config's `env` |
| `MCP 서버에는 mcp 패키지가 필요합니다` | installed without the `[mcp]` extra. Use `pip install 'kiwoom-client[mcp]'` or `uvx --from 'kiwoom-client[mcp]' ...` |
| `ImportError: ServerRequestContext` | an old `mcp` 1.x is installed. Run `pip install -U 'mcp>=2.0,<3'` |
| `KIWOOM_IS_MOCK=... 를 해석할 수 없습니다` | use true/false (or 1/0, yes/no) |
| error 8030/8031 | the paper/live key does not match `KIWOOM_IS_MOCK` |
| no order tools | intended (live server without the opt-in). Test on paper trading, or see "Live-order guard" above |
