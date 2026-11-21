"""Tests for stock name <-> code lookup (ka10099 종목정보 리스트)."""

from __future__ import annotations

import json

import pytest

from kiwoom_client import AsyncKiwoomAPI, KiwoomAPI
from kiwoom_client.codes import StockListMarket
from kiwoom_client.stocks import StockCache, pick_stock_code, search_stocks

URL = "https://mockapi.kiwoom.com/api/dostk/stkinfo"
TOKEN_URL = "https://mockapi.kiwoom.com/oauth2/token"

KOSPI = [
    {"code": "005930", "name": "삼성전자", "marketCode": "0", "marketName": "거래소"},
    {"code": "005935", "name": "삼성전자우", "marketCode": "0", "marketName": "거래소"},
    {"code": "000660", "name": "SK하이닉스", "marketCode": "0", "marketName": "거래소"},
    {"code": "028260", "name": "삼성물산", "marketCode": "0", "marketName": "거래소"},
    {"code": "006400", "name": "삼성SDI", "marketCode": "0", "marketName": "거래소"},
]
KOSDAQ = [
    {"code": "247540", "name": "에코프로비엠", "marketCode": "10", "marketName": "코스닥"},
    {"code": "091990", "name": "셀트리온헬스케어", "marketCode": "10", "marketName": "코스닥"},
]
ALL = KOSPI + KOSDAQ


class TestSearchStocks:
    def test_exact_name_first(self):
        hits = search_stocks(ALL, "삼성전자")
        assert [h["code"] for h in hits] == ["005930", "005935"]

    def test_prefix_then_substring_shorter_first(self):
        hits = search_stocks(ALL, "삼성")
        assert [h["name"] for h in hits] == ["삼성전자", "삼성물산", "삼성전자우", "삼성SDI"]

    def test_substring(self):
        assert [h["code"] for h in search_stocks(ALL, "하이닉스")] == ["000660"]

    def test_case_and_space_insensitive(self):
        assert search_stocks(ALL, "sk 하이닉스")[0]["code"] == "000660"

    def test_code_exact_and_prefix(self):
        assert search_stocks(ALL, "005930")[0]["name"] == "삼성전자"
        assert [h["code"] for h in search_stocks(ALL, "0059")] == ["005930", "005935"]

    def test_limit(self):
        assert len(search_stocks(ALL, "삼성", limit=2)) == 2
        assert len(search_stocks(ALL, "삼성", limit=None)) == 4

    def test_no_match_and_blank(self):
        assert search_stocks(ALL, "없는회사") == []
        assert search_stocks(ALL, "   ") == []

    def test_returns_copies(self):
        hit = search_stocks(ALL, "삼성전자")[0]
        hit["name"] = "x"
        assert KOSPI[0]["name"] == "삼성전자"


class TestPickStockCode:
    def test_exact(self):
        assert pick_stock_code(ALL, "삼성전자") == "005930"
        assert pick_stock_code(ALL, "sk하이닉스") == "000660"

    def test_code_passthrough(self):
        assert pick_stock_code(ALL, "005930") == "005930"

    def test_not_found_lists_candidates(self):
        with pytest.raises(LookupError, match="삼성전자\\(005930\\)"):
            pick_stock_code(ALL, "삼성전")

    def test_ambiguous(self):
        dup = [*ALL, {"code": "999999", "name": "삼성전자", "marketName": "코넥스"}]
        with pytest.raises(LookupError, match="여러 종목"):
            pick_stock_code(dup, "삼성전자")


class TestStockCache:
    def test_stale_refresh_and_ttl(self, monkeypatch):
        cache = StockCache()
        assert cache.stale(["0", "10"]) == ["0", "10"]
        cache.store("0", KOSPI)
        assert cache.stale([StockListMarket.KOSPI, "10"]) == ["10"]
        assert cache.stale(["0"], refresh=True) == ["0"]
        now = [1000.0]
        monkeypatch.setattr("kiwoom_client.stocks.time.monotonic", lambda: now[0])
        cache.store("0", KOSPI)
        now[0] += 59
        assert cache.stale(["0"], cache_ttl=60) == []
        now[0] += 1
        assert cache.stale(["0"], cache_ttl=60) == ["0"]

    def test_records_dedupe_by_code(self):
        cache = StockCache()
        cache.store("0", KOSPI)
        cache.store("10", [*KOSDAQ, KOSPI[0]])
        codes = [r["code"] for r in cache.records(["0", "10"])]
        assert len(codes) == len(set(codes)) == len(ALL)

    def test_clear(self):
        cache = StockCache()
        cache.store("0", KOSPI)
        cache.clear()
        assert cache.records(["0"]) == []


def _mock_listing(httpx_mock, pages_by_market):
    """Answer ka10099 per mrkt_tp; a list value means paginated pages."""
    httpx_mock.add_response(url=TOKEN_URL, json={"token": "t", "expires_in": 3600},
                            is_reusable=True, is_optional=True)

    def respond(request):
        import httpx

        body = json.loads(request.content)
        pages = pages_by_market[body["mrkt_tp"]]
        idx = 1 if request.headers.get("cont-yn") == "Y" else 0
        more = idx + 1 < len(pages)
        headers = {"cont-yn": "Y" if more else "N", "next-key": "k" if more else ""}
        return httpx.Response(
            200, json={"return_code": 0, "list": pages[idx]}, headers=headers
        )

    httpx_mock.add_callback(respond, url=URL, is_reusable=True)


def _ka10099_requests(httpx_mock):
    return [r for r in httpx_mock.get_requests() if r.headers.get("api-id") == "ka10099"]


class TestFacade:
    def test_find_and_cache(self, httpx_mock):
        _mock_listing(httpx_mock, {"0": [KOSPI[:3], KOSPI[3:]], "10": [KOSDAQ]})
        with KiwoomAPI("k", "s", is_mock=True, rate_limit=None) as api:
            assert api.find_stock("삼성전자")[0]["code"] == "005930"
            assert api.stock_code("에코프로비엠") == "247540"
            assert api.find_stock("삼성물산")[0]["code"] == "028260"  # from page 2
            # 2 pages KOSPI + 1 page KOSDAQ, then everything from cache
            assert len(_ka10099_requests(httpx_mock)) == 3
            assert len(api.stock_list()) == len(ALL)

            api.find_stock("삼성", refresh=True)
            assert len(_ka10099_requests(httpx_mock)) == 6

    def test_markets_argument(self, httpx_mock):
        _mock_listing(httpx_mock, {"10": [KOSDAQ]})
        with KiwoomAPI("k", "s", is_mock=True, rate_limit=None) as api:
            hits = api.find_stock("삼성", markets=[StockListMarket.KOSDAQ])
            assert hits == []
            sent = [json.loads(r.content) for r in _ka10099_requests(httpx_mock)]
            assert sent == [{"mrkt_tp": "10"}]

    def test_stock_code_not_found(self, httpx_mock):
        _mock_listing(httpx_mock, {"0": [KOSPI], "10": [KOSDAQ]})
        with KiwoomAPI("k", "s", is_mock=True, rate_limit=None) as api:
            with pytest.raises(LookupError):
                api.stock_code("없는회사")

    async def test_async(self, httpx_mock):
        _mock_listing(httpx_mock, {"0": [KOSPI], "10": [KOSDAQ]})
        async with AsyncKiwoomAPI("k", "s", is_mock=True, rate_limit=None) as api:
            hits = await api.find_stock("하이닉스")
            assert hits[0]["code"] == "000660"
            assert await api.stock_code("삼성전자") == "005930"
            assert len(await api.stock_list()) == len(ALL)
            assert len(_ka10099_requests(httpx_mock)) == 2
