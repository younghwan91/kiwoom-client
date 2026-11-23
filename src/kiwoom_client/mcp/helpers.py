"""Backward-compatible home of the first three helper tools.

They now live in :mod:`kiwoom_client.mcp.intents.lookup` with the other
intent tools; this module re-exports them so existing imports keep working.
"""

from __future__ import annotations

from kiwoom_client.mcp.intents.lookup import (
    DEFAULT_MARKETS,
    account_summary,
    lookup_tools,
    stock_search,
    stock_snapshot,
)
from kiwoom_client.mcp.intents.registry import IntentContext
from kiwoom_client.mcp.local_tools import LocalTool

__all__ = [
    "DEFAULT_MARKETS",
    "account_summary",
    "helper_tools",
    "stock_search",
    "stock_snapshot",
]


def helper_tools() -> list[LocalTool]:
    """The three original convenience tools (stock_search, stock_snapshot, account_summary)."""
    return lookup_tools(IntentContext())
