"""Trading example: buy, sell, modify, and cancel orders.

WARNING: This example uses is_mock=True (mock trading server).
Do NOT run against production without reviewing the parameters carefully.
"""

import os
import sys

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
    account_no = os.environ.get("KIWOOM_ACCOUNT_NO", "1234567890")

    api = KiwoomAPI(app_key=app_key, app_secret=app_secret, is_mock=True)

    print("Logging in...")
    api.login()
    print("Login successful.\n")

    # 1. Buy order - Samsung Electronics at limit price
    print("Placing buy order for 005930 (Samsung Electronics)...")
    buy_result = api.order.buy_order(
        acnt_no=account_no,
        acnt_prdt_cd="01",   # 계좌상품코드
        stk_cd="005930",
        ord_qty="10",        # 주문수량
        ord_uv="70000",      # 주문단가
        ord_dv="00",         # 주문구분: 00=지정가
    )
    print(f"Buy order response: {buy_result}")
    ord_no = buy_result.get("ord_no", "")
    print(f"Order number: {ord_no}\n")

    # 2. Sell order - limit price
    print("Placing sell order for 005930...")
    sell_result = api.order.sell_order(
        acnt_no=account_no,
        acnt_prdt_cd="01",
        stk_cd="005930",
        ord_qty="5",
        ord_uv="72000",
        ord_dv="00",
    )
    print(f"Sell order response: {sell_result}")
    sell_ord_no = sell_result.get("ord_no", "")
    print(f"Sell order number: {sell_ord_no}\n")

    # 3. Modify order - change price of the buy order
    if ord_no:
        print(f"Modifying buy order {ord_no}...")
        modify_result = api.order.modify_order(
            acnt_no=account_no,
            acnt_prdt_cd="01",
            orig_ord_no=ord_no,  # 원주문번호
            stk_cd="005930",
            ord_qty="10",
            ord_uv="69000",      # new price
            ord_dv="00",
        )
        print(f"Modify order response: {modify_result}\n")

    # 4. Cancel order - cancel the sell order
    if sell_ord_no:
        print(f"Cancelling sell order {sell_ord_no}...")
        cancel_result = api.order.cancel_order(
            acnt_no=account_no,
            acnt_prdt_cd="01",
            orig_ord_no=sell_ord_no,  # 원주문번호
            stk_cd="005930",
            ord_qty="5",
        )
        print(f"Cancel order response: {cancel_result}\n")

    api.logout()
    api.close()
    print("Done.")


if __name__ == "__main__":
    main()
