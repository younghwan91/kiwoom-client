"""The first intent tools: find a stock, one stock's snapshot, account summary.

- ``stock_search``    — 종목명/코드로 종목코드 찾기 (:meth:`AsyncKiwoomAPI.find_stock`, ka10099)
- ``stock_snapshot``  — 현재가·등락·밸류에이션 한 번에 (ka10001 주식기본정보)
- ``account_summary`` — 계좌 평가 합계 + 보유 종목 (kt00018 계좌평가잔고내역)

These keep the names, inputs and output keys they had in ``mcp/helpers.py``
(Kiwoom field ids as keys). Newer intent tools use readable keys instead.
"""

from __future__ import annotations

from typing import Any

from kiwoom_client.mcp.intents.normalize import num, price
from kiwoom_client.mcp.intents.registry import IntentContext, read_only_tool, register
from kiwoom_client.mcp.intents.resolve import NAME_MARKETS, resolve_stock
from kiwoom_client.mcp.local_tools import LocalTool

#: ka10099 mrkt_tp values searched by default: 코스피, 코스닥, ETF.
DEFAULT_MARKETS: tuple[str, ...] = NAME_MARKETS

_SNAPSHOT_FIELDS = (
    "stk_cd", "stk_nm", "cur_prc", "pred_pre", "flu_rt", "trde_qty",
    "open_pric", "high_pric", "low_pric", "base_pric", "upl_pric", "lst_pric",
    "mac", "flo_stk", "for_exh_rt", "per", "pbr", "eps", "roe", "bps",
    "250hgst", "250lwst", "oyr_hgst", "oyr_lwst",
)  # fmt: skip

#: Prices whose sign is the direction of the move, not part of the value.
_PRICE_FIELDS = frozenset({
    "cur_prc", "open_pric", "high_pric", "low_pric", "base_pric", "upl_pric", "lst_pric",
    "250hgst", "250lwst", "oyr_hgst", "oyr_lwst", "pur_pric",
})  # fmt: skip

_ACCOUNT_TOTAL_FIELDS = (
    "tot_pur_amt", "tot_evlt_amt", "tot_evlt_pl", "tot_prft_rt", "prsm_dpst_aset_amt",
    "tot_loan_amt", "tot_crd_loan_amt",
)  # fmt: skip

_HOLDING_FIELDS = (
    "stk_cd", "stk_nm", "rmnd_qty", "trde_able_qty", "pur_pric", "cur_prc",
    "evlt_amt", "evltv_prft", "prft_rt", "poss_rt",
)  # fmt: skip

_STOCK_FIELDS = ("code", "name", "marketName", "upName", "state", "orderWarning", "lastPrice")

#: Identifier/text fields — never converted to numbers.
_TEXT_FIELDS = frozenset({"stk_cd", "stk_nm", "code", "name", "marketName", "upName", "state"})


def _convert(key: str, value: Any) -> Any:
    if key in _TEXT_FIELDS:
        return value
    converted = price(value) if key in _PRICE_FIELDS else num(value)
    # Keep non-numeric text (e.g. a status word) rather than dropping it.
    return value if converted is None and isinstance(value, str) and value.strip() else converted


def _pick(record: dict[str, Any], fields: tuple[str, ...], *, numbers: bool) -> dict[str, Any]:
    """Keep ``fields`` (in order); with ``numbers``, convert non-text fields."""
    picked = {key: record[key] for key in fields if key in record}
    if numbers:
        picked = {k: _convert(k, v) for k, v in picked.items()}
    return picked


async def stock_search(
    api: Any, query: str, *, markets: tuple[str, ...], limit: int
) -> dict[str, Any]:
    """Thin wrapper over :meth:`AsyncKiwoomAPI.find_stock` (ka10099, cached on ``api``)."""
    query = query.strip()
    if not query:
        raise ValueError("query(종목명 또는 종목코드)가 필요합니다")
    rows = await api.find_stock(query, markets=markets, limit=limit)
    results = [_pick(row, _STOCK_FIELDS, numbers=False) for row in rows]
    return {"query": query, "results": results}


async def stock_snapshot(api: Any, stk_cd: str) -> dict[str, Any]:
    stk_cd = stk_cd.strip()
    if not stk_cd:
        raise ValueError("stk_cd(종목코드) 또는 stock(종목명)이 필요합니다")
    resp = await api.stock_info.basic_stock_info(stk_cd=stk_cd)
    return {"source": "ka10001 주식기본정보요청", **_pick(resp, _SNAPSHOT_FIELDS, numbers=True)}


async def account_summary(api: Any, dmst_stex_tp: str) -> dict[str, Any]:
    resp = await api.account.evaluation_balance_detail(qry_tp="1", dmst_stex_tp=dmst_stex_tp)
    holdings = [
        _pick(row, _HOLDING_FIELDS, numbers=True)
        for row in resp.get("acnt_evlt_remn_indv_tot") or []
        if isinstance(row, dict)
    ]
    return {
        "source": "kt00018 계좌평가잔고내역요청 (합산)",
        "totals": _pick(resp, _ACCOUNT_TOTAL_FIELDS, numbers=True),
        "holdings_count": len(holdings),
        "holdings": holdings,
    }


@register
def lookup_tools(_context: IntentContext) -> list[LocalTool]:
    async def on_search(api: Any, arguments: dict[str, Any]) -> dict[str, Any]:
        markets = tuple(str(m) for m in arguments.get("markets") or DEFAULT_MARKETS)
        limit = max(1, min(int(arguments.get("limit", 10)), 50))
        return await stock_search(
            api, str(arguments.get("query", "")), markets=markets, limit=limit
        )

    async def on_snapshot(api: Any, arguments: dict[str, Any]) -> dict[str, Any]:
        code = str(arguments.get("stk_cd") or "").strip()
        if not code and str(arguments.get("stock") or "").strip():
            code = (await resolve_stock(api, arguments["stock"])).code
        return await stock_snapshot(api, code)

    async def on_account(api: Any, arguments: dict[str, Any]) -> dict[str, Any]:
        return await account_summary(api, str(arguments.get("dmst_stex_tp", "KRX")))

    return [
        read_only_tool(
            name="stock_search",
            title="종목 검색 (이름→코드)",
            description=(
                "종목명(일부도 가능, 공백 무시) 또는 종목코드로 종목을 찾아 코드·이름·시장을 "
                "돌려준다. 다른 도구에 넣을 stk_cd 를 모를 때 먼저 부른다. 첫 호출 때 "
                "ka10099 종목 리스트를 시장별로 받아 서버 프로세스 안에 캐시한다."
            ),
            example={"query": "삼성전자"},
            properties={
                "query": {"type": "string", "description": "예: '삼성전자', '카카오', '005930'"},
                "markets": {
                    "type": "array",
                    "items": {"type": "string"},
                    "default": list(DEFAULT_MARKETS),
                    "description": "ka10099 mrkt_tp (0 코스피, 10 코스닥, 8 ETF, 50 코넥스)",
                },
                "limit": {"type": "integer", "default": 10, "minimum": 1, "maximum": 50},
            },
            required=("query",),
            toolset="stock_info",
            handler=on_search,
        ),
        read_only_tool(
            name="stock_snapshot",
            title="종목 현재가·기본정보",
            description=(
                "종목 하나의 현재가·전일대비·등락률·거래량·시고저·상하한가·시가총액·"
                "PER/PBR/EPS/ROE·52주(250일) 고저를 숫자로 한 번에 돌려준다(ka10001). "
                "종목은 stk_cd(코드) 또는 stock(이름도 가능)으로 준다."
            ),
            example={"stock": "삼성전자"},
            properties={
                "stk_cd": {"type": "string", "description": "종목코드 (예: 005930)"},
                "stock": {
                    "type": "string",
                    "description": "stk_cd 대신 종목명 또는 코드 (예: '삼성전자')",
                },
            },
            toolset="stock_info",
            handler=on_snapshot,
        ),
        read_only_tool(
            name="account_summary",
            title="계좌 잔고·평가 요약",
            description=(
                "계좌의 총매입·총평가·평가손익·수익률·추정예탁자산과 보유 종목별 수량·"
                "매입가·현재가·평가손익·수익률을 한 번에 돌려준다(kt00018, 합산). 조회만 한다."
            ),
            example={},
            properties={
                "dmst_stex_tp": {"type": "string", "enum": ["KRX", "NXT"], "default": "KRX"}
            },
            toolset="account",
            handler=on_account,
        ),
    ]
