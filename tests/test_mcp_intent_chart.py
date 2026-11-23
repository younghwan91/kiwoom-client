"""get_chart: OHLCV rows (oldest first) + summary, following continuation pages."""

from __future__ import annotations

import json

import pytest

from kiwoom_client import ohlcv_rows
from kiwoom_client.mcp.intents.chart import summarize
from kiwoom_client.mcp.server import build_server

from .intent_support import BASE, call, mock_api, mock_listing

CHART = f"{BASE}/api/dostk/chart"
KEY = "stk_dt_pole_chart_qry"


@pytest.fixture
async def api(httpx_mock):
    async with mock_api(httpx_mock) as client:
        yield client


def _daily(day: int, close: int, volume: int = 1000) -> dict:
    return {
        "dt": f"202611{day:02d}",
        "open_pric": str(close - 100),
        "high_pric": f"+{close + 200}",
        "low_pric": f"-{close - 300}",
        "cur_prc": f"{close}",
        "trde_qty": str(volume),
        "pred_pre": "+100",
    }


MINUTE_BAR = {
    "cntr_tm": "20261124090500", "open_pric": "+100", "high_pric": "+110",
    "low_pric": "-95", "cur_prc": "-105", "trde_qty": "10",
}  # fmt: skip


class TestOhlcvRows:
    def test_daily_rows_oldest_first_without_signs(self):
        rows = ohlcv_rows({"stk_dt_pole_chart_qry": [_daily(24, 70000), _daily(21, 69000)]})
        assert [r["date"] for r in rows] == ["2026-11-21", "2026-11-24"]
        assert rows[1] == {
            "date": "2026-11-24", "open": 69900, "high": 70200, "low": 69700,
            "close": 70000, "volume": 1000,
        }  # fmt: skip

    def test_minute_rows_use_datetime(self):
        rows = ohlcv_rows([
            {"cntr_tm": "20261124090100", "open_pric": "-100", "high_pric": "101",
             "low_pric": "99", "cur_prc": "-100", "trde_qty": "5"},
        ])  # fmt: skip
        assert rows[0]["datetime"] == "2026-11-24T09:01:00"
        assert rows[0]["close"] == 100

    def test_matches_to_ohlcv(self):
        pytest.importorskip("pandas")
        from kiwoom_client import to_ohlcv

        resp = {"stk_dt_pole_chart_qry": [_daily(24, 70000), _daily(21, 69000)]}
        frame = to_ohlcv(resp)
        rows = ohlcv_rows(resp)
        assert frame["close"].tolist() == [r["close"] for r in rows]
        assert frame["volume"].tolist() == [r["volume"] for r in rows]

    def test_not_a_chart(self):
        with pytest.raises(KeyError):
            ohlcv_rows({"list": [{"foo": "1"}]})
        assert ohlcv_rows({"stk_dt_pole_chart_qry": []}) == []


class TestSummary:
    def test_values(self):
        rows = [
            {"date": f"d{i}", "open": c, "high": c + 10, "low": c - 10, "close": c, "volume": 100}
            for i, c in enumerate(range(100, 125))
        ]
        s = summarize(rows)
        assert s["rows"] == 25
        assert s["last_close"] == 124
        assert s["period_return_pct"] == 24.0
        assert (s["high"], s["low"]) == (134, 90)
        assert s["sma5"] == 122.0
        assert s["sma20"] == 114.5
        assert s["avg_volume"] == 100

    def test_short_series_has_no_sma20(self):
        s = summarize([{"date": "d", "open": 1, "high": 1, "low": 1, "close": 1, "volume": 1}])
        assert s["sma20"] is None and s["sma5"] is None
        assert summarize([]) == {"rows": 0}


class TestGetChart:
    async def test_follows_pages_until_count_and_returns_newest_rows(self, httpx_mock, api):
        httpx_mock.add_response(
            url=CHART,
            match_headers={"api-id": "ka10081", "cont-yn": "N"},
            json={"return_code": 0, KEY: [_daily(d, 70000 + d) for d in (24, 23, 22)]},
            headers={"cont-yn": "Y", "next-key": "k2"},
        )
        httpx_mock.add_response(
            url=CHART,
            match_headers={"api-id": "ka10081", "cont-yn": "Y", "next-key": "k2"},
            json={"return_code": 0, KEY: [_daily(d, 70000 + d) for d in (21, 20, 19)]},
            headers={"cont-yn": "Y", "next-key": "k3"},
        )
        app, _specs = build_server(api, allow_live_orders=False)
        is_error, out = await call(app, "get_chart", {"stock": "005930", "count": 4})
        assert is_error is False, out
        assert [r["date"] for r in out["rows"]] == [
            "2026-11-21", "2026-11-22", "2026-11-23", "2026-11-24",
        ]  # fmt: skip
        assert out["summary"]["last_close"] == 70024
        assert out["stock"]["code"] == "005930"
        assert out["source"].startswith("ka10081")
        requests = httpx_mock.get_requests(url=CHART)
        assert len(requests) == 2  # 4개를 채운 뒤 세 번째 페이지는 부르지 않는다
        body = json.loads(requests[0].content)
        assert body["stk_cd"] == "005930" and body["upd_stkpc_tp"] == "1"
        assert len(body["base_dt"]) == 8

    async def test_minute_chart_by_name(self, httpx_mock, api):
        mock_listing(httpx_mock)
        httpx_mock.add_response(
            url=CHART,
            match_headers={"api-id": "ka10080"},
            match_json={"stk_cd": "005930", "tic_scope": "5", "upd_stkpc_tp": "0"},
            json={"return_code": 0, "stk_min_pole_chart_qry": [MINUTE_BAR]},
        )
        app, _specs = build_server(api, allow_live_orders=False)
        args = {"stock": "삼성전자", "period": "minute", "interval": 5, "adjusted": False}
        is_error, out = await call(app, "get_chart", args)
        assert is_error is False, out
        assert out["interval_minutes"] == 5
        assert out["rows"][0]["close"] == 105
        assert out["stock"]["name"] == "삼성전자"

    async def test_week_and_month_use_their_trs(self, httpx_mock, api):
        trs = (("ka10082", "stk_stk_pole_chart_qry"), ("ka10083", "stk_mth_pole_chart_qry"))
        for api_id, key in trs:
            httpx_mock.add_response(
                url=CHART,
                match_headers={"api-id": api_id},
                match_json={"stk_cd": "005930", "base_dt": "20251231", "upd_stkpc_tp": "1"},
                json={"return_code": 0, key: [_daily(1, 100)]},
            )
        app, _specs = build_server(api, allow_live_orders=False)
        for period in ("week", "month"):
            args = {"stock": "005930", "period": period, "end_date": "2025-12-31"}
            is_error, out = await call(app, "get_chart", args)
            assert is_error is False, out
            assert out["summary"]["rows"] == 1

    @pytest.mark.parametrize(
        "args",
        [
            {"stock": "005930", "period": "year"},
            {"stock": "005930", "period": "minute", "interval": 7},
            {"stock": "005930", "end_date": "24/11/2026"},
            {},
        ],
    )
    async def test_bad_arguments_are_tool_errors(self, api, args):
        app, _specs = build_server(api, allow_live_orders=False)
        is_error, _text = await call(app, "get_chart", args)
        assert is_error is True
