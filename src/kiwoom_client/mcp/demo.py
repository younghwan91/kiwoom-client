"""Demo mode switch for the MCP server (``--demo`` / ``KIWOOM_MCP_DEMO``).

In demo mode the server runs on :meth:`kiwoom_client.AsyncKiwoomAPI.demo`:
synthetic data, paper orders, no key needed and no connection anywhere.
"""

from __future__ import annotations

import os
from collections.abc import Mapping

from kiwoom_client._env import parse_bool

ENV_VAR = "KIWOOM_MCP_DEMO"


def demo_from_env(env: Mapping[str, str] | None = None) -> bool:
    """``KIWOOM_MCP_DEMO`` as a boolean; unset or empty is ``False``.

    Raises:
        ValueError: a value that is not a recognised boolean.
    """
    source = os.environ if env is None else env
    value = source.get(ENV_VAR, "")
    return parse_bool(value, ENV_VAR) if value.strip() else False
