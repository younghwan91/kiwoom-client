"""Order-safety settings for the MCP server, read from the environment.

No ``mcp`` import here: the CLI validates these before the server starts.
Every setting can only add checks on top of the live-order opt-in guard.
"""

from __future__ import annotations

import os
from collections.abc import Mapping
from dataclasses import dataclass

from kiwoom_client._env import parse_bool

#: Require a ``confirm_token`` from ``order_preview`` on the raw TR order
#: tools (``order_*``, ``credit_order_*``). Default: true on live, false on mock.
#: The high-level tools (``place_order`` ...) always require one.
REQUIRE_CONFIRM_ENV = "KIWOOM_MCP_REQUIRE_CONFIRM"

#: Seconds a confirmation token stays valid.
DEFAULT_CONFIRM_TTL = 120


def _bool(env: Mapping[str, str], name: str, default: bool) -> bool:
    value = env.get(name, "")
    return parse_bool(value, name) if value.strip() else default


@dataclass(frozen=True)
class OrderPolicy:
    """What the order gate enforces. The defaults are the strict (live) ones."""

    require_confirm: bool = True
    confirm_ttl: int = DEFAULT_CONFIRM_TTL

    @classmethod
    def from_env(cls, *, is_mock: bool, env: Mapping[str, str] | None = None) -> OrderPolicy:
        """Read the ``KIWOOM_MCP_*`` order settings.

        Raises:
            ValueError: for a value that can't be parsed — the server refuses
                to start rather than guess.
        """
        source = os.environ if env is None else env
        return cls(require_confirm=_bool(source, REQUIRE_CONFIRM_ENV, not is_mock))
