"""Intent tools: one call per thing a person asks, no api_id or field names needed.

Importing this package registers every intent module with
:mod:`.registry`; :func:`intent_tools` returns the finished tool list.
Add a new intent module by decorating its factory with
:func:`~kiwoom_client.mcp.intents.registry.register` and importing it below.
"""

from __future__ import annotations

from typing import Any

from kiwoom_client.mcp.intents import (  # noqa: F401  (registers tools)
    chart,
    conditions,
    flow,
    lookup,
    movers,
    orders,
    portfolio,
    quotes,
    rebalance,
    watch,
)
from kiwoom_client.mcp.intents.registry import IntentContext, build_intent_tools
from kiwoom_client.mcp.local_tools import LocalTool

__all__ = ["IntentContext", "intent_tools"]


def intent_tools(session: Any = None) -> list[LocalTool]:
    """Every intent tool, bound to the server's WebSocket ``session`` (may be ``None``)."""
    return build_intent_tools(IntentContext(session=session))
