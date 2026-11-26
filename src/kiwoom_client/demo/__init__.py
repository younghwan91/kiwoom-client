"""Demo mode: try kiwoom-client with no Kiwoom account, app key or network.

:class:`DemoBackend` is a fake Kiwoom REST server living in the process
(an ``httpx.MockTransport``). It serves synthetic, deterministic data for
real stock names and codes — **the prices are made up** and every response
carries ``"_demo": "가상 데이터 — 실제 시세·계좌가 아닙니다"``. Orders are paper
trades in memory. :class:`DemoWebSocket` fakes the real-time socket (0B
trades, condition search) the same way.

Nothing here opens a socket: no real key, no live server, no mock server.
"""

from __future__ import annotations

from kiwoom_client.demo.backend import (
    DEMO_BASE_URL,
    DEMO_KEY,
    DEMO_NOTICE,
    DemoBackend,
    DemoRefusal,
)
from kiwoom_client.demo.market import DEFAULT_SEED, UNIVERSE, DemoStock
from kiwoom_client.demo.websocket import DemoWebSocket

__all__ = [
    "DEFAULT_SEED",
    "DEMO_BASE_URL",
    "DEMO_KEY",
    "DEMO_NOTICE",
    "UNIVERSE",
    "DemoBackend",
    "DemoRefusal",
    "DemoStock",
    "DemoWebSocket",
]
