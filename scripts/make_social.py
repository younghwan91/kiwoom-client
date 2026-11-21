"""GitHub 소셜 프리뷰 이미지 (1280×640 PNG) 생성기.

실행 (레포 루트):
    uv run --extra mcp --with cairosvg python scripts/make_social.py
→ docs/images/social-preview.png

숫자는 네트워크 없이 코드에서 센다(REST = MCP 가 노출하는 REST 도구 수, 실시간 = REALTIME_TYPES).
업로드는 레포 설정(Settings → General → Social preview)에서 사람이 한다.
글꼴: Noto Sans KR, DejaVu Sans Mono (시스템에 설치돼 있어야 한다).
"""

from __future__ import annotations

import sys
from pathlib import Path
from xml.sax.saxutils import escape

sys.path.insert(0, str(Path(__file__).resolve().parent))

import cairosvg
from brand_tokens import P
from make_logo import _glyph

from kiwoom_client.mcp.tools import discover_rest_tools
from kiwoom_client.websocket import REALTIME_TYPES

OUT = Path(__file__).resolve().parent.parent / "docs" / "images" / "social-preview.png"
W, H = 1280, 640
SANS = "Noto Sans KR"
MONO = "DejaVu Sans Mono"


def t(x, y, s, size, fill, weight=400, family=SANS, anchor="start"):
    return (
        f'<text x="{x}" y="{y}" font-family="{family}" font-size="{size}" font-weight="{weight}" '
        f'fill="{fill}" text-anchor="{anchor}">{escape(s)}</text>'
    )


def svg() -> str:
    p = P["dark"]
    n_rest = len(discover_rest_tools())
    n_rt = len(REALTIME_TYPES)
    m = 88  # 좌우 여백
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">',
        f'<rect width="{W}" height="{H}" fill="{p["surface"]}"/>',
        # 마크 + 워드마크
        f'<g transform="translate({m} 86) scale(1.5)">'
        f'<rect width="64" height="64" rx="14" fill="{p["blue"]}"/>{_glyph("#ffffff")}</g>',
        f'<text x="{m + 96 + 28}" y="155" font-family="{SANS}" font-size="64">'
        f'<tspan font-weight="700" fill="{p["ink"]}">kiwoom</tspan>'
        f'<tspan font-weight="400" fill="{p["ink2"]}">-client</tspan></text>',
        # 태그라인
        t(m, 284, "The Kiwoom REST API,", 54, p["ink"], 700),
        t(m, 350, "from Python and AI agents.", 54, p["ink"], 700),
        t(m, 408, "키움 REST API, 파이썬과 AI 에이전트로.", 30, p["ink2"]),
    ]
    # 사실 줄 (숫자는 코드에서 센 값)
    facts = [f"{n_rest} REST endpoints", f"{n_rt} real-time types", "MCP server", "live-order guard"]
    sep = f'<tspan fill="{p["blue"]}" font-weight="700">  ·  </tspan>'
    body = sep.join(escape(f) for f in facts)
    parts.append(
        f'<text x="{m}" y="486" font-family="{SANS}" font-size="26" fill="{p["ink"]}" '
        f'xml:space="preserve">{body}</text>'
    )
    # 설치 명령 칩
    cmd = "$ pip install kiwoom-client"
    parts += [
        f'<rect x="{m}" y="526" width="{len(cmd) * 15.7 + 48:.0f}" height="58" rx="10" '
        f'fill="{p["surface2"]}" stroke="{p["grid"]}"/>',
        t(m + 24, 564, cmd, 26, p["ink"], 400, MONO),
        t(W - m, 564, "Unofficial · not affiliated with Kiwoom Securities", 20, p["ink3"],
          anchor="end"),
        # 위쪽 브랜드 띠
        f'<rect width="{W}" height="8" fill="{p["blue"]}"/>',
        "</svg>",
    ]
    return "".join(parts)


def main() -> None:
    OUT.parent.mkdir(parents=True, exist_ok=True)
    cairosvg.svg2png(bytestring=svg().encode(), write_to=str(OUT), output_width=W, output_height=H)
    print(OUT)


if __name__ == "__main__":
    main()
