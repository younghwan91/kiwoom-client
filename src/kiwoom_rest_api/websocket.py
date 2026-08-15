"""WebSocket client for Kiwoom REST API real-time data.

The protocol is message-typed by a ``trnm`` field:

- ``LOGIN``  — sent right after connecting, carrying the access token. The
  server answers with the same ``trnm`` and a ``return_code``.
- ``PING``   — sent by the server; echo the frame back verbatim or the
  server drops the connection.
- ``REG`` / ``REMOVE`` — register or unregister real-time items.
- ``REAL``   — the real-time push itself, carrying a ``data`` list whose
  entries each name their own ``type`` (``"0B"``, ``"0D"``, …).
- ``CNSRLST`` / ``CNSRREQ`` / ``CNSRCLR`` — condition search.

Note: this follows Kiwoom's published protocol but has not been verified
against a live account yet.
"""

from __future__ import annotations

import asyncio
import inspect
import json
import logging
from collections.abc import Awaitable, Callable
from typing import Any

import websockets
from websockets.asyncio.client import ClientConnection

logger = logging.getLogger(__name__)

#: Callback for a real-time item or a raw frame. May be sync or async.
Callback = Callable[[dict[str, Any]], Any | Awaitable[Any]]

# Real-time data type codes
REALTIME_TYPES = {
    "00": "주문체결",
    "04": "잔고",
    "0A": "주식기세",
    "0B": "주식체결",
    "0C": "주식우선호가",
    "0D": "주식호가잔량",
    "0E": "주식시간외호가",
    "0F": "주식당일거래원",
    "0G": "ETF NAV",
    "0H": "주식예상체결",
    "0I": "국제금환산가격",
    "0J": "업종지수",
    "0U": "업종등락",
    "0g": "주식종목정보",
    "0m": "ELW 이론가",
    "0s": "장시작시간",
    "0u": "ELW 지표",
    "0w": "종목프로그램매매",
    "1h": "VI발동/해제",
}


class KiwoomWebSocketError(Exception):
    """WebSocket login or protocol failure."""


class KiwoomWebSocket:
    """WebSocket client for real-time market data from Kiwoom.

    Args:
        access_token: Bearer access token.
        is_mock: Use mock trading WebSocket server if True.
        ws_url: Override the WebSocket URL (mainly for tests).
        reconnect_delay: Seconds to wait before retrying a lost connection.
    """

    PROD_WS_URL = "wss://api.kiwoom.com:10000/api/dostk/websocket"
    MOCK_WS_URL = "wss://mockapi.kiwoom.com:10000/api/dostk/websocket"

    def __init__(
        self,
        access_token: str,
        is_mock: bool = False,
        ws_url: str | None = None,
        reconnect_delay: float = 1.0,
    ):
        self.access_token = access_token
        if ws_url:
            self.ws_url = ws_url
        else:
            self.ws_url = self.MOCK_WS_URL if is_mock else self.PROD_WS_URL
        self.reconnect_delay = reconnect_delay
        self._ws: ClientConnection | None = None
        self._callbacks: dict[str, list[Callback]] = {}
        self._trnm_callbacks: dict[str, list[Callback]] = {}
        self._message_callbacks: list[Callback] = []
        # Registered items, kept so a reconnect can restore them.
        self._subscriptions: list[dict[str, Any]] = []
        self._running = False

    async def connect(self) -> None:
        """Open the connection and complete the LOGIN handshake.

        Raises:
            KiwoomWebSocketError: If the server rejects the token.
        """
        self._ws = await websockets.connect(self.ws_url)
        logger.info("WebSocket connected to %s", self.ws_url)
        await self._login()

    async def _login(self) -> None:
        assert self._ws is not None
        await self._ws.send(json.dumps({"trnm": "LOGIN", "token": self.access_token}))

        # The login reply is the first frame back; anything else means the
        # handshake changed, so surface it instead of guessing.
        data = json.loads(await self._ws.recv())
        if data.get("trnm") != "LOGIN":
            raise KiwoomWebSocketError(f"LOGIN 응답 대신 {data.get('trnm')!r} 수신: {data}")
        if data.get("return_code", 0) != 0:
            msg = data.get("return_msg", "알 수 없는 오류")
            raise KiwoomWebSocketError(f"WebSocket 로그인 실패: {msg}")
        logger.info("WebSocket login succeeded")

    async def disconnect(self) -> None:
        """Close the connection and stop the listener."""
        self._running = False
        if self._ws:
            await self._ws.close()
            self._ws = None
            logger.info("WebSocket disconnected")

    async def __aenter__(self) -> KiwoomWebSocket:
        await self.connect()
        return self

    async def __aexit__(self, *args: Any) -> None:
        await self.disconnect()

    # --- callbacks ---

    def on(self, data_type: str, callback: Callback) -> None:
        """Register a callback for a real-time data type.

        The callback receives one entry of the REAL frame's ``data`` list —
        a dict carrying ``type``, ``item`` and ``values``.

        Args:
            data_type: Real-time data type code (e.g., "0B" for 주식체결).
            callback: Sync or async function called for each matching item.
        """
        self._callbacks.setdefault(data_type, []).append(callback)

    def on_trnm(self, trnm: str, callback: Callback) -> None:
        """Register a callback for a non-REAL message type (e.g. "CNSRLST")."""
        self._trnm_callbacks.setdefault(trnm, []).append(callback)

    def on_message(self, callback: Callback) -> None:
        """Register a callback that receives every decoded frame."""
        self._message_callbacks.append(callback)

    # --- subscriptions ---

    async def subscribe(
        self,
        types: list[str] | str,
        items: list[str] | str,
        grp_no: str = "1",
        refresh: str = "1",
    ) -> None:
        """Register real-time data for the given types and items.

        Args:
            types: Real-time type code(s), e.g. "0B" or ["0B", "0D"].
            items: Stock code(s), e.g. "005930" or ["005930", "000660"].
            grp_no: Group number. Kiwoom keys registrations by group.
            refresh: "1" keeps existing registrations, "0" replaces them.
        """
        payload = self._registration("REG", types, items, grp_no, refresh)
        await self.send(payload)
        self._subscriptions.append(payload)
        logger.info("Subscribed: %s", payload["data"])

    async def unsubscribe(
        self,
        types: list[str] | str,
        items: list[str] | str,
        grp_no: str = "1",
        refresh: str = "1",
    ) -> None:
        """Unregister real-time data for the given types and items."""
        await self.send(self._registration("REMOVE", types, items, grp_no, refresh))
        registered = self._registration("REG", types, items, grp_no, refresh)
        self._subscriptions = [s for s in self._subscriptions if s != registered]
        logger.info("Unsubscribed: %s", registered["data"])

    @staticmethod
    def _registration(
        trnm: str,
        types: list[str] | str,
        items: list[str] | str,
        grp_no: str,
        refresh: str,
    ) -> dict[str, Any]:
        return {
            "trnm": trnm,
            "grp_no": grp_no,
            "refresh": refresh,
            "data": [{
                "item": [items] if isinstance(items, str) else list(items),
                "type": [types] if isinstance(types, str) else list(types),
            }],
        }

    async def send(self, payload: dict[str, Any]) -> None:
        """Send a raw protocol message.

        Use it with the payloads built by ``api.condition_search``.

        Raises:
            RuntimeError: If not connected.
        """
        if not self._ws:
            raise RuntimeError("WebSocket not connected. Call connect() first.")
        await self._ws.send(json.dumps(payload))

    # --- listening ---

    async def listen(self) -> None:
        """Receive frames and dispatch them until ``disconnect()`` is called.

        Answers PING frames, restores subscriptions after a reconnect, and
        keeps running when a callback raises.
        """
        if not self._ws:
            raise RuntimeError("WebSocket not connected. Call connect() first.")

        self._running = True
        while self._running:
            try:
                raw = await self._ws.recv()
            except websockets.ConnectionClosed:
                if not self._running or not await self._reconnect():
                    break
                continue

            try:
                data = json.loads(raw)
            except (TypeError, ValueError):
                logger.warning("Undecodable WebSocket frame: %r", raw)
                continue

            await self._dispatch(data)

    async def _reconnect(self) -> bool:
        """Reconnect, log in again and re-register subscriptions."""
        logger.warning("WebSocket connection lost. Reconnecting...")
        while self._running:
            await asyncio.sleep(self.reconnect_delay)
            if not self._running:
                break
            try:
                self._ws = await websockets.connect(self.ws_url)
                await self._login()
            except (OSError, websockets.WebSocketException, KiwoomWebSocketError):
                logger.exception("Reconnection failed. Retrying...")
                continue

            # Registrations do not survive a new connection.
            for payload in list(self._subscriptions):
                await self.send(payload)
            logger.info(
                "Reconnected and restored %d subscription(s)", len(self._subscriptions)
            )
            return True
        return False

    async def _dispatch(self, data: dict[str, Any]) -> None:
        trnm = data.get("trnm")

        # PING must be echoed back verbatim or the server drops us.
        if trnm == "PING":
            try:
                await self.send(data)
            except (RuntimeError, websockets.ConnectionClosed):
                logger.warning("Could not answer PING — connection is gone")
            return

        await self._invoke(self._message_callbacks, data)

        if trnm == "REAL":
            for item in data.get("data") or []:
                if isinstance(item, dict):
                    await self._invoke(self._callbacks.get(item.get("type", ""), []), item)
            return

        if trnm:
            await self._invoke(self._trnm_callbacks.get(trnm, []), data)

    @staticmethod
    async def _invoke(callbacks: list[Callback], payload: dict[str, Any]) -> None:
        """Run callbacks, letting one failure not take down the rest."""
        for cb in callbacks:
            try:
                result = cb(payload)
                if inspect.isawaitable(result):
                    await result
            except asyncio.CancelledError:
                raise
            except Exception:
                logger.exception(
                    "Callback error for %s", payload.get("type") or payload.get("trnm")
                )
