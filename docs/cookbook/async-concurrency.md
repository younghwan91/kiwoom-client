# asyncio 로 동시에 조회하기

`AsyncKiwoomAPI` 는 `KiwoomAPI` 와 같은 메서드를 갖고, 호출 앞에 `await` 만 붙입니다. 이득은 **서로 다른 TR** 을
동시에 보낼 때 납니다. 키움의 호출 제한은 TR(api_id)마다 따로라서, 라이브러리도 TR 마다 따로 줄을 세웁니다.

| 동시에 보내는 것 | 걸리는 시간 (기본 Rate Limiter: TR당 초당 1건, 버스트 2) |
|---|---|
| 서로 다른 TR 3개 | 한 번 왕복 시간 — 서로 기다리지 않음 |
| 같은 TR 10번 (종목 10개) | 약 8초 — 처음 2건은 바로, 나머지는 초당 1건 |

## 서로 다른 TR 을 한꺼번에

```python
import asyncio

from kiwoom_client import AsyncKiwoomAPI, to_dataframe


async def main():
    async with AsyncKiwoomAPI.from_env(is_mock=True) as api:
        info, quote, daily = await asyncio.gather(
            api.stock_info.basic_stock_info(stk_cd="005930"),   # ka10001
            api.market.stock_quote(stk_cd="005930"),            # ka10004
            api.chart.stock_daily_chart(stk_cd="005930", base_dt="20260326", upd_stkpc_tp="1"),
        )
    print(info["stk_nm"], "매도1", quote["sel_fpr_bid"], "매수1", quote["buy_fpr_bid"])
    print(to_dataframe(daily).head())


asyncio.run(main())
```

## 여러 종목 — 같은 TR 이면 줄을 선다

종목 여러 개에 같은 TR 을 부르면 `gather` 로 묶어도 TR 하나의 제한(초당 1건)을 넘지 않게 라이브러리가 순서를 맞춥니다.
429 를 맞고 재시도하는 것보다 빠르고, 코드는 그대로 둘 수 있습니다.

```python
import asyncio

from kiwoom_client import AsyncKiwoomAPI, KiwoomAPIError

CODES = ["005930", "000660", "035420", "005380", "051910"]


async def main():
    async with AsyncKiwoomAPI.from_env(is_mock=True) as api:
        results = await asyncio.gather(
            *(api.stock_info.basic_stock_info(stk_cd=code) for code in CODES),
            return_exceptions=True,  # 한 종목이 실패해도 나머지는 받는다
        )
    for code, res in zip(CODES, results):
        if isinstance(res, KiwoomAPIError):
            print(code, "실패:", res)
        elif isinstance(res, BaseException):
            raise res
        else:
            print(code, res["stk_nm"], res["cur_prc"])


asyncio.run(main())
```

- 같은 TR 을 많이 부르는 작업(전 종목 순회 등)은 TR 을 바꿀 수 없다면 시간이 줄지 않습니다. 이때는 한 번에 여러 종목이
  오는 TR(순위·업종·조건검색)을 찾아보거나, 미리 받아 둔 데이터를 쓰세요.
- 여러 **프로세스**가 같은 앱키로 같은 TR 을 부르면 프로세스마다 따로 세므로 합쳐서 제한을 넘을 수 있습니다 —
  [호출 제한 다루기](rate-limits.md).
- `AsyncKiwoomAPI` 는 `async with` 로 쓰거나 끝에 `await api.close()` 를 부르세요.
