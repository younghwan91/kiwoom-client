---
seo_title: "키움 REST API 오류 코드와 해결 — 토큰·429·연속조회"
description: "키움증권 REST API 를 파이썬으로 쓸 때 자주 만나는 에러와 고치는 법. 키움 공식 오류코드(8005 토큰, 1700 호출 제한 등)의 뜻과 kiwoom-client 에서 확인할 값을 정리했습니다."
---

# 문제 해결 (Troubleshooting)

자주 만나는 에러와 고치는 법입니다. 에러 코드의 뜻은 키움 공식 [REST API 가이드](https://openapi.kiwoom.com/guide/apiguide)
"오류코드" 와 공식 [REST API 스펙](https://github.com/Kiwoom-Securities/Kiwoom-REST-API)을 기준으로 줄여 적었습니다.

## 먼저: 에러 객체에서 볼 것

```python
from kiwoom_client import KiwoomAPI, KiwoomAPIError

api = KiwoomAPI.from_env(is_mock=True)
try:
    api.stock_info.basic_stock_info(stk_cd="005930")
except KiwoomAPIError as e:
    print(type(e).__name__)  # KiwoomServerMismatchError 처럼 원인별 하위 클래스
    print(e.code)            # 응답의 return_code (3, 5 …)
    print(e.error_code)      # return_msg 안의 키움 4자리 코드 ("[8005:…]" → 8005), 없으면 None
    print(e.message)         # return_msg 원문
    print(e.hint)            # 라이브러리가 붙이는 다음 할 일 한 줄 (없으면 None)
```

키움은 응답의 `return_code` 를 3·5 처럼 뭉뚱그려 주고 **진짜 원인 코드는 `return_msg` 안에** `[8005:…]` 꼴로 넣습니다.
그래서 `e.code` 보다 `e.error_code` 와 예외 클래스를 보세요. 클래스 계층은 `kiwoom_client.errors` 에 있습니다 —
모두 `KiwoomAPIError` 의 하위 클래스라 기존 `except KiwoomAPIError` 는 그대로 잡습니다.

## 인증·토큰

### 모의투자 키로 실서버를(또는 반대로) 불렀다 — 8030 / 8031

`KiwoomServerMismatchError`. 모의투자용 키와 실전투자용 키는 **서로 다른 키**이고, 서버도 다릅니다.

| | `is_mock` | 서버 |
|---|---|---|
| 모의투자 키 | `True` | `mockapi.kiwoom.com` |
| 실전투자 키 | `False` (기본값) | `api.kiwoom.com` |

- `KiwoomAPI(...)` 의 기본값은 `is_mock=False` 입니다. 모의투자 키라면 `is_mock=True` 를 꼭 넘기세요.
- `from_env()` 는 `KIWOOM_IS_MOCK` 을 읽습니다. 없으면 실서버로 붙고 경고 로그를 남깁니다.
- 8030 은 앱키, 8031 은 토큰의 투자구분이 맞지 않을 때입니다.

### 앱키·시크릿키 검증 실패 — 8001 / 8002

키를 잘못 넣었거나(공백·따옴표가 섞이기 쉽습니다), 키 종류와 `is_mock` 이 짝이 아닙니다.
[키움 REST API 포털](https://openapi.kiwoom.com)에서 발급 상태와 키를 다시 확인하세요.

### 토큰이 유효하지 않다 — 8005 (`return_code` 3)

라이브러리가 **자동으로 토큰을 다시 받아 한 번 더 보냅니다.** 키움은 만료·무효 토큰에 HTTP 401 이 아니라
HTTP 200 + `return_code: 3` 을 돌려주는데(0.2.1 에서 대응), 이것도 재발급 대상입니다. 재발급 뒤에도 `KiwoomTokenError` 가 나면:

- 다른 프로그램이 같은 앱키의 토큰을 폐기했을 수 있습니다(`api.logout()` / 토큰 폐기 API). 공유 앱키라면 `logout()` 을 부르지 마세요.
- 키 종류와 `is_mock` 이 짝인지 다시 보세요.

### 토큰을 받은 IP 와 요청한 IP 가 다르다 — 8010

토큰을 한 곳에서 받아 다른 서버·컨테이너에서 쓰거나, 나가는 IP 가 바뀌는 프록시·NAT 뒤에 있을 때입니다.
토큰을 쓰는 곳에서 직접 받게 하세요(기본 동작이 그렇습니다).

### 토큰 발급 자체가 실패한다 — `KiwoomAuthError`

`/oauth2/token` 요청이 HTTP 에러로 끝났거나 응답에 토큰이 없을 때입니다. 메시지에 키움의 `return_msg` 가 들어 있습니다.
네트워크(방화벽·DNS)와 키를 확인하세요.

## 호출 제한 — HTTP 429, `return_code` 5, 1700 / 1701 / 1702

`KiwoomRateLimitError`, 또는 재시도 뒤에도 429 면 `httpx.HTTPStatusError`. 라이브러리가 TR별로 속도를 맞추고 재시도하므로,
보통은 **여러 프로세스가 같은 앱키로 같은 TR 을 동시에** 부를 때 납니다. → [호출 제한 다루기](cookbook/rate-limits.md)

## 요청 필드·종목코드

| 코드 | 무슨 뜻 | 예외 | 할 일 |
|---|---|---|---|
| 1511 | 필수 입력 값이 비었음 | `KiwoomRequestError` | `kiwoom_client.spec.get(api_id).required_fields` 로 필수 필드 확인 |
| 1517 | 입력 값 형식이 틀림 | `KiwoomRequestError` | 값은 문자열로(`ord_qty="10"`), 날짜는 `YYYYMMDD`, 코드값은 `kiwoom_client.codes` |
| 1504 · 1505 | 그 URL 에 없는 / 존재하지 않는 API ID | `KiwoomRequestError` | 메서드를 쓰면 생기지 않음 — `request()` 를 직접 불렀다면 URL·api_id 짝 확인 |
| 1901 · 1902 · 1903 | 시장 코드·종목 정보가 없음 | `KiwoomStockNotFoundError` | 종목코드 6자리 확인. NXT·SOR 은 `005930_NX` · `005930_AL` 꼴 (`codes.exchange_stock_code`) |

모르는 필드 이름·빠진 필수 필드는 보내기 전에 잡을 수 있습니다(공식 스펙 카탈로그와 대조, 비슷한 이름도 알려 줌):

<!-- docs-test: skip -->
```python
from kiwoom_client import KiwoomAPI

api = KiwoomAPI.from_env(is_mock=True, validate_params="warn")  # "error" 면 보내지 않고 KiwoomParamError
api.chart.stock_daily_chart(stk_cd="005930", base_date="20260326")  # base_date → 경고 (정답: base_dt)
```

## 모의투자·계좌 종류

- **8104** 모의투자에서 지원하지 않는 API — `KiwoomUnsupportedError`. 실전투자 서버에서만 되는 TR 입니다.
- **8200** 법인 고객은 지원하지 않는 API — `KiwoomUnsupportedError`.
- 모의투자 주문은 거래소 구분 `KRX` 만 됩니다(`dmst_stex_tp="KRX"`).

## 주문

- **지정가가 거부되거나 다른 가격이 된다**: `ord_uv` 가 호가단위의 배수가 아닌 경우입니다. `round_to_tick()` · `add_ticks()` 로 맞추세요
  → [지정가 주문 레시피](cookbook/limit-order.md).
- **값을 숫자로 넘겼다**: 키움 필드는 전부 문자열입니다. `ord_qty="10"`, `ord_uv=str(price)`.
- **MCP 에서 주문 도구가 안 보인다**: 의도된 동작입니다. 실전투자(`KIWOOM_IS_MOCK=false`)에서는
  `KIWOOM_MCP_ALLOW_LIVE_ORDERS=true` 를 켜기 전까지 주문 도구를 등록하지 않습니다.

## 응답 다루기

- **`to_dataframe()` 이 ImportError**: pandas 가 필요합니다 — `pip install 'kiwoom-client[pandas]'`.
- **숫자가 문자열로 남는다**: `to_number()`·`normalize()` 는 `"005930"` 처럼 앞자리가 0 으로 채워진 값과 `_cd`·`_dt`·`_no`·`_nm` 으로
  끝나는 필드를 **코드로 보고 일부러 남깁니다.** 금액이 0 으로 채워져 온다면 직접 `int()` 로 바꾸세요 → [잔고 레시피](cookbook/account-summary.md).
- **가격이 음수다**: 키움 시세의 부호는 전일 대비 방향입니다. 가격으로 쓸 땐 `abs()`.
- **연속조회가 첫 페이지에서 멈춘다**: 0.4.0 미만의 버그입니다(키움은 연속 여부를 응답 헤더로 주는데 본문에서만 찾았음). 올리세요 → [연속조회](cookbook/pagination.md).

## WebSocket

- **`connect()` 가 `KiwoomWebSocketError`**: LOGIN 응답이 실패였습니다. 메시지의 `return_msg` 를 보고, 토큰·`is_mock` 을 확인하세요.
- **"서버가 LOGIN 응답 없이 연결을 종료했습니다"**: 짧은 간격으로 다시 접속할 때 서버가 끊는 경우가 있었습니다. 잠시 뒤 다시 시도하세요.
- **콜백이 안 불린다**: `connect()` 다음에 `subscribe()` 했는지, `listen()` 이 돌고 있는지, `ws.on()` 의 타입 코드(`"0B"`)가
  구독한 타입과 같은지 보세요. 장이 닫혀 있으면 체결이 오지 않습니다. 모든 프레임은 `ws.on_message()` 로 볼 수 있습니다.
- **`RuntimeError: WebSocket not connected`**: `send()`·`listen()` 전에 `await ws.connect()`.

## 설치·임포트

- **`ModuleNotFoundError: kiwoom_rest_api`**: 0.3.0 에서 임포트 이름이 `kiwoom_client` 로 바뀌었습니다. `from kiwoom_client import KiwoomAPI`.
- **Python 3.9 이하**: 3.10 이상이 필요합니다.

여기 없는 문제는 [이슈](https://github.com/younghwan91/kiwoom-client/issues)로 알려 주세요. 키·계좌번호는 지우고 올려 주세요.
