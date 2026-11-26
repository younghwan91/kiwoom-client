---
seo_title: "Kiwoom REST API convenience helpers — from_env, stock codes, ticks"
description: "kiwoom-client helpers: from_env() from environment variables, stock name ↔ code, official code constants, chart → OHLCV DataFrame, tick math, exception types and a read-only CLI."
---

# Convenience helpers — shorter, without mistakes

Beyond calling the 182 endpoints as they are, these are tools that shorten common tasks and prevent common mistakes.
All of them are **additions** that leave existing behavior unchanged, so code you already have does not need to change.

## Starting from environment variables — `from_env()`

```python
from kiwoom_client import KiwoomAPI

api = KiwoomAPI.from_env(is_mock=True)   # KIWOOM_APP_KEY / KIWOOM_APP_SECRET
api = KiwoomAPI.from_env(".env", is_mock=True)  # also reads a .env file (no new dependency)
```

| Variable | Meaning |
|---|---|
| `KIWOOM_APP_KEY` | App key (required) |
| `KIWOOM_APP_SECRET` | Secret key (required) |
| `KIWOOM_IS_MOCK` | `true` mock trading / `false` live trading |

- The names are the same as the MCP server's, so one `.env` serves both.
- Precedence: the `is_mock=` argument > process environment variables > the `.env` file.
- `KIWOOM_IS_MOCK` accepts only `true/false`, `1/0`, `yes/no`, `on/off`. A typo like `ture` does not fall through to
  live trading; it raises `ValueError`.
- **If it is set nowhere, you connect to the live trading server** (`is_mock=False`, the same default as the constructor
  and the MCP server) and a warning goes to the `kiwoom_client` logger. Pass `is_mock=True` explicitly at first.
- Other arguments (`rate_limit`, `max_retries`, `timeout` ...) are passed through to the constructor.
  `AsyncKiwoomAPI.from_env()` works the same way.

## Stock name ↔ stock code — `find_stock()`

```python
api.find_stock("삼성")        # [{'code': '005930', 'name': '삼성전자', 'marketName': ...}, ...]
api.stock_code("SK하이닉스")   # '000660'
api.stock_list()              # every KOSPI + KOSDAQ stock
```

- It fetches the stock info list (**ka10099**) once per market, all pages, and caches it on the client. `refresh=True`
  fetches again; `cache_ttl=seconds` expires it automatically.
- Order: exact code > exact name > name prefix > code prefix > part of the name. Case and whitespace are ignored.
- `stock_code()` returns a code only when the name matches exactly one stock; otherwise it raises `LookupError` with
  the candidates.
- Other markets: `markets=[StockListMarket.ETF]` (see the code constants below).

## Code constants — `kiwoom_client.codes`

Kiwoom takes options as short strings, and the same field name uses different codes in different TRs. With named
constants, typos show up right away. They are all `str`, so passing one sends the original code value.

```python
from kiwoom_client import Exchange, OrderType

api.order.buy_order(
    dmst_stex_tp=Exchange.KRX, stk_cd="005930", ord_qty="10",
    ord_uv="70000", trde_tp=OrderType.LIMIT,   # "0" normal (limit)
)
```

| Constant | Field | Values |
|---|---|---|
| `Exchange` | order `dmst_stex_tp` | `KRX` · `NXT` · `SOR` |
| `OrderType` | order `trde_tp` | `LIMIT`="0", `MARKET`="3", `STOP_LIMIT`="28" and others, 18 in all |
| `QueryExchange` | query `stex_tp` | `KRX`="1", `NXT`="2", `ALL`="3" (combined) |
| `Market` | ranking and stock TRs `mrkt_tp` | `ALL`="000", `KOSPI`="001", `KOSDAQ`="101" |
| `StockListMarket` | ka10099 `mrkt_tp` | `KOSPI`="0", `KOSDAQ`="10", `ETF`="8" and others, 16 in all |
| `AdjustedPrice` | chart `upd_stkpc_tp` | `RAW`="0", `ADJUSTED`="1" |
| `PriceChangeSign` | response `pred_pre_sig` | 1 upper limit · 2 up · 3 unchanged · 4 lower limit · 5 down |

`exchange_stock_code("005930", Exchange.NXT)` builds the per-exchange code `"005930_NX"` that quote and chart TRs take
(`_AL` for SOR). Only values confirmed per TR in the
[Kiwoom REST API guide](https://openapi.kiwoom.com/guide/apiguide) are included.

## Chart → OHLCV DataFrame — `to_ohlcv()`

```python
from kiwoom_client import to_ohlcv

resp = api.chart.stock_daily_chart(stk_cd="005930", base_dt="20260327", upd_stkpc_tp="1")
df = to_ohlcv(resp)   # open/high/low/close/volume, DatetimeIndex, oldest first
```

- It takes tick, minute, daily, weekly, monthly and yearly bars for stocks, sectors and gold spot. A list from
  `request_all()` works too.
- The `+`/`-` in front of minute and tick bar prices is the change direction, not a negative number, so it is removed.
- If you also need other fields, such as trading value, use `keep=["trde_prica"]` (the unit differs by TR: millions of
  won for daily bars, won for weekly and monthly bars).
- Sector index values are exactly as Kiwoom sends them (with the decimal point removed).
- Needs pandas: `pip install 'kiwoom-client[pandas]'`. If you need every original field, use the existing
  `to_dataframe()`.

## Tick math — `add_ticks()` · `ticks_between()`

```python
from kiwoom_client import add_ticks, is_on_tick, round_up_to_tick, ticks_between

add_ticks(49_950, 2)           # Decimal('50100') — at the 50,000 won boundary the tick goes from 50 to 100
add_ticks(2_000, -1)           # Decimal('1999')  — not 1995
ticks_between(49_900, 50_100)  # 3
round_up_to_tick(70_101)       # Decimal('70200') — the round-up version of round_to_tick()
is_on_tick(70_150)             # False
```

When you set a stop-loss or take-profit "N ticks below/above", this keeps you from going wrong at band boundaries. A
value that is not a valid quote price raises `ValueError`. The results of the existing `tick_size()` ·
`round_to_tick()` · `ticks_in()` have not changed.

## Exceptions — what went wrong, by type

```python
from kiwoom_client import KiwoomAPIError, KiwoomRateLimitError, KiwoomServerMismatchError

try:
    api.stock_info.basic_stock_info(stk_cd="005930")
except KiwoomServerMismatchError as e:   # mock/live key mismatch (8030/8031)
    print(e.hint)                        # which is_mock matches the server you are connected to
except KiwoomRateLimitError:             # limit exceeded — even after automatic retries
    ...
except KiwoomAPIError as e:              # any other return_code != 0 (same as before)
    print(e.code, e.error_code, e.message)
```

```
KiwoomError
├── KiwoomAuthError              token issue / revoke failed
├── KiwoomWebSocketError         WebSocket login / protocol failure
└── KiwoomAPIError               return_code != 0
    ├── KiwoomTokenError         token rejected (return_code 3)
    │   └── KiwoomServerMismatchError  mock/live mismatch
    ├── KiwoomRateLimitError     rate limit exceeded (return_code 5)
    ├── KiwoomRequestError       parameter / header error
    │   └── KiwoomStockNotFoundError  no such stock code
    └── KiwoomUnsupportedError   API not supported for mock trading / corporate accounts
```

- The finer-grained exceptions are all `KiwoomAPIError`, so an existing `except KiwoomAPIError` still catches them.
  `code` · `message` · `response` are unchanged too.
- `error_code` is the 4-digit code inside `return_msg` (`[8005:...]`).
- For errors with a known cause, the second line of `str(e)` carries a `힌트:` (hint) line (`e.hint`). Token issue
  failures (`KiwoomAuthError`) do the same.

## Command line — `kiwoom`

```bash
kiwoom quote 005930 --mock        # current price (a stock name works too: kiwoom quote 삼성전자)
kiwoom chart 005930 --daily -n 10 # --weekly --monthly --yearly --minute --tick
kiwoom balance --mock             # account evaluation balance (kt00018)
kiwoom find 하이닉스 --mock
kiwoom endpoints 체결             # find method ↔ TR (no keys needed)
kiwoom --json quote 005930        # the raw response JSON
kiwoom --demo quote 005930        # synthetic data with no key (connects nowhere)
```

Keys are read from environment variables, like `from_env()`, and `--env-file` points to a `.env`. `--mock`/`--live`
take precedence over `KIWOOM_IS_MOCK`.
`--demo` needs no key: it uses the [demo backend](mcp.md#demo-mode-try-it-without-a-key) and prints a `[데모] 가상 데이터`
("demo, synthetic data") banner as the first line (on stderr with `--json`). The prices are not real.
**It only queries** — there are deliberately no commands for orders or token revocation. `python -m kiwoom_client`
runs it too.

## Debugging — repr · logs · timeout

```python
print(api)
# KiwoomAPI(server='mock', base_url='https://mockapi.kiwoom.com', app_key='****AbCd', token='set')
```

- `print(api)` shows right away which server you are connected to. Not even part of the secret key or token is shown.
- Request tracing: `logging.getLogger("kiwoom_client").setLevel(logging.DEBUG)` — logs the api-id, HTTP status,
  return_code, retries and token reissues, but not headers (the token) or bodies (account numbers).
- `KiwoomAPI(..., timeout=10.0)` — the HTTP timeout (seconds or an `httpx.Timeout`). The default is 30 seconds.
