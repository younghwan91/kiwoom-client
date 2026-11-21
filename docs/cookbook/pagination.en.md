# Paging through a continuation query

A TR whose results do not fit in one response marks that there is a next page — a continuation query (연속조회).
Kiwoom sends the marker in the **response headers** (`cont-yn`, `next-key`), and kiwoom-client copies those values into
the response dict under the keys `"cont-yn"` · `"next-key"`.

- If `resp["cont-yn"] == "Y"`, there is another page.
- Send the next request with the same fields plus `cont_yn="Y", next_key=resp["next-key"]`.
- Since you call the same TR back to back, the default rate limiter (1 request per second per TR, burst 2) paces the
  calls.

## Looping yourself — stop at the date you want

This example fetches daily bars back to `2020-01-01`.

```python
from kiwoom_client import KiwoomAPI, extract_records

api = KiwoomAPI.from_env(is_mock=True)

fields = {"stk_cd": "005930", "base_dt": "20260326", "upd_stkpc_tp": "1"}
rows: list[dict] = []
cont_yn, next_key = "N", ""
while True:
    resp = api.chart.stock_daily_chart(cont_yn=cont_yn, next_key=next_key, **fields)
    _, page = extract_records(resp)  # (list key, records)
    rows += page
    if not page or min(r["dt"] for r in page) <= "20200101":
        break  # reached the date we wanted
    if resp.get("cont-yn") != "Y" or not resp.get("next-key"):
        break  # nothing more
    cont_yn, next_key = "Y", resp["next-key"]

rows = [r for r in rows if r["dt"] >= "20200101"]
print(len(rows), "days")
```

## `request_all()` — all pages in one call

If the stopping condition is "until the end", the low-level client's `request_all()` does the same job. Give it the
list key (`data_key`) and it returns a single list, the lists from every page joined together. As a safeguard it stops
at `max_pages` (default 100).

```python
from kiwoom_client import KiwoomAPI, to_dataframe

api = KiwoomAPI.from_env(is_mock=True)

rows = api._client.request_all(
    "/api/dostk/chart",           # URL — the module URL in the endpoint reference
    "ka10081",                    # api_id
    {"stk_cd": "005930", "base_dt": "20260326", "upd_stkpc_tp": "1"},
    data_key="stk_dt_pole_chart_qry",  # the list key in the response (official spec)
    max_pages=20,
)
df = to_dataframe(rows)
```

Without `data_key` you get a list of the per-page response dicts. If you do not know the list key, look for the field
with `type == "list"` in `kiwoom_client.spec.get("ka10081").response`, or fetch once and check
`extract_records(resp)[0]`.

## asyncio

The same works with `AsyncKiwoomAPI` — just put `await` in front of the method call.

```python
import asyncio

from kiwoom_client import AsyncKiwoomAPI


async def main():
    async with AsyncKiwoomAPI.from_env(is_mock=True) as api:
        rows = await api._client.request_all(
            "/api/dostk/chart", "ka10081",
            {"stk_cd": "005930", "base_dt": "20260326", "upd_stkpc_tp": "1"},
            data_key="stk_dt_pole_chart_qry",
        )
        print(len(rows))


asyncio.run(main())
```
