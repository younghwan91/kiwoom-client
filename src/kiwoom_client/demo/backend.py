"""A fake Kiwoom REST server that runs inside the process (``httpx.MockTransport``).

:class:`DemoBackend` answers the same HTTP requests the real server gets —
``POST /oauth2/token``, ``POST /api/dostk/...`` with an ``api-id`` header —
so the client code above it (token handling, paging, parsing, MCP tools)
runs unchanged. Nothing leaves the process.

Responses follow the TR catalog (:mod:`kiwoom_client.spec`): every response
field the catalog lists for a TR is present. The TRs the intent tools and
the CLI use get coherent synthetic values (:mod:`.market`, :mod:`.paper`);
any other REST TR gets plausible filler shaped by the catalog, so a raw
``call_tool`` still returns the right keys. Every response carries
``"_demo"`` (:data:`DEMO_NOTICE`).
"""

from __future__ import annotations

import json
import threading
import zlib
from collections.abc import Callable, Iterable, Mapping
from datetime import datetime, timedelta
from typing import Any

import httpx

from kiwoom_client import spec
from kiwoom_client.demo.market import (
    BY_CODE,
    KST,
    MARKET_NAMES,
    UNIVERSE,
    Bar,
    DemoStock,
    Market,
    aggregate,
    business_days,
)
from kiwoom_client.demo.paper import (
    ACCOUNT_NO,
    TRADE_TYPE_NAMES,
    OrderRefused,
    PaperAccount,
    PaperBook,
    PaperOrder,
    commission,
    sell_tax,
)
from kiwoom_client.tick_size import tick_size

#: Key and text of the marker every demo response carries.
DEMO_KEY = "_demo"
DEMO_NOTICE = "가상 데이터 — 실제 시세·계좌가 아닙니다"

#: Base URL demo clients point at. ``.invalid`` never resolves (RFC 6761), and
#: the transport answers before any connection would be attempted anyway.
DEMO_BASE_URL = "https://demo.kiwoom-client.invalid"

OK_MSG = "정상적으로 처리되었습니다 (데모)"
ORDER_MSG = "주문이 접수되었습니다 (데모 — 메모리 안의 가상 주문, 키움에 전송하지 않음)"

#: Rows per page for long lists, so continuation (cont-yn/next-key) is exercised.
CHART_PAGE = 300
MINUTE_PAGE = 900

#: Order TRs. Paper trading (:class:`~.paper.PaperBook`) handles the cash ones;
#: credit and gold-spot orders are refused.
ORDER_API_IDS = frozenset({
    "kt10000", "kt10001", "kt10002", "kt10003",  # 주식 매수·매도·정정·취소
    "kt10006", "kt10007", "kt10008", "kt10009",  # 신용
    "kt50000", "kt50001", "kt50002", "kt50003",  # 금현물
})  # fmt: skip

Handler = Callable[[dict[str, Any], str], tuple[dict[str, Any], str]]


# --- formatting (Kiwoom sends every value as a string) -----------------------


def signed(value: float) -> str:
    """``+1200`` / ``-1200`` / ``0``."""
    number = int(value)
    return f"{number:+d}" if number else "0"


def directed(price: int, change: float) -> str:
    """A price carrying the direction of the move, as Kiwoom sends ``cur_prc``."""
    return f"+{price}" if change > 0 else f"-{price}" if change < 0 else str(price)


def rate(value: float) -> str:
    return f"{value:+.2f}" if value else "0.00"


def sign_code(change: float) -> str:
    """전일대비기호: 2 상승, 3 보합, 5 하락."""
    return "2" if change > 0 else "5" if change < 0 else "3"


def _hash(*parts: object) -> int:
    return zlib.crc32(":".join(map(str, parts)).encode())


class DemoRefusal(Exception):
    """A request the demo server answers with a non-zero ``return_code``."""


class DemoBackend:
    """In-memory fake of the Kiwoom REST server.

    Args:
        seed: Fixes every synthetic price; the same seed gives the same data.
        today: Pretend it is this day (tests); default today in Korea.

    The paper account (:attr:`account`) lives as long as the backend, so one
    backend shared by a sync and an async client sees the same balance.
    """

    def __init__(self, seed: int | None = None, today: Any = None) -> None:
        from kiwoom_client.demo.market import DEFAULT_SEED

        self.market = Market(DEFAULT_SEED if seed is None else seed, today)
        self.account = PaperAccount()
        self.book = PaperBook(self.account)
        self.requests: list[str] = []
        self._lock = threading.Lock()
        self._handlers: dict[str, Handler] = {
            "ka10099": self._stock_list,
            "ka10001": self._basic_info,
            "ka10095": self._watchlist,
            "ka10081": self._chart("day"),
            "ka10082": self._chart("week"),
            "ka10083": self._chart("month"),
            "ka10094": self._chart("year"),
            "ka10080": self._minute_chart,
            "ka10030": self._top_volume,
            "ka10027": self._top_change,
            "ka10032": self._top_value,
            "ka10023": self._volume_spike,
            "ka10059": self._investor_flow,
            "ka00001": self._account_no,
            "kt00001": self._deposit,
            "kt00011": self._orderable_qty,
            "kt00018": self._balance,
            "kt10000": self._new_order("buy"),
            "kt10001": self._new_order("sell"),
            "kt10002": self._modify_order,
            "kt10003": self._cancel_order,
            "ka10075": self._open_orders,
            "ka10076": self._filled_orders,
            "kt00007": self._order_history,
        }

    # --- transport ----------------------------------------------------------

    def transport(self) -> httpx.MockTransport:
        """An httpx transport answering from this backend (sync and async clients)."""
        return httpx.MockTransport(self.handle)

    def attach(self, api: Any) -> Any:
        """Point a ``KiwoomAPI``/``AsyncKiwoomAPI`` at this backend and return it.

        Swaps the HTTP clients of its REST client and its token client for
        ones using :meth:`transport`; everything above them is unchanged.
        ``KiwoomAPI.demo()`` is the usual way in — this is for building one
        by hand (e.g. with other constructor options).
        """
        for holder in (api._base_client, api._auth):
            old = holder._client
            cls = httpx.AsyncClient if isinstance(old, httpx.AsyncClient) else httpx.Client
            holder._client = cls(
                base_url=str(old.base_url), timeout=old.timeout, transport=self.transport()
            )
            if isinstance(old, httpx.Client):
                old.close()
            # An unused AsyncClient holds no connection; nothing to close.
        api._demo_backend = self
        return api

    def handle(self, request: httpx.Request) -> httpx.Response:
        path = request.url.path
        body = json.loads(request.content or b"{}") if request.content else {}
        if path == "/oauth2/token":
            expires = datetime.now(KST).replace(tzinfo=None) + timedelta(days=1)
            return self._json({
                "expires_dt": expires.strftime("%Y%m%d%H%M%S"),
                "token_type": "bearer",
                "token": "demo-token-not-a-real-kiwoom-token",
                "return_code": 0,
                "return_msg": OK_MSG,
            })  # fmt: skip
        if path == "/oauth2/revoke":
            return self._json({"return_code": 0, "return_msg": OK_MSG})
        api_id = request.headers.get("api-id", "")
        next_key = (
            request.headers.get("next-key", "") if request.headers.get("cont-yn") == "Y" else ""
        )
        with self._lock:
            self.requests.append(api_id)
            data, more = self._dispatch(api_id, body, next_key)
        headers = {"api-id": api_id, "cont-yn": "Y" if more else "N", "next-key": more}
        return self._json(data, headers)

    def _json(
        self, data: dict[str, Any], headers: Mapping[str, str] | None = None
    ) -> httpx.Response:
        return httpx.Response(200, json={**data, DEMO_KEY: DEMO_NOTICE}, headers=headers)

    def _dispatch(
        self, api_id: str, body: dict[str, Any], next_key: str
    ) -> tuple[dict[str, Any], str]:
        handler = self._handlers.get(api_id)
        if handler is not None:
            try:
                data, more = handler(body, next_key)
            except (DemoRefusal, OrderRefused) as exc:
                return self._refuse(str(exc)), ""
            message = ORDER_MSG if api_id in ORDER_API_IDS else OK_MSG
            return {**self._shape(api_id, data), "return_code": 0, "return_msg": message}, more
        if api_id in ORDER_API_IDS:
            return self._refuse(
                f"데모 모드는 {api_id} 주문을 지원하지 않습니다 — 아무것도 전송하지 않았습니다"
            ), ""
        try:
            tr = spec.get(api_id)
        except KeyError:
            return self._refuse(
                f"api-id 를 확인하세요: {api_id!r} [1504:데모 서버가 모르는 TR]"
            ), ""
        if tr.transport != "rest":
            return self._refuse(f"{api_id} 는 WebSocket TR 입니다"), ""
        return {**self._generic(tr, body), "return_code": 0, "return_msg": OK_MSG}, ""

    @staticmethod
    def _refuse(message: str) -> dict[str, Any]:
        return {"return_code": 2, "return_msg": f"{message} (데모)"}

    # --- shaping by the catalog ---------------------------------------------

    def _shape(self, api_id: str, data: dict[str, Any]) -> dict[str, Any]:
        """Add catalog fields the handler left out, as filler, so the keys match the spec."""
        try:
            tr = spec.get(api_id)
        except KeyError:
            return data
        top = [f for f in tr.response if f.parent is None]
        children = _children(tr.response)
        if not top:
            return data
        context = self._context(data.get("stk_cd"))
        out: dict[str, Any] = {}
        for f in top:  # catalog order, catalog keys only
            if f.type == "list":
                rows = data.get(f.id)
                fields = children.get(f.id, [])
                out[f.id] = [
                    self._fill_row(fields, row, i) if fields else row
                    for i, row in enumerate(rows if isinstance(rows, list) else [])
                ]
            else:
                out[f.id] = data[f.id] if f.id in data else self._guess(f, context, 0)
        return out

    def _fill_row(
        self, fields: Iterable[spec.Field], row: dict[str, Any], i: int
    ) -> dict[str, Any]:
        context = self._context(row.get("stk_cd") or row.get("code"))
        return {f.id: row[f.id] if f.id in row else self._guess(f, context, i) for f in fields}

    def _context(self, code: Any) -> dict[str, Any]:
        stock = self.market.stock(str(code or "")) or UNIVERSE[0]
        return self._quote(stock)

    def _guess(self, f: spec.Field, quote: dict[str, Any], i: int) -> Any:
        """A plausible value for a field the handlers don't compute."""
        if f.type == "list":
            return []
        if f.id in quote:
            return quote[f.id]
        name, fid = f.name, f.id
        h = _hash(fid, quote.get("stk_cd"), i)
        if "종목코드" in name or "종목번호" in name:
            return quote["stk_cd"]
        if "종목명" in name:
            return quote["stk_nm"]
        if "계좌" in name and "번호" in name:
            return ACCOUNT_NO
        if "일자" in name or fid == "dt" or fid.endswith("_dt"):
            days = business_days(self.market.session, i + 1)
            return days[0].strftime("%Y%m%d")
        if "시간" in name or fid.endswith("_tm") or fid == "tm":
            return "153000"
        if any(word in name for word in ("율", "률", "비율", "%", "비중")):
            if "등락" in name or "대비" in name:
                return rate((h % 2000 - 1000) / 100)
            return f"{h % 1000 / 100:.2f}"
        if name.endswith("가") or any(word in name for word in ("가격", "단가", "호가", "현재가")):
            return str(quote["_price"])
        if any(word in name for word in ("수량", "잔량", "거래량", "주식수", "건수", "량")):
            return str(h % 100000)
        if any(word in name for word in ("금액", "대금", "손익", "자산", "금")):
            return str(h % 100_000_000)
        if any(word in name for word in ("구분", "기호", "여부", "코드", "상태")):
            return ""
        return ""

    def _generic(self, tr: spec.TRSpec, body: dict[str, Any]) -> dict[str, Any]:
        """A whole response for a TR without a handler, shaped by the catalog."""
        children = _children(tr.response)
        quote = self._context(body.get("stk_cd"))
        out: dict[str, Any] = {}
        for f in tr.response:
            if f.parent is not None:
                continue
            if f.type == "list":
                fields = children.get(f.id, ())
                per_stock = any("종목" in c.name for c in fields)
                stocks = (
                    UNIVERSE[:10]
                    if per_stock
                    else (self.market.stock(str(body.get("stk_cd") or "")) or UNIVERSE[0],) * 10
                )
                out[f.id] = [
                    {c.id: self._guess(c, self._quote(stock), i) for c in fields}
                    for i, stock in enumerate(stocks)
                ]
            else:
                out[f.id] = self._guess(f, quote, 0)
        return out

    # --- market data --------------------------------------------------------

    def _quote(self, stock: DemoStock) -> dict[str, Any]:
        """Today's common quote fields of a stock, Kiwoom-formatted."""
        bar = self.market.today_bar(stock.code)
        upper, lower = self.market.limits(stock.code)
        prev = bar.prev_close
        tick = int(tick_size(bar.close))
        prev_volume = self.market.daily(stock.code)[-2].volume
        mac = bar.close * stock.shares // 100_000_000  # 억원
        return {
            "_price": bar.close,
            "stk_cd": stock.code,
            "stk_nm": stock.name,
            "cur_prc": directed(bar.close, bar.change),
            "pred_pre": signed(bar.change),
            "pred_pre_sig": sign_code(bar.change),
            "pre_sig": sign_code(bar.change),
            "flu_rt": rate(bar.change_pct),
            "trde_qty": str(bar.volume),
            "now_trde_qty": str(bar.volume),
            "pred_trde_qty": str(prev_volume),
            "trde_prica": str(bar.value // 1_000_000),  # 백만원
            "open_pric": directed(bar.open, bar.open - prev),
            "high_pric": directed(bar.high, bar.high - prev),
            "low_pric": directed(bar.low, bar.low - prev),
            "close_pric": str(bar.close),
            "base_pric": str(prev),
            "upl_pric": f"+{upper}",
            "lst_pric": f"-{lower}",
            "sel_bid": f"+{bar.close + tick}" if bar.close + tick > prev else str(bar.close + tick),
            "buy_bid": directed(bar.close, bar.change),
            "mac": str(mac),
            "stkcnt": str(stock.shares // 1000),
            "cntr_tm": "153000",
            "cntr_str": rate(100 + (_hash(stock.code, "str") % 4000 - 2000) / 100).lstrip("+"),
            "dt": bar.time,
        }

    def _stock_list(self, body: dict[str, Any], _next: str) -> tuple[dict[str, Any], str]:
        market = str(body.get("mrkt_tp", "0"))
        rows = [
            {
                "code": s.code,
                "name": s.name,
                "listCount": f"{s.shares:016d}",
                "auditInfo": "정상",
                "regDay": "19750611" if s.market == "0" else "20070702",
                "lastPrice": f"{self.market.today_bar(s.code).prev_close:08d}",
                "state": "증거금" + f"{s.margin_rate}%",
                "marketCode": s.market,
                "marketName": MARKET_NAMES[s.market],
                "upName": s.sector,
                "upSizeName": "대형주" if s.market == "0" else "",
                "companyClassName": "",
                "orderWarning": "0",
                "nxtEnable": "Y",
            }
            for s in UNIVERSE
            if s.market == market
        ]
        return {"list": rows}, ""

    def _basic_info(self, body: dict[str, Any], _next: str) -> tuple[dict[str, Any], str]:
        stock = self._require_stock(body.get("stk_cd"))
        bars = self.market.daily(stock.code)
        bar = bars[-1]
        year = [b for b in bars if b.time[:4] == bar.time[:4]]
        last250 = bars[-250:]
        hi250 = max(last250, key=lambda b: b.high)
        lo250 = min(last250, key=lambda b: b.low)
        eps = int(bar.close / stock.per) if stock.per else 0
        bps = int(bar.close / stock.pbr) if stock.pbr else 0
        out = {k: v for k, v in self._quote(stock).items() if not k.startswith("_")}
        out.update({
            "setl_mm": "12",
            "fav": "100" if stock.code == "005930" else "5000",
            "fav_unit": "원",
            "cap": str(stock.shares * 5000 // 100_000_000),
            "flo_stk": str(stock.shares // 1000),
            "dstr_stk": str(int(stock.shares * 0.75) // 1000),
            "dstr_rt": "75.00",
            "crd_rt": "+0.12",
            "mac_wght": "",
            "for_exh_rt": rate(20 + _hash(stock.code, "frgn") % 3500 / 100).lstrip("+"),
            "repl_pric": str(int(bar.prev_close * 0.7)),
            "per": f"{stock.per:.2f}" if stock.per else "",
            "pbr": f"{stock.pbr:.2f}" if stock.pbr else "",
            "roe": f"{stock.roe:.2f}" if stock.roe else "",
            "eps": str(eps),
            "bps": str(bps),
            "ev": "",
            "sale_amt": str(stock.shares * bar.close // 100_000_000 // 2),
            "bus_pro": str(stock.shares * bar.close // 100_000_000 // 20),
            "cup_nga": str(stock.shares * eps // 100_000_000),
            "oyr_hgst": f"+{max(b.high for b in year)}",
            "oyr_lwst": f"-{min(b.low for b in year)}",
            "250hgst": f"+{hi250.high}",
            "250lwst": f"-{lo250.low}",
            "250hgst_pric_dt": hi250.time,
            "250lwst_pric_dt": lo250.time,
            "250hgst_pric_pre_rt": rate((bar.close / hi250.high - 1) * 100),
            "250lwst_pric_pre_rt": rate((bar.close / lo250.low - 1) * 100),
            "exp_cntr_pric": "0",
            "exp_cntr_qty": "0",
            "trde_pre": rate((bar.volume / max(bars[-2].volume, 1) - 1) * 100),
        })  # fmt: skip
        return out, ""

    def _watchlist(self, body: dict[str, Any], _next: str) -> tuple[dict[str, Any], str]:
        codes = [c for c in str(body.get("stk_cd") or "").split("|") if c.strip()]
        rows = []
        for code in codes:
            stock = self.market.stock(code)
            if stock is not None:
                rows.append({k: v for k, v in self._quote(stock).items() if not k.startswith("_")})
        return {"atn_stk_infr": rows}, ""

    def _chart(self, period: str) -> Handler:
        key = {
            "day": "stk_dt_pole_chart_qry",
            "week": "stk_stk_pole_chart_qry",
            "month": "stk_mth_pole_chart_qry",
            "year": "stk_yr_pole_chart_qry",
        }[period]

        def handler(body: dict[str, Any], next_key: str) -> tuple[dict[str, Any], str]:
            stock = self._require_stock(body.get("stk_cd"))
            base = str(body.get("base_dt") or self.market.session.strftime("%Y%m%d"))
            bars = [b for b in self.market.daily(stock.code) if b.time <= base]
            if period != "day":
                bars = aggregate(bars, 1, group=period)
            rows = [_candle(b) for b in reversed(bars)]  # newest first, as Kiwoom sends
            page, more = _page(rows, next_key, CHART_PAGE)
            return {"stk_cd": stock.code, key: page}, more

        return handler

    def _minute_chart(self, body: dict[str, Any], next_key: str) -> tuple[dict[str, Any], str]:
        stock = self._require_stock(body.get("stk_cd"))
        scope = max(int(str(body.get("tic_scope") or "1") or 1), 1)
        session = self.market.session.strftime("%Y%m%d")
        base = str(body.get("base_dt") or session)
        bars = self.market.minutes(stock.code) if base == session else []
        if scope > 1:
            bars = aggregate(bars, scope, group="minute")
        rows = []
        for b in reversed(bars):
            row = _candle(b)
            row["cntr_tm"] = row.pop("dt")
            rows.append(row)
        page, more = _page(rows, next_key, MINUTE_PAGE)
        return {"stk_cd": stock.code, "stk_min_pole_chart_qry": page}, more

    # --- rankings -----------------------------------------------------------

    def _ranked(self, body: dict[str, Any]) -> list[tuple[DemoStock, Bar, Bar]]:
        markets = {"000": ("0", "10", "8"), "001": ("0",), "101": ("10",)}
        allowed = markets.get(str(body.get("mrkt_tp") or "000"), ("0", "10", "8"))
        out = []
        for stock in UNIVERSE:
            if stock.market in allowed:
                daily = self.market.daily(stock.code)
                out.append((stock, daily[-1], daily[-2]))
        return out

    def _rank_row(self, stock: DemoStock, **extra: str) -> dict[str, Any]:
        row = {k: v for k, v in self._quote(stock).items() if not k.startswith("_")}
        row.update(extra)
        return row

    def _top_volume(self, body: dict[str, Any], _next: str) -> tuple[dict[str, Any], str]:
        ranked = sorted(self._ranked(body), key=lambda t: t[1].volume, reverse=True)
        rows = [
            self._rank_row(
                stock,
                pred_rt=rate((bar.volume / prev.volume) * 100) if prev.volume else "0.00",
                trde_tern_rt=rate(bar.volume / stock.shares * 100).lstrip("+"),
                trde_amt=str(bar.value // 1_000_000),
                opmr_trde_qty=str(bar.volume),
            )
            for stock, bar, prev in ranked
        ]
        return {"tdy_trde_qty_upper": rows}, ""

    def _top_change(self, body: dict[str, Any], _next: str) -> tuple[dict[str, Any], str]:
        sort = str(body.get("sort_tp") or "1")
        ranked = self._ranked(body)
        if sort in ("1", "2"):
            ranked = [t for t in ranked if t[1].change > 0]
        elif sort in ("3", "4"):
            ranked = [t for t in ranked if t[1].change < 0]
        else:
            ranked = [t for t in ranked if t[1].change == 0]
        keys: dict[str, Callable[[tuple[DemoStock, Bar, Bar]], float]] = {
            "1": lambda t: -t[1].change_pct,
            "2": lambda t: -t[1].change,
            "3": lambda t: t[1].change_pct,
            "4": lambda t: t[1].change,
        }
        ranked.sort(key=keys.get(sort, lambda t: 0.0))
        rows = [self._rank_row(stock) for stock, _bar, _prev in ranked]
        return {"pred_pre_flu_rt_upper": rows}, ""

    def _top_value(self, body: dict[str, Any], _next: str) -> tuple[dict[str, Any], str]:
        ranked = self._ranked(body)
        by_prev = sorted(ranked, key=lambda t: t[2].value, reverse=True)
        prev_rank = {t[0].code: i for i, t in enumerate(by_prev, start=1)}
        ranked.sort(key=lambda t: t[1].value, reverse=True)
        rows = [
            self._rank_row(
                stock,
                now_rank=str(i),
                pred_rank=str(prev_rank[stock.code]),
                trde_prica=str(bar.value // 1_000_000),
            )
            for i, (stock, bar, _prev) in enumerate(ranked, start=1)
        ]
        return {"trde_prica_upper": rows}, ""

    def _volume_spike(self, body: dict[str, Any], _next: str) -> tuple[dict[str, Any], str]:
        ranked = [t for t in self._ranked(body) if t[1].volume > t[2].volume]
        ranked.sort(key=lambda t: t[1].volume / t[2].volume, reverse=True)
        rows = [
            self._rank_row(
                stock,
                prev_trde_qty=str(prev.volume),
                sdnin_qty=signed(bar.volume - prev.volume),
                sdnin_rt=rate((bar.volume / prev.volume - 1) * 100),
            )
            for stock, bar, prev in ranked
        ]
        return {"trde_qty_sdnin": rows}, ""

    # --- investors ----------------------------------------------------------

    def _investor_flow(self, body: dict[str, Any], next_key: str) -> tuple[dict[str, Any], str]:
        stock = self._require_stock(body.get("stk_cd"))
        end = str(body.get("dt") or self.market.session.strftime("%Y%m%d"))
        quantity = str(body.get("amt_qty_tp") or "1") == "2"
        bars = [b for b in self.market.daily(stock.code) if b.time <= end]
        rows = [self._flow_row(stock, b, quantity) for b in reversed(bars)]
        page, more = _page(rows, next_key, 100)
        return {"stk_invsr_orgn": page}, more

    def _flow_row(self, stock: DemoStock, bar: Bar, quantity: bool) -> dict[str, Any]:
        import random

        rng = random.Random(_hash(self.market.seed, stock.code, bar.time, "flow"))
        scale = bar.value / 1_000_000 * 0.08  # 백만원
        foreign = rng.gauss(0.15 * bar.change_pct, 1) * scale
        parts = {
            name: rng.gauss(0.05 * bar.change_pct, 1) * scale * weight
            for name, weight in (
                ("fnnc_invt", 0.35), ("insrnc", 0.1), ("invtrt", 0.2), ("etc_fnnc", 0.05),
                ("bank", 0.05), ("penfnd_etc", 0.3), ("samo_fund", 0.1), ("natn", 0.02),
            )
        }  # fmt: skip
        institution = sum(parts.values())
        corp = rng.gauss(0, 0.1) * scale
        individual = -(foreign + institution + corp)
        unit = 1_000_000 / bar.close if quantity else 1
        values = {
            "ind_invsr": individual, "frgnr_invsr": foreign, "orgn": institution,
            **parts, "etc_corp": corp, "natfor": 0.0,
        }  # fmt: skip
        return {
            "dt": bar.time,
            "cur_prc": directed(bar.close, bar.change),
            "pre_sig": sign_code(bar.change),
            "pred_pre": signed(bar.change),
            "flu_rt": rate(bar.change_pct),
            "acc_trde_qty": str(bar.volume),
            "acc_trde_prica": str(bar.value // 1_000_000),
            **{k: signed(round(v * unit)) for k, v in values.items()},
        }

    # --- account ------------------------------------------------------------

    def _account_no(self, _body: dict[str, Any], _next: str) -> tuple[dict[str, Any], str]:
        return {"acctNo": ACCOUNT_NO}, ""

    def _holding_rows(self) -> list[dict[str, Any]]:
        rows = []
        total_value = sum(
            h.qty * self.market.price(code) for code, h in self.account.holdings.items() if h.qty
        )
        for code, h in self.account.holdings.items():
            if h.qty <= 0:
                continue
            stock = BY_CODE[code]
            bar = self.market.today_bar(code)
            purchase = h.qty * h.avg_price
            value = h.qty * bar.close
            buy_fee, sell_fee, tax = commission(purchase), commission(value), sell_tax(value)
            pnl = value - purchase - buy_fee - sell_fee - tax
            rows.append({
                "stk_cd": f"A{code}",
                "stk_nm": stock.name,
                "evltv_prft": signed(pnl),
                "prft_rt": rate(pnl / purchase * 100 if purchase else 0),
                "pur_pric": str(h.avg_price),
                "pred_close_pric": str(bar.prev_close),
                "rmnd_qty": str(h.qty),
                "trde_able_qty": str(h.sellable),
                "cur_prc": str(bar.close),
                "pred_buyq": "0",
                "pred_sellq": "0",
                "tdy_buyq": str(self._today_qty(code, "buy")),
                "tdy_sellq": str(self._today_qty(code, "sell")),
                "pur_amt": str(purchase),
                "pur_cmsn": str(buy_fee),
                "evlt_amt": str(value),
                "sell_cmsn": str(sell_fee),
                "tax": str(tax),
                "sum_cmsn": str(buy_fee + sell_fee),
                "poss_rt": rate(value / total_value * 100 if total_value else 0).lstrip("+"),
                "crd_tp": "00",
                "crd_tp_nm": "",
                "crd_loan_dt": "",
            })  # fmt: skip
        return rows

    def _today_qty(self, code: str, side: str) -> int:
        today = self._stamp()[0]
        return sum(
            o.filled_qty
            for o in self.book.orders
            if o.code == code and o.side == side and o.date == today
        )

    def _balance(self, _body: dict[str, Any], _next: str) -> tuple[dict[str, Any], str]:
        rows = self._holding_rows()
        purchase = sum(int(r["pur_amt"]) for r in rows)
        value = sum(int(r["evlt_amt"]) for r in rows)
        pnl = sum(int(r["evltv_prft"]) for r in rows)
        return {
            "tot_pur_amt": str(purchase),
            "tot_evlt_amt": str(value),
            "tot_evlt_pl": signed(pnl),
            "tot_prft_rt": rate(pnl / purchase * 100 if purchase else 0),
            "prsm_dpst_aset_amt": str(value + self.account.cash),
            "tot_loan_amt": "0",
            "tot_crd_loan_amt": "0",
            "tot_crd_ls_amt": "0",
            "acnt_evlt_remn_indv_tot": rows,
        }, ""

    def _deposit(self, _body: dict[str, Any], _next: str) -> tuple[dict[str, Any], str]:
        cash = self.account.cash
        orderable = self.account.orderable_cash
        out: dict[str, Any] = {
            "entr": str(cash),
            "d1_entra": str(cash),
            "d2_entra": str(cash),
            "ord_alow_amt": str(orderable),
            "pymn_alow_amt": str(orderable),
            "d1_pymn_alow_amt": str(orderable),
            "d2_pymn_alow_amt": str(orderable),
            "profa_ch": str(self.account.reserved_cash),
            "ch_uncla": "0",
            "ch_uncla_tot": "0",
            "stk_entr_prst": [],
        }
        for pct in (20, 30, 40, 50, 60, 100):
            out[f"{pct}stk_ord_alow_amt"] = str(orderable)
        return out, ""

    def _orderable_qty(self, body: dict[str, Any], _next: str) -> tuple[dict[str, Any], str]:
        stock = self._require_stock(body.get("stk_cd"))
        price = int(str(body.get("uv") or "0") or 0) or self.market.price(stock.code)
        cash = self.account.orderable_cash
        out: dict[str, Any] = {
            "stk_profa_rt": str(stock.margin_rate),
            "profa_rt": "100",  # the demo account is a cash (100%) account
            "aplc_rt": "100",
            "entr": str(self.account.cash),
            "repl_amt": "0",
            "uncla": "0",
            "ord_pos_repl": "0",
            "ord_alowa": str(cash),
            "min_ord_alow_amt": str(cash),
            "min_ord_alowq": str(cash // price),
            "min_pred_reu_amt": "0",
            "min_tdy_reu_amt": "0",
        }
        for pct in (20, 30, 40, 50, 60, 100):
            amount = cash * 100 // pct if pct >= stock.margin_rate else 0
            out[f"profa_{pct}ord_alow_amt"] = str(amount)
            out[f"profa_{pct}ord_alowq"] = str(amount // price)
            out[f"profa_{pct}pred_reu_amt"] = "0"
            out[f"profa_{pct}tdy_reu_amt"] = "0"
        return out, ""

    # --- paper trading ------------------------------------------------------

    def _stamp(self) -> tuple[str, str]:
        now = datetime.now(KST)
        return now.strftime("%Y%m%d"), now.strftime("%H%M%S")

    def _new_order(self, side: str) -> Handler:
        def handler(body: dict[str, Any], _next: str) -> tuple[dict[str, Any], str]:
            stock = self._require_stock(body.get("stk_cd"))
            trade_type = str(body.get("trde_tp") or "0")
            price = _int(body.get("ord_uv"))
            current = self.market.price(stock.code)
            if trade_type == "0":
                self._check_limit_price(stock.code, price)
            order = self.book.place(
                side=side, code=stock.code, qty=_int(body.get("ord_qty")),
                price=price or None, trade_type=trade_type, current=current,
                stamp=self._stamp(), exchange=_exchange(body),
            )  # fmt: skip
            return {"ord_no": order.no, "dmst_stex_tp": order.exchange}, ""

        return handler

    def _check_limit_price(self, code: str, price: int) -> None:
        upper, lower = self.market.limits(code)
        if price <= 0:
            raise DemoRefusal("지정가 주문은 주문단가(ord_uv)가 필요합니다")
        if not lower <= price <= upper:
            raise DemoRefusal(f"주문단가가 하한가({lower:,})~상한가({upper:,}) 밖입니다: {price:,}")
        if price % int(tick_size(price)):
            raise DemoRefusal(
                f"호가단위({int(tick_size(price))}원)에 맞지 않는 단가입니다: {price:,}"
            )

    def _modify_order(self, body: dict[str, Any], _next: str) -> tuple[dict[str, Any], str]:
        stock = self._require_stock(body.get("stk_cd"))
        price = _int(body.get("mdfy_uv"))
        self._check_limit_price(stock.code, price)
        order = self.book.modify(
            str(body.get("orig_ord_no") or ""), stock.code, _int(body.get("mdfy_qty")), price,
            self.market.price(stock.code), self._stamp(),
        )  # fmt: skip
        return {
            "ord_no": order.no,
            "base_orig_ord_no": order.orig_no,
            "mdfy_qty": str(order.qty),
            "dmst_stex_tp": order.exchange,
        }, ""

    def _cancel_order(self, body: dict[str, Any], _next: str) -> tuple[dict[str, Any], str]:
        stock = self._require_stock(body.get("stk_cd"))
        order = self.book.cancel(
            str(body.get("orig_ord_no") or ""), stock.code, _int(body.get("cncl_qty")),
            self._stamp(),
        )  # fmt: skip
        return {
            "ord_no": order.no,
            "base_orig_ord_no": order.orig_no,
            "cncl_qty": str(order.qty),
        }, ""

    def _orders(self, body: dict[str, Any], side_key: str, code_flag: str) -> list[PaperOrder]:
        today = self._stamp()[0]
        side = {"1": "sell", "2": "buy"}.get(str(body.get(side_key) or "0"))
        code = str(body.get("stk_cd") or "").strip()
        filter_code = str(body.get(code_flag) or "0") == "1" and code
        return [
            o for o in reversed(self.book.orders)  # newest first
            if o.date == today and (side is None or o.side == side)
            and (not filter_code or o.code == code)
        ]  # fmt: skip

    def _order_row(self, o: PaperOrder) -> dict[str, Any]:
        stock = BY_CODE[o.code]
        current = self.market.price(o.code)
        return {
            "acnt_no": ACCOUNT_NO,
            "ord_no": o.no,
            "stk_cd": o.code,
            "stk_nm": stock.name,
            "ord_stt": o.status,
            "ord_qty": str(o.qty),
            "ord_pric": str(o.price),
            "oso_qty": str(o.open_qty),
            "cntr_tot_amt": str(o.filled_qty * o.filled_price),
            "orig_ord_no": o.orig_no,
            "io_tp_nm": o.label,
            "trde_tp": TRADE_TYPE_NAMES.get(o.trade_type, o.trade_type),
            "tm": o.time,
            "ord_tm": o.time,
            "cntr_qty": str(o.filled_qty),
            "cntr_pric": str(o.filled_price),
            "cur_prc": str(current),
            "tdy_trde_cmsn": str(o.fee),
            "tdy_trde_tax": str(o.tax),
            "stex_tp": "1" if o.exchange == "KRX" else "2",
            "stex_tp_txt": o.exchange,
            "sor_yn": "N",
            "stop_pric": "0",
        }

    def _open_orders(self, body: dict[str, Any], _next: str) -> tuple[dict[str, Any], str]:
        orders = [o for o in self._orders(body, "trde_tp", "all_stk_tp") if o.open_qty > 0]
        return {"oso": [self._order_row(o) for o in orders]}, ""

    def _filled_orders(self, body: dict[str, Any], _next: str) -> tuple[dict[str, Any], str]:
        orders = [o for o in self._orders(body, "sell_tp", "qry_tp") if o.filled_qty > 0]
        return {"cntr": [self._order_row(o) for o in orders]}, ""

    def _order_history(self, body: dict[str, Any], _next: str) -> tuple[dict[str, Any], str]:
        if str(body.get("ord_dt") or "") != self._stamp()[0]:
            return {"acnt_ord_cntr_prps_dtl": []}, ""  # the paper account starts fresh today
        orders = self._orders({**body, "code_flag": "1"}, "sell_tp", "code_flag")
        rows = [
            {
                "ord_no": o.no, "stk_cd": o.code, "stk_nm": BY_CODE[o.code].name,
                "trde_tp": TRADE_TYPE_NAMES.get(o.trade_type, o.trade_type), "crd_tp": "보통",
                "ord_qty": str(o.qty), "ord_uv": str(o.price), "cnfm_qty": str(o.qty),
                "acpt_tp": "접수", "rsrv_tp": "", "ord_tm": o.time, "ori_ord": o.orig_no,
                "io_tp_nm": o.label, "loan_dt": "", "cntr_qty": str(o.filled_qty),
                "cntr_uv": str(o.filled_price), "ord_remnq": str(o.open_qty),
                "comm_ord_tp": "", "mdfy_cncl": _MODIFY_CANCEL.get(o.kind, ""),
                "cnfm_tm": o.time, "dmst_stex_tp": o.exchange, "cond_uv": "0",
            }
            for o in orders
        ]  # fmt: skip
        return {"acnt_ord_cntr_prps_dtl": rows}, ""

    # --- helpers ------------------------------------------------------------

    def _require_stock(self, code: Any) -> DemoStock:
        stock = self.market.stock(str(code or ""))
        if stock is None:
            listed = ", ".join(f"{s.name}({s.code})" for s in UNIVERSE[:5])
            raise DemoRefusal(
                f"데모 종목에 없는 코드입니다: {code!r} [1902:종목정보가 없습니다]. "
                f"데모 종목 예: {listed} …"
            )
        return stock


_MODIFY_CANCEL = {"modify": "정정", "cancel": "취소"}


def _int(value: Any) -> int:
    text = str(value or "").strip().replace(",", "")
    try:
        return int(float(text)) if text else 0
    except ValueError as exc:
        raise DemoRefusal(f"숫자가 아닙니다: {value!r}") from exc


def _exchange(body: dict[str, Any]) -> str:
    exchange = str(body.get("dmst_stex_tp") or "KRX").strip().upper()
    if exchange not in ("KRX", "NXT", "SOR"):
        raise DemoRefusal(f"국내거래소구분(dmst_stex_tp)을 확인하세요: {exchange!r}")
    return exchange


def _children(fields: Iterable[spec.Field]) -> dict[str, list[spec.Field]]:
    out: dict[str, list[spec.Field]] = {}
    for f in fields:
        if f.parent is not None:
            out.setdefault(f.parent, []).append(f)
    return out


def _candle(bar: Bar) -> dict[str, Any]:
    return {
        "cur_prc": str(bar.close),
        "trde_qty": str(bar.volume),
        "trde_prica": str(bar.value // 1_000_000),
        "dt": bar.time,
        "open_pric": str(bar.open),
        "high_pric": str(bar.high),
        "low_pric": str(bar.low),
        "pred_pre": signed(bar.change),
        "pred_pre_sig": sign_code(bar.change),
    }


def _page(rows: list[dict[str, Any]], next_key: str, size: int) -> tuple[list[dict[str, Any]], str]:
    start = int(next_key) if next_key.isdigit() else 0
    end = start + size
    return rows[start:end], str(end) if end < len(rows) else ""
