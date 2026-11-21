"""KRX tick-size (호가가격단위) rules.

KRX unified the price-band tick-size table across KOSPI, KOSDAQ, and KONEX
effective 2023-01-25 -- before that date KOSDAQ used a coarser table at low
price bands, but the current table below applies identically to all three
markets. Sources:
  - KRX host/member notices on the 2023-01-25 호가가격단위 개편 (e.g. broker
    notices such as Samsung Securities' "국내 증권/파생시장 호가가격단위
    변경 안내" and contemporaneous news coverage of the change), which
    describe the table as applying uniformly to 코스피/코스닥/코넥스/주식선물
    from that date forward.

The table (KRW, price P, tick size):
    P <         2,000            ->      1
    2,000  <= P <     5,000       ->      5
    5,000  <= P <    20,000       ->     10
    20,000 <= P <    50,000       ->     50
    50,000 <= P <   200,000       ->    100
    200,000 <= P <   500,000       ->    500
    P >=      500,000             ->  1,000

Extracted here because three separate repos (scalp-it, krx-signal-engine,
and originally this one's own order-placement callers) each need a valid
price to place a Kiwoom order, and duplicating a boundary table invites
drift -- a single off-by-one at a band edge silently produces a rejected
or mispriced order.
"""

from __future__ import annotations

from decimal import Decimal

__all__ = [
    "add_ticks",
    "is_on_tick",
    "round_to_tick",
    "round_up_to_tick",
    "tick_size",
    "ticks_between",
    "ticks_in",
]

# (upper_bound_exclusive, tick_size) pairs, ascending by price. The last
# entry's upper bound is unused (falls through as "and above").
_TICK_BANDS: tuple[tuple[Decimal, Decimal], ...] = (
    (Decimal("2000"), Decimal("1")),
    (Decimal("5000"), Decimal("5")),
    (Decimal("20000"), Decimal("10")),
    (Decimal("50000"), Decimal("50")),
    (Decimal("200000"), Decimal("100")),
    (Decimal("500000"), Decimal("500")),
)
_TOP_TICK = Decimal("1000")


def tick_size(price: Decimal | int | float) -> Decimal:
    """Return the KRX minimum quote increment (호가가격단위) for a price.

    Args:
        price: The price to quote, in KRW. Must be positive.

    Returns:
        The minimum tick size (KRW) applicable at that price band.

    Raises:
        ValueError: If price is not positive.
    """
    price = Decimal(str(price))
    if price <= 0:
        raise ValueError("price must be positive")
    for upper_bound, tick in _TICK_BANDS:
        if price < upper_bound:
            return tick
    return _TOP_TICK


def round_to_tick(price: Decimal | int | float) -> Decimal:
    """Round a price down to the nearest valid KRX tick for its band.

    Args:
        price: The price to round, in KRW. Must be positive.

    Returns:
        `price` rounded down to the nearest multiple of its tick size.
    """
    price = Decimal(str(price))
    tick = tick_size(price)
    return (price // tick) * tick


def ticks_in(width: Decimal | int | float, price: Decimal | int | float) -> Decimal:
    """How many ticks a price gap ``width`` (KRW) spans at price band ``price``.

    Returns the exact (non-rounded) quotient -- callers that need to
    distinguish e.g. "2.2 ticks" from "3.0 ticks" (a real difference in stop
    noise risk at low price bands) should not round this themselves.
    """
    width = Decimal(str(width))
    return abs(width) / tick_size(price)


# --- Tick arithmetic -------------------------------------------------------
#
# Added on top of the three functions above without touching them. Every
# band edge (2,000 / 5,000 / 20,000 / 50,000 / 200,000 / 500,000) is a
# multiple of the tick on both sides, so "the n-th valid price" is a clean
# piecewise-linear index: band [lower, upper) with tick t holds
# (upper - lower) / t prices.


def _to_decimal(price: Decimal | int | float) -> Decimal:
    return Decimal(str(price))


def is_on_tick(price: Decimal | int | float) -> bool:
    """True if ``price`` is a valid KRX quote — positive and a multiple of its tick.

    >>> is_on_tick(70100), is_on_tick(70150)
    (True, False)
    """
    price = _to_decimal(price)
    if price <= 0:
        return False
    return price % tick_size(price) == 0


def round_up_to_tick(price: Decimal | int | float) -> Decimal:
    """Round a price **up** to the nearest valid KRX tick for its band.

    The counterpart of :func:`round_to_tick` (which rounds down). Rounding up
    can cross into the next band: ``round_up_to_tick(1999.5)`` is ``2000``.

    Raises:
        ValueError: If price is not positive.
    """
    price = _to_decimal(price)
    tick = tick_size(price)
    floored = (price // tick) * tick
    return floored if floored == price else floored + tick


def _require_on_tick(price: Decimal, name: str = "price") -> None:
    if not is_on_tick(price):
        raise ValueError(
            f"{name}={price} 는 유효한 호가가 아닙니다 (호가단위 {tick_size(price)}원). "
            "round_to_tick() / round_up_to_tick() 으로 먼저 맞추세요."
            if price > 0
            else f"{name} must be positive"
        )


def _tick_index(price: Decimal) -> Decimal:
    """Number of valid prices in (0, price] — price must be on a tick."""
    count = Decimal(0)
    lower = Decimal(0)
    for upper, tick in _TICK_BANDS:
        if price <= upper:
            return count + (price - lower) / tick
        count += (upper - lower) / tick
        lower = upper
    return count + (price - lower) / _TOP_TICK


def _price_at_index(index: Decimal) -> Decimal:
    """Inverse of :func:`_tick_index` for index >= 1."""
    count = Decimal(0)
    lower = Decimal(0)
    for upper, tick in _TICK_BANDS:
        size = (upper - lower) / tick
        if index <= count + size:
            return lower + (index - count) * tick
        count += size
        lower = upper
    return lower + (index - count) * _TOP_TICK


def add_ticks(price: Decimal | int | float, ticks: int) -> Decimal:
    """Move ``ticks`` valid quotes up (positive) or down (negative) from ``price``.

    Band edges are handled: one tick up from 1,999 is 2,000, one tick down
    from 2,000 is 1,999 (not 1,995).

    >>> add_ticks(49_950, 2)
    Decimal('50100')

    Args:
        price: A valid quote (see :func:`is_on_tick`).
        ticks: Number of ticks to move; 0 returns ``price``.

    Raises:
        ValueError: If ``price`` is not on a tick, or the move would go to
            zero or below.
    """
    if isinstance(ticks, bool) or not isinstance(ticks, int):
        raise TypeError("ticks must be an int")
    price = _to_decimal(price)
    _require_on_tick(price)
    target = _tick_index(price) + ticks
    if target < 1:
        raise ValueError(f"{price} 에서 {ticks}틱 이동하면 0원 이하가 됩니다")
    return _price_at_index(target)


def ticks_between(start: Decimal | int | float, end: Decimal | int | float) -> int:
    """Signed number of ticks from ``start`` to ``end`` across bands.

    ``add_ticks(start, ticks_between(start, end)) == end`` always holds.
    Unlike :func:`ticks_in`, which divides a width by a single band's tick,
    this counts each band at its own tick size.

    >>> ticks_between(49_900, 50_100)
    3

    Raises:
        ValueError: If either price is not on a tick.
    """
    start_d = _to_decimal(start)
    end_d = _to_decimal(end)
    _require_on_tick(start_d, "start")
    _require_on_tick(end_d, "end")
    return int(_tick_index(end_d) - _tick_index(start_d))
