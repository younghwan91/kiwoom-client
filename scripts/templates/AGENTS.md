# AGENTS.md

Instructions for AI coding agents (Codex, Claude Code, Cursor, Copilot, …) that **use** kiwoom-client in
someone's code, or **work on** this repository. Humans: see [README](README.md) and [CONTRIBUTING](CONTRIBUTING.md).

kiwoom-client is a Python client for the Kiwoom Securities (키움증권) REST API and WebSocket —
$n_rest REST endpoints, $n_cs condition-search calls, $n_rt real-time types. It can place **real orders on a real
brokerage account**, so the safety rules below come first.

## Writing code that uses kiwoom-client

$usage_rules

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
  `python scripts/gen_docs.py` (docs/endpoints.md, llms.txt, llms-full.txt, AGENTS.md) and
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
