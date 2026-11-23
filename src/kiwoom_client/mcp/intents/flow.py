"""``investor_flow`` — daily net buying by individuals, foreigners and institutions.

ka10059 (종목별투자자기관별요청) with 순매수 (``trde_tp=0``), one row per day,
followed across pages until ``days`` rows. ``unit="amount"`` reports 백만원
(``amt_qty_tp=1``), ``unit="quantity"`` reports shares (``amt_qty_tp=2``,
``unit_tp=1`` 단주) — the units the Kiwoom spec gives for these fields.
"""

from __future__ import annotations

from typing import Any

from kiwoom_client.mcp.intents.common import date_arg, fetch_rows, today_kst
from kiwoom_client.mcp.intents.limits import count_schema, row_count
from kiwoom_client.mcp.intents.normalize import date, num, pick, price
from kiwoom_client.mcp.intents.registry import IntentContext, read_only_tool, register
from kiwoom_client.mcp.intents.resolve import resolve_stock, stock_schema
from kiwoom_client.mcp.local_tools import LocalTool

SOURCE = "ka10059 종목별투자자기관별요청 (순매수)"
KEY = "stk_invsr_orgn"

#: unit argument → (amt_qty_tp, label)
UNITS: dict[str, tuple[str, str]] = {"amount": ("1", "million_krw"), "quantity": ("2", "shares")}

#: Investor groups reported, in output order.
INVESTORS: dict[str, str] = {
    "individual": "ind_invsr",
    "foreign": "frgnr_invsr",
    "institution": "orgn",
    "financial_investment": "fnnc_invt",
    "investment_trust": "invtrt",
    "pension": "penfnd_etc",
    "private_fund": "samo_fund",
    "insurance": "insrnc",
    "bank": "bank",
    "other_corporation": "etc_corp",
}

_ROW_FIELDS: dict[str, tuple[str, Any]] = {
    "date": ("dt", date),
    "close": ("cur_prc", price),
    "change": ("pred_pre", num),
    **{name: (field, num) for name, field in INVESTORS.items()},
}

DEFAULT_DAYS = 20
MAX_DAYS = 250


def summarize_flow(rows: list[dict[str, Any]]) -> dict[str, Any]:
    """Per investor group: total net buying and the number of net-buying days. Pure."""
    summary: dict[str, Any] = {"days": len(rows)}
    if rows:
        summary["from"] = rows[0].get("date")
        summary["to"] = rows[-1].get("date")
    for name in INVESTORS:
        values = [row[name] for row in rows if isinstance(row.get(name), (int, float))]
        if values:
            summary[name] = {
                "net_total": sum(values),
                "buy_days": sum(1 for v in values if v > 0),
                "sell_days": sum(1 for v in values if v < 0),
            }
    return summary


async def investor_flow(
    api: Any, stock: Any, *, days: Any = None, unit: str = "amount", end_date: Any = None
) -> dict[str, Any]:
    unit = str(unit or "amount").strip().lower()
    if unit not in UNITS:
        raise ValueError(f"unit 은 {', '.join(UNITS)} 중 하나여야 합니다: {unit!r}")
    want = row_count(days, default=DEFAULT_DAYS, maximum=MAX_DAYS)
    resolved = await resolve_stock(api, stock)
    amt_qty_tp, unit_label = UNITS[unit]
    params = {
        "dt": date_arg(end_date, "end_date") or today_kst(),
        "stk_cd": resolved.code,
        "amt_qty_tp": amt_qty_tp,
        "trde_tp": "0",
        "unit_tp": "1",
    }
    _first, records = await fetch_rows(
        api.stock_info.investor_institution_by_stock, KEY, params, want=want
    )
    rows = [pick(r, _ROW_FIELDS) for r in records if str(r.get("dt") or "").strip()]
    rows = sorted(rows, key=lambda r: r.get("date") or "")[-want:]
    return {
        "stock": resolved.as_dict(),
        "unit": unit_label,
        "source": SOURCE,
        "summary": summarize_flow(rows),
        "rows": rows,
    }


@register
def flow_tools(_context: IntentContext) -> list[LocalTool]:
    async def handler(api: Any, arguments: dict[str, Any]) -> dict[str, Any]:
        return await investor_flow(
            api,
            arguments.get("stock"),
            days=arguments.get("days"),
            unit=str(arguments.get("unit") or "amount"),
            end_date=arguments.get("end_date"),
        )

    return [
        read_only_tool(
            name="investor_flow",
            title="투자자별 순매수 (외국인·기관·개인)",
            description=(
                "종목 하나의 일별 투자자별 순매수(개인·외국인·기관계와 금융투자·투신·연기금 "
                "등 세부)를 날짜 오름차순으로, 기간 합계·순매수일 수 요약과 함께 돌려준다"
                "(ka10059). '외국인이 사고 있어?' 같은 수급 질문에 쓴다. 금액 단위 백만원"
                "(unit=quantity 면 주)."
            ),
            properties={
                "stock": stock_schema(),
                "days": {**count_schema(DEFAULT_DAYS, MAX_DAYS), "description": "거래일 수"},
                "unit": {
                    "type": "string",
                    "enum": list(UNITS),
                    "default": "amount",
                    "description": "amount 금액(백만원), quantity 수량(주)",
                },
                "end_date": {
                    "type": "string",
                    "description": "이 날짜까지(YYYY-MM-DD). 생략하면 오늘",
                },
            },
            required=("stock",),
            toolset="stock_info",
            handler=handler,
            example={"stock": "삼성전자", "days": 20},
        )
    ]
