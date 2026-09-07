"""Tests for ConditionSearchSession's WebSocket request/response correlation."""

from __future__ import annotations

import asyncio
import contextlib
import json

import pytest
import websockets

from kiwoom_client.mcp.condition_search_session import (
    ConditionSearchSession,
    ConditionSearchTimeout,
)
from kiwoom_client.websocket import KiwoomWebSocket


class FakeConditionServer:
    """LOGIN + CNSRLST/CNSRREQ/CNSRCLR 을 흉내내는 로컬 WebSocket 서버."""

    def __init__(self) -> None:
        self.received: list[dict] = []
        self._server: websockets.asyncio.server.Server | None = None
        self._conns: list = []

    async def __aenter__(self) -> FakeConditionServer:
        self._server = await websockets.serve(self._handler, "127.0.0.1", 0)
        return self

    async def __aexit__(self, *args) -> None:
        assert self._server is not None
        self._server.close()
        await self._server.wait_closed()

    @property
    def url(self) -> str:
        assert self._server is not None
        host, port = self._server.sockets[0].getsockname()[:2]
        return f"ws://{host}:{port}"

    async def _handler(self, conn) -> None:
        self._conns.append(conn)
        try:
            async for raw in conn:
                msg = json.loads(raw)
                self.received.append(msg)
                if msg.get("trnm") == "LOGIN":
                    await conn.send(json.dumps(
                        {"trnm": "LOGIN", "return_code": 0, "return_msg": ""}
                    ))
                elif msg.get("trnm") == "CNSRLST":
                    await conn.send(json.dumps({
                        "trnm": "CNSRLST",
                        "data": [["0", "급등주 조건"], ["1", "거래량 급증"]],
                    }))
                elif msg.get("trnm") == "CNSRREQ":
                    # seq "999": 응답은 오지만 다른 seq를 달고 와서 매칭되지 않는
                    # 상황(콜백 응답의 실제 순서 뒤섞임 등)을 흉내낸다.
                    reply_seq = "998" if msg["seq"] == "999" else msg["seq"]
                    await conn.send(json.dumps({
                        "trnm": "CNSRREQ", "seq": reply_seq, "data": [{"jmcode": "005930"}],
                    }))
                # CNSRCLR: 키움 프로토콜상 ack 프레임 없음 — 응답하지 않는다.
        except websockets.ConnectionClosed:
            pass

    async def close_all_connections(self) -> None:
        for conn in list(self._conns):
            with contextlib.suppress(websockets.ConnectionClosed):
                await conn.close()


async def _connect(url: str) -> KiwoomWebSocket:
    ws = KiwoomWebSocket("tok-123", ws_url=url)
    await ws.connect()
    return ws


class TestConditionSearchSession:
    async def test_condition_list_returns_matching_reply(self):
        async with FakeConditionServer() as server:
            session = ConditionSearchSession(connect=lambda: _connect(server.url))
            result = await session.request({"trnm": "CNSRLST"})
            assert result["trnm"] == "CNSRLST"
            assert result["data"][0] == ["0", "급등주 조건"]

    async def test_condition_search_matches_by_seq(self):
        async with FakeConditionServer() as server:
            session = ConditionSearchSession(connect=lambda: _connect(server.url))
            result = await session.request(
                {"trnm": "CNSRREQ", "seq": "3", "search_type": "0", "stex_tp": "K",
                 "cont_yn": "N", "next_key": ""}
            )
            assert result["seq"] == "3"
            assert result["data"] == [{"jmcode": "005930"}]

    async def test_reuses_the_same_connection_across_calls(self):
        async with FakeConditionServer() as server:
            connect_calls = 0

            async def counted_connect() -> KiwoomWebSocket:
                nonlocal connect_calls
                connect_calls += 1
                return await _connect(server.url)

            session = ConditionSearchSession(connect=counted_connect)
            await session.request({"trnm": "CNSRLST"})
            await session.request(
                {"trnm": "CNSRREQ", "seq": "1", "search_type": "0", "stex_tp": "K",
                 "cont_yn": "N", "next_key": ""}
            )
            assert connect_calls == 1

    async def test_expect_reply_false_sends_without_waiting(self):
        async with FakeConditionServer() as server:
            session = ConditionSearchSession(connect=lambda: _connect(server.url))
            result = await session.request({"trnm": "CNSRCLR", "seq": "3"}, expect_reply=False)
            assert result is None

            async def _sent() -> bool:
                return any(m.get("trnm") == "CNSRCLR" for m in server.received)

            for _ in range(50):
                if await _sent():
                    break
                await asyncio.sleep(0.01)
            assert await _sent()

    async def test_times_out_when_no_reply_arrives(self, monkeypatch):
        import kiwoom_client.mcp.condition_search_session as mod

        monkeypatch.setattr(mod, "RESPONSE_TIMEOUT", 0.05)
        async with FakeConditionServer() as server:
            session = ConditionSearchSession(connect=lambda: _connect(server.url))
            with pytest.raises(ConditionSearchTimeout):
                # seq "999" 는 서버가 응답하지 않는 값이 아니라, CNSRREQ 자체는
                # 응답하지만 seq 불일치로 매칭되지 않는 상황을 흉내낸다.
                await session.request(
                    {"trnm": "CNSRREQ", "seq": "999", "search_type": "0", "stex_tp": "K",
                     "cont_yn": "N", "next_key": ""}
                )
