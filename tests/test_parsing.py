"""Tests for response parsing helpers."""

from __future__ import annotations

import pytest

from kiwoom_rest_api.parsing import extract_records, normalize, to_dataframe, to_number


class TestToNumber:
    @pytest.mark.parametrize(
        "raw,expected",
        [
            ("+70000", 70000),
            ("-1500", -1500),
            ("70000", 70000),
            ("+1.23", 1.23),
            ("-1.23", -1.23),
            ("1,234,567", 1234567),
            ("-1,234", -1234),
            ("  +500  ", 500),
        ],
    )
    def test_parses_signed_numbers(self, raw, expected):
        assert to_number(raw) == expected

    @pytest.mark.parametrize("raw", ["", "   ", None])
    def test_blank_becomes_none(self, raw):
        assert to_number(raw) is None

    @pytest.mark.parametrize(
        "raw",
        [
            "005930",  # 종목코드 — 앞자리 0 이 의미를 가진다
            "0B",
            "삼성전자",
            "N",
            "+",
            "-",
            "1.2.3",
        ],
    )
    def test_leaves_non_numeric_and_coded_strings_alone(self, raw):
        assert to_number(raw) == raw

    def test_zero_itself_is_numeric(self):
        assert to_number("0") == 0
        assert to_number("0.5") == 0.5
        assert to_number("-0.5") == -0.5

    def test_non_strings_pass_through(self):
        assert to_number(42) == 42
        assert to_number(1.5) == 1.5
        assert to_number(True) is True

    def test_int_vs_float_types(self):
        assert isinstance(to_number("+70000"), int)
        assert isinstance(to_number("+1.0"), float)


class TestExtractRecords:
    def test_finds_the_list_payload(self):
        resp = {
            "return_code": 0,
            "return_msg": "OK",
            "stk_infr": [{"a": 1}, {"a": 2}],
        }
        key, records = extract_records(resp)
        assert key == "stk_infr"
        assert len(records) == 2

    def test_prefers_the_longest_list_of_dicts(self):
        resp = {
            "return_code": 0,
            "short": [{"a": 1}],
            "long": [{"a": 1}, {"a": 2}, {"a": 3}],
        }
        key, _ = extract_records(resp)
        assert key == "long"

    def test_explicit_key_wins(self):
        resp = {"short": [{"a": 1}], "long": [{"a": 1}, {"a": 2}]}
        key, records = extract_records(resp, key="short")
        assert key == "short"
        assert len(records) == 1

    def test_missing_explicit_key_raises(self):
        with pytest.raises(KeyError):
            extract_records({"a": [{"x": 1}]}, key="nope")

    def test_ignores_lists_of_scalars(self):
        resp = {"codes": ["005930", "000660"], "rows": [{"a": 1}]}
        key, _ = extract_records(resp)
        assert key == "rows"

    def test_a_bare_list_is_its_own_payload(self):
        records = [{"a": 1}, {"a": 2}]
        key, out = extract_records(records)
        assert key is None
        assert out == records

    def test_request_all_output_of_dicts(self):
        """request_all() 이 페이지 dict 를 그대로 쌓아준 경우도 받는다."""
        pages = [{"return_code": 0, "a": 1}, {"return_code": 0, "a": 2}]
        key, out = extract_records(pages)
        assert key is None
        assert len(out) == 2

    def test_no_records_returns_empty(self):
        key, out = extract_records({"return_code": 0, "return_msg": "OK"})
        assert key is None
        assert out == []


class TestNormalize:
    def test_converts_nested_values(self):
        resp = {
            "return_code": 0,
            "rows": [
                {"stk_cd": "005930", "cur_prc": "+70000", "flu_rt": "-1.23"},
            ],
        }
        out = normalize(resp)
        assert out["rows"][0]["cur_prc"] == 70000
        assert out["rows"][0]["flu_rt"] == -1.23
        assert out["rows"][0]["stk_cd"] == "005930", "종목코드는 문자열 유지"

    def test_does_not_mutate_input(self):
        resp = {"rows": [{"cur_prc": "+70000"}]}
        normalize(resp)
        assert resp["rows"][0]["cur_prc"] == "+70000"

    def test_handles_scalars_and_lists(self):
        assert normalize("+100") == 100
        assert normalize(["+1", "-2"]) == [1, -2]

    def test_exclude_keys_are_left_alone(self):
        out = normalize({"qty": "+10", "raw": "+10"}, exclude={"raw"})
        assert out["qty"] == 10
        assert out["raw"] == "+10"

    def test_date_and_code_keys_stay_strings(self):
        """앞자리 0 이 없어 숫자로 보이는 날짜/코드도 키 이름으로 지켜낸다."""
        resp = {
            "base_dt": "20260815",
            "dt": "20260815",
            "stk_cd": "123456",
            "acnt_no": "12345678",
            "trde_qty": "20260815",  # 같은 값이어도 수량 컬럼이면 숫자
        }
        out = normalize(resp)
        assert out["base_dt"] == "20260815"
        assert out["dt"] == "20260815"
        assert out["stk_cd"] == "123456"
        assert out["acnt_no"] == "12345678"
        assert out["trde_qty"] == 20260815


class TestToDataFrame:
    def test_builds_dataframe_with_numeric_columns(self):
        pd = pytest.importorskip("pandas")
        resp = {
            "return_code": 0,
            "rows": [
                {"stk_cd": "005930", "cur_prc": "+70000", "flu_rt": "-1.23"},
                {"stk_cd": "000660", "cur_prc": "+180000", "flu_rt": "+2.50"},
            ],
        }
        df = to_dataframe(resp)
        assert list(df.columns) == ["stk_cd", "cur_prc", "flu_rt"]
        assert len(df) == 2
        assert df["cur_prc"].tolist() == [70000, 180000]
        assert pd.api.types.is_numeric_dtype(df["flu_rt"])
        assert df["stk_cd"].tolist() == ["005930", "000660"]

    def test_numeric_false_keeps_raw_strings(self):
        pytest.importorskip("pandas")
        resp = {"rows": [{"cur_prc": "+70000"}]}
        df = to_dataframe(resp, numeric=False)
        assert df["cur_prc"].tolist() == ["+70000"]

    def test_explicit_key(self):
        pytest.importorskip("pandas")
        resp = {"a": [{"x": "1"}], "b": [{"y": "2"}, {"y": "3"}]}
        df = to_dataframe(resp, key="a")
        assert list(df.columns) == ["x"]

    def test_empty_response_gives_empty_frame(self):
        pytest.importorskip("pandas")
        df = to_dataframe({"return_code": 0, "return_msg": "OK"})
        assert df.empty

    def test_helpful_error_without_pandas(self, monkeypatch):
        """pandas 미설치 환경을 sys.modules 로 재현 (import pandas 가 ImportError)."""
        import sys

        monkeypatch.setitem(sys.modules, "pandas", None)
        with pytest.raises(ImportError) as exc:
            to_dataframe({"rows": [{"a": 1}]})
        assert "pandas" in str(exc.value)
        assert "kiwoom-client[pandas]" in str(exc.value)
