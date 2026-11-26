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


#: trde_tp codes that execute at the current price (market and best-price kinds).
MARKETABLE_TYPES = frozenset({"3", "13", "23", "6", "16", "26", "7", "29", "30", "31"})
#: trde_tp codes whose unfilled remainder is cancelled at once (IOC / FOK).
IMMEDIATE_TYPES = frozenset({"10", "13", "16", "20", "23", "26", "30", "31"})
#: trde_tp codes the demo accepts (regular session kinds; no stop/after-hours).
SUPPORTED_TYPES = frozenset({"0", *MARKETABLE_TYPES, *IMMEDIATE_TYPES})

TRADE_TYPE_NAMES = {"0": "보통", "3": "시장가", "6": "최유리지정가", "7": "최우선지정가"}


class OrderRefused(Exception):
    """The paper account refuses the order (Kiwoom would answer return_code != 0)."""


@dataclass
class PaperOrder:
    """One order (new, modify or cancel) of the paper account."""

    no: str
    code: str
    side: str  # "buy" | "sell"
    qty: int
    price: int  # limit price; for a marketable order the price it executed at
    trade_type: str
    time: str  # HHMMSS
    date: str  # YYYYMMDD
    kind: str = "new"  # "new" | "modify" | "cancel"
    orig_no: str = "0000000"
    exchange: str = "KRX"
    filled_qty: int = 0
    filled_price: int = 0
    open_qty: int = 0
    fee: int = 0
    tax: int = 0
    #: Cash (buy) reserved for the open quantity, so cancel can release it exactly.
    reserved_cash: int = 0

    @property
    def label(self) -> str:
        """주문구분 as Kiwoom shows it: ``+매수``, ``-매도정정``, ``매수취소`` ..."""
        side = "매수" if self.side == "buy" else "매도"
        if self.kind == "cancel":
            return f"{side}취소"
        sign = "+" if self.side == "buy" else "-"
        return f"{sign}{side}{'정정' if self.kind == 'modify' else ''}"

    @property
    def status(self) -> str:
        if self.kind == "cancel":
            return "확인"
        if self.open_qty > 0:
            return "접수"
        return "체결" if self.filled_qty else "확인"


@dataclass
class Fill:
    qty: int
    price: int


def _book(account: PaperAccount, order: PaperOrder, fill: Fill) -> None:
    """Apply a fill to cash and holdings."""
    amount = fill.qty * fill.price
    fee = commission(amount)
    if order.side == "buy":
        account.cash -= amount + fee
        holding = account.holdings.get(order.code)
        if holding is None:
            account.holdings[order.code] = Holding(fill.qty, fill.price)
        else:
            total = holding.qty * holding.avg_price + amount
            holding.qty += fill.qty
            holding.avg_price = round(total / holding.qty)
    else:
        tax = sell_tax(amount)
        account.cash += amount - fee - tax
        order.tax += tax
        holding = account.holdings[order.code]
        holding.qty -= fill.qty
        if holding.qty <= 0:
            del account.holdings[order.code]
    total_filled = order.filled_qty + fill.qty
    order.filled_price = round((order.filled_qty * order.filled_price + amount) / total_filled)
    order.filled_qty = total_filled
    order.fee += fee


class PaperBook:
    """Order matching for :class:`PaperAccount` against a static current price.

    A marketable order (market/best-price kinds, or a limit at or through the
    current price) fills in full at the current price. Any other limit order
    stays open — prices in the demo don't move, so it fills only if it is
    modified to a marketable price. Open orders reserve cash or shares.
    """

    def __init__(self, account: PaperAccount) -> None:
        self.account = account
        self.orders: list[PaperOrder] = []
        self._next_no = 1

    def _number(self) -> str:
        number = f"{self._next_no:07d}"
        self._next_no += 1
        return number

    def find(self, number: str) -> PaperOrder | None:
        wanted = number.strip().lstrip("0")
        return next((o for o in self.orders if o.no.lstrip("0") == wanted), None)

    def place(
        self,
        *,
        side: str,
        code: str,
        qty: int,
        price: int | None,
        trade_type: str,
        current: int,
        stamp: tuple[str, str],
        exchange: str = "KRX",
        kind: str = "new",
        orig_no: str = "0000000",
    ) -> PaperOrder:
        """Accept an order and match it. ``price`` is None for market kinds."""
        if trade_type not in SUPPORTED_TYPES:
            raise OrderRefused(
                f"데모 모드에서 지원하지 않는 매매구분입니다: trde_tp={trade_type!r}"
            )
        if qty <= 0:
            raise OrderRefused("주문수량을 확인하세요 (1주 이상)")
        marketable = trade_type in MARKETABLE_TYPES
        limit = current if marketable or price is None else price
        crosses = marketable or (limit >= current if side == "buy" else limit <= current)
        exec_price = current if crosses else limit
        if side == "buy":
            need = qty * exec_price + commission(qty * exec_price)
            if need > self.account.orderable_cash:
                raise OrderRefused(
                    f"주문가능금액이 부족합니다 (필요 {need:,}원, "
                    f"주문가능 {self.account.orderable_cash:,}원)"
                )
        else:
            holding = self.account.holdings.get(code)
            sellable = holding.sellable if holding else 0
            if qty > sellable:
                raise OrderRefused(
                    f"매도가능수량이 부족합니다 (주문 {qty}주, 매도가능 {sellable}주)"
                )
        day, time = stamp
        order = PaperOrder(
            no=self._number(), code=code, side=side, qty=qty, price=limit,
            trade_type=trade_type, time=time, date=day, kind=kind, orig_no=orig_no,
            exchange=exchange,
        )  # fmt: skip
        self.orders.append(order)
        if crosses:
            _book(self.account, order, Fill(qty, current))
        elif trade_type not in IMMEDIATE_TYPES:
            order.open_qty = qty
            self._reserve(order)
        return order

    def _reserve(self, order: PaperOrder) -> None:
        if order.side == "buy":
            amount = order.open_qty * order.price
            order.reserved_cash = amount + commission(amount)
            self.account.reserved_cash += order.reserved_cash
        else:
            self.account.holdings[order.code].reserved += order.open_qty

    def _release(self, order: PaperOrder, qty: int) -> None:
        """Take ``qty`` off an open order and free what it reserved."""
        if order.side == "buy":
            share = round(order.reserved_cash * qty / order.open_qty)
            order.reserved_cash -= share
            self.account.reserved_cash -= share
        else:
            holding = self.account.holdings.get(order.code)
            if holding is not None:
                holding.reserved -= qty
        order.open_qty -= qty

    def _open(self, number: str, code: str) -> PaperOrder:
        order = self.find(number)
        if order is None or order.kind == "cancel":
            raise OrderRefused(f"원주문번호를 찾을 수 없습니다: {number!r}")
        if order.code != code:
            raise OrderRefused(f"원주문의 종목({order.code})과 다릅니다: {code}")
        if order.open_qty <= 0:
            raise OrderRefused(f"정정·취소할 미체결 수량이 없습니다 (주문번호 {order.no})")
        return order

    def modify(
        self, number: str, code: str, qty: int, price: int, current: int, stamp: tuple[str, str]
    ) -> PaperOrder:
        original = self._open(number, code)
        qty = qty or original.open_qty
        if qty > original.open_qty:
            raise OrderRefused(f"정정수량이 미체결수량({original.open_qty}주)보다 많습니다")
        self._release(original, qty)
        try:
            return self.place(
                side=original.side, code=code, qty=qty, price=price, trade_type="0",
                current=current, stamp=stamp, exchange=original.exchange, kind="modify",
                orig_no=original.no,
            )  # fmt: skip
        except OrderRefused:
            original.open_qty += qty
            self._reserve_more(original, qty)
            raise

    def _reserve_more(self, order: PaperOrder, qty: int) -> None:
        if order.side == "buy":
            amount = qty * order.price
            extra = amount + commission(amount)
            order.reserved_cash += extra
            self.account.reserved_cash += extra
        else:
            self.account.holdings[order.code].reserved += qty

    def cancel(self, number: str, code: str, qty: int, stamp: tuple[str, str]) -> PaperOrder:
        original = self._open(number, code)
        qty = qty or original.open_qty  # 0 = the whole remainder
        if qty > original.open_qty:
            raise OrderRefused(f"취소수량이 미체결수량({original.open_qty}주)보다 많습니다")
        self._release(original, qty)
        day, time = stamp
        order = PaperOrder(
            no=self._number(), code=code, side=original.side, qty=qty, price=original.price,
            trade_type=original.trade_type, time=time, date=day, kind="cancel",
            orig_no=original.no, exchange=original.exchange,
        )  # fmt: skip
        self.orders.append(order)
        return order
