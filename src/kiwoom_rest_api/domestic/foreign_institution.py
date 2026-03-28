"""Foreign Institution (외국인/기관) endpoints for the Kiwoom REST API."""

from __future__ import annotations

from typing import Any

from kiwoom_rest_api.base import BaseClient


class ForeignInstitution:
    """Wraps all Foreign Institution (외국인/기관) endpoints under /api/dostk/frgnistt.

    Args:
        client: Authenticated BaseClient instance.
    """

    RESOURCE_URL = "/api/dostk/frgnistt"

    def __init__(self, client: BaseClient) -> None:
        self._client = client

    def foreign_trading_trend(
        self, cont_yn: str = "N", next_key: str = "", **kwargs: Any
    ) -> dict[str, Any]:
        """주식외국인종목별매매동향 (Foreign Trading Trend by Stock)"""
        return self._client.request(self.RESOURCE_URL, "ka10008", kwargs, cont_yn, next_key)

    def institutional_stock(
        self, cont_yn: str = "N", next_key: str = "", **kwargs: Any
    ) -> dict[str, Any]:
        """주식기관요청 (Institutional Stock)"""
        return self._client.request(self.RESOURCE_URL, "ka10009", kwargs, cont_yn, next_key)

    def consecutive_trading_status(
        self, cont_yn: str = "N", next_key: str = "", **kwargs: Any
    ) -> dict[str, Any]:
        """기관외국인연속매매현황요청 (Institution and Foreign Consecutive Trading Status)"""
        return self._client.request(self.RESOURCE_URL, "ka10131", kwargs, cont_yn, next_key)

    def gold_spot_investor_status(
        self, cont_yn: str = "N", next_key: str = "", **kwargs: Any
    ) -> dict[str, Any]:
        """금현물투자자현황 (Gold Spot Investor Status)"""
        return self._client.request(self.RESOURCE_URL, "ka52301", kwargs, cont_yn, next_key)
