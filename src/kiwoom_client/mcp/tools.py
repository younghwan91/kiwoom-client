"""Reflection-based discovery of MCP tools from the REST endpoint modules.

Every public method on the 15 endpoint modules follows the same signature —
``(self, cont_yn="N", next_key="", **kwargs)`` — so no per-endpoint mapping is
maintained here; the module list comes straight from
:data:`kiwoom_client._registry.MODULE_NAMES`.
"""

from __future__ import annotations

import inspect
from dataclasses import dataclass

from kiwoom_client._registry import MODULE_NAMES, ModuleRegistry

#: Modules whose methods place live orders. Gated by the opt-in guard in
#: :mod:`kiwoom_client.mcp.guard` when the client is not in mock mode.
GUARDED_MODULES: frozenset[str] = frozenset({"order", "credit_order"})

#: condition_search rides the WebSocket, not REST — handled separately by
#: :mod:`kiwoom_client.mcp.condition_search_session`.
_SKIP_MODULES = frozenset({"condition_search"})


@dataclass(frozen=True)
class RestToolSpec:
    """One discovered REST endpoint method, ready to become an MCP tool."""

    module_name: str
    method_name: str
    tool_name: str
    description: str
    guarded: bool


def discover_rest_tools() -> list[RestToolSpec]:
    """Scan the REST endpoint modules and list their public methods.

    A throwaway ``ModuleRegistry`` (client=``object()``) is enough — module
    ``__init__`` only stores the client, it never calls it during discovery.
    """
    registry: ModuleRegistry = ModuleRegistry()
    registry._client = object()  # type: ignore[assignment]
    registry._init_modules()

    specs: list[RestToolSpec] = []
    for module_name in MODULE_NAMES:
        if module_name in _SKIP_MODULES:
            continue
        module_obj = getattr(registry, module_name)
        for method_name, method in inspect.getmembers(module_obj, inspect.ismethod):
            if method_name.startswith("_"):
                continue
            specs.append(
                RestToolSpec(
                    module_name=module_name,
                    method_name=method_name,
                    tool_name=f"{module_name}_{method_name}",
                    description=(inspect.getdoc(method) or "").strip(),
                    guarded=module_name in GUARDED_MODULES,
                )
            )
    return specs
