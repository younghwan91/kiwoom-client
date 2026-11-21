"""MCP resources and prompts: reference data and ready-made workflows.

Resources (read-only, no network):

- ``kiwoom://guide``             — how an agent should use this server (markdown)
- ``kiwoom://tools``             — index of the tools this server exposes right now
- ``kiwoom://codes/trade-types`` — 매매구분 ``trde_tp`` (kt10000)
- ``kiwoom://codes/markets``     — 시장구분 ``mrkt_tp`` (ka10099)
- ``kiwoom://tr/{api_id}``       — request/response fields of one TR (template)

Prompts: ``analyze_stock``, ``review_account``, ``order_checklist``.

Everything here is derived from the TR catalog (:mod:`kiwoom_client.spec`)
and the server's own, already guard-filtered, tool catalog — so the tool
index never lists an order tool the guard has removed.
"""

from __future__ import annotations

import json
from collections.abc import Callable
from dataclasses import dataclass
from typing import Any

from mcp import types

from kiwoom_client import spec
from kiwoom_client.mcp.codes import EXCHANGES, TRADE_TYPES
from kiwoom_client.mcp.discovery import CatalogEntry

GUIDE_URI = "kiwoom://guide"
TOOLS_URI = "kiwoom://tools"
TRADE_TYPES_URI = "kiwoom://codes/trade-types"
MARKETS_URI = "kiwoom://codes/markets"
TR_URI_PREFIX = "kiwoom://tr/"
TR_URI_TEMPLATE = TR_URI_PREFIX + "{api_id}"

_JSON = "application/json"
_MARKDOWN = "text/markdown"

GUIDE = """\
# kiwoom-client MCP 서버 — 에이전트 가이드

- 종목코드를 모르면 `stock_search` 로 먼저 찾는다 (예: "삼성전자" → 005930).
- 현재가·기본 지표는 `stock_snapshot`, 계좌 요약은 `account_summary` 한 번이면 된다.
- 그 밖의 TR 도구는 `<모듈>_<메서드>` 이름이고 `params` 에 키움 요청 필드를 문자열로 넣는다.
  필드 목록은 각 도구의 입력 스키마나 `kiwoom://tr/{api_id}` 리소스에 있다.
- 리스트가 긴 TR(차트·순위)은 `max_rows` 로 행 수를 줄인다. 잘리면 `_truncated` 가 붙는다.
  다음 페이지는 응답의 `cont-yn`/`next-key` 를 `cont_yn="Y"`, `next_key` 로 넘긴다.
- 도구가 너무 많으면 서버를 `--discovery` 로 띄운다.
  `search_tools` → `describe_tool` → `call_tool` 순으로 쓴다.

## 주문

- 주문 전에는 항상 `order_preview` 로 호가단위 보정·검증 결과를 만들고 사용자에게 보여 준다.
- 사용자가 그 내용을 명시적으로 확인하기 전에는 주문 도구를 부르지 않는다.
- 실전 계좌에서는 `KIWOOM_MCP_ALLOW_LIVE_ORDERS=true` 없이는 주문 도구가 아예 없다.
  없으면 없는 것이다 — 다른 경로로 주문을 시도하지 않는다.
"""


@dataclass(frozen=True)
class _Resource:
    uri: str
    name: str
    title: str
    description: str
    mime_type: str
    read: Callable[[], str]

    def to_mcp(self) -> types.Resource:
        return types.Resource(
            uri=self.uri,
            name=self.name,
            title=self.title,
            description=self.description,
            mime_type=self.mime_type,
        )


def _dumps(data: Any) -> str:
    return json.dumps(data, ensure_ascii=False, indent=2)


def market_codes() -> dict[str, str]:
    field = spec.get("ka10099").request_field("mrkt_tp")
    return dict(field.codes) if field is not None else {}


def tool_index(catalog: list[CatalogEntry]) -> list[dict[str, Any]]:
    """name/title/toolset/read_only/api_id for every exposed tool."""
    api_ids = {
        f"{module}_{method}": api_id for (module, method), api_id in spec.endpoint_index().items()
    }
    index = []
    for entry in catalog:
        ann = entry.tool.annotations
        item: dict[str, Any] = {
            "name": entry.tool.name,
            "title": entry.tool.title,
            "toolset": entry.toolset,
            "read_only": bool(ann and ann.read_only_hint),
        }
        if entry.tool.name in api_ids:
            item["api_id"] = api_ids[entry.tool.name]
        index.append(item)
    return index


def _field_json(field: spec.Field) -> dict[str, Any]:
    out: dict[str, Any] = {"id": field.id, "name": field.name, "type": field.type}
    if field.required:
        out["required"] = True
    if field.length is not None:
        out["length"] = field.length
    if field.desc:
        out["desc"] = field.desc
    if field.codes:
        out["codes"] = dict(field.codes)
    if field.parent:
        out["parent"] = field.parent
    return out


def tr_detail(api_id: str) -> dict[str, Any]:
    """One TR's catalog entry as plain JSON (empty attributes dropped)."""
    tr = spec.get(api_id)  # KeyError for unknown ids
    detail: dict[str, Any] = {
        "api_id": tr.api_id,
        "name": tr.name,
        "menu": list(tr.menu),
        "method": tr.method,
        "url": tr.url,
        "request": [_field_json(f) for f in tr.request],
        "response": [_field_json(f) for f in tr.response],
    }
    if tr.note:
        detail["note"] = tr.note
    return detail


def _resources(catalog: list[CatalogEntry]) -> list[_Resource]:
    return [
        _Resource(
            GUIDE_URI, "guide", "에이전트 가이드",
            "이 서버를 쓰는 순서와 주문 규칙", _MARKDOWN, lambda: GUIDE,
        ),
        _Resource(
            TOOLS_URI, "tools", "도구 목록",
            "지금 이 서버가 노출하는 도구(이름·toolset·조회 여부·api_id)", _JSON,
            lambda: _dumps(tool_index(catalog)),
        ),
        _Resource(
            TRADE_TYPES_URI, "trade-types", "매매구분·거래소구분 코드",
            "주식 주문 trde_tp·dmst_stex_tp 코드값 (kt10000)", _JSON,
            lambda: _dumps({"trde_tp": TRADE_TYPES, "dmst_stex_tp": EXCHANGES}),
        ),
        _Resource(
            MARKETS_URI, "markets", "시장구분 코드",
            "종목정보 리스트 mrkt_tp 코드값 (ka10099)", _JSON,
            lambda: _dumps({"mrkt_tp": market_codes()}),
        ),
    ]  # fmt: skip


@dataclass(frozen=True)
class _Prompt:
    name: str
    title: str
    description: str
    arguments: tuple[types.PromptArgument, ...]
    render: Callable[[dict[str, str]], str]

    def to_mcp(self) -> types.Prompt:
        return types.Prompt(
            name=self.name,
            title=self.title,
            description=self.description,
            arguments=list(self.arguments),
        )


def _analyze_stock(args: dict[str, str]) -> str:
    stock = args.get("stock", "").strip()
    if not stock:
        raise ValueError("stock(종목명 또는 종목코드)이 필요합니다")
    return (
        f"'{stock}' 종목을 분석해 줘.\n\n"
        "1. 종목코드가 아니면 stock_search 로 코드를 찾는다 "
        "(여러 개면 가장 맞는 것을 고르고 밝힌다).\n"
        "2. stock_snapshot 으로 현재가·등락률·거래량·시가총액·PER/PBR/ROE·250일 고저를 본다.\n"
        "3. chart_stock_daily_chart 로 최근 일봉을 max_rows=60 으로 받아 추세·거래량 변화를 본다.\n"
        "4. 가능하면 투자자별 매매(stock_info_investor_institution_by_stock 등)로 수급을 본다.\n"
        "5. 숫자는 출처 도구와 함께 적고, 사실과 해석을 구분해 요약한다. "
        "매수·매도 권유나 주문은 하지 않는다.\n\n"
        "discovery 모드라면 같은 도구를 call_tool 로 부른다."
    )


def _review_account(_args: dict[str, str]) -> str:
    return (
        "내 계좌를 점검해 줘.\n\n"
        "1. account_summary 로 총평가·평가손익·수익률과 보유 종목을 본다.\n"
        "2. account_unfilled_orders 로 미체결 주문이 있는지 본다.\n"
        "3. 비중이 큰 종목, 손실이 큰 종목, 미체결 주문을 정리해 표로 보여 준다.\n"
        "조회만 한다 — 주문·정정·취소는 하지 않는다."
    )


def _order_checklist(args: dict[str, str]) -> str:
    request = args.get("request", "").strip()
    if not request:
        raise ValueError("request(원하는 주문 내용)가 필요합니다")
    return (
        f"다음 주문을 준비해 줘: {request}\n\n"
        "1. 종목코드가 없으면 stock_search 로 찾고, stock_snapshot 으로 현재가를 확인한다.\n"
        "2. order_preview 로 미리보기를 만든다(전송 안 됨). "
        "호가단위 보정·경고를 그대로 보여 준다.\n"
        "3. 종목·수량·단가·매매구분·예상금액을 표로 보여 주고 사용자의 명시적 확인을 기다린다.\n"
        "4. 확인을 받기 전에는 주문 도구를 부르지 않는다. order_tools_enabled 가 false 면 "
        "이 서버로는 주문할 수 없다고 알리고 멈춘다 — 가드를 끄라고 권하지 않는다."
    )


_PROMPTS = (
    _Prompt(
        "analyze_stock", "종목 분석",
        "종목 하나를 시세·지표·일봉·수급으로 요약한다(조회만)",
        (types.PromptArgument(name="stock", description="종목명 또는 종목코드", required=True),),
        _analyze_stock,
    ),
    _Prompt(
        "review_account", "계좌 점검",
        "잔고·평가손익·미체결 주문을 한 번에 점검한다(조회만)",
        (),
        _review_account,
    ),
    _Prompt(
        "order_checklist", "주문 전 점검",
        "order_preview 로 미리보기를 만들고 사용자 확인 전에는 주문하지 않는 절차",
        (
            types.PromptArgument(
                name="request", description="예: 삼성전자 10주 7만원 매수", required=True
            ),
        ),
        _order_checklist,
    ),
)  # fmt: skip


def register(app: Any, catalog: list[CatalogEntry]) -> None:
    """Add resources/* and prompts/* handlers to ``app`` (a lowlevel Server)."""
    resources = _resources(catalog)
    by_uri = {resource.uri: resource for resource in resources}
    prompts = {prompt.name: prompt for prompt in _PROMPTS}

    async def list_resources(_ctx: Any, _params: Any) -> types.ListResourcesResult:
        return types.ListResourcesResult(resources=[r.to_mcp() for r in resources])

    async def list_templates(_ctx: Any, _params: Any) -> types.ListResourceTemplatesResult:
        return types.ListResourceTemplatesResult(
            resource_templates=[
                types.ResourceTemplate(
                    uri_template=TR_URI_TEMPLATE,
                    name="tr",
                    title="TR 명세",
                    description="api_id(예: ka10001) 하나의 요청·응답 필드와 코드값",
                    mime_type=_JSON,
                )
            ]
        )

    async def read_resource(
        _ctx: Any, params: types.ReadResourceRequestParams
    ) -> types.ReadResourceResult:
        uri = str(params.uri)
        resource = by_uri.get(uri)
        if resource is not None:
            text, mime = resource.read(), resource.mime_type
        elif uri.startswith(TR_URI_PREFIX):
            api_id = uri[len(TR_URI_PREFIX) :]
            try:
                text, mime = _dumps(tr_detail(api_id)), _JSON
            except KeyError as exc:
                raise ValueError(f"Unknown resource: {uri}") from exc
        else:
            raise ValueError(f"Unknown resource: {uri}")
        return types.ReadResourceResult(
            contents=[types.TextResourceContents(uri=uri, mime_type=mime, text=text)]
        )

    async def list_prompts(_ctx: Any, _params: Any) -> types.ListPromptsResult:
        return types.ListPromptsResult(prompts=[p.to_mcp() for p in prompts.values()])

    async def get_prompt(_ctx: Any, params: types.GetPromptRequestParams) -> types.GetPromptResult:
        prompt = prompts.get(params.name)
        if prompt is None:
            raise ValueError(f"Unknown prompt: {params.name}")
        text = prompt.render(dict(params.arguments or {}))
        return types.GetPromptResult(
            description=prompt.description,
            messages=[
                types.PromptMessage(role="user", content=types.TextContent(type="text", text=text))
            ],
        )

    paginated = types.PaginatedRequestParams
    app.add_request_handler("resources/list", paginated, list_resources)
    app.add_request_handler("resources/templates/list", paginated, list_templates)
    app.add_request_handler("resources/read", types.ReadResourceRequestParams, read_resource)
    app.add_request_handler("prompts/list", paginated, list_prompts)
    app.add_request_handler("prompts/get", types.GetPromptRequestParams, get_prompt)
