"""Kiwoom REST API Python Wrapper (키움 REST API).

A comprehensive Python client for Kiwoom Securities REST API,
covering all domestic stock (국내주식) endpoints.

Usage:
    from kiwoom_rest_api import KiwoomAPI

    api = KiwoomAPI(app_key="YOUR_KEY", app_secret="YOUR_SECRET")
    api.login()

    # Get stock info
    info = api.stock_info.basic_stock_info(stk_cd="005930")

    # Place order
    result = api.order.buy_order(stk_cd="005930", ord_qty=10, ord_uv=70000, ...)
"""

from __future__ import annotations

from typing import Any

from kiwoom_rest_api.auth import KiwoomAuth
from kiwoom_rest_api.base import BaseClient, KiwoomAPIError
from kiwoom_rest_api.domestic.account import Account
from kiwoom_rest_api.domestic.chart import Chart
from kiwoom_rest_api.domestic.condition_search import ConditionSearch
from kiwoom_rest_api.domestic.credit_order import CreditOrder
from kiwoom_rest_api.domestic.elw import ELW
from kiwoom_rest_api.domestic.etf import ETF
from kiwoom_rest_api.domestic.foreign_institution import ForeignInstitution
from kiwoom_rest_api.domestic.market import Market
from kiwoom_rest_api.domestic.order import Order
from kiwoom_rest_api.domestic.ranking import Ranking
from kiwoom_rest_api.domestic.sector import Sector
from kiwoom_rest_api.domestic.short_selling import ShortSelling
from kiwoom_rest_api.domestic.slb import SLB
from kiwoom_rest_api.domestic.stock_info import StockInfo
from kiwoom_rest_api.domestic.theme import Theme
from kiwoom_rest_api.websocket import KiwoomWebSocket

__version__ = "0.1.0"
__all__ = ["KiwoomAPI", "KiwoomAPIError", "KiwoomWebSocket"]


class KiwoomAPI:
    """Unified facade for all Kiwoom REST API endpoints.

    Args:
        app_key: API app key from Kiwoom developer portal.
        app_secret: API app secret from Kiwoom developer portal.
        base_url: Override API base URL.
        is_mock: Use mock trading server if True.
    """

    def __init__(
        self,
        app_key: str,
        app_secret: str,
        base_url: str | None = None,
        is_mock: bool = False,
    ):
        self._client = BaseClient(app_key, app_secret, base_url, is_mock)
        self._auth = KiwoomAuth(app_key, app_secret, self._client.base_url)
        self._is_mock = is_mock

        # Domestic stock modules
        self._account: Account | None = None
        self._stock_info: StockInfo | None = None
        self._market: Market | None = None
        self._chart: Chart | None = None
        self._order: Order | None = None
        self._credit_order: CreditOrder | None = None
        self._ranking: Ranking | None = None
        self._sector: Sector | None = None
        self._foreign_institution: ForeignInstitution | None = None
        self._short_selling: ShortSelling | None = None
        self._slb: SLB | None = None
        self._theme: Theme | None = None
        self._condition_search: ConditionSearch | None = None
        self._elw: ELW | None = None
        self._etf: ETF | None = None

    def login(self) -> dict[str, Any]:
        """Authenticate and obtain access token.

        Returns:
            Token response dict from the API.
        """
        result = self._auth.issue_token()
        token = result.get("token") or result.get("access_token", "")
        self._client.access_token = token
        return result

    def logout(self) -> dict[str, Any]:
        """Revoke the current access token."""
        if not self._client.access_token:
            raise RuntimeError("Not logged in")
        result = self._auth.revoke_token(self._client.access_token)
        self._client.access_token = None
        return result

    def close(self) -> None:
        """Close all connections."""
        self._client.close()
        self._auth.close()

    def __enter__(self) -> KiwoomAPI:
        return self

    def __exit__(self, *args: Any) -> None:
        self.close()

    def create_websocket(self) -> KiwoomWebSocket:
        """Create a WebSocket client for real-time data.

        Returns:
            KiwoomWebSocket instance configured with current auth.
        """
        if not self._client.access_token:
            raise RuntimeError("Not logged in. Call login() first.")
        return KiwoomWebSocket(self._client.access_token, self._is_mock)

    # --- Lazy-loaded sub-module properties ---

    @property
    def account(self) -> Account:
        """계좌 (Account) endpoints."""
        if self._account is None:
            self._account = Account(self._client)
        return self._account

    @property
    def stock_info(self) -> StockInfo:
        """종목정보 (Stock Information) endpoints."""
        if self._stock_info is None:
            self._stock_info = StockInfo(self._client)
        return self._stock_info

    @property
    def market(self) -> Market:
        """시세 (Market Condition) endpoints."""
        if self._market is None:
            self._market = Market(self._client)
        return self._market

    @property
    def chart(self) -> Chart:
        """차트 (Chart) endpoints."""
        if self._chart is None:
            self._chart = Chart(self._client)
        return self._chart

    @property
    def order(self) -> Order:
        """주문 (Order) endpoints."""
        if self._order is None:
            self._order = Order(self._client)
        return self._order

    @property
    def credit_order(self) -> CreditOrder:
        """신용주문 (Credit Order) endpoints."""
        if self._credit_order is None:
            self._credit_order = CreditOrder(self._client)
        return self._credit_order

    @property
    def ranking(self) -> Ranking:
        """순위정보 (Ranking) endpoints."""
        if self._ranking is None:
            self._ranking = Ranking(self._client)
        return self._ranking

    @property
    def sector(self) -> Sector:
        """업종 (Sector) endpoints."""
        if self._sector is None:
            self._sector = Sector(self._client)
        return self._sector

    @property
    def foreign_institution(self) -> ForeignInstitution:
        """기관/외국인 (Foreign/Institution) endpoints."""
        if self._foreign_institution is None:
            self._foreign_institution = ForeignInstitution(self._client)
        return self._foreign_institution

    @property
    def short_selling(self) -> ShortSelling:
        """공매도 (Short Selling) endpoints."""
        if self._short_selling is None:
            self._short_selling = ShortSelling(self._client)
        return self._short_selling

    @property
    def slb(self) -> SLB:
        """대차거래 (Stock Lending & Borrowing) endpoints."""
        if self._slb is None:
            self._slb = SLB(self._client)
        return self._slb

    @property
    def theme(self) -> Theme:
        """테마 (Theme) endpoints."""
        if self._theme is None:
            self._theme = Theme(self._client)
        return self._theme

    @property
    def condition_search(self) -> ConditionSearch:
        """조건검색 (Condition Search) endpoints (WebSocket)."""
        if self._condition_search is None:
            self._condition_search = ConditionSearch(self._client)
        return self._condition_search

    @property
    def elw(self) -> ELW:
        """ELW endpoints."""
        if self._elw is None:
            self._elw = ELW(self._client)
        return self._elw

    @property
    def etf(self) -> ETF:
        """ETF endpoints."""
        if self._etf is None:
            self._etf = ETF(self._client)
        return self._etf
