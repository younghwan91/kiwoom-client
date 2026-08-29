# 사용 가이드

[← README](../README.md)

- [사전 준비](#사전-준비)
- [환경 설정](#환경-설정)
- [계좌 조회와 주문](#계좌-조회와-주문)
- [asyncio](#asyncio)
- [응답을 숫자·DataFrame 으로](#응답을-숫자dataframe-으로)
- [연속 조회 (페이지네이션)](#연속-조회-페이지네이션)
- [에러 처리](#에러-처리)
- [요청 제한 (Rate Limit)](#요청-제한-rate-limit)

## 사전 준비

1. [키움 REST API 포털](https://openapi.kiwoom.com)에 가입합니다.
2. **API 사용신청**으로 `앱키(appkey)`와 `시크릿키(secretkey)`를 발급받습니다.
3. 키는 `.env` 에 보관하고 코드에 하드코딩하지 마세요 — [`.env.example`](../.env.example) 참고.
4. 먼저 **모의투자**(`is_mock=True`)로 검증한 뒤 실전으로 넘어가세요.

## 환경 설정

| 구분 | 실전투자 | 모의투자 |
|------|---------|---------|
| `is_mock` | `False` (기본값) | `True` |
| REST URL | `https://api.kiwoom.com` | `https://mockapi.kiwoom.com` |
| WebSocket URL | `wss://api.kiwoom.com:10000` | `wss://mockapi.kiwoom.com:10000` |

모의투자는 KRX 만 지원됩니다.

접근토큰은 첫 호출에서 자동 발급되고 만료 전에 갱신되므로 따로 할 일이 없습니다.
키가 올바른지 즉시 확인하고 싶을 때만 `api.login()` 을 부르세요.
`with` 문을 쓰면 `close()` 는 자동입니다.

```python
with KiwoomAPI(app_key="앱키", app_secret="시크릿키", is_mock=True) as api:
    info = api.stock_info.basic_stock_info(stk_cd="005930")
```

여러 프로세스가 토큰을 공유해야 한다면 `TokenProvider` 프로토콜
(`get_valid_token()` / `refresh_token()`)을 구현해 넘기면 Redis 등 외부 캐시를 쓸 수 있습니다.
갱신 시점은 `KiwoomAPI(..., expiry_margin=300)` 으로 조절합니다.

## 계좌 조회와 주문

```python
evaluation = api.account.account_evaluation()   # 계좌 평가 현황
deposit    = api.account.deposit_detail()       # 예수금 상세
position   = api.account.filled_position()      # 체결 잔고
unfilled   = api.account.unfilled_orders()      # 미체결 주문
```

```python
# 삼성전자 10주 지정가 매수
result = api.order.buy_order(
    dmst_stex_tp="01",   # 거래소 구분 (01: KRX)
    stk_cd="005930",     # 종목코드
    ord_qty=10,          # 주문 수량
    trde_tp="00",        # 주문 유형 (00: 지정가)
    ord_uv=70000,        # 주문 단가
)

api.order.sell_order(dmst_stex_tp="01", stk_cd="005930", ord_qty=10, trde_tp="00", ord_uv=75000)
api.order.modify_order(org_ord_no="원래주문번호", ord_qty=5, ord_uv=71000)
api.order.cancel_order(org_ord_no="원래주문번호", ord_qty=5)
```

전체 파라미터는 [키움 공식 가이드](https://openapi.kiwoom.com/guide/apiguide)를,
메서드 목록은 [지원 API 전체 목록](api-reference.md)을 보세요.

## asyncio

`AsyncKiwoomAPI` 는 `KiwoomAPI` 와 같은 엔드포인트를 제공하며, 앞에 `await` 만 붙이면 됩니다.

```python
import asyncio
from kiwoom_rest_api import AsyncKiwoomAPI

async def main():
    async with AsyncKiwoomAPI(app_key="앱키", app_secret="시크릿키", is_mock=True) as api:
        # 서로 다른 TR 은 동시에 나간다 — 직렬로 돌리면 3배 걸린다
        info, chart, ranking = await asyncio.gather(
            api.stock_info.basic_stock_info(stk_cd="005930"),
            api.chart.stock_daily_chart(stk_cd="005930", base_dt="20260326"),
            api.ranking.top_volume_today(mrkt_tp="0", stk_cnd="0", trde_qty_tp="0",
                                         prc_tp="0", trde_amt_tp="0", updn_tp="0"),
        )
        print(info["stk_nm"])

asyncio.run(main())
```

Rate Limiter 는 TR(api_id)별로 걸립니다. 서로 다른 TR 은 서로를 막지 않고,
같은 TR 을 반복할 때만 초당 1건으로 조여집니다.
전체 예제는 [`examples/async_usage.py`](../examples/async_usage.py).

## 응답을 숫자·DataFrame 으로

키움은 모든 값을 문자열로 돌려줍니다. 가격은 `"+70000"`, 등락률은 `"-1.23"`,
거래량은 `"1,234,567"` 같은 식이라 그대로는 계산에 쓸 수 없습니다.

```python
from kiwoom_rest_api import to_dataframe, to_number, normalize

result = api.ranking.top_volume_today(...)

df = to_dataframe(result)      # 페이로드 키를 자동으로 찾아 DataFrame 으로
print(df["cur_prc"].mean())

data = normalize(result)       # dict 그대로 쓰고 싶다면
price = to_number("+70000")    # 70000
```

종목코드(`"005930"`)처럼 앞자리 0 이 의미를 갖는 값과, `base_dt` 같은 날짜·식별자
필드는 숫자로 바꾸지 않고 문자열로 남깁니다.
`to_dataframe()` 에는 pandas 가 필요합니다: `pip install 'kiwoom-client[pandas]'`.

## 연속 조회 (페이지네이션)

응답 헤더의 `cont_yn` 이 `"Y"` 이면 다음 페이지가 있다는 뜻입니다.

```python
# 수동
result = api.account.filled_orders()
next_result = api.account.filled_orders(cont_yn="Y", next_key=result["next_key"])

# 자동 — 모든 페이지를 한 번에
all_data = api._client.request_all(
    "/api/dostk/acnt", "ka10076",
    data_key="filled_list",   # 응답에서 리스트 데이터의 키 이름
)
```

## 에러 처리

```python
from kiwoom_rest_api.base import KiwoomAPIError

try:
    result = api.order.buy_order(stk_cd="005930", ord_qty=10, ord_uv=70000)
except KiwoomAPIError as e:
    print(e.code, e.message, e.response)
```

WebSocket 의 로그인·프로토콜 실패는 `KiwoomWebSocketError` 로 올라옵니다.

## 요청 제한 (Rate Limit)

키움 REST API 는 **TR(api_id)별로 독립적인** 호출 제한을 둡니다. 실측 결과는 다음과 같습니다.

| 항목 | 측정값 |
|---|---|
| 지속(sustained) 안전 속도 | **TR당 약 1 req/s** (이 속도에선 거부 0) |
| 순간 버스트(burst) 허용량 | **TR당 약 2건** |
| 초과 시 응답 | HTTP `429` + `{"return_code": 5, "return_msg": "허용된 요청 개수를 초과하였습니다"}` |
| 제한 단위 | **TR(api_id)별 독립** — 서로 다른 TR 은 영향 없음 |

라이브러리는 기본적으로 TR별 토큰 버킷(1 req/s, 버스트 2)을 적용하고,
그래도 `429` 가 나면 백오프 후 자동 재시도합니다. 별도 설정 없이 안전하게 동작합니다.

```python
# 기본값
api = KiwoomAPI(app_key="...", app_secret="...")

# 직접 조정
api = KiwoomAPI(app_key="...", app_secret="...",
                rate_limit=2.0, rate_burst=3, max_retries=5)

# 클라이언트 측 스로틀 비활성화
api = KiwoomAPI(app_key="...", app_secret="...", rate_limit=None)
```

제한이 TR별이라 **서로 다른 TR 을 섞어** 호출하면 합산 처리량이 더 높습니다.
반대로 **같은 TR 을 반복**(연속조회 루프 등)할 때는 1 req/s 에 수렴하므로
`request_all()` 로 처리하세요.
