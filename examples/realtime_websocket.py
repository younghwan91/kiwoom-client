"""Real-time WebSocket example: subscribe to execution (0B) and order book (0D) data."""

import asyncio
import os
import sys
from typing import Any

from kiwoom_rest_api import KiwoomAPI, KiwoomWebSocket


def get_credentials() -> tuple[str, str]:
    app_key = os.environ.get("KIWOOM_APP_KEY")
    app_secret = os.environ.get("KIWOOM_APP_SECRET")
    if not app_key or not app_secret:
        print("Error: KIWOOM_APP_KEY and KIWOOM_APP_SECRET environment variables must be set.")
        sys.exit(1)
    return app_key, app_secret


def on_execution(data: dict[str, Any]) -> None:
    """Callback for 0B (주식체결) real-time data."""
    stk_cd = data.get("stk_cd", "")
    cur_prc = data.get("cur_prc", "")
    cum_vol = data.get("cum_vol", "")
    print(f"[체결] {stk_cd} | 현재가: {cur_prc} | 누적거래량: {cum_vol}")


def on_orderbook(data: dict[str, Any]) -> None:
    """Callback for 0D (주식호가잔량) real-time data."""
    stk_cd = data.get("stk_cd", "")
    ask1 = data.get("ask_prc1", "")
    bid1 = data.get("bid_prc1", "")
    print(f"[호가] {stk_cd} | 매도1호가: {ask1} | 매수1호가: {bid1}")


async def run(ws: KiwoomWebSocket, stock_codes: list[str]) -> None:
    """Connect, subscribe, listen for 30 seconds, then disconnect."""
    await ws.connect()
    print("WebSocket connected.\n")

    # Register callbacks
    ws.on("0B", on_execution)
    ws.on("0D", on_orderbook)

    # Subscribe to execution (0B) and order book (0D) for multiple stocks
    print(f"Subscribing to 0B (체결) for: {stock_codes}")
    await ws.subscribe("0B", stock_codes)

    print(f"Subscribing to 0D (호가잔량) for: {stock_codes}")
    await ws.subscribe("0D", stock_codes)

    print("\nListening for 30 seconds... (press Ctrl+C to stop early)\n")

    # Run listen loop for 30 seconds then disconnect
    try:
        await asyncio.wait_for(ws.listen(), timeout=30.0)
    except asyncio.TimeoutError:
        print("\n30 seconds elapsed.")

    await ws.disconnect()
    print("WebSocket disconnected.")


def main() -> None:
    app_key, app_secret = get_credentials()

    api = KiwoomAPI(app_key=app_key, app_secret=app_secret, is_mock=True)

    print("Logging in...")
    api.login()
    print("Login successful.\n")

    # Create WebSocket client from the authenticated API
    ws = api.create_websocket()

    # Subscribe to multiple stocks
    stock_codes = ["005930", "000660", "035420"]  # Samsung, SK Hynix, NAVER
    print(f"Watching stocks: {stock_codes}\n")

    try:
        asyncio.run(run(ws, stock_codes))
    except KeyboardInterrupt:
        print("\nInterrupted by user.")

    api.logout()
    api.close()
    print("Done.")


if __name__ == "__main__":
    main()
