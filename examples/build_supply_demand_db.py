#!/usr/bin/env python3
"""코스피·코스닥 전 종목의 최근 N일 투자자별 수급을 SQLite DB로 수집.

우리가 만든 kiwoom_rest_api 사용. TR 은 단일(ka10059)이라 라이브러리 기본
Rate Limiter(1 req/s) 에 맞춰 종목당 1회 호출한다(전수 ~70분).

테이블:
  stocks(code, name, market, sector, kind)
  supply_demand(code, date, close, flu_rt, acc_trde_qty,
                individual, foreign_, institution, + 기관 세부)

사용법:
    # 동작 확인 (5종목만)
    python examples/build_supply_demand_db.py --limit 5
    # 코스피만, 최근 30일
    python examples/build_supply_demand_db.py --market kospi --days 30
    # 전수, 실서버
    python examples/build_supply_demand_db.py --market all --prod
    # 중단 후 이어받기 (이미 수집된 종목 건너뜀)
    python examples/build_supply_demand_db.py --resume
"""

from __future__ import annotations

import argparse
import sqlite3
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))

from kiwoom_rest_api import KiwoomAPI  # noqa: E402
from kiwoom_rest_api.base import KiwoomAPIError  # noqa: E402

MARKETS = {"kospi": "0", "kosdaq": "10"}  # ka10099 mrkt_tp

# ka10059 응답 → DB 컬럼 매핑 (투자주체별 순매수)
INVESTOR_FIELDS = {
    "individual": "ind_invsr",     # 개인
    "foreign_": "frgnr_invsr",     # 외국인
    "institution": "orgn",         # 기관계
    "fnnc_invt": "fnnc_invt",      # 금융투자
    "insrnc": "insrnc",            # 보험
    "invtrt": "invtrt",            # 투신
    "bank": "bank",                # 은행
    "penfnd_etc": "penfnd_etc",    # 연기금등
    "samo_fund": "samo_fund",      # 사모펀드
    "natn": "natn",                # 국가
    "etc_corp": "etc_corp",        # 기타법인
}


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
    s = (s or "").replace("+", "").strip()
    try:
        return int(s)
    except ValueError:
        return 0


def to_float(s: str) -> float:
    s = (s or "").replace("+", "").strip()
    try:
        return float(s)
    except ValueError:
        return 0.0


def is_common_stock(row: dict) -> bool:
    """보통주만 True. ETF/ETN/리츠(marketName!=거래소/코스닥)와 우선주(코드 끝!=0) 제외."""
    return row["market"] in ("거래소", "코스닥") and row["code"].endswith("0")


def init_db(con: sqlite3.Connection) -> None:
    con.executescript(
        """
        CREATE TABLE IF NOT EXISTS stocks (
            code   TEXT PRIMARY KEY,
            name   TEXT,
            market TEXT,
            sector TEXT,
            kind   TEXT
        );
        CREATE TABLE IF NOT EXISTS supply_demand (
            code         TEXT NOT NULL,
            date         TEXT NOT NULL,
            close        INTEGER,
            flu_rt       REAL,
            acc_trde_qty INTEGER,
            individual   INTEGER,
            foreign_     INTEGER,
            institution  INTEGER,
            fnnc_invt    INTEGER,
            insrnc       INTEGER,
            invtrt       INTEGER,
            bank         INTEGER,
            penfnd_etc   INTEGER,
            samo_fund    INTEGER,
            natn         INTEGER,
            etc_corp     INTEGER,
            PRIMARY KEY (code, date)
        );
        CREATE INDEX IF NOT EXISTS idx_sd_date ON supply_demand(date);
        """
    )
    con.commit()


def fetch_stock_list(api: KiwoomAPI, markets: list[str]) -> list[dict]:
    out = []
    for m in markets:
        r = api.stock_info.stock_info_list(mrkt_tp=MARKETS[m])
        for row in r.get("list", []):
            out.append(
                {
                    "code": row.get("code", "").strip(),
                    "name": row.get("name", "").strip(),
                    "market": row.get("marketName", "").strip(),
                    "sector": row.get("upName", "").strip(),
                    "kind": row.get("kind", "").strip(),
                }
            )
    return out


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--prod", action="store_true", help="실서버 사용")
    parser.add_argument("--market", choices=["kospi", "kosdaq", "all"], default="all")
    parser.add_argument("--days", type=int, default=30, help="최근 N일")
    parser.add_argument("--limit", type=int, default=0, help="앞에서 N종목만 (테스트)")
    parser.add_argument("--db", default=str(ROOT / "data" / "supply_demand.db"))
    parser.add_argument("--resume", action="store_true", help="이미 수집된 종목 건너뜀")
    parser.add_argument("--all-kinds", action="store_true",
                        help="ETF/ETN/리츠/우선주 등 모두 포함 (기본: 보통주만)")
    args = parser.parse_args()

    db_path = Path(args.db)
    db_path.parent.mkdir(parents=True, exist_ok=True)
    con = sqlite3.connect(db_path)
    init_db(con)

    ak, sk = load_keys()
    api = KiwoomAPI(app_key=ak, app_secret=sk, is_mock=not args.prod)  # 기본 1 req/s + 429 재시도
    api.login()

    markets = ["kospi", "kosdaq"] if args.market == "all" else [args.market]
    stocks = fetch_stock_list(api, markets)
    if not args.all_kinds:
        stocks = [s for s in stocks if is_common_stock(s)]  # 보통주만 (ETF/우선주 제외)
    if args.limit:
        stocks = stocks[: args.limit]

    # stocks 마스터 upsert
    con.executemany(
        "INSERT OR REPLACE INTO stocks(code,name,market,sector,kind) VALUES(?,?,?,?,?)",
        [(s["code"], s["name"], s["market"], s["sector"], s["kind"]) for s in stocks],
    )
    con.commit()

    cutoff = time.strftime("%Y%m%d", time.localtime(time.time() - args.days * 86400))
    today = time.strftime("%Y%m%d")
    server = "모의" if not args.prod else "실서버"
    print(f"🔌 {server} | 시장={args.market} | 종목 {len(stocks)}개 | 최근 {args.days}일(>= {cutoff})")
    print(f"💾 DB: {db_path}\n")

    done = skipped = failed = rows_total = 0
    t0 = time.monotonic()
    cols = ["code", "date", "close", "flu_rt", "acc_trde_qty", *INVESTOR_FIELDS.keys()]
    placeholders = ",".join("?" * len(cols))
    insert_sql = f"INSERT OR REPLACE INTO supply_demand({','.join(cols)}) VALUES({placeholders})"

    for i, s in enumerate(stocks, 1):
        code = s["code"]
        if args.resume:
            cur = con.execute(
                "SELECT COUNT(*) FROM supply_demand WHERE code=? AND date>=?", (code, cutoff)
            )
            if cur.fetchone()[0] > 0:
                skipped += 1
                continue
        try:
            r = api.stock_info.investor_institution_by_stock(
                dt=today, stk_cd=code, amt_qty_tp="2", trde_tp="0", unit_tp="1"
            )
            rows = r.get("stk_invsr_orgn", []) or []
            batch = []
            for row in rows:
                d = row.get("dt", "")
                if d < cutoff:
                    continue
                rec = [
                    code, d, to_int(row.get("cur_prc")), to_float(row.get("flu_rt")),
                    to_int(row.get("acc_trde_qty")),
                    *[to_int(row.get(src)) for src in INVESTOR_FIELDS.values()],
                ]
                batch.append(rec)
            if batch:
                con.executemany(insert_sql, batch)
                con.commit()
                rows_total += len(batch)
            done += 1
        except KiwoomAPIError as e:
            failed += 1
            print(f"  ⚠️ {code} {s['name']}: rc={e.code} {e.message[:50]}")
        except Exception as e:  # noqa: BLE001
            failed += 1
            print(f"  💥 {code} {s['name']}: {type(e).__name__}: {e}")

        if i % 50 == 0 or i == len(stocks):
            el = time.monotonic() - t0
            rate = i / el if el else 0
            eta = (len(stocks) - i) / rate if rate else 0
            print(f"  [{i}/{len(stocks)}] 수집 {done} 건너뜀 {skipped} 실패 {failed} "
                  f"| {rows_total:,}행 | {rate:.1f}종목/s | ETA {eta/60:.1f}분")

    api.close()
    con.close()
    print(f"\n✅ 완료: 종목 {done}, 건너뜀 {skipped}, 실패 {failed}, 총 {rows_total:,}행, "
          f"{(time.monotonic()-t0)/60:.1f}분")
    print(f"💾 {db_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
