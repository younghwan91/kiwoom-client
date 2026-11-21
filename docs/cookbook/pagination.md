# 연속조회를 끝까지

한 번에 다 안 오는 TR 은 응답에 다음 페이지 표시가 붙습니다. 키움은 이것을 **응답 헤더**(`cont-yn`, `next-key`)로
주고, kiwoom-client 는 그 값을 응답 dict 에 `"cont-yn"`·`"next-key"` 키로 옮겨 넣습니다.

- `resp["cont-yn"] == "Y"` 이면 다음 페이지가 있습니다.
- 다음 요청은 같은 필드에 `cont_yn="Y", next_key=resp["next-key"]` 를 더해 보냅니다.
- 같은 TR 을 연달아 부르므로 기본 Rate Limiter(TR당 초당 1건, 버스트 2)에 맞춰 천천히 갑니다.

## 직접 돌기 — 원하는 날짜에서 멈추기

일봉을 `2020-01-01` 까지 거슬러 받는 예입니다.

```python
from kiwoom_client import KiwoomAPI, extract_records

api = KiwoomAPI.from_env(is_mock=True)

fields = {"stk_cd": "005930", "base_dt": "20260326", "upd_stkpc_tp": "1"}
rows: list[dict] = []
cont_yn, next_key = "N", ""
while True:
    resp = api.chart.stock_daily_chart(cont_yn=cont_yn, next_key=next_key, **fields)
    _, page = extract_records(resp)  # (리스트 키, 레코드 목록)
    rows += page
    if not page or min(r["dt"] for r in page) <= "20200101":
        break  # 원하는 날짜까지 왔다
    if resp.get("cont-yn") != "Y" or not resp.get("next-key"):
        break  # 더 없다
    cont_yn, next_key = "Y", resp["next-key"]

rows = [r for r in rows if r["dt"] >= "20200101"]
print(len(rows), "일")
```

## `request_all()` — 끝까지 한 번에

멈출 조건이 "끝까지" 면 저수준 클라이언트의 `request_all()` 이 같은 일을 합니다. 리스트 키(`data_key`)를 주면
페이지마다 그 리스트를 이어 붙인 하나의 리스트를 돌려줍니다. 안전장치로 `max_pages`(기본 100)에서 멈춥니다.

```python
from kiwoom_client import KiwoomAPI, to_dataframe

api = KiwoomAPI.from_env(is_mock=True)

rows = api._client.request_all(
    "/api/dostk/chart",           # URL — 엔드포인트 표의 모듈 URL
    "ka10081",                    # api_id
    {"stk_cd": "005930", "base_dt": "20260326", "upd_stkpc_tp": "1"},
    data_key="stk_dt_pole_chart_qry",  # 응답의 리스트 키 (공식 스펙)
    max_pages=20,
)
df = to_dataframe(rows)
```

`data_key` 를 빼면 페이지 응답 dict 들의 리스트가 옵니다. 리스트 키를 모를 때는
`kiwoom_client.spec.get("ka10081").response` 에서 `type == "list"` 인 필드를 찾거나, 한 번 받아 보고
`extract_records(resp)[0]` 으로 확인하세요.

## asyncio

`AsyncKiwoomAPI` 에서도 같습니다 — 메서드 호출 앞에 `await` 만 붙입니다.

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
