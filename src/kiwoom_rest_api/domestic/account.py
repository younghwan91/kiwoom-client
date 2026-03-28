"""Account (계좌) endpoints for the Kiwoom REST API."""

from __future__ import annotations

from typing import Any

from kiwoom_rest_api.base import BaseClient


class Account:
    """Wraps all Account (계좌) endpoints under /api/dostk/acnt.

    Args:
        client: Authenticated BaseClient instance.
    """

    RESOURCE_URL = "/api/dostk/acnt"

    def __init__(self, client: BaseClient) -> None:
        self._client = client

    def realized_profit_by_date(
        self, cont_yn: str = "N", next_key: str = "", **kwargs: Any
    ) -> dict[str, Any]:
        """일자별종목별실현손익요청_일자 (Realized Profit by Date per Stock)"""
        return self._client.request(self.RESOURCE_URL, "ka10072", kwargs, cont_yn, next_key)

    def realized_profit_by_period(
        self, cont_yn: str = "N", next_key: str = "", **kwargs: Any
    ) -> dict[str, Any]:
        """일자별종목별실현손익요청_기간 (Realized Profit by Period per Stock)"""
        return self._client.request(self.RESOURCE_URL, "ka10073", kwargs, cont_yn, next_key)

    def daily_realized_profit(
        self, cont_yn: str = "N", next_key: str = "", **kwargs: Any
    ) -> dict[str, Any]:
        """일별실현손익요청 (Daily Realized Profit)"""
        return self._client.request(self.RESOURCE_URL, "ka10074", kwargs, cont_yn, next_key)

    def unfilled_orders(
        self, cont_yn: str = "N", next_key: str = "", **kwargs: Any
    ) -> dict[str, Any]:
        """미체결요청 (Unfilled Orders)"""
        return self._client.request(self.RESOURCE_URL, "ka10075", kwargs, cont_yn, next_key)

    def filled_orders(
        self, cont_yn: str = "N", next_key: str = "", **kwargs: Any
    ) -> dict[str, Any]:
        """체결요청 (Filled Orders History)"""
        return self._client.request(self.RESOURCE_URL, "ka10076", kwargs, cont_yn, next_key)

    def today_realized_profit_detail(
        self, cont_yn: str = "N", next_key: str = "", **kwargs: Any
    ) -> dict[str, Any]:
        """당일실현손익상세요청 (Today Realized Profit Detail)"""
        return self._client.request(self.RESOURCE_URL, "ka10077", kwargs, cont_yn, next_key)

    def account_return_rate(
        self, cont_yn: str = "N", next_key: str = "", **kwargs: Any
    ) -> dict[str, Any]:
        """계좌수익률요청 (Account Return Rate)"""
        return self._client.request(self.RESOURCE_URL, "ka10085", kwargs, cont_yn, next_key)

    def unfilled_split_order_detail(
        self, cont_yn: str = "N", next_key: str = "", **kwargs: Any
    ) -> dict[str, Any]:
        """미체결 분할주문 상세 (Unfilled Split Order Detail)"""
        return self._client.request(self.RESOURCE_URL, "ka10088", kwargs, cont_yn, next_key)

    def today_trading_journal(
        self, cont_yn: str = "N", next_key: str = "", **kwargs: Any
    ) -> dict[str, Any]:
        """당일매매일지요청 (Today Trading Journal)"""
        return self._client.request(self.RESOURCE_URL, "ka10170", kwargs, cont_yn, next_key)

    def deposit_detail(
        self, cont_yn: str = "N", next_key: str = "", **kwargs: Any
    ) -> dict[str, Any]:
        """예수금상세현황요청 (Deposit Detail Status)"""
        return self._client.request(self.RESOURCE_URL, "kt00001", kwargs, cont_yn, next_key)

    def daily_estimated_deposit(
        self, cont_yn: str = "N", next_key: str = "", **kwargs: Any
    ) -> dict[str, Any]:
        """일별추정예탁자산현황요청 (Daily Estimated Deposit Asset Status)"""
        return self._client.request(self.RESOURCE_URL, "kt00002", kwargs, cont_yn, next_key)

    def estimated_asset(
        self, cont_yn: str = "N", next_key: str = "", **kwargs: Any
    ) -> dict[str, Any]:
        """추정자산조회요청 (Estimated Asset Inquiry)"""
        return self._client.request(self.RESOURCE_URL, "kt00003", kwargs, cont_yn, next_key)

    def account_evaluation(
        self, cont_yn: str = "N", next_key: str = "", **kwargs: Any
    ) -> dict[str, Any]:
        """계좌평가현황요청 (Account Evaluation Status)"""
        return self._client.request(self.RESOURCE_URL, "kt00004", kwargs, cont_yn, next_key)

    def filled_position(
        self, cont_yn: str = "N", next_key: str = "", **kwargs: Any
    ) -> dict[str, Any]:
        """체결잔고요청 (Filled Position Balance)"""
        return self._client.request(self.RESOURCE_URL, "kt00005", kwargs, cont_yn, next_key)

    def order_execution_detail(
        self, cont_yn: str = "N", next_key: str = "", **kwargs: Any
    ) -> dict[str, Any]:
        """계좌별주문체결내역상세요청 (Account Order Execution Detail)"""
        return self._client.request(self.RESOURCE_URL, "kt00007", kwargs, cont_yn, next_key)

    def next_day_settlement(
        self, cont_yn: str = "N", next_key: str = "", **kwargs: Any
    ) -> dict[str, Any]:
        """계좌별익일결제예정내역요청 (Next Day Settlement Schedule)"""
        return self._client.request(self.RESOURCE_URL, "kt00008", kwargs, cont_yn, next_key)

    def order_execution_status(
        self, cont_yn: str = "N", next_key: str = "", **kwargs: Any
    ) -> dict[str, Any]:
        """계좌별주문체결현황요청 (Account Order Execution Status)"""
        return self._client.request(self.RESOURCE_URL, "kt00009", kwargs, cont_yn, next_key)

    def withdrawable_amount(
        self, cont_yn: str = "N", next_key: str = "", **kwargs: Any
    ) -> dict[str, Any]:
        """주문인출가능금액요청 (Withdrawable Order Amount)"""
        return self._client.request(self.RESOURCE_URL, "kt00010", kwargs, cont_yn, next_key)

    def orderable_qty_by_margin(
        self, cont_yn: str = "N", next_key: str = "", **kwargs: Any
    ) -> dict[str, Any]:
        """증거금율별주문가능수량조회요청 (Orderable Quantity by Margin Rate)"""
        return self._client.request(self.RESOURCE_URL, "kt00011", kwargs, cont_yn, next_key)

    def orderable_qty_by_credit(
        self, cont_yn: str = "N", next_key: str = "", **kwargs: Any
    ) -> dict[str, Any]:
        """신용보증금율별주문가능수량조회요청 (Orderable Quantity by Credit Margin Rate)"""
        return self._client.request(self.RESOURCE_URL, "kt00012", kwargs, cont_yn, next_key)

    def margin_detail(
        self, cont_yn: str = "N", next_key: str = "", **kwargs: Any
    ) -> dict[str, Any]:
        """증거금세부내역조회요청 (Margin Detail Inquiry)"""
        return self._client.request(self.RESOURCE_URL, "kt00013", kwargs, cont_yn, next_key)

    def comprehensive_transaction_history(
        self, cont_yn: str = "N", next_key: str = "", **kwargs: Any
    ) -> dict[str, Any]:
        """위탁종합거래내역요청 (Comprehensive Transaction History)"""
        return self._client.request(self.RESOURCE_URL, "kt00015", kwargs, cont_yn, next_key)

    def daily_return_detail(
        self, cont_yn: str = "N", next_key: str = "", **kwargs: Any
    ) -> dict[str, Any]:
        """일별계좌수익률상세현황요청 (Daily Account Return Rate Detail)"""
        return self._client.request(self.RESOURCE_URL, "kt00016", kwargs, cont_yn, next_key)

    def today_account_status(
        self, cont_yn: str = "N", next_key: str = "", **kwargs: Any
    ) -> dict[str, Any]:
        """계좌별당일현황요청 (Today Account Status by Account)"""
        return self._client.request(self.RESOURCE_URL, "kt00017", kwargs, cont_yn, next_key)

    def evaluation_balance_detail(
        self, cont_yn: str = "N", next_key: str = "", **kwargs: Any
    ) -> dict[str, Any]:
        """계좌평가잔고내역요청 (Account Evaluation Balance Detail)"""
        return self._client.request(self.RESOURCE_URL, "kt00018", kwargs, cont_yn, next_key)

    def account_number_inquiry(
        self, cont_yn: str = "N", next_key: str = "", **kwargs: Any
    ) -> dict[str, Any]:
        """계좌번호조회 (Account Number Inquiry)"""
        return self._client.request(self.RESOURCE_URL, "ka00001", kwargs, cont_yn, next_key)

    def daily_balance_return_rate(
        self, cont_yn: str = "N", next_key: str = "", **kwargs: Any
    ) -> dict[str, Any]:
        """일별잔고수익률 (Daily Balance Return Rate)"""
        return self._client.request(self.RESOURCE_URL, "ka01690", kwargs, cont_yn, next_key)

    def gold_spot_balance(
        self, cont_yn: str = "N", next_key: str = "", **kwargs: Any
    ) -> dict[str, Any]:
        """금현물 잔고확인 (Gold Spot Balance)"""
        return self._client.request(self.RESOURCE_URL, "kt50020", kwargs, cont_yn, next_key)

    def gold_spot_deposit(
        self, cont_yn: str = "N", next_key: str = "", **kwargs: Any
    ) -> dict[str, Any]:
        """금현물 예수금 (Gold Spot Deposit)"""
        return self._client.request(self.RESOURCE_URL, "kt50021", kwargs, cont_yn, next_key)

    def gold_spot_order_execution_all(
        self, cont_yn: str = "N", next_key: str = "", **kwargs: Any
    ) -> dict[str, Any]:
        """금현물 주문체결전체조회 (Gold Spot All Order Execution)"""
        return self._client.request(self.RESOURCE_URL, "kt50030", kwargs, cont_yn, next_key)

    def gold_spot_order_execution(
        self, cont_yn: str = "N", next_key: str = "", **kwargs: Any
    ) -> dict[str, Any]:
        """금현물 주문체결조회 (Gold Spot Order Execution)"""
        return self._client.request(self.RESOURCE_URL, "kt50031", kwargs, cont_yn, next_key)

    def gold_spot_transaction_history(
        self, cont_yn: str = "N", next_key: str = "", **kwargs: Any
    ) -> dict[str, Any]:
        """금현물 거래내역조회 (Gold Spot Transaction History)"""
        return self._client.request(self.RESOURCE_URL, "kt50032", kwargs, cont_yn, next_key)

    def gold_spot_unfilled_orders(
        self, cont_yn: str = "N", next_key: str = "", **kwargs: Any
    ) -> dict[str, Any]:
        """금현물 미체결조회 (Gold Spot Unfilled Orders)"""
        return self._client.request(self.RESOURCE_URL, "kt50075", kwargs, cont_yn, next_key)
