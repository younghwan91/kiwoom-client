---
seo_title: "A Kiwoom condition-search price alert bot in 10 minutes (Python, keyless demo)"
description: "Build a condition-search plus real-time price alert bot with kiwoom-client that runs right away in demo mode, with no Kiwoom account or app key. A saved HTS condition picks the stocks and WebSocket trades drive the alerts. No orders."
---

# A condition-search alert bot in 10 minutes

This bot picks stocks with a condition you saved in Kiwoom's HTS (영웅문4), watches their real-time trades, and raises an
alert when a price moves by a set percentage. One Python file, about 60 lines.

- **Start without a key.** `KiwoomAPI.demo()` attaches to a fake Kiwoom server inside the process. You get real stock names
  and codes with synthetic prices, and nothing goes over the network. Every response carries a `"_demo"` marker (these are
  not real quotes).
- **No orders.** The bot only uses condition search and real-time quotes.
- To run it on a real account later, you change the one line that creates the client ([On a real account](#on-a-real-account)).

## Setup (1 minute)

```bash
pip install kiwoom-client
```

Python 3.10 or later. Paste the code blocks below, top to bottom, into one file, `alert_bot.py`.

## 1. Settings and the client

```python
import asyncio

from kiwoom_client import KiwoomAPI

CONDITION = "급등주"  # name of a condition saved in HTS (a part of the name is enough)
ALERT_PCT = 0.5       # alert when the price moves this many percent from the condition-search price
SECONDS = 30          # how long to watch (seconds)

api = KiwoomAPI.demo()  # synthetic data: no key, account or network
print("demo mode:", api.is_demo)
```

The demo account has four saved conditions: `급등주` (surging), `거래량 급증` (volume spike), `52주 신고가 근접` (near 52-week
high) and `대형 우량주` (large caps).

## 2. Send one request, wait for the reply

Condition search goes over the same WebSocket as real-time data, not REST. Replies come back separately, tagged with a `trnm`
(`CNSRLST` for the condition list, `CNSRREQ` for search results), so a small helper sends a request and waits for the first
reply with that `trnm`.

```python
async def ask(ws, trnm, message):
    """Send one WebSocket request and wait for the first reply with the same trnm."""
    reply = asyncio.get_running_loop().create_future()
    ws.on_trnm(trnm, lambda frame: reply.done() or reply.set_result(frame))
    await ws.send(message)
    return await asyncio.wait_for(reply, timeout=10)
```

## 3. Pick stocks with the condition

Find the condition's number (`seq`) by name in the list, run it once, and collect the code, name and price of each match.
Result rows are keyed by FID number (`9001` stock code, `302` name, `10` current price).

```python
async def find_stocks(ws, name):
    """Find a condition's seq by name, run it once, and return the matching stocks."""
    listing = await ask(ws, "CNSRLST", api.condition_search.condition_list())
    seq = next(s for s, n in listing["data"] if name in n)
    result = await ask(ws, "CNSRREQ", api.condition_search.condition_search(seq=seq))
    stocks = {}
    for row in result["data"]:
        code = row["9001"].lstrip("A")  # "A005930" -> "005930"
        stocks[code] = {"name": row["302"], "start": abs(int(row["10"]))}  # "000071900" -> 71900
    return stocks
```

## 4. The alert callback

Called for every real-time trade (`0B`). Registered with `named=True`, the `values` keys are Kiwoom's Korean field names
(`"현재가"`, current price) instead of FID numbers. Each stock alerts once.

```python
def make_alert(stocks, pct):
    """Callback for each trade. Alerts once per stock."""
    alerted = set()

    def on_trade(item):
        code = item["item"]
        price = abs(int(item["values"]["현재가"]))  # "+71900": the sign is the direction vs. the previous close
        info = stocks[code]
        move = (price - info["start"]) / info["start"] * 100
        if abs(move) >= pct and code not in alerted:
            alerted.add(code)
            notify(f"{info['name']} ({code}) {price:,} won, {move:+.2f}% since the condition search")

    return on_trade, alerted


def notify(text):
    print("[alert]", text)  # swap in a Slack webhook, mail, a log file...
```

## 5. Put it together

```python
async def main():
    ws = api.create_websocket()
    async with ws:  # from LOGIN to close
        listener = asyncio.create_task(ws.listen())  # receives replies and trades, runs the callbacks
        stocks = await find_stocks(ws, CONDITION)
        for code, info in stocks.items():
            print(f"{info['name']} ({code}) {info['start']:,} won")
        on_trade, alerted = make_alert(stocks, ALERT_PCT)
        ws.on("0B", on_trade, named=True)
        await ws.subscribe("0B", list(stocks))
        await asyncio.sleep(SECONDS)
    await listener
    print(f"{len(alerted)} alerts in {SECONDS} seconds")


asyncio.run(main())
```

```bash
python alert_bot.py
```

Output from a demo run (synthetic prices). Demo prices are generated per date, so the stocks and prices change with the day
you run it.

```text
demo mode: True
LG화학 (051910) 284,500 won
삼성물산 (028260) 132,400 won
SK하이닉스 (000660) 182,000 won
POSCO홀딩스 (005490) 312,000 won
현대차 (005380) 214,500 won
[alert] 현대차 (005380) 216,000 won, +0.70% since the condition search
[alert] POSCO홀딩스 (005490) 310,000 won, -0.64% since the condition search
[alert] LG화학 (051910) 283,000 won, -0.53% since the condition search
[alert] 삼성물산 (028260) 131,700 won, -0.53% since the condition search
[alert] SK하이닉스 (000660) 183,000 won, +0.55% since the condition search
5 alerts in 30 seconds
```

## On a real account

1. Get an app key and secret from the [Kiwoom REST API portal](https://openapi.kiwoom.com) and set `KIWOOM_APP_KEY` and `KIWOOM_APP_SECRET`.
2. Save the condition you want in HTS (영웅문4) and set `CONDITION` to its name.
3. Change the client line from step 1:

<!-- docs-test: no-exec -->
```python
api = KiwoomAPI.from_env(is_mock=True)  # paper-trading key; with a live key use is_mock=False
```

The rest stays the same. Worth knowing:

- The bot calls no order method, so even with a live key it only looks things up. Add `api.order.*` and a live key sends real
  orders (direct Python calls have no guard).
- Real-time trades arrive only during market hours. Outside them you get the stock list and no alerts.
- For long runs, `listen()` handles PING replies, reconnects and restoring subscriptions. To keep receiving condition-search
  changes in real time, see [Condition search results in real time](../cookbook/condition-search-realtime.md).

## Next steps

- To send alerts to a person, swap `notify()` for a Slack webhook or mail. Keep them for yourself: relaying them to others as
  trading signals can fall under investment-advisory rules in Korea.
- To watch the order book instead of trades, subscribe to `0D` ([Real-time trades and order book](../cookbook/realtime-trades.md)).
- To have Claude do the same, use the MCP server's `condition_search_run` and `watch` tools (items 13 and 14 in the
  [prompt library](../prompts.md)).

<small>A test (`tests/test_tutorial_exec.py`) runs these code blocks against the demo backend.</small>
