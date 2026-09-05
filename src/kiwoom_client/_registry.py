"""The endpoint-module registry shared by the sync and async facades.

Defining the 15 lazy module properties once, generic over the response type,
keeps ``KiwoomAPI`` and ``AsyncKiwoomAPI`` from drifting apart while leaving
both fully typed: ``api.account`` resolves to ``Account[dict]`` on the sync
facade and ``Account[Awaitable[dict]]`` on the async one.
"""

from __future__ import annotations

from typing import Generic

from kiwoom_client.base import ClientProtocol, ResponseT
from kiwoom_client.domestic.account import Account
from kiwoom_client.domestic.chart import Chart
from kiwoom_client.domestic.condition_search import ConditionSearch
from kiwoom_client.domestic.credit_order import CreditOrder
from kiwoom_client.domestic.elw import ELW
from kiwoom_client.domestic.etf import ETF
from kiwoom_client.domestic.foreign_institution import ForeignInstitution
from kiwoom_client.domestic.market import Market
from kiwoom_client.domestic.order import Order
from kiwoom_client.domestic.ranking import Ranking
from kiwoom_client.domestic.sector import Sector
from kiwoom_client.domestic.short_selling import ShortSelling
from kiwoom_client.domestic.slb import SLB
from kiwoom_client.domestic.stock_info import StockInfo
from kiwoom_client.domestic.theme import Theme

#: Property name → module class, in the order they appear on the facades.
MODULE_NAMES = (
    "account",
    "stock_info",
    "market",
    "chart",
    "order",
    "credit_order",
    "ranking",
    "sector",
    "foreign_institution",
    "short_selling",
    "slb",
    "theme",
    "condition_search",
    "elw",
    "etf",
)


class ModuleRegistry(Generic[ResponseT]):
    """Lazily instantiates the endpoint modules against a client."""

    _client: ClientProtocol[ResponseT]

    def _init_modules(self) -> None:
        self._account: Account[ResponseT] | None = None
        self._stock_info: StockInfo[ResponseT] | None = None
        self._market: Market[ResponseT] | None = None
        self._chart: Chart[ResponseT] | None = None
        self._order: Order[ResponseT] | None = None
        self._credit_order: CreditOrder[ResponseT] | None = None
        self._ranking: Ranking[ResponseT] | None = None
        self._sector: Sector[ResponseT] | None = None
        self._foreign_institution: ForeignInstitution[ResponseT] | None = None
        self._short_selling: ShortSelling[ResponseT] | None = None
        self._slb: SLB[ResponseT] | None = None
        self._theme: Theme[ResponseT] | None = None
        self._condition_search: ConditionSearch | None = None
        self._elw: ELW[ResponseT] | None = None
        self._etf: ETF[ResponseT] | None = None

    @property
    def account(self) -> Account[ResponseT]:
        """계좌 (Account) endpoints."""
        if self._account is None:
            self._account = Account(self._client)
        return self._account

    @property
    def stock_info(self) -> StockInfo[ResponseT]:
        """종목정보 (Stock Information) endpoints."""
        if self._stock_info is None:
            self._stock_info = StockInfo(self._client)
        return self._stock_info

    @property
    def market(self) -> Market[ResponseT]:
        """시세 (Market Condition) endpoints."""
        if self._market is None:
            self._market = Market(self._client)
        return self._market

    @property
    def chart(self) -> Chart[ResponseT]:
        """차트 (Chart) endpoints."""
        if self._chart is None:
            self._chart = Chart(self._client)
        return self._chart

    @property
    def order(self) -> Order[ResponseT]:
        """주문 (Order) endpoints."""
        if self._order is None:
            self._order = Order(self._client)
        return self._order

    @property
    def credit_order(self) -> CreditOrder[ResponseT]:
        """신용주문 (Credit Order) endpoints."""
        if self._credit_order is None:
            self._credit_order = CreditOrder(self._client)
        return self._credit_order

    @property
    def ranking(self) -> Ranking[ResponseT]:
        """순위정보 (Ranking) endpoints."""
        if self._ranking is None:
            self._ranking = Ranking(self._client)
        return self._ranking

    @property
    def sector(self) -> Sector[ResponseT]:
        """업종 (Sector) endpoints."""
        if self._sector is None:
            self._sector = Sector(self._client)
        return self._sector

    @property
    def foreign_institution(self) -> ForeignInstitution[ResponseT]:
        """기관/외국인 (Foreign/Institution) endpoints."""
        if self._foreign_institution is None:
            self._foreign_institution = ForeignInstitution(self._client)
        return self._foreign_institution

    @property
    def short_selling(self) -> ShortSelling[ResponseT]:
        """공매도 (Short Selling) endpoints."""
        if self._short_selling is None:
            self._short_selling = ShortSelling(self._client)
        return self._short_selling

    @property
    def slb(self) -> SLB[ResponseT]:
        """대차거래 (Stock Lending & Borrowing) endpoints."""
        if self._slb is None:
            self._slb = SLB(self._client)
        return self._slb

    @property
    def theme(self) -> Theme[ResponseT]:
        """테마 (Theme) endpoints."""
        if self._theme is None:
            self._theme = Theme(self._client)
        return self._theme

    @property
    def condition_search(self) -> ConditionSearch:
        """조건검색 (Condition Search) endpoints (WebSocket).

        Builds request payloads only — these travel over the WebSocket, so the
        methods are the same whether the facade is sync or async.
        """
        if self._condition_search is None:
            self._condition_search = ConditionSearch(self._client)
        return self._condition_search

    @property
    def elw(self) -> ELW[ResponseT]:
        """ELW endpoints."""
        if self._elw is None:
            self._elw = ELW(self._client)
        return self._elw

    @property
    def etf(self) -> ETF[ResponseT]:
        """ETF endpoints."""
        if self._etf is None:
            self._etf = ETF(self._client)
        return self._etf
