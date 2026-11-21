"""MCP tool annotations (``title``, ``readOnlyHint``, ``destructiveHint`` ...).

Clients such as Claude Code and Claude Desktop use these hints to decide how
to present a tool and whether to ask before running it: a read-only lookup
can be auto-approved, a destructive one gets a confirmation prompt. The hints
are derived from the same ``guarded`` flag the live-order guard uses, so the
two can never disagree about which tools place orders.

Annotations are hints only — they never replace the opt-in guard in
:mod:`kiwoom_client.mcp.guard`, which keeps order tools off the server
entirely unless explicitly allowed.
"""

from __future__ import annotations

from mcp import types

from kiwoom_client.mcp.tools import RestToolSpec

#: Prefixed to the title of every order tool so it stands out in tool pickers.
LIVE_ORDER_TITLE_PREFIX = "[주문] "

#: condition_search tools that change server-side subscription state
#: (register / drop a real-time condition) rather than just reading.
_SUBSCRIPTION_TOOLS = frozenset({"condition_search_realtime", "condition_search_cancel"})


def tool_title(spec: RestToolSpec) -> str:
    """Human-readable title: the first line of the tool's description."""
    first_line = spec.description.strip().splitlines()[0] if spec.description.strip() else ""
    title = first_line or spec.tool_name
    if spec.guarded:
        title = LIVE_ORDER_TITLE_PREFIX + title
    return title


def tool_annotations(spec: RestToolSpec) -> types.ToolAnnotations:
    """Behaviour hints for one tool.

    - Order tools (``guarded``): may place, modify or cancel a real order —
      destructive, not idempotent (sending the same buy twice buys twice).
    - condition_search real-time register/cancel: mutates subscription state
      only — not read-only, but not destructive and safe to repeat.
    - Everything else is a lookup: read-only.

    Every tool talks to the Kiwoom servers, so ``openWorldHint`` is always true.
    """
    title = tool_title(spec)
    if spec.guarded:
        return types.ToolAnnotations(
            title=title,
            read_only_hint=False,
            destructive_hint=True,
            idempotent_hint=False,
            open_world_hint=True,
        )
    if spec.module_name == "condition_search" and spec.method_name in _SUBSCRIPTION_TOOLS:
        return types.ToolAnnotations(
            title=title,
            read_only_hint=False,
            destructive_hint=False,
            idempotent_hint=True,
            open_world_hint=True,
        )
    return types.ToolAnnotations(title=title, read_only_hint=True, open_world_hint=True)
