<!-- 자동 생성 파일 — scripts/templates/AGENTS.md (와 usage-rules.md) 를 고치고 `python scripts/gen_docs.py` 로 다시 만듭니다. -->

# AGENTS.md

Instructions for AI coding agents (Codex, Claude Code, Cursor, Copilot, …) that **use** kiwoom-client in
someone's code, or **work on** this repository. Humans: see [README](README.md) and [CONTRIBUTING](CONTRIBUTING.md).

kiwoom-client is a Python client for the Kiwoom Securities (키움증권) REST API and WebSocket —
182 REST endpoints, 4 condition-search calls, 19 real-time types. It can place **real orders on a real
brokerage account**, so the safety rules below come first.

## Writing code that uses kiwoom-client

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

Where to look things up:

| Need | Look here |
|---|---|
| Method for an api_id (`ka10081`) or a Korean TR name (`주식일봉차트조회요청`) | [`docs/endpoints.md`](docs/endpoints.md) |
| Request/response fields of a TR | `kiwoom_client.spec.get("ka10081")`, `spec.search("일봉")`, `spec.for_method("chart", "stock_daily_chart")`, or [Kiwoom's guide](https://openapi.kiwoom.com/guide/apiguide) |
| Every public signature and docstring in one file | [`llms-full.txt`](llms-full.txt) |
| Coming from OpenAPI+ (OCX) / pykiwoom (`opt10001`, `SendOrder`, `SetRealReg`) | [`docs/migration-from-openapi-plus.md`](docs/migration-from-openapi-plus.md) |
| Using it as MCP tools instead of Python | README, "MCP 서버로 사용하기" / "MCP server" |

A safe starting point (paper trading, keys from the environment):

```python
from kiwoom_client import KiwoomAPI, to_dataframe

api = KiwoomAPI.from_env(is_mock=True)
resp = api.chart.stock_daily_chart(stk_cd="005930", base_dt="20260326", upd_stkpc_tp="1")
df = to_dataframe(resp)
```

## Working on this repository

[CONTRIBUTING.md](CONTRIBUTING.md) has the full rules. The ones an agent is most likely to break:

- **No live servers, no real keys.** Unit tests mock HTTP with `pytest-httpx`; never send requests to
  `api.kiwoom.com` or `mockapi.kiwoom.com`. Do not run `tests/integration_*_smoke.py` (live-server scripts, not
  collected by pytest) or `examples/*.py`, and never call `logout()` / `revoke_token`.
- **Add, don't change.** Trading daemons install new releases automatically (`kiwoom-client>=…`). Keep
  `request()` / `request_all()`, token issue/refresh, the rate limiter, `tick_size` / `round_to_tick` results, the
  `is_mock=False` default and existing method signatures exactly as they are. New behaviour goes behind a new
  function or an option whose default is the old behaviour.
- **Never weaken the live-order guards**: the MCP opt-in (`KIWOOM_MCP_ALLOW_LIVE_ORDERS`,
  `src/kiwoom_client/mcp/guard.py`, `GUARDED_MODULES`) and `.claude/hooks/live_order_guard.py`. If a guard blocks
  you, show the command to the user instead of working around it.
- **Generated files** — after changing endpoints, docstrings or `__all__`, regenerate and commit them together;
  CI compares them with the code:
  `python scripts/gen_docs.py` (docs/endpoints.md, llms.txt, llms-full.txt, AGENTS.md, the skill, Cursor/Copilot rules) and
  `python scripts/build_stubs.py` (`domestic/*.pyi`).
- **Docs code is tested**: Python blocks must compile, `api.<module>.<method>(` and api_ids must exist, and
  examples under `docs/` must build clients with `is_mock=True` (`tests/test_docs_code_blocks.py`).
- Public repository: no account numbers, keys or e-mail addresses in code, docs or commits. Do not bump the
  version, tag or publish — releases are the maintainer's.

Adding an endpoint: one method on the module class in `src/kiwoom_client/domestic/` with the docstring
`"한글 TR 이름 (English name)"`, a mocked test in `tests/test_modules.py`, then regenerate. The MCP tool
(`<module>_<method>`) appears on its own.

```bash
uv run --extra dev --extra mcp pytest tests/ -q
uv run --extra dev --extra mcp ruff check src tests examples
uv run --extra dev --extra mcp mypy
```
