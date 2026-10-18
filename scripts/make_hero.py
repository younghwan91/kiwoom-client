"""README 히어로 이미지: 라이브러리가 감싼 키움 엔드포인트 전체를 도메인별 타일 모자이크로.

실행 (레포 루트):
    uv run --with matplotlib --with numpy python scripts/make_hero.py
→ docs/images/hero-light.png, docs/images/hero-dark.png

목록은 네트워크 없이 코드에서만 센다:
- REST: ``kiwoom_client._registry.MODULE_NAMES`` 의 각 모듈 클래스 메서드 소스에서
  ``api_id``("ka10001" 꼴)
- 조건검색: ``kiwoom_client.domestic.condition_search.ConditionSearch`` 의 ``trnm`` 페이로드 메서드
- 실시간: ``kiwoom_client.websocket.REALTIME_TYPES``
"""

from __future__ import annotations

import inspect
import math
import re
import sys
from dataclasses import dataclass
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from hero_style import caption, render_both
from matplotlib.patches import Rectangle

from kiwoom_client import _registry
from kiwoom_client.domestic.condition_search import ConditionSearch
from kiwoom_client.websocket import REALTIME_TYPES

GENERATED = "2026-10-19"
API_ID = re.compile(r'"(k[a-z]\d{5})"')
TRNM = re.compile(r'"trnm":\s*"([A-Z]+)"')

LABELS = {
    "account": "Account",
    "stock_info": "Stock info",
    "market": "Market",
    "ranking": "Ranking",
    "chart": "Chart",
    "elw": "ELW",
    "etf": "ETF",
    "order": "Order",
    "sector": "Sector",
    "credit_order": "Credit order",
    "foreign_institution": "Foreign / inst.",
    "slb": "SLB",
    "theme": "Theme",
    "short_selling": "Short selling",
}


@dataclass
class Block:
    label: str
    ids: list[str]
    kind: str  # "rest" | "ws"

    @property
    def n(self) -> int:
        return len(self.ids)


def collect() -> tuple[list[Block], list[Block]]:
    """(REST 블록, WebSocket 블록) — 코드 정적 목록."""
    rest: list[Block] = []
    for name in _registry.MODULE_NAMES:
        cls = inspect.getattr_static(_registry.ModuleRegistry, name).fget.__annotations__["return"]
        cls = cls.split("[")[0]  # "Account[ResponseT]" → "Account"
        mod_cls = getattr(_registry, cls)
        if mod_cls is ConditionSearch:
            continue
        ids: list[str] = []
        for _, fn in inspect.getmembers(mod_cls, inspect.isfunction):
            if fn.__name__.startswith("_"):
                continue
            ids.extend(API_ID.findall(inspect.getsource(fn)))
        if len(ids) != len(set(ids)):
            raise SystemExit(f"{name}: duplicate api_id")
        rest.append(Block(LABELS[name], ids, "rest"))
    rest.sort(key=lambda b: -b.n)

    # 공개 메서드 하나 = 조건검색 호출 하나 (trnm 페이로드를 직접 만들거나 다른 메서드에 위임)
    cond = [
        fn.__name__
        for _, fn in inspect.getmembers(ConditionSearch, inspect.isfunction)
        if not fn.__name__.startswith("_")
    ]
    if not TRNM.findall(inspect.getsource(ConditionSearch)):
        raise SystemExit("ConditionSearch: no trnm payloads found")
    ws = [
        Block("Real-time types", list(REALTIME_TYPES), "ws"),
        Block("Condition search", cond, "ws"),
    ]
    return rest, ws


# ---- layout -----------------------------------------------------------------
ROWS = 6            # 블록 한 개의 타일 행 수
GAP_BLOCK = 1.0     # 블록 사이 간격 (타일 단위)
GAP_BAND = 2.2      # 밴드(줄) 사이 간격 — 라벨 자리 포함
LABEL_PT = 10.5
TILE_INSET = 0.04   # 타일 사이 표면색 간격 (≈2px @200dpi)


def _text_in(fig, text: str, size: float, weight: str = "normal") -> float:
    """글자 폭(inch) — 렌더러로 실측."""
    t = fig.text(0, 0, text, fontsize=size, fontweight=weight)
    w = t.get_window_extent(fig.canvas.get_renderer()).width / fig.dpi
    t.remove()
    return w


def pack(fig, blocks: list[Block], max_w: float, unit_in: float):
    """블록을 왼→오로 흘리고 넘치면 다음 밴드로. [(block, x, cols, label_w)] 의 밴드 목록."""
    bands: list[list[tuple[Block, float, int, float]]] = [[]]
    x = 0.0
    for b in blocks:
        cols = math.ceil(b.n / ROWS)
        label_w = _text_in(fig, f"{b.label} {b.n}", LABEL_PT, "bold") / unit_in + 0.25
        adv = max(cols, label_w)
        if x > 0 and x + adv > max_w:
            bands.append([])
            x = 0.0
        bands[-1].append((b, x, cols, label_w))
        x += adv + GAP_BLOCK
    return bands


def draw(fig, ax, p):
    rest, ws = collect()
    blocks = rest + ws
    n_rest = sum(b.n for b in rest)
    n_ws = sum(b.n for b in ws)

    fig.subplots_adjust(left=0, right=1, top=1, bottom=0)
    fig_w, fig_h = fig.get_size_inches()
    max_w = 42.0
    unit_in = fig_w / max_w
    for _ in range(2):  # 라벨 폭(타일 단위)이 unit_in 에 의존하므로 두 번 돌려 수렴
        bands = pack(fig, blocks, max_w, unit_in)
        used_w = max(x + max(cols, lw) for band in bands for _, x, cols, lw in band)
        unit_in = fig_w / used_w

    top_pad, bottom_pad = 2.6, 2.2  # 제목 / 범례 자리 (타일 단위)
    body_h = len(bands) * (ROWS + GAP_BAND) - GAP_BAND
    total_h = top_pad + body_h + bottom_pad
    units_h = used_w * fig_h / fig_w  # 그림 비율을 꽉 채우는 높이 (타일 단위)
    ax.set_xlim(0, used_w)
    ax.set_ylim(max(total_h, units_h), 0)  # 위에서 아래로
    ax.set_aspect("equal", adjustable="box")
    ax.set_anchor("N")
    ax.axis("off")
    ax.grid(False)

    title = (f"{n_rest} Kiwoom REST endpoints and {n_ws} WebSocket calls behind one client, "
             "grouped by domain")
    ax.text(0, 0.3, title, color=p["ink"], fontsize=15, fontweight="bold", ha="left", va="top")

    colors = {"rest": p["blue"], "ws": p["amber"]}
    y = top_pad
    for band in bands:
        for b, x, _cols, _ in band:
            ax.text(x, y - 0.45, b.label, color=p["ink"], fontsize=LABEL_PT, fontweight="bold",
                    ha="left", va="baseline")
            name_w = _text_in(fig, b.label, LABEL_PT, "bold") / unit_in
            ax.text(x + name_w + 0.25, y - 0.45, str(b.n), color=p["ink2"], fontsize=LABEL_PT,
                    ha="left", va="baseline")
            for i in range(b.n):
                c, r = divmod(i, ROWS)
                ax.add_patch(Rectangle(
                    (x + c + TILE_INSET, y + r + TILE_INSET),
                    1 - 2 * TILE_INSET, 1 - 2 * TILE_INSET,
                    facecolor=colors[b.kind], edgecolor="none",
                ))
        y += ROWS + GAP_BAND

    # 범례: 색 = 전송 방식 (글자는 ink 색만)
    lx, ly = 0.0, total_h - 0.9
    for k, label in (("rest", "REST (api_id)"), ("ws", "WebSocket (trnm / real-time type)")):
        ax.add_patch(Rectangle((lx, ly - 0.35), 0.7, 0.7, facecolor=colors[k], edgecolor="none"))
        ax.text(lx + 1.0, ly, label, color=p["ink2"], fontsize=10, ha="left", va="center")
        lx += 1.0 + _text_in(fig, label, 10) / unit_in + 1.5
    ax.text(used_w, ly, "1 tile = 1 endpoint", color=p["ink3"], fontsize=10,
            ha="right", va="center")

    caption(
        fig,
        "Counted statically from kiwoom_client.domestic (api_id per method), "
        "ConditionSearch trnm payloads and websocket.REALTIME_TYPES · generated "
        + GENERATED,
        p,
    )


if __name__ == "__main__":
    rest, ws = collect()
    for b in rest + ws:
        print(f"{b.label:18s} {b.n:3d}  {b.kind}")
    print("REST total:", sum(b.n for b in rest), " WS total:", sum(b.n for b in ws))
    out = Path(__file__).resolve().parent.parent / "docs" / "images"
    for path in render_both(draw, out_dir=str(out), name="hero", figsize=(12, 6)):
        print("wrote", path)
