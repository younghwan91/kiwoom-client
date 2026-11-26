---
seo_title: "10분 만에 키움 조건검색 가격 알림 봇 (파이썬, 키 없이 데모로)"
description: "kiwoom-client 데모 모드로 키움 계좌·앱키 없이 바로 돌아가는 조건검색 + 실시간 가격 알림 봇을 만듭니다. 영웅문4 조건식으로 종목을 고르고 WebSocket 체결로 가격 변동을 알립니다. 주문은 하지 않습니다."
---

# 10분 만에 조건검색 알림 봇

영웅문4에 저장해 둔 조건식으로 종목을 고르고, 그 종목들의 실시간 체결을 지켜보다가 가격이 일정 비율 움직이면
알림을 띄우는 봇을 만듭니다. 파이썬 파일 하나, 60줄 정도입니다.

- **키 없이 시작합니다.** `KiwoomAPI.demo()` 는 프로세스 안의 가짜 키움 서버에 붙습니다. 실제 종목명·코드에 가상 시세가
  나오고, 네트워크에 아무것도 보내지 않습니다. 응답마다 `"_demo"` 표시가 붙습니다(실제 시세가 아닙니다).
- **주문은 하지 않습니다.** 이 봇은 조건검색과 실시간 시세만 씁니다.
- 다 만든 뒤 실제 계좌로 돌릴 때는 클라이언트를 만드는 한 줄만 바꿉니다([실제 계좌로](#실제-계좌로)).

## 준비 (1분)

```bash
pip install kiwoom-client
```

Python 3.10 이상이면 됩니다. 아래 코드 블록을 위에서부터 차례로 `alert_bot.py` 한 파일에 붙여 넣으세요.

## 1. 설정과 클라이언트

```python
import asyncio

from kiwoom_client import KiwoomAPI

CONDITION = "급등주"  # 영웅문4에 저장한 조건식 이름 (일부만 써도 된다)
ALERT_PCT = 0.5       # 조건검색 때 가격에서 이만큼(%) 움직이면 알림
SECONDS = 30          # 감시할 시간(초)

api = KiwoomAPI.demo()  # 가상 데이터 — 키·계좌·네트워크 없이 돈다
print("데모 모드:", api.is_demo)
```

데모 계좌에는 조건식 네 개(`급등주`·`거래량 급증`·`52주 신고가 근접`·`대형 우량주`)가 저장돼 있습니다.

## 2. 요청 하나 보내고 답 기다리기

조건검색은 REST 가 아니라 실시간과 같은 WebSocket 으로 주고받습니다. 요청을 보내면 응답이 `trnm`(`CNSRLST` 조건식 목록,
`CNSRREQ` 검색 결과)을 달고 따로 돌아오므로, 보내고 그 `trnm` 의 첫 응답을 기다리는 작은 함수를 둡니다.

```python
async def ask(ws, trnm, message):
    """WebSocket 요청 하나를 보내고 같은 trnm 의 첫 응답을 기다린다."""
    reply = asyncio.get_running_loop().create_future()
    ws.on_trnm(trnm, lambda frame: reply.done() or reply.set_result(frame))
    await ws.send(message)
    return await asyncio.wait_for(reply, timeout=10)
```

## 3. 조건식으로 종목 고르기

조건식 목록에서 이름으로 번호(`seq`)를 찾고, 한 번 실행해 걸린 종목의 코드·이름·현재가를 받습니다.
응답 행의 키는 FID 번호입니다(`9001` 종목코드, `302` 종목명, `10` 현재가).

```python
async def find_stocks(ws, name):
    """조건식 이름으로 번호(seq)를 찾아 한 번 실행하고, 걸린 종목을 돌려준다."""
    listing = await ask(ws, "CNSRLST", api.condition_search.condition_list())
    seq = next(s for s, n in listing["data"] if name in n)
    result = await ask(ws, "CNSRREQ", api.condition_search.condition_search(seq=seq))
    stocks = {}
    for row in result["data"]:
        code = row["9001"].lstrip("A")  # "A005930" → "005930"
        stocks[code] = {"name": row["302"], "start": abs(int(row["10"]))}  # "000071900" → 71900
    return stocks
```

## 4. 가격 알림 콜백

실시간 체결(`0B`)이 올 때마다 불리는 콜백입니다. `named=True` 로 등록하면 `values` 키가 FID 번호 대신
한글 필드명(`"현재가"`)이 됩니다. 종목마다 한 번만 알립니다.

```python
def make_alert(stocks, pct):
    """체결이 올 때마다 불리는 콜백. 종목마다 한 번만 알린다."""
    alerted = set()

    def on_trade(item):
        code = item["item"]
        price = abs(int(item["values"]["현재가"]))  # "+71900": 부호는 전일 대비 방향
        info = stocks[code]
        move = (price - info["start"]) / info["start"] * 100
        if abs(move) >= pct and code not in alerted:
            alerted.add(code)
            notify(f"{info['name']}({code}) {price:,}원 — 조건검색 때보다 {move:+.2f}%")

    return on_trade, alerted


def notify(text):
    print("[알림]", text)  # 슬랙 웹훅·메일·로그 파일 등으로 바꿔 끼운다
```

## 5. 묶어서 돌리기

```python
async def main():
    ws = api.create_websocket()
    async with ws:  # LOGIN 부터 종료까지
        listener = asyncio.create_task(ws.listen())  # 응답·체결을 받아 콜백에 넘긴다
        stocks = await find_stocks(ws, CONDITION)
        for code, info in stocks.items():
            print(f"{info['name']}({code}) {info['start']:,}원")
        on_trade, alerted = make_alert(stocks, ALERT_PCT)
        ws.on("0B", on_trade, named=True)
        await ws.subscribe("0B", list(stocks))
        await asyncio.sleep(SECONDS)
    await listener
    print(f"{SECONDS}초 동안 {len(alerted)}종목 알림")


asyncio.run(main())
```

```bash
python alert_bot.py
```

데모에서 돌린 출력입니다(가상 시세). 데모 시세는 날짜에 따라 만들어지므로 돌리는 날에 따라 종목과 가격이 달라집니다.

```text
데모 모드: True
LG화학(051910) 284,500원
삼성물산(028260) 132,400원
SK하이닉스(000660) 182,000원
POSCO홀딩스(005490) 312,000원
현대차(005380) 214,500원
[알림] 현대차(005380) 216,000원 — 조건검색 때보다 +0.70%
[알림] POSCO홀딩스(005490) 310,000원 — 조건검색 때보다 -0.64%
[알림] LG화학(051910) 283,000원 — 조건검색 때보다 -0.53%
[알림] 삼성물산(028260) 131,700원 — 조건검색 때보다 -0.53%
[알림] SK하이닉스(000660) 183,000원 — 조건검색 때보다 +0.55%
30초 동안 5종목 알림
```

## 실제 계좌로

1. [키움 REST API 포털](https://openapi.kiwoom.com)에서 앱키·시크릿키를 받아 환경변수 `KIWOOM_APP_KEY`·`KIWOOM_APP_SECRET` 에 넣습니다.
2. 영웅문4에서 쓸 조건식을 저장하고, `CONDITION` 을 그 이름으로 바꿉니다.
3. 1단계의 클라이언트 한 줄을 바꿉니다.

<!-- docs-test: no-exec -->
```python
api = KiwoomAPI.from_env(is_mock=True)  # 모의투자 키. 실전 키면 is_mock=False
```

나머지 코드는 그대로입니다. 알아 둘 점:

- 이 봇은 주문 메서드를 부르지 않으므로 실전 키로 돌려도 조회만 합니다. 여기에 `api.order.*` 를 더하면 실전 키에서는
  그대로 실주문이 나갑니다(파이썬 직접 호출에는 가드가 없습니다).
- 실시간 체결은 장중에만 들어옵니다. 장 밖에서는 종목 목록만 찍히고 알림 없이 끝납니다.
- 오래 돌릴 때는 `listen()` 이 PING 응답·재연결·구독 복원을 맡습니다. 조건검색 결과를 실시간으로 계속 받으려면
  [조건검색 결과를 실시간으로](../cookbook/condition-search-realtime.md)를 보세요.

## 다음 단계

- 알림을 사람에게 보내려면 `notify()` 를 슬랙 웹훅이나 메일로 바꿉니다. 알림은 본인만 받는 용도로 쓰세요. 남에게 매매 신호로
  돌리는 서비스는 투자자문 규제에 걸릴 수 있습니다.
- 체결 대신 호가를 보려면 `0D`(주식호가잔량)를 구독합니다([실시간 체결·호가](../cookbook/realtime-trades.md)).
- 같은 일을 Claude 에 시키려면 MCP 서버의 `condition_search_run`·`watch` 도구를 씁니다
  ([프롬프트 모음](../prompts.md)의 13·14번).

<small>코드 블록은 테스트(`tests/test_tutorial_exec.py`)가 데모 백엔드로 실제 실행합니다.</small>
