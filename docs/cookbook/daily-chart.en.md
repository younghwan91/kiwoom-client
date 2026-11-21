# Daily bars as a DataFrame

`ka10081` stock daily chart (주식일봉차트조회요청) → `api.chart.stock_daily_chart()`. Fields are in the
[chart reference](../reference/chart.md#ka10081).

```python
from kiwoom_client import KiwoomAPI, to_dataframe

api = KiwoomAPI.from_env(is_mock=True)  # KIWOOM_APP_KEY / KIWOOM_APP_SECRET environment variables

resp = api.chart.stock_daily_chart(
    stk_cd="005930",     # stock code (Samsung Electronics)
    base_dt="20260326",  # base date YYYYMMDD — rows go back in time from this day
    upd_stkpc_tp="1",    # apply adjusted prices (0 or 1)
)

df = to_dataframe(resp)  # finds the list in the response (stk_dt_pole_chart_qry), converts it to numbers
df = df.rename(columns={
    "dt": "date", "open_pric": "open", "high_pric": "high", "low_pric": "low",
    "cur_prc": "close", "trde_qty": "volume", "trde_prica": "value",
})
prices = ["open", "high", "low", "close"]
df[prices] = df[prices].abs()  # Kiwoom's sign means "direction vs. previous close" — drop it for prices
df = df.sort_values("date").set_index("date")
print(df[[*prices, "volume"]].tail())
```

- `to_dataframe()` needs pandas: `pip install 'kiwoom-client[pandas]'`.
- Fields whose names mark them as dates or codes, such as `dt` (date) and `stk_cd`, stay strings instead of being
  converted to numbers.
- Kiwoom decides how many rows come back at once. To go further back, use a [continuation query](pagination.md).
- Minute bars are `api.chart.stock_minute_chart(stk_cd=..., tic_scope="1", upd_stkpc_tp="1")` (`ka10080`); weekly,
  monthly and yearly bars are `stock_weekly_chart` · `stock_monthly_chart` · `stock_yearly_chart` — see the
  [endpoint reference](../endpoints.md#chart).

## Saving to CSV · Parquet

<!-- docs-test: no-exec -->
```python
df.to_csv("005930_daily.csv")
df.to_parquet("005930_daily.parquet")  # needs pyarrow
```
