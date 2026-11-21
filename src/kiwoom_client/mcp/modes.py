"""Server listing mode (no ``mcp`` import, so the CLI can read it cheaply)."""

from __future__ import annotations

import os
from collections.abc import Mapping

#: ``discovery`` lists only search_tools/describe_tool/call_tool (see
#: :mod:`.discovery`); anything else, including unset, lists every tool.
ENV_VAR = "KIWOOM_MCP_MODE"
DISCOVERY = "discovery"


def discovery_from_env(env: Mapping[str, str] | None = None) -> bool:
    source = os.environ if env is None else env
    return source.get(ENV_VAR, "").strip().lower() == DISCOVERY
