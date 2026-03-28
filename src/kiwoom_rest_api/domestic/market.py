"""Market (시세) endpoints for the Kiwoom REST API."""

from __future__ import annotations

from typing import Any

from kiwoom_rest_api.base import BaseClient


class Market:
    """Wraps all Market (시세) endpoints under /api/dostk/mrkcond.

    Args:
        client: Authenticated BaseClient instance.
    """

    RESOURCE_URL = "/api/dostk/mrkcond"

    def __init__(self, client: BaseClient) -> None:
        self._client = client

    def stock_quote(
        self, cont_yn: str = "N", next_key: str = "", **kwargs: Any
    ) -> dict[str, Any]:
        """주식호가요청 (Stock Quote)"""
        return self._client.request(self.RESOURCE_URL, "ka10004", kwargs, cont_yn, next_key)

    def stock_daily_weekly_monthly(
        self, cont_yn: str = "N", next_key: str = "", **kwargs: Any
    ) -> dict[str, Any]:
        """주식일주월시분요청 (Stock Daily/Weekly/Monthly by Time)"""
        return self._client.request(self.RESOURCE_URL, "ka10005", kwargs, cont_yn, next_key)

    def stock_minute_price(
        self, cont_yn: str = "N", next_key: str = "", **kwargs: Any
    ) -> dict[str, Any]:
        """주식시분요청 (Stock Minute Price)"""
        return self._client.request(self.RESOURCE_URL, "ka10006", kwargs, cont_yn, next_key)

    def order_book_info(
        self, cont_yn: str = "N", next_key: str = "", **kwargs: Any
    ) -> dict[str, Any]:
        """시세표성정보요청 (Order Book Info)"""
        return self._client.request(self.RESOURCE_URL, "ka10007", kwargs, cont_yn, next_key)

    def rights_issue_price(
        self, cont_yn: str = "N", next_key: str = "", **kwargs: Any
    ) -> dict[str, Any]:
        """신주인수권전체시세요청 (Rights Issue Price)"""
        return self._client.request(self.RESOURCE_URL, "ka10011", kwargs, cont_yn, next_key)

    def daily_institutional_trading(
        self, cont_yn: str = "N", next_key: str = "", **kwargs: Any
    ) -> dict[str, Any]:
        """일별기관매매종목요청 (Daily Institutional Trading by Stock)"""
        return self._client.request(self.RESOURCE_URL, "ka10044", kwargs, cont_yn, next_key)

    def institutional_trading_trend(
        self, cont_yn: str = "N", next_key: str = "", **kwargs: Any
    ) -> dict[str, Any]:
        """종목별기관매매추이요청 (Institutional Trading Trend by Stock)"""
        return self._client.request(self.RESOURCE_URL, "ka10045", kwargs, cont_yn, next_key)

    def hourly_execution_strength(
        self, cont_yn: str = "N", next_key: str = "", **kwargs: Any
    ) -> dict[str, Any]:
        """체결강도추이시간별요청 (Hourly Execution Strength)"""
        return self._client.request(self.RESOURCE_URL, "ka10046", kwargs, cont_yn, next_key)

    def daily_execution_strength(
        self, cont_yn: str = "N", next_key: str = "", **kwargs: Any
    ) -> dict[str, Any]:
        """체결강도추이일별요청 (Daily Execution Strength)"""
        return self._client.request(self.RESOURCE_URL, "ka10047", kwargs, cont_yn, next_key)

    def intraday_investor_trading(
        self, cont_yn: str = "N", next_key: str = "", **kwargs: Any
    ) -> dict[str, Any]:
        """장중투자자별매매요청 (Intraday Investor Trading by Time Slot)"""
        return self._client.request(self.RESOURCE_URL, "ka10063", kwargs, cont_yn, next_key)

    def after_hours_investor_trading(
        self, cont_yn: str = "N", next_key: str = "", **kwargs: Any
    ) -> dict[str, Any]:
        """장마감후투자자별매매요청 (After-Hours Investor Trading)"""
        return self._client.request(self.RESOURCE_URL, "ka10066", kwargs, cont_yn, next_key)

    def broker_stock_trading_trend(
        self, cont_yn: str = "N", next_key: str = "", **kwargs: Any
    ) -> dict[str, Any]:
        """증권사별종목매매동향요청 (Broker Stock Trading Trend)"""
        return self._client.request(self.RESOURCE_URL, "ka10078", kwargs, cont_yn, next_key)

    def daily_stock_price(
        self, cont_yn: str = "N", next_key: str = "", **kwargs: Any
    ) -> dict[str, Any]:
        """일자별주가요청 (Daily Stock Price)"""
        return self._client.request(self.RESOURCE_URL, "ka10086", kwargs, cont_yn, next_key)

    def after_hours_single_price(
        self, cont_yn: str = "N", next_key: str = "", **kwargs: Any
    ) -> dict[str, Any]:
        """시간외단일가요청 (After-Hours Single Price)"""
        return self._client.request(self.RESOURCE_URL, "ka10087", kwargs, cont_yn, next_key)

    def program_trading_by_time(
        self, cont_yn: str = "N", next_key: str = "", **kwargs: Any
    ) -> dict[str, Any]:
        """프로그램매매추이요청 시간대별 (Program Trading by Time Slot)"""
        return self._client.request(self.RESOURCE_URL, "ka90005", kwargs, cont_yn, next_key)

    def program_arbitrage_balance(
        self, cont_yn: str = "N", next_key: str = "", **kwargs: Any
    ) -> dict[str, Any]:
        """프로그램매매차익잔고추이요청 (Program Arbitrage Balance Trend)"""
        return self._client.request(self.RESOURCE_URL, "ka90006", kwargs, cont_yn, next_key)

    def cumulative_program_trading(
        self, cont_yn: str = "N", next_key: str = "", **kwargs: Any
    ) -> dict[str, Any]:
        """프로그램매매누적추이요청 (Cumulative Program Trading Trend)"""
        return self._client.request(self.RESOURCE_URL, "ka90007", kwargs, cont_yn, next_key)

    def program_trading_by_stock_time(
        self, cont_yn: str = "N", next_key: str = "", **kwargs: Any
    ) -> dict[str, Any]:
        """종목시간별프로그램매매추이요청 (Program Trading by Stock and Time Slot)"""
        return self._client.request(self.RESOURCE_URL, "ka90008", kwargs, cont_yn, next_key)

    def program_trading_by_date(
        self, cont_yn: str = "N", next_key: str = "", **kwargs: Any
    ) -> dict[str, Any]:
        """프로그램매매추이요청 일자별 (Program Trading by Date)"""
        return self._client.request(self.RESOURCE_URL, "ka90010", kwargs, cont_yn, next_key)

    def program_trading_by_stock_day(
        self, cont_yn: str = "N", next_key: str = "", **kwargs: Any
    ) -> dict[str, Any]:
        """종목일별프로그램매매추이요청 (Program Trading by Stock and Day)"""
        return self._client.request(self.RESOURCE_URL, "ka90013", kwargs, cont_yn, next_key)

    def gold_spot_execution_trend(
        self, cont_yn: str = "N", next_key: str = "", **kwargs: Any
    ) -> dict[str, Any]:
        """금현물체결추이 (Gold Spot Execution Trend)"""
        return self._client.request(self.RESOURCE_URL, "ka50010", kwargs, cont_yn, next_key)

    def gold_spot_daily_trend(
        self, cont_yn: str = "N", next_key: str = "", **kwargs: Any
    ) -> dict[str, Any]:
        """금현물일별추이 (Gold Spot Daily Trend)"""
        return self._client.request(self.RESOURCE_URL, "ka50012", kwargs, cont_yn, next_key)

    def gold_spot_expected_execution(
        self, cont_yn: str = "N", next_key: str = "", **kwargs: Any
    ) -> dict[str, Any]:
        """금현물예상체결 (Gold Spot Expected Execution)"""
        return self._client.request(self.RESOURCE_URL, "ka50087", kwargs, cont_yn, next_key)

    def gold_spot_price_info(
        self, cont_yn: str = "N", next_key: str = "", **kwargs: Any
    ) -> dict[str, Any]:
        """금현물 시세정보 (Gold Spot Price Info)"""
        return self._client.request(self.RESOURCE_URL, "ka50100", kwargs, cont_yn, next_key)

    def gold_spot_order_book(
        self, cont_yn: str = "N", next_key: str = "", **kwargs: Any
    ) -> dict[str, Any]:
        """금현물 호가 (Gold Spot Order Book)"""
        return self._client.request(self.RESOURCE_URL, "ka50101", kwargs, cont_yn, next_key)
