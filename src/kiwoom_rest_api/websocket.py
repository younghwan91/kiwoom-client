"""WebSocket client for Kiwoom REST API real-time data."""

from __future__ import annotations

import asyncio
import json
import logging
from typing import Any, Callable

import websockets
from websockets.asyncio.client import ClientConnection

logger = logging.getLogger(__name__)

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


class KiwoomWebSocket:
    """WebSocket client for real-time market data from Kiwoom.

    Args:
        access_token: Bearer access token.
        is_mock: Use mock trading WebSocket server if True.
    """

    PROD_WS_URL = "wss://api.kiwoom.com:10000/api/dostk/websocket"
    MOCK_WS_URL = "wss://mockapi.kiwoom.com:10000/api/dostk/websocket"

    def __init__(self, access_token: str, is_mock: bool = False):
        self.access_token = access_token
        self.ws_url = self.MOCK_WS_URL if is_mock else self.PROD_WS_URL
        self._ws: ClientConnection | None = None
        self._callbacks: dict[str, list[Callable[[dict[str, Any]], None]]] = {}
        self._running = False

    async def connect(self) -> None:
        """Establish WebSocket connection."""
        self._ws = await websockets.connect(
            self.ws_url,
            additional_headers={"authorization": f"Bearer {self.access_token}"},
        )
        logger.info("WebSocket connected to %s", self.ws_url)

    async def disconnect(self) -> None:
        """Close WebSocket connection."""
        self._running = False
        if self._ws:
            await self._ws.close()
            self._ws = None
            logger.info("WebSocket disconnected")

    def on(self, data_type: str, callback: Callable[[dict[str, Any]], None]) -> None:
        """Register a callback for a real-time data type.

        Args:
            data_type: Real-time data type code (e.g., "0B" for 주식체결).
            callback: Function to call when data of this type arrives.
        """
        if data_type not in self._callbacks:
            self._callbacks[data_type] = []
        self._callbacks[data_type].append(callback)

    async def subscribe(self, api_id: str, stock_codes: list[str] | str) -> None:
        """Subscribe to real-time data for given stock codes.

        Args:
            api_id: Real-time data type code (e.g., "0B").
            stock_codes: Single stock code or list of stock codes.
        """
        if not self._ws:
            raise RuntimeError("WebSocket not connected. Call connect() first.")

        if isinstance(stock_codes, str):
            stock_codes = [stock_codes]

        msg = {
            "trnm": "subscribe",
            "grp_no": api_id,
            "refresh": "0",
            "stk_cd_lst": stock_codes,
        }
        await self._ws.send(json.dumps(msg))
        logger.info("Subscribed to %s for %s", api_id, stock_codes)

    async def unsubscribe(self, api_id: str, stock_codes: list[str] | str) -> None:
        """Unsubscribe from real-time data.

        Args:
            api_id: Real-time data type code.
            stock_codes: Single stock code or list of stock codes.
        """
        if not self._ws:
            raise RuntimeError("WebSocket not connected. Call connect() first.")

        if isinstance(stock_codes, str):
            stock_codes = [stock_codes]

        msg = {
            "trnm": "unsubscribe",
            "grp_no": api_id,
            "stk_cd_lst": stock_codes,
        }
        await self._ws.send(json.dumps(msg))
        logger.info("Unsubscribed from %s for %s", api_id, stock_codes)

    async def send_condition_search(self, api_id: str, body: dict[str, Any]) -> None:
        """Send a condition search request via WebSocket.

        Args:
            api_id: Condition search API ID (ka10171-ka10174).
            body: Request body parameters.
        """
        if not self._ws:
            raise RuntimeError("WebSocket not connected. Call connect() first.")

        msg = {"api_id": api_id, **body}
        await self._ws.send(json.dumps(msg))

    async def listen(self) -> None:
        """Listen for incoming WebSocket messages and dispatch to callbacks.

        Runs until disconnect() is called or connection is lost.
        Automatically attempts reconnection on connection failure.
        """
        if not self._ws:
            raise RuntimeError("WebSocket not connected. Call connect() first.")

        self._running = True
        while self._running:
            try:
                raw = await self._ws.recv()
                data = json.loads(raw)
                data_type = data.get("grp_no") or data.get("api_id", "")

                callbacks = self._callbacks.get(data_type, [])
                for cb in callbacks:
                    try:
                        cb(data)
                    except Exception:
                        logger.exception("Callback error for type %s", data_type)

            except websockets.ConnectionClosed:
                if not self._running:
                    break
                logger.warning("WebSocket connection lost. Reconnecting...")
                await asyncio.sleep(1)
                try:
                    await self.connect()
                except Exception:
                    logger.exception("Reconnection failed. Retrying in 5s...")
                    await asyncio.sleep(5)
