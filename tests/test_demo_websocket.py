"""Demo WebSocket: LOGIN, real-time 0B pushes and condition search without a socket."""

from __future__ import annotations

import asyncio

import pytest

from kiwoom_client.demo import DEMO_KEY, DemoBackend
from kiwoom_client.demo.websocket import CONDITIONS, DemoWebSocket
from kiwoom_client.domestic.condition_search import ConditionSearch
from tests.demo_support import no_network  # noqa: F401

pytestmark = pytest.mark.usefixtures("no_network")


async def test_login_subscribe_and_receive_trades():
    backend = DemoBackend()
    ws = DemoWebSocket(backend)
    items: list[dict] = []
    named: list[dict] = []
    ws.on("0B", items.append)
    ws.on("0B", named.append, named=True)
    async with ws:
        listener = asyncio.create_task(ws.listen())
        await ws.subscribe("0B", ["005930", "000660"])
        await asyncio.sleep(0.5)
        await ws.unsubscribe("0B", ["005930", "000660"])
        await asyncio.sleep(0.3)
        seen = len(items)
        await asyncio.sleep(0.3)
        assert len(items) == seen  # nothing after REMOVE
    await asyncio.wait_for(listener, 1)
    assert {i["item"] for i in items} == {"005930", "000660"}
    close = backend.market.price("005930")
    for item in items:
        if item["item"] == "005930":
            price = abs(int(item["values"]["10"]))
            assert close * 0.98 <= price <= close * 1.02
    assert "현재가" in named[0]["values"]


async def test_condition_list_and_search():
    ws = DemoWebSocket(DemoBackend())
    frames: dict[str, dict] = {}
    for trnm in ("CNSRLST", "CNSRREQ"):
        ws.on_trnm(trnm, lambda f, t=trnm: frames.__setitem__(t, f))
    cs = ConditionSearch()
    async with ws:
        listener = asyncio.create_task(ws.listen())
        await ws.send(cs.condition_list())
        await ws.send(cs.condition_search(seq="0"))
        await asyncio.sleep(0.1)
    await asyncio.wait_for(listener, 1)
    assert frames["CNSRLST"]["data"] == [list(c) for c in CONDITIONS]
    rows = frames["CNSRREQ"]["data"]
    assert rows and rows[0]["9001"].startswith("A") and rows[0]["302"]
    assert frames["CNSRREQ"][DEMO_KEY]


async def test_mcp_session_runs_on_the_demo_socket():
    from kiwoom_client.mcp.condition_search_session import ConditionSearchSession

    async def connect():
        ws = DemoWebSocket(DemoBackend())
        await ws.connect()
        return ws

    session = ConditionSearchSession(connect=connect)
    try:
        reply = await session.request(ConditionSearch().condition_search(seq="3"))
        assert reply["trnm"] == "CNSRREQ" and len(reply["data"]) == 6
        async with session.realtime(["0B"], ["005930"]) as queue:
            item = await asyncio.wait_for(queue.get(), 2)
        assert item["item"] == "005930"
    finally:
        await session.close()
