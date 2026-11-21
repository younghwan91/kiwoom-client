"""예외가 pickle 왕복을 견디는지 — multiprocessing 이 워커의 예외를 pickle 로 넘긴다.

``KiwoomAPIError(code, message, response)`` 는 생성자 인자가 ``args`` 와 달라 기본 pickle 이
``TypeError`` 로 깨졌다. 속성·``str()``·타입이 그대로 돌아와야 한다.
"""

from __future__ import annotations

import copy
import inspect
import pickle

import pytest

from kiwoom_client import errors
from kiwoom_client.base import KiwoomAPIError, api_error_class
from kiwoom_client.errors import KiwoomAuthError, KiwoomError, KiwoomParamError
from kiwoom_client.spec.validation import ParamProblem

API_ERRORS = sorted(
    {
        obj
        for obj in vars(errors).values()
        if inspect.isclass(obj) and issubclass(obj, KiwoomAPIError)
    },
    key=lambda c: c.__name__,
)

RESPONSE = {"return_code": 3, "return_msg": "인증에 실패했습니다[8005:Token이 유효하지 않습니다]"}


def _roundtrip(exc):
    return pickle.loads(pickle.dumps(exc))


def _same(a: BaseException, b: BaseException) -> None:
    assert type(a) is type(b)
    assert str(a) == str(b)
    assert a.args == b.args
    assert a.__dict__ == b.__dict__


def test_every_api_error_class_is_covered():
    assert len(API_ERRORS) >= 7
    assert KiwoomAPIError in API_ERRORS


@pytest.mark.parametrize("cls", API_ERRORS, ids=lambda c: c.__name__)
def test_api_errors_roundtrip(cls):
    exc = cls(3, RESPONSE["return_msg"], RESPONSE)
    back = _roundtrip(exc)
    _same(exc, back)
    assert (back.code, back.message, back.response) == (3, RESPONSE["return_msg"], RESPONSE)
    assert back.error_code == 8005
    assert back.hint is None


@pytest.mark.parametrize("cls", API_ERRORS, ids=lambda c: c.__name__)
def test_api_errors_roundtrip_with_hint(cls):
    exc = cls(3, RESPONSE["return_msg"], RESPONSE)._with_hint("is_mock=True 로 바꾸세요")
    back = _roundtrip(exc)
    _same(exc, back)
    assert back.hint == "is_mock=True 로 바꾸세요"
    assert str(back).count("힌트") == 1


def test_api_error_without_response_roundtrips():
    _same(KiwoomAPIError(1, "x"), _roundtrip(KiwoomAPIError(1, "x")))


def test_classified_error_from_server_roundtrips():
    cls = api_error_class(5, "[1700:허용된 요청 개수를 초과하였습니다]")
    exc = cls(5, "[1700:허용된 요청 개수를 초과하였습니다]", {"return_code": 5})
    _same(exc, _roundtrip(exc))


def test_copy_also_works():
    exc = KiwoomAPIError(3, RESPONSE["return_msg"], RESPONSE)._with_hint("h")
    _same(exc, copy.copy(exc))
    _same(exc, copy.deepcopy(exc))


@pytest.mark.parametrize(
    "exc",
    [
        KiwoomError("x"),
        KiwoomAuthError("토큰 발급 실패: [8030:모의투자 키]", hint="is_mock=True"),
        KiwoomAuthError("plain"),
        errors.KiwoomWebSocketError("login failed"),
        KiwoomParamError(
            "ka10081",
            [ParamProblem("missing", "upd_stkpc_tp", "수정주가구분"), ParamProblem("unknown", "x")],
        ),
    ],
    ids=lambda e: type(e).__name__,
)
def test_other_errors_roundtrip(exc):
    back = _roundtrip(exc)
    _same(exc, back)


def test_param_error_keeps_fields():
    problems = [ParamProblem("missing", "upd_stkpc_tp")]
    back = _roundtrip(KiwoomParamError("ka10081", problems))
    assert back.api_id == "ka10081"
    assert back.problems == problems
    assert isinstance(back, ValueError)
