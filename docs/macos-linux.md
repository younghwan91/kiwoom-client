---
seo_title: "맥·리눅스에서 키움증권 API 쓰기 — OCX 없이 REST 로 파이썬 자동매매"
description: "키움 OpenAPI+(OCX)는 Windows 전용이지만 키움 REST API 는 macOS·Linux·서버에서 됩니다. 앱키 발급부터 pip 설치, 첫 시세 조회, 일봉 DataFrame, 실시간 체결, 서버에서 돌리기까지."
---

# 맥·리눅스에서 키움증권 API 쓰기

키움증권 **OpenAPI+** 는 Windows COM/OCX 컨트롤이라 맥·리눅스에서는 돌지 않고, 오랫동안 32bit 파이썬에 묶여
있었습니다. 키움 **REST API** 는 HTTPS(JSON)와 WebSocket 이라 운영체제를 가리지 않습니다. 이 페이지는 macOS 나
Linux 에서 설치부터 첫 조회까지 순서대로 따라가는 안내입니다. 두 방식의 차이는 [왜 kiwoom-client 인가](why.md),
OpenAPI+ 코드를 옮길 때는 [OpenAPI+ · pykiwoom 에서 옮겨 오기](migration-from-openapi-plus.md)를 보세요.

| 필요한 것 | 비고 |
|---|---|
| 키움증권 계좌 | API 사용신청에 필요 |
| 앱키·시크릿키 | [키움 REST API 포털](https://openapi.kiwoom.com)에서 API 사용신청. **모의투자용과 실전투자용 키가 따로** 나옵니다 |
| 파이썬 3.10 이상 (64bit) | macOS·Linux 기본 파이썬, Homebrew·pyenv·uv 어느 것이든 |
| Windows·OCX·로그인 창 | 필요 없음 |

## 1. 설치

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install 'kiwoom-client[pandas]'   # DataFrame 변환까지. 기본만이면 kiwoom-client
```

uv 를 쓴다면 `uv add 'kiwoom-client[pandas]'`.

## 2. 키를 환경변수로

키를 코드에 적지 말고 환경변수나 `.env` 파일에 둡니다. MCP 서버도 같은 이름을 씁니다.

```bash
export KIWOOM_APP_KEY=발급받은_앱키
export KIWOOM_APP_SECRET=발급받은_시크릿키
export KIWOOM_IS_MOCK=true          # 모의투자 키라면
```

!!! warning "기본값은 실서버입니다"
    `is_mock` 을 어디에도 주지 않으면 **실전투자 서버**에 붙습니다. 처음에는 코드에서 `is_mock=True` 를 직접 넘기세요.
    모의투자 키로 실서버에 붙으면(또는 그 반대) 인증이 거부됩니다(8030/8031 — [문제 해결](troubleshooting.md)).

## 3. 첫 조회

```python
from kiwoom_client import KiwoomAPI

api = KiwoomAPI.from_env(is_mock=True)   # 토큰 발급·갱신은 라이브러리가 한다

info = api.stock_info.basic_stock_info(stk_cd="005930")   # ka10001 주식기본정보
print(info["stk_nm"], info["cur_prc"])
```

종목명으로 코드를 찾으려면 `api.stock_code("삼성전자")`. 쓸 수 있는 TR 182개는
[엔드포인트 전체 목록](endpoints.md)에 api_id·한글 이름·메서드로 정리돼 있습니다.

명령줄에서 바로 확인할 수도 있습니다(조회 전용 — 주문 명령은 없습니다).

```bash
kiwoom quote 005930 --mock
kiwoom chart 005930 --daily -n 5 --mock
```

## 4. 일봉을 DataFrame 으로

```python
from kiwoom_client import to_ohlcv

resp = api.chart.stock_daily_chart(stk_cd="005930", base_dt="20260327", upd_stkpc_tp="1")
df = to_ohlcv(resp)   # open/high/low/close/volume, 날짜 인덱스, 오래된 순
print(df.tail())
```

한 번에 다 안 오는 TR 은 응답의 `cont-yn`·`next-key` 로 이어 받습니다 — [연속조회를 끝까지](cookbook/pagination.md).

## 5. 실시간 체결 (WebSocket)

```python
import asyncio

from kiwoom_client import KiwoomAPI


async def main():
    api = KiwoomAPI.from_env(is_mock=True)
    ws = api.create_websocket()
    await ws.connect()                                   # LOGIN 까지
    ws.on("0B", lambda d: print(d["item"], d["values"].get("10")))   # 10 = 현재가
    await ws.subscribe("0B", "005930")
    await ws.listen()                                    # PING·재연결·구독 복원 포함


asyncio.run(main())
```

자세한 것은 [WebSocket 으로 실시간 체결·호가 받기](cookbook/realtime-trades.md).

## 6. 서버에서 돌리기 (cron · systemd · Docker)

로그인 창이 없으니 화면 없는 Linux 서버·컨테이너에서 그대로 돕니다. 키는 환경변수로 넘기면 됩니다.

```bash
docker run --rm --env-file .env python:3.12-slim \
  sh -c "pip install -q kiwoom-client && kiwoom quote 005930 --mock"
```

- **토큰은 받은 IP 에서만 씁니다.** 한 곳에서 받은 토큰을 다른 서버에서 쓰거나, 나가는 IP 가 바뀌는 NAT 뒤라면
  8010 오류가 납니다 — 프로세스마다 자기 토큰을 받게 두세요([문제 해결](troubleshooting.md)).
- 호출 제한은 TR 마다 따로입니다. 기본 Rate Limiter 가 맞춰 주고, 넘치면 429 를 재시도합니다
  — [호출 제한(429) 다루기](cookbook/rate-limits.md).
- 실계좌 키로 `api.order.*`·`api.credit_order.*` 를 부르면 그대로 주문이 나갑니다. 자동매매는 모의투자로 충분히
  돌려 본 뒤에 실전 키로 바꾸세요 — [호가단위에 맞춘 지정가 주문](cookbook/limit-order.md).

## 다음

- AI 에이전트에서 쓰기: [MCP 서버](mcp.md) — Claude Code·Cursor 가 시세·계좌를 조회
- 막히면: [문제 해결](troubleshooting.md) · [FAQ](faq.md)
