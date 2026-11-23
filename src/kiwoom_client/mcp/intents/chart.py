"""``get_chart`` — a stock's OHLCV candles plus a short summary, in one call.

Day/week/month/minute charts (ka10081/ka10082/ka10083/ka10080), followed
across continuation pages until ``count`` candles are in, parsed with the
same field rules as :func:`kiwoom_client.to_ohlcv` (:func:`~kiwoom_client.ohlcv_rows`).
"""

from __future__ import annotations

from statistics import fmean
from typing import Any

from kiwoom_client.mcp.intents.common import date_arg, fetch_rows, today_kst
from kiwoom_client.mcp.intents.limits import count_schema, row_count
from kiwoom_client.mcp.intents.registry import IntentContext, read_only_tool, register
from kiwoom_client.mcp.intents.resolve import resolve_stock, stock_schema
from kiwoom_client.mcp.local_tools import LocalTool
from kiwoom_client.parsing import ohlcv_rows

#: period → (chart method, source label, response list key)
PERIODS: dict[str, tuple[str, str, str]] = {
    "day": ("stock_daily_chart", "ka10081 주식일봉차트조회요청", "stk_dt_pole_chart_qry"),
    "week": ("stock_weekly_chart", "ka10082 주식주봉차트조회요청", "stk_stk_pole_chart_qry"),
    "month": ("stock_monthly_chart", "ka10083 주식월봉차트조회요청", "stk_mth_pole_chart_qry"),
    "minute": ("stock_minute_chart", "ka10080 주식분봉차트조회요청", "stk_min_pole_chart_qry"),
}

#: ka10080 tic_scope values (minutes).
MINUTE_INTERVALS: tuple[int, ...] = (1, 3, 5, 10, 15, 30, 45, 60)

DEFAULT_COUNT = 60
MAX_COUNT = 500


def _mean(values: list[float], last: int) -> float | None:
    return round(fmean(values[-last:]), 2) if len(values) >= last else None


def summarize(rows: list[dict[str, Any]]) -> dict[str, Any]:
    """Period return, range, average volume and simple moving averages. Pure."""
    if not rows:
        return {"rows": 0}
    time_key = "date" if "date" in rows[0] else "datetime"
    closes = [r["close"] for r in rows if r.get("close") is not None]
    highs = [r["high"] for r in rows if r.get("high") is not None]
    lows = [r["low"] for r in rows if r.get("low") is not None]
    volumes = [r["volume"] for r in rows if r.get("volume") is not None]
    summary: dict[str, Any] = {
        "rows": len(rows),
        "first": rows[0][time_key],
        "last": rows[-1][time_key],
        "last_close": closes[-1] if closes else None,
        "period_return_pct": (
            round((closes[-1] / closes[0] - 1) * 100, 2) if closes and closes[0] else None
        ),
        "high": max(highs) if highs else None,
        "low": min(lows) if lows else None,
        "avg_volume": round(fmean(volumes)) if volumes else None,
        "sma5": _mean(closes, 5),
        "sma20": _mean(closes, 20),
    }
    return summary


async def get_chart(
    api: Any,
    stock: Any,
    *,
    period: str = "day",
    interval: Any = None,
    count: Any = None,
    adjusted: bool = True,
    end_date: Any = None,
) -> dict[str, Any]:
    period = str(period or "day").strip().lower()
    if period not in PERIODS:
        raise ValueError(f"period 는 {', '.join(PERIODS)} 중 하나여야 합니다: {period!r}")
    want = row_count(count, default=DEFAULT_COUNT, maximum=MAX_COUNT)
    resolved = await resolve_stock(api, stock)
    method_name, source, key = PERIODS[period]
    params: dict[str, Any] = {"stk_cd": resolved.code, "upd_stkpc_tp": "1" if adjusted else "0"}
    base_dt = date_arg(end_date, "end_date")
    out: dict[str, Any] = {"stock": resolved.as_dict(), "period": period}
    if period == "minute":
        minutes = int(interval) if interval not in (None, "") else 1
        if minutes not in MINUTE_INTERVALS:
            raise ValueError(
                f"interval(분) 은 {', '.join(map(str, MINUTE_INTERVALS))} 중 하나여야 합니다"
            )
        params["tic_scope"] = str(minutes)
        if base_dt:
            params["base_dt"] = base_dt
        out["interval_minutes"] = minutes
    else:
        params["base_dt"] = base_dt or today_kst()
    out.update({"adjusted": bool(adjusted), "source": source})

    method = getattr(api.chart, method_name)
    _first, records = await fetch_rows(method, key, params, want=want)
    # A trailing record without a time stamp would make the widths mixed.
    records = [r for r in records if str(r.get("dt") or r.get("cntr_tm") or "").strip()]
    rows = ohlcv_rows(records)[-want:]
    out["summary"] = summarize(rows)
    out["rows"] = rows
    return out


def _bool(value: Any, default: bool) -> bool:
    if value is None:
        return default
    if isinstance(value, str):
        return value.strip().lower() not in ("false", "0", "no", "n", "")
    return bool(value)


@register
def chart_tools(_context: IntentContext) -> list[LocalTool]:
    async def handler(api: Any, arguments: dict[str, Any]) -> dict[str, Any]:
        return await get_chart(
            api,
            arguments.get("stock"),
            period=str(arguments.get("period") or "day"),
            interval=arguments.get("interval"),
            count=arguments.get("count"),
            adjusted=_bool(arguments.get("adjusted"), True),
            end_date=arguments.get("end_date"),
        )

    return [
        read_only_tool(
            name="get_chart",
            title="종목 차트 (일·주·월·분봉) + 요약",
            description=(
                "종목 하나의 봉차트(시가·고가·저가·종가·거래량, 날짜 오름차순)와 요약(기간 수익률·"
                "고저·평균 거래량·5/20 이동평균·마지막 종가)을 한 번에 돌려준다. 추세·이동평균·"
                "기간 수익률을 물을 때 쓴다. 연속조회로 count 개까지 채운다."
            ),
            example={"stock": "삼성전자", "period": "day", "count": 60},
            properties={
                "stock": stock_schema(),
                "period": {
                    "type": "string",
                    "enum": list(PERIODS),
                    "default": "day",
                    "description": "day 일봉, week 주봉, month 월봉, minute 분봉",
                },
                "interval": {
                    "type": "integer",
                    "enum": list(MINUTE_INTERVALS),
                    "default": 1,
                    "description": "분봉 간격(분). period=minute 일 때만",
                },
                "count": count_schema(DEFAULT_COUNT, MAX_COUNT),
                "adjusted": {
                    "type": "boolean",
                    "default": True,
                    "description": "수정주가 적용 (액면분할 등 반영)",
                },
                "end_date": {
                    "type": "string",
                    "description": "이 날짜까지(YYYY-MM-DD). 생략하면 오늘",
                },
            },
            required=("stock",),
            toolset="chart",
            handler=handler,
        )
    ]
