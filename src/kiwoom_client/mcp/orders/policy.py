"""Order-safety settings for the MCP server, read from the environment.

No ``mcp`` import here: the CLI validates these before the server starts.
Every setting can only add checks on top of the live-order opt-in guard.
"""

from __future__ import annotations

import os
from collections.abc import Mapping
from dataclasses import dataclass

from kiwoom_client._env import parse_bool

#: Require a ``confirm_token`` from ``order_preview`` on the raw TR order
#: tools (``order_*``, ``credit_order_*``). Default: true on live, false on mock.
#: The high-level tools (``place_order`` ...) always require one.
REQUIRE_CONFIRM_ENV = "KIWOOM_MCP_REQUIRE_CONFIRM"

#: Seconds a confirmation token stays valid.
DEFAULT_CONFIRM_TTL = 120

#: Largest amount (원, price * quantity) of one new order or change.
MAX_ORDER_AMOUNT_ENV = "KIWOOM_MCP_MAX_ORDER_AMOUNT"
#: Largest quantity (주) of one new order or change.
MAX_ORDER_QTY_ENV = "KIWOOM_MCP_MAX_ORDER_QTY"
#: Comma-separated stock codes orders may name; anything else is refused.
ALLOWED_STOCKS_ENV = "KIWOOM_MCP_ALLOWED_STOCKS"
#: Orders (new, change and cancel) this server process may send per day (KST).
DAILY_ORDER_LIMIT_ENV = "KIWOOM_MCP_DAILY_ORDER_LIMIT"


def _bool(env: Mapping[str, str], name: str, default: bool) -> bool:
    value = env.get(name, "")
    return parse_bool(value, name) if value.strip() else default


def _positive_int(env: Mapping[str, str], name: str) -> int | None:
    value = env.get(name, "").strip().replace(",", "").replace("_", "")
    if not value:
        return None
    if not value.isdigit() or int(value) <= 0:
        raise ValueError(f"{name}={env.get(name)!r} 는 양의 정수여야 합니다 (비우면 제한 없음)")
    return int(value)


def _stocks(env: Mapping[str, str], name: str) -> frozenset[str] | None:
    value = env.get(name, "")
    if not value.strip():
        return None
    codes = frozenset(c.strip().upper() for c in value.split(",") if c.strip())
    if not codes:
        raise ValueError(f"{name}={value!r} 에 종목코드가 없습니다 (비우면 제한 없음)")
    return codes


@dataclass(frozen=True)
class OrderPolicy:
    """What the order gate enforces. The defaults are the strict (live) ones."""

    require_confirm: bool = True
    confirm_ttl: int = DEFAULT_CONFIRM_TTL
    #: ``None`` = no limit (the default for every limit below).
    max_order_amount: int | None = None
    max_order_qty: int | None = None
    allowed_stocks: frozenset[str] | None = None
    daily_order_limit: int | None = None

    @classmethod
    def from_env(cls, *, is_mock: bool, env: Mapping[str, str] | None = None) -> OrderPolicy:
        """Read the ``KIWOOM_MCP_*`` order settings.

        Raises:
            ValueError: for a value that can't be parsed — the server refuses
                to start rather than guess.
        """
        source = os.environ if env is None else env
        return cls(
            require_confirm=_bool(source, REQUIRE_CONFIRM_ENV, not is_mock),
            max_order_amount=_positive_int(source, MAX_ORDER_AMOUNT_ENV),
            max_order_qty=_positive_int(source, MAX_ORDER_QTY_ENV),
            allowed_stocks=_stocks(source, ALLOWED_STOCKS_ENV),
            daily_order_limit=_positive_int(source, DAILY_ORDER_LIMIT_ENV),
        )
