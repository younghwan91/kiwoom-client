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

__all__ = ["tick_size", "round_to_tick", "ticks_in"]

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
