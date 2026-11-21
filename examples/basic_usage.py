"""Basic usage example: login, query stock info, account evaluation, logout."""

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

    # Initialize with mock trading server
    api = KiwoomAPI(app_key=app_key, app_secret=app_secret, is_mock=True)

    # 1. Login - obtain access token
    print("Logging in...")
    token_info = api.login()
    print(f"Login successful. Token type: {token_info.get('token_type')}")

    # 2. Query basic stock info for Samsung Electronics (005930)
    print("\nFetching basic stock info for 005930 (Samsung Electronics)...")
    stock_info = api.stock_info.basic_stock_info(stk_cd="005930")
    print(f"Stock info response: {stock_info}")

    # 3. Query account evaluation status
    # The account is the one the app key was issued for — there is no account-number field.
    print("\nFetching account evaluation...")
    eval_status = api.account.account_evaluation(qry_tp="0", dmst_stex_tp="KRX")
    print(f"Account evaluation response: {eval_status}")

    # 4. Logout - revoke access token
    print("\nLogging out...")
    api.logout()
    print("Logout successful.")

    api.close()


if __name__ == "__main__":
    main()
