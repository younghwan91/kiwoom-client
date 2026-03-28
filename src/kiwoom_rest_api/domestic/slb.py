"""SLB (대차거래) endpoints for the Kiwoom REST API."""

from __future__ import annotations

from typing import Any

from kiwoom_rest_api.base import BaseClient


class SLB:
    """Wraps all SLB (대차거래) endpoints under /api/dostk/slb.

    Args:
        client: Authenticated BaseClient instance.
    """

    RESOURCE_URL = "/api/dostk/slb"

    def __init__(self, client: BaseClient) -> None:
        self._client = client

    def lending_trend(
        self, cont_yn: str = "N", next_key: str = "", **kwargs: Any
    ) -> dict[str, Any]:
        """대차거래추이요청 (Lending Trend)"""
        return self._client.request(self.RESOURCE_URL, "ka10068", kwargs, cont_yn, next_key)

    def top10_lending(
        self, cont_yn: str = "N", next_key: str = "", **kwargs: Any
    ) -> dict[str, Any]:
        """대차거래상위10종목요청 (Top 10 Lending Stocks)"""
        return self._client.request(self.RESOURCE_URL, "ka10069", kwargs, cont_yn, next_key)

    def lending_trend_by_stock(
        self, cont_yn: str = "N", next_key: str = "", **kwargs: Any
    ) -> dict[str, Any]:
        """대차거래추이요청종목별 (Lending Trend by Stock)"""
        return self._client.request(self.RESOURCE_URL, "ka20068", kwargs, cont_yn, next_key)

    def lending_details(
        self, cont_yn: str = "N", next_key: str = "", **kwargs: Any
    ) -> dict[str, Any]:
        """대차거래내역요청 (Lending Details)"""
        return self._client.request(self.RESOURCE_URL, "ka90012", kwargs, cont_yn, next_key)
