"""pandas DataFrame 활용 예제: API 응답을 DataFrame으로 변환하여 분석하기."""

import os
import sys

import pandas as pd

from kiwoom_rest_api import KiwoomAPI


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
    api.login()

    # 1. 당일 거래량 상위 종목 조회 → DataFrame 변환
    print("거래량 상위 종목을 DataFrame으로 변환합니다...")
    result = api.ranking.top_volume_today(
        mrkt_tp="0",      # 코스피
        stk_cnd="0",      # 전체
        trde_qty_tp="0",  # 전체
        prc_tp="0",       # 전체
        trde_amt_tp="0",  # 전체
        updn_tp="0",      # 전체
    )

    # API 응답의 리스트 데이터를 DataFrame으로 변환
    # 응답 구조에 따라 적절한 키를 사용하세요 (예: "output", "stk_list" 등)
    if "output" in result:
        df = pd.DataFrame(result["output"])
    else:
        # 응답 키가 다를 수 있으므로 리스트 타입인 첫 번째 값을 사용
        for key, value in result.items():
            if isinstance(value, list) and value:
                df = pd.DataFrame(value)
                break
        else:
            print("리스트 데이터를 찾을 수 없습니다.")
            api.logout()
            api.close()
            return

    print(f"\n거래량 상위 종목 ({len(df)}개):")
    print(df.head(10))

    # 2. 일봉 차트 데이터 → DataFrame 변환
    print("\n\n삼성전자 일봉 차트를 DataFrame으로 변환합니다...")
    chart = api.chart.stock_daily_chart(stk_cd="005930", base_dt="20260326")

    for key, value in chart.items():
        if isinstance(value, list) and value:
            chart_df = pd.DataFrame(value)
            print(f"\n일봉 데이터 ({len(chart_df)}행):")
            print(chart_df.head())
            break

    api.logout()
    api.close()


if __name__ == "__main__":
    main()
