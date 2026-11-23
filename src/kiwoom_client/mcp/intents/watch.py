"""``watch`` — collect live trades (주식체결, real-time type 0B) for a few seconds.

MCP tools answer once, so this registers 0B for the stocks on the server's
shared WebSocket session, gathers trades for up to :data:`MAX_SECONDS`
seconds, unregisters, and returns one summary per stock. With ``until``
(``{"stock": "005930", "above": 72000}`` or ``"below"``) it returns as soon
as a trade crosses that price.

Field ids are those of the 0B spec: 10 현재가 (sign = direction), 12 등락율,
13 누적거래량, 15 거래량 (+ 매수체결, - 매도체결), 20 체결시간.
"""

from __future__ import annotations

import asyncio
from typing import Any

from kiwoom_client.mcp.intents.normalize import date, num, pct, price, stock_code
from kiwoom_client.mcp.intents.quotes import parse_stock_list
from kiwoom_client.mcp.intents.registry import IntentContext, read_only_tool, register
from kiwoom_client.mcp.intents.resolve import resolve_stock
from kiwoom_client.mcp.local_tools import LocalTool

REALTIME_TYPE = "0B"
DEFAULT_SECONDS = 10
MAX_SECONDS = 60
MAX_STOCKS = 10

#: Real-time group used for watches, apart from anything else registered.
WATCH_GROUP = "9"

NO_TICKS = "체결이 없었습니다 — 장 시간이 아니거나 거래가 없는 종목일 수 있습니다"


class TickStats:
    """Running summary of one stock's trades."""

    def __init__(self, code: str, name: str | None) -> None:
        self.code = code
        self.name = name
        self.ticks = 0
        self.first: float | None = None
        self.last: float | None = None
        self.high: float | None = None
        self.low: float | None = None
        self.volume = 0
        self.buy_volume = 0
        self.sell_volume = 0
        self.cumulative_volume: Any = None
        self.change_pct: float | None = None
        self.last_time: str | None = None

    def add(self, values: dict[str, Any]) -> float | None:
        trade_price = price(values.get("10"))
        if trade_price is None:
            return None
        self.ticks += 1
        self.first = trade_price if self.first is None else self.first
        self.last = trade_price
        self.high = trade_price if self.high is None else max(self.high, trade_price)
        self.low = trade_price if self.low is None else min(self.low, trade_price)
        qty = num(values.get("15"))
        if isinstance(qty, (int, float)):
            self.volume += abs(int(qty))
            if qty > 0:
                self.buy_volume += int(qty)
            elif qty < 0:
                self.sell_volume += -int(qty)
        if values.get("13") not in (None, ""):
            self.cumulative_volume = price(values.get("13"))
        if values.get("12") not in (None, ""):
            self.change_pct = pct(values.get("12"))
        if values.get("20") not in (None, ""):
            self.last_time = date(values.get("20"))
        return trade_price

    def as_dict(self) -> dict[str, Any]:
        out: dict[str, Any] = {"code": self.code, "name": self.name, "ticks": self.ticks}
        if not self.ticks:
            out["note"] = NO_TICKS
            return out
        out.update(
            first_price=self.first,
            last_price=self.last,
            high=self.high,
            low=self.low,
            move_pct=(
                round((self.last / self.first - 1) * 100, 2)
                if self.first and self.last is not None
                else None
            ),
            volume=self.volume,
            buy_volume=self.buy_volume,
            sell_volume=self.sell_volume,
            cumulative_volume=self.cumulative_volume,
            change_pct=self.change_pct,
            last_time=self.last_time,
        )
        return out


def _seconds(value: Any) -> float:
    if value in (None, ""):
        return float(DEFAULT_SECONDS)
    try:
        seconds = float(value)
    except (TypeError, ValueError) as exc:
        raise ValueError(f"seconds 는 숫자여야 합니다: {value!r}") from exc
    return max(1.0, min(seconds, float(MAX_SECONDS)))


async def _condition(api: Any, until: Any, codes: list[str]) -> tuple[str, str, float] | None:
    """``until`` → ``(code, "above"|"below", price)``; ``None`` when unset."""
    if until in (None, "", {}):
        return None
    if not isinstance(until, dict):
        raise ValueError('until 은 {"stock": "005930", "above": 72000} 형태여야 합니다')
    directions = [key for key in ("above", "below") if until.get(key) not in (None, "")]
    if len(directions) != 1:
        raise ValueError("until 에는 above 나 below 중 하나만 넣습니다")
    direction = directions[0]
    level = num(until[direction])
    if level is None or level <= 0:
        raise ValueError(f"until.{direction} 는 양수 가격이어야 합니다")
    if until.get("stock") in (None, ""):
        if len(codes) != 1:
            raise ValueError("여러 종목을 볼 때는 until.stock 으로 조건 종목을 정합니다")
        code = codes[0]
    else:
        code = (await resolve_stock(api, until["stock"])).code
        if code not in codes:
            raise ValueError(f"until.stock {code} 가 stocks 에 없습니다")
    return code, direction, float(level)


async def watch(
    api: Any, session: Any, stocks: Any, *, seconds: Any = None, until: Any = None
) -> dict[str, Any]:
    if session is None:
        raise ValueError("이 서버에는 WebSocket 세션이 없어 실시간 감시를 할 수 없습니다")
    queries = parse_stock_list(stocks)
    if not queries:
        raise ValueError("stocks(종목명 또는 코드 목록)이 필요합니다")
    if len(queries) > MAX_STOCKS:
        raise ValueError(f"한 번에 {MAX_STOCKS}종목까지 감시합니다")
    resolved = [await resolve_stock(api, query) for query in queries]
    stats = {stock.code: TickStats(stock.code, stock.name) for stock in resolved}
    codes = list(stats)
    condition = await _condition(api, until, codes)
    window = _seconds(seconds)

    loop = asyncio.get_running_loop()
    started = loop.time()
    deadline = started + window
    triggered: dict[str, Any] | None = None
    async with session.realtime([REALTIME_TYPE], codes, grp_no=WATCH_GROUP) as queue:
        while triggered is None:
            remaining = deadline - loop.time()
            if remaining <= 0:
                break
            try:
                item = await asyncio.wait_for(queue.get(), remaining)
            except asyncio.TimeoutError:
                break
            code = stock_code(item.get("item"))
            values = item.get("values")
            if code not in stats or not isinstance(values, dict):
                continue
            trade_price = stats[code].add(values)
            if condition and trade_price is not None and code == condition[0]:
                _, direction, level = condition
                if (direction == "above" and trade_price >= level) or (
                    direction == "below" and trade_price <= level
                ):
                    triggered = {
                        "stock": code,
                        "condition": f"{direction} {level:g}",
                        "price": trade_price,
                        "time": stats[code].last_time,
                    }
    elapsed = round(loop.time() - started, 1)
    return {
        "source": "실시간 0B 주식체결 (WebSocket)",
        "seconds_requested": window,
        "elapsed_seconds": elapsed,
        "until": ({"stock": condition[0], condition[1]: condition[2]} if condition else None),
        "triggered": triggered,
        "stocks": [stats[code].as_dict() for code in codes],
    }


@register
def watch_tools(context: IntentContext) -> list[LocalTool]:
    async def handler(api: Any, arguments: dict[str, Any]) -> dict[str, Any]:
        return await watch(
            api,
            context.session,
            arguments.get("stocks"),
            seconds=arguments.get("seconds"),
            until=arguments.get("until"),
        )

    return [
        read_only_tool(
            name="watch",
            title="실시간 체결 감시 (최대 60초)",
            description=(
                f"종목(최대 {MAX_STOCKS}개)의 실시간 체결을 seconds 초(최대 {MAX_SECONDS}) 동안 "
                "모아 종목별 마지막가·고저·체결량(매수/매도)·틱 수를 돌려준다(WebSocket 0B). "
                'until 가격 조건(예: {"stock": "005930", "above": 72000})에 걸리면 바로 '
                "돌아온다. '지금 삼성전자 움직임 봐줘', '7만2천 넘으면 알려줘'에 쓴다. "
                "장 시간이 아니면 체결이 없다."
            ),
            properties={
                "stocks": {
                    "type": "array",
                    "items": {"type": "string"},
                    "maxItems": MAX_STOCKS,
                    "description": "종목명 또는 코드 목록",
                },
                "seconds": {
                    "type": "number",
                    "minimum": 1,
                    "maximum": MAX_SECONDS,
                    "default": DEFAULT_SECONDS,
                },
                "until": {
                    "type": "object",
                    "properties": {
                        "stock": {"type": "string"},
                        "above": {"type": "number"},
                        "below": {"type": "number"},
                    },
                    "description": "이 가격 이상(above)·이하(below) 체결이 나오면 즉시 반환",
                },
            },
            required=("stocks",),
            toolset="market",
            handler=handler,
            example={"stocks": ["005930"], "seconds": 5},
        )
    ]
