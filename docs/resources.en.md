---
seo_title: "Kiwoom REST API resources — official guide, spec, community"
description: "Links for using the Kiwoom Securities REST API from Python or AI agents: Kiwoom's official guide and spec, MCP material, public market data and community, with sources."
---

# Resources

Links you keep coming back to when using the Kiwoom REST API from Python or AI agents. The official material belongs to
Kiwoom Securities; everything else is labelled with its source. Report a broken link or suggest one in
[Issues](https://github.com/younghwan91/kiwoom-client/issues).

## Kiwoom Securities (official)

| Resource | What you find there |
|---|---|
| [Kiwoom REST API portal](https://openapi.kiwoom.com) | Apply for API access, issue the app key and secret, notices |
| [REST API guide](https://openapi.kiwoom.com/guide/apiguide) | Request and response fields per api_id (`ka10001`, ...). This library's keyword arguments use the same names |
| [Kiwoom-REST-API (GitHub)](https://github.com/Kiwoom-Securities/Kiwoom-REST-API) | Kiwoom's official repository: API specs, example code, Postman collection, MCP servers. The CLI is `kwcli` on PyPI |

- Live (실전투자) and mock (모의투자) keys are issued separately and are rejected by the other server; match `is_mock`.
- The mock server supports KRX only.

## kiwoom-client docs

| Resource | What you find there |
|---|---|
| [README](https://github.com/younghwan91/kiwoom-client/blob/main/README.en.md) | Install, quick start, accounts and orders, asyncio, WebSocket, pagination, rate limits, MCP server |
| [Endpoint reference](endpoints.md) | api_id, Korean TR name and URL for all 182 methods; condition search; real-time types |
| [Why kiwoom-client](why.md) | Comparison with OpenAPI+, pykiwoom and other REST wrappers |
| [examples/](https://github.com/younghwan91/kiwoom-client/tree/main/examples) | Example scripts against the mock server |
| [llms.txt](https://raw.githubusercontent.com/younghwan91/kiwoom-client/main/llms.txt) · [llms-full.txt](https://raw.githubusercontent.com/younghwan91/kiwoom-client/main/llms-full.txt) | Summary and full API text to paste into AI coding tools |
| [CHANGELOG](https://github.com/younghwan91/kiwoom-client/blob/main/CHANGELOG.md) | Changes per release |

## MCP and AI agents

| Resource | What you find there |
|---|---|
| [Model Context Protocol](https://modelcontextprotocol.io) | The MCP specification and concepts |
| [Claude Code — MCP](https://code.claude.com/docs/en/mcp) | Registering a server with `claude mcp add` |
| [Cursor — MCP](https://docs.cursor.com/context/model-context-protocol) | Cursor's `mcp.json` |
| [MCP Registry](https://registry.modelcontextprotocol.io) | Public MCP servers |

## Korean market data (public)

| Resource | What you find there |
|---|---|
| [KRX Data Marketplace](https://data.krx.co.kr) | Listings, indices, trading by investor type |
| [DART Open API](https://opendart.fss.or.kr) | Corporate filings and financial statements (Financial Supervisory Service) |

## Community

- [GitHub `kiwoom` topic](https://github.com/topics/kiwoom): open-source projects around Kiwoom
- Questions and bug reports: [kiwoom-client Issues](https://github.com/younghwan91/kiwoom-client/issues)

<small>kiwoom-client is an unofficial open-source project, not affiliated with Kiwoom Securities. The Kiwoom links above are for convenience; Kiwoom's own site is the source of truth.</small>
