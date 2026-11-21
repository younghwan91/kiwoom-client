# Troubleshooting

Common errors and how to fix them. Error-code meanings are summarised from Kiwoom's official
[REST API guide](https://openapi.kiwoom.com/guide/apiguide) ("오류코드") and the official
[REST API spec](https://github.com/Kiwoom-Securities/Kiwoom-REST-API).

## First: what to read on the exception

```python
from kiwoom_client import KiwoomAPI, KiwoomAPIError

api = KiwoomAPI.from_env(is_mock=True)
try:
    api.stock_info.basic_stock_info(stk_cd="005930")
except KiwoomAPIError as e:
    print(type(e).__name__)  # a cause-specific subclass such as KiwoomServerMismatchError
    print(e.code)            # return_code from the payload (3, 5, ...)
    print(e.error_code)      # Kiwoom's 4-digit code inside return_msg ("[8005:...]" -> 8005), or None
    print(e.message)         # return_msg as sent
    print(e.hint)            # a one-line next step added by the library, or None
```

Kiwoom's `return_code` is coarse (3, 5, …); the **real cause is inside `return_msg`** as `[8005:…]`. Look at `e.error_code`
and the exception class. The hierarchy lives in `kiwoom_client.errors`; every class is a `KiwoomAPIError`, so existing
`except KiwoomAPIError` blocks still catch them.

## Authentication and tokens

### Paper key on the live server, or the reverse — 8030 / 8031

`KiwoomServerMismatchError`. Paper-trading (모의투자) and live (실전투자) keys are **different keys** for different servers.

| | `is_mock` | Server |
|---|---|---|
| Paper key | `True` | `mockapi.kiwoom.com` |
| Live key | `False` (default) | `api.kiwoom.com` |

- `KiwoomAPI(...)` defaults to `is_mock=False`. With a paper key, always pass `is_mock=True`.
- `from_env()` reads `KIWOOM_IS_MOCK`; when it is unset it connects to the live server and logs a warning.
- 8030 is about the app key, 8031 about the token.

### App key / secret rejected — 8001 / 8002

The key is wrong (stray spaces or quotes are common) or the key kind does not match `is_mock`. Re-check the key on the
[Kiwoom REST API portal](https://openapi.kiwoom.com).

### Invalid token — 8005 (`return_code` 3)

The library **reissues the token and retries once by itself.** Kiwoom answers an expired or invalid token with HTTP 200 and
`return_code: 3`, not HTTP 401 (handled since 0.2.1). If `KiwoomTokenError` still comes back:

- another program may have revoked the token of the same app key (`api.logout()` / token revocation) — do not call
  `logout()` on a shared key;
- check that the key kind and `is_mock` match.

### Token used from a different IP — 8010

The token was issued in one place and used from another server or container, or the outgoing IP changes behind a proxy/NAT.
Let each place issue its own token (the default behaviour).

### Token issuance fails — `KiwoomAuthError`

The `/oauth2/token` request failed over HTTP or the reply had no token; the message carries Kiwoom's `return_msg`.
Check the network (firewall, DNS) and the key.

## Rate limits — HTTP 429, `return_code` 5, 1700 / 1701 / 1702

`KiwoomRateLimitError`, or `httpx.HTTPStatusError` if HTTP 429 survives the retries. The client already paces each TR and
retries, so this usually means **several processes call the same TR with the same app key**. See the
[rate-limit recipe (Korean)](cookbook/rate-limits.md).

## Request fields and stock codes

| Code | Meaning | Exception | What to do |
|---|---|---|---|
| 1511 | a required field is empty | `KiwoomRequestError` | `kiwoom_client.spec.get(api_id).required_fields` |
| 1517 | a value has the wrong format | `KiwoomRequestError` | send strings (`ord_qty="10"`), dates as `YYYYMMDD`, coded values from `kiwoom_client.codes` |
| 1504 · 1505 | API ID not served at that URL / unknown API ID | `KiwoomRequestError` | cannot happen through the methods; check URL + api_id if you call `request()` yourself |
| 1901 · 1902 · 1903 | no market code / no such stock | `KiwoomStockNotFoundError` | check the 6-digit code; NXT/SOR use `005930_NX` / `005930_AL` (`codes.exchange_stock_code`) |

Unknown field names and missing required fields can be caught before sending (checked against the official spec catalog,
with close-match suggestions):

<!-- docs-test: skip -->
```python
from kiwoom_client import KiwoomAPI

api = KiwoomAPI.from_env(is_mock=True, validate_params="warn")  # "error": raise KiwoomParamError, send nothing
api.chart.stock_daily_chart(stk_cd="005930", base_date="20260326")  # warns: base_date (correct: base_dt)
```

## Paper trading and account types

- **8104** API not offered on the paper-trading server — `KiwoomUnsupportedError`; live server only.
- **8200** API not offered to corporate customers — `KiwoomUnsupportedError`.
- Paper-trading orders accept exchange `KRX` only (`dmst_stex_tp="KRX"`).

## Orders

- **A limit order is rejected or fills at another price**: `ord_uv` is not a multiple of the tick size. Use
  `round_to_tick()` / `add_ticks()` — [limit-order recipe (Korean)](cookbook/limit-order.md).
- **Numbers passed as numbers**: every Kiwoom field is a string — `ord_qty="10"`, `ord_uv=str(price)`.
- **Order tools missing in MCP**: by design. On a live account (`KIWOOM_IS_MOCK=false`) they are not registered until
  `KIWOOM_MCP_ALLOW_LIVE_ORDERS=true`.

## Responses

- **`to_dataframe()` raises ImportError**: install pandas — `pip install 'kiwoom-client[pandas]'`.
- **Numbers stay strings**: `to_number()` / `normalize()` deliberately keep zero-padded values (`"005930"`) and fields ending
  in `_cd`, `_dt`, `_no`, `_nm` as strings. If an amount arrives zero-padded, convert it with `int()` yourself.
- **Prices are negative**: the sign on Kiwoom quotes is the direction versus the previous close. Use `abs()` for a price.
- **Continuation stops after page one**: a bug before 0.4.0 (Kiwoom sends the continuation flags as response headers).
  Upgrade.

## WebSocket

- **`connect()` raises `KiwoomWebSocketError`**: the LOGIN reply was a failure; read its `return_msg` and check the token
  and `is_mock`.
- **"서버가 LOGIN 응답 없이 연결을 종료했습니다" (closed before the LOGIN reply)**: seen on rapid reconnects. Wait and retry.
- **Callbacks never fire**: subscribe after `connect()`, keep `listen()` running, and register `ws.on()` with the same type
  code you subscribed (`"0B"`). Nothing trades while the market is closed. `ws.on_message()` shows every frame.
- **`RuntimeError: WebSocket not connected`**: `await ws.connect()` before `send()` / `listen()`.

## Install and import

- **`ModuleNotFoundError: kiwoom_rest_api`**: the import name became `kiwoom_client` in 0.3.0.
- **Python 3.9 or older**: 3.10+ is required.

Anything else: open an [issue](https://github.com/younghwan91/kiwoom-client/issues) — with keys and account numbers removed.
