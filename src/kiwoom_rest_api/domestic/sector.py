"""Sector (업종) endpoints for the Kiwoom REST API."""

from __future__ import annotations

from typing import Any

from kiwoom_rest_api.base import BaseClient


class Sector:
    """Wraps all Sector (업종) endpoints under /api/dostk/sect.

    Args:
        client: Authenticated BaseClient instance.
    """

    RESOURCE_URL = "/api/dostk/sect"

    def __init__(self, client: BaseClient) -> None:
        self._client = client

    def industry_program_trading(
        self, cont_yn: str = "N", next_key: str = "", **kwargs: Any
    ) -> dict[str, Any]:
        """업종프로그램매매요청 (Industry Program Trading)"""
        return self._client.request(self.RESOURCE_URL, "ka10010", kwargs, cont_yn, next_key)

    def industry_investor_net_buy(
        self, cont_yn: str = "N", next_key: str = "", **kwargs: Any
    ) -> dict[str, Any]:
        """업종별투자자순매수요청 (Industry Investor Net Buy)"""
        return self._client.request(self.RESOURCE_URL, "ka10051", kwargs, cont_yn, next_key)

    def industry_current_price(
        self, cont_yn: str = "N", next_key: str = "", **kwargs: Any
    ) -> dict[str, Any]:
        """업종현재가요청 (Industry Current Price)"""
        return self._client.request(self.RESOURCE_URL, "ka20001", kwargs, cont_yn, next_key)

    def industry_stock_price(
        self, cont_yn: str = "N", next_key: str = "", **kwargs: Any
    ) -> dict[str, Any]:
        """업종별주가요청 (Industry Stock Price)"""
        return self._client.request(self.RESOURCE_URL, "ka20002", kwargs, cont_yn, next_key)

    def all_industry_index(
        self, cont_yn: str = "N", next_key: str = "", **kwargs: Any
    ) -> dict[str, Any]:
        """전업종지수요청 (All Industry Index)"""
        return self._client.request(self.RESOURCE_URL, "ka20003", kwargs, cont_yn, next_key)

    def industry_daily_price(
        self, cont_yn: str = "N", next_key: str = "", **kwargs: Any
    ) -> dict[str, Any]:
        """업종현재가일별요청 (Industry Daily Price)"""
        return self._client.request(self.RESOURCE_URL, "ka20009", kwargs, cont_yn, next_key)
