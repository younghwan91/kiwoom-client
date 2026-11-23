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


class OrderGate:
    """Holds this server process's tokens and order policy."""

    def __init__(self, policy: OrderPolicy, *, tokens: ConfirmTokens | None = None) -> None:
        self.policy = policy
        self.tokens = tokens if tokens is not None else ConfirmTokens(ttl=policy.confirm_ttl)

    def issue(self, call: OrderCall) -> dict[str, Any]:
        """Token fields to add to a preview of ``call``."""
        return {
            TOKEN_ARGUMENT: self.tokens.issue(call.tool, call.body),
            "confirm_expires_in": self.tokens.ttl,
        }

    async def send(
        self,
        call: OrderCall,
        token: str | None,
        *,
        require_token: bool,
        sender: Callable[[], Awaitable[Any]],
    ) -> Any:
        """Check ``call``; if every check passes, use up the token and send.

        A token that was given is always checked, even where none is required.

        Raises:
            OrderRejected: any check failed — ``sender`` was not called.
        """
        nonce: str | None = None
        if token is not None or require_token:
            try:
                nonce = self.tokens.check(token or "", call.tool, call.body)
            except ValueError as exc:
                raise OrderRejected(f"주문 거부(전송 안 함): {exc}") from exc
        if nonce is not None:
            self.tokens.consume(nonce)
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
