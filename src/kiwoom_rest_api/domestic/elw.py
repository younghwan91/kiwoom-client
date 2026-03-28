"""ELW endpoints for the Kiwoom REST API."""

from __future__ import annotations

from typing import Any

from kiwoom_rest_api.base import BaseClient


class ELW:
    """Wraps all ELW endpoints under /api/dostk/elw.

    Args:
        client: Authenticated BaseClient instance.
    """

    RESOURCE_URL = "/api/dostk/elw"

    def __init__(self, client: BaseClient) -> None:
        self._client = client

    def daily_sensitivity_indicator(
        self, cont_yn: str = "N", next_key: str = "", **kwargs: Any
    ) -> dict[str, Any]:
        """ELW일별민감도지표요청 (ELW Daily Sensitivity Indicator)"""
        return self._client.request(self.RESOURCE_URL, "ka10048", kwargs, cont_yn, next_key)

    def sensitivity_indicator(
        self, cont_yn: str = "N", next_key: str = "", **kwargs: Any
    ) -> dict[str, Any]:
        """ELW민감도지표요청 (ELW Sensitivity Indicator)"""
        return self._client.request(self.RESOURCE_URL, "ka10050", kwargs, cont_yn, next_key)

    def price_spike(
        self, cont_yn: str = "N", next_key: str = "", **kwargs: Any
    ) -> dict[str, Any]:
        """ELW급등락요청 (ELW Price Spike)"""
        return self._client.request(self.RESOURCE_URL, "ka30001", kwargs, cont_yn, next_key)

    def top_net_buying_by_broker(
        self, cont_yn: str = "N", next_key: str = "", **kwargs: Any
    ) -> dict[str, Any]:
        """ELW회원사별순매수상위요청 (ELW Top Net Buying by Broker)"""
        return self._client.request(self.RESOURCE_URL, "ka30002", kwargs, cont_yn, next_key)

    def lp_daily_holding_trend(
        self, cont_yn: str = "N", next_key: str = "", **kwargs: Any
    ) -> dict[str, Any]:
        """ELW LP일별보유추이요청 (ELW LP Daily Holding Trend)"""
        return self._client.request(self.RESOURCE_URL, "ka30003", kwargs, cont_yn, next_key)

    def premium_rate(
        self, cont_yn: str = "N", next_key: str = "", **kwargs: Any
    ) -> dict[str, Any]:
        """ELW괴리율요청 (ELW Premium Rate)"""
        return self._client.request(self.RESOURCE_URL, "ka30004", kwargs, cont_yn, next_key)

    def condition_search(
        self, cont_yn: str = "N", next_key: str = "", **kwargs: Any
    ) -> dict[str, Any]:
        """ELW조건검색요청 (ELW Condition Search)"""
        return self._client.request(self.RESOURCE_URL, "ka30005", kwargs, cont_yn, next_key)

    def change_rate_ranking(
        self, cont_yn: str = "N", next_key: str = "", **kwargs: Any
    ) -> dict[str, Any]:
        """ELW등락율순위요청 (ELW Change Rate Ranking)"""
        return self._client.request(self.RESOURCE_URL, "ka30009", kwargs, cont_yn, next_key)

    def order_volume_ranking(
        self, cont_yn: str = "N", next_key: str = "", **kwargs: Any
    ) -> dict[str, Any]:
        """ELW호가잔량순위요청 (ELW Order Volume Ranking)"""
        return self._client.request(self.RESOURCE_URL, "ka30010", kwargs, cont_yn, next_key)

    def proximity_rate(
        self, cont_yn: str = "N", next_key: str = "", **kwargs: Any
    ) -> dict[str, Any]:
        """ELW근접율요청 (ELW Proximity Rate)"""
        return self._client.request(self.RESOURCE_URL, "ka30011", kwargs, cont_yn, next_key)

    def detailed_stock_info(
        self, cont_yn: str = "N", next_key: str = "", **kwargs: Any
    ) -> dict[str, Any]:
        """ELW종목상세정보요청 (ELW Detailed Stock Info)"""
        return self._client.request(self.RESOURCE_URL, "ka30012", kwargs, cont_yn, next_key)
