"""watch: real-time 0B trades on the shared session, summarised per stock.

A local WebSocket server plays Kiwoom: LOGIN, REG/REMOVE acks, REAL pushes.
"""

from __future__ import annotations

import asyncio
import contextlib
import json

import pytest
import websockets

from kiwoom_client.mcp.condition_search_session import ConditionSearchSession
from kiwoom_client.mcp.intents.watch import TickStats
from kiwoom_client.mcp.server import build_server
from kiwoom_client.websocket import KiwoomWebSocket

from .intent_support import call


class FakeRealtimeServer:
    """LOGIN, REG/REMOVE acks, then ``frames`` pushed after each REG."""

    def __init__(self, frames: list[dict], delay: float = 0.01) -> None:
        self.frames = frames
        self.delay = delay
        self.received: list[dict] = []
        self._server = None

    async def __aenter__(self) -> FakeRealtimeServer:
        self._server = await websockets.serve(self._handler, "127.0.0.1", 0)
        return self

    async def __aexit__(self, *args) -> None:
        self._server.close()
        await self._server.wait_closed()

    @property
    def url(self) -> str:
        host, port = self._server.sockets[0].getsockname()[:2]
        return f"ws://{host}:{port}"

    async def _handler(self, conn) -> None:
        with contextlib.suppress(websockets.ConnectionClosed):
            async for raw in conn:
                msg = json.loads(raw)
                self.received.append(msg)
                if msg.get("trnm") == "LOGIN":
                    await conn.send(json.dumps({"trnm": "LOGIN", "return_code": 0}))
                elif msg.get("trnm") in ("REG", "REMOVE"):
                    await conn.send(json.dumps({"trnm": msg["trnm"], "return_code": 0}))
                    if msg["trnm"] == "REG":
                        for frame in self.frames:
                            await asyncio.sleep(self.delay)
                            await conn.send(json.dumps(frame))

    def sent(self, trnm: str) -> list[dict]:
        return [m for m in self.received if m.get("trnm") == trnm]


def _trade(code: str, price: str, qty: str, time: str, rate: str = "+1.00") -> dict:
    return {
        "trnm": "REAL",
        "data": [{
            "type": "0B", "name": "주식체결", "item": code,
            "values": {"10": price, "15": qty, "13": "1000000", "12": rate, "20": time},
        }],
    }  # fmt: skip


@contextlib.asynccontextmanager
async def _app(server: FakeRealtimeServer):
    async def connect() -> KiwoomWebSocket:
        ws = KiwoomWebSocket("tok", ws_url=server.url)
        await ws.connect()
        return ws

    session = ConditionSearchSession(connect=connect)
    app, _specs = build_server(api=None, allow_live_orders=False, session=session)
    try:
        yield app
    finally:
        await session.close()


def test_tick_stats():
    stats = TickStats("005930", None)
    stats.add({"10": "+70000", "15": "+10", "20": "090001"})
    stats.add({"10": "-69900", "15": "-4"})
    stats.add({"10": "+70100", "15": "3"})
    out = stats.as_dict()
    assert (out["first_price"], out["last_price"], out["high"], out["low"]) == (
        70000, 70100, 70100, 69900,
    )  # fmt: skip
    assert (out["volume"], out["buy_volume"], out["sell_volume"]) == (17, 13, 4)
    assert out["ticks"] == 3 and out["last_time"] == "09:00:01"
    assert TickStats("x", None).as_dict()["ticks"] == 0


async def test_collects_until_the_window_ends_and_unregisters():
    frames = [
        _trade("005930", "+70000", "+10", "090001"),
        _trade("000660", "-180000", "-5", "090001"),
        _trade("005930", "+70100", "-2", "090002"),
        _trade("999999", "+1", "+1", "090002"),  # 등록하지 않은 종목은 무시
    ]
    async with FakeRealtimeServer(frames) as server, _app(server) as app:
        is_error, out = await call(app, "watch", {"stocks": ["005930", "000660"], "seconds": 1})
    assert is_error is False, out
    samsung, hynix = out["stocks"]
    assert samsung["ticks"] == 2 and samsung["last_price"] == 70100
    assert samsung["buy_volume"] == 10 and samsung["sell_volume"] == 2
    assert hynix["last_price"] == 180000
    assert out["triggered"] is None
    assert 0.9 <= out["elapsed_seconds"] <= 3
    (reg,) = server.sent("REG")
    assert reg["data"] == [{"item": ["005930", "000660"], "type": ["0B"]}]
    assert reg["grp_no"] == "9"
    assert server.sent("REMOVE"), "감시가 끝나면 등록을 지운다"


async def test_until_returns_as_soon_as_the_price_crosses():
    frames = [
        _trade("005930", "+71900", "+1", "090001"),
        _trade("005930", "+72000", "+1", "090002"),
        _trade("005930", "+72100", "+1", "090003"),
    ]
    async with FakeRealtimeServer(frames) as server, _app(server) as app:
        args = {"stocks": ["005930"], "seconds": 30, "until": {"above": 72000}}
        is_error, out = await call(app, "watch", args)
    assert is_error is False, out
    assert out["triggered"] == {
        "stock": "005930", "condition": "above 72000", "price": 72000, "time": "09:00:02",
    }  # fmt: skip
    assert out["elapsed_seconds"] < 5
    assert out["stocks"][0]["ticks"] == 2


async def test_no_trades_says_so():
    async with FakeRealtimeServer([]) as server, _app(server) as app:
        is_error, out = await call(app, "watch", {"stocks": "005930", "seconds": 1})
    assert is_error is False, out
    assert out["stocks"][0]["ticks"] == 0 and "체결이 없었습니다" in out["stocks"][0]["note"]


@pytest.mark.parametrize(
    "args",
    [
        {"stocks": []},
        {"stocks": [f"{i:06d}" for i in range(11)]},
        {"stocks": ["005930", "000660"], "until": {"above": 1}},
        {"stocks": ["005930"], "until": {"above": 1, "below": 2}},
        {"stocks": ["005930"], "until": {"stock": "000660", "above": 1}},
        {"stocks": ["005930"], "seconds": "soon"},
    ],
)
async def test_bad_arguments(args):
    async with FakeRealtimeServer([]) as server, _app(server) as app:
        is_error, _text = await call(app, "watch", args)
    assert is_error is True


async def test_without_a_session_it_refuses():
    app, _specs = build_server(api=None, allow_live_orders=False)
    is_error, text = await call(app, "watch", {"stocks": ["005930"]})
    assert is_error is True and "WebSocket" in text
