# Real-time trades and order book over WebSocket

Real-time quotes come over a single WebSocket, not REST. The steps are always the same:
`create_websocket()` → `connect()` (through LOGIN) → `on(type, callback)` → `subscribe(type, codes)` → `listen()`.

| Type | Name | Common FIDs (keys of `values`) |
|---|---|---|
| `0B` | Stock trade (주식체결) | `20` trade time, `10` current price, `15` volume (+buy/−sell), `13` cumulative volume, `12` change rate, `228` execution strength |
| `0D` | Order book (주식호가잔량) | `21` quote time, `41`–`50` ask 1–10, `51`–`60` bid 1–10, `61`/`71` ask/bid quantity 1 |
| `0C` | Best bid/ask (주식우선호가) | `27` (best) ask, `28` (best) bid |

FID names follow Kiwoom's official REST spec; all types are in the
[real-time section of the endpoint reference](../endpoints.md#realtime).

## Receive trades and keep the last price

```python
import asyncio

from kiwoom_client import KiwoomAPI, to_number

last_price: dict[str, int] = {}


def on_trade(d: dict) -> None:
    v = d["values"]
    price = abs(to_number(v.get("10", "0")))  # the sign is the direction vs. the previous close
    last_price[d["item"]] = price
    print(f"{v.get('20')} {d['item']} {price:>9,} volume {v.get('15')}")


async def main():
    api = KiwoomAPI.from_env(is_mock=True)
    ws = api.create_websocket()
    await ws.connect()                      # KiwoomWebSocketError if LOGIN fails
    ws.on("0B", on_trade)
    await ws.subscribe("0B", ["005930", "000660"])

    listener = asyncio.create_task(ws.listen())  # listen() answers PING, reconnects, restores subscriptions
    await asyncio.sleep(60)                 # receive for one minute
    await ws.disconnect()                   # then stop
    await listener
    print(last_price)


asyncio.run(main())
```

## The order book on the same socket

```python
import asyncio

from kiwoom_client import KiwoomAPI


def on_book(d: dict) -> None:
    v = d["values"]
    print(d["item"], "ask1", v.get("41"), "x", v.get("61"), "| bid1", v.get("51"), "x", v.get("71"))


async def main():
    api = KiwoomAPI.from_env(is_mock=True)
    async with api.create_websocket() as ws:   # disconnect() on exit
        ws.on("0D", on_book)
        await ws.subscribe(["0B", "0D"], "005930")
        await ws.listen()


asyncio.run(main())
```

- Callbacks can be plain functions or `async def`. If a callback raises, the other callbacks and receiving keep going
  (the error is logged).
- `subscribe(..., refresh="1")` (the default) keeps existing registrations and adds to them. With `"0"` it clears the
  existing registrations and keeps only this one.
- To get Korean field names instead of FID numbers, `ws.on("0B", on_trade, named=True)` — the callback's `values` keys
  become `"현재가"` (current price), `"체결시간"` (trade time) and so on (values stay strings; FIDs the spec does not know
  keep their number). Other callbacks for the same type still get FID keys.
- To remove a registration, `await ws.unsubscribe("0B", "005930")`.
- To see every frame, `ws.on_message(callback)` — when a REAL frame arrives you get the whole `data` list.
- The field names of the items (`item`/`values`) match the official spec's example, but this library has not yet
  confirmed them on the live server during market hours (the "Verification status" note in the README). If something
  looks off, please open an issue.
