"""``get_orders`` and ``get_buying_power`` — the account's orders and how much it can buy.

- open orders today:   ka10075 미체결요청
- filled orders today: ka10076 체결요청
- either, another day: kt00007 계좌별주문체결내역상세요청 (``date``)
- buying power:        kt00011 증거금율별주문가능수량조회 (with ``stock``) or
  kt00001 예수금상세현황 (추정조회) for the account as a whole

Lookups only. Open orders carry ``cancel_preview_args`` — arguments for
``order_preview`` (action=cancel), which shows the cancel and issues the
confirmation token; nothing here sends a cancel.
"""

from __future__ import annotations

from typing import Any

from kiwoom_client.mcp.intents.common import date_arg, fetch_rows, today_kst
from kiwoom_client.mcp.intents.limits import count_schema, row_count
from kiwoom_client.mcp.intents.normalize import date, num, pct, pick, price, stock_code, text
from kiwoom_client.mcp.intents.registry import IntentContext, read_only_tool, register
from kiwoom_client.mcp.intents.resolve import resolve_stock, stock_schema
from kiwoom_client.mcp.local_tools import LocalTool

STATUSES = ("open", "filled")
DEFAULT_ROWS = 50
MAX_ROWS = 200


def _order_no(value: Any) -> str | None:
    """Original order numbers are ``"0000000"`` when there is none."""
    number = text(value)
    return None if number is None or set(number) == {"0"} else number


_OPEN_FIELDS: dict[str, tuple[str, Any]] = {
    "order_no": ("ord_no", text),
    "code": ("stk_cd", stock_code),
    "name": ("stk_nm", text),
    "order_kind": ("io_tp_nm", text),
    "trade_type": ("trde_tp", text),
    "status": ("ord_stt", text),
    "qty": ("ord_qty", price),
    "price": ("ord_pric", price),
    "open_qty": ("oso_qty", price),
    "filled_qty": ("cntr_qty", price),
    "filled_price": ("cntr_pric", price),
    "current_price": ("cur_prc", price),
    "time": ("tm", date),
    "original_order_no": ("orig_ord_no", _order_no),
    "exchange": ("stex_tp_txt", text),
}

_FILLED_FIELDS: dict[str, tuple[str, Any]] = {
    "order_no": ("ord_no", text),
    "code": ("stk_cd", stock_code),
    "name": ("stk_nm", text),
    "order_kind": ("io_tp_nm", text),
    "trade_type": ("trde_tp", text),
    "status": ("ord_stt", text),
    "qty": ("ord_qty", price),
    "price": ("ord_pric", price),
    "filled_qty": ("cntr_qty", price),
    "filled_price": ("cntr_pric", price),
    "open_qty": ("oso_qty", price),
    "fee": ("tdy_trde_cmsn", num),
    "tax": ("tdy_trde_tax", num),
    "time": ("ord_tm", date),
    "original_order_no": ("orig_ord_no", _order_no),
    "exchange": ("stex_tp_txt", text),
}

_HISTORY_FIELDS: dict[str, tuple[str, Any]] = {
    "order_no": ("ord_no", text),
    "code": ("stk_cd", stock_code),
    "name": ("stk_nm", text),
    "order_kind": ("io_tp_nm", text),
    "trade_type": ("trde_tp", text),
    "qty": ("ord_qty", price),
    "price": ("ord_uv", price),
    "filled_qty": ("cntr_qty", price),
    "filled_price": ("cntr_uv", price),
    "open_qty": ("ord_remnq", price),
    "time": ("ord_tm", date),
    "original_order_no": ("ori_ord", _order_no),
    "modify_cancel": ("mdfy_cncl", text),
    "accepted": ("acpt_tp", text),
    "exchange": ("dmst_stex_tp", text),
}

#: (method, source, list key, fields)
_TODAY = {
    "open": ("unfilled_orders", "ka10075 미체결요청", "oso", _OPEN_FIELDS),
    "filled": ("filled_orders", "ka10076 체결요청", "cntr", _FILLED_FIELDS),
}
_HISTORY = (
    "order_execution_detail",
    "kt00007 계좌별주문체결내역상세요청",
    "acnt_ord_cntr_prps_dtl",
)


def _side(kind: Any) -> str | None:
    label = str(kind or "")
    if "매수" in label:
        return "buy"
    if "매도" in label:
        return "sell"
    return None


def _cancel_exchange(record: dict[str, Any]) -> str | None:
    if str(record.get("sor_yn") or "").strip().upper() == "Y":
        return "SOR"
    exchange = str(record.get("stex_tp_txt") or "").strip().upper()
    return exchange if exchange in ("KRX", "NXT") else None


def _order_row(
    record: dict[str, Any], fields: dict[str, tuple[str, Any]], *, open_: bool
) -> dict[str, Any]:
    row = pick(record, fields)
    row["side"] = _side(row.get("order_kind"))
    if open_ and row.get("order_no") and row.get("code") and (row.get("open_qty") or 0) > 0:
        args: dict[str, Any] = {
            "action": "cancel",
            "stock": row["code"],
            "order_no": row["order_no"],
            "qty": "all",
        }
        exchange = _cancel_exchange(record)
        if exchange:
            args["dmst_stex_tp"] = exchange
        row["cancel_preview_args"] = args
    return row


async def get_orders(
    api: Any,
    *,
    status: str = "open",
    date_value: Any = None,
    stock: Any = None,
    count: Any = None,
) -> dict[str, Any]:
    status = str(status or "open").strip().lower()
    if status not in STATUSES:
        raise ValueError(f"status 는 {', '.join(STATUSES)} 중 하나여야 합니다: {status!r}")
    want = row_count(count, default=DEFAULT_ROWS, maximum=MAX_ROWS)
    code = (await resolve_stock(api, stock)).code if str(stock or "").strip() else ""
    day = date_arg(date_value, "date")
    if day and day != today_kst():
        method_name, source, key = _HISTORY
        params = {
            "ord_dt": day,
            "qry_tp": "3" if status == "open" else "4",
            "stk_bond_tp": "1",
            "sell_tp": "0",
            "stk_cd": code,
            "fr_ord_no": "",
            "dmst_stex_tp": "%",
        }
        fields = _HISTORY_FIELDS
    else:
        method_name, source, key, fields = _TODAY[status]
        if status == "open":
            params = {"all_stk_tp": "1" if code else "0", "trde_tp": "0", "stex_tp": "0"}
        else:
            params = {"qry_tp": "1" if code else "0", "sell_tp": "0", "stex_tp": "0"}
        if code:
            params["stk_cd"] = code
    method = getattr(api.account, method_name)
    _first, records = await fetch_rows(method, key, params, want=want)
    rows = [_order_row(r, fields, open_=status == "open") for r in records[:want]]
    return {
        "status": status,
        "date": date(day) if day else None,
        "source": source,
        "count": len(rows),
        "orders": rows,
    }


#: margin-rate table fields of kt00011 (rate → amount, qty).
_MARGIN_RATES = ("20", "30", "40", "50", "60", "100")

_ACCOUNT_CASH_FIELDS: dict[str, tuple[str, Any]] = {
    "deposit": ("entr", num),
    "d1_estimated_deposit": ("d1_entra", num),
    "d2_estimated_deposit": ("d2_entra", num),
    "orderable_amount": ("ord_alow_amt", num),
    "withdrawable_amount": ("pymn_alow_amt", num),
    "unpaid_cash_total": ("ch_uncla_tot", num),
}


async def get_buying_power(
    api: Any, *, stock: Any = None, price_value: Any = None
) -> dict[str, Any]:
    if not str(stock or "").strip():
        resp = await api.account.deposit_detail(qry_tp="3")
        amounts = {
            rate: num(resp.get(f"{rate}stk_ord_alow_amt"))
            for rate in ("20", "30", "40", "100")
            if f"{rate}stk_ord_alow_amt" in resp
        }
        return {
            "source": "kt00001 예수금상세현황요청 (추정조회)",
            "unit": "krw",
            **pick(resp, _ACCOUNT_CASH_FIELDS),
            "orderable_amount_by_stock_margin_rate": amounts,
        }

    resolved = await resolve_stock(api, stock)
    params = {"stk_cd": resolved.code}
    if price_value not in (None, ""):
        amount = num(price_value)
        if amount is None or amount <= 0:
            raise ValueError(f"price 는 양수여야 합니다: {price_value!r}")
        params["uv"] = str(int(amount))
    resp = await api.account.orderable_qty_by_margin(**params)
    by_rate: dict[str, dict[str, Any]] = {
        rate: {
            "amount": num(resp.get(f"profa_{rate}ord_alow_amt")),
            "qty": num(resp.get(f"profa_{rate}ord_alowq")),
        }
        for rate in _MARGIN_RATES
        if f"profa_{rate}ord_alowq" in resp
    }
    applied = pct(resp.get("aplc_rt"))
    applied_key = str(int(applied)) if applied is not None and applied.is_integer() else None
    out: dict[str, Any] = {
        "stock": resolved.as_dict(),
        "price": num(params.get("uv")),
        "source": "kt00011 증거금율별주문가능수량조회요청",
        "unit": "krw",
        "applied_margin_rate_pct": applied,
        "stock_margin_rate_pct": pct(resp.get("stk_profa_rt")),
        "account_margin_rate_pct": pct(resp.get("profa_rt")),
        "orderable": by_rate.get(applied_key or ""),
        "cash_only": {
            "amount": num(resp.get("min_ord_alow_amt")),
            "qty": num(resp.get("min_ord_alowq")),
        },
        "deposit": num(resp.get("entr")),
        "orderable_cash": num(resp.get("ord_alowa")),
        "by_margin_rate": by_rate,
    }
    return out


@register
def order_tools(_context: IntentContext) -> list[LocalTool]:
    async def on_orders(api: Any, arguments: dict[str, Any]) -> dict[str, Any]:
        return await get_orders(
            api,
            status=str(arguments.get("status") or "open"),
            date_value=arguments.get("date"),
            stock=arguments.get("stock"),
            count=arguments.get("count"),
        )

    async def on_power(api: Any, arguments: dict[str, Any]) -> dict[str, Any]:
        return await get_buying_power(
            api, stock=arguments.get("stock"), price_value=arguments.get("price")
        )

    return [
        read_only_tool(
            name="get_orders",
            title="주문 목록 (미체결·체결)",
            description=(
                "계좌의 미체결(open) 또는 체결(filled) 주문을 주문번호·종목·매수/매도·수량·단가·"
                "체결량·미체결량·시간과 함께 돌려준다(오늘: ka10075/ka10076, 다른 날: kt00007). "
                "'미체결 있어?', '오늘 뭐 체결됐어?'에 쓴다. 미체결 행의 cancel_preview_args 를 "
                "order_preview 에 넘기면 취소 미리보기가 된다(이 도구는 취소하지 않는다)."
            ),
            properties={
                "status": {"type": "string", "enum": list(STATUSES), "default": "open"},
                "date": {"type": "string", "description": "주문일(YYYY-MM-DD). 생략하면 오늘"},
                "stock": stock_schema("이 종목만 (종목명 또는 코드). 생략하면 전체"),
                "count": count_schema(DEFAULT_ROWS, MAX_ROWS),
            },
            toolset="account",
            handler=on_orders,
            example={"status": "open"},
        ),
        read_only_tool(
            name="get_buying_power",
            title="주문가능금액·수량",
            description=(
                "stock 을 주면 그 종목을 price(생략 시 현재가 기준)에 살 수 있는 수량·금액을 "
                "증거금률별로, 현금만으로(미수 불가) 살 수 있는 수량과 함께 돌려준다(kt00011). "
                "stock 을 빼면 계좌의 예수금·D+1/D+2 추정예수금·주문가능금액·출금가능금액"
                "(kt00001 추정조회). '삼성전자 몇 주 살 수 있어?'에 쓴다. 금액 단위 원."
            ),
            properties={
                "stock": stock_schema("종목명 또는 코드. 생략하면 계좌 전체 주문가능금액"),
                "price": {"type": "number", "description": "매수 단가(원). 생략하면 현재가"},
            },
            toolset="account",
            handler=on_power,
            example={"stock": "삼성전자", "price": 70000},
        ),
    ]
