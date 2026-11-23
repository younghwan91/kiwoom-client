"""``rebalance_plan`` — buy/sell quantities to reach target weights. Sends nothing.

The network part reads the portfolio (:mod:`.portfolio`) and fresh prices
(:func:`.quotes.fetch_quotes`); :func:`plan_rebalance` does the rest as a
pure function: whole shares, KRX tick-valid limit prices (buy rounded down,
sell rounded up — the same direction as ``order_preview``), sells first,
and buys trimmed so the plan never spends more cash than it frees.

Every order row carries ``order_preview_args`` for ``order_preview``; the
agent shows the plan, the person confirms, and only then do order tools run.
"""

from __future__ import annotations

import math
from dataclasses import dataclass, field
from decimal import Decimal
from typing import Any

from kiwoom_client.mcp.intents.portfolio import fetch_portfolio
from kiwoom_client.mcp.intents.quotes import MAX_STOCKS, fetch_quotes
from kiwoom_client.mcp.intents.registry import IntentContext, read_only_tool, register
from kiwoom_client.mcp.intents.resolve import resolve_stock
from kiwoom_client.mcp.local_tools import LocalTool
from kiwoom_client.tick_size import is_on_tick, round_to_tick, round_up_to_tick

#: Target keys that mean "keep this share in cash" rather than a stock.
CASH_KEYS = frozenset({"cash", "현금", "krw"})

NOTE = (
    "주문은 보내지 않았다. 각 행의 order_preview_args 를 order_preview 에 넘겨 미리보기와 "
    "확인 토큰을 받고, 사용자 확인 뒤에만 주문 도구를 쓴다. 매도를 먼저 체결한 뒤 매수한다."
)


@dataclass(frozen=True)
class Position:
    code: str
    name: str | None
    qty: int
    sellable_qty: int
    price: float


@dataclass
class Plan:
    orders: list[dict[str, Any]] = field(default_factory=list)
    holds: list[dict[str, Any]] = field(default_factory=list)
    basis: dict[str, Any] = field(default_factory=dict)
    summary: dict[str, Any] = field(default_factory=dict)
    warnings: list[str] = field(default_factory=list)


def normalize_weights(raw: dict[str, Any]) -> tuple[dict[str, float], float]:
    """``{stock: weight}`` → fractions, plus the cash share named explicitly.

    Weights may be fractions (0.3) or percents (30); if any weight is above
    1 they are all read as percents. The stock and cash weights may not add
    up to more than 100%.

    Raises:
        ValueError: negative, non-numeric or over-100% weights, or no stocks.
    """
    if not isinstance(raw, dict) or not raw:
        raise ValueError('targets 는 {"종목": 비중} 형태여야 합니다 (예: {"삼성전자": 0.5})')
    values: dict[str, float] = {}
    for key, value in raw.items():
        try:
            weight = float(str(value).strip().rstrip("%"))
        except ValueError as exc:
            raise ValueError(f"비중은 숫자여야 합니다: {key}={value!r}") from exc
        if weight < 0 or math.isnan(weight):
            raise ValueError(f"비중은 0 이상이어야 합니다: {key}={value!r}")
        values[str(key).strip()] = weight
    scale = 100.0 if any(v > 1 for v in values.values()) else 1.0
    fractions = {k: v / scale for k, v in values.items()}
    cash = sum(v for k, v in fractions.items() if k.casefold() in CASH_KEYS)
    stocks = {k: v for k, v in fractions.items() if k.casefold() not in CASH_KEYS}
    if not stocks:
        raise ValueError("targets 에 종목이 하나도 없습니다")
    if sum(stocks.values()) + cash > 1 + 1e-9:
        total = (sum(stocks.values()) + cash) * 100
        raise ValueError(f"비중 합계가 100% 를 넘습니다 ({total:.2f}%)")
    return stocks, cash


def _limit_price(price: float, side: str) -> int:
    value = Decimal(str(price))
    if is_on_tick(value):
        return int(value)
    return int(round_to_tick(value) if side == "buy" else round_up_to_tick(value))


def _pct(part: float, whole: float) -> float:
    return round(part / whole * 100, 2) if whole > 0 else 0.0


def plan_rebalance(
    positions: list[Position],
    cash: float,
    targets: dict[str, float],
    prices: dict[str, float],
    names: dict[str, str | None] | None = None,
    *,
    cash_buffer: float = 0,
    sell_unlisted: bool = False,
    exchange: str = "KRX",
) -> Plan:
    """Quantities to trade so each target stock ends near its weight. Pure.

    ``targets`` maps codes to fractions of the *investable* amount: the value
    of the positions being rebalanced plus ``cash`` minus ``cash_buffer``.
    Positions not in ``targets`` are left alone (and excluded from that
    amount) unless ``sell_unlisted``, which targets them at 0.

    Raises:
        ValueError: nothing investable, or a target without a price.
    """
    names = dict(names or {})
    held = {p.code: p for p in positions if p.qty > 0}
    included = {c: p for c, p in held.items() if c in targets or sell_unlisted}
    untouched = {c: p for c, p in held.items() if c not in included}
    price_of = {c: p.price for c, p in held.items()}
    price_of.update({c: v for c, v in prices.items() if v})
    missing = [c for c in targets if not price_of.get(c)]
    if missing:
        raise ValueError(f"현재가를 알 수 없는 종목: {', '.join(missing)}")

    included_value = sum(p.qty * price_of[c] for c, p in included.items())
    investable = included_value + cash - cash_buffer
    if investable <= 0:
        raise ValueError("리밸런싱할 금액이 없습니다 (보유 평가금액 + 현금 - cash_buffer ≤ 0)")

    plan = Plan()
    plan.basis = {
        "investable": round(investable),
        "rebalanced_stock_value": round(included_value),
        "cash": round(cash),
        "cash_buffer": round(cash_buffer),
        "untouched_value": round(sum(p.qty * price_of[c] for c, p in untouched.items())),
        "untouched": sorted(untouched),
        "sell_unlisted": sell_unlisted,
        "exchange": exchange,
    }

    sells: list[dict[str, Any]] = []
    buys: list[dict[str, Any]] = []
    for code in list(dict.fromkeys([*targets, *included])):
        position = held.get(code)
        current_qty = position.qty if position else 0
        weight = targets.get(code, 0.0)
        side_price = price_of[code]
        target_qty = math.floor(weight * investable / side_price)
        row: dict[str, Any] = {
            "code": code,
            "name": names.get(code) or (position.name if position else None),
            "current_qty": current_qty,
            "target_qty": target_qty,
            "current_weight_pct": _pct(current_qty * side_price, investable),
            "target_weight_pct": round(weight * 100, 2),
        }
        delta = target_qty - current_qty
        if delta < 0:
            qty = -delta
            sellable = position.sellable_qty if position else 0
            if qty > sellable:
                plan.warnings.append(
                    f"{code}: 매도할 {qty}주 중 매도가능 {sellable}주만 계획에 넣었습니다"
                )
                qty = sellable
            if qty == 0:
                plan.holds.append(row)
                continue
            row.update(action="sell", qty=qty, price=_limit_price(side_price, "sell"))
            sells.append(row)
        elif delta > 0:
            row.update(action="buy", qty=delta, price=_limit_price(side_price, "buy"))
            buys.append(row)
        else:
            plan.holds.append(row)

    proceeds = sum(r["qty"] * r["price"] for r in sells)
    budget = cash + proceeds - cash_buffer
    spend = sum(r["qty"] * r["price"] for r in buys)
    if spend > budget:
        plan.warnings.append("현금이 모자라 매수 수량을 줄였습니다 (큰 매수부터)")
        for row in sorted(buys, key=lambda r: r["qty"] * r["price"], reverse=True):
            excess = spend - budget
            if excess <= 0:
                break
            cut = min(row["qty"], math.ceil(excess / row["price"]))
            row["qty"] -= cut
            spend -= cut * row["price"]
        buys = [r for r in buys if r["qty"] > 0]

    for row in sells + buys:
        row["amount"] = row["qty"] * row["price"]
        after_qty = row["current_qty"] + (row["qty"] if row["action"] == "buy" else -row["qty"])
        row["after_weight_pct"] = _pct(after_qty * price_of[row["code"]], investable)
        row["order_preview_args"] = {
            "action": "new",
            "side": row["action"],
            "stock": row["code"],
            "qty": row["qty"],
            "price": row["price"],
            "trde_tp": "0",
            "dmst_stex_tp": exchange,
        }
    plan.orders = sells + buys
    plan.summary = {
        "sell_amount": proceeds,
        "buy_amount": spend,
        "cash_after_estimate": round(cash + proceeds - spend),
        "orders": len(plan.orders),
    }
    plan.warnings.append(
        "수수료·세금은 계산에 넣지 않았습니다 — 체결가도 현재가와 다를 수 있습니다"
    )
    return plan


async def rebalance_plan(
    api: Any,
    targets: Any,
    *,
    cash_buffer: Any = 0,
    sell_unlisted: bool = False,
    exchange: str = "KRX",
) -> dict[str, Any]:
    weights, _cash_weight = normalize_weights(targets)  # the rest stays cash anyway
    buffer = float(cash_buffer or 0)
    if buffer < 0:
        raise ValueError("cash_buffer 는 0 이상(원)이어야 합니다")

    codes: dict[str, float] = {}
    names: dict[str, str | None] = {}
    errors: list[str] = []
    for query, weight in weights.items():
        try:
            stock = await resolve_stock(api, query)
        except ValueError as exc:
            errors.append(str(exc))
            continue
        if stock.code in codes:
            errors.append(f"'{query}' 가 다른 목표와 같은 종목({stock.code})입니다")
            continue
        codes[stock.code] = weight
        names[stock.code] = stock.name
    if errors:
        raise ValueError("목표 종목을 확인하세요: " + " / ".join(errors))
    if len(codes) > MAX_STOCKS:
        raise ValueError(f"목표 종목은 {MAX_STOCKS}개까지입니다")

    portfolio = await fetch_portfolio(api, exchange)
    holdings = portfolio["holdings"]
    quotes = await fetch_quotes(api, list(codes))
    prices = {code: q["price"] for code, q in quotes.items() if q.get("price")}
    names.update({code: q.get("name") for code, q in quotes.items() if q.get("name")})
    positions = [
        Position(
            code=h["code"],
            name=h.get("name"),
            qty=int(h.get("qty") or 0),
            sellable_qty=int(h.get("sellable_qty") or 0),
            price=float(h.get("price") or 0),
        )
        for h in holdings
    ]
    cash = float(portfolio["totals"].get("cash_d2") or 0)
    plan = plan_rebalance(
        positions,
        cash,
        codes,
        prices,
        names,
        cash_buffer=max(buffer, 0.0),
        sell_unlisted=sell_unlisted,
        exchange=exchange,
    )
    return {
        "sent": False,
        "note": NOTE,
        "account": portfolio.get("account"),
        "basis": plan.basis,
        "summary": plan.summary,
        "orders": plan.orders,
        "holds": plan.holds,
        "warnings": plan.warnings,
    }


def _bool(value: Any) -> bool:
    if isinstance(value, str):
        return value.strip().lower() in ("true", "1", "yes", "y")
    return bool(value)


@register
def rebalance_tools(_context: IntentContext) -> list[LocalTool]:
    async def handler(api: Any, arguments: dict[str, Any]) -> dict[str, Any]:
        exchange = str(arguments.get("dmst_stex_tp") or "KRX").strip().upper()
        if exchange not in ("KRX", "NXT"):
            raise ValueError(f"dmst_stex_tp 는 KRX 또는 NXT 입니다: {exchange!r}")
        return await rebalance_plan(
            api,
            arguments.get("targets"),
            cash_buffer=arguments.get("cash_buffer", 0),
            sell_unlisted=_bool(arguments.get("sell_unlisted", False)),
            exchange=exchange,
        )

    return [
        read_only_tool(
            name="rebalance_plan",
            title="리밸런싱 계획 (주문 안 함)",
            description=(
                "목표 비중까지 종목별로 사고팔 수량을 현재 잔고·현재가로 계산한다. 정수 주식·"
                "호가단위 단가, 매도 먼저, 현금 안에서만 매수. 주문은 보내지 않고 각 행에 "
                "order_preview 로 넘길 인자를 붙인다. targets 에 없는 보유 종목은 그대로 둔다"
                "(sell_unlisted=true 면 전량 매도). '삼성전자 50%, SK하이닉스 30% 로 맞춰줘'에 "
                "쓴다."
            ),
            properties={
                "targets": {
                    "type": "object",
                    "additionalProperties": {"type": "number"},
                    "description": (
                        "종목명 또는 코드 → 비중 (0.3 또는 30). 합계 100% 이하, 나머지는 현금 "
                        "('현금' 키로 적어도 된다)"
                    ),
                },
                "cash_buffer": {
                    "type": "number",
                    "default": 0,
                    "description": "매매 뒤에도 남겨 둘 현금(원)",
                },
                "sell_unlisted": {
                    "type": "boolean",
                    "default": False,
                    "description": "targets 에 없는 보유 종목을 전량 매도 대상으로 넣는다",
                },
                "dmst_stex_tp": {"type": "string", "enum": ["KRX", "NXT"], "default": "KRX"},
            },
            required=("targets",),
            toolset="account",
            handler=handler,
            example={"targets": {"삼성전자": 0.5, "000660": 0.3}, "cash_buffer": 100000},
        )
    ]
