"""ETF endpoints for the Kiwoom REST API."""

from __future__ import annotations

from typing import Any, Generic

from kiwoom_client.base import ClientProtocol, ResponseT


class ETF(Generic[ResponseT]):
    """Wraps all ETF endpoints under /api/dostk/etf.

    Args:
        client: An authenticated BaseClient (sync) or AsyncBaseClient.
    """

    RESOURCE_URL = "/api/dostk/etf"

    def __init__(self, client: ClientProtocol[ResponseT]) -> None:
        self._client = client

    def return_rate(
        self, cont_yn: str = "N", next_key: str = "", **kwargs: Any
    ) -> ResponseT:
        """ETF수익률요청 (ETF Return Rate)"""
        return self._client.request(self.RESOURCE_URL, "ka40001", kwargs, cont_yn, next_key)

    def stock_info(
        self, cont_yn: str = "N", next_key: str = "", **kwargs: Any
    ) -> ResponseT:
        """ETF종목정보요청 (ETF Stock Info)"""
        return self._client.request(self.RESOURCE_URL, "ka40002", kwargs, cont_yn, next_key)

    def daily_trend(
        self, cont_yn: str = "N", next_key: str = "", **kwargs: Any
    ) -> ResponseT:
        """ETF일별추이요청 (ETF Daily Trend)"""
        return self._client.request(self.RESOURCE_URL, "ka40003", kwargs, cont_yn, next_key)

    def overall_market_price(
        self, cont_yn: str = "N", next_key: str = "", **kwargs: Any
    ) -> ResponseT:
        """ETF전체시세요청 (ETF Overall Market Price)"""
        return self._client.request(self.RESOURCE_URL, "ka40004", kwargs, cont_yn, next_key)

    def time_segment_trend(
        self, cont_yn: str = "N", next_key: str = "", **kwargs: Any
    ) -> ResponseT:
        """ETF시간대별추이요청 (ETF Time Segment Trend)"""
        return self._client.request(self.RESOURCE_URL, "ka40006", kwargs, cont_yn, next_key)

    def time_segment_execution(
        self, cont_yn: str = "N", next_key: str = "", **kwargs: Any
    ) -> ResponseT:
        """ETF시간대별체결요청 (ETF Time Segment Execution)"""
        return self._client.request(self.RESOURCE_URL, "ka40007", kwargs, cont_yn, next_key)

    def daily_execution(
        self, cont_yn: str = "N", next_key: str = "", **kwargs: Any
    ) -> ResponseT:
        """ETF일자별체결요청 (ETF Daily Execution)"""
        return self._client.request(self.RESOURCE_URL, "ka40008", kwargs, cont_yn, next_key)

    def time_nav(
        self, cont_yn: str = "N", next_key: str = "", **kwargs: Any
    ) -> ResponseT:
        """ETF시간대별NAV요청 (ETF Time NAV)"""
        return self._client.request(self.RESOURCE_URL, "ka40009", kwargs, cont_yn, next_key)

    def time_trend(
        self, cont_yn: str = "N", next_key: str = "", **kwargs: Any
    ) -> ResponseT:
        """ETF시간대별추이요청 (ETF Time Trend)"""
        return self._client.request(self.RESOURCE_URL, "ka40010", kwargs, cont_yn, next_key)
