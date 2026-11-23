"""One-time confirmation tokens for MCP orders.

``order_preview`` issues a token for one exact order: the TR tool it would
call and its normalised request body. The order tools accept the order only
with a token that

- was issued by this server process (HMAC over a random per-process secret —
  a model can't make one up, and a restart invalidates every token),
- matches the order's parameters exactly (after the same normalisation),
- has not expired (default 120 s), and
- has not been used before.

The parameters are not inside the token; it carries only an expiry, a nonce
and the MAC, so it reveals nothing about the order.
"""

from __future__ import annotations

import hashlib
import hmac
import json
import secrets
import time
from collections.abc import Callable, Mapping
from typing import Any

from kiwoom_client.mcp.orders.policy import DEFAULT_CONFIRM_TTL


class ConfirmError(ValueError):
    """The token does not authorise this order. The message says why."""


def normalize_params(params: Mapping[str, Any]) -> dict[str, str]:
    """Request body as the token sees it: string values, stripped, empty
    values dropped (an omitted optional field and ``""`` are the same order)."""
    normalized: dict[str, str] = {}
    for key, value in params.items():
        text = "" if value is None else str(value).strip()
        if text:
            normalized[str(key)] = text
    return normalized


def _canonical(tool: str, params: Mapping[str, Any]) -> bytes:
    body = {"tool": tool, "params": normalize_params(params)}
    return json.dumps(body, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()


class ConfirmTokens:
    """Issues and redeems tokens. One instance per server process."""

    def __init__(
        self,
        *,
        ttl: int = DEFAULT_CONFIRM_TTL,
        secret: bytes | None = None,
        clock: Callable[[], float] = time.time,
    ) -> None:
        if ttl <= 0:
            raise ValueError("ttl 은 양수여야 합니다")
        self.ttl = ttl
        self._secret = secret if secret is not None else secrets.token_bytes(32)
        self._clock = clock
        self._used: dict[str, float] = {}  # nonce -> expiry

    def _mac(self, expires: int, nonce: str, tool: str, params: Mapping[str, Any]) -> str:
        message = f"{expires}.{nonce}.".encode() + _canonical(tool, params)
        return hmac.new(self._secret, message, hashlib.sha256).hexdigest()

    def issue(self, tool: str, params: Mapping[str, Any]) -> str:
        expires = int(self._clock()) + self.ttl
        nonce = secrets.token_hex(8)
        return f"{expires}.{nonce}.{self._mac(expires, nonce, tool, params)}"

    def check(self, token: str, tool: str, params: Mapping[str, Any]) -> str:
        """Validate ``token`` for this order without using it up.

        Returns the nonce to pass to :meth:`consume`.

        Raises:
            ConfirmError: missing, malformed, for different parameters,
                expired or already used.
        """
        if not token or not isinstance(token, str):
            raise ConfirmError(
                "confirm_token 이 없습니다 — order_preview 로 미리보기를 만들어 사용자 확인을 "
                "받은 뒤, 미리보기가 돌려준 confirm_token 을 넣으세요"
            )
        parts = token.strip().split(".")
        if len(parts) != 3 or not parts[0].isdigit():
            raise ConfirmError(
                "confirm_token 형식이 올바르지 않습니다 — order_preview 를 다시 부르세요"
            )
        expires, nonce, mac = int(parts[0]), parts[1], parts[2]
        if not hmac.compare_digest(mac, self._mac(expires, nonce, tool, params)):
            raise ConfirmError(
                "confirm_token 이 이 주문과 맞지 않습니다 — 미리보기 뒤에 종목·수량·단가 등이 "
                "바뀌었거나 다른 주문(또는 재시작 전 서버)의 토큰입니다. "
                "order_preview 를 다시 부르세요"
            )
        if self._clock() > expires:
            raise ConfirmError(
                f"confirm_token 이 만료됐습니다(유효 {self.ttl}초) — order_preview 를 다시 부르세요"
            )
        self._prune()
        if nonce in self._used:
            raise ConfirmError(
                "이미 쓴 confirm_token 입니다 — 주문마다 order_preview 를 새로 부르세요"
            )
        return nonce

    def consume(self, nonce: str, expires_at: float | None = None) -> None:
        """Mark a checked token as used (call right before sending)."""
        self._used[nonce] = expires_at if expires_at is not None else self._clock() + self.ttl

    def redeem(self, token: str, tool: str, params: Mapping[str, Any]) -> None:
        """:meth:`check` then :meth:`consume`."""
        self.consume(self.check(token, tool, params))

    def _prune(self) -> None:
        now = self._clock()
        for nonce in [n for n, exp in self._used.items() if exp < now]:
            del self._used[nonce]
