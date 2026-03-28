"""Tests for each domestic stock module - one endpoint per module."""

import pytest

from kiwoom_rest_api import KiwoomAPI


@pytest.fixture
def api(httpx_mock):
    """Create a mock API client."""
    # Mock token endpoint
    httpx_mock.add_response(
        url="https://mockapi.kiwoom.com/oauth2/token",
        json={"token": "test_token", "token_type": "Bearer", "expires_in": 86400},
    )
    api = KiwoomAPI("key", "secret", is_mock=True)
    api.login()
    return api


def _mock_success(httpx_mock, url_path):
    httpx_mock.add_response(
        url=f"https://mockapi.kiwoom.com{url_path}",
        json={"return_code": 0, "return_msg": "OK", "data": "test"},
    )


class TestAccountModule:
    def test_deposit_detail(self, httpx_mock, api):
        _mock_success(httpx_mock, "/api/dostk/acnt")
        result = api.account.deposit_detail()
        assert result["return_code"] == 0

    def test_account_number_inquiry(self, httpx_mock, api):
        _mock_success(httpx_mock, "/api/dostk/acnt")
        result = api.account.account_number_inquiry()
        assert result["return_code"] == 0

    def test_gold_spot_balance(self, httpx_mock, api):
        _mock_success(httpx_mock, "/api/dostk/acnt")
        result = api.account.gold_spot_balance()
        assert result["return_code"] == 0


class TestStockInfoModule:
    def test_basic_stock_info(self, httpx_mock, api):
        _mock_success(httpx_mock, "/api/dostk/stkinfo")
        result = api.stock_info.basic_stock_info(stk_cd="005930")
        assert result["return_code"] == 0

    def test_realtime_stock_inquiry_rank(self, httpx_mock, api):
        _mock_success(httpx_mock, "/api/dostk/stkinfo")
        result = api.stock_info.realtime_stock_inquiry_rank(qry_tp="4")
        assert result["return_code"] == 0

    def test_margin_loan_available_stocks(self, httpx_mock, api):
        _mock_success(httpx_mock, "/api/dostk/stkinfo")
        result = api.stock_info.margin_loan_available_stocks()
        assert result["return_code"] == 0


class TestMarketModule:
    def test_stock_quote(self, httpx_mock, api):
        _mock_success(httpx_mock, "/api/dostk/mrkcond")
        result = api.market.stock_quote(stk_cd="005930")
        assert result["return_code"] == 0

    def test_gold_spot_price_info(self, httpx_mock, api):
        _mock_success(httpx_mock, "/api/dostk/mrkcond")
        result = api.market.gold_spot_price_info()
        assert result["return_code"] == 0


class TestChartModule:
    def test_stock_daily_chart(self, httpx_mock, api):
        _mock_success(httpx_mock, "/api/dostk/chart")
        result = api.chart.stock_daily_chart(stk_cd="005930", base_dt="20260326")
        assert result["return_code"] == 0

    def test_gold_spot_daily_chart(self, httpx_mock, api):
        _mock_success(httpx_mock, "/api/dostk/chart")
        result = api.chart.gold_spot_daily_chart()
        assert result["return_code"] == 0


class TestOrderModule:
    def test_buy_order(self, httpx_mock, api):
        _mock_success(httpx_mock, "/api/dostk/ordr")
        result = api.order.buy_order(stk_cd="005930", ord_qty=10, ord_uv=70000)
        assert result["return_code"] == 0

    def test_gold_spot_buy_order(self, httpx_mock, api):
        _mock_success(httpx_mock, "/api/dostk/ordr")
        result = api.order.gold_spot_buy_order(ord_qty=1, ord_uv=100000)
        assert result["return_code"] == 0


class TestCreditOrderModule:
    def test_margin_buy_order(self, httpx_mock, api):
        _mock_success(httpx_mock, "/api/dostk/crdordr")
        result = api.credit_order.margin_buy_order(stk_cd="005930")
        assert result["return_code"] == 0


class TestRankingModule:
    def test_top_volume_today(self, httpx_mock, api):
        _mock_success(httpx_mock, "/api/dostk/rkinfo")
        result = api.ranking.top_volume_today()
        assert result["return_code"] == 0


class TestSectorModule:
    def test_industry_current_price(self, httpx_mock, api):
        _mock_success(httpx_mock, "/api/dostk/sect")
        result = api.sector.industry_current_price(inds_cd="001")
        assert result["return_code"] == 0


class TestForeignInstitutionModule:
    def test_foreign_trading_trend(self, httpx_mock, api):
        _mock_success(httpx_mock, "/api/dostk/frgnistt")
        result = api.foreign_institution.foreign_trading_trend(stk_cd="005930")
        assert result["return_code"] == 0

    def test_gold_spot_investor_status(self, httpx_mock, api):
        _mock_success(httpx_mock, "/api/dostk/frgnistt")
        result = api.foreign_institution.gold_spot_investor_status()
        assert result["return_code"] == 0


class TestShortSellingModule:
    def test_short_selling_trend(self, httpx_mock, api):
        _mock_success(httpx_mock, "/api/dostk/shsa")
        result = api.short_selling.short_selling_trend(stk_cd="005930")
        assert result["return_code"] == 0


class TestSLBModule:
    def test_lending_trend(self, httpx_mock, api):
        _mock_success(httpx_mock, "/api/dostk/slb")
        result = api.slb.lending_trend()
        assert result["return_code"] == 0


class TestThemeModule:
    def test_theme_group_list(self, httpx_mock, api):
        _mock_success(httpx_mock, "/api/dostk/thme")
        result = api.theme.theme_group_list()
        assert result["return_code"] == 0


class TestConditionSearchModule:
    def test_condition_list(self, api):
        result = api.condition_search.condition_list()
        assert result["api_id"] == "ka10171"


class TestELWModule:
    def test_daily_sensitivity(self, httpx_mock, api):
        _mock_success(httpx_mock, "/api/dostk/elw")
        result = api.elw.daily_sensitivity_indicator(stk_cd="500001")
        assert result["return_code"] == 0


class TestETFModule:
    def test_return_rate(self, httpx_mock, api):
        _mock_success(httpx_mock, "/api/dostk/etf")
        result = api.etf.return_rate()
        assert result["return_code"] == 0
