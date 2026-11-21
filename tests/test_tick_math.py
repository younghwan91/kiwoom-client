"""Tests for the tick-arithmetic helpers added to kiwoom_client.tick_size.

Also pins the results of the three original functions at every band edge:
krx-quant-core treats this module as the canonical tick table, so their
output must never move.
"""

from __future__ import annotations

from decimal import Decimal

import pytest

import kiwoom_client
from kiwoom_client.tick_size import (
    add_ticks,
    is_on_tick,
    round_to_tick,
    round_up_to_tick,
    tick_size,
    ticks_between,
    ticks_in,
)

EDGES = (2_000, 5_000, 20_000, 50_000, 200_000, 500_000)

# (price, tick_size, round_to_tick) — the existing behaviour, frozen.
GOLDEN = [
    (1, 1, 1),
    (1_999, 1, 1_999),
    (2_000, 5, 2_000),
    (2_001, 5, 2_000),
    (2_004, 5, 2_000),
    (4_999, 5, 4_995),
    (5_000, 10, 5_000),
    (5_009, 10, 5_000),
    (19_999, 10, 19_990),
    (20_000, 50, 20_000),
    (20_049, 50, 20_000),
    (49_999, 50, 49_950),
    (50_000, 100, 50_000),
    (70_123, 100, 70_100),
    (199_999, 100, 199_900),
    (200_000, 500, 200_000),
    (499_999, 500, 499_500),
    (500_000, 1_000, 500_000),
    (999_999, 1_000, 999_000),
]


class TestExistingFunctionsUnchanged:
    @pytest.mark.parametrize(("price", "tick", "rounded"), GOLDEN)
    def test_golden(self, price, tick, rounded):
        assert tick_size(price) == Decimal(tick)
        assert round_to_tick(price) == Decimal(rounded)

    def test_ticks_in_golden(self):
        assert ticks_in(500, 70_000) == Decimal("5")
        assert ticks_in(-500, 70_000) == Decimal("5")
        assert ticks_in(Decimal("2.2"), 539) == Decimal("2.2")


class TestIsOnTick:
    @pytest.mark.parametrize("price", [1, 1_999, 2_000, 2_005, 4_995, 5_000, 19_990, 20_050,
                                       49_950, 50_000, 70_100, 199_900, 200_500, 500_000,
                                       1_001_000, Decimal("70100.0")])
    def test_valid(self, price):
        assert is_on_tick(price)

    @pytest.mark.parametrize("price", [0, -5, Decimal("0.5"), 1999.5, 2_001, 4_999, 5_005,
                                       20_010, 49_999, 50_050, 200_100, 500_500])
    def test_invalid(self, price):
        assert not is_on_tick(price)


class TestRoundUpToTick:
    @pytest.mark.parametrize(
        ("price", "expected"),
        [(1_999, 1_999), (1999.5, 2_000), (2_001, 2_005), (4_996, 5_000), (19_991, 20_000),
         (49_951, 50_000), (70_101, 70_200), (199_901, 200_000), (499_501, 500_000),
         (500_001, 501_000), (70_100, 70_100)],
    )
    def test_values(self, price, expected):
        assert round_up_to_tick(price) == Decimal(expected)

    def test_result_is_always_on_tick_and_not_below(self):
        for price in range(1, 60_000, 7):
            up = round_up_to_tick(price)
            assert is_on_tick(up)
            assert up >= price
            assert up - price < tick_size(price)

    def test_rejects_nonpositive(self):
        with pytest.raises(ValueError):
            round_up_to_tick(0)


def _step(price: Decimal, n: int) -> Decimal:
    """Reference implementation: walk one tick at a time."""
    for _ in range(abs(n)):
        price = price + tick_size(price) if n > 0 else price - tick_size(price - 1)
    return price


class TestAddTicks:
    @pytest.mark.parametrize(
        ("price", "ticks", "expected"),
        [
            (1_999, 1, 2_000), (2_000, -1, 1_999), (2_000, 1, 2_005), (1_998, 3, 2_005),
            (4_995, 1, 5_000), (5_000, -1, 4_995), (19_990, 1, 20_000), (20_000, -1, 19_990),
            (49_950, 1, 50_000), (50_000, -1, 49_950), (49_950, 2, 50_100),
            (199_900, 1, 200_000), (200_000, -1, 199_900), (499_500, 1, 500_000),
            (500_000, -1, 499_500), (500_000, 3, 503_000), (70_100, 0, 70_100), (2, -1, 1),
        ],
    )
    def test_values(self, price, ticks, expected):
        assert add_ticks(price, ticks) == Decimal(expected)

    @pytest.mark.parametrize("edge", EDGES)
    @pytest.mark.parametrize("n", [-25, -3, -1, 1, 3, 25])
    def test_matches_stepwise_walk_around_edges(self, edge, n):
        for price in (Decimal(edge), add_ticks(edge, -2), add_ticks(edge, 2)):
            assert add_ticks(price, n) == _step(price, n)

    def test_round_trip(self):
        for price in (1, 1_999, 2_000, 4_995, 50_000, 499_500, 750_000):
            for n in (1, 10, 1_000, 5_000):
                assert add_ticks(add_ticks(price, n), -n) == Decimal(price)

    def test_rejects_off_tick(self):
        with pytest.raises(ValueError, match="round_to_tick"):
            add_ticks(70_150, 1)

    def test_rejects_going_to_zero(self):
        with pytest.raises(ValueError):
            add_ticks(1, -1)
        with pytest.raises(ValueError):
            add_ticks(5, -5)

    @pytest.mark.parametrize("bad", [1.0, "1", True])
    def test_ticks_must_be_int(self, bad):
        with pytest.raises(TypeError):
            add_ticks(70_100, bad)


class TestTicksBetween:
    @pytest.mark.parametrize(
        ("start", "end", "expected"),
        [
            (49_900, 50_100, 3), (50_100, 49_900, -3), (1_999, 2_005, 2), (2_000, 2_000, 0),
            (1, 2_000, 1_999), (2_000, 5_000, 600), (5_000, 20_000, 1_500),
            (20_000, 50_000, 600), (50_000, 200_000, 1_500), (200_000, 500_000, 600),
            (500_000, 510_000, 10),
        ],
    )
    def test_values(self, start, end, expected):
        assert ticks_between(start, end) == expected

    def test_inverse_of_add_ticks(self):
        for start in (1, 1_995, 2_000, 19_990, 49_950, 199_900, 499_500, 600_000):
            for n in (-500, -1, 0, 1, 7, 2_500):
                try:
                    end = add_ticks(start, n)
                except ValueError:
                    continue
                assert ticks_between(start, end) == n

    def test_rejects_off_tick(self):
        with pytest.raises(ValueError, match="end"):
            ticks_between(70_100, 70_150)
        with pytest.raises(ValueError, match="start"):
            ticks_between(0, 70_100)

    def test_returns_int(self):
        assert type(ticks_between(2_000, 5_000)) is int


def test_top_level_exports():
    for name in ("add_ticks", "is_on_tick", "round_up_to_tick", "ticks_between"):
        assert getattr(kiwoom_client, name) is globals()[name]
