"""로고 마크·워드마크·파비콘 생성기 ("캔들 K", docs/brand.md 의 로고 콘셉트).

실행 (레포 루트):
    uv run --no-project --with fonttools --with cairosvg python scripts/make_logo.py
→ docs/images/brand/
    mark.svg               둥근 사각형 + 흰 마크 (파비콘·아바타)
    mark-white.svg         투명 배경 흰 마크 (문서 사이트 헤더처럼 색 배경 위)
    wordmark-light.svg     마크 + "kiwoom-client" (밝은 배경용)
    wordmark-dark.svg      같은 것, 어두운 배경용
    favicon-32.png, mark-512.png   (cairosvg 가 있으면 PNG 도 렌더)

워드마크 글자는 Noto Sans KR 윤곽선을 path 로 박아 넣는다 — 보는 쪽에 글꼴이 없어도 똑같이 보인다.
키움증권 로고·마젠타 계열 색은 쓰지 않는다(비공식 프로젝트). 색은 brand_tokens.P 에서 가져온다.
"""

from __future__ import annotations

import glob
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.ttLib import TTFont

from brand_tokens import P

OUT = Path(__file__).resolve().parent.parent / "docs" / "images" / "brand"
GRID = 64  # 마크 좌표계


def _glyph(color: str) -> str:
    """64×64 좌표계의 캔들 K. 세로획 = 캔들(꼬리+몸통), 두 팔 = 점 달린 연결선."""
    return (
        f'<g fill="{color}" stroke="{color}" stroke-linecap="round" stroke-linejoin="round">'
        # 꼬리(위아래 심지)
        '<line x1="22" y1="9" x2="22" y2="55" stroke-width="4" fill="none"/>'
        # 몸통
        '<rect x="15" y="17" width="14" height="30" rx="3" stroke="none"/>'
        # 위 팔 → 노드
        '<line x1="29" y1="33" x2="44" y2="19" stroke-width="5.5" fill="none"/>'
        '<circle cx="46.5" cy="16.5" r="5.5" stroke="none"/>'
        # 아래 팔 → 노드
        '<line x1="31" y1="35" x2="44" y2="47" stroke-width="5.5" fill="none"/>'
        '<circle cx="46.5" cy="49.5" r="5.5" stroke="none"/>'
        "</g>"
    )


def mark_svg(bg: str | None, fg: str, size: int = GRID) -> str:
    rect = f'<rect width="64" height="64" rx="14" fill="{bg}"/>' if bg else ""
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}" '
        f'viewBox="0 0 64 64">{rect}{_glyph(fg)}</svg>\n'
    )


def _font(weight: str) -> TTFont:
    pats = [
        f"/usr/share/fonts/**/NotoSansKR-{weight}.*",
        str(Path.home() / f".local/share/fonts/**/NotoSansKR-{weight}.*"),
    ]
    for pat in pats:
        for f in sorted(glob.glob(pat, recursive=True)):
            return TTFont(f)
    raise SystemExit(f"Noto Sans KR {weight} 글꼴을 찾지 못했다 (fonts-noto-cjk 또는 NotoSansKR 설치)")


def text_path(text: str, font: TTFont, x: float, baseline: float, px: float) -> tuple[str, float]:
    """text 를 SVG path d 로. (d, 진행 폭) 반환. px = 글자 크기(em)."""
    gs = font.getGlyphSet()
    cmap = font.getBestCmap()
    upm = font["head"].unitsPerEm
    s = px / upm
    pen = SVGPathPen(gs)
    cur = x
    for ch in text:
        name = cmap[ord(ch)]
        tp = TransformPen(pen, (s, 0, 0, -s, cur, baseline))
        gs[name].draw(tp)
        cur += gs[name].width * s
    return pen.getCommands(), cur - x


def wordmark_svg(mode: str) -> str:
    p = P[mode]
    bold, regular = _font("Bold"), _font("Regular")
    h = 64
    px = 34.0
    baseline = 44.0
    x0 = 64 + 16
    d1, w1 = text_path("kiwoom", bold, x0, baseline, px)
    d2, w2 = text_path("-client", regular, x0 + w1 + 1, baseline, px)
    w = round(x0 + w1 + 1 + w2 + 4)
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{w * 2}" height="{h * 2}" '
        f'viewBox="0 0 {w} {h}" role="img" aria-label="kiwoom-client">'
        f'<rect width="64" height="64" rx="14" fill="{p["blue"]}"/>{_glyph("#ffffff")}'
        f'<path d="{d1}" fill="{p["ink"]}"/><path d="{d2}" fill="{p["ink2"]}"/>'
        "</svg>\n"
    )


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    files = {
        "mark.svg": mark_svg(P["light"]["blue"], "#ffffff"),
        "mark-white.svg": mark_svg(None, "#ffffff"),
        "wordmark-light.svg": wordmark_svg("light"),
        "wordmark-dark.svg": wordmark_svg("dark"),
    }
    for name, svg in files.items():
        (OUT / name).write_text(svg, encoding="utf-8")
        print(OUT / name)
    try:
        import cairosvg
    except ImportError:
        print("cairosvg 없음 — PNG 는 건너뜀")
        return
    for name, size in (("favicon-32.png", 32), ("mark-512.png", 512)):
        cairosvg.svg2png(bytestring=files["mark.svg"].encode(), write_to=str(OUT / name),
                         output_width=size, output_height=size)
        print(OUT / name)


if __name__ == "__main__":
    main()
