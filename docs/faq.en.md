# FAQ

## Getting started

**Q. Is this Kiwoom's official library?**
No. It is an open-source (MIT) client unaffiliated with Kiwoom Securities. It wraps Kiwoom's published REST API as is,
and field names and codes follow Kiwoom's official documentation and spec.

**Q. Where do I get an app key?**
Apply for API use on the [Kiwoom REST API portal](https://openapi.kiwoom.com) to get an app key and secret.
**Paper-trading (모의투자) and live (실전투자) keys are different keys.**

**Q. What should I do first?**
Start with a paper-trading key.

```python
from kiwoom_client import KiwoomAPI

api = KiwoomAPI.from_env(is_mock=True)  # KIWOOM_APP_KEY / KIWOOM_APP_SECRET
print(api.stock_info.basic_stock_info(stk_cd="005930")["stk_nm"])
```

`is_mock` defaults to `False` (the live server). Forgetting it with a paper key gives error 8030/8031 —
see [Troubleshooting](troubleshooting.md).

**Q. Does it need Windows or 32-bit Python?**
No. It is REST, so it runs on Windows, macOS and Linux with 64-bit Python 3.10+. There is no OCX or login window, so it
runs on servers and in containers.

**Q. How do I port OpenAPI+ (KOA Studio) / pykiwoom code?**
What `opt10081`-style TRs, `SendOrder` and `SetRealReg` become in REST is in
[Migrating from OpenAPI+ (Korean)](migration-from-openapi-plus.md).

## Usage

**Q. How do I find the method for a TR (api_id)?**
Search the [endpoint reference](endpoints.md) for the api_id (`ka10081`) or the Korean TR name. In code:

```python
from kiwoom_client import spec

print([(t.api_id, t.name) for t in spec.search("일봉")])
print(spec.get("ka10081").required_fields)  # required request fields
```

**Q. How do I pass request fields?**
As keyword arguments named exactly like Kiwoom's fields, with **string** values (`stk_cd="005930"`, `ord_qty="10"`).
Field lists are in the [field reference](reference/index.md) and `kiwoom_client.spec`; common coded values have names in
`kiwoom_client.codes` (`OrderType.LIMIT`, `Exchange.KRX`, …).

**Q. Every value in the response is a string.**
That is how Kiwoom sends them (`"+70000"`, `"1,234"`). Convert with `to_dataframe()` / `normalize()` / `to_number()`;
stock codes and dates stay strings.

**Q. Sync (`KiwoomAPI`) or async (`AsyncKiwoomAPI`)?**
Sync for simple scripts. Async when calling different TRs concurrently or alongside the WebSocket —
[asyncio recipe (Korean)](cookbook/async-concurrency.md).

**Q. What about continuation (next page)?**
If the response's `"cont-yn"` is `"Y"`, call again with `cont_yn="Y", next_key=resp["next-key"]`, or use
`request_all()` — [pagination recipe (Korean)](cookbook/pagination.md).

**Q. Do I need to manage the token?**
No. It is issued on the first call, refreshed before it expires, and reissued (with one retry) if rejected. Measured on the
live server, a token lasted about 18 hours, and reissuing within that time returned the same token (0.2.1 changelog).

**Q. Should I call `api.logout()`?**
No need. `logout()` **revokes** the token, which can cut off other programs using the same app key. To just close
connections, use `api.close()` or a `with` block.

**Q. Rate limits?**
Kiwoom limits each TR (api_id) separately. The client paces each TR at 1 request/s with a burst of 2 and retries on 429 —
[rate-limit recipe (Korean)](cookbook/rate-limits.md).

**Q. NXT / SOR?**
Put `KRX`, `NXT` or `SOR` in the order field `dmst_stex_tp`. Quote and chart TRs take stock codes like `005930_NX` /
`005930_AL` per the official spec; `kiwoom_client.codes.exchange_stock_code("005930", "NXT")` builds them. Paper trading
supports KRX only.

**Q. Overseas stocks?**
This library wraps the domestic-stock API only (182 REST endpoints + condition search + real-time). Gold-spot quote and
order TRs are included.

## Orders and safety

**Q. Is it safe to run order code?**
With `is_mock=True` it talks to the paper-trading server and nothing really fills. With `is_mock=False` (the default),
`api.order.*` and `api.credit_order.*` **place real orders on a real account.** Nothing in the Python API blocks them, so
add your own quantity/price checks before going live.

**Q. My limit order is rejected.**
A price that is not a multiple of the tick size is rejected or repriced. Use `round_to_tick()` —
[limit-order recipe (Korean)](cookbook/limit-order.md).

## AI agents and MCP

**Q. Can I use it from Claude Code or Cursor?**
Two ways: ① the MCP server (`pip install 'kiwoom-client[mcp]'`, `kiwoom-client-mcp`) exposes the endpoints as tools;
② rules and a skill that help an AI write code with this library (`llms.txt`, `AGENTS.md`, a Claude Code skill, Cursor and
Copilot rules) — [Using it from AI coding tools](ai-tools.md).

**Q. Can an AI place live orders through MCP on its own?**
On a live account (`KIWOOM_IS_MOCK=false`) the order tools are **not even registered** until you set
`KIWOOM_MCP_ALLOW_LIVE_ORDERS=true` yourself. In paper trading they are always available.

## Other

**Q. Does it work without pandas?**
Yes. Only `to_dataframe()` needs pandas (`pip install 'kiwoom-client[pandas]'`).

**Q. Where do bugs and requests go?**
[GitHub Issues](https://github.com/younghwan91/kiwoom-client/issues). Remove keys and account numbers first.
