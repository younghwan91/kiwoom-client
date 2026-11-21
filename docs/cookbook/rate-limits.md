# 호출 제한(429) 다루기

키움 REST API 는 **TR(api_id)마다 따로** 호출 수를 제한합니다. 넘기면 HTTP `429` 와
`{"return_code": 5, "return_msg": "허용된 요청 개수를 초과하였습니다"}` 가 옵니다(이 라이브러리의 실측).
키움 공식 오류코드에는 `1700`(API 요청 개수 초과) · `1701`(전체 요청 개수 초과) · `1702`(그룹 요청 개수 초과)가 있습니다.

## 라이브러리가 이미 하는 일

| 장치 | 기본값 | 바꾸는 인자 |
|---|---|---|
| TR별 토큰 버킷 — 보내기 전에 기다린다 | 초당 1건, 버스트 2 | `rate_limit=`, `rate_burst=` (`rate_limit=None` 이면 끔) |
| 429 · `return_code` 5 면 기다렸다 다시 보냄 | 3번, 1.1초 × 시도 횟수 | `max_retries=`, `retry_backoff=` |

그래서 한 프로세스 안에서는 보통 아무것도 안 해도 됩니다. 서로 다른 TR 은 서로를 막지 않고, 같은 TR 을 반복할 때만
초당 1건으로 줄어듭니다.

```python
from kiwoom_client import KiwoomAPI

api = KiwoomAPI.from_env(is_mock=True)                                   # 기본값
api = KiwoomAPI.from_env(is_mock=True, rate_limit=0.5, rate_burst=1)     # 더 천천히 (여러 프로세스가 나눠 쓸 때)
api = KiwoomAPI.from_env(is_mock=True, max_retries=5, retry_backoff=2.0)  # 더 끈질기게
```

## 그래도 넘쳤을 때

재시도를 다 쓰고도 넘치면 예외가 납니다. 어떤 신호로 거절됐느냐에 따라 둘 중 하나입니다.

```python
import httpx

from kiwoom_client import KiwoomAPI, KiwoomRateLimitError

api = KiwoomAPI.from_env(is_mock=True)

try:
    info = api.stock_info.basic_stock_info(stk_cd="005930")
except KiwoomRateLimitError as e:          # return_code 5 / 1700·1701·1702
    print("호출 한도 초과:", e.error_code, e.message)
except httpx.HTTPStatusError as e:         # 재시도 뒤에도 HTTP 429
    if e.response.status_code != 429:
        raise
    print("HTTP 429 — 잠시 뒤 다시")
```

## 여러 프로세스·여러 프로그램이 같은 앱키를 쓸 때

Rate Limiter 는 **프로세스 안에서만** 셉니다. 같은 앱키로 도는 프로그램이 여럿이면(수집 배치 + 매매 봇 등) 합쳐서
제한을 넘을 수 있습니다.

- 같은 TR 을 부르는 프로그램끼리는 `rate_limit` 을 나눠 갖게 낮추세요(둘이면 각자 `0.5`).
- 가능하면 조회를 한 프로세스로 모으고, 나머지는 그 결과를 받아 쓰게 하세요.
- 무엇이 몇 번 재시도됐는지는 `logging.getLogger("kiwoom_client")` 를 DEBUG 로 켜면 보입니다.

```python
import logging

logging.basicConfig(level=logging.INFO)
logging.getLogger("kiwoom_client").setLevel(logging.DEBUG)
```

## 많이 부르기 전에 줄이는 법

- **연속조회** 는 같은 TR 반복이라 초당 1건입니다. 필요한 날짜에서 멈추세요 — [연속조회](pagination.md).
- **여러 종목**: 종목마다 같은 TR 을 부르기보다 한 번에 여러 종목이 오는 TR(순위 `api.ranking.*`, 업종, 조건검색)을 찾아보세요.
- **asyncio**: 서로 다른 TR 은 동시에 나가므로 묶어 보내면 빨라집니다 — [asyncio 로 동시에 조회하기](async-concurrency.md).
- **실시간**: 계속 보는 값은 REST 로 반복 조회하지 말고 WebSocket 으로 받으세요 — [실시간 체결](realtime-trades.md).
