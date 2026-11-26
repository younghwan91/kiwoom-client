"""DEMO session: an agent's MCP tool calls against `kiwoom-client-mcp --demo` (no keys, no network).

    uv run --extra mcp python scripts/demo_mock_session.py                # print the session
    uv run --extra mcp python scripts/demo_mock_session.py --cast x.cast  # also write an asciicast
    agg --font-family "DejaVu Sans Mono,Noto Sans KR" x.cast docs/images/demo-mock.gif

The MCP server is the real one, wired exactly as ``kiwoom-client-mcp --demo`` wires it
(:func:`kiwoom_client.mcp.server.client_and_order_settings` + ``build_server(demo=True)``),
and the tool results are its real output. Only two things are made up: the market and account
(the package's demo backend, :mod:`kiwoom_client.demo` — synthetic prices, nothing connects
anywhere) and the agent (the tool calls are a fixed script, not a language model).
``order_preview`` sends nothing — it only checks and summarises the order.
``tests/test_demo_mock_session.py`` runs this so the GIF cannot drift from the code.
"""

from __future__ import annotations

import argparse
import asyncio
import json
import sys
from collections.abc import Callable
from typing import Any

from mcp import types

from kiwoom_client.mcp.server import build_server, client_and_order_settings

#: What the user types, the tool calls, and what the agent says (from the results).
Reply = Callable[[list[dict[str, Any]]], str]


def _quote_reply(results: list[dict[str, Any]]) -> str:
    parts = [
        f"{q['name']} {q['price']:,}원({q['change_pct']:+.2f}%)" for q in results[0]["quotes"]
    ]
    return ", ".join(parts) + "입니다 — 데모용 가상 시세입니다."


def _preview_reply(results: list[dict[str, Any]]) -> str:
    o = results[0]
    price = o["price"]
    return (
        f"호가단위({int(price['tick_size']):,}원)에 맞춰 {int(price['adjusted']):,}원으로 "
        f"내렸습니다. 예상 금액 {o['estimated_amount']:,}원,\n"
        f"  주문가능수량 {o['checks']['orderable_qty']}주 안입니다.\n"
        "  아직 주문은 나가지 않았습니다. 보내려면 확인해 주세요."
    )


SESSION: list[tuple[str, list[tuple[str, dict[str, Any]]], Reply]] = [
    (
        "삼성전자랑 SK하이닉스 지금 얼마야?",
        [("get_quotes", {"stocks": ["삼성전자", "SK하이닉스"]})],
        _quote_reply,
    ),
    (
        "삼성전자 10주 70,050원에 사는 주문 초안 만들어 줘.",
        [("order_preview", {"side": "buy", "stock": "삼성전자", "qty": 10, "price": 70050})],
        _preview_reply,
    ),
]


def _j(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False)


def _quotes(o: dict[str, Any]) -> list[str]:
    rows = [_j({k: q[k] for k in ("name", "code", "price", "change_pct")}) for q in o["quotes"]]
    return [f'"_demo": {_j(o["_demo"])}', *rows]


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
    # Exactly what kiwoom-client-mcp --demo builds (the key is never read).
    api, allow_orders, policy = client_and_order_settings(
        app_key="", app_secret="", is_mock=True, demo=True, env={}
    )
    app, _ = build_server(
        api, allow_live_orders=allow_orders, order_policy=policy, mode="smart", demo=True
    )
    handler = app.get_request_handler("tools/call").handler

    rec.out(
        f"{YELLOW}{BOLD}[DEMO]{RESET}{YELLOW} 가상 데이터 · 키 없음 · 키움에 연결하지 않음 · "
        f"주문 전송 없음{RESET}\n",
        0.4,
    )
    rec.out(f"{DIM}$ uvx --from 'kiwoom-client[mcp]' kiwoom-client-mcp --demo{RESET}\n\n", 1.0)
    for user, calls, reply in SESSION:
        rec.type(f"{BOLD}> {RESET}", user)
        results = []
        for tool, args in calls:
            rec.out(
                f"{CYAN}  ● {tool}{RESET} {DIM}{json.dumps(args, ensure_ascii=False)}{RESET}\n", 0.8
            )
            result = await handler(None, types.CallToolRequestParams(name=tool, arguments=args))
            payload = json.loads(result.content[0].text)
            results.append(payload)
            for i, line in enumerate(SHOW[tool](payload)):
                rec.out(f"{DIM}    {'⎿' if i == 0 else ' '} {line}{RESET}\n", 0.35)
            rec.out("", 0.8)
        rec.out(f"{GREEN}  {reply(results)}{RESET}\n\n", 2.5)
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
            "title": "kiwoom-client DEMO (synthetic data)",
        }
        with open(args.cast, "w", encoding="utf-8") as f:
            f.write(json.dumps(header) + "\n")
            for t, text in rec.events:
                f.write(json.dumps([t, "o", text], ensure_ascii=False) + "\n")
            f.write(json.dumps([round(rec.t + 2, 3), "o", ""]) + "\n")


if __name__ == "__main__":
    main()
