"""MCP REST 도구의 입력 스키마 — TR 카탈로그(:mod:`kiwoom_client.spec`)에서 만든다.

형태는 기존과 같이 ``{"cont_yn", "next_key", "params": {...}}`` 다. 바뀐 것은 ``params`` 안에
카탈로그의 요청 필드가 ``properties``/``required`` 로 들어간다는 점뿐이라, 이미
``params={...}`` 로 부르던 클라이언트는 그대로 동작한다. ``additionalProperties`` 는 열어 둔다
(카탈로그에 없는 필드도 지금처럼 키움에 넘긴다).

설명은 한글 필드명과 필수 여부뿐이다 — 카탈로그는 키움 필드 설명 원문·코드값을 싣지 않는다
(``spec/SOURCE.md``). 코드값은 ``enum`` 으로 강제하지 않는다. 자주 쓰는 코드값은
``kiwoom://codes/*`` 리소스와 :mod:`kiwoom_client.codes` 에 있다.
"""

from __future__ import annotations

from typing import Any

from kiwoom_client import spec

#: 요청 필드로 쓰면 안 되는 최상위 인자 이름 (도구 인자와 겹친다).
RESERVED_ARGUMENTS = frozenset({"cont_yn", "next_key", "params"})

# 도구 182개에 반복되므로 짧게 쓴다 (tools/list 전체 크기가 그대로 에이전트 컨텍스트다).
_PAGING = {
    "cont_yn": {"type": "string", "default": "N", "description": "연속조회 여부 (다음 페이지면 Y)"},
    "next_key": {"type": "string", "default": "", "description": "연속조회 키 (이전 응답의 값)"},
}


def field_description(field: spec.Field) -> str:
    """필드 하나의 사람이 읽을 설명: ``한글명`` 또는 ``한글명 (필수)``."""
    head = field.name or field.id
    if field.required:
        head += " (필수)"
    return head


def _field_schema(field: spec.Field) -> dict[str, Any]:
    return {"type": "string", "description": field_description(field)}


def params_schema(tr: spec.TRSpec) -> dict[str, Any]:
    """TR 요청 바디(``params``)의 JSON Schema."""
    fields = [f for f in tr.request_fields if f.id not in RESERVED_ARGUMENTS]
    schema: dict[str, Any] = {
        "type": "object",
        "description": f"{tr.api_id} 요청 필드 (값은 문자열)",
        "properties": {f.id: _field_schema(f) for f in fields},
        "additionalProperties": True,
    }
    required = [f.id for f in fields if f.required]
    if required:
        schema["required"] = required
    return schema


def generic_rest_input_schema() -> dict[str, Any]:
    """카탈로그에 없는 메서드용 — 예전 스키마 그대로."""
    return {
        "type": "object",
        "properties": {
            **_PAGING,
            "params": {"type": "object", "description": "TR 요청 필드 (키움 API 가이드 참고)"},
        },
    }


def rest_input_schema(module_name: str, method_name: str) -> dict[str, Any]:
    """``api.<module_name>.<method_name>`` 도구의 입력 스키마."""
    try:
        tr = spec.for_method(module_name, method_name)
    except KeyError:
        return generic_rest_input_schema()
    params = params_schema(tr)
    schema: dict[str, Any] = {
        "type": "object",
        "properties": {**_PAGING, "params": params},
    }
    if params.get("required"):
        schema["required"] = ["params"]
    return schema


def split_arguments(arguments: dict[str, Any]) -> tuple[dict[str, Any], str, str]:
    """도구 인자 → (요청 바디, cont_yn, next_key).

    스키마는 ``params`` 로 감싸지만, 필드를 최상위에 평평하게 넣는 클라이언트도 받는다.
    둘 다 있으면 ``params`` 쪽이 이긴다.
    """
    nested = arguments.get("params") or {}
    if not isinstance(nested, dict):
        raise ValueError("params 는 객체(JSON object)여야 합니다.")
    flat = {k: v for k, v in arguments.items() if k not in RESERVED_ARGUMENTS}
    body = {**flat, **nested}
    return body, arguments.get("cont_yn", "N"), arguments.get("next_key", "")


#: 설명에 싣는 응답 필드 수 (최상위·목록마다). 도구 182개의 설명이 모두 에이전트 컨텍스트에
#: 들어가므로 핵심만 — 전체는 docs/reference 와 ``kiwoom_client.spec`` 에 있다.
_RESPONSE_PREVIEW = 6


def _preview(fields: list[spec.Field]) -> str:
    shown = ", ".join(f"{f.id}({f.name})" if f.name else f.id for f in fields[:_RESPONSE_PREVIEW])
    rest = len(fields) - _RESPONSE_PREVIEW
    return f"{shown} 외 {rest}개" if rest > 0 else shown


def response_summary(tr: spec.TRSpec) -> list[str]:
    """응답에서 무엇이 돌아오는지 — 최상위 필드와 목록(list) 필드별 핵심 항목."""
    top = [f for f in tr.response if f.parent is None and f.type != "list"]
    lists = [f for f in tr.response if f.type == "list"]
    lines = []
    if top:
        lines.append(f"응답: {_preview(top)}")
    for lst in lists:
        children = [f for f in tr.response if f.parent == lst.id]
        label = f"{lst.id}[]" + (f"({lst.name})" if lst.name else "")
        lines.append(f"응답 목록 {label}: {_preview(children)}")
    return lines


def rest_tool_description(module_name: str, method_name: str, docstring: str) -> str:
    """REST 도구 설명 — 독스트링 첫 줄 + 공식 TR 이름·api_id·URL·응답 핵심 필드 (카탈로그에서)."""
    first = docstring.strip().splitlines()[0] if docstring.strip() else method_name
    try:
        tr = spec.for_method(module_name, method_name)
    except KeyError:
        return docstring.strip()
    # 요청 필드·필수 여부는 입력 스키마에 있으니 여기엔 응답(무엇이 돌아오나)만 싣는다.
    lines = [first, f"{tr.api_id} · {tr.name} · {tr.method} {tr.url}"]
    lines += response_summary(tr)
    if any(f.type == "list" for f in tr.response):
        lines.append("연속조회: 응답 cont_yn=Y 면 cont_yn=Y·next_key 로 다음 페이지")
    if tr.source != "official":
        lines.append(f"(카탈로그 출처 {tr.source}: {tr.note})")
    return "\n".join(lines)
