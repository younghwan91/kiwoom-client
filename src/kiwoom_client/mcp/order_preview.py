"""``order_preview`` — check and summarise a stock order without sending it.

Lets an agent (and the person watching it) see exactly what an order would
look like — tick-size-corrected price, filled-in fields, estimated amount,
warnings — before anything reaches Kiwoom. It sends no order and is not an
order tool: the real ``order_*`` tools remain behind the live-order guard.
The only request it may make is a stock lookup (ka10099) when given a name.

When order tools are registered it also returns a ``confirm_token`` bound to
the exact order (:mod:`kiwoom_client.mcp.orders.confirm`); the order tools
require it (``place_order``/``modify_order``/``cancel_order`` always, the raw
TR tools per ``KIWOOM_MCP_REQUIRE_CONFIRM``).
"""

from __future__ import annotations

import re
from decimal import Decimal, InvalidOperation
from functools import lru_cache
from typing import Any

from mcp import types

from kiwoom_client import spec
from kiwoom_client.mcp.codes import (
    EXCHANGES,
    LIMIT_PRICE_TRADE_TYPES,
    NO_PRICE_TRADE_TYPES,
    TRADE_TYPES,
)
from kiwoom_client.mcp.local_tools import LocalTool
from kiwoom_client.mcp.orders.checks import market_checks
from kiwoom_client.mcp.orders.confirm import normalize_params
from kiwoom_client.mcp.orders.gate import OrderCall, OrderGate
from kiwoom_client.mcp.tools import discover_rest_tools
from kiwoom_client.tick_size import round_to_tick, tick_size

TOOL_NAME = "order_preview"

_SIDES = {"buy": ("매수", "order_buy_order"), "sell": ("매도", "order_sell_order")}
_STOCK_CODE = re.compile(r"^[0-9A-Z]{6}$")

#: ``action`` values. ``new`` (default) is a buy/sell; the others act on an
#: open order (``order_no``).
ACTIONS = ("new", "modify", "cancel")
MODIFY_TOOL = "order_modify_order"
CANCEL_TOOL = "order_cancel_order"

#: ``price`` value meaning a market order (trde_tp 3).
MARKET = "market"
_MARKET_TRADE_TYPE = "3"

INPUT_SCHEMA: dict[str, Any] = {
    "type": "object",
    "properties": {
        "action": {
            "type": "string",
            "enum": list(ACTIONS),
            "default": "new",
            "description": (
                "new=신규 매수/매도, modify=정정, cancel=취소 (modify/cancel 은 order_no 필요)"
            ),
        },
        "side": {
            "type": "string",
            "enum": list(_SIDES),
            "description": "buy=매수, sell=매도 (new 에서 필수, modify 에서는 호가단위 보정 방향)",
        },
        "stock": {"type": "string", "description": "종목명 또는 종목코드 (예: 삼성전자, 005930)"},
        "stk_cd": {"type": "string", "description": "종목코드 6자리 (stock 대신 써도 된다)"},
        "qty": {
            "type": ["integer", "string"],
            "description": "수량 (주, 양의 정수). cancel 은 'all' = 잔량 전부(기본)",
        },
        "price": {
            "type": ["number", "string"],
            "description": "단가 (원) 또는 'market'(시장가). 지정가 계열·modify 에서 필수",
        },
        "order_no": {"type": "string", "description": "원주문번호 (modify/cancel)"},
        "ord_qty": {"type": ["integer", "string"], "description": "qty 와 같음 (TR 필드명)"},
        "ord_uv": {"type": ["number", "string"], "description": "price 와 같음 (TR 필드명)"},
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
        "tool": {
            "type": "string",
            "description": (
                "TR 주문 도구 이름(예: credit_order_margin_buy_order, order_gold_spot_buy_order). "
                "주면 params 를 그대로 검사해 그 도구용 토큰을 만든다(위 필드는 무시)"
            ),
        },
        "params": {"type": "object", "description": "tool 과 함께: 그 TR 의 요청 필드"},
    },
}

DESCRIPTION = (
    "주문 미리보기 — 실제로 보내지 않는다(주문 요청 없음, 종목명이면 종목 조회만). 주문·정정·"
    "취소 전에 호출해 호가단위 보정(매수는 내림·매도는 올림), 필드 검증, 예상 주문금액, 경고를 "
    "확인하고, 결과를 사용자에게 보여 준 뒤에만 주문 도구를 쓴다. 주문 도구가 등록된 서버면 "
    "그 주문에만 쓸 수 있는 1회용 confirm_token(기본 120초)을 돌려준다 — 주문 도구에 그대로 "
    "넣는다. 종목·수량·단가가 하나라도 바뀌면 토큰이 맞지 않는다. order_tools_enabled 가 "
    "false 면 이 서버에는 주문 도구가 등록돼 있지 않다."
)


def _positive_int(value: Any, field: str) -> int:
    try:
        number = Decimal(str(value).strip().replace(",", ""))
    except InvalidOperation as exc:
        raise ValueError(f"{field} 는 숫자여야 합니다: {value!r}") from exc
    if number <= 0 or number != number.to_integral_value():
        raise ValueError(f"{field} 는 양의 정수여야 합니다: {value!r}")
    return int(number)


def _price(value: Any, field: str = "ord_uv") -> Decimal:
    try:
        price = Decimal(str(value).strip().replace(",", ""))
    except InvalidOperation as exc:
        raise ValueError(f"{field} 는 숫자여야 합니다: {value!r}") from exc
    if price <= 0:
        raise ValueError(f"{field} 는 0보다 커야 합니다: {value!r}")
    return price


def _snap(price: Decimal, side: str) -> Decimal:
    """Nearest valid tick that is never worse for the caller than ``price``:
    down for a buy (don't pay more), up for a sell (don't sell for less)."""
    down = round_to_tick(price)
    if side == "buy" or down == price:
        return down
    return down + tick_size(down)


def _first(arguments: dict[str, Any], *names: str) -> Any:
    for name in names:
        value = arguments.get(name)
        if value not in (None, ""):
            return value
    return None


def _is_market(value: Any) -> bool:
    return isinstance(value, str) and value.strip().lower() == MARKET


def _stock_code(arguments: dict[str, Any], warnings: list[str]) -> str:
    stk_cd = str(_first(arguments, "stk_cd", "stock") or "").strip().upper()
    if not stk_cd:
        raise ValueError("stk_cd(종목코드) 또는 stock(종목명·코드)이 필요합니다")
    if not _STOCK_CODE.match(stk_cd):
        warnings.append(f"종목코드 {stk_cd!r} 가 6자리 형식이 아닙니다 — 코드를 다시 확인하세요")
    return stk_cd


def _exchange(arguments: dict[str, Any], warnings: list[str]) -> str:
    exchange = str(_first(arguments, "dmst_stex_tp", "exchange") or "KRX").strip().upper()
    if exchange not in EXCHANGES:
        warnings.append(f"알 수 없는 거래소구분 dmst_stex_tp={exchange!r} (KRX/NXT/SOR)")
    return exchange


def _disabled_warning(order_tools_enabled: bool, warnings: list[str]) -> None:
    if not order_tools_enabled:
        warnings.append(
            "이 서버에는 주문 도구가 등록돼 있지 않습니다 (실전 계좌는 "
            "KIWOOM_MCP_ALLOW_LIVE_ORDERS opt-in 필요)"
        )


def preview_order(arguments: dict[str, Any], *, order_tools_enabled: bool) -> dict[str, Any]:
    """Validate and normalise one new stock order (buy/sell). Pure: no I/O.

    Accepts the TR field names (``stk_cd``/``ord_qty``/``ord_uv``) or the
    friendlier ``stock``/``qty``/``price`` (``price="market"`` = 시장가).
    ``stock`` must already be a code here — see :func:`resolve_stock`.

    Raises:
        ValueError: for input that can't form an order at all (bad side,
            quantity, price). Softer problems come back in ``warnings``.
    """
    side = str(arguments.get("side", "")).strip().lower()
    if side not in _SIDES:
        raise ValueError(f"side 는 buy 또는 sell 이어야 합니다: {arguments.get('side')!r}")
    side_label, tool_name = _SIDES[side]

    warnings: list[str] = []
    stk_cd = _stock_code(arguments, warnings)
    qty = _positive_int(_first(arguments, "ord_qty", "qty"), "ord_qty")

    raw_price = _first(arguments, "ord_uv", "price")
    market = _is_market(raw_price)
    if market:
        raw_price = None
    trde_tp = str(arguments.get("trde_tp") or (_MARKET_TRADE_TYPE if market else "0")).strip()
    trde_label = TRADE_TYPES.get(trde_tp)
    if market and trde_tp not in NO_PRICE_TRADE_TYPES:
        raise ValueError(
            f"price='market' 과 지정가 계열 trde_tp={trde_tp!r} 를 함께 쓸 수 없습니다"
        )
    if trde_label is None:
        warnings.append(f"알 수 없는 매매구분 trde_tp={trde_tp!r} — 키움 가이드에서 확인하세요")

    exchange = _exchange(arguments, warnings)

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
    _disabled_warning(order_tools_enabled, warnings)

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


def _order_no(arguments: dict[str, Any]) -> str:
    order_no = str(_first(arguments, "order_no", "orig_ord_no") or "").strip()
    if not order_no:
        raise ValueError("order_no(원주문번호)가 필요합니다")
    return order_no


def preview_modify(arguments: dict[str, Any], *, order_tools_enabled: bool) -> dict[str, Any]:
    """Validate and normalise a price/quantity change of an open order. Pure.

    The price must be on a tick. With ``side`` it is snapped like a new order
    (buy down, sell up); without it an off-tick price is an error, since the
    safe direction depends on the original order's side.
    """
    warnings: list[str] = []
    order_no = _order_no(arguments)
    stk_cd = _stock_code(arguments, warnings)
    qty = _positive_int(_first(arguments, "mdfy_qty", "qty", "ord_qty"), "qty")
    raw_price = _first(arguments, "mdfy_uv", "price", "ord_uv")
    if raw_price is None or _is_market(raw_price):
        raise ValueError(
            "modify 에는 price(정정단가, 원)가 필요합니다 — 시장가 정정은 지원하지 않습니다"
        )
    requested = _price(raw_price, "price")
    side = str(arguments.get("side", "")).strip().lower()
    if side in _SIDES:
        adjusted = _snap(requested, side)
        if adjusted != requested:
            direction = "내림" if side == "buy" else "올림"
            warnings.append(f"단가 {requested} 를 호가단위 {adjusted} 로 {direction}했습니다")
    else:
        adjusted = round_to_tick(requested)
        if adjusted != requested:
            up = adjusted + tick_size(adjusted)
            raise ValueError(
                f"정정단가 {requested} 는 호가단위가 아닙니다 — {adjusted} 또는 {up} 로 넣거나 "
                "side(buy/sell)를 주면 안전한 쪽으로 맞춥니다"
            )
    exchange = _exchange(arguments, warnings)
    params = {
        "dmst_stex_tp": exchange,
        "orig_ord_no": order_no,
        "stk_cd": stk_cd,
        "mdfy_qty": str(qty),
        "mdfy_uv": str(adjusted),
    }
    _disabled_warning(order_tools_enabled, warnings)
    return {
        "sent": False,
        "summary": f"주문 {order_no} 정정: {stk_cd} {qty:,}주 {int(adjusted):,}원 ({exchange})",
        "would_call": MODIFY_TOOL,
        "params": params,
        "price": {"requested": str(requested), "adjusted": str(adjusted),
                  "tick_size": str(tick_size(adjusted)), "changed": adjusted != requested},
        "estimated_amount": int(adjusted * qty),
        "order_tools_enabled": order_tools_enabled,
        "warnings": warnings,
    }  # fmt: skip


def preview_cancel(arguments: dict[str, Any], *, order_tools_enabled: bool) -> dict[str, Any]:
    """Validate and normalise a cancel of an open order. Pure.
    ``qty="all"`` (default) cancels the whole remaining quantity (cncl_qty 0)."""
    warnings: list[str] = []
    order_no = _order_no(arguments)
    stk_cd = _stock_code(arguments, warnings)
    raw_qty = _first(arguments, "cncl_qty", "qty", "ord_qty")
    if raw_qty is None or str(raw_qty).strip().lower() in ("all", "0"):
        cncl_qty, qty_text = "0", "잔량 전부"
    else:
        qty = _positive_int(raw_qty, "qty")
        cncl_qty, qty_text = str(qty), f"{qty:,}주"
    exchange = _exchange(arguments, warnings)
    params = {
        "dmst_stex_tp": exchange,
        "orig_ord_no": order_no,
        "stk_cd": stk_cd,
        "cncl_qty": cncl_qty,
    }
    _disabled_warning(order_tools_enabled, warnings)
    return {
        "sent": False,
        "summary": f"주문 {order_no} 취소: {stk_cd} {qty_text} ({exchange})",
        "would_call": CANCEL_TOOL,
        "params": params,
        "price": None,
        "estimated_amount": None,
        "order_tools_enabled": order_tools_enabled,
        "warnings": warnings,
    }


@lru_cache(maxsize=1)
def _guarded_tools() -> dict[str, tuple[str, str]]:
    """Raw TR order tool name -> (module, method)."""
    return {s.tool_name: (s.module_name, s.method_name) for s in discover_rest_tools() if s.guarded}


def preview_tr(arguments: dict[str, Any], *, order_tools_enabled: bool) -> dict[str, Any]:
    """Any raw TR order tool (신용·금현물 포함) with its ``params`` as given —
    checked for the catalog's required fields, not rewritten. Pure."""
    tool = str(arguments.get("tool") or "").strip()
    methods = _guarded_tools()
    if tool not in methods:
        names = ", ".join(sorted(methods))
        raise ValueError(f"tool 은 주문 TR 도구 이름이어야 합니다 ({names}): {tool!r}")
    raw = arguments.get("params") or {}
    if not isinstance(raw, dict):
        raise ValueError("params 는 객체(JSON object)여야 합니다")
    params = normalize_params(raw)
    warnings: list[str] = []
    try:
        tr = spec.for_method(*methods[tool])
    except KeyError:
        tr = None
    if tr is not None:
        missing = [f.id for f in tr.request_fields if f.required and f.id not in params]
        if missing:
            raise ValueError(f"{tool}({tr.api_id}) 필수 필드가 없습니다: {', '.join(missing)}")
    amount = None
    qty = params.get("ord_qty") or params.get("mdfy_qty")
    price = params.get("ord_uv") or params.get("mdfy_uv")
    if qty and price:
        try:
            amount = int(Decimal(price) * Decimal(qty))
        except InvalidOperation:
            warnings.append("수량·단가가 숫자가 아니어서 예상금액을 계산하지 못했습니다")
    _disabled_warning(order_tools_enabled, warnings)
    label = f"{tr.api_id} {tr.name}" if tr is not None else tool
    return {
        "sent": False,
        "summary": f"{label}: " + ", ".join(f"{k}={v}" for k, v in params.items()),
        "would_call": tool,
        "params": params,
        "price": None,
        "estimated_amount": amount,
        "order_tools_enabled": order_tools_enabled,
        "warnings": warnings,
    }


def preview_any(arguments: dict[str, Any], *, order_tools_enabled: bool) -> dict[str, Any]:
    """Dispatch on ``tool`` (raw TR mode) or ``action`` (new/modify/cancel). Pure."""
    if arguments.get("tool") not in (None, ""):
        return preview_tr(arguments, order_tools_enabled=order_tools_enabled)
    action = str(arguments.get("action") or "new").strip().lower()
    if action == "new":
        return preview_order(arguments, order_tools_enabled=order_tools_enabled)
    if action == "modify":
        return preview_modify(arguments, order_tools_enabled=order_tools_enabled)
    if action == "cancel":
        return preview_cancel(arguments, order_tools_enabled=order_tools_enabled)
    raise ValueError(f"action 은 {'/'.join(ACTIONS)} 중 하나여야 합니다: {action!r}")


async def resolve_stock(api: Any, arguments: dict[str, Any]) -> dict[str, Any]:
    """Turn ``stock`` (a name or a code) into ``stk_cd``.

    A 6-character code is used as is (no request). A name needs an exact,
    unique match (:meth:`AsyncKiwoomAPI.stock_code`, ka10099 — cached).
    """
    if arguments.get("stk_cd") not in (None, ""):
        return arguments
    stock = str(arguments.get("stock") or "").strip()
    if not stock or _STOCK_CODE.match(stock.upper()):
        return arguments
    if api is None:
        raise ValueError(
            f"종목명 {stock!r} 을 코드로 바꾸려면 서버 연결이 필요합니다 — 종목코드를 넣으세요"
        )
    try:
        code = await api.stock_code(stock)
    except LookupError as exc:
        raise ValueError(str(exc)) from exc
    return {**arguments, "stk_cd": code}


async def build_preview(
    api: Any, arguments: dict[str, Any], *, order_tools_enabled: bool, gate: OrderGate | None
) -> dict[str, Any]:
    """Resolve the stock, preview, run the live-data checks when there is a
    connection (:mod:`.orders.checks`), and attach a token when orders are
    possible and no check found an error."""
    resolved = await resolve_stock(api, arguments)
    result = preview_any(resolved, order_tools_enabled=order_tools_enabled)
    result["errors"] = []
    if api is not None:
        checks = await market_checks(api, result)
        result["errors"] = checks.errors
        result["warnings"] += checks.warnings
        if checks.facts:
            result["checks"] = checks.facts
    if gate is not None:
        result["errors"] += await gate.problems(OrderCall(result["would_call"], result["params"]))
    if result["errors"]:
        result["warnings"].append(
            "errors 가 있어 confirm_token 을 만들지 않았습니다 — 주문을 고치세요"
        )
    elif order_tools_enabled and gate is not None:
        result.update(gate.issue(OrderCall(result["would_call"], result["params"])))
    return result


def order_preview_tool(*, order_tools_enabled: bool, gate: OrderGate | None = None) -> LocalTool:
    """The ``order_preview`` MCP tool, bound to this server's guard state."""

    async def handler(api: Any, arguments: dict[str, Any]) -> dict[str, Any]:
        return await build_preview(
            api, arguments, order_tools_enabled=order_tools_enabled, gate=gate
        )

    return LocalTool(
        name=TOOL_NAME,
        title="주문 미리보기 (전송 안 함)",
        description=DESCRIPTION,
        input_schema=INPUT_SCHEMA,
        annotations=types.ToolAnnotations(
            title="주문 미리보기 (전송 안 함)",
            read_only_hint=True,
            idempotent_hint=False,
            open_world_hint=True,
        ),
        toolset="order",
        handler=handler,
    )
