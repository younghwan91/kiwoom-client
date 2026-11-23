"""High-level order tools: ``place_order``, ``modify_order``, ``cancel_order``.

Each takes friendly arguments (stock name or code, ``qty``, ``price`` or
``"market"``), builds exactly the TR call ``order_preview`` showed, and sends
it through the :class:`~kiwoom_client.mcp.orders.gate.OrderGate` — always with
a ``confirm_token`` required, whatever ``KIWOOM_MCP_REQUIRE_CONFIRM`` says.

They are order tools: the server registers them only where the live-order
opt-in guard registers the raw ``order_*`` tools.
"""

from __future__ import annotations

from typing import Any

from mcp import types

from kiwoom_client.mcp.local_tools import LocalTool
from kiwoom_client.mcp.order_preview import EXCHANGES, preview_any, resolve_stock
from kiwoom_client.mcp.orders.gate import (
    TOKEN_ARGUMENT,
    OrderCall,
    OrderGate,
    OrderRejected,
    pop_token,
)

PLACE_ORDER = "place_order"
MODIFY_ORDER = "modify_order"
CANCEL_ORDER = "cancel_order"
TOOL_NAMES = frozenset({PLACE_ORDER, MODIFY_ORDER, CANCEL_ORDER})

#: TR tool name -> (module, method) on AsyncKiwoomAPI.
_TR_METHODS = {
    "order_buy_order": ("order", "buy_order"),
    "order_sell_order": ("order", "sell_order"),
    "order_modify_order": ("order", "modify_order"),
    "order_cancel_order": ("order", "cancel_order"),
}

_WARNING = (
    " ⚠️ 실계좌 서버라면 실제로 체결되는 되돌릴 수 없는 주문이다. 먼저 order_preview 를 같은 "
    "인자로 불러 사용자에게 보여 주고 확인을 받은 뒤, 그 confirm_token 을 넣는다. 토큰이 없거나 "
    "인자가 바뀌었거나 만료·재사용이면 서버가 거부한다(전송 안 함)."
)

_TOKEN = {"type": "string", "description": "order_preview 가 돌려준 confirm_token (1회용)"}
_STOCK = {"type": "string", "description": "종목명 또는 종목코드 (예: 삼성전자, 005930)"}
_EXCHANGE = {"type": "string", "enum": list(EXCHANGES), "default": "KRX"}
_ORDER_NO = {"type": "string", "description": "원주문번호 (미체결 조회의 ord_no)"}

_SCHEMAS: dict[str, dict[str, Any]] = {
    PLACE_ORDER: {
        "type": "object",
        "properties": {
            "stock": _STOCK,
            "side": {"type": "string", "enum": ["buy", "sell"]},
            "qty": {"type": ["integer", "string"], "description": "수량 (주)"},
            "price": {
                "type": ["number", "string"],
                "description": "지정가 단가(원) 또는 'market'(시장가)",
            },
            "dmst_stex_tp": _EXCHANGE,
            TOKEN_ARGUMENT: _TOKEN,
        },
        "additionalProperties": False,
        "required": ["stock", "side", "qty", "price", TOKEN_ARGUMENT],
    },
    MODIFY_ORDER: {
        "type": "object",
        "properties": {
            "order_no": _ORDER_NO,
            "stock": _STOCK,
            "qty": {"type": ["integer", "string"], "description": "정정 수량 (주)"},
            "price": {"type": ["number", "string"], "description": "정정 단가 (원, 호가단위)"},
            "side": {
                "type": "string",
                "enum": ["buy", "sell"],
                "description": "원주문 방향 — 주면 단가를 안전한 쪽 호가로 맞춘다",
            },
            "dmst_stex_tp": _EXCHANGE,
            TOKEN_ARGUMENT: _TOKEN,
        },
        "additionalProperties": False,
        "required": ["order_no", "stock", "qty", "price", TOKEN_ARGUMENT],
    },
    CANCEL_ORDER: {
        "type": "object",
        "properties": {
            "order_no": _ORDER_NO,
            "stock": _STOCK,
            "qty": {
                "type": ["integer", "string"],
                "default": "all",
                "description": "취소 수량 (주) 또는 'all'(잔량 전부)",
            },
            "dmst_stex_tp": _EXCHANGE,
            TOKEN_ARGUMENT: _TOKEN,
        },
        "additionalProperties": False,
        "required": ["order_no", "stock", TOKEN_ARGUMENT],
    },
}

_ACTIONS = {PLACE_ORDER: "new", MODIFY_ORDER: "modify", CANCEL_ORDER: "cancel"}

_DESCRIPTIONS = {
    PLACE_ORDER: "주식 신규 주문(매수/매도) — 종목명·수량·단가(또는 'market')만으로." + _WARNING,
    MODIFY_ORDER: "미체결 주문의 수량·단가 정정." + _WARNING,
    CANCEL_ORDER: "미체결 주문 취소 (qty='all' 이면 잔량 전부)." + _WARNING,
}

_TITLES = {
    PLACE_ORDER: "[주문] 주식 주문 (확인 토큰 필요)",
    MODIFY_ORDER: "[주문] 주문 정정 (확인 토큰 필요)",
    CANCEL_ORDER: "[주문] 주문 취소 (확인 토큰 필요)",
}


async def build_call(api: Any, tool: str, arguments: dict[str, Any]) -> OrderCall:
    """The TR call a high-level tool would make — the same one
    ``order_preview`` previews for the same arguments."""
    resolved = await resolve_stock(api, {**arguments, "action": _ACTIONS[tool]})
    preview = preview_any(resolved, order_tools_enabled=True)
    return OrderCall(preview["would_call"], preview["params"])


def order_tools(gate: OrderGate) -> list[LocalTool]:
    """The three high-level order tools, bound to ``gate``."""

    def make(tool: str) -> LocalTool:
        allowed = frozenset(_SCHEMAS[tool]["properties"])

        async def handler(api: Any, arguments: dict[str, Any]) -> dict[str, Any]:
            # The preview logic also reads TR field names (trde_tp, ord_uv ...);
            # here only the schema's own arguments may shape the order.
            unknown = sorted(set(arguments) - allowed)
            if unknown:
                raise OrderRejected(
                    f"주문 거부(전송 안 함): {tool} 가 받지 않는 인자입니다: {', '.join(unknown)}"
                )
            clean, token = pop_token(arguments)
            call = await build_call(api, tool, clean)
            module, method = _TR_METHODS[call.tool]

            async def sender() -> Any:
                return await getattr(getattr(api, module), method)(**call.params)

            response = await gate.send(call, token, require_token=True, sender=sender, via=tool)
            params = dict(call.params)
            return {"sent": True, "tool": call.tool, "params": params, "response": response}

        return LocalTool(
            name=tool,
            title=_TITLES[tool],
            description=_DESCRIPTIONS[tool],
            input_schema=_SCHEMAS[tool],
            annotations=types.ToolAnnotations(
                title=_TITLES[tool],
                read_only_hint=False,
                destructive_hint=True,
                idempotent_hint=False,
                open_world_hint=True,
            ),
            toolset="order",
            handler=handler,
        )

    return [make(PLACE_ORDER), make(MODIFY_ORDER), make(CANCEL_ORDER)]
