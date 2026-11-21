"""opt-in 요청 검증 (validate_params). 기본값은 예전 그대로 검사 없이 보낸다."""

from __future__ import annotations

import warnings

import pytest

from kiwoom_client import AsyncKiwoomAPI, KiwoomAPI
from kiwoom_client.errors import KiwoomError, KiwoomParamError, KiwoomParamWarning
from kiwoom_client.spec.validation import ParamProblem, check_params, resolve_mode

TOKEN_URL = "https://mockapi.kiwoom.com/oauth2/token"
STKINFO_URL = "https://mockapi.kiwoom.com/api/dostk/stkinfo"
TOKEN = {"token": "t", "token_type": "Bearer", "expires_in": 86400}
OK = {"return_code": 0, "return_msg": "OK"}


def test_check_params_ok():
    assert check_params("ka10001", {"stk_cd": "005930"}) == []


def test_check_params_unknown_with_hint_and_missing():
    problems = check_params("ka10001", {"stk_code": "005930"})
    assert problems == [
        ParamProblem("unknown", "stk_code", "혹시 'stk_cd'?"),
        ParamProblem("missing", "stk_cd", "종목코드"),
    ]
    assert "필수 필드 'stk_cd'" in str(problems[1])


def test_check_params_ignores_unknown_api_id_and_repo_unknowns():
    assert check_params("zz99999", {"x": "1"}) == []
    # ka10009 는 source=repo — 필드 목록이 불완전할 수 있어 모르는 필드는 보지 않는다.
    assert check_params("ka10009", {"stk_cd": "005930", "extra": "1"}) == []
    assert [p.kind for p in check_params("ka10009", {})] == ["missing"]


@pytest.mark.parametrize(
    ("value", "mode"),
    [(False, None), (None, None), (True, "error"), ("error", "error"), ("warn", "warn")],
)
def test_resolve_mode(value, mode):
    assert resolve_mode(value) == mode


def test_resolve_mode_rejects_typos():
    with pytest.raises(ValueError, match="validate_params"):
        resolve_mode("strict")


def test_default_sends_anything_as_before(httpx_mock):
    httpx_mock.add_response(url=TOKEN_URL, json=TOKEN)
    httpx_mock.add_response(url=STKINFO_URL, match_json={"stk_code": "005930"}, json=OK)
    with KiwoomAPI("k", "s", is_mock=True, rate_limit=None) as api:
        with warnings.catch_warnings():
            warnings.simplefilter("error")
            assert api.stock_info.basic_stock_info(stk_code="005930")["return_code"] == 0


def test_error_mode_raises_before_sending(httpx_mock):
    with KiwoomAPI("k", "s", is_mock=True, validate_params="error") as api:
        with pytest.raises(KiwoomParamError) as exc_info:
            api.stock_info.basic_stock_info(stk_code="005930")
    err = exc_info.value
    assert err.api_id == "ka10001"
    assert isinstance(err, KiwoomError) and isinstance(err, ValueError)
    assert "혹시 'stk_cd'?" in str(err)
    assert httpx_mock.get_requests() == []  # 토큰 발급도, 본 요청도 나가지 않았다


def test_warn_mode_warns_and_still_sends(httpx_mock):
    httpx_mock.add_response(url=TOKEN_URL, json=TOKEN)
    httpx_mock.add_response(url=STKINFO_URL, json=OK)
    with KiwoomAPI("k", "s", is_mock=True, rate_limit=None, validate_params="warn") as api:
        with pytest.warns(KiwoomParamWarning, match="ka10001"):
            assert api.stock_info.basic_stock_info(stk_code="005930")["return_code"] == 0


def test_valid_request_passes_validation(httpx_mock):
    httpx_mock.add_response(url=TOKEN_URL, json=TOKEN)
    httpx_mock.add_response(url=STKINFO_URL, match_json={"stk_cd": "005930"}, json=OK)
    with KiwoomAPI("k", "s", is_mock=True, rate_limit=None, validate_params=True) as api:
        assert api.stock_info.basic_stock_info(stk_cd="005930")["return_code"] == 0


async def test_async_error_mode(httpx_mock):
    async with AsyncKiwoomAPI("k", "s", is_mock=True, validate_params="error") as api:
        with pytest.raises(KiwoomParamError):
            await api.stock_info.basic_stock_info()
    assert httpx_mock.get_requests() == []


async def test_async_valid_request(httpx_mock):
    httpx_mock.add_response(url=TOKEN_URL, json=TOKEN)
    httpx_mock.add_response(url=STKINFO_URL, json=OK)
    async with AsyncKiwoomAPI(
        "k", "s", is_mock=True, rate_limit=None, validate_params="error"
    ) as api:
        assert (await api.stock_info.basic_stock_info(stk_cd="005930"))["return_code"] == 0
