"""KiwoomWebSocket 의 경계 동작 — 재연결 실패·재시도, 재연결 중 종료, 깨진 프레임, 콜백 예외.

동작은 바꾸지 않고, 커버리지 리포트에서 비어 있던 분기를 로컬 가짜 서버로 고정한다.
키움 서버에는 아무것도 보내지 않는다.
"""

from __future__ import annotations

import asyncio
import json
from typing import Any

import pytest
import websockets

from kiwoom_client.websocket import KiwoomWebSocket, KiwoomWebSocketError
from tests.test_websocket import FakeKiwoomServer, _until


class FlakyLoginServer(FakeKiwoomServer):
    """N 번째 LOGIN 들만 거절한다 — 재연결 중 로그인 실패를 흉내낸다."""

    def __init__(self, reject_logins: set[int]) -> None:
        super().__init__()
        self.reject_logins = reject_logins

    async def _handler(self, conn: Any) -> None:
        self._conns.append(conn)
        try:
            async for raw in conn:
                msg = json.loads(raw)
                self.received.append(msg)
                if msg.get("trnm") == "LOGIN":
                    self.logins += 1
                    rejected = self.logins in self.reject_logins
                    await conn.send(json.dumps({
                        "trnm": "LOGIN",
                        "return_code": 1 if rejected else 0,
                        "return_msg": "인증 실패" if rejected else "",
                    }))
                elif msg.get("trnm") in ("REG", "REMOVE"):
                    await conn.send(json.dumps({
                        "trnm": msg["trnm"], "return_code": 0, "return_msg": ""
                    }))
        except websockets.ConnectionClosed:
            pass


async def _serve_once(handler: Any) -> tuple[Any, str]:
    server = await websockets.serve(handler, "127.0.0.1", 0)
    host, port = server.sockets[0].getsockname()[:2]
    return server, f"ws://{host}:{port}"


class TestHandshake:
    async def test_other_frame_instead_of_login_reply_raises(self):
        async def wrong_reply(conn: Any) -> None:
            await conn.recv()
            await conn.send(json.dumps({"trnm": "PING"}))
            await asyncio.sleep(0.2)

        server, url = await _serve_once(wrong_reply)
        try:
            ws = KiwoomWebSocket("tok", ws_url=url)
            with pytest.raises(KiwoomWebSocketError, match="PING"):
                await ws.connect()
            await ws.disconnect()
        finally:
            server.close()
            await server.wait_closed()


class TestLifecycle:
    async def test_async_context_manager_connects_and_disconnects(self):
        async with FakeKiwoomServer() as server:
            async with KiwoomWebSocket("tok", ws_url=server.url) as ws:
                assert server.logins == 1
                assert ws._ws is not None
            assert ws._ws is None

    async def test_disconnect_twice_is_safe(self):
        async with FakeKiwoomServer() as server:
            ws = KiwoomWebSocket("tok", ws_url=server.url)
            await ws.connect()
            await ws.disconnect()
            await ws.disconnect()
            assert ws._ws is None

    async def test_listen_before_connect_raises(self):
        with pytest.raises(RuntimeError, match="connect"):
            await KiwoomWebSocket("tok").listen()


class TestListenRobustness:
    async def test_undecodable_frame_is_skipped(self):
        async with FakeKiwoomServer() as server:
            ws = KiwoomWebSocket("tok", ws_url=server.url)
            await ws.connect()
            got: list[dict[str, Any]] = []
            ws.on("0B", got.append)
            listener = asyncio.create_task(ws.listen())

            for conn in list(server._conns):
                await conn.send("not json")
            await server.push({
                "trnm": "REAL",
                "data": [{"type": "0B", "item": "005930", "values": {"10": "+70000"}}],
            })
            await _until(lambda: got)

            assert got[0]["item"] == "005930"
            await ws.disconnect()
            listener.cancel()

    async def test_real_frame_ignores_non_dict_items_and_missing_data(self):
        async with FakeKiwoomServer() as server:
            ws = KiwoomWebSocket("tok", ws_url=server.url)
            await ws.connect()
            got: list[dict[str, Any]] = []
            seen: list[dict[str, Any]] = []
            ws.on("0B", got.append)
            ws.on_message(seen.append)
            listener = asyncio.create_task(ws.listen())

            await server.push({"trnm": "REAL", "data": None})
            await server.push({"trnm": "REAL", "data": ["junk", 3, {"type": "0B", "item": "A"}]})
            await server.push({"no_trnm": True})
            await _until(lambda: len(seen) == 3)

            assert [g["item"] for g in got] == ["A"]
            assert seen[2] == {"no_trnm": True}
            await ws.disconnect()
            listener.cancel()


class TestReconnectEdges:
    async def test_failed_relogin_is_retried_then_subscriptions_restored(self):
        # 1 = 최초 접속, 2 = 첫 재연결(거절), 3 = 재시도(성공)
        async with FlakyLoginServer(reject_logins={2}) as server:
            ws = KiwoomWebSocket("tok", ws_url=server.url, reconnect_delay=0.01)
            await ws.connect()
            await ws.subscribe("0B", "005930")
            listener = asyncio.create_task(ws.listen())

            for conn in list(server._conns):
                await conn.close()
            await _until(lambda: server.logins == 3 and len(server.sent("REG")) == 2)

            assert server.sent("REG")[1] == server.sent("REG")[0]
            await ws.disconnect()
            listener.cancel()

    async def test_disconnect_while_waiting_to_reconnect_ends_listen(self):
        async with FakeKiwoomServer() as server:
            ws = KiwoomWebSocket("tok", ws_url=server.url, reconnect_delay=0.3)
            await ws.connect()
            listener = asyncio.create_task(ws.listen())
            await asyncio.sleep(0.05)

            for conn in list(server._conns):
                await conn.close()
            await asyncio.sleep(0.1)  # _reconnect 가 sleep 중
            await ws.disconnect()

            await asyncio.wait_for(listener, 2.0)
            assert server.logins == 1, "종료 뒤에는 다시 로그인하지 않는다"


class TestDispatchEdges:
    async def test_ping_without_connection_is_swallowed(self):
        ws = KiwoomWebSocket("tok")
        await ws._dispatch({"trnm": "PING"})  # RuntimeError 를 삼키고 경고만

    async def test_cancelled_error_from_callback_propagates(self):
        def cancel(_: dict[str, Any]) -> None:
            raise asyncio.CancelledError

        calls: list[str] = []
        with pytest.raises(asyncio.CancelledError):
            await KiwoomWebSocket._invoke([cancel, lambda d: calls.append("x")], {"type": "0B"})
        assert calls == [], "취소는 다음 콜백으로 넘어가지 않고 그대로 올라간다"

    async def test_other_callback_errors_do_not_stop_the_rest(self):
        def boom(_: dict[str, Any]) -> None:
            raise ValueError("boom")

        calls: list[str] = []
        await KiwoomWebSocket._invoke([boom, lambda d: calls.append("ok")], {"trnm": "CNSRLST"})
        assert calls == ["ok"]
