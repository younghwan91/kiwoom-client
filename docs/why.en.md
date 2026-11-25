---
seo_title: "Kiwoom Python libraries compared — OpenAPI+ (OCX), pykiwoom, REST API"
description: "Kiwoom OpenAPI+ (OCX/COM) vs the Kiwoom REST API, and the Python libraries for each, compared on facts: OS, 64-bit, servers, authentication — and when to pick something else."
---

# Why kiwoom-client

There are two ways to automate Kiwoom Securities from Python: libraries around the older **OpenAPI+ (OCX/COM)**, and
libraries around the newer **Kiwoom REST API**. This page compares the two, and the REST alternatives, on facts.
The right pick depends on what you are building, so read "When to pick something else" too.

## OpenAPI+ (OCX) vs. the REST API

| | OpenAPI+ (OCX/COM) | Kiwoom REST API |
|---|---|---|
| Interface | Windows COM control + event callbacks | HTTPS (JSON) + WebSocket |
| OS | Windows only | Windows, macOS, Linux |
| Python | 32-bit only for a long time, tied to a Qt event loop | 64-bit, plain `asyncio` or threads |
| Servers, Docker, cloud | Hard: needs a GUI session | Headless |
| Login | OpenAPI login window (manual, or auto-login setting) | Token from app key + secret |

Moving to REST lets you run on a Linux server or a Mac without anyone clicking a login window. Some OpenAPI+ features may
not exist in REST yet, so look up the TRs you rely on in the
[Kiwoom REST API guide](https://openapi.kiwoom.com/guide/apiguide) first. What kiwoom-client wraps is listed in the
[endpoint reference](endpoints.md); the OpenAPI+ TR and function mapping is in
[Moving from OpenAPI+ (OCX) and pykiwoom](migration-from-openapi-plus.md).

## Python libraries at a glance

As of 2026-11-21, from PyPI metadata and each project's README. Versions and features change; check each project before
you choose.

### Official, from Kiwoom Securities

| Repository / package | Latest (uploaded) | Python | License | Stated in its README |
|---|---|---|---|---|
| [Kiwoom-Securities/Kiwoom-REST-API](https://github.com/Kiwoom-Securities/Kiwoom-REST-API) · PyPI `kwcli` | `kwcli` 1.0.3 (2026-09) | ≥ 3.13 | Kiwoom's own license (use limited to Kiwoom OpenAPI) | Specs for 337 APIs (Korean **and US** stocks), 362 per-function examples, Postman collection, `kiwoomcli` CLI, two MCP servers (spec search and execution; orders only when explicitly allowed) |

Published by Kiwoom itself, so it is the closest thing to the source of truth for the API, and it covers US stocks. Read
the comparison below knowing that it overlaps with these official tools.

On MCP alone: the official execution server finds and runs commands through a command list (`kiwoom_commands`), help
(`kiwoom_help`) and run (`kiwoom_query`) tools, and ships a `.mcpb` bundle for Claude Desktop. kiwoom-client's MCP server
lists high-level tools that take a stock name (quotes, charts, account, order preview) first in its default mode, finds the
other TRs through `search_tools`, and also ships a `.mcpb` bundle ([MCP server](mcp.md)).

### OpenAPI+ (OCX) wrappers

| Package | Latest (uploaded) | Python | Notes |
|---|---|---|---|
| [pykiwoom](https://github.com/sharebook-kr/pykiwoom) | 0.1.6 (2024-01) | not stated | pywin32 + PyQt5. The most Korean tutorials |
| [KOAPY](https://github.com/elbakramer/koapy) | 0.9.0 (2022-09) | 3.8–3.10 | Calls the OCX remotely through a gRPC server |
| [kiwoom](https://github.com/breadum/kiwoom) | 1.5.0 (2025-08) | 3.8–3.11 | Thin PyQt5 wrapper |

### REST API wrappers

| Package | Latest (uploaded) | Python | License | Features stated in its README |
|---|---|---|---|---|
| **kiwoom-client** (this project) | see PyPI | ≥ 3.10 | MIT | Same sync/async surface, auto token refresh, per-TR rate limiter, real-time WebSocket, MCP server with opt-in live orders |
| [pykiwoom-rest](https://github.com/unohee/pykiwoom-rest) | 2.2.0 (2026-07) | ≥ 3.8 (MCP ≥ 3.10) | MIT | Library + `kiwoom` CLI + MCP server, pandas output |
| [kiwoom-cli](https://github.com/gejyn14/kiwoom-cli) / [kiwoom-mcp](https://github.com/gejyn14/kiwoom-plugin) | 2.14.0 / 0.1.2 (2026-07) | ≥ 3.10 | own license / Apache-2.0 | CLI first. MCP registers order tools only with `--allow-orders`; order pre-check and dry-run |
| [kiwoompy](https://github.com/meonji-gogo/kiwoompy) | 0.1.6 (2026-03) | ≥ 3.12 | MIT | Attribute-style response models (`balance.tot_evlt_amt`), docs site |
| [kiwoom-rest-api](https://pypi.org/project/kiwoom-rest-api/) | 0.1.12 (2025-06) | ≥ 3.9 | not stated | Per-module classes + CLI |

## What kiwoom-client does differently

Only things you can check in the code and tests.

- **Endpoints counted from code.** 182 REST endpoints, 4 condition-search calls and 19 real-time types across 15 modules;
  the [endpoint reference](endpoints.md) is generated from the source, with Kiwoom's own api_id (`ka10001`, ...) next to
  every method.
- **Same surface for sync and async.** `KiwoomAPI` and `AsyncKiwoomAPI` have the same modules and methods, so moving a
  script to `asyncio.gather` is not a rewrite.
- **Defaults for long-running bots.** Tokens refresh before expiry and are reissued on 401. The rate limiter is a per-TR
  token bucket tuned to the measured limit (about 1 req/s, burst 2) and backs off and retries on 429.
- **Agents never see live orders by default.** On the live server the built-in MCP server does **not register** its 12
  order tools until `KIWOOM_MCP_ALLOW_LIVE_ORDERS=true`. On the mock server they are always available.
  If you use Kiwoom's official MCP server or plugin and also want the order *content* checked (amount and quantity caps,
  market buys, repeated submits, daily counts), pair it with the same author's Claude Code hook
  [kiwoom-order-guard](https://github.com/younghwan91/kiwoom-order-guard).
- **Responses you can compute with.** `to_dataframe()` and `to_number()` turn `"+70000"` and `"1,234,567"` into numbers
  and keep codes with meaningful leading zeros as strings. `round_to_tick()` snaps limit prices to KRX ticks.
- **Typed.** Ships `py.typed`; CI runs mypy.

## When to pick something else

- You mainly want a **CLI** to query and trade from the terminal: kiwoom-cli or pykiwoom-rest. kiwoom-client is a library
  plus an MCP server only.
- You want **attribute-style response models**: look at kiwoompy. kiwoom-client returns Kiwoom's JSON as dicts and
  converts on request with `to_dataframe()`.
- You want **tools maintained by Kiwoom itself**, or the **US-stock APIs**: use the [official repository](https://github.com/Kiwoom-Securities/Kiwoom-REST-API) and `kwcli`. kiwoom-client wraps the domestic (Korean) REST API only.
- You depend on something **only OpenAPI+ has**: you may still need an OCX wrapper such as pykiwoom.
- You are on **Python 3.8 or 3.9**: kiwoom-client needs 3.10+.

If you want an MIT-licensed `pip install` library for the domestic REST API with the same sync and async surface, and an
MCP server from the same package, kiwoom-client fits.

The background is in two Korean velog posts: [why the REST client was built](https://velog.io/@younghwan91/%ED%82%A4%EC%9B%80-OCX32bit-%EC%97%86%EC%9D%B4-Python%EC%9C%BC%EB%A1%9C-%EC%9E%90%EB%8F%99%EB%A7%A4%EB%A7%A4-kiwoom-rest-api%EB%A5%BC-%EB%A7%8C%EB%93%A0-%EC%9D%B4%EC%9C%A0) and [guarding live orders from AI agents](https://velog.io/@younghwan91/ai-%EC%97%90%EC%9D%B4%EC%A0%84%ED%8A%B8%EC%97%90%EA%B2%8C-%ED%82%A4%EC%9B%80-%EC%A3%BC%EB%AC%B8%EC%9D%84-%EB%A7%A1%EA%B8%B0%EA%B8%B0-%EC%A0%84%EC%97%90-kiwoom-client-mcp-%EC%84%9C%EB%B2%84%EC%99%80-%EC%8B%A4%EC%A3%BC%EB%AC%B8-%EA%B0%80%EB%93%9C).

If something here is wrong or a project is missing, [open an issue](https://github.com/younghwan91/kiwoom-client/issues)
and it will be fixed.

<small>kiwoom-client is an unofficial open-source project, not affiliated with Kiwoom Securities.</small>
