"""``kiwoom`` — read-only command line for quick lookups.

::

    kiwoom quote 005930              # 현재가·등락률·거래량
    kiwoom quote 삼성전자 --mock     # 이름도 된다 (ka10099 로 코드 찾기)
    kiwoom chart 005930 --daily -n 10
    kiwoom chart 005930 --minute 5
    kiwoom balance                   # 계좌평가잔고 (kt00018)
    kiwoom find 하이닉스
    kiwoom endpoints 체결            # 어떤 메서드가 어떤 TR 인지 (키 필요 없음)
    kiwoom --json quote 005930       # 원 응답 JSON

Credentials come from ``KIWOOM_APP_KEY`` / ``KIWOOM_APP_SECRET`` /
``KIWOOM_IS_MOCK`` (see :meth:`KiwoomAPI.from_env`), optionally from
``--env-file``. ``--mock`` / ``--live`` override ``KIWOOM_IS_MOCK``.

There is deliberately **no order command** and nothing that revokes a token:
every subcommand is a query. Orders belong in code you can review.
"""

from __future__ import annotations

import argparse
import json
import logging
import re
import sys
from collections.abc import Callable, Sequence
from datetime import date
from typing import Any

import httpx

from kiwoom_client._errors import KiwoomError
from kiwoom_client.parsing import _unsigned_number, extract_records

__all__ = ["main"]

_CODE = re.compile(r"^(?=.*\d)[0-9A-Z]{6}(?:_NX|_AL)?$")

_CHART_KINDS = {
    "daily": "stock_daily_chart",
    "weekly": "stock_weekly_chart",
    "monthly": "stock_monthly_chart",
    "yearly": "stock_yearly_chart",
    "minute": "stock_minute_chart",
    "tick": "stock_tick_chart",
}


def _signed(value: Any) -> int | float | None:
    """Kiwoom numeric string -> number, keeping the sign (zero padding ok)."""
    if value is None:
        return None
    text = str(value).strip().replace(",", "")
    if not text or text in "+-":
        return None
    try:
        return int(text)
    except ValueError:
        try:
            return float(text)
        except ValueError:
            return None


def _fmt(value: Any, signed: bool = False) -> str:
    if value is None:
        return "-"
    if isinstance(value, float):
        return f"{value:+,.2f}" if signed else f"{value:,.2f}"
    if isinstance(value, int):
        return f"{value:+,}" if signed else f"{value:,}"
    return str(value)


_NUMERIC_CELL = re.compile(r"^(?:[+-]?[\d,]+(?:\.\d+)?%?|-)$")


def _table(headers: Sequence[str], rows: Sequence[Sequence[str]]) -> str:
    """Plain-text table: numeric columns right-aligned, text left-aligned."""
    widths = [max(len(h), *(len(r[i]) for r in rows)) if rows else len(h)
              for i, h in enumerate(headers)]
    numeric = [bool(rows) and all(_NUMERIC_CELL.match(r[i]) for r in rows)
               for i in range(len(headers))]

    def line(cells: Sequence[str]) -> str:
        return "  ".join(
            c.rjust(w) if num else c.ljust(w)
            for c, w, num in zip(cells, widths, numeric, strict=True)
        ).rstrip()

    return "\n".join([line(headers), *(line(row) for row in rows)])


def _print_json(data: Any) -> None:
    print(json.dumps(data, ensure_ascii=False, indent=2))


def _open_api(args: argparse.Namespace) -> Any:
    from kiwoom_client import KiwoomAPI

    is_mock: bool | None = None
    if getattr(args, "mock", False):
        is_mock = True
    elif getattr(args, "live", False):
        is_mock = False
    return KiwoomAPI.from_env(getattr(args, "env_file", None), is_mock=is_mock)


def _resolve_code(api: Any, text: str) -> str:
    """A stock code as typed, or the code of the stock with that exact name."""
    candidate = text.strip().upper()
    if _CODE.match(candidate):
        return candidate
    return str(api.stock_code(text))


# --- subcommands -------------------------------------------------------------


def _cmd_quote(api: Any, args: argparse.Namespace) -> None:
    code = _resolve_code(api, args.stock)
    data = api.stock_info.basic_stock_info(stk_cd=code)
    if args.json:
        _print_json(data)
        return
    price = _unsigned_number(data.get("cur_prc"))
    print(f"{data.get('stk_nm', '?')} ({data.get('stk_cd', code)})")
    print(f"  현재가  {_fmt(price)}  ({_fmt(_signed(data.get('flu_rt')), signed=True)}%)")
    print(
        "  시/고/저  "
        + " / ".join(_fmt(_unsigned_number(data.get(k))) for k in ("open_pric", "high_pric",
                                                                    "low_pric"))
    )
    print(f"  거래량  {_fmt(_signed(data.get('trde_qty')))}")


def _today() -> str:
    return date.today().strftime("%Y%m%d")


def _cmd_chart(api: Any, args: argparse.Namespace) -> None:
    code = _resolve_code(api, args.stock)
    kind = args.kind or "daily"
    params: dict[str, Any] = {"stk_cd": code, "upd_stkpc_tp": "0" if args.raw_price else "1"}
    if kind in ("minute", "tick"):
        params["tic_scope"] = str(args.scope)
        if kind == "minute" and args.date:
            params["base_dt"] = args.date
    else:
        params["base_dt"] = args.date or _today()
    data = getattr(api.chart, _CHART_KINDS[kind])(**params)
    if args.json:
        _print_json(data)
        return
    _, records = extract_records(data)
    records = list(reversed(records[: args.n]))  # Kiwoom sends newest first
    time_key = "cntr_tm" if kind in ("minute", "tick") else "dt"
    rows = [
        [str(r.get(time_key, ""))]
        + [_fmt(_unsigned_number(r.get(k)))
           for k in ("open_pric", "high_pric", "low_pric", "cur_prc", "trde_qty")]
        for r in records
    ]
    print(f"{code} {kind}")
    print(_table(["time" if time_key == "cntr_tm" else "date",
                  "open", "high", "low", "close", "volume"], rows))


def _cmd_balance(api: Any, args: argparse.Namespace) -> None:
    data = api.account.evaluation_balance_detail(qry_tp="1", dmst_stex_tp=args.exchange)
    if args.json:
        _print_json(data)
        return
    totals = [
        ("총매입", "tot_pur_amt"), ("총평가", "tot_evlt_amt"), ("평가손익", "tot_evlt_pl"),
        ("추정예탁자산", "prsm_dpst_aset_amt"),
    ]
    for label, key in totals:
        print(f"  {label}  {_fmt(_signed(data.get(key)), signed=key == 'tot_evlt_pl')}")
    print(f"  수익률  {_fmt(_signed(data.get('tot_prft_rt')), signed=True)}%")
    holdings = [h for h in data.get("acnt_evlt_remn_indv_tot") or [] if isinstance(h, dict)]
    if not holdings:
        print("  (보유 종목 없음)")
        return
    rows = [
        [
            str(h.get("stk_cd", "")).lstrip("AJQ"),
            str(h.get("stk_nm", "")),
            _fmt(_signed(h.get("rmnd_qty"))),
            _fmt(_signed(h.get("pur_pric"))),
            _fmt(_signed(h.get("cur_prc"))),
            _fmt(_signed(h.get("evltv_prft")), signed=True),
            _fmt(_signed(h.get("prft_rt")), signed=True),
        ]
        for h in holdings
    ]
    print(_table(["code", "name", "qty", "avg", "price", "P/L", "%"], rows))


def _cmd_find(api: Any, args: argparse.Namespace) -> None:
    hits = api.find_stock(args.query, limit=args.n)
    if args.json:
        _print_json(hits)
        return
    if not hits:
        print(f"'{args.query}' 와 맞는 종목이 없습니다.")
        return
    print(_table(["code", "name", "market"],
                 [[str(h.get("code", "")), str(h.get("name", "")),
                   str(h.get("marketName", ""))] for h in hits]))


def _cmd_endpoints(args: argparse.Namespace) -> None:
    from kiwoom_client import spec

    query = (args.query or "").strip().lower()
    rows = []
    for (module, method), api_id in sorted(spec.endpoint_index().items()):
        try:
            name = spec.get(api_id).name
        except KeyError:
            name = ""
        haystack = f"{api_id} {module}.{method} {name}".lower()
        if query and query not in haystack:
            continue
        rows.append({"api_id": api_id, "method": f"api.{module}.{method}", "name": name})
    if args.json:
        _print_json(rows)
        return
    if not rows:
        print(f"'{args.query}' 와 맞는 엔드포인트가 없습니다.")
        return
    print(_table(["api_id", "method", "name"],
                 [[r["api_id"], r["method"], r["name"]] for r in rows]))


# --- parser ------------------------------------------------------------------


def _common(suppress: bool) -> argparse.ArgumentParser:
    """Global options, accepted before or after the subcommand."""
    default: Any = argparse.SUPPRESS if suppress else None
    flag_default: Any = argparse.SUPPRESS if suppress else False
    common = argparse.ArgumentParser(add_help=False)
    server = common.add_mutually_exclusive_group()
    server.add_argument("--mock", action="store_true", default=flag_default,
                        help="모의투자 서버 (KIWOOM_IS_MOCK 무시)")
    server.add_argument("--live", action="store_true", default=flag_default,
                        help="실전투자 서버 (KIWOOM_IS_MOCK 무시)")
    common.add_argument("--env-file", metavar="PATH", default=default,
                        help=".env 파일 경로 (환경변수가 우선)")
    common.add_argument("--json", action="store_true", default=flag_default,
                        help="가공하지 않은 응답 JSON 출력")
    common.add_argument("-v", "--verbose", action="store_true", default=flag_default,
                        help="DEBUG 로그 (요청 추적)")
    return common


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="kiwoom",
        description="키움 REST API 조회용 CLI (주문 기능 없음). "
                    "키: KIWOOM_APP_KEY / KIWOOM_APP_SECRET / KIWOOM_IS_MOCK",
        parents=[_common(suppress=False)],
    )
    sub = parser.add_subparsers(dest="command", required=True, metavar="COMMAND")
    common = [_common(suppress=True)]

    p = sub.add_parser("quote", parents=common, help="현재가 (ka10001)")
    p.add_argument("stock", help="종목코드(005930) 또는 정확한 종목명")

    p = sub.add_parser("chart", parents=common, help="차트 (일·주·월·년·분·틱)")
    p.add_argument("stock", help="종목코드 또는 정확한 종목명")
    kinds = p.add_mutually_exclusive_group()
    for kind in ("daily", "weekly", "monthly", "yearly"):
        kinds.add_argument(f"--{kind}", dest="kind", action="store_const", const=kind)
    kinds.add_argument("--minute", dest="kind", action="store_const", const="minute",
                       help="분봉 (--scope 분, 기본 1)")
    kinds.add_argument("--tick", dest="kind", action="store_const", const="tick",
                       help="틱봉 (--scope 틱, 기본 1)")
    p.add_argument("--scope", type=int, default=1, help="분·틱 범위 (1,3,5,10,...)")
    p.add_argument("--date", metavar="YYYYMMDD", help="기준일 (기본: 오늘)")
    p.add_argument("-n", type=int, default=20, help="표시할 봉 수 (기본 20)")
    p.add_argument("--raw-price", action="store_true", help="수정주가 미적용")

    p = sub.add_parser("balance", parents=common, help="계좌평가잔고 (kt00018)")
    p.add_argument("--exchange", choices=["KRX", "NXT"], default="KRX")

    p = sub.add_parser("find", parents=common, help="종목 검색 (ka10099)")
    p.add_argument("query", help="종목명 일부 또는 코드")
    p.add_argument("-n", type=int, default=10, help="최대 결과 수")

    p = sub.add_parser("endpoints", parents=common, help="메서드 ↔ TR 목록 검색 (키 불필요)")
    p.add_argument("query", nargs="?", help="api_id·메서드·TR 이름 일부")
    return parser


_COMMANDS: dict[str, Callable[[Any, argparse.Namespace], None]] = {
    "quote": _cmd_quote,
    "chart": _cmd_chart,
    "balance": _cmd_balance,
    "find": _cmd_find,
}


def main(argv: Sequence[str] | None = None) -> int:
    """Entry point of the ``kiwoom`` script. Returns the exit status."""
    args = build_parser().parse_args(argv)
    if args.verbose:
        logging.basicConfig(level=logging.DEBUG, format="%(levelname)s %(name)s %(message)s")
    try:
        if args.command == "endpoints":
            _cmd_endpoints(args)
            return 0
        with _open_api(args) as api:
            _COMMANDS[args.command](api, args)
        return 0
    except (KiwoomError, LookupError, ValueError, OSError, httpx.HTTPError) as exc:
        print(f"kiwoom: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":  # pragma: no cover
    sys.exit(main())
