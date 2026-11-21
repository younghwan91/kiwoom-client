"""Toolset filter: expose only some endpoint modules as MCP tools.

~180 tools cost an agent a lot of context before it has done anything.
``KIWOOM_MCP_TOOLSETS=market,chart,account`` (or ``--toolsets``) keeps only
those modules' tools. Unset or empty means every module — the default and the
behaviour before this option existed.

The filter only ever *removes* tools. It runs after the live-order guard, so
naming ``order`` here cannot bring back order tools the guard has dropped.
"""

from __future__ import annotations

import os
from collections.abc import Mapping

from kiwoom_client._registry import MODULE_NAMES

#: Environment variable holding a comma-separated list of toolset names.
ENV_VAR = "KIWOOM_MCP_TOOLSETS"

#: Valid toolset names — one per endpoint module, in facade order.
TOOLSET_NAMES: tuple[str, ...] = MODULE_NAMES


def parse_toolsets(value: str | None) -> frozenset[str] | None:
    """Parse ``"market, chart"`` into a set of toolset names.

    Returns ``None`` (= all toolsets) for ``None``, ``""`` or ``"all"``.

    Raises:
        ValueError: if a name is not one of :data:`TOOLSET_NAMES`.
    """
    if value is None:
        return None
    names = {part.strip().lower() for part in value.split(",") if part.strip()}
    if not names or names == {"all"}:
        return None
    unknown = sorted(names - set(TOOLSET_NAMES))
    if unknown:
        raise ValueError(
            f"알 수 없는 toolset: {', '.join(unknown)} (가능한 값: {', '.join(TOOLSET_NAMES)})"
        )
    return frozenset(names)


def toolsets_from_env(env: Mapping[str, str] | None = None) -> frozenset[str] | None:
    """Read :data:`ENV_VAR` from ``env`` (default ``os.environ``)."""
    source = os.environ if env is None else env
    return parse_toolsets(source.get(ENV_VAR))
