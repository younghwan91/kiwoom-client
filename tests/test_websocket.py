"""Tests for the real-time WebSocket client.

실계좌 대신 로컬 WebSocket 서버로 키움 프로토콜을 흉내내 검증한다.
프로토콜 근거는 키움 공식 가이드와 공개 구현체들이며, 실계좌 검증은 아직이다.
"""

from __future__ import annotations

import asyncio
import contextlib
import json

import pytest
import websockets

from kiwoom_rest_api.websocket import KiwoomWebSocket, KiwoomWebSocketError


class FakeKiwoomServer:
    """키움 WebSocket 서버 흉내: LOGIN 응답, PING 발신, REAL 푸시."""

    def __init__(self, login_return_code: int = 0) -> None:
        self.login_return_code = login_return_code
        self.received: list[dict] = []
        self.tokens: list[str] = []
        self._server: websockets.asyncio.server.Server | None = None
        self._conns: list = []
        self.logins = 0

    async def __aenter__(self) -> FakeKiwoomServer:
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
                    self.logins += 1
                    self.tokens.append(msg.get("token", ""))
                    await conn.send(json.dumps({
                        "trnm": "LOGIN",
                        "return_code": self.login_return_code,
                        "return_msg": "" if self.login_return_code == 0 else "인증 실패",
                    }))
                elif msg.get("trnm") in ("REG", "REMOVE"):
                    await conn.send(json.dumps({
                        "trnm": msg["trnm"], "return_code": 0, "return_msg": ""
                    }))
        except websockets.ConnectionClosed:
            pass

    async def push(self, payload: dict) -> None:
        """접속된 클라이언트 전부에게 메시지를 보낸다."""
        for conn in list(self._conns):
            with contextlib.suppress(websockets.ConnectionClosed):
                await conn.send(json.dumps(payload))

    def sent(self, trnm: str) -> list[dict]:
        return [m for m in self.received if m.get("trnm") == trnm]


async def _until(condition, timeout: float = 2.0) -> None:
    """condition() 이 참이 될 때까지 이벤트 루프를 돌린다.

    asyncio.timeout() 은 3.11+ 이라 wait_for 로 쓴다 (최소 지원 버전 3.10).
    """
    async def _poll() -> None:
        while not condition():
            await asyncio.sleep(0.01)

    await asyncio.wait_for(_poll(), timeout)


async def _drain(coro_task: asyncio.Task, condition, timeout: float = 2.0) -> None:
    """리스너 태스크가 도는 동안 condition() 을 기다린다."""
    await _until(condition, timeout)


class TestLogin:
    async def test_sends_login_handshake_on_connect(self):
        async with FakeKiwoomServer() as server:
            ws = KiwoomWebSocket("tok-123", ws_url=server.url)
            await ws.connect()
            await _until(lambda: server.sent("LOGIN"))
            await ws.disconnect()

        assert server.sent("LOGIN") == [{"trnm": "LOGIN", "token": "tok-123"}]

    async def test_raises_when_login_rejected(self):
        async with FakeKiwoomServer(login_return_code=1) as server:
            ws = KiwoomWebSocket("bad", ws_url=server.url)
            with pytest.raises(KiwoomWebSocketError) as exc:
                await ws.connect()
            assert "인증 실패" in str(exc.value)
            await ws.disconnect()


class TestPing:
    async def test_ping_is_echoed_back_verbatim(self):
        """PING 에 응답하지 않으면 서버가 연결을 끊는다."""
        async with FakeKiwoomServer() as server:
            ws = KiwoomWebSocket("tok", ws_url=server.url)
            await ws.connect()
            listener = asyncio.create_task(ws.listen())

            await server.push({"trnm": "PING", "seq": "42"})
            await _drain(listener, lambda: server.sent("PING"))

            assert server.sent("PING") == [{"trnm": "PING", "seq": "42"}]

            await ws.disconnect()
            listener.cancel()

    async def test_ping_does_not_reach_type_callbacks(self):
        async with FakeKiwoomServer() as server:
            ws = KiwoomWebSocket("tok", ws_url=server.url)
            seen: list[dict] = []
            ws.on("0B", seen.append)
            await ws.connect()
            listener = asyncio.create_task(ws.listen())

            await server.push({"trnm": "PING"})
            await _drain(listener, lambda: server.sent("PING"))

            assert seen == []
            await ws.disconnect()
            listener.cancel()


class TestSubscribe:
    async def test_reg_payload_matches_kiwoom_format(self):
        async with FakeKiwoomServer() as server:
            ws = KiwoomWebSocket("tok", ws_url=server.url)
            await ws.connect()
            await ws.subscribe("0B", ["005930", "000660"])
            await _until(lambda: server.sent("REG"))
            await ws.disconnect()

        assert server.sent("REG") == [{
            "trnm": "REG",
            "grp_no": "1",
            "refresh": "1",
            "data": [{"item": ["005930", "000660"], "type": ["0B"]}],
        }]

    async def test_accepts_scalars_and_lists(self):
        async with FakeKiwoomServer() as server:
            ws = KiwoomWebSocket("tok", ws_url=server.url)
            await ws.connect()
            await ws.subscribe(["0B", "0D"], "005930")
            await _until(lambda: server.sent("REG"))
            await ws.disconnect()

        assert server.sent("REG")[0]["data"] == [
            {"item": ["005930"], "type": ["0B", "0D"]}
        ]

    async def test_unsubscribe_sends_remove(self):
        async with FakeKiwoomServer() as server:
            ws = KiwoomWebSocket("tok", ws_url=server.url)
            await ws.connect()
            await ws.subscribe("0B", "005930")
            await ws.unsubscribe("0B", "005930")
            await _until(lambda: server.sent("REMOVE"))
            await ws.disconnect()

        assert server.sent("REMOVE") == [{
            "trnm": "REMOVE",
            "grp_no": "1",
            "refresh": "1",
            "data": [{"item": ["005930"], "type": ["0B"]}],
        }]

    async def test_subscribe_before_connect_raises(self):
        ws = KiwoomWebSocket("tok", ws_url="ws://127.0.0.1:1")
        with pytest.raises(RuntimeError):
            await ws.subscribe("0B", "005930")


class TestRealDispatch:
    async def test_dispatches_each_item_by_type(self):
        async with FakeKiwoomServer() as server:
            ws = KiwoomWebSocket("tok", ws_url=server.url)
            trades: list[dict] = []
            quotes: list[dict] = []
            ws.on("0B", trades.append)
            ws.on("0D", quotes.append)
            await ws.connect()
            listener = asyncio.create_task(ws.listen())

            await server.push({
                "trnm": "REAL",
                "data": [
                    {"type": "0B", "item": "005930", "values": {"10": "+70000"}},
                    {"type": "0D", "item": "005930", "values": {"41": "70100"}},
                    {"type": "0B", "item": "000660", "values": {"10": "-180000"}},
                ],
            })
            await _drain(listener, lambda: len(trades) == 2 and len(quotes) == 1)

            assert [t["item"] for t in trades] == ["005930", "000660"]
            assert trades[0]["values"]["10"] == "+70000"
            assert quotes[0]["type"] == "0D"

            await ws.disconnect()
            listener.cancel()

    async def test_unregistered_type_is_ignored(self):
        async with FakeKiwoomServer() as server:
            ws = KiwoomWebSocket("tok", ws_url=server.url)
            seen: list[dict] = []
            ws.on("0B", seen.append)
            await ws.connect()
            listener = asyncio.create_task(ws.listen())

            await server.push({"trnm": "REAL", "data": [{"type": "0J", "item": "001"}]})
            await server.push({"trnm": "REAL", "data": [{"type": "0B", "item": "005930"}]})
            await _drain(listener, lambda: len(seen) == 1)

            assert seen[0]["item"] == "005930"
            await ws.disconnect()
            listener.cancel()

    async def test_callback_error_does_not_kill_the_listener(self):
        async with FakeKiwoomServer() as server:
            ws = KiwoomWebSocket("tok", ws_url=server.url)
            seen: list[dict] = []
            ws.on("0B", lambda _: (_ for _ in ()).throw(ValueError("boom")))
            ws.on("0B", seen.append)
            await ws.connect()
            listener = asyncio.create_task(ws.listen())

            await server.push({"trnm": "REAL", "data": [{"type": "0B", "item": "1"}]})
            await server.push({"trnm": "REAL", "data": [{"type": "0B", "item": "2"}]})
            await _drain(listener, lambda: len(seen) == 2)

            assert [s["item"] for s in seen] == ["1", "2"]
            await ws.disconnect()
            listener.cancel()

    async def test_async_callbacks_are_awaited(self):
        async with FakeKiwoomServer() as server:
            ws = KiwoomWebSocket("tok", ws_url=server.url)
            seen: list[dict] = []

            async def handler(data: dict) -> None:
                await asyncio.sleep(0)
                seen.append(data)

            ws.on("0B", handler)
            await ws.connect()
            listener = asyncio.create_task(ws.listen())

            await server.push({"trnm": "REAL", "data": [{"type": "0B", "item": "1"}]})
            await _drain(listener, lambda: len(seen) == 1)

            await ws.disconnect()
            listener.cancel()

    async def test_on_message_sees_every_frame(self):
        async with FakeKiwoomServer() as server:
            ws = KiwoomWebSocket("tok", ws_url=server.url)
            frames: list[dict] = []
            ws.on_message(frames.append)
            await ws.connect()
            listener = asyncio.create_task(ws.listen())

            await server.push({"trnm": "REAL", "data": [{"type": "0B"}]})
            await _drain(listener, lambda: len(frames) >= 1)

            assert frames[0]["trnm"] == "REAL"
            await ws.disconnect()
            listener.cancel()


class TestConditionSearch:
    async def test_condition_list_payload(self):
        async with FakeKiwoomServer() as server:
            ws = KiwoomWebSocket("tok", ws_url=server.url)
            await ws.connect()
            await ws.send({"trnm": "CNSRLST"})
            await _until(lambda: server.sent("CNSRLST"))
            await ws.disconnect()

        assert server.sent("CNSRLST") == [{"trnm": "CNSRLST"}]

    async def test_condition_search_module_builds_ws_payloads(self):
        from kiwoom_rest_api.domestic.condition_search import ConditionSearch

        cs = ConditionSearch(None)
        assert cs.condition_list() == {"trnm": "CNSRLST"}
        assert cs.condition_search(seq="1") == {
            "trnm": "CNSRREQ",
            "seq": "1",
            "search_type": "0",
            "stex_tp": "K",
            "cont_yn": "N",
            "next_key": "",
        }
        assert cs.condition_search_realtime(seq="1")["search_type"] == "1"
        assert cs.condition_search_cancel(seq="1") == {"trnm": "CNSRCLR", "seq": "1"}

    async def test_trnm_callbacks_receive_responses(self):
        async with FakeKiwoomServer() as server:
            ws = KiwoomWebSocket("tok", ws_url=server.url)
            hits: list[dict] = []
            ws.on_trnm("CNSRLST", hits.append)
            await ws.connect()
            listener = asyncio.create_task(ws.listen())

            await server.push({"trnm": "CNSRLST", "data": [["1", "조건식A"]]})
            await _drain(listener, lambda: len(hits) == 1)

            assert hits[0]["data"] == [["1", "조건식A"]]
            await ws.disconnect()
            listener.cancel()


class TestReconnect:
    async def test_reconnect_relogins_and_resubscribes(self):
        """재연결은 LOGIN 부터 다시 하고 기존 구독을 복원해야 한다."""
        async with FakeKiwoomServer() as server:
            ws = KiwoomWebSocket("tok", ws_url=server.url, reconnect_delay=0.01)
            await ws.connect()
            await ws.subscribe("0B", "005930")
            listener = asyncio.create_task(ws.listen())

            # 서버가 연결을 끊는다.
            for conn in list(server._conns):
                await conn.close()

            await _drain(listener, lambda: server.logins == 2 and len(server.sent("REG")) == 2)

            assert server.logins == 2, "재연결 시 LOGIN 재수행"
            assert server.sent("REG")[1] == server.sent("REG")[0], "구독 복원"

            await ws.disconnect()
            listener.cancel()

    async def test_disconnect_stops_the_listener(self):
        async with FakeKiwoomServer() as server:
            ws = KiwoomWebSocket("tok", ws_url=server.url, reconnect_delay=0.01)
            await ws.connect()
            listener = asyncio.create_task(ws.listen())
            await asyncio.sleep(0.05)

            await ws.disconnect()
            # 재연결 루프에 갇히지 않고 빠져나온다
            await asyncio.wait_for(listener, 2.0)


class TestUrls:
    def test_prod_and_mock_urls(self):
        assert KiwoomWebSocket("t").ws_url == KiwoomWebSocket.PROD_WS_URL
        assert KiwoomWebSocket("t", is_mock=True).ws_url == KiwoomWebSocket.MOCK_WS_URL
        assert KiwoomWebSocket("t", ws_url="ws://x").ws_url == "ws://x"
