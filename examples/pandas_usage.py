"""pandas DataFrame 활용 예제: API 응답을 DataFrame으로 변환하여 분석하기.

`pip install 'kiwoom-client[pandas]'` 로 pandas 를 함께 설치하세요.
"""

import os
import sys

from kiwoom_rest_api import KiwoomAPI, to_dataframe


def get_credentials() -> tuple[str, str]:
    app_key = os.environ.get("KIWOOM_APP_KEY")
    app_secret = os.environ.get("KIWOOM_APP_SECRET")
    if not app_key or not app_secret:
        print("Error: KIWOOM_APP_KEY and KIWOOM_APP_SECRET environment variables must be set.")
        sys.exit(1)
    return app_key, app_secret


def main() -> None:
    app_key, app_secret = get_credentials()

    # login() 은 선택. 토큰은 첫 요청에서 발급되고 만료 전 자동 갱신된다.
    api = KiwoomAPI(app_key=app_key, app_secret=app_secret, is_mock=True)

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

    # 응답 키는 엔드포인트마다 다르다. to_dataframe() 이 알아서 찾아주고,
    # "+70000" 같은 부호 문자열을 숫자로 바꿔준다 (종목코드·날짜는 문자열 유지).
    df = to_dataframe(result)

    print(f"\n거래량 상위 종목 ({len(df)}개):")
    print(df.head(10))

    # 숫자로 들어왔으니 바로 계산할 수 있다.
    if "cur_prc" in df.columns:
        print(f"\n현재가 평균: {df['cur_prc'].mean():,.0f}원")

    # 2. 일봉 차트 데이터 → DataFrame 변환
    print("\n\n삼성전자 일봉 차트를 DataFrame으로 변환합니다...")
    chart = api.chart.stock_daily_chart(stk_cd="005930", base_dt="20260326")
    chart_df = to_dataframe(chart)

    print(f"\n일봉 데이터 ({len(chart_df)}행):")
    print(chart_df.head())

    # 3. 원본 문자열이 필요하면 numeric=False, 특정 키를 직접 지정하려면 key=
    #    raw_df = to_dataframe(chart, key="stk_dt_pole_chart_qry", numeric=False)

    api.logout()
    api.close()


if __name__ == "__main__":
    main()
