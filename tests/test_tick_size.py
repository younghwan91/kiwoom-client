from decimal import Decimal

import pytest

from kiwoom_client.tick_size import round_to_tick, tick_size, ticks_in


@pytest.mark.parametrize(
    "price,expected",
    [
        (1_000, 1),
        (1_999, 1),
        (2_000, 5),
        (4_999, 5),
        (5_000, 10),
        (19_999, 10),
        (20_000, 50),
        (49_999, 50),
        (50_000, 100),
        (199_999, 100),
        (200_000, 500),
        (499_999, 500),
        (500_000, 1_000),
        (1_000_000, 1_000),
    ],
)
def test_tick_size_bands(price, expected):
    assert tick_size(price) == Decimal(expected)


def test_tick_size_rejects_nonpositive():
    with pytest.raises(ValueError):
        tick_size(0)
    with pytest.raises(ValueError):
        tick_size(-100)


@pytest.mark.parametrize(
    "price,expected",
    [
        (70_123, 70_100),
        (539, 539),
        (2_004, 2_000),
        (999_999, 999_000),
    ],
)
def test_round_to_tick(price, expected):
    assert round_to_tick(price) == Decimal(expected)


def test_ticks_in_not_rounded():
    # 539원대 1틱=1원, 폭 2.2원 -> 정확히 2.2틱 (반올림하지 않는다).
    assert ticks_in(Decimal("2.2"), 539) == Decimal("2.2")


def test_ticks_in_uses_price_band_of_the_price_arg():
    # 70,000원대 1틱=100원, 폭 500원 -> 5.0틱.
    assert ticks_in(500, 70_000) == Decimal("5.0")
