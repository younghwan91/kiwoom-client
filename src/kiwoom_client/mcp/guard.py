"""Opt-in guard for live (실전투자) order tools on the MCP server.

Applies only to the MCP tool-registration path — direct use of
``KiwoomAPI``/``AsyncKiwoomAPI`` from Python code is never gated.
"""

from __future__ import annotations

import os

#: Set to "true" (case-insensitive) to register order/credit_order tools
#: when the server is running against a live (non-mock) account.
ENV_VAR = "KIWOOM_MCP_ALLOW_LIVE_ORDERS"


def live_orders_allowed(*, is_mock: bool, env: dict[str, str] | None = None) -> bool:
    """Whether guarded (order/credit_order) tools should be registered.

    Mock trading (``is_mock=True``) is always allowed — nothing actually
    executes. Live trading requires the opt-in environment variable.
    """
    if is_mock:
        return True
    source = os.environ if env is None else env
    return source.get(ENV_VAR, "").strip().lower() == "true"
