"""Server-side checks ``order_preview`` runs against live data (lookups only).

``order_preview`` alone checks the shape of an order (tick size, fields). With
a connection it also asks Kiwoom what the order would run into:

- 상한가/하한가 — ka10001 주식기본정보 ``upl_pric``/``lst_pric`` (and
  ``cur_prc`` for a market order's estimate). A limit price outside the band
  is an error; within :data:`NEAR_LIMIT_PCT` of it is a warning.
- 매수 주문가능수량 — kt00011 증거금율별주문가능수량조회 at the order price:
  the quantity for the account's applied margin rate (``aplc_rt``). More than
  that is an error; more than the cash-only quantity (``min_ord_alowq``) is a
  warning (미수 발생 가능).
- 매도 가능수량 — kt00018 계좌평가잔고내역 ``trde_able_qty``. More than that is
  an error.

Errors stop the preview from issuing a confirm token. A lookup that fails or
returns nothing usable becomes a warning — the check is reported as not done,
never as passed. Every request here is a lookup; none goes to an order TR.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from decimal import Decimal
from typing import Any

import httpx

from kiwoom_client.base import KiwoomAPIError
from kiwoom_client.mcp.intents.normalize import price as to_price

#: A limit price within this many percent of 상한가/하한가 gets a warning.
NEAR_LIMIT_PCT = Decimal("2")

_NEW = frozenset({"order_buy_order", "order_sell_order"})
_MODIFY = "order_modify_order"


@dataclass
class CheckResult:
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    facts: dict[str, Any] = field(default_factory=dict)


def _int(value: Any) -> int | None:
    number = to_price(value)
    return None if number is None else int(number)


async def _quote(api: Any, stk_cd: str, out: CheckResult) -> dict[str, int | None] | None:
    try:
        resp = await api.stock_info.basic_stock_info(stk_cd=stk_cd)
    except (KiwoomAPIError, httpx.HTTPError) as exc:
        out.warnings.append(f"상·하한가 확인 실패(ka10001): {exc} — 검사하지 못했습니다")
        return None
    quote = {
        "upper_limit": _int(resp.get("upl_pric")),
        "lower_limit": _int(resp.get("lst_pric")),
        "current_price": _int(resp.get("cur_prc")),
    }
    out.facts.update({k: v for k, v in quote.items() if v is not None})
    return quote


def _price_band(price: int, quote: dict[str, int | None], out: CheckResult) -> None:
    upper, lower = quote["upper_limit"], quote["lower_limit"]
    if not upper or not lower:
        out.warnings.append("상·하한가를 응답에서 찾지 못해 가격 범위를 검사하지 못했습니다")
        return
    if price > upper:
        out.errors.append(f"단가 {price:,}원이 상한가 {upper:,}원보다 높습니다")
    elif price < lower:
        out.errors.append(f"단가 {price:,}원이 하한가 {lower:,}원보다 낮습니다")
    else:
        if Decimal(upper - price) * 100 <= Decimal(upper) * NEAR_LIMIT_PCT:
            out.warnings.append(f"단가 {price:,}원이 상한가 {upper:,}원에 가깝습니다")
        if Decimal(price - lower) * 100 <= Decimal(lower) * NEAR_LIMIT_PCT:
            out.warnings.append(f"단가 {price:,}원이 하한가 {lower:,}원에 가깝습니다")


async def _buyable(api: Any, stk_cd: str, price: int, qty: int, out: CheckResult) -> None:
    try:
        resp = await api.account.orderable_qty_by_margin(stk_cd=stk_cd, uv=str(price))
    except (KiwoomAPIError, httpx.HTTPError) as exc:
        out.warnings.append(f"주문가능수량 확인 실패(kt00011): {exc} — 검사하지 못했습니다")
        return
    rate = _int(resp.get("aplc_rt"))
    allowed = _int(resp.get(f"profa_{rate}ord_alowq")) if rate else None
    cash_only = _int(resp.get("min_ord_alowq"))
    if allowed is None:
        allowed = cash_only
    if allowed is None:
        out.warnings.append("주문가능수량을 응답에서 찾지 못해 검사하지 못했습니다(kt00011)")
        return
    out.facts["orderable_qty"] = allowed
    if cash_only is not None:
        out.facts["orderable_qty_cash_only"] = cash_only
    cash = _int(resp.get("ord_alowa"))
    if cash is not None:
        out.facts["orderable_cash"] = cash
    if qty > allowed:
        out.errors.append(f"수량 {qty:,}주가 주문가능수량 {allowed:,}주보다 많습니다")
    elif cash_only is not None and qty > cash_only:
        out.warnings.append(
            f"수량 {qty:,}주가 미수 없이 살 수 있는 {cash_only:,}주보다 많습니다 — "
            "미수가 생길 수 있습니다"
        )
    elif qty * 100 >= allowed * 90:
        out.warnings.append(f"수량 {qty:,}주가 주문가능수량 {allowed:,}주에 가깝습니다")


async def _sellable(api: Any, stk_cd: str, qty: int, exchange: str, out: CheckResult) -> None:
    try:
        resp = await api.account.evaluation_balance_detail(qry_tp="1", dmst_stex_tp=exchange)
    except (KiwoomAPIError, httpx.HTTPError) as exc:
        out.warnings.append(f"매도가능수량 확인 실패(kt00018): {exc} — 검사하지 못했습니다")
        return
    rows = [r for r in resp.get("acnt_evlt_remn_indv_tot") or [] if isinstance(r, dict)]
    held = [r for r in rows if str(r.get("stk_cd", "")).strip().lstrip("A") == stk_cd]
    if not held:
        if rows and resp.get("cont-yn") != "Y" and resp.get("cont_yn") != "Y":
            out.errors.append(f"{stk_cd} 를 보유하고 있지 않습니다(kt00018 잔고)")
        else:
            out.warnings.append(
                f"잔고 첫 페이지에 {stk_cd} 가 없어 매도가능수량을 검사하지 못했습니다"
            )
        return
    sellable = sum(_int(r.get("trde_able_qty")) or 0 for r in held)
    out.facts["sellable_qty"] = sellable
    if qty > sellable:
        out.errors.append(f"수량 {qty:,}주가 매도가능수량 {sellable:,}주보다 많습니다")


async def market_checks(api: Any, preview: dict[str, Any]) -> CheckResult:
    """Lookups for one preview (see module docstring). Cancels need none."""
    out = CheckResult()
    tool, params = preview["would_call"], preview["params"]
    if tool not in _NEW and tool != _MODIFY:
        return out
    stk_cd = params["stk_cd"]
    qty = int(params.get("ord_qty") or params.get("mdfy_qty") or 0)
    raw_price = params.get("ord_uv") or params.get("mdfy_uv") or ""
    limit_price = int(Decimal(raw_price)) if raw_price else None

    quote = await _quote(api, stk_cd, out)
    if quote is not None and limit_price is not None:
        _price_band(limit_price, quote, out)
    if tool == _MODIFY:
        return out
    if tool == "order_buy_order":
        basis = limit_price or (quote or {}).get("upper_limit") or (quote or {}).get(
            "current_price"
        )
        if basis:
            await _buyable(api, stk_cd, int(basis), qty, out)
        else:
            out.warnings.append("기준 가격을 몰라 주문가능수량을 검사하지 못했습니다")
    else:
        await _sellable(api, stk_cd, qty, params.get("dmst_stex_tp") or "KRX", out)
    return out
