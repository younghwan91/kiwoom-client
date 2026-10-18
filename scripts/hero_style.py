"""README 히어로 이미지 공통 스타일 (matplotlib).

사용:
    from hero_style import render_both, P
    def draw(fig, ax, p):      # p = 현재 모드의 팔레트 dict
        ...
    render_both(draw, out_dir="docs/images", name="hero", figsize=(12, 5))
→ docs/images/hero-light.png, docs/images/hero-dark.png (2x, 투명 배경 아님)

README 삽입 (배지 줄 바로 아래):
<picture>
  <source media="(prefers-color-scheme: dark)" srcset="docs/images/hero-dark.png">
  <img alt="<한 줄 설명>" src="docs/images/hero-light.png" width="100%">
</picture>

규칙 (dataviz 스킬 — 검증기 통과한 팔레트):
- 범주색은 아래 순서대로 고정 배정 (blue → amber → green → violet). 5번째 범주는 "기타"로 접는다.
- 연속값(크기)은 blue 단일 색 명암. 양/음은 blue/amber 두 극 + 중간 회색.
- 좋음/경고/위험 상태색은 status 슬롯만. 범주로 재사용 금지.
- 이중 y축 금지. 선 2px, 마커 ≥ 8px, 막대 ≤ 24px 두께. 격자는 1px 실선, 옅게.
- 글자는 항상 ink 색(검정/회색), 데이터 색으로 글자 쓰지 않는다.
- 시리즈 2개 이상이면 범례 또는 직접 라벨. 모든 점에 숫자 쓰지 않는다.
"""
from __future__ import annotations

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager

P = {
    "light": dict(
        surface="#ffffff", surface2="#f6f8fa", grid="#e5e7eb",
        ink="#0b0f19", ink2="#4b5563", ink3="#9ca3af",
        blue="#2563EB", amber="#B45309", green="#059669", violet="#7C3AED",
        blue_wash="#2563EB1a", amber_wash="#B453091a", green_wash="#0596691a",
        good="#059669", warn="#B45309", bad="#DC2626",
        seq=["#cde2fb", "#9ec5f4", "#6da7ec", "#3987e5", "#256abf", "#184f95", "#0d366b"],
    ),
    "dark": dict(
        surface="#0d1117", surface2="#161b22", grid="#30363d",
        ink="#e6edf3", ink2="#9da7b3", ink3="#6e7681",
        blue="#3B82F6", amber="#D97706", green="#059669", violet="#8B5CF6",
        blue_wash="#3B82F626", amber_wash="#D9770626", green_wash="#05966926",
        good="#059669", warn="#D97706", bad="#F87171",
        seq=["#0d366b", "#184f95", "#256abf", "#3987e5", "#6da7ec", "#9ec5f4", "#cde2fb"],
    ),
}

SERIES = ["blue", "amber", "green", "violet"]  # 범주 색 고정 순서


def _font():
    """시스템 글꼴 파일을 직접 등록한다 (matplotlib 캐시가 OTF 를 놓치는 경우 대비)."""
    import glob
    for pat in ("/usr/share/fonts/**/NotoSansKR*", "/usr/share/fonts/**/NotoSansCJK*", str(__import__("pathlib").Path.home() / ".local/share/fonts/**/NotoSansKR*")):
        for f in glob.glob(pat, recursive=True):
            try:
                font_manager.fontManager.addfont(f)
            except Exception:
                pass
    names = {f.name for f in font_manager.fontManager.ttflist}
    for name in ("Inter", "IBM Plex Sans", "Noto Sans KR", "Noto Sans CJK KR", "DejaVu Sans"):
        if name in names:
            return name
    return "DejaVu Sans"


def apply(mode: str) -> dict:
    p = P[mode]
    plt.rcParams.update({
        "font.family": "sans-serif", "font.sans-serif": [_font(), "Noto Sans KR", "DejaVu Sans"],
        "font.size": 12,
        "figure.facecolor": p["surface"], "axes.facecolor": p["surface"], "savefig.facecolor": p["surface"],
        "axes.edgecolor": p["grid"], "axes.labelcolor": p["ink2"],
        "axes.titlecolor": p["ink"], "axes.titleweight": "bold", "axes.titlesize": 15, "axes.titlelocation": "left",
        "axes.spines.top": False, "axes.spines.right": False,
        "axes.grid": True, "grid.color": p["grid"], "grid.linewidth": 1, "grid.linestyle": "-", "axes.axisbelow": True,
        "xtick.color": p["ink2"], "ytick.color": p["ink2"], "xtick.labelsize": 11, "ytick.labelsize": 11,
        "lines.linewidth": 2, "lines.solid_joinstyle": "round", "lines.solid_capstyle": "round",
        "lines.markersize": 8, "lines.markeredgewidth": 2, "lines.markeredgecolor": p["surface"],
        "legend.frameon": False, "legend.labelcolor": p["ink2"], "legend.fontsize": 11,
        "text.color": p["ink"],
        "savefig.dpi": 200, "savefig.bbox": "tight", "savefig.pad_inches": 0.25,
    })
    return p


def render_both(draw, out_dir="docs/images", name="hero", figsize=(12, 5), ncols=1, nrows=1, **subplot_kw):
    """draw(fig, ax_or_axes, p) 를 light/dark 로 두 번 호출해 PNG 두 장을 저장한다."""
    import pathlib
    out = pathlib.Path(out_dir); out.mkdir(parents=True, exist_ok=True)
    paths = []
    for mode in ("light", "dark"):
        p = apply(mode)
        fig, ax = plt.subplots(nrows, ncols, figsize=figsize, **subplot_kw)
        draw(fig, ax, p)
        path = out / f"{name}-{mode}.png"
        fig.savefig(path)
        plt.close(fig)
        paths.append(path)
    return paths


def caption(fig, text: str, p: dict):
    """그림 아래 한 줄 출처/설명 (ink3 색, 작은 글자)."""
    fig.text(0.0, -0.02, text, color=p["ink3"], fontsize=9.5, ha="left", va="top", transform=fig.transFigure)
