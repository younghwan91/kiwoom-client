"""Order (주문) endpoints for the Kiwoom REST API."""

from __future__ import annotations

from typing import Any

from kiwoom_rest_api.base import BaseClient


class Order:
    """Wraps all Order (주문) endpoints under /api/dostk/ordr.

    Args:
        client: Authenticated BaseClient instance.
    """

    RESOURCE_URL = "/api/dostk/ordr"

    def __init__(self, client: BaseClient) -> None:
        self._client = client

    def buy_order(
        self, cont_yn: str = "N", next_key: str = "", **kwargs: Any
    ) -> dict[str, Any]:
        """주식매수주문 (Stock Buy Order)"""
        return self._client.request(self.RESOURCE_URL, "kt10000", kwargs, cont_yn, next_key)

    def sell_order(
        self, cont_yn: str = "N", next_key: str = "", **kwargs: Any
    ) -> dict[str, Any]:
        """주식매도주문 (Stock Sell Order)"""
        return self._client.request(self.RESOURCE_URL, "kt10001", kwargs, cont_yn, next_key)

    def modify_order(
        self, cont_yn: str = "N", next_key: str = "", **kwargs: Any
    ) -> dict[str, Any]:
        """주식정정주문 (Stock Modify Order)"""
        return self._client.request(self.RESOURCE_URL, "kt10002", kwargs, cont_yn, next_key)

    def cancel_order(
        self, cont_yn: str = "N", next_key: str = "", **kwargs: Any
    ) -> dict[str, Any]:
        """주식취소주문 (Stock Cancel Order)"""
        return self._client.request(self.RESOURCE_URL, "kt10003", kwargs, cont_yn, next_key)

    def gold_spot_buy_order(
        self, cont_yn: str = "N", next_key: str = "", **kwargs: Any
    ) -> dict[str, Any]:
        """금현물 매수주문 (Gold Spot Buy Order)"""
        return self._client.request(self.RESOURCE_URL, "kt50000", kwargs, cont_yn, next_key)

    def gold_spot_sell_order(
        self, cont_yn: str = "N", next_key: str = "", **kwargs: Any
    ) -> dict[str, Any]:
        """금현물 매도주문 (Gold Spot Sell Order)"""
        return self._client.request(self.RESOURCE_URL, "kt50001", kwargs, cont_yn, next_key)

    def gold_spot_modify_order(
        self, cont_yn: str = "N", next_key: str = "", **kwargs: Any
    ) -> dict[str, Any]:
        """금현물 정정주문 (Gold Spot Modify Order)"""
        return self._client.request(self.RESOURCE_URL, "kt50002", kwargs, cont_yn, next_key)

    def gold_spot_cancel_order(
        self, cont_yn: str = "N", next_key: str = "", **kwargs: Any
    ) -> dict[str, Any]:
        """금현물 취소주문 (Gold Spot Cancel Order)"""
        return self._client.request(self.RESOURCE_URL, "kt50003", kwargs, cont_yn, next_key)
