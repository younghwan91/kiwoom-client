"""High-level lookup tools for the questions agents ask most.

Each one answers a common question in one call, built only from existing
endpoint methods — no new Kiwoom endpoints, no orders:

- ``stock_search``   — 종목명/코드로 종목코드 찾기 (:meth:`AsyncKiwoomAPI.find_stock`, ka10099)
- ``stock_snapshot`` — 현재가·등락·밸류에이션 한 번에 (ka10001 주식기본정보)
- ``account_summary`` — 계좌 평가 합계 + 보유 종목 (kt00018 계좌평가잔고내역)

Field names come from the TR catalog (:mod:`kiwoom_client.spec`). Amounts and
rates come back as numbers (zero padding and ``+``/``,`` removed); codes and
names stay strings.
"""

from __future__ import annotations

from typing import Any

from mcp import types

from kiwoom_client.mcp.local_tools import LocalTool

#: ka10099 mrkt_tp values searched by default: 코스피, 코스닥, ETF.
DEFAULT_MARKETS: tuple[str, ...] = ("0", "10", "8")

_SNAPSHOT_FIELDS = (
    "stk_cd", "stk_nm", "cur_prc", "pred_pre", "flu_rt", "trde_qty",
    "open_pric", "high_pric", "low_pric", "base_pric", "upl_pric", "lst_pric",
    "mac", "flo_stk", "for_exh_rt", "per", "pbr", "eps", "roe", "bps",
    "250hgst", "250lwst", "oyr_hgst", "oyr_lwst",
)  # fmt: skip

_ACCOUNT_TOTAL_FIELDS = (
    "tot_pur_amt", "tot_evlt_amt", "tot_evlt_pl", "tot_prft_rt", "prsm_dpst_aset_amt",
    "tot_loan_amt", "tot_crd_loan_amt",
)  # fmt: skip

_HOLDING_FIELDS = (
    "stk_cd", "stk_nm", "rmnd_qty", "trde_able_qty", "pur_pric", "cur_prc",
    "evlt_amt", "evltv_prft", "prft_rt", "poss_rt",
)  # fmt: skip

_STOCK_FIELDS = ("code", "name", "marketName", "upName", "state", "orderWarning", "lastPrice")

_READ_ONLY = {"read_only_hint": True, "open_world_hint": True}


#: Identifier/text fields — never converted to numbers.
_TEXT_FIELDS = frozenset({"stk_cd", "stk_nm", "code", "name", "marketName", "upName", "state"})


def _number(value: Any) -> Any:
    """Kiwoom numeric string → int/float, including zero-padded amounts
    (``"000001000000"`` → ``1000000``) that generic parsing keeps as text."""
    if not isinstance(value, str):
        return value
    text = value.strip().replace(",", "")
    if not text:
        return None
    try:
        number = float(text)
    except ValueError:
        return value
    return int(number) if "." not in text and number.is_integer() else number


def _pick(record: dict[str, Any], fields: tuple[str, ...], *, numbers: bool) -> dict[str, Any]:
    """Keep ``fields`` (in order); with ``numbers``, convert non-text fields."""
    picked = {key: record[key] for key in fields if key in record}
    if numbers:
        picked = {k: v if k in _TEXT_FIELDS else _number(v) for k, v in picked.items()}
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
        raise ValueError("stk_cd(종목코드)가 필요합니다")
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


def helper_tools() -> list[LocalTool]:
    """The three convenience tools."""

    async def on_search(api: Any, arguments: dict[str, Any]) -> dict[str, Any]:
        markets = tuple(str(m) for m in arguments.get("markets") or DEFAULT_MARKETS)
        limit = max(1, min(int(arguments.get("limit", 10)), 50))
        return await stock_search(
            api, str(arguments.get("query", "")), markets=markets, limit=limit
        )

    async def on_snapshot(api: Any, arguments: dict[str, Any]) -> dict[str, Any]:
        return await stock_snapshot(api, str(arguments.get("stk_cd", "")))

    async def on_account(api: Any, arguments: dict[str, Any]) -> dict[str, Any]:
        return await account_summary(api, str(arguments.get("dmst_stex_tp", "KRX")))

    return [
        LocalTool(
            name="stock_search",
            title="종목 검색 (이름→코드)",
            description=(
                "종목명(일부도 가능, 공백 무시) 또는 종목코드로 종목을 찾아 코드·이름·시장을 "
                "돌려준다. 다른 도구에 넣을 stk_cd 를 모를 때 먼저 부른다. 첫 호출 때 "
                "ka10099 종목 리스트를 시장별로 받아 서버 프로세스 안에 캐시한다."
            ),
            input_schema={
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "예: '삼성전자', '카카오', '005930'",
                    },
                    "markets": {
                        "type": "array",
                        "items": {"type": "string"},
                        "default": list(DEFAULT_MARKETS),
                        "description": "ka10099 mrkt_tp (0 코스피, 10 코스닥, 8 ETF, 50 코넥스)",
                    },
                    "limit": {"type": "integer", "default": 10, "minimum": 1, "maximum": 50},
                },
                "required": ["query"],
            },
            annotations=types.ToolAnnotations(title="종목 검색 (이름→코드)", **_READ_ONLY),
            toolset="stock_info",
            handler=on_search,
        ),
        LocalTool(
            name="stock_snapshot",
            title="종목 현재가·기본정보",
            description=(
                "종목 하나의 현재가·전일대비·등락률·거래량·시고저·상하한가·시가총액·"
                "PER/PBR/EPS/ROE·52주(250일) 고저를 숫자로 한 번에 돌려준다(ka10001)."
            ),
            input_schema={
                "type": "object",
                "properties": {
                    "stk_cd": {"type": "string", "description": "종목코드 (예: 005930)"}
                },
                "required": ["stk_cd"],
            },
            annotations=types.ToolAnnotations(title="종목 현재가·기본정보", **_READ_ONLY),
            toolset="stock_info",
            handler=on_snapshot,
        ),
        LocalTool(
            name="account_summary",
            title="계좌 잔고·평가 요약",
            description=(
                "계좌의 총매입·총평가·평가손익·수익률·추정예탁자산과 보유 종목별 수량·"
                "매입가·현재가·평가손익·수익률을 한 번에 돌려준다(kt00018, 합산). 조회만 한다."
            ),
            input_schema={
                "type": "object",
                "properties": {
                    "dmst_stex_tp": {"type": "string", "enum": ["KRX", "NXT"], "default": "KRX"}
                },
            },
            annotations=types.ToolAnnotations(title="계좌 잔고·평가 요약", **_READ_ONLY),
            toolset="account",
            handler=on_account,
        ),
    ]
