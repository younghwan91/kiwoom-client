"""Registry of intent tools — one place where every intent tool is declared.

An *intent tool* answers one thing a person asks ("내 잔고", "삼성전자 일봉")
in one call, without the agent knowing api_ids or Kiwoom field names. Each
module in this package registers a factory with :func:`register`; the server
asks :func:`build_intent_tools` for the finished :class:`LocalTool` list.

Intent tools only read. None of them may place, modify or cancel an order —
order tools exist only as guarded REST tools, so the live-order guard stays
the single gate for them.
"""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from typing import Any

from mcp import types

from kiwoom_client.mcp.local_tools import Handler, LocalTool


@dataclass(frozen=True)
class IntentContext:
    """What a factory may bind into its handlers besides ``api``.

    ``session`` is the server's shared WebSocket session (condition search,
    real-time watch). ``None`` when the server was built without one, e.g. in
    tests that only list tools.
    """

    session: Any = None


Factory = Callable[[IntentContext], list[LocalTool]]

_FACTORIES: list[Factory] = []


def register(factory: Factory) -> Factory:
    """Decorator: add a factory of intent tools. Order of registration is
    the order tools are listed in."""
    _FACTORIES.append(factory)
    return factory


def build_intent_tools(context: IntentContext | None = None) -> list[LocalTool]:
    """Every registered intent tool, in registration order.

    Raises:
        RuntimeError: if two tools share a name.
    """
    context = context or IntentContext()
    tools = [tool for factory in _FACTORIES for tool in factory(context)]
    names = [tool.name for tool in tools]
    duplicates = sorted({name for name in names if names.count(name) > 1})
    if duplicates:
        raise RuntimeError(f"intent 도구 이름이 겹칩니다: {', '.join(duplicates)}")
    return tools


def read_only_tool(
    *,
    name: str,
    title: str,
    description: str,
    properties: dict[str, Any],
    toolset: str,
    handler: Handler,
    required: tuple[str, ...] = (),
) -> LocalTool:
    """A lookup tool: ``readOnlyHint=true``, talks to Kiwoom (open world)."""
    schema: dict[str, Any] = {"type": "object", "properties": properties}
    if required:
        schema["required"] = list(required)
    return LocalTool(
        name=name,
        title=title,
        description=description,
        input_schema=schema,
        annotations=types.ToolAnnotations(
            title=title, read_only_hint=True, destructive_hint=False, open_world_hint=True
        ),
        toolset=toolset,
        handler=handler,
    )
