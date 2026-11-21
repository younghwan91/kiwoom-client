"""요청 바디를 TR 카탈로그와 대조한다 — 모르는 필드, 빠진 필수 필드.

기본은 꺼져 있다. ``KiwoomAPI(..., validate_params="warn")`` 이면 경고만,
``validate_params="error"``(또는 ``True``)면 요청을 보내기 전에 :class:`KiwoomParamError` 를 낸다.
값의 타입·코드값은 보지 않는다 — 카탈로그 코드값은 휴리스틱이라 유효한 값을 막을 수 있다.
"""

from __future__ import annotations

import difflib
import warnings
from collections.abc import Mapping
from dataclasses import dataclass
from typing import Any, Generic, Literal

from kiwoom_client._errors import KiwoomError
from kiwoom_client.base import ClientProtocol, ResponseT

ValidateMode = Literal["warn", "error"]

__all__ = [
    "KiwoomParamError",
    "KiwoomParamWarning",
    "ParamProblem",
    "ValidatingClient",
    "check_params",
    "resolve_mode",
]


class KiwoomParamError(KiwoomError, ValueError):
    """``validate_params="error"`` 에서 요청 바디가 카탈로그와 다를 때. 요청은 나가지 않았다."""

    def __init__(self, api_id: str, problems: list[ParamProblem]) -> None:
        self.api_id = api_id
        self.problems = problems
        lines = "\n".join(f"  - {p}" for p in problems)
        super().__init__(f"{api_id} 요청 필드 문제 {len(problems)}개:\n{lines}")


class KiwoomParamWarning(UserWarning):
    """``validate_params="warn"`` 에서 요청 바디가 카탈로그와 맞지 않을 때."""


@dataclass(frozen=True)
class ParamProblem:
    """요청 바디 문제 하나."""

    kind: Literal["unknown", "missing"]
    field: str
    hint: str = ""

    def __str__(self) -> str:
        if self.kind == "missing":
            text = f"필수 필드 {self.field!r} 가 없다"
        else:
            text = f"카탈로그에 없는 필드 {self.field!r}"
        return f"{text} ({self.hint})" if self.hint else text


def check_params(api_id: str, body: Mapping[str, Any] | None) -> list[ParamProblem]:
    """``body`` 를 ``api_id`` 의 카탈로그 요청 필드와 대조한 문제 목록 (없으면 빈 목록).

    카탈로그에 없는 api_id 는 검사하지 않는다. 출처가 ``repo``(필드 목록이 불완전할 수 있다)인
    TR 은 빠진 필수 필드만 본다.
    """
    from kiwoom_client import spec

    try:
        tr = spec.get(api_id)
    except KeyError:
        return []
    body = body or {}
    known = {f.id: f for f in tr.request_fields}
    problems: list[ParamProblem] = []
    if tr.source == "official":
        for key in body:
            if key in known:
                continue
            close = difflib.get_close_matches(key, list(known), n=1, cutoff=0.6)
            hint = f"혹시 {close[0]!r}?" if close else ""
            problems.append(ParamProblem("unknown", key, hint))
    for field_id in tr.required_fields:
        if field_id not in body:
            problems.append(ParamProblem("missing", field_id, known[field_id].name))
    return problems


def resolve_mode(validate_params: bool | str) -> ValidateMode | None:
    """생성자 인자 → 검증 모드. ``False`` 면 ``None`` (검증 안 함)."""
    if validate_params is False or validate_params is None:
        return None
    if validate_params is True or validate_params == "error":
        return "error"
    if validate_params == "warn":
        return "warn"
    raise ValueError(f"validate_params 는 False·True·'warn'·'error' 중 하나: {validate_params!r}")


class ValidatingClient(Generic[ResponseT]):
    """엔드포인트 모듈과 실제 클라이언트 사이에서 ``request()`` 바디만 검사하고 그대로 넘긴다.

    응답·재시도·토큰 처리는 감싼 클라이언트가 전부 한다. 검사를 통과하거나 경고만 낸 요청은
    검증이 없을 때와 똑같이 나간다.
    """

    def __init__(self, inner: ClientProtocol[ResponseT], mode: ValidateMode) -> None:
        self._inner = inner
        self._mode = mode

    def request(
        self,
        resource_url: str,
        api_id: str,
        body: dict[str, Any] | None = None,
        cont_yn: str = "N",
        next_key: str = "",
        extra_headers: dict[str, str] | None = None,
    ) -> ResponseT:
        problems = check_params(api_id, body)
        if problems:
            if self._mode == "error":
                raise KiwoomParamError(api_id, problems)
            joined = "; ".join(str(p) for p in problems)
            warnings.warn(f"{api_id}: {joined}", KiwoomParamWarning, stacklevel=3)
        return self._inner.request(resource_url, api_id, body, cont_yn, next_key, extra_headers)

    def __getattr__(self, name: str) -> Any:
        return getattr(self._inner, name)
