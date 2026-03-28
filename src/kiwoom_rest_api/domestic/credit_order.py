"""Credit Order (신용주문) endpoints for the Kiwoom REST API."""

from __future__ import annotations

from typing import Any

from kiwoom_rest_api.base import BaseClient


class CreditOrder:
    """Wraps all Credit Order (신용주문) endpoints under /api/dostk/crdordr.

    Args:
        client: Authenticated BaseClient instance.
    """

    RESOURCE_URL = "/api/dostk/crdordr"

    def __init__(self, client: BaseClient) -> None:
        self._client = client

    def margin_buy_order(
        self, cont_yn: str = "N", next_key: str = "", **kwargs: Any
    ) -> dict[str, Any]:
        """신용매수주문 (Credit Margin Buy Order)"""
        return self._client.request(self.RESOURCE_URL, "kt10006", kwargs, cont_yn, next_key)

    def margin_sell_order(
        self, cont_yn: str = "N", next_key: str = "", **kwargs: Any
    ) -> dict[str, Any]:
        """신용매도주문 (Credit Margin Sell Order)"""
        return self._client.request(self.RESOURCE_URL, "kt10007", kwargs, cont_yn, next_key)

    def margin_modify_order(
        self, cont_yn: str = "N", next_key: str = "", **kwargs: Any
    ) -> dict[str, Any]:
        """신용정정주문 (Credit Margin Modify Order)"""
        return self._client.request(self.RESOURCE_URL, "kt10008", kwargs, cont_yn, next_key)

    def margin_cancel_order(
        self, cont_yn: str = "N", next_key: str = "", **kwargs: Any
    ) -> dict[str, Any]:
        """신용취소주문 (Credit Margin Cancel Order)"""
        return self._client.request(self.RESOURCE_URL, "kt10009", kwargs, cont_yn, next_key)
