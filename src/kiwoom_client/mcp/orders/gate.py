"""The single checkpoint every MCP order passes right before it is sent.

Both kinds of order tool go through :meth:`OrderGate.send`:

- the raw TR tools (``order_buy_order`` ... ``credit_order_margin_cancel_order``),
  from the server's ``tools/call`` handler (and ``call_tool`` in discovery mode),
- the high-level tools of :mod:`.tools` (``place_order`` ...).

The gate only ever adds refusals. It runs after the live-order opt-in guard,
which already decided at registration whether order tools exist at all.
"""

from __future__ import annotations

from collections.abc import Awaitable, Callable, Mapping
from dataclasses import dataclass, field
from datetime import datetime, timedelta, timezone
from decimal import Decimal, InvalidOperation
from typing import Any

from kiwoom_client.mcp.orders.confirm import ConfirmTokens, normalize_params
from kiwoom_client.mcp.orders.policy import OrderPolicy

#: Tool argument carrying the token. Never forwarded to Kiwoom.
TOKEN_ARGUMENT = "confirm_token"


def with_token_argument(schema: dict[str, Any]) -> dict[str, Any]:
    """Input schema of a raw TR order tool plus the ``confirm_token`` argument."""
    properties = dict(schema.get("properties", {}))
    properties[TOKEN_ARGUMENT] = {
        "type": "string",
        "description": (
            "order_preview 가 돌려준 1회용 확인 토큰. 실전 서버는 기본으로 필수"
            "(KIWOOM_MCP_REQUIRE_CONFIRM) — 요청 필드로 전송되지 않는다"
        ),
    }
    return {**schema, "properties": properties}


class OrderRejected(ValueError):
    """The gate refused the order; nothing was sent. The message says why."""


@dataclass(frozen=True)
class OrderCall:
    """One order as it would reach Kiwoom: the TR tool and its request body."""

    tool: str
    params: Mapping[str, Any] = field(default_factory=dict)

    @property
    def body(self) -> dict[str, str]:
        return normalize_params(self.params)


def pop_token(arguments: dict[str, Any]) -> tuple[dict[str, Any], str | None]:
    """Take ``confirm_token`` out of tool arguments (top level or inside
    ``params``) so it is never sent to Kiwoom as a request field."""
    arguments = dict(arguments)
    token = arguments.pop(TOKEN_ARGUMENT, None)
    nested = arguments.get("params")
    if isinstance(nested, dict) and TOKEN_ARGUMENT in nested:
        nested = dict(nested)
        inner = nested.pop(TOKEN_ARGUMENT)
        token = token if token not in (None, "") else inner
        arguments["params"] = nested
    return arguments, None if token in (None, "") else str(token)


#: Returns a conservative unit price (원) for a stock — the upper price limit —
#: to bound a market order's amount; ``None`` when it can't be looked up.
Quote = Callable[[str], Awaitable[int | None]]

_KST = timezone(timedelta(hours=9))


@dataclass(frozen=True)
class OrderFacts:
    """What the limits look at, read from a TR call's body."""

    kind: str  # "new" | "modify" | "cancel" | "other"
    stock: str
    qty: int | None
    price: int | None


def _int(value: Any) -> int | None:
    try:
        number = Decimal(str(value).strip().replace(",", ""))
    except InvalidOperation:
        return None
    return int(number) if number == number.to_integral_value() else None


def order_facts(call: OrderCall) -> OrderFacts:
    body = call.body
    stock = body.get("stk_cd", "").strip().upper()
    if call.tool.endswith(("_buy_order", "_sell_order")):
        kind, qty, price = "new", body.get("ord_qty"), body.get("ord_uv")
    elif call.tool.endswith("_modify_order"):
        kind, qty, price = "modify", body.get("mdfy_qty"), body.get("mdfy_uv")
    elif call.tool.endswith("_cancel_order"):
        kind, qty, price = "cancel", body.get("cncl_qty"), None
    else:
        kind, qty, price = "other", None, None
    return OrderFacts(
        kind=kind,
        stock=stock,
        qty=None if qty is None else _int(qty),
        price=None if price is None else _int(price),
    )


class OrderGate:
    """Holds this server process's tokens, order policy and daily count."""

    def __init__(
        self,
        policy: OrderPolicy,
        *,
        tokens: ConfirmTokens | None = None,
        quote: Quote | None = None,
        now: Callable[[], datetime] = lambda: datetime.now(_KST),
    ) -> None:
        self.policy = policy
        self.tokens = tokens if tokens is not None else ConfirmTokens(ttl=policy.confirm_ttl)
        self._quote = quote
        self._now = now
        self._day = now().date()
        self.sent_today = 0

    def issue(self, call: OrderCall) -> dict[str, Any]:
        """Token fields to add to a preview of ``call``."""
        return {
            TOKEN_ARGUMENT: self.tokens.issue(call.tool, call.body),
            "confirm_expires_in": self.tokens.ttl,
        }

    def _roll_day(self) -> None:
        today = self._now().date()
        if today != self._day:
            self._day, self.sent_today = today, 0

    async def problems(self, call: OrderCall) -> list[str]:
        """Why ``call`` breaks the configured limits (empty = within them).

        Used both by ``order_preview`` (as errors, no token) and right before
        sending (as a refusal). Unset limits check nothing.
        """
        policy, facts = self.policy, order_facts(call)
        found: list[str] = []
        if policy.allowed_stocks is not None and facts.stock not in policy.allowed_stocks:
            found.append(
                f"종목 {facts.stock or '(없음)'} 은 허용 목록(KIWOOM_MCP_ALLOWED_STOCKS)에 없습니다"
            )
        if facts.kind in ("new", "modify"):
            if facts.qty is None:
                found.append("수량을 읽을 수 없어 한도를 검사할 수 없습니다")
            elif policy.max_order_qty is not None and facts.qty > policy.max_order_qty:
                found.append(
                    f"수량 {facts.qty:,}주가 한도 {policy.max_order_qty:,}주"
                    "(KIWOOM_MCP_MAX_ORDER_QTY)를 넘습니다"
                )
            if policy.max_order_amount is not None and facts.qty is not None:
                found += await self._amount_problems(facts, policy.max_order_amount)
        if policy.daily_order_limit is not None:
            self._roll_day()
            if self.sent_today >= policy.daily_order_limit:
                found.append(
                    f"오늘 이 서버가 보낸 주문이 한도 {policy.daily_order_limit:,}건"
                    "(KIWOOM_MCP_DAILY_ORDER_LIMIT)에 닿았습니다"
                )
        return found

    async def _amount_problems(self, facts: OrderFacts, limit: int) -> list[str]:
        assert facts.qty is not None
        price, basis = facts.price, "단가"
        if price is None:
            price = await self._quote(facts.stock) if self._quote is not None else None
            basis = "상한가"
            if price is None:
                return [
                    "시장가 주문의 금액을 상한가로 추정하지 못해 금액 한도"
                    "(KIWOOM_MCP_MAX_ORDER_AMOUNT)를 검사할 수 없습니다"
                ]
        amount = price * facts.qty
        if amount > limit:
            return [
                f"주문금액 {amount:,}원({basis} {price:,}원 x {facts.qty:,}주)이 한도 {limit:,}원"
                "(KIWOOM_MCP_MAX_ORDER_AMOUNT)을 넘습니다"
            ]
        return []

    async def send(
        self,
        call: OrderCall,
        token: str | None,
        *,
        require_token: bool,
        sender: Callable[[], Awaitable[Any]],
    ) -> Any:
        """Check ``call``; if every check passes, use up the token and send.

        Limits are checked again here (not only in the preview), then the
        token. A token that was given is always checked, even where none is
        required.

        Raises:
            OrderRejected: any check failed — ``sender`` was not called.
        """
        found = await self.problems(call)
        if found:
            raise OrderRejected("주문 거부(전송 안 함): " + "; ".join(found))
        nonce: str | None = None
        if token is not None or require_token:
            try:
                nonce = self.tokens.check(token or "", call.tool, call.body)
            except ValueError as exc:
                raise OrderRejected(f"주문 거부(전송 안 함): {exc}") from exc
        if nonce is not None:
            self.tokens.consume(nonce)
        self._roll_day()
        self.sent_today += 1  # an attempt that reaches Kiwoom counts, whatever it answers
        return await sender()

    async def send_tr(
        self,
        tool: str,
        arguments: dict[str, Any],
        dispatch: Callable[[dict[str, Any]], Awaitable[Any]],
        *,
        body_of: Callable[[dict[str, Any]], Mapping[str, Any]],
    ) -> Any:
        """Raw TR order tool: strip the token, check, then ``dispatch`` the
        remaining arguments. ``body_of`` extracts the request body."""
        clean, token = pop_token(arguments)
        call = OrderCall(tool, body_of(clean))
        return await self.send(
            call, token, require_token=self.policy.require_confirm, sender=lambda: dispatch(clean)
        )
