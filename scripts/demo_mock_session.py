"""Demo session: an agent's MCP tool calls in demo mode (no keys, no network).

    uv run --extra mcp python scripts/demo_mock_session.py                # print the session
    uv run --extra mcp python scripts/demo_mock_session.py --cast x.cast  # also write an asciicast
    agg --font-family "DejaVu Sans Mono,Noto Sans KR" --font-size 13 --fps-cap 8 \
        x.cast docs/images/demo-mock.gif

The MCP server is the real one, wired exactly like ``kiwoom-client-mcp --demo``
(:func:`~kiwoom_client.mcp.server.client_and_order_settings` with ``demo=True``),
and the tool results are its real output on the built-in demo backend: synthetic
prices, a made-up paper account, every result marked ``"_demo"``. Only the agent
is scripted (the tool calls are fixed, not a language model). The flow is
portfolio summary → rebalance plan → order preview; ``order_preview`` sends
nothing. ``tests/test_demo_mock_session.py`` runs this so the GIF cannot drift
from the code.
"""

from __future__ import annotations

import argparse
import asyncio
import json
import sys
from typing import Any

from mcp import types

from kiwoom_client.mcp.server import build_server, client_and_order_settings

#: Target weights for the rebalance step (카카오 0 = sell it all).
TARGETS = {"삼성전자": 0.3, "SK하이닉스": 0.2, "카카오": 0}


def _j(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False)


def _won(value: float) -> str:
    return f"{value:,.0f}원"


def _portfolio(o: dict[str, Any]) -> list[str]:
    t = o["totals"]
    lines = [
        f'"total_assets": {t["total_assets"]}, "cash_d2": {t["cash_d2"]}, '
        f'"return_pct": {t["return_pct"]}'
    ]
    keys = ("name", "qty", "weight_pct", "return_pct")
    lines += [_j({k: h[k] for k in keys}) for h in o["holdings"]]
    return lines


def _rebalance(o: dict[str, Any]) -> list[str]:
    keys = ("action", "name", "qty", "price", "after_weight_pct")
    return [f'"sent": {_j(o["sent"])}'] + [_j({k: r[k] for k in keys}) for r in o["orders"]]


def _preview(o: dict[str, Any]) -> list[str]:
    token = o.get("confirm_token", "")
    return [
        f'"sent": {_j(o["sent"])}, "would_call": {_j(o["would_call"])}',
        f'"summary": {_j(o["summary"])}',
        f'"estimated_amount": {o["estimated_amount"]}, "errors": {_j(o.get("errors", []))}',
        f'"confirm_token": "{token[:18]}…", "confirm_expires_in": {o.get("confirm_expires_in")}',
    ]


def _say_portfolio(o: dict[str, Any], _results: dict[str, Any]) -> str:
    t = o["totals"]
    top = max(o["holdings"], key=lambda h: h["weight_pct"])
    return (
        f"총자산 {_won(t['total_assets'])}, 평가손익 {t['return_pct']:+.2f}%, "
        f"현금 비중 {t['cash_weight_pct']:.1f}%.\n"
        f"  {len(o['holdings'])}종목 중 {top['name']} 비중이 "
        f"{top['weight_pct']:.1f}% 로 가장 큽니다."
    )


def _say_rebalance(o: dict[str, Any], _results: dict[str, Any]) -> str:
    side = {"sell": "매도", "buy": "매수"}
    rows = ", ".join(f"{r['name']} {r['qty']}주 {side[r['action']]}" for r in o["orders"])
    return f"{rows} — 매도 먼저, 현금 안에서 매수합니다.\n  주문은 하지 않았습니다(계산만)."


def _say_preview(o: dict[str, Any], results: dict[str, Any]) -> str:
    row = results["rebalance_plan"]["orders"][0]
    side = "매도" if row["action"] == "sell" else "매수"
    return (
        f"{row['name']} {row['qty']}주 {row['price']:,}원 지정가 {side}, "
        f"예상 {_won(o['estimated_amount'])}.\n"
        "  아직 주문은 나가지 않았습니다. 보내려면 확인해 주세요."
    )


def _first_row_args(plan: dict[str, Any]) -> dict[str, Any]:
    """The first row's preview args by stock name, minus the defaults (new, 지정가, KRX)."""
    row = plan["orders"][0]
    args = row["order_preview_args"]
    assert (args["action"], args["trde_tp"], args["dmst_stex_tp"]) == ("new", "0", "KRX")
    return {"side": args["side"], "stock": row["name"], "qty": args["qty"], "price": args["price"]}


# (what the user types, tool, arguments or a function of earlier results, what is shown, reply)
SESSION: list[tuple[str, str, Any, Any, Any]] = [
    ("내 포트폴리오 요약해 줘.", "get_portfolio", {}, _portfolio, _say_portfolio),
    (
        "삼성전자 30%, SK하이닉스 20%, 카카오는 정리. 어떻게 사고팔면 돼? 주문은 하지 마.",
        "rebalance_plan",
        {"targets": TARGETS},
        _rebalance,
        _say_rebalance,
    ),
    (
        "첫 줄 주문 미리보기 만들어 줘. 보내지는 마.",
        "order_preview",
        lambda prev: _first_row_args(prev["rebalance_plan"]),
        _preview,
        _say_preview,
    ),
]

DIM, BOLD, CYAN, GREEN, YELLOW, RESET = (
    "\x1b[2m",
    "\x1b[1m",
    "\x1b[36m",
    "\x1b[32m",
    "\x1b[33m",
    "\x1b[0m",
)


BANNER = (
    f"{YELLOW}{BOLD}[데모]{RESET}{YELLOW} 가상 데이터 — 실제 시세·계좌가 아닙니다 · "
    f"키 없음 · 주문 전송 없음{RESET}\n"
)
CLEAR = "\x1b[2J\x1b[H"
COMMAND = "uvx --from 'kiwoom-client[mcp]' kiwoom-client-mcp --demo"


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
        for i in range(0, len(text), 3):  # three characters per frame keeps the GIF small
            self.out(text[i : i + 3], 0.12)
        self.out("\n", 0.6)


async def run(rec: Recorder) -> dict[str, Any]:
    """Play the session; returns each tool's result by tool name."""
    # Same wiring as `kiwoom-client-mcp --demo` (env={} so the shell's settings don't leak in).
    api, allow_orders, policy = client_and_order_settings(
        app_key="", app_secret="", is_mock=True, demo=True, env={}
    )
    app, _ = build_server(api, allow_live_orders=allow_orders, order_policy=policy, demo=True)
    handler = app.get_request_handler("tools/call").handler
    results: dict[str, Any] = {}

    try:
        for turn, (user, tool, args, show, say) in enumerate(SESSION):
            arguments = args(results) if callable(args) else args
            # Each turn on a fresh screen under the banner: the "가상 데이터" line is in every
            # frame, and an unscrolled screen keeps the GIF small.
            rec.out(CLEAR if turn else "")
            rec.out(BANNER, 0.4)
            rec.out(f"{DIM}$ {COMMAND}{RESET}\n\n", 1.0)
            rec.type(f"{BOLD}> {RESET}", user)
            rec.out(f"{CYAN}  ● {tool}{RESET} {DIM}{_j(arguments)}{RESET}\n", 0.8)
            params = types.CallToolRequestParams(name=tool, arguments=arguments)
            result = await handler(None, params)
            payload = json.loads(result.content[0].text)
            if result.is_error:
                raise RuntimeError(f"{tool}: {payload}")
            results[tool] = payload
            lines = [f'"_demo": {_j(payload["_demo"])}', *show(payload)]
            for i, line in enumerate(lines):
                rec.out(f"{DIM}    {'⎿' if i == 0 else ' '} {line}{RESET}\n", 0.3)
            rec.out("", 0.8)
            rec.out(f"{GREEN}  {say(payload, results)}{RESET}\n", 3.0)
    finally:
        await api.close()
    return results


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--cast", help="write an asciicast v2 file here")
    parser.add_argument("--width", type=int, default=100)
    parser.add_argument("--height", type=int, default=16)
    args = parser.parse_args()
    rec = Recorder()
    asyncio.run(run(rec))
    if args.cast:
        header = {
            "version": 2,
            "width": args.width,
            "height": args.height,
            "title": "kiwoom-client demo mode",
        }
        with open(args.cast, "w", encoding="utf-8") as f:
            f.write(json.dumps(header) + "\n")
            for t, text in rec.events:
                f.write(json.dumps([t, "o", text], ensure_ascii=False) + "\n")
            f.write(json.dumps([round(rec.t + 2, 3), "o", ""]) + "\n")


if __name__ == "__main__":
    main()
