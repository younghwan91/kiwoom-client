"""Ranking (순위) endpoints for the Kiwoom REST API."""

from __future__ import annotations

from typing import Any

from kiwoom_rest_api.base import BaseClient


class Ranking:
    """Wraps all Ranking (순위) endpoints under /api/dostk/rkinfo.

    Args:
        client: Authenticated BaseClient instance.
    """

    RESOURCE_URL = "/api/dostk/rkinfo"

    def __init__(self, client: BaseClient) -> None:
        self._client = client

    def top_order_book_volume(
        self, cont_yn: str = "N", next_key: str = "", **kwargs: Any
    ) -> dict[str, Any]:
        """호가잔량상위요청 (Top Order Book Volume)"""
        return self._client.request(self.RESOURCE_URL, "ka10020", kwargs, cont_yn, next_key)

    def sudden_order_book_increase(
        self, cont_yn: str = "N", next_key: str = "", **kwargs: Any
    ) -> dict[str, Any]:
        """호가잔량급증요청 (Sudden Order Book Increase)"""
        return self._client.request(self.RESOURCE_URL, "ka10021", kwargs, cont_yn, next_key)

    def sudden_order_ratio_increase(
        self, cont_yn: str = "N", next_key: str = "", **kwargs: Any
    ) -> dict[str, Any]:
        """잔량율급증요청 (Sudden Order Ratio Increase)"""
        return self._client.request(self.RESOURCE_URL, "ka10022", kwargs, cont_yn, next_key)

    def sudden_volume_increase(
        self, cont_yn: str = "N", next_key: str = "", **kwargs: Any
    ) -> dict[str, Any]:
        """거래량급증요청 (Sudden Volume Increase)"""
        return self._client.request(self.RESOURCE_URL, "ka10023", kwargs, cont_yn, next_key)

    def top_change_rate(
        self, cont_yn: str = "N", next_key: str = "", **kwargs: Any
    ) -> dict[str, Any]:
        """전일대비등락률상위요청 (Top Change Rate vs Previous Day)"""
        return self._client.request(self.RESOURCE_URL, "ka10027", kwargs, cont_yn, next_key)

    def top_expected_change_rate(
        self, cont_yn: str = "N", next_key: str = "", **kwargs: Any
    ) -> dict[str, Any]:
        """예상체결등락률상위요청 (Top Expected Execution Change Rate)"""
        return self._client.request(self.RESOURCE_URL, "ka10029", kwargs, cont_yn, next_key)

    def top_volume_today(
        self, cont_yn: str = "N", next_key: str = "", **kwargs: Any
    ) -> dict[str, Any]:
        """당일거래량상위요청 (Top Volume Today)"""
        return self._client.request(self.RESOURCE_URL, "ka10030", kwargs, cont_yn, next_key)

    def top_volume_yesterday(
        self, cont_yn: str = "N", next_key: str = "", **kwargs: Any
    ) -> dict[str, Any]:
        """전일거래량상위요청 (Top Volume Yesterday)"""
        return self._client.request(self.RESOURCE_URL, "ka10031", kwargs, cont_yn, next_key)

    def top_trading_value(
        self, cont_yn: str = "N", next_key: str = "", **kwargs: Any
    ) -> dict[str, Any]:
        """거래대금상위요청 (Top Trading Value)"""
        return self._client.request(self.RESOURCE_URL, "ka10032", kwargs, cont_yn, next_key)

    def top_credit_ratio(
        self, cont_yn: str = "N", next_key: str = "", **kwargs: Any
    ) -> dict[str, Any]:
        """신용비율상위요청 (Top Credit Ratio)"""
        return self._client.request(self.RESOURCE_URL, "ka10033", kwargs, cont_yn, next_key)

    def top_foreign_trades_by_period(
        self, cont_yn: str = "N", next_key: str = "", **kwargs: Any
    ) -> dict[str, Any]:
        """외인기간별매매상위요청 (Top Foreign Trades by Period)"""
        return self._client.request(self.RESOURCE_URL, "ka10034", kwargs, cont_yn, next_key)

    def top_foreign_consecutive_buy(
        self, cont_yn: str = "N", next_key: str = "", **kwargs: Any
    ) -> dict[str, Any]:
        """외인연속순매매상위요청 (Top Foreign Consecutive Net Buy)"""
        return self._client.request(self.RESOURCE_URL, "ka10035", kwargs, cont_yn, next_key)

    def top_foreign_limit_increase(
        self, cont_yn: str = "N", next_key: str = "", **kwargs: Any
    ) -> dict[str, Any]:
        """외인한도소진율증가상위 (Top Foreign Limit Exhaustion Rate Increase)"""
        return self._client.request(self.RESOURCE_URL, "ka10036", kwargs, cont_yn, next_key)

    def top_foreign_broker_trading(
        self, cont_yn: str = "N", next_key: str = "", **kwargs: Any
    ) -> dict[str, Any]:
        """외국계창구매매상위요청 (Top Foreign Holding Broker Trading)"""
        return self._client.request(self.RESOURCE_URL, "ka10037", kwargs, cont_yn, next_key)

    def broker_ranking_by_stock(
        self, cont_yn: str = "N", next_key: str = "", **kwargs: Any
    ) -> dict[str, Any]:
        """종목별증권사순위요청 (Broker Ranking by Stock)"""
        return self._client.request(self.RESOURCE_URL, "ka10038", kwargs, cont_yn, next_key)

    def top_broker_by_stock(
        self, cont_yn: str = "N", next_key: str = "", **kwargs: Any
    ) -> dict[str, Any]:
        """증권사별매매상위요청 (Top Broker by Stock)"""
        return self._client.request(self.RESOURCE_URL, "ka10039", kwargs, cont_yn, next_key)

    def main_brokers_today(
        self, cont_yn: str = "N", next_key: str = "", **kwargs: Any
    ) -> dict[str, Any]:
        """당일주요거래원요청 (Main Brokers Today)"""
        return self._client.request(self.RESOURCE_URL, "ka10040", kwargs, cont_yn, next_key)

    def top_net_buying_brokers(
        self, cont_yn: str = "N", next_key: str = "", **kwargs: Any
    ) -> dict[str, Any]:
        """순매수거래원순위요청 (Top Net Buying Brokers)"""
        return self._client.request(self.RESOURCE_URL, "ka10042", kwargs, cont_yn, next_key)

    def departed_brokers_today(
        self, cont_yn: str = "N", next_key: str = "", **kwargs: Any
    ) -> dict[str, Any]:
        """당일상위이탈원요청 (Departed Brokers Today)"""
        return self._client.request(self.RESOURCE_URL, "ka10053", kwargs, cont_yn, next_key)

    def same_day_net_buying_rank(
        self, cont_yn: str = "N", next_key: str = "", **kwargs: Any
    ) -> dict[str, Any]:
        """동일순매매순위요청 (Same Day Net Buying Rank)"""
        return self._client.request(self.RESOURCE_URL, "ka10062", kwargs, cont_yn, next_key)

    def top_intraday_investor_trading(
        self, cont_yn: str = "N", next_key: str = "", **kwargs: Any
    ) -> dict[str, Any]:
        """장중투자자별매매상위요청 (Top Intraday Investor Trading by Time)"""
        return self._client.request(self.RESOURCE_URL, "ka10065", kwargs, cont_yn, next_key)

    def after_hours_change_rate_rank(
        self, cont_yn: str = "N", next_key: str = "", **kwargs: Any
    ) -> dict[str, Any]:
        """시간외단일가등락율순위요청 (After Hours Change Rate Rank)"""
        return self._client.request(self.RESOURCE_URL, "ka10098", kwargs, cont_yn, next_key)

    def top_foreign_institution_trades(
        self, cont_yn: str = "N", next_key: str = "", **kwargs: Any
    ) -> dict[str, Any]:
        """외국인기관매매상위요청 (Top Foreign Institution Trades)"""
        return self._client.request(self.RESOURCE_URL, "ka90009", kwargs, cont_yn, next_key)
