"""MCP stdio server exposing every kiwoom-client REST endpoint as a tool.

Tool list is generated at startup by reflection (see :mod:`.tools`) — no
per-endpoint mapping is maintained here. Order/credit_order tools are
registered only when :func:`kiwoom_client.mcp.guard.live_orders_allowed`
says so.
"""

from __future__ import annotations

import asyncio
import json
import logging
from collections.abc import Collection
from typing import Any

from mcp import types
from mcp.server import Server, ServerRequestContext
from mcp.server.stdio import stdio_server

from kiwoom_client import AsyncKiwoomAPI
from kiwoom_client.base import KiwoomAPIError
from kiwoom_client.domestic.condition_search import ConditionSearch
from kiwoom_client.mcp.annotations import tool_annotations, tool_title
from kiwoom_client.mcp.condition_search_session import (
    ConditionSearchSession,
    ConditionSearchTimeout,
)
from kiwoom_client.mcp.discovery import CatalogEntry, discovery_tools
from kiwoom_client.mcp.guard import live_orders_allowed
from kiwoom_client.mcp.helpers import helper_tools
from kiwoom_client.mcp.local_tools import LocalTool
from kiwoom_client.mcp.order_preview import order_preview_tool
from kiwoom_client.mcp.response_size import ARGUMENT as MAX_ROWS_ARGUMENT
from kiwoom_client.mcp.response_size import limit_rows, parse_max_rows, with_max_rows_argument
from kiwoom_client.mcp.schema import rest_input_schema, split_arguments
from kiwoom_client.mcp.tools import RestToolSpec, discover_rest_tools
from kiwoom_client.websocket import KiwoomWebSocket

logger = logging.getLogger(__name__)

#: The 4 condition_search tools don't fit the generic **kwargs pattern (they
#: have real, non-passthrough parameters), so they're spelled out here.
_CONDITION_SEARCH_SPECS: list[RestToolSpec] = [
    RestToolSpec(
        module_name="condition_search", method_name="condition_list",
        tool_name="condition_search_condition_list",
        description=(
            "조건검색 목록조회 — 다른 condition_search 도구를 쓰기 전에 먼저 호출해 "
            "seq 값을 얻는다."
        ),
        guarded=False,
    ),
    RestToolSpec(
        module_name="condition_search", method_name="condition_search",
        tool_name="condition_search_condition_search",
        description="조건검색 요청 일반. seq: condition_list 로 얻은 조건검색식 일련번호.",
        guarded=False,
    ),
    RestToolSpec(
        module_name="condition_search", method_name="condition_search_realtime",
        tool_name="condition_search_condition_search_realtime",
        description=(
            "조건검색 요청 실시간. 최초 응답 프레임만 반환한다 — 이후 조건 "
            "편입/이탈에 따라 계속 도착하는 후속 프레임은 이 도구로 받을 수 없다."
        ),
        guarded=False,
    ),
    RestToolSpec(
        module_name="condition_search", method_name="condition_search_cancel",
        tool_name="condition_search_condition_search_cancel",
        description="조건검색 실시간 해제. 키움 프로토콜상 ack 프레임이 없어 전송만 하고 반환한다.",
        guarded=False,
    ),
]


def build_server(
    api: AsyncKiwoomAPI | None,
    *,
    allow_live_orders: bool,
    session: ConditionSearchSession | None = None,
    toolsets: Collection[str] | None = None,
    discovery: bool = False,
    max_rows: int | None = None,
) -> tuple[Server, list[RestToolSpec]]:
    """Assemble the MCP Server, wired with its ``tools/list``/``tools/call``
    handlers, and the filtered list of tool specs.

    No stdio, no network of its own. ``api``/``session`` may be ``None`` when
    the caller only wants ``specs`` for tool-filtering tests — that's safe as
    long as the registered handlers are never actually invoked, since both
    are closures that only touch ``api``/``session`` when called.

    ``toolsets`` (module names, ``None`` = all) narrows the list further. It
    is applied after the live-order guard and can only remove tools.

    ``discovery=True`` lists only the meta tools of :mod:`.discovery`, which
    search and call into that same filtered catalog — never beyond it.

    ``max_rows`` is the default row limit for lookup tools' list responses
    (``None`` = no limit); a call can override it with its own ``max_rows``.
    """
    rest_specs = [
        spec for spec in discover_rest_tools() if not spec.guarded or allow_live_orders
    ]
    all_specs = rest_specs + _CONDITION_SEARCH_SPECS
    if toolsets is not None:
        all_specs = [spec for spec in all_specs if spec.module_name in toolsets]
    spec_by_name = {spec.tool_name: spec for spec in all_specs}
    local_tools = [
        tool
        for tool in _local_tools(allow_live_orders=allow_live_orders)
        if toolsets is None or tool.toolset in toolsets
    ]
    local_by_name = {tool.name: tool for tool in local_tools}
    app: Server = Server("kiwoom-client")

    catalog = [
        CatalogEntry(
            tool=types.Tool(
                name=spec.tool_name,
                title=tool_title(spec),
                description=spec.description,
                input_schema=(
                    _input_schema(spec)
                    if spec.guarded
                    else with_max_rows_argument(_input_schema(spec))
                ),
                annotations=tool_annotations(spec),
            ),
            toolset=spec.module_name,
        )
        for spec in all_specs
    ] + [CatalogEntry(tool=tool.to_mcp(), toolset=tool.toolset) for tool in local_tools]

    async def call_catalog_tool(name: str, arguments: dict[str, Any]) -> Any:
        local = local_by_name.get(name)
        if local is not None:
            return await local.handler(api, arguments)
        arguments = dict(arguments)
        requested = arguments.pop(MAX_ROWS_ARGUMENT, None)
        limit = max_rows if requested is None else parse_max_rows(requested)
        assert api is not None
        result = await dispatch_tool(api, session, spec_by_name, name, arguments)
        return limit_rows(result, limit)

    if discovery:
        meta_tools = discovery_tools(catalog, call_catalog_tool)
        meta_by_name = {tool.name: tool for tool in meta_tools}
        listed = [tool.to_mcp() for tool in meta_tools]
    else:
        listed = [entry.tool for entry in catalog]

    async def call_listed_tool(name: str, arguments: dict[str, Any]) -> Any:
        if discovery:
            meta = meta_by_name.get(name)
            if meta is None:
                raise ValueError(f"Unknown tool: {name} — discovery 모드에서는 call_tool 로 부른다")
            return await meta.handler(api, arguments)
        return await call_catalog_tool(name, arguments)

    async def on_list_tools(
        _ctx: ServerRequestContext[Any], _params: types.PaginatedRequestParams | None
    ) -> types.ListToolsResult:
        return types.ListToolsResult(tools=listed)

    async def on_call_tool(
        _ctx: ServerRequestContext[Any], params: types.CallToolRequestParams
    ) -> types.CallToolResult:
        try:
            result = await call_listed_tool(params.name, params.arguments or {})
        except (KiwoomAPIError, ConditionSearchTimeout, ValueError) as exc:
            return types.CallToolResult(
                content=[types.TextContent(type="text", text=str(exc))],
                is_error=True,
            )
        return types.CallToolResult(
            content=[types.TextContent(type="text", text=json.dumps(result, ensure_ascii=False))]
        )

    app.add_request_handler("tools/list", types.PaginatedRequestParams, on_list_tools)
    app.add_request_handler("tools/call", types.CallToolRequestParams, on_call_tool)

    return app, all_specs


def _local_tools(*, allow_live_orders: bool) -> list[LocalTool]:
    """Hand-written helper tools. None of them can place an order."""
    return [order_preview_tool(order_tools_enabled=allow_live_orders), *helper_tools()]


async def dispatch_tool(
    api: AsyncKiwoomAPI,
    session: ConditionSearchSession | None,
    spec_by_name: dict[str, RestToolSpec],
    name: str,
    arguments: dict[str, Any],
) -> dict[str, Any] | None:
    """Run one tool call and return the raw response dict.

    REST tools call straight through to the matching ``AsyncKiwoomAPI``
    module method. condition_search tools build their WebSocket payload and
    send it through ``session``.
    """
    spec = spec_by_name.get(name)
    if spec is None:
        raise ValueError(f"Unknown tool: {name}")

    if spec.module_name == "condition_search":
        assert session is not None
        cs = ConditionSearch()
        if spec.method_name == "condition_list":
            return await session.request(cs.condition_list())
        if spec.method_name == "condition_search":
            payload = cs.condition_search(
                seq=arguments["seq"],
                search_type=arguments.get("search_type", "0"),
                stex_tp=arguments.get("stex_tp", "K"),
                cont_yn=arguments.get("cont_yn", "N"),
                next_key=arguments.get("next_key", ""),
            )
            return await session.request(payload)
        if spec.method_name == "condition_search_realtime":
            payload = cs.condition_search_realtime(
                seq=arguments["seq"],
                stex_tp=arguments.get("stex_tp", "K"),
                cont_yn=arguments.get("cont_yn", "N"),
                next_key=arguments.get("next_key", ""),
            )
            return await session.request(payload)
        if spec.method_name == "condition_search_cancel":
            payload = cs.condition_search_cancel(seq=arguments["seq"])
            await session.request(payload, expect_reply=False)
            return {"trnm": "CNSRCLR", "seq": arguments["seq"], "status": "sent"}
        raise ValueError(f"Unknown condition_search tool: {name}")

    module_obj = getattr(api, spec.module_name)
    method = getattr(module_obj, spec.method_name)
    params, cont_yn, next_key = split_arguments(arguments)
    return await method(cont_yn=cont_yn, next_key=next_key, **params)


def _condition_search_input_schema(method_name: str) -> dict[str, Any]:
    if method_name == "condition_list":
        return {"type": "object", "properties": {}}
    if method_name == "condition_search_cancel":
        return {
            "type": "object",
            "properties": {"seq": {"type": "string", "description": "조건검색식 일련번호"}},
            "required": ["seq"],
        }
    return {
        "type": "object",
        "properties": {
            "seq": {"type": "string", "description": "조건검색식 일련번호"},
            "search_type": {"type": "string", "default": "0"},
            "stex_tp": {"type": "string", "default": "K"},
            "cont_yn": {"type": "string", "default": "N"},
            "next_key": {"type": "string", "default": ""},
        },
        "required": ["seq"],
    }


def _input_schema(spec: RestToolSpec) -> dict[str, Any]:
    if spec.module_name == "condition_search":
        return _condition_search_input_schema(spec.method_name)
    return rest_input_schema(spec.module_name, spec.method_name)


def run_server(
    *,
    app_key: str,
    app_secret: str,
    is_mock: bool,
    toolsets: Collection[str] | None = None,
    discovery: bool = False,
    max_rows: int | None = None,
) -> None:
    """Start the stdio MCP server and block until the client disconnects."""
    logging.basicConfig(level=logging.INFO)

    api = AsyncKiwoomAPI(app_key, app_secret, is_mock=is_mock)
    allow_live_orders = live_orders_allowed(is_mock=is_mock)
    session = ConditionSearchSession(connect=lambda: _connect_condition_search(api))
    app, specs = build_server(
        api,
        allow_live_orders=allow_live_orders,
        session=session,
        toolsets=toolsets,
        discovery=discovery,
        max_rows=max_rows,
    )
    if not allow_live_orders:
        excluded = sum(1 for s in discover_rest_tools() if s.guarded)
        logger.info("실주문 opt-in 미설정 — 주문 도구 %d개를 등록하지 않았습니다.", excluded)
    if toolsets is not None:
        logger.info("toolset 필터 %s — 도구 %d개를 등록했습니다.", sorted(toolsets), len(specs))
    if discovery:
        logger.info("discovery 모드 — search_tools/describe_tool/call_tool 만 노출합니다.")
    if max_rows is not None:
        logger.info("리스트 응답을 기본 %d행으로 자릅니다 (호출별 max_rows 로 변경).", max_rows)

    async def _run() -> None:
        try:
            async with stdio_server() as (read_stream, write_stream):
                await app.run(read_stream, write_stream, app.create_initialization_options())
        finally:
            await session.close()
            await api.close()

    asyncio.run(_run())


def main() -> None:
    """Backward-compatible entry point — the CLI lives in :mod:`.cli`."""
    from kiwoom_client.mcp.cli import main as cli_main

    cli_main()


async def _connect_condition_search(api: AsyncKiwoomAPI) -> KiwoomWebSocket:
    ws = await api.create_websocket()
    await ws.connect()
    return ws


if __name__ == "__main__":
    main()
