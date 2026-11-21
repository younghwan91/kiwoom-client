"""Quickstart on the mock server: credentials from the environment, three calls.

    export KIWOOM_APP_KEY="모의투자_앱키"
    export KIWOOM_APP_SECRET="모의투자_시크릿키"
    uv run python examples/quickstart.py

A ``.env`` file in the current directory is read too (environment variables
win). ``is_mock=True`` is passed explicitly, so this script never talks to the
live server whatever ``KIWOOM_IS_MOCK`` says — and it places no orders.
"""

from __future__ import annotations

from datetime import date
from pathlib import Path

from kiwoom_client import KiwoomAPI, KiwoomError, add_ticks, round_to_tick


def main() -> None:
    env_file = ".env" if Path(".env").exists() else None
    with KiwoomAPI.from_env(env_file, is_mock=True) as api:
        print(api)  # server='mock', key masked

        # 1. Name -> code (ka10099, cached on the client)
        code = api.stock_code("삼성전자")
        print("삼성전자 =", code)

        # 2. Current price (ka10001)
        info = api.stock_info.basic_stock_info(stk_cd=code)
        print(info["stk_nm"], info["cur_prc"], f"{info['flu_rt']}%")

        # 3. Daily chart (ka10081) -> OHLCV DataFrame when pandas is installed
        chart = api.chart.stock_daily_chart(
            stk_cd=code, base_dt=date.today().strftime("%Y%m%d"), upd_stkpc_tp="1"
        )
        try:
            from kiwoom_client import to_ohlcv

            print(to_ohlcv(chart).tail())
        except ImportError:
            print("pandas 가 없어 원 응답 키만 출력:", sorted(chart))

        # Tick math for a limit price two ticks under the current price
        price = round_to_tick(abs(int(info["cur_prc"])))
        print("2틱 아래 지정가:", add_ticks(price, -2))


if __name__ == "__main__":
    try:
        main()
    except (KiwoomError, LookupError, ValueError) as exc:
        raise SystemExit(f"error: {exc}") from exc
