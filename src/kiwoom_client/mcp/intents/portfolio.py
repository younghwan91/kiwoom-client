"""``get_portfolio`` — holdings with weights and P&L, cash, and totals.

Built from three lookups sent concurrently (different TRs, so the per-TR
limiter doesn't serialise them):

- kt00018 계좌평가잔고내역 (합산) — holdings, followed across pages, and totals
- kt00001 예수금상세현황 (추정조회) — D+2 estimated deposit (cash) and orderable cash
- ka00001 계좌번호조회 — the account number, returned masked

Weights are computed here: ``weight_pct`` of total assets (stock value +
D+2 cash) and ``stock_weight_pct`` of stock value alone.
"""

from __future__ import annotations

import asyncio
from typing import Any

from kiwoom_client.mcp.intents.common import fetch_rows
from kiwoom_client.mcp.intents.normalize import mask_account, num, pct, pick, price, stock_code
from kiwoom_client.mcp.intents.normalize import text as text_value
from kiwoom_client.mcp.intents.registry import IntentContext, read_only_tool, register
from kiwoom_client.mcp.local_tools import LocalTool

HOLDINGS_KEY = "acnt_evlt_remn_indv_tot"
SOURCES = (
    "kt00018 계좌평가잔고내역요청 (합산)",
    "kt00001 예수금상세현황요청 (추정조회)",
    "ka00001 계좌번호조회",
)

#: Pages of holdings followed at most (each page holds many rows).
MAX_HOLDING_PAGES = 10

HOLDING_FIELDS: dict[str, tuple[str, Any]] = {
    "code": ("stk_cd", stock_code),
    "name": ("stk_nm", text_value),
    "qty": ("rmnd_qty", num),
    "sellable_qty": ("trde_able_qty", num),
    "avg_price": ("pur_pric", price),
    "price": ("cur_prc", price),
    "purchase_amount": ("pur_amt", num),
    "value": ("evlt_amt", num),
    "pnl": ("evltv_prft", num),
    "return_pct": ("prft_rt", pct),
}

TOTAL_FIELDS: dict[str, tuple[str, Any]] = {
    "purchase_amount": ("tot_pur_amt", num),
    "stock_value": ("tot_evlt_amt", num),
    "pnl": ("tot_evlt_pl", num),
    "return_pct": ("tot_prft_rt", pct),
    "estimated_deposit_assets": ("prsm_dpst_aset_amt", num),
    "loan_amount": ("tot_loan_amt", num),
}

CASH_FIELDS: dict[str, tuple[str, Any]] = {
    "cash_d2": ("d2_entra", num),
    "deposit": ("entr", num),
    "orderable_cash": ("ord_alow_amt", num),
}


def _share(part: Any, whole: Any) -> float | None:
    if not isinstance(part, (int, float)) or not isinstance(whole, (int, float)) or whole <= 0:
        return None
    return round(part / whole * 100, 2)


def build_portfolio(
    balance: dict[str, Any],
    holdings: list[dict[str, Any]],
    deposit: dict[str, Any],
    account_no: Any = None,
) -> dict[str, Any]:
    """Assemble the portfolio from raw kt00018 / kt00001 / ka00001 data. Pure."""
    rows = [pick(record, HOLDING_FIELDS) for record in holdings]
    rows = [row for row in rows if row.get("code") and (row.get("qty") or 0) > 0]
    totals = pick(balance, TOTAL_FIELDS)
    cash = pick(deposit, CASH_FIELDS)
    stock_value = sum(row.get("value") or 0 for row in rows)
    if totals.get("stock_value") is None:
        totals["stock_value"] = stock_value
    cash_d2 = cash.get("cash_d2")
    total_assets = stock_value + (cash_d2 or 0)
    for row in rows:
        row["weight_pct"] = _share(row.get("value"), total_assets)
        row["stock_weight_pct"] = _share(row.get("value"), stock_value)
    rows.sort(key=lambda row: row.get("value") or 0, reverse=True)
    totals.update(cash)
    totals["total_assets"] = total_assets
    totals["cash_weight_pct"] = _share(cash_d2, total_assets)
    return {
        "account": mask_account(account_no),
        "sources": list(SOURCES),
        "unit": "krw",
        "totals": totals,
        "holdings_count": len(rows),
        "holdings": rows,
    }


async def fetch_portfolio(api: Any, exchange: str = "KRX") -> dict[str, Any]:
    async def balance() -> tuple[dict[str, Any], list[dict[str, Any]]]:
        return await fetch_rows(
            api.account.evaluation_balance_detail,
            HOLDINGS_KEY,
            {"qry_tp": "1", "dmst_stex_tp": exchange},
            want=10**9,
            max_pages=MAX_HOLDING_PAGES,
        )

    (first, holdings), deposit, account = await asyncio.gather(
        balance(),
        api.account.deposit_detail(qry_tp="3"),
        api.account.account_number_inquiry(),
    )
    return build_portfolio(first, holdings, deposit, (account or {}).get("acctNo"))


@register
def portfolio_tools(_context: IntentContext) -> list[LocalTool]:
    async def handler(api: Any, arguments: dict[str, Any]) -> dict[str, Any]:
        exchange = str(arguments.get("dmst_stex_tp") or "KRX").strip().upper()
        if exchange not in ("KRX", "NXT"):
            raise ValueError(f"dmst_stex_tp 는 KRX 또는 NXT 입니다: {exchange!r}")
        return await fetch_portfolio(api, exchange)

    return [
        read_only_tool(
            name="get_portfolio",
            title="포트폴리오 (비중·손익·현금)",
            description=(
                "보유 종목별 수량·평균단가·현재가·평가금액·평가손익·수익률·비중(총자산 대비, 주식 "
                "대비)과 현금(D+2 추정예수금)·주문가능금액·총자산·총손익을 한 번에 돌려준다"
                "(kt00018+kt00001, 계좌번호는 마스킹). '내 잔고·수익률 보여줘'에 쓴다. "
                "금액 단위 원."
            ),
            properties={
                "dmst_stex_tp": {"type": "string", "enum": ["KRX", "NXT"], "default": "KRX"}
            },
            toolset="account",
            handler=handler,
            example={},
        )
    ]
