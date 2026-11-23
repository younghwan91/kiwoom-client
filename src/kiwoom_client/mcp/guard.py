"""Opt-in guard for live (실전투자) order tools on the MCP server.

Applies only to the MCP tool-registration path — direct use of
``KiwoomAPI``/``AsyncKiwoomAPI`` from Python code is never gated.
"""

from __future__ import annotations

import os
from collections.abc import Mapping

from kiwoom_client._env import parse_bool

#: Set to "true" (case-insensitive) to register order/credit_order tools
#: when the server is running against a live (non-mock) account.
ENV_VAR = "KIWOOM_MCP_ALLOW_LIVE_ORDERS"

#: Set to "true" to register no order tool at all — mock trading included.
#: It can only remove tools; it never brings back what the opt-in withholds.
READ_ONLY_ENV = "KIWOOM_MCP_READ_ONLY"


def live_orders_allowed(*, is_mock: bool, env: dict[str, str] | None = None) -> bool:
    """Whether guarded (order/credit_order) tools should be registered.

    Mock trading (``is_mock=True``) is always allowed — nothing actually
    executes. Live trading requires the opt-in environment variable.
    """
    if is_mock:
        return True
    source = os.environ if env is None else env
    return source.get(ENV_VAR, "").strip().lower() == "true"


def read_only(env: Mapping[str, str] | None = None) -> bool:
    """``KIWOOM_MCP_READ_ONLY`` (unset = false).

    Raises:
        ValueError: a value that is not a recognised boolean — the server
            refuses to start rather than guess.
    """
    source = os.environ if env is None else env
    value = source.get(READ_ONLY_ENV, "")
    return parse_bool(value, READ_ONLY_ENV) if value.strip() else False


def order_tools_allowed(*, is_mock: bool, env: Mapping[str, str] | None = None) -> bool:
    """Whether to register order tools: never in read-only mode, otherwise
    exactly :func:`live_orders_allowed`."""
    if read_only(env):
        return False
    return live_orders_allowed(is_mock=is_mock, env=None if env is None else dict(env))
