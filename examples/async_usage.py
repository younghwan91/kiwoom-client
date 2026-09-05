"""asyncio 활용 예제: 여러 TR 을 동시에 조회하기.

Rate Limiter 는 TR(api_id) 별로 걸리므로, 서로 다른 TR 은 서로를 막지 않고
동시에 나간다. 같은 TR 을 반복 호출할 때만 초당 1건으로 조여진다.
"""

import asyncio
import os
import sys

from kiwoom_client import AsyncKiwoomAPI, to_number


def get_credentials() -> tuple[str, str]:
    app_key = os.environ.get("KIWOOM_APP_KEY")
    app_secret = os.environ.get("KIWOOM_APP_SECRET")
    if not app_key or not app_secret:
        print("Error: KIWOOM_APP_KEY and KIWOOM_APP_SECRET environment variables must be set.")
        sys.exit(1)
    return app_key, app_secret


async def main() -> None:
    app_key, app_secret = get_credentials()

    # login() 은 선택. 토큰은 첫 요청에서 발급되고 만료 전 자동 갱신된다.
    async with AsyncKiwoomAPI(app_key=app_key, app_secret=app_secret, is_mock=True) as api:
        # 1. 서로 다른 TR 3개를 동시에 — 직렬로 돌리면 3배 걸린다.
        info, chart, ranking = await asyncio.gather(
            api.stock_info.basic_stock_info(stk_cd="005930"),
            api.chart.stock_daily_chart(stk_cd="005930", base_dt="20260326"),
            api.ranking.top_volume_today(
                mrkt_tp="0", stk_cnd="0", trde_qty_tp="0",
                prc_tp="0", trde_amt_tp="0", updn_tp="0",
            ),
        )

        print(f"종목명: {info.get('stk_nm')}")
        print(f"현재가: {to_number(info.get('cur_prc')):,}원")
        meta = ("return_code", "return_msg")
        print(f"차트 응답 키: {[k for k in chart if k not in meta]}")
        print(f"거래량 상위 응답 키: {[k for k in ranking if k not in meta]}")

        # 2. 여러 종목을 동시에 조회 — 같은 TR 이라 Rate Limiter 가 순서대로 흘려보낸다.
        codes = ["005930", "000660", "035420"]
        results = await asyncio.gather(
            *(api.stock_info.basic_stock_info(stk_cd=code) for code in codes)
        )
        for code, result in zip(codes, results, strict=True):
            print(f"{code} {result.get('stk_nm')}: {result.get('cur_prc')}")

        await api.logout()


if __name__ == "__main__":
    asyncio.run(main())
