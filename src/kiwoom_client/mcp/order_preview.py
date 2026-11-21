"""``order_preview`` — check and summarise a stock order without sending it.

Lets an agent (and the person watching it) see exactly what an order would
look like — tick-size-corrected price, filled-in fields, estimated amount,
warnings — before anything reaches Kiwoom. It never touches the network and
is not an order tool: the real ``order_buy_order``/``order_sell_order`` tools
remain behind the live-order guard.
"""

from __future__ import annotations

import re
from decimal import Decimal, InvalidOperation
from typing import Any

from mcp import types

from kiwoom_client.mcp.codes import (
    EXCHANGES,
    LIMIT_PRICE_TRADE_TYPES,
    NO_PRICE_TRADE_TYPES,
    TRADE_TYPES,
)
from kiwoom_client.mcp.local_tools import LocalTool
from kiwoom_client.tick_size import round_to_tick, tick_size

TOOL_NAME = "order_preview"

_SIDES = {"buy": ("매수", "order_buy_order"), "sell": ("매도", "order_sell_order")}
_STOCK_CODE = re.compile(r"^[0-9A-Z]{6}$")

INPUT_SCHEMA: dict[str, Any] = {
    "type": "object",
    "properties": {
        "side": {"type": "string", "enum": list(_SIDES), "description": "buy=매수, sell=매도"},
        "stk_cd": {"type": "string", "description": "종목코드 6자리 (예: 005930)"},
        "ord_qty": {
            "type": ["integer", "string"],
            "description": "주문수량 (주, 양의 정수)",
        },
        "ord_uv": {
            "type": ["number", "string"],
            "description": "주문단가 (원). 지정가 계열에서만 — 시장가 계열은 비워 둔다",
        },
        "trde_tp": {
            "type": "string",
            "default": "0",
            "description": "매매구분 (0 보통, 3 시장가, 5 조건부지정가, 6 최유리 ...)",
        },
        "dmst_stex_tp": {
            "type": "string",
            "enum": list(EXCHANGES),
            "default": "KRX",
            "description": "국내거래소구분",
        },
    },
    "required": ["side", "stk_cd", "ord_qty"],
}

DESCRIPTION = (
    "주문 미리보기 — 실제로 보내지 않는다(네트워크 호출 없음). 주문 전에 호출해 "
    "호가단위 보정(매수는 내림·매도는 올림), 필드 검증, 예상 주문금액, 경고를 "
    "확인하고, 반환된 params 를 사용자에게 보여 준 뒤에만 실제 주문 도구를 쓴다. "
    "order_tools_enabled 가 false 면 이 서버에는 주문 도구가 등록돼 있지 않다."
)


def _positive_int(value: Any, field: str) -> int:
    try:
        number = Decimal(str(value).strip().replace(",", ""))
    except InvalidOperation as exc:
        raise ValueError(f"{field} 는 숫자여야 합니다: {value!r}") from exc
    if number <= 0 or number != number.to_integral_value():
        raise ValueError(f"{field} 는 양의 정수여야 합니다: {value!r}")
    return int(number)


def _price(value: Any) -> Decimal:
    try:
        price = Decimal(str(value).strip().replace(",", ""))
    except InvalidOperation as exc:
        raise ValueError(f"ord_uv 는 숫자여야 합니다: {value!r}") from exc
    if price <= 0:
        raise ValueError(f"ord_uv 는 0보다 커야 합니다: {value!r}")
    return price


def _snap(price: Decimal, side: str) -> Decimal:
    """Nearest valid tick that is never worse for the caller than ``price``:
    down for a buy (don't pay more), up for a sell (don't sell for less)."""
    down = round_to_tick(price)
    if side == "buy" or down == price:
        return down
    return down + tick_size(down)


def preview_order(arguments: dict[str, Any], *, order_tools_enabled: bool) -> dict[str, Any]:
    """Validate and normalise one stock order. Pure: no I/O.

    Raises:
        ValueError: for input that can't form an order at all (bad side,
            quantity, price). Softer problems come back in ``warnings``.
    """
    side = str(arguments.get("side", "")).strip().lower()
    if side not in _SIDES:
        raise ValueError(f"side 는 buy 또는 sell 이어야 합니다: {arguments.get('side')!r}")
    side_label, tool_name = _SIDES[side]

    warnings: list[str] = []
    stk_cd = str(arguments.get("stk_cd", "")).strip().upper()
    if not stk_cd:
        raise ValueError("stk_cd(종목코드)가 필요합니다")
    if not _STOCK_CODE.match(stk_cd):
        warnings.append(f"종목코드 {stk_cd!r} 가 6자리 형식이 아닙니다 — 코드를 다시 확인하세요")

    qty = _positive_int(arguments.get("ord_qty"), "ord_qty")

    trde_tp = str(arguments.get("trde_tp", "0")).strip() or "0"
    trde_label = TRADE_TYPES.get(trde_tp)
    if trde_label is None:
        warnings.append(f"알 수 없는 매매구분 trde_tp={trde_tp!r} — 키움 가이드에서 확인하세요")

    exchange = str(arguments.get("dmst_stex_tp", "KRX")).strip().upper() or "KRX"
    if exchange not in EXCHANGES:
        warnings.append(f"알 수 없는 거래소구분 dmst_stex_tp={exchange!r} (KRX/NXT/SOR)")

    raw_price = arguments.get("ord_uv")
    has_price = raw_price not in (None, "")
    price_info: dict[str, Any] | None = None
    ord_uv = ""

    if trde_tp in NO_PRICE_TRADE_TYPES:
        if has_price:
            warnings.append(f"{trde_label} 주문은 단가를 쓰지 않습니다 — ord_uv 를 비웠습니다")
    elif has_price:
        requested = _price(raw_price)
        adjusted = _snap(requested, side)
        ord_uv = str(adjusted)
        price_info = {
            "requested": str(requested),
            "adjusted": ord_uv,
            "tick_size": str(tick_size(adjusted)),
            "changed": adjusted != requested,
        }
        if adjusted != requested:
            direction = "내림" if side == "buy" else "올림"
            warnings.append(
                f"단가 {requested} 는 호가단위가 아니어서 {adjusted} 로 {direction}했습니다"
            )
    elif trde_tp in LIMIT_PRICE_TRADE_TYPES:
        raise ValueError(f"{trde_label} 주문에는 ord_uv(주문단가)가 필요합니다")

    params = {
        "dmst_stex_tp": exchange,
        "stk_cd": stk_cd,
        "ord_qty": str(qty),
        "ord_uv": ord_uv,
        "trde_tp": trde_tp,
    }
    amount = int(Decimal(ord_uv) * qty) if ord_uv else None
    price_text = f"{int(Decimal(ord_uv)):,}원" if ord_uv else "시장가격"
    summary = f"{stk_cd} {qty:,}주 {price_text} {trde_label or trde_tp} {side_label} ({exchange})"
    if not order_tools_enabled:
        warnings.append(
            "이 서버에는 주문 도구가 등록돼 있지 않습니다 (실전 계좌는 "
            "KIWOOM_MCP_ALLOW_LIVE_ORDERS opt-in 필요)"
        )

    return {
        "sent": False,
        "summary": summary,
        "would_call": tool_name,
        "params": params,
        "price": price_info,
        "estimated_amount": amount,
        "order_tools_enabled": order_tools_enabled,
        "warnings": warnings,
    }


def order_preview_tool(*, order_tools_enabled: bool) -> LocalTool:
    """The ``order_preview`` MCP tool, bound to this server's guard state."""

    async def handler(_api: Any, arguments: dict[str, Any]) -> dict[str, Any]:
        return preview_order(arguments, order_tools_enabled=order_tools_enabled)

    return LocalTool(
        name=TOOL_NAME,
        title="주문 미리보기 (전송 안 함)",
        description=DESCRIPTION,
        input_schema=INPUT_SCHEMA,
        annotations=types.ToolAnnotations(
            title="주문 미리보기 (전송 안 함)",
            read_only_hint=True,
            idempotent_hint=True,
            open_world_hint=False,
        ),
        toolset="order",
        handler=handler,
    )
