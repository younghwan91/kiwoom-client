"""Chart (차트) endpoints for the Kiwoom REST API."""

from __future__ import annotations

from typing import Any

from kiwoom_rest_api.base import BaseClient


class Chart:
    """Wraps all Chart (차트) endpoints under /api/dostk/chart.

    Args:
        client: Authenticated BaseClient instance.
    """

    RESOURCE_URL = "/api/dostk/chart"

    def __init__(self, client: BaseClient) -> None:
        self._client = client

    def investor_institution_chart(
        self, cont_yn: str = "N", next_key: str = "", **kwargs: Any
    ) -> dict[str, Any]:
        """종목별투자자기관별차트요청 (Investor/Institution Chart by Stock)"""
        return self._client.request(self.RESOURCE_URL, "ka10060", kwargs, cont_yn, next_key)

    def intraday_investor_chart(
        self, cont_yn: str = "N", next_key: str = "", **kwargs: Any
    ) -> dict[str, Any]:
        """시간대별투자자매매차트요청 (Intraday Investor Trading Chart by Time Slot)"""
        return self._client.request(self.RESOURCE_URL, "ka10064", kwargs, cont_yn, next_key)

    def stock_tick_chart(
        self, cont_yn: str = "N", next_key: str = "", **kwargs: Any
    ) -> dict[str, Any]:
        """주식틱차트요청 (Stock Tick Chart)"""
        return self._client.request(self.RESOURCE_URL, "ka10079", kwargs, cont_yn, next_key)

    def stock_minute_chart(
        self, cont_yn: str = "N", next_key: str = "", **kwargs: Any
    ) -> dict[str, Any]:
        """주식분봉차트요청 (Stock Minute Chart)"""
        return self._client.request(self.RESOURCE_URL, "ka10080", kwargs, cont_yn, next_key)

    def stock_daily_chart(
        self, cont_yn: str = "N", next_key: str = "", **kwargs: Any
    ) -> dict[str, Any]:
        """주식일봉차트요청 (Stock Daily Chart)"""
        return self._client.request(self.RESOURCE_URL, "ka10081", kwargs, cont_yn, next_key)

    def stock_weekly_chart(
        self, cont_yn: str = "N", next_key: str = "", **kwargs: Any
    ) -> dict[str, Any]:
        """주식주봉차트요청 (Stock Weekly Chart)"""
        return self._client.request(self.RESOURCE_URL, "ka10082", kwargs, cont_yn, next_key)

    def stock_monthly_chart(
        self, cont_yn: str = "N", next_key: str = "", **kwargs: Any
    ) -> dict[str, Any]:
        """주식월봉차트요청 (Stock Monthly Chart)"""
        return self._client.request(self.RESOURCE_URL, "ka10083", kwargs, cont_yn, next_key)

    def stock_yearly_chart(
        self, cont_yn: str = "N", next_key: str = "", **kwargs: Any
    ) -> dict[str, Any]:
        """주식년봉차트요청 (Stock Yearly Chart)"""
        return self._client.request(self.RESOURCE_URL, "ka10094", kwargs, cont_yn, next_key)

    def industry_tick_chart(
        self, cont_yn: str = "N", next_key: str = "", **kwargs: Any
    ) -> dict[str, Any]:
        """업종틱차트요청 (Industry Tick Chart)"""
        return self._client.request(self.RESOURCE_URL, "ka20004", kwargs, cont_yn, next_key)

    def industry_minute_chart(
        self, cont_yn: str = "N", next_key: str = "", **kwargs: Any
    ) -> dict[str, Any]:
        """업종분봉차트요청 (Industry Minute Chart)"""
        return self._client.request(self.RESOURCE_URL, "ka20005", kwargs, cont_yn, next_key)

    def industry_daily_chart(
        self, cont_yn: str = "N", next_key: str = "", **kwargs: Any
    ) -> dict[str, Any]:
        """업종일봉차트요청 (Industry Daily Chart)"""
        return self._client.request(self.RESOURCE_URL, "ka20006", kwargs, cont_yn, next_key)

    def industry_weekly_chart(
        self, cont_yn: str = "N", next_key: str = "", **kwargs: Any
    ) -> dict[str, Any]:
        """업종주봉차트요청 (Industry Weekly Chart)"""
        return self._client.request(self.RESOURCE_URL, "ka20007", kwargs, cont_yn, next_key)

    def industry_monthly_chart(
        self, cont_yn: str = "N", next_key: str = "", **kwargs: Any
    ) -> dict[str, Any]:
        """업종월봉차트요청 (Industry Monthly Chart)"""
        return self._client.request(self.RESOURCE_URL, "ka20008", kwargs, cont_yn, next_key)

    def industry_yearly_chart(
        self, cont_yn: str = "N", next_key: str = "", **kwargs: Any
    ) -> dict[str, Any]:
        """업종년봉차트요청 (Industry Yearly Chart)"""
        return self._client.request(self.RESOURCE_URL, "ka20019", kwargs, cont_yn, next_key)

    def gold_spot_tick_chart(
        self, cont_yn: str = "N", next_key: str = "", **kwargs: Any
    ) -> dict[str, Any]:
        """금현물틱차트조회요청 (Gold Spot Tick Chart)"""
        return self._client.request(self.RESOURCE_URL, "ka50079", kwargs, cont_yn, next_key)

    def gold_spot_minute_chart(
        self, cont_yn: str = "N", next_key: str = "", **kwargs: Any
    ) -> dict[str, Any]:
        """금현물분봉차트조회요청 (Gold Spot Minute Chart)"""
        return self._client.request(self.RESOURCE_URL, "ka50080", kwargs, cont_yn, next_key)

    def gold_spot_daily_chart(
        self, cont_yn: str = "N", next_key: str = "", **kwargs: Any
    ) -> dict[str, Any]:
        """금현물일봉차트조회요청 (Gold Spot Daily Chart)"""
        return self._client.request(self.RESOURCE_URL, "ka50081", kwargs, cont_yn, next_key)

    def gold_spot_weekly_chart(
        self, cont_yn: str = "N", next_key: str = "", **kwargs: Any
    ) -> dict[str, Any]:
        """금현물주봉차트조회요청 (Gold Spot Weekly Chart)"""
        return self._client.request(self.RESOURCE_URL, "ka50082", kwargs, cont_yn, next_key)

    def gold_spot_monthly_chart(
        self, cont_yn: str = "N", next_key: str = "", **kwargs: Any
    ) -> dict[str, Any]:
        """금현물월봉차트조회요청 (Gold Spot Monthly Chart)"""
        return self._client.request(self.RESOURCE_URL, "ka50083", kwargs, cont_yn, next_key)

    def gold_spot_intraday_tick_chart(
        self, cont_yn: str = "N", next_key: str = "", **kwargs: Any
    ) -> dict[str, Any]:
        """금현물당일틱차트조회요청 (Gold Spot Intraday Tick Chart)"""
        return self._client.request(self.RESOURCE_URL, "ka50091", kwargs, cont_yn, next_key)

    def gold_spot_intraday_minute_chart(
        self, cont_yn: str = "N", next_key: str = "", **kwargs: Any
    ) -> dict[str, Any]:
        """금현물당일분봉차트조회요청 (Gold Spot Intraday Minute Chart)"""
        return self._client.request(self.RESOURCE_URL, "ka50092", kwargs, cont_yn, next_key)
