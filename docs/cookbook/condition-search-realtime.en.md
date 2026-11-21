# Condition search results in real time

Search stocks with a **condition** (조건식) you built and saved in the HTS (Kiwoom's 영웅문), then receive stocks
entering and leaving the result in real time. Condition search (조건검색) is sent not over REST but over the same
WebSocket as real-time quotes — `api.condition_search` only builds the messages (dicts) to send.

| Step | Method | `trnm` | Official docs |
|---|---|---|---|
| List conditions | `api.condition_search.condition_list()` | `CNSRLST` | `ka10171` |
| Search once | `api.condition_search.condition_search(seq)` | `CNSRREQ` | `ka10172` |
| Search + real time | `api.condition_search.condition_search_realtime(seq)` | `CNSRREQ` | `ka10173` |
| Stop real time | `api.condition_search.condition_search_cancel(seq)` | `CNSRCLR` | `ka10174` |

Response shapes (official spec):

- `CNSRLST` → `data`: `[{"seq": ..., "name": ...}, ...]`
- `CNSRREQ` (real time) → once at first, `data`: `[{"jmcode": "A005930"}, ...]` — the stock code has a one-letter
  prefix (A stock · J ELW · Q ETN)
- After that, stocks entering and leaving arrive as `REAL` frames, whose items carry in `values`: `841` sequence
  number · `9001` stock code · `843` insert/delete flag (`I` entered / `D` left) · `20` trade time.

```python
import asyncio

from kiwoom_client import KiwoomAPI

CONDITION_NAME = "my condition"  # the name of a condition saved in the HTS

members: set[str] = set()


async def main():
    api = KiwoomAPI.from_env(is_mock=True)
    ws = api.create_websocket()
    await ws.connect()

    found = asyncio.get_running_loop().create_future()

    def on_list(frame: dict) -> None:
        names = {c["name"]: c["seq"] for c in frame.get("data") or []}
        print("conditions:", list(names))
        if not found.done():
            found.set_result(names.get(CONDITION_NAME))

    def on_result(frame: dict) -> None:
        for row in frame.get("data") or []:
            members.add(row["jmcode"])
        print("first result:", len(members), "stocks")

    def on_frame(frame: dict) -> None:
        if frame.get("trnm") != "REAL":
            return
        for item in frame.get("data") or []:
            v = item.get("values") or {}
            if "843" not in v:  # only condition-search enter/leave items
                continue
            code = v.get("9001", "")
            if v["843"] == "I":
                members.add(code)
                print("entered", code)
            elif v["843"] == "D":
                members.discard(code)
                print("left", code)

    ws.on_trnm("CNSRLST", on_list)
    ws.on_trnm("CNSRREQ", on_result)
    ws.on_message(on_frame)

    listener = asyncio.create_task(ws.listen())
    await ws.send(api.condition_search.condition_list())
    seq = await asyncio.wait_for(found, timeout=10)
    if seq is None:
        raise SystemExit(f"no condition named {CONDITION_NAME!r}")

    await ws.send(api.condition_search.condition_search_realtime(seq=seq))
    try:
        await asyncio.sleep(300)  # receive entries and exits for five minutes
    finally:
        await ws.send(api.condition_search.condition_search_cancel(seq=seq))
        await ws.disconnect()
        await listener


asyncio.run(main())
```

- Stop a real-time condition search you no longer need with `condition_search_cancel()`.
- To also get quotes for the stocks that entered, register them on the same socket with `ws.subscribe("0B", ...)`.
  For prefixed codes like `jmcode` (`A005930`), drop the first character before passing them —
  [real-time trades](realtime-trades.md).
- The MCP server exposes the same four as tools (`condition_search_*`).
