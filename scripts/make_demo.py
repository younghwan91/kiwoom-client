"""README "30초 데모" 그림: MCP 클라이언트에서 시세를 묻고, 실주문은 가드에 막히는 대화 (예시).

실행 (레포 루트):
    uv run --no-project --with cairosvg python scripts/make_demo.py
→ docs/images/demo-mcp-{ko,en}-{light,dark}.png

**실서버를 부르지 않고 그린 예시 그림**이다. 시세 값은 가상이고, 그림 안에 "예시" 표시를 넣는다.
도구 이름(stock_info_basic_stock_info)과 가드 동작(실전투자에서 KIWOOM_MCP_ALLOW_LIVE_ORDERS 없이는
주문 도구가 등록되지 않음)은 코드와 같다 — tests/test_mcp_guard.py, mcp/tools.py.
글꼴: Noto Sans KR, DejaVu Sans Mono.
"""

from __future__ import annotations

import sys
from pathlib import Path
from xml.sax.saxutils import escape

sys.path.insert(0, str(Path(__file__).resolve().parent))

import cairosvg
from brand_tokens import P

OUT = Path(__file__).resolve().parent.parent / "docs" / "images"
W = 960
SANS = "Noto Sans KR"
MONO = "DejaVu Sans Mono"

# (종류, 텍스트) — user / call / result / say / guard
SCRIPT = {
    "ko": dict(
        title="MCP 클라이언트 · kiwoom-client-mcp (실전투자 서버)",
        badge="예시",
        lines=[
            ("user", "삼성전자 지금 얼마야?"),
            ("call", 'stock_info_basic_stock_info  {"params": {"stk_cd": "005930"}}'),
            ("result", '{"stk_cd": "005930", "cur_prc": "+70000", "flu_rt": "+1.45", ...}'),
            ("say", "삼성전자는 70,000원, 전일 대비 +1.45% 입니다."),
            ("user", "그럼 10주 시장가로 사 줘."),
            ("guard", "지금 연결된 kiwoom-client 서버에는 주문 도구가 없어서 주문할 수 없습니다."),
            ("guard2", "실전투자에서 주문하려면 KIWOOM_MCP_ALLOW_LIVE_ORDERS=true 로 서버를 다시 띄워야 합니다."),
        ],
        note="실서버를 호출하지 않고 만든 예시 화면입니다. 시세 값은 가상입니다.",
    ),
    "en": dict(
        title="MCP client · kiwoom-client-mcp (live server)",
        badge="EXAMPLE",
        lines=[
            ("user", "What's Samsung Electronics trading at?"),
            ("call", 'stock_info_basic_stock_info  {"params": {"stk_cd": "005930"}}'),
            ("result", '{"stk_cd": "005930", "cur_prc": "+70000", "flu_rt": "+1.45", ...}'),
            ("say", "Samsung Electronics is at 70,000 KRW, up 1.45% on the day."),
            ("user", "Buy 10 shares at market, then."),
            ("guard", "The kiwoom-client server I'm connected to has no order tools, so I can't place it."),
            ("guard2", "On a live account, restart the server with KIWOOM_MCP_ALLOW_LIVE_ORDERS=true to allow orders."),
        ],
        note="Illustration made without calling the live server. Prices are made up.",
    ),
}


def text(x, y, s, size, fill, family=SANS, weight=400, anchor="start"):
    return (
        f'<text x="{x}" y="{y}" font-family="{family}" font-size="{size}" font-weight="{weight}" '
        f'fill="{fill}" text-anchor="{anchor}" xml:space="preserve">{escape(s)}</text>'
    )


def svg(lang: str, mode: str) -> str:
    p = P[mode]
    sc = SCRIPT[lang]
    pad, top = 32, 44
    body: list[str] = []
    y = top + 30
    for kind, s in sc["lines"]:
        if kind == "user":
            y += 10
            body.append(
                f'<rect x="{pad}" y="{y - 24}" width="{W - 2 * pad}" height="38" rx="8" '
                f'fill="{p["surface2"]}"/>'
            )
            body.append(text(pad + 16, y, "›", 20, p["ink3"], weight=700))
            body.append(text(pad + 40, y, s, 18, p["ink"], weight=700))
            y += 44
        elif kind == "call":
            body.append(f'<circle cx="{pad + 22}" cy="{y - 6}" r="5" fill="{p["blue"]}"/>')
            body.append(text(pad + 40, y, "kiwoom-client · ", 15, p["ink2"], MONO))
            body.append(text(pad + 40 + 16 * 9.05, y, s, 15, p["ink"], MONO))
            y += 28
        elif kind == "result":
            body.append(text(pad + 40, y, "└ " + s, 15, p["ink3"], MONO))
            y += 38
        elif kind == "say":
            body.append(f'<circle cx="{pad + 22}" cy="{y - 6}" r="5" fill="{p["ink2"]}"/>')
            body.append(text(pad + 40, y, s, 17, p["ink"]))
            y += 36
        elif kind == "guard":
            box_h = 74
            body.append(
                f'<rect x="{pad + 30}" y="{y - 26}" width="{W - 2 * pad - 30}" height="{box_h}" rx="8" '
                f'fill="{p["good"]}" fill-opacity="0.12" stroke="{p["good"]}" stroke-opacity="0.6"/>'
            )
            body.append(f'<circle cx="{pad + 22}" cy="{y - 6}" r="5" fill="{p["good"]}"/>')
            body.append(text(pad + 46, y, s, 17, p["ink"]))
            y += 30
        elif kind == "guard2":
            body.append(text(pad + 46, y, s, 15, p["ink2"]))
            y += 50
    h = y + 24
    head = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{h}" viewBox="0 0 {W} {h}">',
        f'<rect x="0.5" y="0.5" width="{W - 1}" height="{h - 1}" rx="12" fill="{p["surface"]}" '
        f'stroke="{p["grid"]}"/>',
        f'<path d="M0.5 44 H{W - 0.5}" stroke="{p["grid"]}"/>',
    ]
    for i, c in enumerate((p["ink3"], p["ink3"], p["ink3"])):
        head.append(f'<circle cx="{24 + i * 18}" cy="22" r="5.5" fill="{c}" fill-opacity="0.5"/>')
    head.append(text(W / 2, 28, sc["title"], 14, p["ink2"], anchor="middle"))
    # "예시" 배지 (오른쪽 위)
    bw = 16 + len(sc["badge"]) * (17 if lang == "ko" else 9.5)
    head.append(
        f'<rect x="{W - 20 - bw}" y="11" width="{bw}" height="22" rx="11" fill="{p["warn"]}"/>'
    )
    head.append(text(W - 20 - bw / 2, 27, sc["badge"], 13, "#ffffff", weight=700, anchor="middle"))
    foot = [text(pad, h - 18, sc["note"], 13, p["ink3"]), "</svg>"]
    return "".join(head + body + foot)


def main() -> None:
    for lang in SCRIPT:
        for mode in ("light", "dark"):
            out = OUT / f"demo-mcp-{lang}-{mode}.png"
            cairosvg.svg2png(bytestring=svg(lang, mode).encode(), write_to=str(out), scale=2)
            print(out)


if __name__ == "__main__":
    main()
