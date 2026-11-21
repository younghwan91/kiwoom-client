# 일봉을 받아 DataFrame 으로

`ka10081` 주식일봉차트조회요청 → `api.chart.stock_daily_chart()`. 필드는 [차트 레퍼런스](../reference/chart.md#ka10081).

```python
from kiwoom_client import KiwoomAPI, to_dataframe

api = KiwoomAPI.from_env(is_mock=True)  # KIWOOM_APP_KEY / KIWOOM_APP_SECRET 환경변수

resp = api.chart.stock_daily_chart(
    stk_cd="005930",     # 종목코드 (삼성전자)
    base_dt="20260326",  # 기준일자 YYYYMMDD — 이 날부터 과거 방향으로 온다
    upd_stkpc_tp="1",    # 수정주가 적용 (0 또는 1)
)

df = to_dataframe(resp)  # 응답에서 리스트(stk_dt_pole_chart_qry)를 찾아 숫자로 바꾼다
df = df.rename(columns={
    "dt": "date", "open_pric": "open", "high_pric": "high", "low_pric": "low",
    "cur_prc": "close", "trde_qty": "volume", "trde_prica": "value",
})
prices = ["open", "high", "low", "close"]
df[prices] = df[prices].abs()  # 키움 시세 값의 부호는 '전일 대비 방향'이다 — 가격으로 쓸 땐 떼어 낸다
df = df.sort_values("date").set_index("date")
print(df[[*prices, "volume"]].tail())
```

- `to_dataframe()` 은 pandas 가 필요합니다: `pip install 'kiwoom-client[pandas]'`.
- `dt`(일자)·`stk_cd` 처럼 이름이 날짜·코드인 필드는 숫자로 바꾸지 않고 문자열로 남깁니다.
- 한 번에 오는 개수는 키움이 정합니다. 더 과거까지 받으려면 [연속조회](pagination.md).
- 분봉은 `api.chart.stock_minute_chart(stk_cd=..., tic_scope="1", upd_stkpc_tp="1")`(`ka10080`), 주·월·년봉은
  `stock_weekly_chart`·`stock_monthly_chart`·`stock_yearly_chart` 입니다 — [엔드포인트 표](../endpoints.md#chart).

## CSV · Parquet 로 저장

<!-- docs-test: no-exec -->
```python
df.to_csv("005930_daily.csv")
df.to_parquet("005930_daily.parquet")  # pyarrow 필요
```
