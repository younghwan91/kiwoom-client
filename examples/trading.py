"""Trading example: buy, sell, modify, and cancel orders.

WARNING: This example uses is_mock=True (mock trading server).
Do NOT run against production without reviewing the parameters carefully.
"""

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

    # Field names and values follow Kiwoom's official REST spec
    # (Kiwoom-Securities/Kiwoom-REST-API kiwoom/_data/kiwoom_api_spec.json).
    # No account number in the body -- the token is bound to the account.

    # 1. Buy order - Samsung Electronics at limit price
    print("Placing buy order for 005930 (Samsung Electronics)...")
    buy_result = api.order.buy_order(
        dmst_stex_tp="KRX",  # 거래소: KRX / NXT / SOR
        stk_cd="005930",
        ord_qty="10",        # 주문수량
        ord_uv="70000",      # 주문단가
        trde_tp="0",         # 매매구분: 0=보통(지정가)
    )
    print(f"Buy order response: {buy_result}")
    ord_no = buy_result.get("ord_no", "")
    print(f"Order number: {ord_no}\n")

    # 2. Sell order - limit price
    print("Placing sell order for 005930...")
    sell_result = api.order.sell_order(
        dmst_stex_tp="KRX",
        stk_cd="005930",
        ord_qty="5",
        ord_uv="72000",
        trde_tp="0",
    )
    print(f"Sell order response: {sell_result}")
    sell_ord_no = sell_result.get("ord_no", "")
    print(f"Sell order number: {sell_ord_no}\n")

    # 3. Modify order (kt10002) - change price of the buy order
    if ord_no:
        print(f"Modifying buy order {ord_no}...")
        modify_result = api.order.modify_order(
            dmst_stex_tp="KRX",
            orig_ord_no=ord_no,  # 원주문번호
            stk_cd="005930",
            mdfy_qty="10",       # 정정수량 ("0" = 잔량 전부)
            mdfy_uv="69000",     # 정정단가
        )
        print(f"Modify order response: {modify_result}\n")

    # 4. Cancel order (kt10003) - cancel the sell order
    if sell_ord_no:
        print(f"Cancelling sell order {sell_ord_no}...")
        cancel_result = api.order.cancel_order(
            dmst_stex_tp="KRX",
            orig_ord_no=sell_ord_no,  # 원주문번호
            stk_cd="005930",
            cncl_qty="5",             # 취소수량 ("0" = 잔량 전부)
        )
        print(f"Cancel order response: {cancel_result}\n")

    api.logout()
    api.close()
    print("Done.")


if __name__ == "__main__":
    main()
