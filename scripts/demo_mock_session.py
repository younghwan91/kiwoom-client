"""MOCK demo: an agent's MCP tool calls against a fake Kiwoom server (no keys, no network).

    uv run --extra mcp python scripts/demo_mock_session.py                # print the session
    uv run --extra mcp python scripts/demo_mock_session.py --cast x.cast  # also write an asciicast
    agg --font-family "DejaVu Sans Mono,Noto Sans KR" x.cast docs/images/demo-mock.gif

The MCP server is the real one (``build_server``) and the tool results are its real output.
Only two things are fake: the Kiwoom HTTP server (an ``httpx.MockTransport`` returning made-up
prices) and the agent (the tool calls are a fixed script, not a language model). The
paper-trading server is used and ``order_preview`` sends nothing — it only checks and summarises
the order. ``tests/test_demo_mock_session.py`` runs this so the GIF cannot drift from the code.
"""

from __future__ import annotations

import argparse
import asyncio
import json
import sys
from typing import Any

import httpx
from mcp import types

from kiwoom_client import AsyncKiwoomAPI
from kiwoom_client.mcp.guard import order_tools_allowed
from kiwoom_client.mcp.orders.policy import OrderPolicy
from kiwoom_client.mcp.server import build_server

LISTING = [
    {"code": "005930", "name": "삼성전자", "marketName": "거래소"},
    {"code": "000660", "name": "SK하이닉스", "marketName": "거래소"},
]
# Made-up quotes (가상 시세) — this is a mock demo.
QUOTES = [
    {"stk_cd": "005930", "stk_nm": "삼성전자", "cur_prc": "+70100", "pred_pre": "+600",
     "flu_rt": "+0.86", "trde_qty": "12,345,678", "trde_prica": "865000", "mac": "4185000",
     "open_pric": "+69800", "high_pric": "+70400", "low_pric": "-69400"},
    {"stk_cd": "000660", "stk_nm": "SK하이닉스", "cur_prc": "-181500", "pred_pre": "-1500",
     "flu_rt": "-0.82", "trde_qty": "2,345,678", "trde_prica": "425000", "mac": "1321000",
     "open_pric": "+183500", "high_pric": "+184000", "low_pric": "-180500"},
]  # fmt: skip


def _fake_kiwoom(request: httpx.Request) -> httpx.Response:
    if request.url.path == "/oauth2/token":
        return httpx.Response(
            200, json={"token": "mock", "token_type": "Bearer", "expires_in": 86400}
        )
    api_id = request.headers.get("api-id")
    body = json.loads(request.content or b"{}")
    if api_id == "ka10099":
        rows = LISTING if body.get("mrkt_tp") == "0" else []
        return httpx.Response(200, json={"return_code": 0, "list": rows})
    if api_id == "ka10095":
        return httpx.Response(200, json={"return_code": 0, "atn_stk_infr": QUOTES})
    if api_id == "ka10001":  # 상·하한가
        return httpx.Response(
            200,
            json={
                "return_code": 0,
                "stk_cd": "005930",
                "cur_prc": "+70100",
                "upl_pric": "+90800",
                "lst_pric": "-49000",
            },
        )
    if api_id == "kt00011":  # 주문가능수량
        return httpx.Response(
            200,
            json={
                "return_code": 0,
                "aplc_rt": "100",
                "profa_100ord_alowq": "142",
                "min_ord_alowq": "142",
                "ord_alowa": "10000000",
            },
        )
    return httpx.Response(200, json={"return_code": 1, "return_msg": f"mock: {api_id} not faked"})


class _MockAsyncClient(httpx.AsyncClient):  # type: ignore[misc]
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        kwargs["transport"] = httpx.MockTransport(_fake_kiwoom)
        super().__init__(*args, **kwargs)


# (what the user types, [(tool, arguments)], what the agent says afterwards)
SESSION = [
    (
        "삼성전자랑 SK하이닉스 지금 얼마야?",
        [("get_quotes", {"stocks": ["삼성전자", "SK하이닉스"]})],
        "삼성전자 70,100원(+0.86%), SK하이닉스 181,500원(-0.82%)입니다.",
    ),
    (
        "삼성전자 10주 70,050원에 사는 주문 초안 만들어 줘.",
        [("order_preview", {"side": "buy", "stock": "삼성전자", "qty": 10, "price": 70050})],
        "호가단위(100원)에 맞춰 70,000원으로 내렸습니다. 예상 금액 700,000원,\n"
        "  주문가능수량 142주 안입니다.\n"
        "  아직 주문은 나가지 않았습니다. 보내려면 확인해 주세요.",
    ),
]


def _j(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False)


def _quotes(o: dict[str, Any]) -> list[str]:
    return [_j({k: q[k] for k in ("name", "code", "price", "change_pct")}) for q in o["quotes"]]


def _preview(o: dict[str, Any]) -> list[str]:
    checks = o["checks"]
    token = o.get("confirm_token", "")
    return [
        f'"sent": {_j(o["sent"])}, "would_call": {_j(o["would_call"])}',
        f'"price": {_j({k: o["price"][k] for k in ("requested", "adjusted", "tick_size")})}',
        f'"estimated_amount": {o["estimated_amount"]}, "orderable_qty": {checks["orderable_qty"]}, '
        f'"limits": [{checks["lower_limit"]}, {checks["upper_limit"]}]',
        f'"confirm_token": "{token[:18]}…", "confirm_expires_in": {o.get("confirm_expires_in")}',
    ]


SHOW = {"get_quotes": _quotes, "order_preview": _preview}

DIM, BOLD, CYAN, GREEN, YELLOW, RESET = (
    "\x1b[2m",
    "\x1b[1m",
    "\x1b[36m",
    "\x1b[32m",
    "\x1b[33m",
    "\x1b[0m",
)


class Recorder:
    """Prints to stdout and, optionally, keeps asciicast v2 events with a fake clock."""

    def __init__(self) -> None:
        self.t = 0.5
        self.events: list[tuple[float, str]] = []

    def out(self, text: str, pause: float = 0.0) -> None:
        sys.stdout.write(text)
        sys.stdout.flush()
        self.events.append((round(self.t, 3), text.replace("\n", "\r\n")))
        self.t += pause

    def type(self, prefix: str, text: str) -> None:
        self.out(prefix, 0.3)
        for ch in text:
            self.out(ch, 0.045)
        self.out("\n", 0.6)


async def run(rec: Recorder) -> None:
    real = httpx.AsyncClient
    httpx.AsyncClient = _MockAsyncClient  # type: ignore[misc]
    try:
        api = AsyncKiwoomAPI("mock-key", "mock-secret", is_mock=True)
    finally:
        httpx.AsyncClient = real  # type: ignore[misc]
    # Same wiring as run_server() on the paper server (KIWOOM_IS_MOCK=true).
    app, _ = build_server(
        api,
        allow_live_orders=order_tools_allowed(is_mock=True),
        order_policy=OrderPolicy.from_env(is_mock=True),
    )
    handler = app.get_request_handler("tools/call").handler

    rec.out(
        f"{YELLOW}{BOLD}[MOCK DEMO]{RESET}{YELLOW} 가짜 키움 서버 · 가상 시세 · 주문 전송 없음 "
        f"(KIWOOM_IS_MOCK=true){RESET}\n",
        0.4,
    )
    rec.out(f"{DIM}$ uvx --from 'kiwoom-client[mcp]' kiwoom-client-mcp{RESET}\n\n", 1.0)
    for user, calls, reply in SESSION:
        rec.type(f"{BOLD}> {RESET}", user)
        for tool, args in calls:
            rec.out(
                f"{CYAN}  ● {tool}{RESET} {DIM}{json.dumps(args, ensure_ascii=False)}{RESET}\n", 0.8
            )
            result = await handler(None, types.CallToolRequestParams(name=tool, arguments=args))
            payload = json.loads(result.content[0].text)
            for i, line in enumerate(SHOW[tool](payload)):
                rec.out(f"{DIM}    {'⎿' if i == 0 else ' '} {line}{RESET}\n", 0.35)
            rec.out("", 0.8)
        rec.out(f"{GREEN}  {reply}{RESET}\n\n", 2.5)
    await api.close()


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--cast", help="write an asciicast v2 file here")
    parser.add_argument("--width", type=int, default=110)
    args = parser.parse_args()
    rec = Recorder()
    asyncio.run(run(rec))
    if args.cast:
        header = {
            "version": 2,
            "width": args.width,
            "height": 22,
            "title": "kiwoom-client MOCK demo",
        }
        with open(args.cast, "w", encoding="utf-8") as f:
            f.write(json.dumps(header) + "\n")
            for t, text in rec.events:
                f.write(json.dumps([t, "o", text], ensure_ascii=False) + "\n")
            f.write(json.dumps([round(rec.t + 2, 3), "o", ""]) + "\n")


if __name__ == "__main__":
    main()
