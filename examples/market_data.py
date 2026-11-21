"""Market data example: stock quote, daily chart, top volume ranking, sector index."""

import os
import sys

from kiwoom_client import KiwoomAPI


def get_credentials() -> tuple[str, str]:
    app_key = os.environ.get("KIWOOM_APP_KEY")
    app_secret = os.environ.get("KIWOOM_APP_SECRET")
    if not app_key or not app_secret:
        print("Error: KIWOOM_APP_KEY and KIWOOM_APP_SECRET environment variables must be set.")
        sys.exit(1)
    return app_key, app_secret


def main() -> None:
    app_key, app_secret = get_credentials()

    api = KiwoomAPI(app_key=app_key, app_secret=app_secret, is_mock=True)

    print("Logging in...")
    api.login()
    print("Login successful.\n")

    # 1. Stock quote (호가) for Samsung Electronics
    print("Fetching stock quote for 005930 (Samsung Electronics)...")
    quote = api.market.stock_quote(stk_cd="005930")
    print(f"Stock quote response: {quote}\n")

    # 2. Daily chart data for Samsung Electronics
    print("Fetching daily chart for 005930...")
    daily_chart = api.chart.stock_daily_chart(
        stk_cd="005930",
        base_dt="20240101",
        upd_stkpc_tp="1",  # 수정주가구분 — 0: 미반영, 1: 반영
    )
    print(f"Daily chart response: {daily_chart}\n")

    # 3. Top volume ranking (거래량 상위)
    print("Fetching top volume ranking...")
    top_volume = api.ranking.top_volume_today(
        mrkt_tp="000",       # 000: 전체, 001: 코스피, 101: 코스닥
        sort_tp="1",         # 1: 거래량, 2: 거래회전율, 3: 거래대금
        mang_stk_incls="0",  # 0: 관리종목 포함
        crd_tp="0",          # 0: 전체조회
        trde_qty_tp="5",     # 5: 5천주 이상
        pric_tp="0",         # 0: 전체조회
        trde_prica_tp="0",   # 0: 전체조회
        mrkt_open_tp="0",    # 0: 전체조회
        stex_tp="3",         # 1: KRX, 2: NXT, 3: 통합
    )
    print(f"Top volume ranking response: {top_volume}\n")

    # 4. All sector index (전업종지수)
    print("Fetching all sector index...")
    sector_index = api.sector.all_industry_index(inds_cd="001")  # 001: 종합(KOSPI)
    print(f"Sector index response: {sector_index}\n")

    api.logout()
    api.close()
    print("Done.")


if __name__ == "__main__":
    main()
