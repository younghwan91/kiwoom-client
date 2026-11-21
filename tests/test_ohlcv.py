"""Tests for to_ohlcv(): chart responses -> time-indexed OHLCV DataFrame."""

from __future__ import annotations

import sys

import pytest

import kiwoom_client
from kiwoom_client.parsing import to_dataframe, to_ohlcv

pd = pytest.importorskip("pandas")

# Shapes follow the official spec for ka10081 (daily) and ka10080 (minute):
# newest first, minute prices carry a direction sign.
DAILY = {
    "stk_cd": "005930",
    "stk_dt_pole_chart_qry": [
        {"cur_prc": "70500", "trde_qty": "1200", "trde_prica": "84", "dt": "20260327",
         "open_pric": "70000", "high_pric": "71000", "low_pric": "69900",
         "pred_pre": "+500", "pred_pre_sig": "2", "trde_tern_rt": "+0.02"},
        {"cur_prc": "70000", "trde_qty": "1,000", "trde_prica": "70", "dt": "20260326",
         "open_pric": "69000", "high_pric": "70100", "low_pric": "68900",
         "pred_pre": "-100", "pred_pre_sig": "5", "trde_tern_rt": "+0.01"},
    ],
    "return_code": 0,
    "return_msg": "정상적으로 처리되었습니다",
}
MINUTE = {
    "stk_cd": "005930",
    "stk_min_pole_chart_qry": [
        {"cur_prc": "-70100", "trde_qty": "30", "cntr_tm": "20260327090200",
         "open_pric": "-70200", "high_pric": "+70300", "low_pric": "-70000"},
        {"cur_prc": "+70200", "trde_qty": "50", "cntr_tm": "20260327090100",
         "open_pric": "+70100", "high_pric": "+70250", "low_pric": "+70050"},
    ],
}


class TestToOhlcv:
    def test_daily(self):
        df = to_ohlcv(DAILY)
        assert list(df.columns) == ["open", "high", "low", "close", "volume"]
        assert isinstance(df.index, pd.DatetimeIndex)
        assert df.index.name == "date"
        assert list(df.index) == [pd.Timestamp("2026-03-26"), pd.Timestamp("2026-03-27")]
        assert df.iloc[0].tolist() == [69000, 70100, 68900, 70000, 1000]
        assert df.iloc[-1]["close"] == 70500

    def test_minute_drops_direction_sign(self):
        df = to_ohlcv(MINUTE)
        assert df.index.name == "datetime"
        assert df.index[0] == pd.Timestamp("2026-03-27 09:01:00")
        last = df.iloc[-1]
        assert (last["open"], last["high"], last["low"], last["close"]) == (
            70200, 70300, 70000, 70100,
        )
        assert (df[["open", "high", "low", "close"]] > 0).all().all()

    def test_keep_extra_fields(self):
        df = to_ohlcv(DAILY, keep=["trde_prica", "pred_pre"])
        assert list(df.columns)[-2:] == ["trde_prica", "pred_pre"]
        assert df["pred_pre"].tolist() == [-100, 500]  # signed as Kiwoom means it

    def test_request_all_list(self):
        pages = DAILY["stk_dt_pole_chart_qry"] + [
            {"cur_prc": "69000", "trde_qty": "900", "dt": "20260325",
             "open_pric": "68000", "high_pric": "69500", "low_pric": "67900"},
        ]
        df = to_ohlcv(pages)
        assert df.index.is_monotonic_increasing
        assert len(df) == 3

    def test_gold_spot_close_and_volume_aliases(self):
        resp = {"gds_min_chart_qry": [
            {"cntr_pric": "+150000", "acc_trde_qty": "12", "open_pric": "149900",
             "high_pric": "150100", "low_pric": "149800", "cntr_tm": "20260327100000",
             "dt": "20260327100000"},
        ]}
        df = to_ohlcv(resp)
        assert df.iloc[0]["close"] == 150000
        assert df.iloc[0]["volume"] == 12

    def test_zero_padded_values_are_numbers(self):
        resp = {"x": [{"dt": "20260327", "open_pric": "000070000", "high_pric": "000071000",
                       "low_pric": "000069000", "cur_prc": "000070500", "trde_qty": "0000100"}]}
        assert to_ohlcv(resp).iloc[0].tolist() == [70000, 71000, 69000, 70500, 100]

    def test_blank_values_become_nan(self):
        resp = {"x": [{"dt": "20260327", "open_pric": "", "high_pric": "1",
                       "low_pric": "1", "cur_prc": "1", "trde_qty": "1"}]}
        assert pd.isna(to_ohlcv(resp).iloc[0]["open"])

    def test_empty(self):
        df = to_ohlcv({"stk_cd": "005930", "stk_dt_pole_chart_qry": []})
        assert df.empty
        assert list(df.columns) == ["open", "high", "low", "close", "volume"]
        assert isinstance(df.index, pd.DatetimeIndex)

    def test_not_a_chart(self):
        with pytest.raises(KeyError, match="차트 응답이 아닙니다"):
            to_ohlcv({"list": [{"code": "005930", "name": "삼성전자"}]})
        with pytest.raises(KeyError, match="close"):
            to_ohlcv({"x": [{"dt": "20260327", "open_pric": "1", "high_pric": "1",
                             "low_pric": "1", "trde_qty": "1"}]})

    def test_bad_time_format(self):
        with pytest.raises(ValueError):
            to_ohlcv({"x": [{"dt": "2026-03-27", "open_pric": "1", "high_pric": "1",
                             "low_pric": "1", "cur_prc": "1", "trde_qty": "1"}]})

    def test_does_not_mutate_input_and_to_dataframe_unchanged(self):
        before = repr(DAILY)
        to_ohlcv(DAILY)
        assert repr(DAILY) == before
        raw = to_dataframe(DAILY)
        assert "cur_prc" in raw.columns and "dt" in raw.columns
        assert raw["dt"].tolist() == ["20260327", "20260326"]

    def test_explicit_key(self):
        assert len(to_ohlcv(DAILY, key="stk_dt_pole_chart_qry")) == 2

    def test_helpful_error_without_pandas(self, monkeypatch):
        monkeypatch.setitem(sys.modules, "pandas", None)
        with pytest.raises(ImportError, match="kiwoom-client\\[pandas\\]"):
            to_ohlcv(DAILY)


def test_top_level_export():
    assert kiwoom_client.to_ohlcv is to_ohlcv
