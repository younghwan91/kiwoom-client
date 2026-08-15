[한국어](README.md) | [English](README_EN.md)

# kiwoom-rest-api — 키움증권 REST API Python 라이브러리

[![PyPI version](https://img.shields.io/pypi/v/kiwoom-client)](https://pypi.org/project/kiwoom-client/)
[![Downloads](https://img.shields.io/pypi/dm/kiwoom-client)](https://pypi.org/project/kiwoom-client/)
[![CI](https://github.com/younghwan91/kiwoom-rest-api/actions/workflows/ci.yml/badge.svg)](https://github.com/younghwan91/kiwoom-rest-api/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/github/license/younghwan91/kiwoom-rest-api)](https://github.com/younghwan91/kiwoom-rest-api/blob/main/LICENSE)
[![Python](https://img.shields.io/pypi/pyversions/kiwoom-rest-api)](https://pypi.org/project/kiwoom-rest-api/)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-younghwan--chae-0A66C2?logo=linkedin&logoColor=white)](https://www.linkedin.com/in/younghwan-chae/)

> **키움증권 OpenAPI를 대체하는 Python REST API 래퍼.**
> COM/OCX 없이 Windows · macOS · Linux 어디서나 **국내주식 자동매매 · 시세조회 · 실시간 WebSocket**을 사용할 수 있습니다.
> 207개 엔드포인트 · 19종 실시간 데이터 · 모의투자/실전투자 지원.

키움증권 REST API를 Python으로 쉽게 사용할 수 있는 래퍼 라이브러리입니다.
기존 키움 **OpenAPI+(OCX/COM)**나 `pykiwoom`과 달리, 32bit·Windows 제약 없이 64bit Python과 서버(헤드리스) 환경에서 그대로 동작합니다.

국내주식 **207개 엔드포인트**와 **19종 실시간 WebSocket 데이터**를 지원합니다.

> 검색 키워드: 키움 OpenAPI 파이썬, 키움증권 자동매매 파이썬, 키움 REST API, pykiwoom 대안, 키움 모의투자 파이썬, KOSPI/KOSDAQ 시세 조회

## 목차

- [왜 이 라이브러리인가?](#왜-이-라이브러리인가)
- [기존 키움 OpenAPI / pykiwoom 과 무엇이 다른가?](#기존-키움-openapi--pykiwoom-과-무엇이-다른가)
- [설치](#설치)
- [사전 준비](#사전-준비)
- [빠른 시작](#빠른-시작)
- [asyncio 사용법](#asyncio-사용법)
- [응답을 숫자·DataFrame으로 받기](#응답을-숫자dataframe으로-받기)
- [실시간 WebSocket 데이터](#실시간-websocket-데이터)
- [연속 조회 (페이지네이션)](#연속-조회-페이지네이션)
- [에러 처리](#에러-처리)
- [요청 제한 (Rate Limit)](#요청-제한-rate-limit)
- [자주 묻는 질문 (FAQ)](#자주-묻는-질문-faq)
- [지원 API 목록](#지원-api-목록)

## 왜 이 라이브러리인가?

- **크로스 플랫폼**: REST API 기반이라 Windows, macOS, Linux 어디서나 동작합니다. COM/OCX 방식과 달리 서버 환경에서도 사용 가능합니다.
- **자동 토큰 관리**: 토큰을 알아서 발급하고, 만료 전에 갱신하고, 401이 나면 재발급 후 재시도합니다. 장시간 도는 봇이 토큰 만료로 죽지 않습니다.
- **sync / async 양쪽 지원**: `KiwoomAPI`와 `AsyncKiwoomAPI`가 같은 API를 제공합니다.
- **자동 페이지네이션**: `request_all()`로 연속조회를 한 줄에 처리합니다.
- **내장 Rate Limiter**: TR(api_id)별 토큰 버킷으로 호출 제한을 자동 관리합니다.
- **바로 쓰는 응답**: `to_dataframe()`이 `"+70000"` 같은 문자열을 숫자로 바꿔 DataFrame으로 넘겨줍니다.
- **완전한 커버리지**: 국내주식 207개 REST 엔드포인트 + 19종 실시간 WebSocket 데이터를 지원합니다.

## 기존 키움 OpenAPI / pykiwoom 과 무엇이 다른가?

기존 키움 **OpenAPI+(OCX/COM)**나 이를 감싼 `pykiwoom`은 32bit Windows에 묶여 있어 서버 배포·자동화가 어렵습니다.
이 라이브러리는 키움의 **신규 REST API**를 사용하므로 그 제약이 없습니다.

| 항목 | 키움 OpenAPI+ (OCX) | pykiwoom | **kiwoom-rest-api** |
|------|---------------------|----------|---------------------|
| 연동 방식 | COM/OCX | OCX 래퍼 | **REST + WebSocket** |
| 운영체제 | Windows 전용 | Windows 전용 | **Windows · macOS · Linux** |
| Python 비트수 | 32bit 전용 | 32bit 전용 | **64bit 지원** |
| 서버/헤드리스 배포 | 어려움 (GUI 필요) | 어려움 | **가능** |
| 실시간 데이터 | 이벤트 콜백 | 이벤트 콜백 | **async WebSocket** |
| 설치 | 별도 모듈 설치 | OCX + 모듈 | **`pip install` 한 줄** |

> 이미 OCX 기반 코드를 쓰고 있다면, REST 방식으로 전환할 때 GUI 의존성과 32bit 제약을 한 번에 제거할 수 있습니다.

## 설치

```bash
pip install kiwoom-client
```

pandas 변환(`to_dataframe()`)까지 함께 쓰려면:
```bash
pip install 'kiwoom-client[pandas]'
```

또는 [uv](https://docs.astral.sh/uv/) 사용:
```bash
uv add kiwoom-client
```

소스에서 설치:
```bash
git clone https://github.com/younghwan91/kiwoom-rest-api.git
cd kiwoom-rest-api
pip install -e .
# 또는
uv pip install -e .
```

## 사전 준비

1. [키움 REST API 포털](https://openapi.kiwoom.com)에 가입합니다.
2. **API 사용신청**을 통해 `앱키(appkey)`와 `시크릿키(secretkey)`를 발급받습니다.
3. 환경변수 설정은 [`.env.example`](.env.example)을 참고하세요.
4. 처음에는 **모의투자**(`is_mock=True`)로 테스트한 뒤, 실전투자로 전환하세요.

## 빠른 시작

### 1단계: 연결

```python
from kiwoom_rest_api import KiwoomAPI

# 모의투자 서버로 연결
api = KiwoomAPI(
    app_key="발급받은_앱키",
    app_secret="발급받은_시크릿키",
    is_mock=True,  # True=모의투자, False=실전투자
)
```

접근토큰은 첫 호출에서 자동 발급되고 만료 전에 갱신되므로 따로 할 일이 없습니다.
키가 올바른지 즉시 확인하고 싶다면 `api.login()`을 호출하세요 (선택).

### 2단계: 종목 조회

```python
# 삼성전자(005930) 기본 정보 조회
info = api.stock_info.basic_stock_info(stk_cd="005930")
print(info)

# 삼성전자 일봉 차트 조회
chart = api.chart.stock_daily_chart(stk_cd="005930", base_dt="20260326")

# 당일 거래량 상위 종목 조회
ranking = api.ranking.top_volume_today()
```

### 3단계: 계좌 조회

```python
# 내 계좌 평가 현황
evaluation = api.account.account_evaluation()

# 예수금 상세 조회
deposit = api.account.deposit_detail()

# 체결 잔고 조회
position = api.account.filled_position()

# 미체결 주문 조회
unfilled = api.account.unfilled_orders()
```

### 4단계: 주문

```python
# 삼성전자 10주 지정가 매수
result = api.order.buy_order(
    dmst_stex_tp="01",   # 거래소 구분 (01: KRX)
    stk_cd="005930",     # 종목코드
    ord_qty=10,          # 주문 수량
    trde_tp="00",        # 주문 유형 (00: 지정가)
    ord_uv=70000,        # 주문 단가
)

# 매도 주문
api.order.sell_order(
    dmst_stex_tp="01",
    stk_cd="005930",
    ord_qty=10,
    trde_tp="00",
    ord_uv=75000,
)

# 주문 정정
api.order.modify_order(org_ord_no="원래주문번호", ord_qty=5, ord_uv=71000)

# 주문 취소
api.order.cancel_order(org_ord_no="원래주문번호", ord_qty=5)
```

### 5단계: 정리

```python
api.logout()  # 토큰 폐기 (선택)
api.close()   # 연결 종료

# with 문을 쓰면 close()는 자동입니다
with KiwoomAPI(app_key="앱키", app_secret="시크릿키", is_mock=True) as api:
    info = api.stock_info.basic_stock_info(stk_cd="005930")
```

## asyncio 사용법

`AsyncKiwoomAPI`는 `KiwoomAPI`와 같은 엔드포인트를 제공하며, 호출 앞에 `await`만 붙이면 됩니다.

```python
import asyncio
from kiwoom_rest_api import AsyncKiwoomAPI

async def main():
    async with AsyncKiwoomAPI(app_key="앱키", app_secret="시크릿키", is_mock=True) as api:
        # 서로 다른 TR은 동시에 나간다 — 직렬로 돌리면 3배 걸린다
        info, chart, ranking = await asyncio.gather(
            api.stock_info.basic_stock_info(stk_cd="005930"),
            api.chart.stock_daily_chart(stk_cd="005930", base_dt="20260326"),
            api.ranking.top_volume_today(
                mrkt_tp="0", stk_cnd="0", trde_qty_tp="0",
                prc_tp="0", trde_amt_tp="0", updn_tp="0",
            ),
        )
        print(info["stk_nm"])

asyncio.run(main())
```

Rate Limiter는 TR(api_id)별로 걸립니다. 서로 다른 TR은 서로를 막지 않고 동시에 나가며,
같은 TR을 반복 호출할 때만 초당 1건으로 조여집니다. 전체 예제는
[`examples/async_usage.py`](examples/async_usage.py)를 참고하세요.

## 응답을 숫자·DataFrame으로 받기

키움은 모든 값을 문자열로 돌려줍니다. 가격은 `"+70000"`, 등락률은 `"-1.23"`,
거래량은 `"1,234,567"` 같은 식이라 그대로는 계산에 쓸 수 없습니다.

```python
from kiwoom_rest_api import to_dataframe, to_number, normalize

result = api.ranking.top_volume_today(...)

# 페이로드 키를 자동으로 찾아 DataFrame으로 변환 (문자열 → 숫자 포함)
df = to_dataframe(result)
print(df["cur_prc"].mean())   # 바로 계산 가능

# dict 그대로 쓰고 싶다면
data = normalize(result)
price = to_number("+70000")   # 70000
```

종목코드(`"005930"`)처럼 앞자리 0이 의미를 갖는 값과, `base_dt` 같은 날짜·식별자
필드는 숫자로 바꾸지 않고 문자열로 남깁니다.

`to_dataframe()`에는 pandas가 필요합니다:

```bash
pip install 'kiwoom-client[pandas]'
```

## 실시간 WebSocket 데이터

실시간 체결가, 호가, 잔고 변동 등을 WebSocket으로 수신할 수 있습니다.

```python
import asyncio
from kiwoom_rest_api import KiwoomAPI

api = KiwoomAPI(app_key="앱키", app_secret="시크릿키")
ws = api.create_websocket()

async def main():
    # connect()가 LOGIN 핸드셰이크까지 끝냅니다. 실패하면 KiwoomWebSocketError
    await ws.connect()

    # 콜백은 REAL 프레임의 항목 하나를 받습니다:
    # {"type": "0B", "item": "005930", "values": {"10": "+70000", ...}}
    ws.on("0B", lambda d: print(f"체결 {d['item']}: {d['values'].get('10')}"))
    ws.on("0D", lambda d: print(f"호가 {d['item']}: {d['values'].get('41')}"))

    # async 콜백도 그대로 등록할 수 있습니다
    async def save(d): ...
    ws.on("0B", save)

    # 삼성전자 실시간 체결+호가 구독
    await ws.subscribe("0B", "005930")
    await ws.subscribe(["0B", "0D"], ["005930", "000660", "035420"])

    # PING 응답과 재연결(재로그인·구독 복원)은 listen()이 알아서 처리합니다
    await ws.listen()

asyncio.run(main())
```

`values`의 키는 키움 FID 번호입니다(10=현재가, 13=누적거래량, 41=매도최우선호가).

### 조건검색

조건검색도 같은 WebSocket을 씁니다. `api.condition_search`가 요청 페이로드를 만들고,
`ws.send()`로 보낸 뒤 `ws.on_trnm()`으로 응답을 받습니다.

```python
await ws.connect()
ws.on_trnm("CNSRLST", lambda d: print("조건식 목록:", d["data"]))
ws.on_trnm("CNSRREQ", lambda d: print("검색 결과:", d.get("data")))

# 조건식 목록을 먼저 조회해야 seq를 알 수 있습니다
await ws.send(api.condition_search.condition_list())

# seq로 검색 (search_type="1"이면 실시간 편입/이탈까지 수신)
await ws.send(api.condition_search.condition_search_realtime(seq="1"))
await ws.listen()
```

> **참고**: WebSocket 계층은 키움 공식 프로토콜 문서를 근거로 구현했고 로컬 테스트로
> 검증했지만, 실계좌 검증은 아직입니다. 이상 동작을 만나면
> [이슈](https://github.com/younghwan91/kiwoom-rest-api/issues)로 알려주세요.

## 연속 조회 (페이지네이션)

데이터가 많은 API는 한 번에 모든 데이터를 반환하지 않습니다.
응답 헤더의 `cont_yn`이 `"Y"`이면 다음 페이지가 있다는 뜻입니다.

```python
# 방법 1: 수동 연속 조회
result = api.account.filled_orders()
# result에 cont_yn="Y"와 next_key가 있으면 다음 페이지 조회
next_result = api.account.filled_orders(cont_yn="Y", next_key=result["next_key"])

# 방법 2: 자동 전체 조회 (모든 페이지를 한번에)
from kiwoom_rest_api.base import BaseClient
all_data = api._client.request_all(
    "/api/dostk/acnt", "ka10076",
    data_key="filled_list",  # 응답에서 리스트 데이터의 키 이름
)
```

## 에러 처리

```python
from kiwoom_rest_api.base import KiwoomAPIError

try:
    result = api.order.buy_order(stk_cd="005930", ord_qty=10, ord_uv=70000)
except KiwoomAPIError as e:
    print(f"에러 코드: {e.code}")
    print(f"에러 메시지: {e.message}")
    print(f"전체 응답: {e.response}")
```

## 요청 제한 (Rate Limit)

키움 REST API는 **TR(api_id)별로 독립적인** 호출 제한을 둡니다. 실측 결과는 다음과 같습니다.

| 항목 | 측정값 |
|---|---|
| 지속(sustained) 안전 속도 | **TR당 약 1 req/s** (이 속도에선 거부 0) |
| 순간 버스트(burst) 허용량 | **TR당 약 2건** |
| 초과 시 응답 | HTTP `429` + `{"return_code": 5, "return_msg": "허용된 요청 개수를 초과하였습니다"}` |
| 제한 단위 | **TR(api_id)별 독립** — 서로 다른 TR은 영향 없음 |

이에 맞춰 라이브러리는 **기본적으로 TR별 토큰 버킷 Rate Limiter(1 req/s, 버스트 2)** 를 적용하고, 그래도 `429`가 발생하면 **자동으로 백오프 후 재시도**합니다. 별도 설정 없이도 안전하게 동작합니다.

```python
# 기본값: TR당 1 req/s, 버스트 2, 429 자동 재시도
api = KiwoomAPI(app_key="...", app_secret="...")

# 직접 조정 (예: TR당 2 req/s, 버스트 3, 재시도 5회)
api = KiwoomAPI(app_key="...", app_secret="...",
                rate_limit=2.0, rate_burst=3, max_retries=5)

# 클라이언트 측 스로틀 비활성화 (직접 제어할 때)
api = KiwoomAPI(app_key="...", app_secret="...", rate_limit=None)
```

> 제한이 TR별이라, **서로 다른 TR을 섞어** 호출하면 합산 처리량은 더 높습니다. 반대로 **같은 TR을 반복**(연속조회 루프 등)할 때는 1 req/s에 수렴합니다 — 이 경우 [`request_all()`](#연속-조회-페이지네이션)을 쓰면 페이지네이션을 안전하게 자동 처리합니다.

## 자주 묻는 질문 (FAQ)

### 키움 앱키(appkey)와 시크릿키는 어떻게 발급받나요?

[키움 REST API 포털](https://openapi.kiwoom.com)에 로그인한 뒤 **API 사용신청** 메뉴에서 신청하면 `appkey`와 `secretkey`가 발급됩니다. 발급받은 키는 `.env`에 보관하고 코드에 직접 하드코딩하지 마세요. ([`.env.example`](.env.example) 참고)

### 모의투자에서 실전투자로 어떻게 전환하나요?

`KiwoomAPI` 생성 시 `is_mock` 값만 바꾸면 됩니다. `is_mock=True`(모의투자) → `is_mock=False`(실전투자). 서버 URL은 라이브러리가 자동으로 전환합니다. 실전 전환 전 반드시 모의투자로 충분히 검증하세요.

```python
api = KiwoomAPI(app_key="...", app_secret="...", is_mock=False)  # 실전투자
```

### 접근토큰(access token)이 만료되면 어떻게 하나요?

할 일이 없습니다. 토큰은 첫 호출에서 발급되고, 만료 60초 전에 선제 재발급되며, 그래도 API가 `401`을 돌려주면 재발급 후 한 번 더 시도합니다. 갱신 시점을 바꾸려면 `KiwoomAPI(..., expiry_margin=300)`처럼 조절하세요.

여러 프로세스가 토큰을 공유해야 한다면 `TokenProvider` 프로토콜(`get_valid_token()` / `refresh_token()`)을 구현해 넘기면 Redis 등 외부 캐시를 쓸 수 있습니다.

### Rate limit(호출 제한) 에러가 발생합니다.

내장 TR별 토큰 버킷 Rate Limiter가 호출 빈도를 자동 조절하고 `429` 발생 시 재시도까지 처리합니다(실측 기준 TR당 1 req/s, 버스트 2). 그래도 제한에 걸린다면 다중 프로세스/스레드에서 **같은 TR을 동시 호출** 중인지 확인하고, 연속조회는 `request_all()`로 한 번에 처리하세요. 자세한 내용은 [요청 제한 (Rate Limit)](#요청-제한-rate-limit)을 참고하세요.

### 조건검색(실시간)은 어떻게 사용하나요?

`api.condition_search`로 조건식 목록 조회·검색·실시간 등록/해제를 지원합니다. 실시간 조건검색은 WebSocket 기반으로 동작합니다. ([지원 API 목록](#조건검색-apicondition_search---4개-websocket) 참고)

### Windows가 아닌 macOS/Linux에서도 되나요?

네. REST/WebSocket 기반이라 OCX·COM이 필요 없어 macOS·Linux·서버(헤드리스) 환경에서 모두 동작합니다.

### pandas DataFrame으로 바로 받을 수 있나요?

`to_dataframe(result)` 한 줄이면 됩니다. 엔드포인트마다 다른 페이로드 키를 자동으로 찾고, `"+70000"` 같은 문자열도 숫자로 바꿔줍니다. [응답을 숫자·DataFrame으로 받기](#응답을-숫자dataframe으로-받기)와 [`examples/pandas_usage.py`](examples/pandas_usage.py)를 참고하세요.

### asyncio를 지원하나요?

네. `AsyncKiwoomAPI`가 `KiwoomAPI`와 같은 엔드포인트를 제공합니다. [asyncio 사용법](#asyncio-사용법)을 참고하세요.

## 환경 설정

| 구분 | 실전투자 | 모의투자 |
|------|---------|---------|
| `is_mock` | `False` (기본값) | `True` |
| REST URL | `https://api.kiwoom.com` | `https://mockapi.kiwoom.com` |
| WebSocket URL | `wss://api.kiwoom.com:10000` | `wss://mockapi.kiwoom.com:10000` |

## 지원 API 목록

### 인증

```python
api.login()      # 접근토큰 발급 (au10001)
api.logout()     # 접근토큰 폐기 (au10002)
```

### 페이지네이션 (연속조회)

```python
# 단일 조회
result = api.stock_info.basic_stock_info(stk_cd="005930")

# 연속 조회 (다음 페이지)
result = api.account.filled_orders(cont_yn="Y", next_key="다음키값")
```

---

### 계좌 (`api.account`) - 33개

| 메서드 | API ID | 설명 |
|--------|--------|------|
| `realized_profit_by_date()` | ka10072 | 일자별종목별실현손익요청_일자 |
| `realized_profit_by_period()` | ka10073 | 일자별종목별실현손익요청_기간 |
| `daily_realized_profit()` | ka10074 | 일자별실현손익요청 |
| `unfilled_orders()` | ka10075 | 미체결요청 |
| `filled_orders()` | ka10076 | 체결요청 |
| `today_realized_profit_detail()` | ka10077 | 당일실현손익상세요청 |
| `account_return_rate()` | ka10085 | 계좌수익률요청 |
| `unfilled_split_order_detail()` | ka10088 | 미체결 분할주문 상세 |
| `today_trading_journal()` | ka10170 | 당일매매일지요청 |
| `deposit_detail()` | kt00001 | 예수금상세현황요청 |
| `daily_estimated_deposit()` | kt00002 | 일별추정예탁자산현황요청 |
| `estimated_asset()` | kt00003 | 추정자산조회요청 |
| `account_evaluation()` | kt00004 | 계좌평가현황요청 |
| `filled_position()` | kt00005 | 체결잔고요청 |
| `order_execution_detail()` | kt00007 | 계좌별주문체결내역상세요청 |
| `next_day_settlement()` | kt00008 | 계좌별익일결제예정내역요청 |
| `order_execution_status()` | kt00009 | 계좌별주문체결현황요청 |
| `withdrawable_amount()` | kt00010 | 주문인출가능금액요청 |
| `orderable_qty_by_margin()` | kt00011 | 증거금율별주문가능수량조회요청 |
| `orderable_qty_by_credit()` | kt00012 | 신용보증금율별주문가능수량조회요청 |
| `margin_detail()` | kt00013 | 증거금세부내역조회요청 |
| `comprehensive_transaction_history()` | kt00015 | 위탁종합거래내역요청 |
| `daily_return_detail()` | kt00016 | 일별계좌수익률상세현황요청 |
| `today_account_status()` | kt00017 | 계좌별당일현황요청 |
| `evaluation_balance_detail()` | kt00018 | 계좌평가잔고내역요청 |
| `account_number_inquiry()` | ka00001 | 계좌번호조회 |
| `daily_balance_return_rate()` | ka01690 | 일별잔고수익률 |
| `gold_spot_balance()` | kt50020 | 금현물 잔고확인 |
| `gold_spot_deposit()` | kt50021 | 금현물 예수금 |
| `gold_spot_order_execution_all()` | kt50030 | 금현물 주문체결전체조회 |
| `gold_spot_order_execution()` | kt50031 | 금현물 주문체결조회 |
| `gold_spot_transaction_history()` | kt50032 | 금현물 거래내역조회 |
| `gold_spot_unfilled_orders()` | kt50075 | 금현물 미체결조회 |

### 종목정보 (`api.stock_info`) - 31개

| 메서드 | API ID | 설명 |
|--------|--------|------|
| `basic_stock_info()` | ka10001 | 주식기본정보요청 |
| `stock_trading_agent()` | ka10002 | 주식거래원요청 |
| `execution_info()` | ka10003 | 체결정보요청 |
| `credit_trading_trend()` | ka10013 | 신용매매동향요청 |
| `daily_transaction_detail()` | ka10015 | 일별거래상세요청 |
| `new_high_low()` | ka10016 | 신고저가요청 |
| `upper_lower_limit()` | ka10017 | 상하한가요청 |
| `near_high_low()` | ka10018 | 고저가근접요청 |
| `rapid_price_change()` | ka10019 | 가격급등락요청 |
| `trading_volume_update()` | ka10024 | 거래량갱신요청 |
| `volume_concentration()` | ka10025 | 매물대집중요청 |
| `high_low_per()` | ka10026 | 고저PER요청 |
| `change_rate_vs_opening()` | ka10028 | 시가대비등락률요청 |
| `trading_agent_supply_demand()` | ka10043 | 거래원매물대분석요청 |
| `trading_agent_instant_volume()` | ka10052 | 거래원순간거래량요청 |
| `vi_triggered_stocks()` | ka10054 | 변동성완화장치발동종목요청 |
| `today_vs_yesterday_volume()` | ka10055 | 당일전일체결량요청 |
| `daily_trading_by_investor()` | ka10058 | 투자자별일별매매종목요청 |
| `investor_institution_by_stock()` | ka10059 | 종목별투자자기관별요청 |
| `investor_institution_aggregate()` | ka10061 | 종목별투자자기관별합계요청 |
| `today_vs_yesterday_execution()` | ka10084 | 당일전일체결요청 |
| `watchlist_stock_info()` | ka10095 | 관심종목정보요청 |
| `stock_info_list()` | ka10099 | 종목정보 리스트 |
| `stock_info_inquiry()` | ka10100 | 종목정보 조회 |
| `industry_code_list()` | ka10101 | 업종코드 리스트 |
| `member_company_list()` | ka10102 | 회원사 리스트 |
| `program_buy_top50()` | ka90003 | 프로그램순매수상위50요청 |
| `program_trading_by_stock()` | ka90004 | 종목별프로그램매매현황요청 |
| `realtime_stock_inquiry_rank()` | ka00198 | 실시간종목조회순위 |
| `margin_loan_available_stocks()` | kt20016 | 신용융자 가능종목요청 |
| `margin_loan_inquiry()` | kt20017 | 신용융자 가능문의 |

### 시세 (`api.market`) - 25개

| 메서드 | API ID | 설명 |
|--------|--------|------|
| `stock_quote()` | ka10004 | 주식호가요청 |
| `stock_daily_weekly_monthly()` | ka10005 | 주식일주월시분요청 |
| `stock_minute_price()` | ka10006 | 주식시분요청 |
| `order_book_info()` | ka10007 | 시세표성정보요청 |
| `rights_issue_price()` | ka10011 | 신주인수권전체시세요청 |
| `daily_institutional_trading()` | ka10044 | 일별기관매매종목요청 |
| `institutional_trading_trend()` | ka10045 | 종목별기관매매추이요청 |
| `hourly_execution_strength()` | ka10046 | 체결강도추이시간별요청 |
| `daily_execution_strength()` | ka10047 | 체결강도추이일별요청 |
| `intraday_investor_trading()` | ka10063 | 장중투자자별매매요청 |
| `after_hours_investor_trading()` | ka10066 | 장마감후투자자별매매요청 |
| `broker_stock_trading_trend()` | ka10078 | 증권사별종목매매동향요청 |
| `daily_stock_price()` | ka10086 | 일별주가요청 |
| `after_hours_single_price()` | ka10087 | 시간외단일가요청 |
| `program_trading_by_time()` | ka90005 | 프로그램매매추이요청 시간대별 |
| `program_arbitrage_balance()` | ka90006 | 프로그램매매차익잔고추이요청 |
| `cumulative_program_trading()` | ka90007 | 프로그램매매누적추이요청 |
| `program_trading_by_stock_time()` | ka90008 | 종목시간별프로그램매매추이요청 |
| `program_trading_by_date()` | ka90010 | 프로그램매매추이요청 일자별 |
| `program_trading_by_stock_day()` | ka90013 | 종목일별프로그램매매추이요청 |
| `gold_spot_execution_trend()` | ka50010 | 금현물체결추이 |
| `gold_spot_daily_trend()` | ka50012 | 금현물일별추이 |
| `gold_spot_expected_execution()` | ka50087 | 금현물예상체결 |
| `gold_spot_price_info()` | ka50100 | 금현물 시세정보 |
| `gold_spot_order_book()` | ka50101 | 금현물 호가 |

### 주문 (`api.order`) - 8개

| 메서드 | API ID | 설명 |
|--------|--------|------|
| `buy_order()` | kt10000 | 주식 매수주문 |
| `sell_order()` | kt10001 | 주식 매도주문 |
| `modify_order()` | kt10002 | 주식 정정주문 |
| `cancel_order()` | kt10003 | 주식 취소주문 |
| `gold_spot_buy_order()` | kt50000 | 금현물 매수주문 |
| `gold_spot_sell_order()` | kt50001 | 금현물 매도주문 |
| `gold_spot_modify_order()` | kt50002 | 금현물 정정주문 |
| `gold_spot_cancel_order()` | kt50003 | 금현물 취소주문 |

### 신용주문 (`api.credit_order`) - 4개

| 메서드 | API ID | 설명 |
|--------|--------|------|
| `margin_buy_order()` | kt10006 | 신용 매수주문 |
| `margin_sell_order()` | kt10007 | 신용 매도주문 |
| `margin_modify_order()` | kt10008 | 신용 정정주문 |
| `margin_cancel_order()` | kt10009 | 신용 취소주문 |

### 차트 (`api.chart`) - 21개

| 메서드 | API ID | 설명 |
|--------|--------|------|
| `investor_institution_chart()` | ka10060 | 종목별투자자기관별차트요청 |
| `intraday_investor_chart()` | ka10064 | 장중투자자별매매차트요청 |
| `stock_tick_chart()` | ka10079 | 주식틱차트조회요청 |
| `stock_minute_chart()` | ka10080 | 주식분봉차트조회요청 |
| `stock_daily_chart()` | ka10081 | 주식일봉차트조회요청 |
| `stock_weekly_chart()` | ka10082 | 주식주봉차트조회요청 |
| `stock_monthly_chart()` | ka10083 | 주식월봉차트조회요청 |
| `stock_yearly_chart()` | ka10094 | 주식년봉차트조회요청 |
| `industry_tick_chart()` | ka20004 | 업종틱차트조회요청 |
| `industry_minute_chart()` | ka20005 | 업종분봉조회요청 |
| `industry_daily_chart()` | ka20006 | 업종일봉조회요청 |
| `industry_weekly_chart()` | ka20007 | 업종주봉조회요청 |
| `industry_monthly_chart()` | ka20008 | 업종월봉조회요청 |
| `industry_yearly_chart()` | ka20019 | 업종년봉조회요청 |
| `gold_spot_tick_chart()` | ka50079 | 금현물틱차트조회요청 |
| `gold_spot_minute_chart()` | ka50080 | 금현물분봉차트조회요청 |
| `gold_spot_daily_chart()` | ka50081 | 금현물일봉차트조회요청 |
| `gold_spot_weekly_chart()` | ka50082 | 금현물주봉차트조회요청 |
| `gold_spot_monthly_chart()` | ka50083 | 금현물월봉차트조회요청 |
| `gold_spot_intraday_tick_chart()` | ka50091 | 금현물당일틱차트조회요청 |
| `gold_spot_intraday_minute_chart()` | ka50092 | 금현물당일분봉차트조회요청 |

### 순위정보 (`api.ranking`) - 23개

| 메서드 | API ID | 설명 |
|--------|--------|------|
| `top_order_book_volume()` | ka10020 | 호가잔량상위요청 |
| `sudden_order_book_increase()` | ka10021 | 호가잔량급증요청 |
| `sudden_order_ratio_increase()` | ka10022 | 잔량율급증요청 |
| `sudden_volume_increase()` | ka10023 | 거래량급증요청 |
| `top_change_rate()` | ka10027 | 전일대비등락률상위요청 |
| `top_expected_change_rate()` | ka10029 | 예상체결등락률상위요청 |
| `top_volume_today()` | ka10030 | 당일거래량상위요청 |
| `top_volume_yesterday()` | ka10031 | 전일거래량상위요청 |
| `top_trading_value()` | ka10032 | 거래대금상위요청 |
| `top_credit_ratio()` | ka10033 | 신용비율상위요청 |
| `top_foreign_trades_by_period()` | ka10034 | 외인기간별매매상위요청 |
| `top_foreign_consecutive_buy()` | ka10035 | 외인연속순매매상위요청 |
| `top_foreign_limit_increase()` | ka10036 | 외인한도소진율증가상위 |
| `top_foreign_broker_trading()` | ka10037 | 외국계창구매매상위요청 |
| `broker_ranking_by_stock()` | ka10038 | 종목별증권사순위요청 |
| `top_broker_by_stock()` | ka10039 | 증권사별매매상위요청 |
| `main_brokers_today()` | ka10040 | 당일주요거래원요청 |
| `top_net_buying_brokers()` | ka10042 | 순매수거래원순위요청 |
| `departed_brokers_today()` | ka10053 | 당일상위이탈원요청 |
| `same_day_net_buying_rank()` | ka10062 | 동일순매매순위요청 |
| `top_intraday_investor_trading()` | ka10065 | 장중투자자별매매상위요청 |
| `after_hours_change_rate_rank()` | ka10098 | 시간외단일가등락율순위요청 |
| `top_foreign_institution_trades()` | ka90009 | 외국인기관매매상위요청 |

### 업종 (`api.sector`) - 6개

| 메서드 | API ID | 설명 |
|--------|--------|------|
| `industry_program_trading()` | ka10010 | 업종프로그램요청 |
| `industry_investor_net_buy()` | ka10051 | 업종별투자자순매수요청 |
| `industry_current_price()` | ka20001 | 업종현재가요청 |
| `industry_stock_price()` | ka20002 | 업종별주가요청 |
| `all_industry_index()` | ka20003 | 전업종지수요청 |
| `industry_daily_price()` | ka20009 | 업종현재가일별요청 |

### 기관/외국인 (`api.foreign_institution`) - 4개

| 메서드 | API ID | 설명 |
|--------|--------|------|
| `foreign_trading_trend()` | ka10008 | 주식외국인종목별매매동향 |
| `institutional_stock()` | ka10009 | 주식기관요청 |
| `consecutive_trading_status()` | ka10131 | 기관외국인연속매매현황요청 |
| `gold_spot_investor_status()` | ka52301 | 금현물투자자현황 |

### 공매도 (`api.short_selling`) - 1개

| 메서드 | API ID | 설명 |
|--------|--------|------|
| `short_selling_trend()` | ka10014 | 공매도추이요청 |

### 대차거래 (`api.slb`) - 4개

| 메서드 | API ID | 설명 |
|--------|--------|------|
| `lending_trend()` | ka10068 | 대차거래추이요청 |
| `top10_lending()` | ka10069 | 대차거래상위10종목요청 |
| `lending_trend_by_stock()` | ka20068 | 대차거래추이요청(종목별) |
| `lending_details()` | ka90012 | 대차거래내역요청 |

### 테마 (`api.theme`) - 2개

| 메서드 | API ID | 설명 |
|--------|--------|------|
| `theme_group_list()` | ka90001 | 테마그룹별요청 |
| `theme_component_stocks()` | ka90002 | 테마구성종목요청 |

### 조건검색 (`api.condition_search`) - 4개 (WebSocket)

| 메서드 | API ID | 설명 |
|--------|--------|------|
| `condition_list()` | ka10171 | 조건검색 목록조회 |
| `condition_search()` | ka10172 | 조건검색 요청 일반 |
| `condition_search_realtime()` | ka10173 | 조건검색 요청 실시간 |
| `condition_search_cancel()` | ka10174 | 조건검색 실시간 해제 |

### ELW (`api.elw`) - 11개

| 메서드 | API ID | 설명 |
|--------|--------|------|
| `daily_sensitivity_indicator()` | ka10048 | ELW일별민감도지표요청 |
| `sensitivity_indicator()` | ka10050 | ELW민감도지표요청 |
| `price_spike()` | ka30001 | ELW가격급등락요청 |
| `top_net_buying_by_broker()` | ka30002 | 거래원별ELW순매매상위요청 |
| `lp_daily_holding_trend()` | ka30003 | ELWLP보유일별추이요청 |
| `premium_rate()` | ka30004 | ELW괴리율요청 |
| `condition_search()` | ka30005 | ELW조건검색요청 |
| `change_rate_ranking()` | ka30009 | ELW등락율순위요청 |
| `order_volume_ranking()` | ka30010 | ELW잔량순위요청 |
| `proximity_rate()` | ka30011 | ELW근접율요청 |
| `detailed_stock_info()` | ka30012 | ELW종목상세정보요청 |

### ETF (`api.etf`) - 9개

| 메서드 | API ID | 설명 |
|--------|--------|------|
| `return_rate()` | ka40001 | ETF수익율요청 |
| `stock_info()` | ka40002 | ETF종목정보요청 |
| `daily_trend()` | ka40003 | ETF일별추이요청 |
| `overall_market_price()` | ka40004 | ETF전체시세요청 |
| `time_segment_trend()` | ka40006 | ETF시간대별추이요청 |
| `time_segment_execution()` | ka40007 | ETF시간대별체결요청 |
| `daily_execution()` | ka40008 | ETF일자별체결요청 |
| `time_nav()` | ka40009 | ETF시간대별체결요청 |
| `time_trend()` | ka40010 | ETF시간대별추이요청 |

### 실시간시세 (`api.create_websocket()`) - 19종

| 코드 | 설명 |
|------|------|
| 00 | 주문체결 |
| 04 | 잔고 |
| 0A | 주식기세 |
| 0B | 주식체결 |
| 0C | 주식우선호가 |
| 0D | 주식호가잔량 |
| 0E | 주식시간외호가 |
| 0F | 주식당일거래원 |
| 0G | ETF NAV |
| 0H | 주식예상체결 |
| 0I | 국제금환산가격 |
| 0J | 업종지수 |
| 0U | 업종등락 |
| 0g | 주식종목정보 |
| 0m | ELW 이론가 |
| 0s | 장시작시간 |
| 0u | ELW 지표 |
| 0w | 종목프로그램매매 |
| 1h | VI발동/해제 |

## 참고

- 공식 API 가이드: https://openapi.kiwoom.com/guide/apiguide
- 모의투자는 KRX만 지원됩니다.
- 모든 API 이름은 키움증권 공식 가이드 기준입니다.

## 라이선스

MIT

---

## ⭐ 도움이 되셨다면

이 라이브러리가 유용했다면 우측 상단 **[⭐ Star](https://github.com/younghwan91/kiwoom-rest-api)** 를 눌러주세요. 검색·추천 노출이 올라가 더 많은 개발자가 찾을 수 있습니다.

- 🐛 버그·질문 → [Issues](https://github.com/younghwan91/kiwoom-rest-api/issues)
- 🔧 개선 → PR 환영 ([CONTRIBUTING](CONTRIBUTING.md))
- 📈 새 엔드포인트·기능 업데이트 소식을 받으려면 [팔로우](https://github.com/younghwan91)

## 관련 프로젝트 — 한국 주식 퀀트 스택

이 라이브러리는 제가 오픈소스로 공개하는 **한국 주식 퀀트 스택**의 일부입니다. 시세·펀더멘탈·뉴스 수집부터 데이터 파이프라인, 알파 리서치까지 이어집니다.

| 프로젝트 | 설명 |
|---|---|
| **[krx-fundamentals-api](https://github.com/younghwan91/krx-fundamentals-api)** | 국내 기업 펀더멘탈 REST API — 재무제표·투자지표·배당·종목 스크리닝 (DART + KRX + 네이버) |
| **[krx-news-rest-api](https://github.com/younghwan91/krx-news-rest-api)** | 한국 주식 뉴스·공시 수집 REST API (FastAPI + Redis) |
| **[kr-quant-airflow](https://github.com/younghwan91/kr-quant-airflow)** | 시세·수급·실적 데이터를 TimescaleDB로 수집하는 Airflow 파이프라인 |
| **[kr-quant](https://github.com/younghwan91/kr-quant)** | 코스피·코스닥 알파 리서치 — walk-forward·랜덤 음성대조를 강제하는 검증 가드레일 |
| **[opt_portfolio](https://github.com/younghwan91/opt_portfolio)** | VAA 기반 전술적 자산배분 백테스트·운용 시스템 |
| **[automated-stock-trading-systems](https://github.com/younghwan91/automated-stock-trading-systems)** | Bensdorp의 7개 비상관 트레이딩 시스템 백테스터 (교육용 재구현) |
| **[quantbox-engine](https://github.com/younghwan91/quantbox-engine)** | 암호화폐 선물 백테스트·실행 엔진 — 룩어헤드 0, 백테스트↔실거래 일체화 |

## 만든 사람

**채영환 (Younghwan Chae)** · [GitHub @younghwan91](https://github.com/younghwan91) · [LinkedIn](https://www.linkedin.com/in/younghwan-chae/)

전체 오픈소스 퀀트 스택은 [프로필](https://github.com/younghwan91)에서 한눈에 볼 수 있습니다.
