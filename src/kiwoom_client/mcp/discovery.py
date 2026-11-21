"""Discovery mode: three meta tools instead of ~180 endpoint tools.

Every tool definition an MCP server lists is loaded into the agent's context.
With ``KIWOOM_MCP_MODE=discovery`` (or ``--discovery``) the server lists only

- ``search_tools``  — find tools by keyword (Korean or English) / toolset
- ``describe_tool`` — full description and input schema of one tool
- ``call_tool``     — run a tool by name

and the agent pulls in the details of just the tools it needs.

The meta tools see exactly the catalog the server would otherwise list —
already filtered by the live-order guard and the toolset filter. ``call_tool``
can therefore never reach a tool that normal mode would not expose: an order
tool dropped by the guard is "Unknown tool" here too.
"""

from __future__ import annotations

from collections.abc import Awaitable, Callable, Mapping
from dataclasses import dataclass
from typing import Any

from mcp import types

from kiwoom_client.mcp.local_tools import LocalTool

SEARCH_TOOLS = "search_tools"
DESCRIBE_TOOL = "describe_tool"
CALL_TOOL = "call_tool"
META_TOOL_NAMES = frozenset({SEARCH_TOOLS, DESCRIBE_TOOL, CALL_TOOL})

DEFAULT_LIMIT = 20
MAX_LIMIT = 50

#: Runs one catalog tool by name; raises ValueError for an unknown name.
Caller = Callable[[str, dict[str, Any]], Awaitable[Any]]


@dataclass(frozen=True)
class CatalogEntry:
    """One tool the server exposes, plus the toolset it belongs to."""

    tool: types.Tool
    toolset: str


def _summary(entry: CatalogEntry) -> dict[str, Any]:
    ann = entry.tool.annotations
    return {
        "name": entry.tool.name,
        "title": entry.tool.title,
        "toolset": entry.toolset,
        "read_only": bool(ann and ann.read_only_hint),
    }


def search(
    entries: list[CatalogEntry],
    query: str = "",
    *,
    toolset: str | None = None,
    limit: int = DEFAULT_LIMIT,
) -> dict[str, Any]:
    """Keyword search over name, title and description (every word must match).

    With no query and no toolset, returns the toolsets and their tool counts
    so the agent can see the shape of the catalog first.
    """
    limit = max(1, min(int(limit), MAX_LIMIT))
    pool = [e for e in entries if toolset is None or e.toolset == toolset]
    words = query.lower().split()

    if not words and toolset is None:
        counts: dict[str, int] = {}
        for entry in entries:
            counts[entry.toolset] = counts.get(entry.toolset, 0) + 1
        return {
            "toolsets": counts,
            "total": len(entries),
            "hint": "query(예: '잔고', '일봉', 'orderbook') 나 toolset 으로 좁혀 다시 검색",
        }

    def rank(entry: CatalogEntry) -> tuple[int, str] | None:
        name = entry.tool.name.lower()
        title = (entry.tool.title or "").lower()
        haystack = f"{name}\n{title}\n{(entry.tool.description or '').lower()}"
        if not all(word in haystack for word in words):
            return None
        in_name_or_title = sum(word in name or word in title for word in words)
        return (-in_name_or_title, entry.tool.name)

    ranked = sorted((key, entry) for entry in pool if (key := rank(entry)) is not None)
    matches = [_summary(entry) for _key, entry in ranked]
    return {"total": len(matches), "tools": matches[:limit], "truncated": len(matches) > limit}


def describe(entries_by_name: Mapping[str, CatalogEntry], name: str) -> dict[str, Any]:
    entry = entries_by_name.get(name)
    if entry is None:
        raise ValueError(f"Unknown tool: {name} — search_tools 로 이름을 확인하세요")
    detail = entry.tool.model_dump(by_alias=True, exclude_none=True, mode="json")
    detail["toolset"] = entry.toolset
    return detail


def discovery_tools(entries: list[CatalogEntry], call: Caller) -> list[LocalTool]:
    """Build the three meta tools over ``entries`` (the already-filtered catalog)."""
    by_name = {entry.tool.name: entry for entry in entries}
    toolsets = sorted({entry.toolset for entry in entries})
    any_destructive = any(
        entry.tool.annotations is not None and entry.tool.annotations.destructive_hint
        for entry in entries
    )

    async def on_search(_api: Any, arguments: dict[str, Any]) -> dict[str, Any]:
        return search(
            entries,
            str(arguments.get("query", "")),
            toolset=arguments.get("toolset") or None,
            limit=arguments.get("limit", DEFAULT_LIMIT),
        )

    async def on_describe(_api: Any, arguments: dict[str, Any]) -> dict[str, Any]:
        return describe(by_name, str(arguments.get("name", "")))

    async def on_call(_api: Any, arguments: dict[str, Any]) -> Any:
        name = str(arguments.get("name", ""))
        if name in META_TOOL_NAMES:
            raise ValueError(f"{name} 는 call_tool 로 부를 수 없습니다")
        if name not in by_name:
            raise ValueError(f"Unknown tool: {name} — search_tools 로 이름을 확인하세요")
        inner = arguments.get("arguments") or {}
        if not isinstance(inner, dict):
            raise ValueError("arguments 는 object 여야 합니다")
        return await call(name, inner)

    return [
        LocalTool(
            name=SEARCH_TOOLS,
            title="도구 검색",
            description=(
                "키움 API 도구를 키워드로 찾는다(한글/영문, 모든 단어 일치). query 없이 "
                "부르면 toolset 별 도구 수를 돌려준다. 찾은 이름은 describe_tool 로 입력 "
                "스키마를 본 뒤 call_tool 로 실행한다."
            ),
            input_schema={
                "type": "object",
                "properties": {
                    "query": {"type": "string", "description": "예: '잔고', '일봉 차트', 'ETF'"},
                    "toolset": {"type": "string", "enum": toolsets},
                    "limit": {
                        "type": "integer",
                        "default": DEFAULT_LIMIT,
                        "minimum": 1,
                        "maximum": MAX_LIMIT,
                    },
                },
            },
            annotations=types.ToolAnnotations(
                title="도구 검색", read_only_hint=True, open_world_hint=False
            ),
            toolset="discovery",
            handler=on_search,
        ),
        LocalTool(
            name=DESCRIBE_TOOL,
            title="도구 상세",
            description="도구 하나의 설명·입력 스키마·annotations 를 돌려준다.",
            input_schema={
                "type": "object",
                "properties": {
                    "name": {"type": "string", "description": "search_tools 결과의 name"}
                },
                "required": ["name"],
            },
            annotations=types.ToolAnnotations(
                title="도구 상세", read_only_hint=True, open_world_hint=False
            ),
            toolset="discovery",
            handler=on_describe,
        ),
        LocalTool(
            name=CALL_TOOL,
            title="도구 실행",
            description=(
                "이름으로 도구를 실행한다. arguments 는 describe_tool 의 input_schema 를 따른다. "
                "이 서버에 등록된 도구만 부를 수 있다(실주문 가드·toolset 필터 그대로)."
            ),
            input_schema={
                "type": "object",
                "properties": {
                    "name": {"type": "string"},
                    "arguments": {"type": "object", "default": {}},
                },
                "required": ["name"],
            },
            annotations=types.ToolAnnotations(
                title="도구 실행",
                read_only_hint=False,
                destructive_hint=any_destructive,
                idempotent_hint=False,
                open_world_hint=True,
            ),
            toolset="discovery",
            handler=on_call,
        ),
    ]
