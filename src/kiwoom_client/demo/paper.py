"""The demo account: cash and holdings kept in memory, nothing else.

It starts with a fixed, made-up portfolio so the account lookups have
something to show. Fees and tax are rough assumptions for the demo, not
Kiwoom's actual schedule.
"""

from __future__ import annotations

from dataclasses import dataclass, field

#: Made-up account number; MCP responses mask all but the last 4 characters.
ACCOUNT_NO = "DEMO00000001"

#: Starting cash (KRW).
STARTING_CASH = 10_000_000

#: Commission per side and sell-side tax — rough demo assumptions.
COMMISSION_RATE = 0.00015
SELL_TAX_RATE = 0.0018

#: code → (qty, average price). Invented starting holdings.
STARTING_HOLDINGS: dict[str, tuple[int, int]] = {
    "005930": (50, 66800),
    "000660": (10, 171000),
    "035420": (15, 201000),
    "035720": (40, 41200),
    "086520": (20, 79500),
}


@dataclass
class Holding:
    qty: int
    avg_price: int
    #: Shares tied up in open sell orders.
    reserved: int = 0

    @property
    def sellable(self) -> int:
        return self.qty - self.reserved


@dataclass
class PaperAccount:
    cash: int = STARTING_CASH
    holdings: dict[str, Holding] = field(
        default_factory=lambda: {c: Holding(q, p) for c, (q, p) in STARTING_HOLDINGS.items()}
    )
    #: Cash tied up in open buy orders.
    reserved_cash: int = 0

    @property
    def orderable_cash(self) -> int:
        return max(self.cash - self.reserved_cash, 0)


def commission(amount: float) -> int:
    return int(amount * COMMISSION_RATE)


def sell_tax(amount: float) -> int:
    return int(amount * SELL_TAX_RATE)
