---
seo_title: "키움 REST API 편의 기능 — from_env·종목코드 찾기·호가 계산"
description: "kiwoom-client 편의 기능 — 환경변수로 시작하는 from_env(), 종목명↔종목코드, 공식 코드값 상수, 차트→OHLCV DataFrame, 호가 계산, 예외 타입, 조회 전용 CLI."
---

# 편의 기능 — 짧게, 실수 없이

엔드포인트 182개를 그대로 부르는 것 말고, 자주 하는 일을 줄이고 흔한 실수를 막는 도구들입니다.
전부 기존 동작은 그대로 두고 **더한** 것이라, 원래 쓰던 코드는 바꿀 필요가 없습니다.

## 환경변수로 시작하기 — `from_env()`

```python
from kiwoom_client import KiwoomAPI

api = KiwoomAPI.from_env(is_mock=True)   # KIWOOM_APP_KEY / KIWOOM_APP_SECRET
api = KiwoomAPI.from_env(".env", is_mock=True)  # .env 파일도 읽는다 (새 의존성 없음)
```

| 변수 | 뜻 |
|---|---|
| `KIWOOM_APP_KEY` | 앱키 (필수) |
| `KIWOOM_APP_SECRET` | 시크릿키 (필수) |
| `KIWOOM_IS_MOCK` | `true` 모의투자 / `false` 실전투자 |

- MCP 서버와 같은 이름이라 `.env` 하나로 둘 다 씁니다.
- 우선순위: `is_mock=` 인자 > 프로세스 환경변수 > `.env` 파일.
- `KIWOOM_IS_MOCK` 은 `true/false`, `1/0`, `yes/no`, `on/off` 만 받습니다. `ture` 같은 오타는 실전투자로 넘어가지 않고 `ValueError` 입니다.
- **어디에도 없으면 실전투자 서버**(`is_mock=False`, 생성자·MCP 서버와 같은 기본값)에 붙고 `kiwoom_client` 로거에 경고를 남깁니다. 처음엔 `is_mock=True` 를 직접 넘기세요.
- 나머지 인자(`rate_limit`, `max_retries`, `timeout` ...)는 그대로 생성자로 넘어갑니다. `AsyncKiwoomAPI.from_env()` 도 같습니다.

## 종목명 ↔ 종목코드 — `find_stock()`

```python
api.find_stock("삼성")        # [{'code': '005930', 'name': '삼성전자', 'marketName': ...}, ...]
api.stock_code("SK하이닉스")   # '000660'
api.stock_list()              # 코스피 + 코스닥 전 종목
```

- 종목정보 리스트(**ka10099**)를 시장마다 전 페이지 한 번 받아 클라이언트에 캐시합니다. `refresh=True` 로 다시 받고, `cache_ttl=초` 로 자동 만료합니다.
- 순서: 정확한 코드 > 정확한 이름 > 이름 앞부분 > 코드 앞부분 > 이름 일부. 대소문자·공백은 무시합니다.
- `stock_code()` 는 이름이 정확히 한 종목과 같을 때만 코드를 주고, 아니면 후보를 담은 `LookupError` 입니다.
- 다른 시장: `markets=[StockListMarket.ETF]` (아래 코드값 참고).

## 코드값 상수 — `kiwoom_client.codes`

키움은 옵션을 짧은 문자열로 받고, 같은 필드 이름이 TR마다 다른 코드를 씁니다. 이름 붙은 상수를 쓰면 오타가 바로 드러납니다.
모두 `str` 이라 그대로 넘기면 원래 코드값이 전송됩니다.

```python
from kiwoom_client import Exchange, OrderType

api.order.buy_order(
    dmst_stex_tp=Exchange.KRX, stk_cd="005930", ord_qty="10",
    ord_uv="70000", trde_tp=OrderType.LIMIT,   # "0" 보통(지정가)
)
```

| 상수 | 필드 | 값 |
|---|---|---|
| `Exchange` | 주문 `dmst_stex_tp` | `KRX` · `NXT` · `SOR` |
| `OrderType` | 주문 `trde_tp` | `LIMIT`="0", `MARKET`="3", `STOP_LIMIT`="28" 등 18종 |
| `QueryExchange` | 조회 `stex_tp` | `KRX`="1", `NXT`="2", `ALL`="3"(통합) |
| `Market` | 순위·종목 TR `mrkt_tp` | `ALL`="000", `KOSPI`="001", `KOSDAQ`="101" |
| `StockListMarket` | ka10099 `mrkt_tp` | `KOSPI`="0", `KOSDAQ`="10", `ETF`="8" 등 16종 |
| `AdjustedPrice` | 차트 `upd_stkpc_tp` | `RAW`="0", `ADJUSTED`="1" |
| `PriceChangeSign` | 응답 `pred_pre_sig` | 1 상한가 · 2 상승 · 3 보합 · 4 하한가 · 5 하락 |

`exchange_stock_code("005930", Exchange.NXT)` 는 시세·차트 TR 이 받는 거래소별 코드 `"005930_NX"` 를 만듭니다(SOR 은 `_AL`).
값은 [키움 REST API 가이드](https://openapi.kiwoom.com/guide/apiguide)에서 TR별로 확인한 것만 넣었습니다.

## 차트 → OHLCV DataFrame — `to_ohlcv()`

```python
from kiwoom_client import to_ohlcv

resp = api.chart.stock_daily_chart(stk_cd="005930", base_dt="20260327", upd_stkpc_tp="1")
df = to_ohlcv(resp)   # open/high/low/close/volume, DatetimeIndex, 오래된 순
```

- 주식·업종·금현물의 틱·분·일·주·월·년봉을 모두 받습니다. `request_all()` 의 리스트도 됩니다.
- 분·틱봉 가격 앞의 `+`/`-` 는 등락 방향이지 음수가 아니라서 떼어 냅니다.
- 거래대금처럼 다른 필드도 필요하면 `keep=["trde_prica"]` (단위가 TR마다 다릅니다: 일봉 백만원, 주·월봉 원).
- 업종 지수 값은 키움이 보낸 그대로(소수점 제거된 값)입니다.
- pandas 가 필요합니다: `pip install 'kiwoom-client[pandas]'`. 원 필드 전부가 필요하면 기존 `to_dataframe()`.

## 호가 계산 — `add_ticks()` · `ticks_between()`

```python
from kiwoom_client import add_ticks, is_on_tick, round_up_to_tick, ticks_between

add_ticks(49_950, 2)           # Decimal('50100') — 5만원 경계에서 호가단위가 50 → 100
add_ticks(2_000, -1)           # Decimal('1999')  — 1995 가 아니다
ticks_between(49_900, 50_100)  # 3
round_up_to_tick(70_101)       # Decimal('70200') — round_to_tick() 의 올림판
is_on_tick(70_150)             # False
```

손절·익절가를 "N틱 아래/위" 로 잡을 때 구간 경계에서 틀리지 않게 합니다. 유효 호가가 아닌 값을 넣으면 `ValueError` 입니다.
기존 `tick_size()`·`round_to_tick()`·`ticks_in()` 결과는 바뀌지 않았습니다.

## 예외 — 무엇이 잘못됐는지 타입으로

```python
from kiwoom_client import KiwoomAPIError, KiwoomRateLimitError, KiwoomServerMismatchError

try:
    api.stock_info.basic_stock_info(stk_cd="005930")
except KiwoomServerMismatchError as e:   # 모의/실전 키 불일치 (8030/8031)
    print(e.hint)                        # 지금 연결된 서버와 맞는 is_mock 안내
except KiwoomRateLimitError:             # 한도 초과 — 자동 재시도 뒤에도
    ...
except KiwoomAPIError as e:              # 그 밖의 return_code != 0 (기존과 같다)
    print(e.code, e.error_code, e.message)
```

```
KiwoomError
├── KiwoomAuthError              토큰 발급·폐기 실패
├── KiwoomWebSocketError         WebSocket 로그인·프로토콜 실패
└── KiwoomAPIError               return_code != 0
    ├── KiwoomTokenError         토큰 거부 (return_code 3)
    │   └── KiwoomServerMismatchError  모의/실전 불일치
    ├── KiwoomRateLimitError     호출 한도 초과 (return_code 5)
    ├── KiwoomRequestError       파라미터·헤더 오류
    │   └── KiwoomStockNotFoundError  종목코드 없음
    └── KiwoomUnsupportedError   모의투자·법인 미지원 API
```

- 세분 예외는 모두 `KiwoomAPIError` 라서 기존 `except KiwoomAPIError` 가 그대로 잡습니다. `code`·`message`·`response` 도 그대로입니다.
- `error_code` 는 `return_msg` 안의 4자리 코드(`[8005:...]`)입니다.
- 원인을 아는 오류는 `str(e)` 둘째 줄에 `힌트:` 가 붙습니다(`e.hint`). 토큰 발급 실패(`KiwoomAuthError`)도 같습니다.

## 명령줄 — `kiwoom`

```bash
kiwoom quote 005930 --mock        # 현재가 (종목명도 됩니다: kiwoom quote 삼성전자)
kiwoom chart 005930 --daily -n 10 # --weekly --monthly --yearly --minute --tick
kiwoom balance --mock             # 계좌평가잔고 (kt00018)
kiwoom find 하이닉스 --mock
kiwoom endpoints 체결             # 메서드 ↔ TR 찾기 (키 없이)
kiwoom --json quote 005930        # 원 응답 JSON
kiwoom --demo quote 삼성전자      # 키 없이 가상 데이터로 (연결 없음)
```

키는 `from_env()` 와 같이 환경변수에서 읽고 `--env-file` 로 `.env` 를 지정할 수 있습니다. `--mock`/`--live` 가 `KIWOOM_IS_MOCK` 보다 우선합니다.
`--demo` 는 키 없이 [데모 백엔드](mcp.md#데모-모드-키-없이-체험)를 쓰고, 출력 첫 줄에 `[데모] 가상 데이터` 배너를 찍습니다(`--json` 이면 stderr). 시세는 실제가 아닙니다.
**조회만 합니다** — 주문·토큰 폐기 명령은 일부러 없습니다. `python -m kiwoom_client` 로도 실행됩니다.

## 디버깅 — repr · 로그 · timeout

```python
print(api)
# KiwoomAPI(server='mock', base_url='https://mockapi.kiwoom.com', app_key='****AbCd', token='set')
```

- `print(api)` 로 어느 서버에 붙었는지 바로 봅니다. 시크릿키와 토큰은 일부도 보이지 않습니다.
- 요청 추적: `logging.getLogger("kiwoom_client").setLevel(logging.DEBUG)` — api-id·HTTP 상태·return_code·재시도·토큰 재발급이 남고, 헤더(토큰)와 본문(계좌번호)은 남지 않습니다.
- `KiwoomAPI(..., timeout=10.0)` — HTTP 타임아웃(초 또는 `httpx.Timeout`). 기본 30초.
