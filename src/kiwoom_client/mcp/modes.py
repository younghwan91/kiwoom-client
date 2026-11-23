"""Server listing mode (no ``mcp`` import, so the CLI can read it cheaply).

What ``tools/list`` shows the agent:

- ``smart`` (default) — the hand-written high-level tools (intent tools such as
  ``stock_snapshot``/``account_summary``/``order_preview``) plus the three
  discovery meta tools ``search_tools``/``describe_tool``/``call_tool``, which
  reach every other TR tool. Small enough to leave on all the time.
- ``full`` — every tool (~180 TR tools, ~220 K characters of definitions).
  This was the default up to 0.5.x.
- ``discovery`` — only the three meta tools.

Every mode lists from the same catalog, which the live-order guard and the
toolset filter have already narrowed — a mode can only hide tools, never add
one back.
"""

from __future__ import annotations

import os
from collections.abc import Mapping

ENV_VAR = "KIWOOM_MCP_MODE"
SMART = "smart"
FULL = "full"
DISCOVERY = "discovery"

#: Valid values for :data:`ENV_VAR`, default first.
MODES: tuple[str, ...] = (SMART, FULL, DISCOVERY)
DEFAULT_MODE = SMART


def parse_mode(value: str | None) -> str:
    """``"Full"`` → ``"full"``; ``None``/``""`` → :data:`DEFAULT_MODE`.

    Raises:
        ValueError: if ``value`` is not one of :data:`MODES`.
    """
    mode = (value or "").strip().lower()
    if not mode:
        return DEFAULT_MODE
    if mode not in MODES:
        raise ValueError(f"알 수 없는 {ENV_VAR}: {value!r} (가능한 값: {', '.join(MODES)})")
    return mode


def mode_from_env(env: Mapping[str, str] | None = None) -> str:
    """Read :data:`ENV_VAR` from ``env`` (default ``os.environ``)."""
    source = os.environ if env is None else env
    return parse_mode(source.get(ENV_VAR))


def discovery_from_env(env: Mapping[str, str] | None = None) -> bool:
    """Whether :data:`ENV_VAR` asks for discovery mode (kept for older callers)."""
    source = os.environ if env is None else env
    return source.get(ENV_VAR, "").strip().lower() == DISCOVERY
