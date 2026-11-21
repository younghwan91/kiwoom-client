"""Tests for the read-only ``kiwoom`` CLI. All HTTP is mocked."""

from __future__ import annotations

import json
import subprocess
import sys

import pytest

from kiwoom_client import cli

MOCK = "https://mockapi.kiwoom.com"
LIVE = "https://api.kiwoom.com"


@pytest.fixture(autouse=True)
def _creds(monkeypatch):
    monkeypatch.setenv("KIWOOM_APP_KEY", "k")
    monkeypatch.setenv("KIWOOM_APP_SECRET", "s")
    monkeypatch.setenv("KIWOOM_IS_MOCK", "true")


def _token(httpx_mock, base=MOCK):
    httpx_mock.add_response(url=f"{base}/oauth2/token", json={"token": "t", "expires_in": 3600})


def _api_ids(httpx_mock):
    return [r.headers.get("api-id") for r in httpx_mock.get_requests() if r.headers.get("api-id")]


BASIC = {
    "return_code": 0, "stk_cd": "005930", "stk_nm": "삼성전자", "cur_prc": "-70500",
    "flu_rt": "-1.23", "trde_qty": "12345678", "open_pric": "+71000", "high_pric": "+71500",
    "low_pric": "-70100",
}


class TestQuote:
    def test_by_code(self, httpx_mock, capsys):
        _token(httpx_mock)
        httpx_mock.add_response(url=f"{MOCK}/api/dostk/stkinfo", json=BASIC)
        assert cli.main(["quote", "005930"]) == 0
        out = capsys.readouterr().out
        assert "삼성전자 (005930)" in out
        assert "70,500" in out and "-1.23%" in out and "12,345,678" in out
        body = json.loads(httpx_mock.get_requests()[-1].content)
        assert body == {"stk_cd": "005930"}

    def test_by_name_resolves_with_ka10099(self, httpx_mock, capsys):
        _token(httpx_mock)
        listing = {"return_code": 0, "list": [{"code": "005930", "name": "삼성전자"}]}

        def respond(request):
            import httpx

            api_id = request.headers["api-id"]
            return httpx.Response(200, json=listing if api_id == "ka10099" else BASIC)

        httpx_mock.add_callback(respond, url=f"{MOCK}/api/dostk/stkinfo", is_reusable=True)
        assert cli.main(["quote", "삼성전자"]) == 0
        assert _api_ids(httpx_mock) == ["ka10099", "ka10099", "ka10001"]

    def test_json(self, httpx_mock, capsys):
        _token(httpx_mock)
        httpx_mock.add_response(url=f"{MOCK}/api/dostk/stkinfo", json=BASIC)
        assert cli.main(["quote", "005930", "--json"]) == 0
        assert json.loads(capsys.readouterr().out)["stk_nm"] == "삼성전자"

    def test_global_options_before_subcommand(self, httpx_mock, capsys, monkeypatch):
        monkeypatch.delenv("KIWOOM_IS_MOCK")
        _token(httpx_mock)
        httpx_mock.add_response(url=f"{MOCK}/api/dostk/stkinfo", json=BASIC)
        assert cli.main(["--mock", "--json", "quote", "005930"]) == 0
        assert json.loads(capsys.readouterr().out)["stk_cd"] == "005930"

    def test_live_flag(self, httpx_mock, capsys):
        _token(httpx_mock, LIVE)
        httpx_mock.add_response(url=f"{LIVE}/api/dostk/stkinfo", json=BASIC)
        assert cli.main(["quote", "005930", "--live"]) == 0


CHART_DAILY = {"return_code": 0, "stk_cd": "005930", "stk_dt_pole_chart_qry": [
    {"dt": "20260327", "open_pric": "70000", "high_pric": "71000", "low_pric": "69900",
     "cur_prc": "70500", "trde_qty": "1200"},
    {"dt": "20260326", "open_pric": "69000", "high_pric": "70100", "low_pric": "68900",
     "cur_prc": "70000", "trde_qty": "1000"},
]}


class TestChart:

    def test_daily_default(self, httpx_mock, capsys):
        _token(httpx_mock)
        httpx_mock.add_response(url=f"{MOCK}/api/dostk/chart", json=CHART_DAILY)
        assert cli.main(["chart", "005930", "--date", "20260327", "-n", "5"]) == 0
        out = capsys.readouterr().out.splitlines()
        assert out[0] == "005930 daily"
        assert "20260326" in out[2] and "20260327" in out[3]  # oldest first
        request = httpx_mock.get_requests()[-1]
        assert request.headers["api-id"] == "ka10081"
        assert json.loads(request.content) == {
            "stk_cd": "005930", "upd_stkpc_tp": "1", "base_dt": "20260327",
        }

    @pytest.mark.parametrize(
        ("flag", "api_id"),
        [("--weekly", "ka10082"), ("--monthly", "ka10083"), ("--yearly", "ka10094")],
    )
    def test_period_flags(self, httpx_mock, capsys, flag, api_id):
        _token(httpx_mock)
        httpx_mock.add_response(url=f"{MOCK}/api/dostk/chart", json={"return_code": 0})
        assert cli.main(["chart", "005930", flag]) == 0
        assert _api_ids(httpx_mock) == [api_id]

    def test_minute(self, httpx_mock, capsys):
        _token(httpx_mock)
        httpx_mock.add_response(url=f"{MOCK}/api/dostk/chart", json={
            "return_code": 0, "stk_min_pole_chart_qry": [
                {"cntr_tm": "20260327090100", "open_pric": "-70100", "high_pric": "+70250",
                 "low_pric": "-70050", "cur_prc": "+70200", "trde_qty": "50"}]})
        assert cli.main(["chart", "005930", "--minute", "--scope", "5", "--raw-price"]) == 0
        out = capsys.readouterr().out
        assert "20260327090100" in out and "-70" not in out
        request = httpx_mock.get_requests()[-1]
        assert request.headers["api-id"] == "ka10080"
        assert json.loads(request.content) == {
            "stk_cd": "005930", "upd_stkpc_tp": "0", "tic_scope": "5",
        }

    def test_tick(self, httpx_mock, capsys):
        _token(httpx_mock)
        httpx_mock.add_response(url=f"{MOCK}/api/dostk/chart", json={"return_code": 0})
        assert cli.main(["chart", "005930", "--tick"]) == 0
        assert _api_ids(httpx_mock) == ["ka10079"]


class TestBalance:
    def test_balance(self, httpx_mock, capsys):
        _token(httpx_mock)
        httpx_mock.add_response(url=f"{MOCK}/api/dostk/acnt", json={
            "return_code": 0, "tot_pur_amt": "000000001000000", "tot_evlt_amt": "000000001050000",
            "tot_evlt_pl": "000000000050000", "tot_prft_rt": "5.00",
            "prsm_dpst_aset_amt": "000000002000000",
            "acnt_evlt_remn_indv_tot": [
                {"stk_cd": "A005930", "stk_nm": "삼성전자", "rmnd_qty": "000000000000010",
                 "pur_pric": "000000000070000", "cur_prc": "000000065000",
                 "evltv_prft": "-00000000050000", "prft_rt": "-7.14"},
            ],
        })
        assert cli.main(["balance"]) == 0
        out = capsys.readouterr().out
        assert "1,050,000" in out and "+50,000" in out and "+5.00%" in out
        assert "005930" in out and "A005930" not in out
        assert "-50,000" in out and "-7.14" in out
        request = httpx_mock.get_requests()[-1]
        assert request.headers["api-id"] == "kt00018"
        assert json.loads(request.content) == {"qry_tp": "1", "dmst_stex_tp": "KRX"}

    def test_empty_balance(self, httpx_mock, capsys):
        _token(httpx_mock)
        httpx_mock.add_response(url=f"{MOCK}/api/dostk/acnt", json={"return_code": 0})
        assert cli.main(["balance"]) == 0
        assert "보유 종목 없음" in capsys.readouterr().out


class TestFindAndEndpoints:
    def test_find(self, httpx_mock, capsys):
        _token(httpx_mock)
        httpx_mock.add_response(
            url=f"{MOCK}/api/dostk/stkinfo",
            json={"return_code": 0, "list": [
                {"code": "000660", "name": "SK하이닉스", "marketName": "거래소"}]},
            is_reusable=True,
        )
        assert cli.main(["find", "하이닉스"]) == 0
        assert "000660" in capsys.readouterr().out

    def test_endpoints_needs_no_credentials(self, monkeypatch, capsys):
        monkeypatch.delenv("KIWOOM_APP_KEY")
        assert cli.main(["endpoints", "ka10081"]) == 0
        out = capsys.readouterr().out
        assert "api.chart.stock_daily_chart" in out

    def test_endpoints_json(self, capsys):
        assert cli.main(["endpoints", "--json"]) == 0
        rows = json.loads(capsys.readouterr().out)
        assert len(rows) > 150
        assert {"api_id", "method", "name"} <= set(rows[0])

    def test_endpoints_no_match(self, capsys):
        assert cli.main(["endpoints", "zzz-nothing"]) == 0
        assert "없습니다" in capsys.readouterr().out


class TestSafety:
    def test_no_order_or_logout_subcommand(self):
        parser = cli.build_parser()
        sub = next(a for a in parser._actions if a.dest == "command")
        assert set(sub.choices) == {"quote", "chart", "balance", "find", "endpoints"}

    def test_missing_credentials_is_a_clean_error(self, monkeypatch, capsys):
        monkeypatch.delenv("KIWOOM_APP_KEY")
        assert cli.main(["quote", "005930"]) == 1
        assert "KIWOOM_APP_KEY" in capsys.readouterr().err

    def test_api_error_is_a_clean_error(self, httpx_mock, capsys):
        _token(httpx_mock)
        httpx_mock.add_response(
            url=f"{MOCK}/api/dostk/stkinfo",
            json={"return_code": 1, "return_msg": "[1902:종목 정보가 없습니다]"},
        )
        assert cli.main(["quote", "999999"]) == 1
        assert "1902" in capsys.readouterr().err

    def test_mock_and_live_are_exclusive(self):
        with pytest.raises(SystemExit):
            cli.main(["quote", "005930", "--mock", "--live"])


def test_python_dash_m_help():
    result = subprocess.run(
        [sys.executable, "-m", "kiwoom_client", "--help"], capture_output=True, text=True,
        check=False,
    )
    assert result.returncode == 0
    assert "quote" in result.stdout and "endpoints" in result.stdout
