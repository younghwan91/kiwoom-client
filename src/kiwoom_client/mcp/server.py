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
import os
import sys
from typing import Any

from mcp import types
from mcp.server import Server, ServerRequestContext
from mcp.server.stdio import stdio_server

from kiwoom_client import AsyncKiwoomAPI
from kiwoom_client.base import KiwoomAPIError
from kiwoom_client.domestic.condition_search import ConditionSearch
from kiwoom_client.mcp.condition_search_session import (
    ConditionSearchSession,
    ConditionSearchTimeout,
)
from kiwoom_client.mcp.guard import live_orders_allowed
from kiwoom_client.mcp.tools import RestToolSpec, discover_rest_tools

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
) -> tuple[Server, list[RestToolSpec]]:
    """Assemble the MCP Server, wired with its ``tools/list``/``tools/call``
    handlers, and the filtered list of tool specs.

    No stdio, no network of its own. ``api``/``session`` may be ``None`` when
    the caller only wants ``specs`` for tool-filtering tests — that's safe as
    long as the registered handlers are never actually invoked, since both
    are closures that only touch ``api``/``session`` when called.
    """
    rest_specs = [
        spec for spec in discover_rest_tools() if not spec.guarded or allow_live_orders
    ]
    all_specs = rest_specs + _CONDITION_SEARCH_SPECS
    spec_by_name = {spec.tool_name: spec for spec in all_specs}
    app: Server = Server("kiwoom-client")

    async def on_list_tools(
        _ctx: ServerRequestContext[Any], _params: types.PaginatedRequestParams | None
    ) -> types.ListToolsResult:
        return types.ListToolsResult(
            tools=[
                types.Tool(
                    name=spec.tool_name,
                    description=spec.description,
                    input_schema=_input_schema(spec),
                )
                for spec in all_specs
            ]
        )

    async def on_call_tool(
        _ctx: ServerRequestContext[Any], params: types.CallToolRequestParams
    ) -> types.CallToolResult:
        assert api is not None
        try:
            result = await dispatch_tool(
                api, session, spec_by_name, params.name, params.arguments or {}
            )
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
    params = arguments.get("params") or {}
    cont_yn = arguments.get("cont_yn", "N")
    next_key = arguments.get("next_key", "")
    return await method(cont_yn=cont_yn, next_key=next_key, **params)


def _rest_input_schema() -> dict[str, Any]:
    return {
        "type": "object",
        "properties": {
            "cont_yn": {"type": "string", "default": "N", "description": "연속조회 여부"},
            "next_key": {"type": "string", "default": "", "description": "연속조회 키"},
            "params": {"type": "object", "description": "TR 요청 필드 (키움 API 가이드 참고)"},
        },
    }


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
    return _rest_input_schema()


def main() -> None:
    """Entry point for the ``kiwoom-client-mcp`` console script."""
    logging.basicConfig(level=logging.INFO)

    app_key = os.environ.get("KIWOOM_APP_KEY")
    app_secret = os.environ.get("KIWOOM_APP_SECRET")
    if not app_key or not app_secret:
        print(
            "Error: KIWOOM_APP_KEY and KIWOOM_APP_SECRET environment variables must be set.",
            file=sys.stderr,
        )
        sys.exit(1)
    is_mock = os.environ.get("KIWOOM_IS_MOCK", "false").strip().lower() == "true"

    api = AsyncKiwoomAPI(app_key, app_secret, is_mock=is_mock)
    allow_live_orders = live_orders_allowed(is_mock=is_mock)
    session = ConditionSearchSession(connect=lambda: _connect_condition_search(api))
    app, specs = build_server(api, allow_live_orders=allow_live_orders, session=session)
    registered_rest = [s for s in specs if s.module_name != "condition_search"]
    excluded = len(discover_rest_tools()) - len(registered_rest)
    if excluded:
        logger.info("실주문 opt-in 미설정 — 주문 도구 %d개를 등록하지 않았습니다.", excluded)

    async def _run() -> None:
        try:
            async with stdio_server() as (read_stream, write_stream):
                await app.run(read_stream, write_stream, app.create_initialization_options())
        finally:
            await session.close()
            await api.close()

    asyncio.run(_run())


async def _connect_condition_search(api: AsyncKiwoomAPI):
    ws = await api.create_websocket()
    await ws.connect()
    return ws


if __name__ == "__main__":
    main()
