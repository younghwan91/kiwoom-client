"""Which request fields an order TR accepts — straight from the TR catalog.

The raw order tools take a free-form ``params`` object. For lookups an extra
key is harmless, but on an order a key the model was talked into adding (a
prompt-injected ``cond_uv``, a field from another TR) changes what is sent.
The order gate therefore refuses any key that is not one of the catalog's
request fields for that TR.
"""

from __future__ import annotations

from collections.abc import Iterable
from functools import lru_cache

from kiwoom_client import spec
from kiwoom_client.mcp.tools import discover_rest_tools


@lru_cache(maxsize=1)
def _order_fields() -> dict[str, frozenset[str] | None]:
    """Raw order tool name -> its request field ids (``None``: not in the catalog)."""
    fields: dict[str, frozenset[str] | None] = {}
    for tool in discover_rest_tools():
        if not tool.guarded:
            continue
        try:
            tr = spec.for_method(tool.module_name, tool.method_name)
        except KeyError:
            fields[tool.tool_name] = None
            continue
        fields[tool.tool_name] = frozenset(f.id for f in tr.request_fields)
    return fields


def order_tool_names() -> frozenset[str]:
    return frozenset(_order_fields())


def unknown_fields(tool: str, keys: Iterable[str]) -> list[str] | None:
    """Keys of ``keys`` that ``tool`` doesn't accept, sorted.

    ``None`` when ``tool`` is not an order TR the catalog describes — the
    caller must refuse rather than guess.
    """
    allowed = _order_fields().get(tool)
    if allowed is None:
        return None
    return sorted(set(keys) - allowed)
