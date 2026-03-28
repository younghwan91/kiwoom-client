"""Stock Info (종목정보) endpoints for the Kiwoom REST API."""

from __future__ import annotations

from typing import Any

from kiwoom_rest_api.base import BaseClient


class StockInfo:
    """Wraps all Stock Info (종목정보) endpoints under /api/dostk/stkinfo.

    Args:
        client: Authenticated BaseClient instance.
    """

    RESOURCE_URL = "/api/dostk/stkinfo"

    def __init__(self, client: BaseClient) -> None:
        self._client = client

    def basic_stock_info(
        self, cont_yn: str = "N", next_key: str = "", **kwargs: Any
    ) -> dict[str, Any]:
        """종목기본정보요청 (Basic Stock Info)"""
        return self._client.request(self.RESOURCE_URL, "ka10001", kwargs, cont_yn, next_key)

    def stock_trading_agent(
        self, cont_yn: str = "N", next_key: str = "", **kwargs: Any
    ) -> dict[str, Any]:
        """종목거래원요청 (Stock Trading Agent)"""
        return self._client.request(self.RESOURCE_URL, "ka10002", kwargs, cont_yn, next_key)

    def execution_info(
        self, cont_yn: str = "N", next_key: str = "", **kwargs: Any
    ) -> dict[str, Any]:
        """체결정보요청 (Execution Info)"""
        return self._client.request(self.RESOURCE_URL, "ka10003", kwargs, cont_yn, next_key)

    def credit_trading_trend(
        self, cont_yn: str = "N", next_key: str = "", **kwargs: Any
    ) -> dict[str, Any]:
        """신용매매동향요청 (Credit Trading Trend)"""
        return self._client.request(self.RESOURCE_URL, "ka10013", kwargs, cont_yn, next_key)

    def daily_transaction_detail(
        self, cont_yn: str = "N", next_key: str = "", **kwargs: Any
    ) -> dict[str, Any]:
        """일별거래상세요청 (Daily Transaction Detail)"""
        return self._client.request(self.RESOURCE_URL, "ka10015", kwargs, cont_yn, next_key)

    def new_high_low(
        self, cont_yn: str = "N", next_key: str = "", **kwargs: Any
    ) -> dict[str, Any]:
        """신고저가요청 (New High/Low)"""
        return self._client.request(self.RESOURCE_URL, "ka10016", kwargs, cont_yn, next_key)

    def upper_lower_limit(
        self, cont_yn: str = "N", next_key: str = "", **kwargs: Any
    ) -> dict[str, Any]:
        """상하한가요청 (Upper/Lower Limit Price)"""
        return self._client.request(self.RESOURCE_URL, "ka10017", kwargs, cont_yn, next_key)

    def near_high_low(
        self, cont_yn: str = "N", next_key: str = "", **kwargs: Any
    ) -> dict[str, Any]:
        """고저근접요청 (Near High/Low)"""
        return self._client.request(self.RESOURCE_URL, "ka10018", kwargs, cont_yn, next_key)

    def rapid_price_change(
        self, cont_yn: str = "N", next_key: str = "", **kwargs: Any
    ) -> dict[str, Any]:
        """급등락요청 (Rapid Price Change)"""
        return self._client.request(self.RESOURCE_URL, "ka10019", kwargs, cont_yn, next_key)

    def trading_volume_update(
        self, cont_yn: str = "N", next_key: str = "", **kwargs: Any
    ) -> dict[str, Any]:
        """거래량갱신요청 (Trading Volume Update)"""
        return self._client.request(self.RESOURCE_URL, "ka10024", kwargs, cont_yn, next_key)

    def volume_concentration(
        self, cont_yn: str = "N", next_key: str = "", **kwargs: Any
    ) -> dict[str, Any]:
        """매물대집중요청 (Volume Concentration)"""
        return self._client.request(self.RESOURCE_URL, "ka10025", kwargs, cont_yn, next_key)

    def high_low_per(
        self, cont_yn: str = "N", next_key: str = "", **kwargs: Any
    ) -> dict[str, Any]:
        """고저PER요청 (High/Low PER)"""
        return self._client.request(self.RESOURCE_URL, "ka10026", kwargs, cont_yn, next_key)

    def change_rate_vs_opening(
        self, cont_yn: str = "N", next_key: str = "", **kwargs: Any
    ) -> dict[str, Any]:
        """시가대비등락률요청 (Change Rate vs Opening Price)"""
        return self._client.request(self.RESOURCE_URL, "ka10028", kwargs, cont_yn, next_key)

    def trading_agent_supply_demand(
        self, cont_yn: str = "N", next_key: str = "", **kwargs: Any
    ) -> dict[str, Any]:
        """거래원매물대분석요청 (Trading Agent Supply/Demand Trend Analysis)"""
        return self._client.request(self.RESOURCE_URL, "ka10043", kwargs, cont_yn, next_key)

    def trading_agent_instant_volume(
        self, cont_yn: str = "N", next_key: str = "", **kwargs: Any
    ) -> dict[str, Any]:
        """거래원순간거래량요청 (Trading Agent Instant Volume)"""
        return self._client.request(self.RESOURCE_URL, "ka10052", kwargs, cont_yn, next_key)

    def vi_triggered_stocks(
        self, cont_yn: str = "N", next_key: str = "", **kwargs: Any
    ) -> dict[str, Any]:
        """변동성완화장치발동종목요청 (VI Triggered Stocks)"""
        return self._client.request(self.RESOURCE_URL, "ka10054", kwargs, cont_yn, next_key)

    def today_vs_yesterday_volume(
        self, cont_yn: str = "N", next_key: str = "", **kwargs: Any
    ) -> dict[str, Any]:
        """당일전일체결량요청 (Today vs Yesterday Execution Volume)"""
        return self._client.request(self.RESOURCE_URL, "ka10055", kwargs, cont_yn, next_key)

    def daily_trading_by_investor(
        self, cont_yn: str = "N", next_key: str = "", **kwargs: Any
    ) -> dict[str, Any]:
        """투자자별일별매매종목요청 (Daily Trading by Investor)"""
        return self._client.request(self.RESOURCE_URL, "ka10058", kwargs, cont_yn, next_key)

    def investor_institution_by_stock(
        self, cont_yn: str = "N", next_key: str = "", **kwargs: Any
    ) -> dict[str, Any]:
        """투자자기관별종목별요청 (Investor/Institution by Stock)"""
        return self._client.request(self.RESOURCE_URL, "ka10059", kwargs, cont_yn, next_key)

    def investor_institution_aggregate(
        self, cont_yn: str = "N", next_key: str = "", **kwargs: Any
    ) -> dict[str, Any]:
        """종목별투자자기관별합계요청 (Investor/Institution by Stock Aggregate)"""
        return self._client.request(self.RESOURCE_URL, "ka10061", kwargs, cont_yn, next_key)

    def today_vs_yesterday_execution(
        self, cont_yn: str = "N", next_key: str = "", **kwargs: Any
    ) -> dict[str, Any]:
        """당일전일체결요청 (Today vs Yesterday Execution)"""
        return self._client.request(self.RESOURCE_URL, "ka10084", kwargs, cont_yn, next_key)

    def watchlist_stock_info(
        self, cont_yn: str = "N", next_key: str = "", **kwargs: Any
    ) -> dict[str, Any]:
        """관심종목정보요청 (Watchlist Stock Info)"""
        return self._client.request(self.RESOURCE_URL, "ka10095", kwargs, cont_yn, next_key)

    def stock_info_list(
        self, cont_yn: str = "N", next_key: str = "", **kwargs: Any
    ) -> dict[str, Any]:
        """종목정보 리스트 (Stock Info List)"""
        return self._client.request(self.RESOURCE_URL, "ka10099", kwargs, cont_yn, next_key)

    def stock_info_inquiry(
        self, cont_yn: str = "N", next_key: str = "", **kwargs: Any
    ) -> dict[str, Any]:
        """종목정보 조회 (Stock Info Inquiry)"""
        return self._client.request(self.RESOURCE_URL, "ka10100", kwargs, cont_yn, next_key)

    def industry_code_list(
        self, cont_yn: str = "N", next_key: str = "", **kwargs: Any
    ) -> dict[str, Any]:
        """업종코드 리스트 (Industry Code List)"""
        return self._client.request(self.RESOURCE_URL, "ka10101", kwargs, cont_yn, next_key)

    def member_company_list(
        self, cont_yn: str = "N", next_key: str = "", **kwargs: Any
    ) -> dict[str, Any]:
        """회원사 리스트 (Member Company List)"""
        return self._client.request(self.RESOURCE_URL, "ka10102", kwargs, cont_yn, next_key)

    def program_buy_top50(
        self, cont_yn: str = "N", next_key: str = "", **kwargs: Any
    ) -> dict[str, Any]:
        """프로그램순매수상위50요청 (Program Buy Top 50)"""
        return self._client.request(self.RESOURCE_URL, "ka90003", kwargs, cont_yn, next_key)

    def program_trading_by_stock(
        self, cont_yn: str = "N", next_key: str = "", **kwargs: Any
    ) -> dict[str, Any]:
        """종목별프로그램매매현황요청 (Program Trading by Stock)"""
        return self._client.request(self.RESOURCE_URL, "ka90004", kwargs, cont_yn, next_key)

    def realtime_stock_inquiry_rank(
        self, cont_yn: str = "N", next_key: str = "", **kwargs: Any
    ) -> dict[str, Any]:
        """실시간종목조회순위 (Real-time Stock Inquiry Ranking)"""
        return self._client.request(self.RESOURCE_URL, "ka00198", kwargs, cont_yn, next_key)

    def margin_loan_available_stocks(
        self, cont_yn: str = "N", next_key: str = "", **kwargs: Any
    ) -> dict[str, Any]:
        """신용융자 가능종목요청 (Margin Loan Available Stocks)"""
        return self._client.request(self.RESOURCE_URL, "kt20016", kwargs, cont_yn, next_key)

    def margin_loan_inquiry(
        self, cont_yn: str = "N", next_key: str = "", **kwargs: Any
    ) -> dict[str, Any]:
        """신용융자 가능문의 (Margin Loan Inquiry)"""
        return self._client.request(self.RESOURCE_URL, "kt20017", kwargs, cont_yn, next_key)
