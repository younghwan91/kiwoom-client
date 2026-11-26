# ruff: noqa: E501  (the UNIVERSE table reads best one stock per line)
"""Synthetic market for demo mode: real stock names and codes, made-up prices.

Everything is a pure function of ``seed`` and the stock code, so the same
seed gives the same prices on every run. Dates are business days (Mon-Fri,
holidays ignored) counted back from the latest one on or before today in
Korea, so a chart always ends "today" while the prices stay put.

None of these prices are real quotes. They only need to look and behave like
a market: on-tick prices, OHLC that hang together, volumes, daily limits.
"""

from __future__ import annotations

import math
import random
from dataclasses import dataclass
from datetime import date, datetime, timedelta, timezone
from functools import lru_cache

from kiwoom_client.tick_size import round_to_tick, round_up_to_tick

#: Korea Standard Time (no DST).
KST = timezone(timedelta(hours=9))

#: Business days of daily history kept per stock (~2.4 years).
HISTORY_DAYS = 600

#: Regular session minutes, 09:00 to 15:29 (the 15:30 close is the last bar's close).
SESSION_MINUTES = 390

#: KRX daily price limit (±30% of the previous close).
LIMIT_RATE = 0.30

DEFAULT_SEED = 7

#: ka10099 mrkt_tp → market name, as the listing shows it.
MARKET_NAMES = {"0": "거래소", "10": "코스닥", "8": "ETF"}


@dataclass(frozen=True)
class DemoStock:
    """One stock of the demo universe. ``close`` is the synthetic last close."""

    code: str
    name: str
    market: str  # ka10099 mrkt_tp: "0" 코스피, "10" 코스닥, "8" ETF
    close: int
    shares: int  # listed shares
    sector: str
    volatility: float  # daily return standard deviation
    margin_rate: int  # 종목증거금율 (%)
    per: float
    pbr: float
    roe: float


#: Real names and codes; every number next to them is invented for the demo.
UNIVERSE: tuple[DemoStock, ...] = (
    DemoStock("005930", "삼성전자", "0", 71500, 5_969_782_550, "전기전자", 0.016, 20, 14.2, 1.31, 9.3),
    DemoStock("000660", "SK하이닉스", "0", 182000, 728_002_365, "전기전자", 0.024, 30, 8.7, 1.92, 22.1),
    DemoStock("373220", "LG에너지솔루션", "0", 365000, 234_000_000, "전기전자", 0.022, 40, 61.5, 3.48, 5.7),
    DemoStock("207940", "삼성바이오로직스", "0", 812000, 71_174_000, "의약품", 0.018, 40, 58.3, 5.84, 10.2),
    DemoStock("005380", "현대차", "0", 214500, 209_416_191, "운수장비", 0.017, 20, 4.9, 0.62, 12.8),
    DemoStock("000270", "기아", "0", 98700, 397_672_632, "운수장비", 0.018, 20, 4.1, 0.88, 19.6),
    DemoStock("068270", "셀트리온", "0", 176300, 216_889_584, "의약품", 0.021, 30, 44.8, 2.65, 5.9),
    DemoStock("035420", "NAVER", "0", 187600, 158_437_008, "서비스업", 0.019, 30, 21.3, 1.12, 5.3),
    DemoStock("035720", "카카오", "0", 38450, 443_000_000, "서비스업", 0.023, 40, 52.4, 1.86, 3.5),
    DemoStock("105560", "KB금융", "0", 79800, 393_500_000, "금융업", 0.015, 20, 6.8, 0.55, 8.9),
    DemoStock("055550", "신한지주", "0", 51200, 509_000_000, "금융업", 0.014, 20, 6.1, 0.49, 8.2),
    DemoStock("005490", "POSCO홀딩스", "0", 312000, 84_571_230, "철강금속", 0.020, 30, 18.9, 0.61, 3.2),
    DemoStock("051910", "LG화학", "0", 284500, 70_592_343, "화학", 0.022, 30, 33.7, 0.82, 2.4),
    DemoStock("006400", "삼성SDI", "0", 251000, 68_764_530, "전기전자", 0.023, 30, 27.6, 1.05, 3.8),
    DemoStock("012330", "현대모비스", "0", 238000, 93_000_000, "운수장비", 0.016, 20, 6.5, 0.52, 8.0),
    DemoStock("028260", "삼성물산", "0", 132400, 169_976_544, "유통업", 0.017, 20, 11.4, 0.71, 6.2),
    DemoStock("086520", "에코프로", "10", 88900, 133_138_340, "일반전기전자", 0.034, 40, 0.0, 6.15, -4.1),
    DemoStock("247540", "에코프로비엠", "10", 152300, 97_801_344, "일반전기전자", 0.031, 40, 0.0, 7.42, -2.6),
    DemoStock("196170", "알테오젠", "10", 341500, 53_000_000, "제약", 0.033, 40, 210.4, 38.1, 18.1),
    DemoStock("069500", "KODEX 200", "8", 36850, 160_000_000, "ETF", 0.012, 20, 0.0, 0.0, 0.0),
)  # fmt: skip

BY_CODE: dict[str, DemoStock] = {stock.code: stock for stock in UNIVERSE}


def today_kst() -> date:
    return datetime.now(KST).date()


def session_day(today: date | None = None) -> date:
    """The latest business day on or before ``today`` (Korea)."""
    day = today or today_kst()
    while day.weekday() >= 5:
        day -= timedelta(days=1)
    return day


def business_days(end: date, count: int) -> list[date]:
    """``count`` business days ending at ``end`` (a business day), oldest first."""
    days: list[date] = []
    day = end
    while len(days) < count:
        if day.weekday() < 5:
            days.append(day)
        day -= timedelta(days=1)
    return days[::-1]


def tick_price(value: float) -> int:
    """A positive on-tick price (rounded down)."""
    return int(round_to_tick(max(value, 1.0)))


@dataclass(frozen=True)
class Bar:
    """One candle. ``time`` is ``YYYYMMDD`` (daily) or ``YYYYMMDDHHMMSS`` (minute)."""

    time: str
    open: int
    high: int
    low: int
    close: int
    volume: int
    prev_close: int

    @property
    def change(self) -> int:
        return self.close - self.prev_close

    @property
    def change_pct(self) -> float:
        return round(self.change / self.prev_close * 100, 2) if self.prev_close else 0.0

    @property
    def value(self) -> int:
        """Traded value in KRW (approximated with the bar's mid price)."""
        return int(self.volume * (self.high + self.low) / 2)


@dataclass
class Market:
    """The synthetic price history of every stock in :data:`UNIVERSE`."""

    seed: int = DEFAULT_SEED
    today: date | None = None

    @property
    def session(self) -> date:
        return session_day(self.today)

    def stock(self, code: str) -> DemoStock | None:
        return BY_CODE.get(code.strip().upper().lstrip("A")[:6]) if code else None

    def daily(self, code: str) -> list[Bar]:
        """Daily bars, oldest first, the last one being the current session."""
        return list(_daily_bars(self.seed, code, self.session))

    def today_bar(self, code: str) -> Bar:
        return self.daily(code)[-1]

    def price(self, code: str) -> int:
        return self.today_bar(code).close

    def limits(self, code: str) -> tuple[int, int]:
        """(upper, lower) daily price limit from the previous close."""
        prev = self.today_bar(code).prev_close
        upper = int(round_to_tick(prev * (1 + LIMIT_RATE)))
        lower = int(round_up_to_tick(max(prev * (1 - LIMIT_RATE), 1)))
        return upper, lower

    def minutes(self, code: str) -> list[Bar]:
        """1-minute bars of the current session, oldest first."""
        return list(_minute_bars(self.seed, code, self.session))


def _rng(seed: int, *parts: object) -> random.Random:
    return random.Random(":".join(["kiwoom-client-demo", str(seed), *map(str, parts)]))


@lru_cache(maxsize=64)
def _daily_bars(seed: int, code: str, end: date) -> tuple[Bar, ...]:
    stock = BY_CODE[code]
    rng = _rng(seed, code, "daily")
    days = business_days(end, HISTORY_DAYS + 1)
    # Walk backwards from the fixed last close, so "today" always shows it.
    closes = [float(stock.close)]
    for _ in range(HISTORY_DAYS):
        ret = rng.gauss(0.0004, stock.volatility)
        closes.append(closes[-1] / (1 + max(ret, -0.25)))
    closes.reverse()
    prices = [tick_price(c) for c in closes]
    base_volume = stock.shares * 0.0022
    bars: list[Bar] = []
    for i in range(1, len(days)):
        prev, close = prices[i - 1], prices[i]
        open_ = tick_price(prev * (1 + rng.gauss(0, stock.volatility / 3)))
        spread = abs(rng.gauss(0, stock.volatility / 2))
        high = max(open_, close, tick_price(max(open_, close) * (1 + spread)))
        low = min(open_, close, tick_price(min(open_, close) * (1 - spread)))
        move = abs(close / prev - 1) / stock.volatility if prev else 0
        volume = int(base_volume * rng.lognormvariate(0, 0.35) * (1 + 0.6 * move))
        bars.append(Bar(days[i].strftime("%Y%m%d"), open_, high, low, close, volume, prev))
    return tuple(bars)


@lru_cache(maxsize=64)
def _minute_bars(seed: int, code: str, day: date) -> tuple[Bar, ...]:
    daily = _daily_bars(seed, code, day)[-1]
    rng = _rng(seed, code, "minute", day.isoformat())
    # A Brownian bridge from the open to the close, kept inside the day's range.
    steps = [rng.gauss(0, 1) for _ in range(SESSION_MINUTES)]
    total = sum(steps)
    path = [float(daily.open)]
    scale = (daily.high - daily.low) / max(math.sqrt(SESSION_MINUTES), 1) or 1.0
    drift = (daily.close - daily.open) / SESSION_MINUTES
    for step in steps:
        path.append(path[-1] + drift + (step - total / SESSION_MINUTES) * scale * 0.6)
    path[-1] = float(daily.close)
    lo, hi = float(daily.low), float(daily.high)
    path = [min(max(p, lo), hi) for p in path]
    weights = [1.6 if i < 30 or i >= SESSION_MINUTES - 30 else 1.0 for i in range(SESSION_MINUTES)]
    unit = daily.volume / sum(weights)
    start = datetime(day.year, day.month, day.day, 9, 0)
    bars: list[Bar] = []
    prev_close = daily.prev_close
    for i in range(SESSION_MINUTES):
        open_, close = tick_price(path[i]), tick_price(path[i + 1])
        wiggle = abs(rng.gauss(0, 0.3)) * (scale or 1)
        high = min(max(open_, close, tick_price(max(open_, close) + wiggle)), daily.high)
        low = max(min(open_, close, tick_price(min(open_, close) - wiggle)), daily.low)
        volume = max(int(unit * weights[i] * rng.lognormvariate(0, 0.5)), 1)
        stamp = (start + timedelta(minutes=i)).strftime("%Y%m%d%H%M%S")
        bars.append(Bar(stamp, open_, high, low, close, volume, prev_close))
    return tuple(bars)


def aggregate(bars: list[Bar], key_len: int, *, group: str = "day") -> list[Bar]:
    """Merge consecutive bars into weekly/monthly/yearly ones (``group``) or
    into N-minute ones (``key_len`` = N, ``group="minute"``). Oldest first."""
    groups: list[list[Bar]] = []
    last_key: object = None
    for i, bar in enumerate(bars):
        if group == "minute":
            key: object = i // key_len
        elif group == "week":
            key = datetime.strptime(bar.time[:8], "%Y%m%d").isocalendar()[:2]
        elif group == "month":
            key = bar.time[:6]
        else:
            key = bar.time[:4]
        if key != last_key:
            groups.append([])
            last_key = key
        groups[-1].append(bar)
    out: list[Bar] = []
    for chunk in groups:
        out.append(
            Bar(
                time=chunk[0].time,
                open=chunk[0].open,
                high=max(b.high for b in chunk),
                low=min(b.low for b in chunk),
                close=chunk[-1].close,
                volume=sum(b.volume for b in chunk),
                prev_close=chunk[0].prev_close,
            )
        )
    return out
