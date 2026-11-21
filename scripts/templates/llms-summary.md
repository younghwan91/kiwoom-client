# kiwoom-client

> Python client for the Kiwoom Securities (키움증권) REST API and real-time WebSocket: $n_rest REST endpoints, $n_cs condition-search calls and $n_rt real-time types, sync (`KiwoomAPI`) and asyncio (`AsyncKiwoomAPI`) facades, automatic token refresh, per-TR rate limiting, response parsing to numbers/DataFrames, KRX tick sizes, and a built-in MCP server. REST, not OCX/COM — runs on Windows, macOS and Linux.

Install `pip install kiwoom-client` (extras `[pandas]`, `[mcp]`), Python 3.10+, import name `kiwoom_client`. Keys come from the Kiwoom REST API portal (https://openapi.kiwoom.com).

Rules for writing code against this library:

$usage_rules
