"""MCP REST 도구의 입력 스키마 — TR 카탈로그(:mod:`kiwoom_client.spec`)에서 만든다.

형태는 기존과 같이 ``{"cont_yn", "next_key", "params": {...}}`` 다. 바뀐 것은 ``params`` 안에
카탈로그의 요청 필드가 ``properties``/``required`` 로 들어간다는 점뿐이라, 이미
``params={...}`` 로 부르던 클라이언트는 그대로 동작한다. ``additionalProperties`` 는 열어 둔다
(카탈로그에 없는 필드도 지금처럼 키움에 넘긴다).

코드값은 ``enum`` 으로 강제하지 않고 설명에 적는다. 코드값은 필드 설명에서 휴리스틱으로
뽑은 것이고(발행사 코드처럼 예시만 적힌 목록도 있다), 강제하면 유효한 값을 클라이언트가
막을 수 있다.
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
    """필드 하나의 사람이 읽을 설명: ``한글명 (필수). 설명``."""
    head = field.name or field.id
    if field.required:
        head += " (필수)"
    desc = " ".join(field.desc.split())
    return f"{head}. {desc}" if desc else head


def _field_schema(field: spec.Field) -> dict[str, Any]:
    # 코드값은 설명에 이미 있다 — examples 로 한 번 더 싣지 않는다.
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
