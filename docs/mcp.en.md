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
| `--discovery` | expose only three meta tools (see "Saving context" below) |
| `--launcher installed` | use `kiwoom-client-mcp` from PATH instead of `uvx` |

## Environment variables and options

| Env var | CLI | Meaning | Default |
|---|---|---|---|
| `KIWOOM_APP_KEY`, `KIWOOM_APP_SECRET` | — | App key and secret (required to serve) | — |
| `KIWOOM_IS_MOCK` | `--mock` | paper-trading server. Accepts true/false, 1/0, yes/no; anything else is an error | `false` (live) |
| `KIWOOM_MCP_TOOLSETS` | `--toolsets` | modules to expose, comma-separated. `all` = every module | all |
| `KIWOOM_MCP_MODE` | `--discovery` | `discovery` = three meta tools only | everything listed |
| `KIWOOM_MCP_MAX_ROWS` | `--max-rows` | default row limit for list responses | no limit |
| `KIWOOM_MCP_ALLOW_LIVE_ORDERS` | (none) | expose order tools on a live account | `false` |

CLI options win over environment variables. The live-order opt-in deliberately has no CLI option.

Toolset names are the endpoint module names: `account`, `stock_info`, `market`, `chart`, `order`, `credit_order`, `ranking`, `sector`, `foreign_institution`, `short_selling`, `slb`, `theme`, `condition_search`, `elw`, `etf`.

## Live-order guard

- When `KIWOOM_IS_MOCK=false` (live) and `KIWOOM_MCP_ALLOW_LIVE_ORDERS` is not `true`, the server **does not register** the order tools (8 `order_*`, 4 `credit_order_*`). They do not appear in the tool list, `call_tool`, `search_tools` or `kiwoom://tools`.
- The toolset filter, discovery mode and the helper tools only ever see what the guard left. Picking `--toolsets order` does not bring order tools back without the opt-in. A regression test (`tests/test_mcp_live_order_regression.py`) pins this.
- Paper trading (`KIWOOM_IS_MOCK=true`) has no real fills, so the order tools are always available there.
- The guard exists only on the MCP server path. Using `KiwoomAPI`/`AsyncKiwoomAPI` from Python is not gated.

Order tools carry the `destructiveHint=true` annotation so clients can ask before running them. Lookup tools carry `readOnlyHint=true`.

### Order preview: `order_preview`

`order_preview` sends nothing (no network call). It returns:

- the price snapped to the tick size (down for a buy, up for a sell)
- field checks
- the estimated amount
- warnings
- the exact `params` to hand to the order tool

`order_tools_enabled` says whether this server has order tools at all. An agent should show the preview to the user and place an order only after explicit confirmation. The server's `instructions` and the `order_checklist` prompt describe that sequence.

## Tools

| Kind | Name | Notes |
|---|---|---|
| Helpers | `stock_search` | find a stock by name or code (ka10099, cached) |
| | `stock_snapshot` | price, change, market cap, PER/PBR and more in one call (ka10001) |
| | `account_summary` | account totals, P&L and holdings (kt00018) |
| | `order_preview` | order preview, never sent |
| TR tools | `<module>_<method>` | e.g. `stock_info_basic_stock_info`, `chart_stock_daily_chart`. [Full list](endpoints.md) |
| Condition search | 4 `condition_search_*` tools | WebSocket. Real-time registration returns the first reply only |

TR tools take Kiwoom request fields, as strings, under `params`. Each tool's input schema lists the field names, whether they are required and what they mean, from the TR catalog.

```json
{"params": {"stk_cd": "005930"}}
```

To fetch the next page, pass the response's `cont-yn`/`next-key` back as `cont_yn="Y"` and `next_key`.

## Saving context

Every tool definition lands in the agent's context. The size of `tools/list` by setting:

| Setting | Tools | `tools/list` size (characters) |
|---|---|---|
| everything (live, guarded) | 178 | about 230 K |
| `--toolsets market,chart,account` | 80 | about 100 K |
| `--discovery` | 3 | about 1.5 K |

(As of 0.4.x. The TR tools' input schemas include field descriptions, which makes them large.)

- **Toolsets**: turn on only the modules you use.
- **Discovery mode**: use every TR through three tools: `search_tools` (keyword or toolset search) → `describe_tool` (input schema) → `call_tool` (run).
- **`max_rows`**: pass `max_rows` to any lookup tool to keep only the first N rows of each list in the response. Set a server-wide default with `--max-rows`. A cut response carries `"_truncated": {"<key>": {"total": 300, "returned": 20}}`.

## Resources and prompts

| URI | Content |
|---|---|
| `kiwoom://guide` | usage rules for agents |
| `kiwoom://tools` | the tools exposed right now (name, toolset, read-only, api_id) |
| `kiwoom://codes/trade-types` | order type `trde_tp` and exchange `dmst_stex_tp` codes |
| `kiwoom://codes/markets` | market codes `mrkt_tp` (ka10099) |
| `kiwoom://tr/{api_id}` | request and response fields of one TR (e.g. `kiwoom://tr/ka10001`) |

There are three prompts:

- `analyze_stock(stock)`: analyse one stock, lookups only
- `review_account()`: check your account, lookups only
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
