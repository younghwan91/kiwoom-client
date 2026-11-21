---
name: kiwoom-client
description: Write, run and debug Python code that uses kiwoom-client, the client for the Kiwoom Securities (키움증권) REST API and WebSocket — quotes, daily/minute charts, rankings, account balances, orders, condition search (조건검색) and real-time data. Use when code imports kiwoom_client, when the user mentions Kiwoom or 키움 REST API, a TR code such as ka10081 or kt10000, or moving code from OpenAPI+/KOA Studio/pykiwoom to REST.
---

<!-- 자동 생성 파일 — scripts/templates/SKILL.md (와 usage-rules.md) 를 고치고 `python scripts/gen_docs.py` 로 다시 만듭니다. -->

# kiwoom-client

`kiwoom-client` (`pip install kiwoom-client`, import `kiwoom_client`) wraps the Kiwoom Securities REST API:
182 REST endpoints as methods on `api.<module>`, 4 condition-search calls and 19 real-time types over
one WebSocket, with automatic token refresh, per-TR rate limiting and string-to-number parsing.

**It can place real orders on a real brokerage account.** Read the rules before writing any call.

## Rules

- `KiwoomAPI(app_key, app_secret, is_mock=False)` — **`is_mock` defaults to `False`, the live server.** Pass `is_mock=True` for paper trading (모의투자, mockapi.kiwoom.com). Live and paper keys are different; a key used against the wrong server is rejected (Kiwoom error 8030/8031, raised as `KiwoomServerMismatchError`).
- `KiwoomAPI.from_env(is_mock=True)` reads `KIWOOM_APP_KEY` / `KIWOOM_APP_SECRET` / `KIWOOM_IS_MOCK` (the same variables as the MCP server). Never hard-code or print keys.
- `api.order.*` and `api.credit_order.*` place **real, irreversible orders** when `is_mock=False`. Nothing in the Python API blocks them; only the MCP server has an opt-in guard (`KIWOOM_MCP_ALLOW_LIVE_ORDERS`). Do not run order code against a live account unless the user explicitly asks.
- `api.logout()` revokes the access token. Other processes sharing the same app key may lose their session — do not call it casually.
- Every REST method has the same signature `(cont_yn="N", next_key="", **fields)`. Pass Kiwoom's own request field names as keyword arguments with **string** values (`stk_cd="005930"`, `ord_qty="10"`). Find the method for an api_id (`ka10081`) or a Korean TR name in the endpoint reference; look fields up with `kiwoom_client.spec.get("ka10081").required_fields` or Kiwoom's guide. Do not invent method names.
- Coded fields have named constants in `kiwoom_client.codes` (`OrderType.LIMIT`, `Exchange.KRX`, …).
- Responses are plain dicts whose values are strings (`"+70000"`, `"1,234"`). `to_dataframe()` / `normalize()` / `to_number()` convert them; codes and dates stay strings. A non-zero `return_code` raises `KiwoomAPIError(code, message, response)` or one of its subclasses in `kiwoom_client.errors`.
- Continuation: a response carries `"cont-yn"` and `"next-key"`; call again with `cont_yn="Y", next_key=...`, or use `api._client.request_all(url, api_id, body)`.
- Rate limits are per api_id (about 1 req/s, burst 2) and handled by the client; different api_ids run concurrently under `AsyncKiwoomAPI`.
- Limit prices must be on the KRX tick grid: `round_to_tick(price)`.
- Real-time: `ws = api.create_websocket()`, `await ws.connect()`, `ws.on("0B", cb)`, `await ws.subscribe("0B", "005930")`, `await ws.listen()`. `values` keys are Kiwoom FID numbers (`"10"` = current price).

## Workflow

1. **Find the method.** Search [endpoints.md](endpoints.md) (next to this file) for the api_id (`ka10081`), the
   Korean TR name (`일봉`) or a method name. Or ask the installed package:
   `python -c "from kiwoom_client import spec; print([(t.api_id, t.name) for t in spec.search('일봉')])"`.
2. **Get the fields.** `spec.get("ka10081").required_fields` lists the required ones,
   `[f.id for f in spec.get("ka10081").request_fields]` all of them, and
   `spec.get("ka10081").request_field("upd_stkpc_tp")` gives one field's `desc` and `codes`.
   Kiwoom's guide is the authority when a meaning is unclear.
3. **Build the client in paper-trading mode**: `KiwoomAPI.from_env(is_mock=True)` with the key in
   `KIWOOM_APP_KEY` / `KIWOOM_APP_SECRET`. Switch to the live server only when the user says so.
4. **Call, then parse**: pass fields as string keyword arguments; turn the response into numbers with
   `to_dataframe()` / `normalize()`.
5. **Handle errors** by class: `KiwoomServerMismatchError` (paper vs live key), `KiwoomRateLimitError`,
   `KiwoomRequestError` (bad fields), `KiwoomStockNotFoundError`, `KiwoomTokenError` — all subclasses of
   `KiwoomAPIError`.

## Examples

Daily candles as a DataFrame:

```python
from kiwoom_client import KiwoomAPI, to_dataframe

api = KiwoomAPI.from_env(is_mock=True)
resp = api.chart.stock_daily_chart(stk_cd="005930", base_dt="20260326", upd_stkpc_tp="1")
df = to_dataframe(resp)  # finds the record list, converts "+70000" -> 70000
```

Every page of a continued query:

```python
from kiwoom_client import KiwoomAPI, extract_records

api = KiwoomAPI.from_env(is_mock=True)
fields = {"stk_cd": "005930", "base_dt": "20260326", "upd_stkpc_tp": "1"}
rows, cont_yn, next_key = [], "N", ""
while True:
    resp = api.chart.stock_daily_chart(cont_yn=cont_yn, next_key=next_key, **fields)
    rows += extract_records(resp)[1]
    if resp.get("cont-yn") != "Y" or not resp.get("next-key"):
        break
    cont_yn, next_key = "Y", resp["next-key"]
```

Different TRs at the same time (asyncio):

```python
import asyncio

from kiwoom_client import AsyncKiwoomAPI


async def main():
    async with AsyncKiwoomAPI.from_env(is_mock=True) as api:
        info, quote = await asyncio.gather(
            api.stock_info.basic_stock_info(stk_cd="005930"),
            api.market.stock_quote(stk_cd="005930"),
        )
        print(info["stk_nm"])


asyncio.run(main())
```

A limit order on the tick grid (paper trading):

```python
from kiwoom_client import KiwoomAPI, round_to_tick
from kiwoom_client.codes import Exchange, OrderType

api = KiwoomAPI.from_env(is_mock=True)
result = api.order.buy_order(
    dmst_stex_tp=Exchange.KRX, stk_cd="005930", ord_qty="1",
    ord_uv=str(round_to_tick(70123)), trde_tp=OrderType.LIMIT,
)
print(result["ord_no"])
```

Real-time trades:

```python
import asyncio

from kiwoom_client import KiwoomAPI


async def main():
    api = KiwoomAPI.from_env(is_mock=True)
    ws = api.create_websocket()
    await ws.connect()
    ws.on("0B", lambda d: print(d["item"], d["values"].get("10")))  # FID 10 = 현재가
    await ws.subscribe("0B", ["005930", "000660"])
    await ws.listen()


asyncio.run(main())
```

## References

- Endpoint list: [endpoints.md](endpoints.md) (this skill) ·
  [docs/endpoints.md](https://github.com/younghwan91/kiwoom-client/blob/main/docs/endpoints.md)
- All public signatures and docstrings: [llms-full.txt](https://raw.githubusercontent.com/younghwan91/kiwoom-client/main/llms-full.txt)
- From OpenAPI+ / pykiwoom: [migration guide](https://github.com/younghwan91/kiwoom-client/blob/main/docs/migration-from-openapi-plus.md)
- Kiwoom's own field definitions: [REST API guide](https://openapi.kiwoom.com/guide/apiguide)
