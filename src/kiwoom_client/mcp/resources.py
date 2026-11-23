"""MCP resources and prompts: reference data and ready-made workflows.

Resources (read-only, no network):

- ``kiwoom://guide``             — how an agent should use this server (markdown)
- ``kiwoom://tools``             — index of the tools this server exposes right now
- ``kiwoom://codes/trade-types`` — 매매구분 ``trde_tp`` (kt10000)
- ``kiwoom://codes/markets``     — 시장구분 ``mrkt_tp`` (ka10099)
- ``kiwoom://tr/{api_id}``       — request/response fields of one TR (template)

Prompts: ``analyze_stock``, ``review_account``, ``market_today``, ``rebalance``,
``order_checklist``.

Everything here is derived from the TR catalog (:mod:`kiwoom_client.spec`),
the code tables in :mod:`kiwoom_client.mcp.codes` and the server's own,
already guard-filtered, tool catalog — so the tool index never lists an order
tool the guard has removed.
"""

from __future__ import annotations

import json
from collections.abc import Callable
from dataclasses import dataclass
from typing import Any

from mcp import types

from kiwoom_client import spec
from kiwoom_client.mcp.codes import EXCHANGES, STOCK_LIST_MARKETS, TRADE_TYPES
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

## 도구 고르는 순서

1. **목록의 편의 도구부터.** 종목은 이름이나 코드로 받는다 — 코드를 모르면 `stock_search`
   (예: "삼성전자" → 005930). 시세·지표는 `stock_snapshot`, 계좌는 `account_summary` 한 번이면 된다.
2. **맞는 도구가 없으면 `search_tools`.** 키워드(한글/영문, 예: "일봉", "거래대금 상위")로
   찾고 `describe_tool` 로 입력 스키마를 본 뒤 `call_tool` 로 실행한다.
   기본(smart) 모드에서는 목록에 없는 TR 도구를 이름으로 바로 부를 수 없다 —
   `call_tool` 을 거친다(`--full` 이면 전부 목록에 있다).
3. TR 도구는 `<모듈>_<메서드>` 이름이고 `params` 에 키움 요청 필드를 문자열로 넣는다.
   필드 목록은 각 도구의 입력 스키마나 `kiwoom://tr/{api_id}` 리소스에 있다.
4. 리스트가 긴 TR(차트·순위)은 `max_rows` 로 행 수를 줄인다. 잘리면 `_truncated` 가 붙는다.
   다음 페이지는 응답의 `cont-yn`/`next-key` 를 `cont_yn="Y"`, `next_key` 로 넘긴다.

## 주문

1. 주문 전에는 항상 `order_preview` 로 미리보기를 만든다(전송 안 함).
   호가단위 보정·검증·경고가 나온다.
2. 종목·수량·단가·매매구분·예상금액을 사용자에게 보여 주고 **명시적 확인**을 받는다.
3. 확인을 받은 뒤에만 주문 도구를 부른다. 미리보기가 `confirm_token` 을 돌려주면
   그 값을 그대로 넘긴다 — 토큰을 지어내거나, 확인 전에 넘기거나, 다른 주문에 재사용하지 않는다.
4. 실전 계좌에서는 `KIWOOM_MCP_ALLOW_LIVE_ORDERS=true` 없이는 주문 도구가 아예 없다.
   없으면 없는 것이다 — 다른 경로로 주문을 시도하거나 가드를 끄라고 권하지 않는다.
"""


#: Sent in the ``initialize`` result; clients show it to the model up front.
#: Kept short — the long form is the ``kiwoom://guide`` resource.
INSTRUCTIONS = (
    "키움증권 REST API 서버. 목록의 편의 도구부터 쓴다: 종목코드는 stock_search(이름으로 찾음), "
    "시세는 stock_snapshot, 계좌는 account_summary. 맞는 도구가 없으면 search_tools 로 찾아 "
    "describe_tool → call_tool 로 부른다. 긴 리스트는 max_rows 로 줄인다. 주문은 order_preview 로 "
    "미리보기 → 사용자에게 보여 주고 명시적 확인 → 그 뒤에만 주문 도구(미리보기가 confirm_token 을 "
    "주면 그대로 넣는다). 주문 도구가 목록에 없으면 이 서버로는 주문할 수 없다 — 우회하지 않는다. "
    "자세한 규칙: kiwoom://guide"
)


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
    return dict(STOCK_LIST_MARKETS)


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


#: Shared tail: how to reach a tool that is not in the list (smart/discovery).
_NOT_LISTED = (
    "도구가 목록에 없으면(smart·discovery 모드) search_tools 로 찾아 같은 이름을 "
    "call_tool 로 부른다."
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
        "4. 가능하면 투자자별 매매(foreign_institution_foreign_trading_trend, "
        "market_institutional_trading_trend 등)로 수급을 본다.\n"
        "5. 숫자는 출처 도구와 함께 적고, 사실과 해석을 구분해 요약한다. "
        "매수·매도 권유나 주문은 하지 않는다.\n\n" + _NOT_LISTED
    )


def _review_account(_args: dict[str, str]) -> str:
    return (
        "내 계좌 잔고를 점검해 줘.\n\n"
        "1. account_summary 로 총평가·평가손익·수익률과 보유 종목을 본다.\n"
        "2. account_unfilled_orders 로 미체결 주문이 있는지 본다.\n"
        "3. 필요하면 account_deposit_detail 로 예수금·주문가능금액을 본다.\n"
        "4. 비중이 큰 종목, 손실이 큰 종목, 미체결 주문을 정리해 표로 보여 준다.\n"
        "조회만 한다 — 주문·정정·취소는 하지 않는다.\n\n" + _NOT_LISTED
    )


def _market_today(args: dict[str, str]) -> str:
    focus = args.get("focus", "").strip()
    topic = f" ({focus} 중심으로)" if focus else ""
    return (
        f"오늘 국내 주식시장을 요약해 줘{topic}.\n\n"
        "1. sector_all_industry_index 로 코스피·코스닥 등 업종 지수의 등락을 본다.\n"
        "2. ranking_top_trading_value 와 ranking_top_change_rate 로 거래대금·등락률 상위 종목을 "
        "max_rows=10 으로 본다.\n"
        "3. ranking_top_foreign_institution_trades 로 외국인·기관 순매수 상위를 본다.\n"
        "4. 지수 → 주도 종목 → 수급 순으로 짧게 정리하고, 숫자마다 출처 도구를 적는다. "
        "장중이면 그 시각 기준임을 밝힌다.\n"
        "조회만 한다 — 종목 추천·주문은 하지 않는다.\n\n" + _NOT_LISTED
    )


def _rebalance(args: dict[str, str]) -> str:
    target = args.get("target", "").strip()
    if not target:
        raise ValueError("target(목표 비중, 예: 삼성전자 30%, 현금 20%)이 필요합니다")
    return (
        f"내 계좌를 다음 목표 비중으로 맞추는 리밸런싱 계획을 세워 줘: {target}\n\n"
        "1. account_summary 로 보유 종목·평가금액·총자산을 보고, "
        "목표에 나온 종목은 stock_search 로 코드를 확인한다.\n"
        "2. 종목별 현재 비중과 목표 비중의 차이, 사고팔 금액을 표로 계산한다. 현재가는 "
        "stock_snapshot 으로 확인한다.\n"
        "3. 주문마다 order_preview 로 미리보기를 만들어 호가단위 보정·수량·예상금액·경고를 "
        "보여 준다(전송 안 됨). 매도를 매수보다 먼저 둔다.\n"
        "4. 여기서 멈추고 계획 전체를 사용자에게 확인받는다. 확인받은 주문만, 하나씩, "
        "미리보기가 준 confirm_token 이 있으면 그대로 넣어 보낸다. "
        "주문 도구가 없으면 계획만 보여 주고 끝낸다.\n\n"
        + _NOT_LISTED
    )


def _order_checklist(args: dict[str, str]) -> str:
    request = args.get("request", "").strip()
    if not request:
        raise ValueError("request(원하는 주문 내용)가 필요합니다")
    return (
        f"다음 주문을 준비해 줘: {request}\n\n"
        "1. 종목코드가 없으면 stock_search 로 찾고, "
        "stock_snapshot 으로 현재가·상하한가를 확인한다.\n"
        "2. order_preview 로 미리보기를 만든다(전송 안 됨). "
        "호가단위 보정·경고를 그대로 보여 준다.\n"
        "3. 종목·수량·단가·매매구분·예상금액을 표로 보여 주고 사용자의 명시적 확인을 기다린다.\n"
        "4. 확인을 받기 전에는 주문 도구를 부르지 않는다. 확인 뒤 주문할 때 "
        "미리보기가 confirm_token 을 돌려줬다면 그 값을 그대로 넣는다 — "
        "지어내거나 다른 주문에 재사용하지 않는다.\n"
        "5. order_tools_enabled 가 false 면 이 서버로는 주문할 수 없다고 알리고 멈춘다 — "
        "가드를 끄라고 권하지 않는다."
    )


_PROMPTS = (
    _Prompt(
        "analyze_stock", "종목 분석",
        "종목 하나를 시세·지표·일봉·수급으로 요약한다(조회만)",
        (types.PromptArgument(name="stock", description="종목명 또는 종목코드", required=True),),
        _analyze_stock,
    ),
    _Prompt(
        "review_account", "잔고 점검",
        "잔고·평가손익·미체결 주문·예수금을 한 번에 점검한다(조회만)",
        (),
        _review_account,
    ),
    _Prompt(
        "market_today", "오늘 시장",
        "업종 지수·거래대금/등락률 상위·외국인·기관 수급으로 오늘 시장을 요약한다(조회만)",
        (
            types.PromptArgument(
                name="focus", description="관심 분야(선택, 예: 반도체, 코스닥)", required=False
            ),
        ),
        _market_today,
    ),
    _Prompt(
        "rebalance", "리밸런싱",
        "목표 비중과 잔고를 비교해 주문 계획·미리보기를 만든다(확인 전 주문 안 함)",
        (
            types.PromptArgument(
                name="target", description="예: 삼성전자 30%, 현금 50%", required=True
            ),
        ),
        _rebalance,
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
