"""Correlates condition_search WebSocket requests with their replies.

condition_search rides the same WebSocket as real-time data: a request is
sent as one frame (``trnm`` + optionally ``seq``) and the reply arrives later
as a separate frame carrying the same ``trnm``/``seq``. This wraps that in an
async request/response call so each MCP tool call can simply await one.

The same connection also serves short real-time watches (:meth:`realtime`,
used by the ``watch`` intent tool), so the server keeps one WebSocket.
"""

from __future__ import annotations

import asyncio
import contextlib
from collections.abc import AsyncIterator, Awaitable, Callable, Sequence
from typing import Any

from kiwoom_client.websocket import KiwoomWebSocket

#: How long to wait for a matching reply frame before giving up.
RESPONSE_TIMEOUT = 15.0


class ConditionSearchTimeout(Exception):
    """No matching reply arrived within RESPONSE_TIMEOUT."""


class ConditionSearchSession:
    """Lazily-connected KiwoomWebSocket shared by all condition_search tools.

    Args:
        connect: Called once, lazily, to obtain a connected KiwoomWebSocket
            (e.g. ``lambda: api.create_websocket()`` followed by ``connect()``
            — see server.py for the concrete factory).
    """

    def __init__(self, connect: Callable[[], Awaitable[KiwoomWebSocket]]) -> None:
        self._connect = connect
        self._ws: KiwoomWebSocket | None = None
        self._listen_task: asyncio.Task[None] | None = None
        self._pending: dict[tuple[str, str | None], asyncio.Future[dict[str, Any]]] = {}
        self._dispatched_trnms: set[str] = set()
        self._realtime_types: set[str] = set()
        self._watchers: set[asyncio.Queue[dict[str, Any]]] = set()
        self._realtime_lock = asyncio.Lock()

    async def _ensure_connected(self) -> KiwoomWebSocket:
        if self._ws is None:
            self._ws = await self._connect()
            self._listen_task = asyncio.create_task(self._ws.listen())
        return self._ws

    def _ensure_dispatcher(self, ws: KiwoomWebSocket, trnm: str) -> None:
        """Register one on_trnm callback per trnm that resolves pending futures.

        Registered once and reused across calls — KiwoomWebSocket has no
        ``off()``, so a callback-per-call would leak.
        """
        if trnm in self._dispatched_trnms:
            return
        self._dispatched_trnms.add(trnm)

        def _dispatch(data: dict[str, Any]) -> None:
            seq = data.get("seq")
            for key in ((trnm, seq), (trnm, None)):
                future = self._pending.pop(key, None)
                if future is not None and not future.done():
                    future.set_result(data)
                    return

        ws.on_trnm(trnm, _dispatch)

    async def request(
        self, payload: dict[str, Any], *, expect_reply: bool = True
    ) -> dict[str, Any] | None:
        """Send a condition_search payload and await its matching reply.

        Args:
            payload: One of the dicts built by ``api.condition_search.*``.
            expect_reply: False for CNSRCLR, which the protocol never acks.
        """
        ws = await self._ensure_connected()
        trnm = payload["trnm"]

        if not expect_reply:
            await ws.send(payload)
            return None

        self._ensure_dispatcher(ws, trnm)
        seq = payload.get("seq")
        key = (trnm, seq)
        loop = asyncio.get_running_loop()
        future: asyncio.Future[dict[str, Any]] = loop.create_future()
        self._pending[key] = future

        await ws.send(payload)
        try:
            return await asyncio.wait_for(future, RESPONSE_TIMEOUT)
        except asyncio.TimeoutError as exc:
            self._pending.pop(key, None)
            raise ConditionSearchTimeout(
                f"{trnm} 응답을 {RESPONSE_TIMEOUT}초 안에 받지 못했습니다"
            ) from exc

    def _ensure_realtime_dispatcher(self, ws: KiwoomWebSocket, data_type: str) -> None:
        """One ``on(type)`` callback per real-time type, fanning items out to
        the active watchers' queues (KiwoomWebSocket has no ``off()``)."""
        if data_type in self._realtime_types:
            return
        self._realtime_types.add(data_type)

        def _dispatch(item: dict[str, Any]) -> None:
            for queue in list(self._watchers):
                queue.put_nowait(item)

        ws.on(data_type, _dispatch)

    @contextlib.asynccontextmanager
    async def realtime(
        self, types: Sequence[str], items: Sequence[str], *, grp_no: str = "9"
    ) -> AsyncIterator[asyncio.Queue[dict[str, Any]]]:
        """Register real-time ``types`` for ``items`` while the block runs.

        Yields a queue that receives every REAL item of those types (each a
        dict with ``type``, ``item``, ``values``). On exit the registration
        is removed. One watch at a time: a second caller waits, so one
        caller's REMOVE can't drop the other's items.
        """
        async with self._realtime_lock:
            ws = await self._ensure_connected()
            for data_type in types:
                self._ensure_realtime_dispatcher(ws, data_type)
            queue: asyncio.Queue[dict[str, Any]] = asyncio.Queue()
            self._watchers.add(queue)
            try:
                await ws.subscribe(list(types), list(items), grp_no=grp_no, refresh="1")
                yield queue
            finally:
                self._watchers.discard(queue)
                with contextlib.suppress(Exception):
                    await ws.unsubscribe(list(types), list(items), grp_no=grp_no, refresh="1")

    async def close(self) -> None:
        if self._listen_task is not None:
            self._listen_task.cancel()
        if self._ws is not None:
            await self._ws.disconnect()
