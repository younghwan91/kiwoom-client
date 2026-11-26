# WebSocket 으로 실시간 체결·호가 받기

실시간 시세는 REST 가 아니라 WebSocket 하나로 받습니다. 순서는 늘 같습니다:
`create_websocket()` → `connect()`(LOGIN 까지) → `on(타입, 콜백)` → `subscribe(타입, 종목)` → `listen()`.

| 타입 | 이름 | 자주 쓰는 FID (`values` 의 키) |
|---|---|---|
| `0B` | 주식체결 | `20` 체결시간, `10` 현재가, `15` 거래량(+매수/−매도), `13` 누적거래량, `12` 등락율, `228` 체결강도 |
| `0D` | 주식호가잔량 | `21` 호가시간, `41`~`50` 매도호가1~10, `51`~`60` 매수호가1~10, `61`/`71` 매도·매수호가수량1 |
| `0C` | 주식우선호가 | `27` (최우선)매도호가, `28` (최우선)매수호가 |

FID 이름은 키움 공식 REST 스펙 기준이고, 전체 타입은 [엔드포인트 표의 실시간 절](../endpoints.md#realtime)에 있습니다.

## 체결을 받아 마지막 가격 들고 있기

```python
import asyncio

from kiwoom_client import KiwoomAPI, to_number

last_price: dict[str, int] = {}


def on_trade(d: dict) -> None:
    v = d["values"]
    price = abs(to_number(v.get("10", "0")))  # 부호는 전일 대비 방향
    last_price[d["item"]] = price
    print(f"{v.get('20')} {d['item']} {price:>9,} 거래량 {v.get('15')}")


async def main():
    api = KiwoomAPI.from_env(is_mock=True)
    ws = api.create_websocket()
    await ws.connect()                      # LOGIN 실패면 KiwoomWebSocketError
    ws.on("0B", on_trade)
    await ws.subscribe("0B", ["005930", "000660"])

    listener = asyncio.create_task(ws.listen())  # PING 응답·재연결·구독 복원은 listen() 이 한다
    await asyncio.sleep(60)                 # 1분만 받고
    await ws.disconnect()                   # 멈춘다
    await listener
    print(last_price)


asyncio.run(main())
```

## 호가를 같은 소켓에

```python
import asyncio

from kiwoom_client import KiwoomAPI


def on_book(d: dict) -> None:
    v = d["values"]
    print(d["item"], "매도1", v.get("41"), "x", v.get("61"), "| 매수1", v.get("51"), "x", v.get("71"))


async def main():
    api = KiwoomAPI.from_env(is_mock=True)
    async with api.create_websocket() as ws:   # 나갈 때 disconnect()
        ws.on("0D", on_book)
        await ws.subscribe(["0B", "0D"], "005930")
        await ws.listen()


asyncio.run(main())
```

- 콜백은 보통 함수와 `async def` 둘 다 됩니다. 콜백 안에서 예외가 나도 다른 콜백과 수신은 계속됩니다(로그에 남음).
- `subscribe(..., refresh="1")`(기본)은 기존 등록을 유지하고 더합니다. `"0"` 이면 기존 등록을 지우고 이것만 남깁니다.
- FID 번호 대신 한글 필드명으로 받으려면 `ws.on("0B", on_trade, named=True)` — 콜백이 받는 `values` 키가
  `"현재가"`, `"체결시간"` 처럼 바뀝니다(값은 문자열 그대로, 스펙에 없는 FID 는 번호로 남음). 같은 타입의 다른 콜백은 FID 키를 그대로 받습니다.
- 등록을 빼려면 `await ws.unsubscribe("0B", "005930")`.
- 모든 프레임을 보고 싶으면 `ws.on_message(콜백)` — REAL 프레임이 오면 `data` 리스트 전체를 받습니다.
- `values` 의 필드 이름(`item`/`values`)은 공식 스펙 예시와 같지만, 이 라이브러리는 장중 실서버에서는 아직 확인하지 못했습니다
  (README "검증 상태"). 이상하면 이슈로 알려 주세요.
