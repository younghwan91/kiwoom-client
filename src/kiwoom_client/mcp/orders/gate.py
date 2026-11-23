"""The single checkpoint every MCP order passes right before it is sent.

Both kinds of order tool go through :meth:`OrderGate.send`:

- the raw TR tools (``order_buy_order`` ... ``credit_order_margin_cancel_order``),
  from the server's ``tools/call`` handler (and ``call_tool`` in discovery mode),
- the high-level tools of :mod:`.tools` (``place_order`` ...).

The gate only ever adds refusals. It runs after the live-order opt-in guard,
which already decided at registration whether order tools exist at all.
"""

from __future__ import annotations

import time
from collections.abc import Awaitable, Callable, Mapping
from dataclasses import dataclass, field
from datetime import datetime, timedelta, timezone
from decimal import Decimal, InvalidOperation
from typing import Any

from kiwoom_client.mcp.orders.audit import AuditLog, summarize_response
from kiwoom_client.mcp.orders.confirm import ConfirmTokens, canonical, normalize_params
from kiwoom_client.mcp.orders.fields import unknown_fields
from kiwoom_client.mcp.orders.policy import OrderPolicy

#: Tool argument carrying the token. Never forwarded to Kiwoom.
TOKEN_ARGUMENT = "confirm_token"


def with_token_argument(schema: dict[str, Any]) -> dict[str, Any]:
    """Input schema of a raw TR order tool plus the ``confirm_token`` argument.

    ``params`` is closed (``additionalProperties: false``): the gate refuses
    any field the TR catalog doesn't list, and the schema says so up front.
    """
    properties = dict(schema.get("properties", {}))
    params = properties.get("params")
    if isinstance(params, dict) and params.get("properties"):
        properties["params"] = {
            **params,
            "additionalProperties": False,
            "description": (params.get("description", "") + " — 목록에 없는 필드는 거부").strip(),
        }
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
        monotonic: Callable[[], float] = time.monotonic,
        audit: AuditLog | None = None,
    ) -> None:
        self.policy = policy
        if audit is None and policy.audit_log is not None:
            audit = AuditLog(policy.audit_log)
        self.audit = audit
        self.tokens = tokens if tokens is not None else ConfirmTokens(ttl=policy.confirm_ttl)
        self._quote = quote
        self._now = now
        self._day = now().date()
        self.sent_today = 0
        self._monotonic = monotonic
        self._recent: dict[bytes, float] = {}  # canonical order -> when it was sent

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
        """Why ``call`` can't be sent: request fields the TR doesn't accept,
        or a configured limit (empty = fine).

        Used both by ``order_preview`` (as errors, no token) and right before
        sending (as a refusal). Unset limits check nothing.
        """
        policy, facts = self.policy, order_facts(call)
        found: list[str] = []
        # Raw keys, not the normalised body: an unknown key with an empty value
        # would still be sent.
        unknown = unknown_fields(call.tool, call.params)
        if unknown is None:
            found.append(f"{call.tool} 는 TR 카탈로그에 요청 필드가 없는 주문 도구입니다")
        elif unknown:
            found.append(
                f"{call.tool} 가 받지 않는 필드가 있습니다: {', '.join(unknown)} — "
                "TR 카탈로그의 요청 필드만 보낼 수 있습니다(입력 스키마 참고)"
            )
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

    def duplicate_of_recent(self, call: OrderCall) -> float | None:
        """Seconds since the exact same order was sent, if within the window."""
        window = self.policy.duplicate_window
        if window <= 0:
            return None
        now = self._monotonic()
        for key in [k for k, t in self._recent.items() if now - t >= window]:
            del self._recent[key]
        sent = self._recent.get(canonical(call.tool, call.body))
        return None if sent is None else now - sent

    def _duplicate_problem(self, call: OrderCall) -> str | None:
        ago = self.duplicate_of_recent(call)
        if ago is None:
            return None
        return (
            f"같은 주문을 {ago:.0f}초 전에 보냈습니다 — 중복으로 보고 거부합니다"
            f"({self.policy.duplicate_window}초 안 재전송, KIWOOM_MCP_DUPLICATE_WINDOW). "
            "정말 한 번 더 보내려면 잠시 뒤 다시 시도하세요"
        )

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
        via: str | None = None,
    ) -> Any:
        """Check ``call``; if every check passes, use up the token and send.
        ``via`` is the tool the agent called (for the audit log).

        Limits are checked again here (not only in the preview), then the
        token. A token that was given is always checked, even where none is
        required.

        Raises:
            OrderRejected: any check failed — ``sender`` was not called.
        """
        found = await self.problems(call)
        duplicate = self._duplicate_problem(call)
        if duplicate:
            found.append(duplicate)
        if not found and (token is not None or require_token):
            try:
                nonce: str | None = self.tokens.check(token or "", call.tool, call.body)
            except ValueError as exc:
                found.append(str(exc))
        else:
            nonce = None
        if found:
            self._audit("rejected", call, via, reasons=found, token_given=token is not None)
            raise OrderRejected("주문 거부(전송 안 함): " + "; ".join(found))
        if nonce is not None:
            self.tokens.consume(nonce)
        self._roll_day()
        self.sent_today += 1  # an attempt that reaches Kiwoom counts, whatever it answers
        self._recent[canonical(call.tool, call.body)] = self._monotonic()
        try:
            response = await sender()
        except Exception as exc:
            self._audit("failed", call, via, error=f"{type(exc).__name__}: {exc}")
            raise
        self._audit("sent", call, via, result=summarize_response(response))
        return response

    def _audit(self, event: str, call: OrderCall, via: str | None, **fields: Any) -> None:
        if self.audit is not None:
            self.audit.record(event, via=via or call.tool, tool=call.tool,
                              params=dict(call.params), **fields)  # fmt: skip

    def audit_preview(self, preview: Mapping[str, Any]) -> None:
        """Log one ``order_preview`` result (never its token)."""
        if self.audit is None:
            return
        self.audit.record(
            "preview",
            via="order_preview",
            tool=preview.get("would_call"),
            params=preview.get("params"),
            errors=preview.get("errors") or None,
            warnings=len(preview.get("warnings") or []),
            token_issued=TOKEN_ARGUMENT in preview,
        )

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
            call,
            token,
            require_token=self.policy.require_confirm,
            sender=lambda: dispatch(clean),
            via=tool,
        )
