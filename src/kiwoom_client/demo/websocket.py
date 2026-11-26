"""A fake Kiwoom WebSocket for demo mode: LOGIN, real-time REG/REAL, condition search.

:class:`DemoWebSocket` is a :class:`~kiwoom_client.websocket.KiwoomWebSocket`
whose connection is an in-process object (:class:`DemoConnection`) instead of
a socket, so ``subscribe``/``listen``/callbacks and the MCP session above
them run unchanged. Real-time trades (0B) are a small random walk around the
demo's synthetic price; they are not real ticks. Every frame carries
``"_demo"``.
"""

from __future__ import annotations

import asyncio
import contextlib
import json
import random
from datetime import datetime
from typing import TYPE_CHECKING, Any

import websockets

from kiwoom_client import spec
from kiwoom_client.demo.backend import (
    DEMO_KEY,
    DEMO_NOTICE,
    directed,
    rate,
    sign_code,
    signed,
)
from kiwoom_client.demo.market import BY_CODE, KST, UNIVERSE, DemoStock
from kiwoom_client.tick_size import add_ticks
from kiwoom_client.websocket import KiwoomWebSocket

if TYPE_CHECKING:
    from kiwoom_client.demo.backend import DemoBackend

DEMO_WS_URL = "demo://kiwoom-client.invalid/websocket"

#: Seconds between real-time pushes.
TICK_INTERVAL = 0.2

#: Saved conditions of the demo account (seq, name).
CONDITIONS: tuple[tuple[str, str], ...] = (
    ("0", "급등주"),
    ("1", "거래량 급증"),
    ("2", "52주 신고가 근접"),
    ("3", "대형 우량주"),
)


class DemoConnection:
    """Stands in for ``websockets.ClientConnection``: ``send``/``recv``/``close``."""

    def __init__(self, backend: DemoBackend) -> None:
        self._backend = backend
        self._inbox: asyncio.Queue[str | None] = asyncio.Queue()
        #: (grp_no, type, item) currently registered.
        self._registered: set[tuple[str, str, str]] = set()
        self._ticker: asyncio.Task[None] | None = None
        self._prices: dict[str, int] = {}
        self._volumes: dict[str, int] = {}
        self._rng = random.Random(f"kiwoom-client-demo:{backend.market.seed}:ticks")
        self.sent: list[dict[str, Any]] = []
        self.closed = False

    # --- the ClientConnection surface KiwoomWebSocket uses ------------------

    async def send(self, raw: str) -> None:
        if self.closed:
            raise websockets.ConnectionClosedOK(None, None)
        message = json.loads(raw)
        self.sent.append(message)
        trnm = message.get("trnm")
        if trnm == "LOGIN":
            self._reply({"trnm": "LOGIN", "return_code": 0, "return_msg": "데모 로그인 (가상)"})
        elif trnm in ("REG", "REMOVE"):
            self._registration(message)
        elif trnm == "CNSRLST":
            self._reply({
                "trnm": "CNSRLST", "return_code": 0, "return_msg": "",
                "data": [list(c) for c in CONDITIONS],
            })  # fmt: skip
        elif trnm == "CNSRREQ":
            self._condition_search(message)
        elif trnm == "CNSRCLR":
            self._reply({"trnm": "CNSRCLR", "seq": message.get("seq"), "return_code": 0})

    async def recv(self) -> str:
        item = await self._inbox.get()
        if item is None:
            raise websockets.ConnectionClosedOK(None, None)
        return item

    async def close(self) -> None:
        if self.closed:
            return
        self.closed = True
        if self._ticker is not None:
            self._ticker.cancel()
            with contextlib.suppress(asyncio.CancelledError):
                await self._ticker
        self._inbox.put_nowait(None)

    # --- protocol -----------------------------------------------------------

    def _reply(self, frame: dict[str, Any]) -> None:
        self._inbox.put_nowait(json.dumps({**frame, DEMO_KEY: DEMO_NOTICE}, ensure_ascii=False))

    def _registration(self, message: dict[str, Any]) -> None:
        trnm, grp = message["trnm"], str(message.get("grp_no", "1"))
        if trnm == "REG" and str(message.get("refresh", "1")) == "0":
            self._registered = {r for r in self._registered if r[0] != grp}
        for entry in message.get("data") or []:
            for data_type in entry.get("type") or []:
                for item in entry.get("item") or []:
                    key = (grp, str(data_type), str(item))
                    if trnm == "REG":
                        self._registered.add(key)
                    else:
                        self._registered.discard(key)
        self._reply({"trnm": trnm, "return_code": 0, "return_msg": ""})
        if self._registered and self._ticker is None:
            self._ticker = asyncio.get_running_loop().create_task(self._tick_forever())

    async def _tick_forever(self) -> None:
        while not self.closed:
            await asyncio.sleep(TICK_INTERVAL)
            pairs = sorted({(t, i) for _g, t, i in self._registered})
            data = [frame for t, i in pairs if (frame := self._real_item(t, i)) is not None]
            if data:
                self._reply({"trnm": "REAL", "data": data})

    def _real_item(self, data_type: str, item: str) -> dict[str, Any] | None:
        stock = BY_CODE.get(item.strip().upper().lstrip("A")[:6])
        if stock is None:
            return None
        values = self._trade(stock) if data_type in ("0B", "0A") else {}
        try:
            tr = spec.get(data_type)
        except KeyError:
            tr = None
        if tr is not None:
            quote = self._backend._quote(stock)
            for f in tr.response:
                if f.parent == "values" and f.id not in values:
                    values[f.id] = self._backend._guess(f, quote, 0)
        name = tr.name if tr is not None else data_type
        return {"type": data_type, "name": name, "item": stock.code, "values": values}

    def _trade(self, stock: DemoStock) -> dict[str, Any]:
        """One synthetic trade: the price moves at most a tick at a time."""
        bar = self._backend.market.today_bar(stock.code)
        price = self._prices.get(stock.code, bar.close)
        step = self._rng.choice((-1, 0, 0, 1))
        moved = int(add_ticks(price, step)) if step else price
        lo, hi = int(bar.close * 0.98), int(bar.close * 1.02)
        price = moved if lo <= moved <= hi else price
        self._prices[stock.code] = price
        qty = self._rng.randint(1, 300) * self._rng.choice((1, -1))
        volume = self._volumes.get(stock.code, bar.volume) + abs(qty)
        self._volumes[stock.code] = volume
        change = price - bar.prev_close
        change_pct = change / bar.prev_close * 100 if bar.prev_close else 0.0
        return {
            "20": datetime.now(KST).strftime("%H%M%S"),
            "10": directed(price, change),
            "11": signed(change),
            "12": rate(change_pct),
            "27": directed(int(add_ticks(price, 1)), change),
            "28": directed(price, change),
            "15": signed(qty),
            "13": str(volume),
            "14": str(volume * price // 1_000_000),
            "16": directed(bar.open, bar.open - bar.prev_close),
            "17": directed(max(bar.high, price), max(bar.high, price) - bar.prev_close),
            "18": directed(min(bar.low, price), min(bar.low, price) - bar.prev_close),
            "25": sign_code(change),
            "290": "2",
            "9081": "1",
        }

    def _condition_search(self, message: dict[str, Any]) -> None:
        seq = str(message.get("seq", ""))
        if seq not in {s for s, _ in CONDITIONS}:
            self._reply({
                "trnm": "CNSRREQ", "seq": seq, "return_code": 1,
                "return_msg": f"조건검색식 번호를 확인하세요: {seq!r} (데모)",
            })  # fmt: skip
            return
        rows = []
        for stock in self._matches(seq):
            bar = self._backend.market.today_bar(stock.code)
            rows.append({
                "9001": f"A{stock.code}",
                "302": stock.name,
                "10": f"{bar.close:09d}",
                "25": sign_code(bar.change),
                "11": f"{bar.change:+010d}" if bar.change else f"{0:010d}",
                "12": f"{bar.change_pct:+013.2f}" if bar.change else "0.00",
                "13": f"{bar.volume:012d}",
                "16": f"{bar.open:09d}",
                "17": f"{bar.high:09d}",
                "18": f"{bar.low:09d}",
            })  # fmt: skip
        self._reply({
            "trnm": "CNSRREQ", "seq": seq, "cont_yn": "N", "next_key": "",
            "return_code": 0, "return_msg": "", "data": rows,
        })  # fmt: skip

    def _matches(self, seq: str) -> list[DemoStock]:
        market = self._backend.market
        stats = [(s, market.daily(s.code)) for s in UNIVERSE if s.market != "8"]
        if seq == "0":
            picked = sorted(stats, key=lambda t: -t[1][-1].change_pct)[:5]
        elif seq == "1":
            picked = sorted(stats, key=lambda t: -t[1][-1].volume / max(t[1][-2].volume, 1))[:5]
        elif seq == "2":
            picked = sorted(
                stats, key=lambda t: -t[1][-1].close / max(b.high for b in t[1][-250:])
            )[:5]
        else:
            picked = sorted(stats, key=lambda t: -t[1][-1].close * t[0].shares)[:6]
        return [s for s, _ in picked]


class DemoWebSocket(KiwoomWebSocket):
    """A :class:`KiwoomWebSocket` wired to the demo backend instead of a server."""

    def __init__(self, backend: DemoBackend, reconnect_delay: float = 1.0) -> None:
        super().__init__("demo-token", ws_url=DEMO_WS_URL, reconnect_delay=reconnect_delay)
        self._backend = backend

    async def connect(self) -> None:
        self._ws = DemoConnection(self._backend)  # type: ignore[assignment]
        await self._login()

    async def _reconnect(self) -> bool:
        return False  # the in-process connection only closes when asked to
