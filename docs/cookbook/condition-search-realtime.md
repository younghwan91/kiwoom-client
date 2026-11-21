# 조건검색 결과를 실시간으로

HTS(영웅문)에서 만들어 저장한 **조건식**으로 종목을 검색하고, 이후 편입·이탈을 실시간으로 받습니다.
조건검색은 REST 가 아니라 실시간 시세와 같은 WebSocket 으로 보냅니다 — `api.condition_search` 는 보낼 메시지(dict)만 만듭니다.

| 단계 | 메서드 | `trnm` | 공식 문서 |
|---|---|---|---|
| 조건식 목록 | `api.condition_search.condition_list()` | `CNSRLST` | `ka10171` |
| 한 번 검색 | `api.condition_search.condition_search(seq)` | `CNSRREQ` | `ka10172` |
| 검색 + 실시간 | `api.condition_search.condition_search_realtime(seq)` | `CNSRREQ` | `ka10173` |
| 실시간 해제 | `api.condition_search.condition_search_cancel(seq)` | `CNSRCLR` | `ka10174` |

응답 모양(공식 스펙):

- `CNSRLST` → `data`: `[{"seq": ..., "name": ...}, ...]`
- `CNSRREQ`(실시간) → 처음 한 번 `data`: `[{"jmcode": "A005930"}, ...]` — 종목코드 앞에 접두어 1자리(A 주식 · J ELW · Q ETN)
- 이후 편입·이탈은 `REAL` 프레임으로 오고, 항목의 `values` 에 `841` 일련번호 · `9001` 종목코드 · `843` 삽입삭제 구분(`I` 편입 / `D` 이탈) · `20` 체결시간 이 들어 있습니다.

```python
import asyncio

from kiwoom_client import KiwoomAPI

CONDITION_NAME = "내 조건식"  # HTS 에 저장한 조건식 이름

members: set[str] = set()


async def main():
    api = KiwoomAPI.from_env(is_mock=True)
    ws = api.create_websocket()
    await ws.connect()

    found = asyncio.get_running_loop().create_future()

    def on_list(frame: dict) -> None:
        names = {c["name"]: c["seq"] for c in frame.get("data") or []}
        print("조건식:", list(names))
        if not found.done():
            found.set_result(names.get(CONDITION_NAME))

    def on_result(frame: dict) -> None:
        for row in frame.get("data") or []:
            members.add(row["jmcode"])
        print("처음 결과", len(members), "종목")

    def on_frame(frame: dict) -> None:
        if frame.get("trnm") != "REAL":
            return
        for item in frame.get("data") or []:
            v = item.get("values") or {}
            if "843" not in v:  # 조건검색 편입·이탈 항목만
                continue
            code = v.get("9001", "")
            if v["843"] == "I":
                members.add(code)
                print("편입", code)
            elif v["843"] == "D":
                members.discard(code)
                print("이탈", code)

    ws.on_trnm("CNSRLST", on_list)
    ws.on_trnm("CNSRREQ", on_result)
    ws.on_message(on_frame)

    listener = asyncio.create_task(ws.listen())
    await ws.send(api.condition_search.condition_list())
    seq = await asyncio.wait_for(found, timeout=10)
    if seq is None:
        raise SystemExit(f"조건식 {CONDITION_NAME!r} 이 없습니다")

    await ws.send(api.condition_search.condition_search_realtime(seq=seq))
    try:
        await asyncio.sleep(300)  # 5분 동안 편입·이탈을 받는다
    finally:
        await ws.send(api.condition_search.condition_search_cancel(seq=seq))
        await ws.disconnect()
        await listener


asyncio.run(main())
```

- 다 쓴 실시간 조건검색은 `condition_search_cancel()` 로 해제하세요.
- 편입 종목의 시세까지 받으려면 같은 소켓에서 `ws.subscribe("0B", ...)` 로 등록합니다. `jmcode`(`A005930`)처럼 접두어가 붙은 코드는 앞 1자리를 떼고 넘기세요 —
  [실시간 체결](realtime-trades.md).
- MCP 서버에서도 같은 4종이 도구(`condition_search_*`)로 노출됩니다.
