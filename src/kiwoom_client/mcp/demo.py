"""Demo mode switch for the MCP server (``--demo`` / ``KIWOOM_MCP_DEMO``).

In demo mode the server runs on :meth:`kiwoom_client.AsyncKiwoomAPI.demo`:
synthetic data, paper orders, no key needed and no connection anywhere.

``KIWOOM_MCP_DEMO`` takes a boolean, or ``auto``: demo only when no app key
and secret are set. The Claude Desktop bundle uses ``auto`` so it works the
moment it is installed and switches to the real server once keys are entered.
"""

from __future__ import annotations

import os
from collections.abc import Mapping

from kiwoom_client._env import parse_bool

ENV_VAR = "KIWOOM_MCP_DEMO"
AUTO = "auto"


def demo_from_env(env: Mapping[str, str] | None = None, *, have_keys: bool = True) -> bool:
    """``KIWOOM_MCP_DEMO`` as a boolean; unset or empty is ``False``.

    ``auto`` is ``True`` exactly when ``have_keys`` is false.

    Raises:
        ValueError: a value that is neither ``auto`` nor a recognised boolean.
    """
    source = os.environ if env is None else env
    value = source.get(ENV_VAR, "").strip()
    if not value:
        return False
    if value.lower() == AUTO:
        return not have_keys
    return parse_bool(value, ENV_VAR)
