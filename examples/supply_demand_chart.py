#!/usr/bin/env python3
"""삼성전자 투자자별 수급(개인/외국인/기관) 차트 — 우리가 만든 kiwoom_rest_api 사용.

ka10059 (투자자기관별종목별요청) 응답으로 일별 순매수를 받아
  - 상단: 종가 추이
  - 하단: 개인/외국인/기관 누적 순매수
를 그려 PNG 로 저장한다.

사용법:
    python examples/supply_demand_chart.py            # 모의서버
    python examples/supply_demand_chart.py --prod     # 실서버
    python examples/supply_demand_chart.py --stk 000660
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")  # GUI 없는 환경(WSL)에서도 PNG 저장 가능
import matplotlib.font_manager as fm  # noqa: E402
import matplotlib.pyplot as plt  # noqa: E402

# 한글 폰트(나눔고딕) 등록 — WSL 사용자 폰트 디렉터리
for _fp in (Path.home() / ".local/share/fonts").glob("NanumGothic*.ttf"):
    fm.fontManager.addfont(str(_fp))
if any("NanumGothic" in f.name for f in fm.fontManager.ttflist):
    plt.rcParams["font.family"] = "NanumGothic"
plt.rcParams["axes.unicode_minus"] = False  # 음수 부호 깨짐 방지

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))

from kiwoom_rest_api import KiwoomAPI  # noqa: E402


def load_keys() -> tuple[str, str]:
    ak = sk = ""
    for line in (ROOT / ".env").read_text().splitlines():
        line = line.strip()
        if line.startswith("#") or "=" not in line:
            continue
        k, v = line.split("=", 1)
        v = v.strip().strip('"').strip("'")
        if k.strip() == "KIWOOM_APP_KEY":
            ak = v
        elif k.strip() == "KIWOOM_APP_SECRET":
            sk = v
    return ak, sk


def to_int(s: str) -> int:
    """'+322500' / '-1979879' / '' → int."""
    s = (s or "").replace("+", "").strip()
    try:
        return int(s)
    except ValueError:
        return 0


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--prod", action="store_true", help="실서버 사용")
    parser.add_argument("--stk", default="005930", help="종목코드 (기본 삼성전자)")
    parser.add_argument("--out", default=str(ROOT / "examples" / "supply_demand_005930.png"))
    args = parser.parse_args()

    ak, sk = load_keys()
    api = KiwoomAPI(app_key=ak, app_secret=sk, is_mock=not args.prod, rate_limit=4.0)
    api.login()

    # 일별 투자자/기관 순매수 (수량 기준). dt 는 조회 기준일.
    import time

    resp = api.stock_info.investor_institution_by_stock(
        dt=time.strftime("%Y%m%d"),
        stk_cd=args.stk,
        amt_qty_tp="2",   # 1=금액, 2=수량
        trde_tp="0",      # 0=순매수
        unit_tp="1",      # 1=단주
    )
    api.close()

    rows = resp.get("stk_invsr_orgn", [])
    if not rows:
        print(f"데이터 없음: {resp.get('return_msg')}")
        return 1

    # API 는 최신→과거 순. 시간순으로 뒤집는다.
    rows = list(reversed(rows))
    dates = [r["dt"] for r in rows]
    price = [abs(to_int(r["cur_prc"])) for r in rows]
    indiv = [to_int(r["ind_invsr"]) for r in rows]
    forgn = [to_int(r["frgnr_invsr"]) for r in rows]
    instn = [to_int(r["orgn"]) for r in rows]

    def cumsum(xs: list[int]) -> list[int]:
        out, acc = [], 0
        for x in xs:
            acc += x
            out.append(acc)
        return out

    cum_i, cum_f, cum_o = cumsum(indiv), cumsum(forgn), cumsum(instn)
    x = range(len(dates))

    fig, (ax1, ax2) = plt.subplots(
        2, 1, figsize=(13, 8), sharex=True, gridspec_kw={"height_ratios": [1, 1.4]}
    )
    server = "모의" if not args.prod else "실서버"
    fig.suptitle(f"삼성전자 ({args.stk}) 투자자별 수급 — Kiwoom REST API [{server}]",
                 fontsize=14, fontweight="bold")

    # 상단: 종가
    ax1.plot(x, price, color="black", lw=1.4)
    ax1.set_ylabel("종가 (원)")
    ax1.grid(True, alpha=0.3)

    # 하단: 누적 순매수
    ax2.plot(x, cum_i, label="개인", color="#1f77b4", lw=1.6)
    ax2.plot(x, cum_f, label="외국인", color="#d62728", lw=1.6)
    ax2.plot(x, cum_o, label="기관", color="#2ca02c", lw=1.6)
    ax2.axhline(0, color="gray", lw=0.8, ls="--")
    ax2.set_ylabel("누적 순매수 (주)")
    ax2.grid(True, alpha=0.3)
    ax2.legend(loc="best")

    # x 축 라벨 솎아내기
    step = max(1, len(dates) // 10)
    ticks = list(x)[::step]
    ax2.set_xticks(ticks)
    ax2.set_xticklabels([dates[i] for i in ticks], rotation=45, ha="right", fontsize=8)

    fig.tight_layout(rect=(0, 0, 1, 0.97))
    fig.savefig(args.out, dpi=120)
    print(f"기간: {dates[0]} ~ {dates[-1]} ({len(dates)}일)")
    print(f"최종 누적 순매수 — 개인:{cum_i[-1]:,}  외국인:{cum_f[-1]:,}  기관:{cum_o[-1]:,}")
    print(f"차트 저장: {args.out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
