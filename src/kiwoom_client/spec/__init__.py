"""TR(api_id)별 요청·응답 필드 카탈로그 — 키움 공식 명세에서 만든 사실 정보.

어떤 메서드에 어떤 필드를 넣어야 하는지를 코드에서 바로 찾는다::

    from kiwoom_client import spec

    tr = spec.get("ka10001")
    tr.name                       # '주식기본정보요청'
    tr.required_fields            # ('stk_cd',)
    [f.id for f in tr.request]    # ['stk_cd']
    spec.for_method("order", "buy_order").api_id   # 'kt10000'

데이터 출처·라이선스·다시 만드는 법은 패키지 안 ``SOURCE.md`` 에 있다. 카탈로그는 공식 문서를
대신하지 않는다 — 필드 뜻이 애매하면 https://openapi.kiwoom.com 이 기준이다.
"""

from __future__ import annotations

import json
from collections.abc import Mapping
from dataclasses import dataclass, field
from functools import lru_cache
from importlib import resources
from types import MappingProxyType
from typing import Any

__all__ = [
    "Field",
    "TRSpec",
    "api_ids",
    "catalog_source",
    "describe",
    "endpoint_index",
    "for_method",
    "get",
    "method_for",
    "resolve",
    "search",
]


@dataclass(frozen=True)
class Field:
    """요청 또는 응답 필드 하나."""

    id: str
    name: str
    type: str
    """``"string"``·``"list"``·``"object"`` 중 하나."""
    required: bool
    length: int | None = None
    desc: str = ""
    codes: Mapping[str, str] = field(default_factory=lambda: MappingProxyType({}))
    """``desc`` 에서 휴리스틱으로 뽑은 ``코드 → 뜻``. 비어 있으면 코드값이 없거나 못 뽑은 것."""
    parent: str | None = None
    """``list`` 필드의 자식이면 그 list 필드의 id."""


@dataclass(frozen=True)
class TRSpec:
    """TR(api_id) 하나의 명세."""

    api_id: str
    name: str
    menu: tuple[str, ...]
    method: str
    url: str
    transport: str
    """``"rest"`` 또는 ``"websocket"``."""
    source: str
    """``"official"``(공식 명세 변환) 또는 ``"repo"``(레포에서 확인한 필드만)."""
    request: tuple[Field, ...]
    response: tuple[Field, ...]
    note: str = ""

    @property
    def request_fields(self) -> tuple[Field, ...]:
        """요청 바디 최상위 필드 (list 자식 제외) — 메서드 키워드 인자가 되는 것."""
        return tuple(f for f in self.request if f.parent is None)

    @property
    def required_fields(self) -> tuple[str, ...]:
        """필수(``required``) 최상위 요청 필드 id."""
        return tuple(f.id for f in self.request_fields if f.required)

    def request_field(self, field_id: str) -> Field | None:
        """최상위 요청 필드 하나를 id 로 찾는다."""
        return next((f for f in self.request_fields if f.id == field_id), None)


def _field(raw: Mapping[str, Any]) -> Field:
    return Field(
        id=raw["id"],
        name=raw.get("name", ""),
        type=raw.get("type", "string"),
        required=bool(raw.get("required", False)),
        length=raw.get("length"),
        desc=raw.get("desc", ""),
        codes=MappingProxyType(dict(raw.get("codes", {}))),
        parent=raw.get("parent"),
    )


def _tr(raw: Mapping[str, Any]) -> TRSpec:
    return TRSpec(
        api_id=raw["api_id"],
        name=raw.get("name", ""),
        menu=tuple(raw.get("menu", ())),
        method=raw.get("method", "POST"),
        url=raw.get("url", ""),
        transport=raw.get("transport", "rest"),
        source=raw.get("source", "official"),
        request=tuple(_field(f) for f in raw.get("request", ())),
        response=tuple(_field(f) for f in raw.get("response", ())),
        note=raw.get("note", ""),
    )


@lru_cache(maxsize=1)
def _raw_catalog() -> dict[str, Any]:
    text = resources.files(__name__).joinpath("catalog.json").read_text(encoding="utf-8")
    data: dict[str, Any] = json.loads(text)
    return data


@lru_cache(maxsize=1)
def _specs() -> Mapping[str, TRSpec]:
    return MappingProxyType({k: _tr(v) for k, v in _raw_catalog()["trs"].items()})


def get(api_id: str) -> TRSpec:
    """api_id 로 TR 명세를 얻는다. 없으면 ``KeyError``."""
    try:
        return _specs()[api_id]
    except KeyError:
        raise KeyError(f"카탈로그에 없는 api_id: {api_id!r}") from None


def api_ids() -> list[str]:
    """카탈로그의 모든 api_id (정렬)."""
    return sorted(_specs())


def search(query: str) -> list[TRSpec]:
    """api_id·TR 이름·메뉴에 ``query`` 가 들어간 TR (대소문자 무시)."""
    q = query.strip().lower()
    return [
        tr
        for tr in _specs().values()
        if q in tr.api_id.lower() or q in tr.name.lower() or any(q in m.lower() for m in tr.menu)
    ]


def catalog_source() -> dict[str, Any]:
    """카탈로그를 만든 원천 (저장소·경로·고정 커밋)."""
    return dict(_raw_catalog()["source"])


class _Recorder:
    """메서드를 불러 보고 어떤 (url, api_id) 로 나가는지만 적는 가짜 클라이언트."""

    def __init__(self) -> None:
        self.calls: list[tuple[str, str]] = []

    def request(self, resource_url: str, api_id: str, *args: Any, **kwargs: Any) -> None:
        self.calls.append((resource_url, api_id))


@lru_cache(maxsize=1)
def endpoint_index() -> Mapping[tuple[str, str], str]:
    """``(모듈 이름, 메서드 이름) → api_id`` — REST 모듈 메서드 전부.

    소스를 파싱하지 않고 각 메서드를 기록용 가짜 클라이언트로 한 번씩 불러 얻는다
    (네트워크 없음). 조건검색(WebSocket)은 api_id 가 아니라 trnm 이라 뺀다.
    """
    import inspect

    from kiwoom_client._registry import MODULE_NAMES, ModuleRegistry

    recorder = _Recorder()
    registry: ModuleRegistry[Any] = ModuleRegistry()
    registry._client = recorder
    registry._init_modules()

    index: dict[tuple[str, str], str] = {}
    for module_name in MODULE_NAMES:
        if module_name == "condition_search":
            continue
        module_obj = getattr(registry, module_name)
        for method_name, method in inspect.getmembers(module_obj, inspect.ismethod):
            if method_name.startswith("_"):
                continue
            recorder.calls.clear()
            method()
            if len(recorder.calls) == 1:
                index[(module_name, method_name)] = recorder.calls[0][1]
    return MappingProxyType(index)


@lru_cache(maxsize=1)
def _module_classes() -> Mapping[type, str]:
    """엔드포인트 모듈 클래스 → 모듈 이름 (``Account`` → ``"account"``)."""
    from kiwoom_client._registry import MODULE_NAMES, ModuleRegistry

    registry: ModuleRegistry[Any] = ModuleRegistry()
    registry._client = _Recorder()
    registry._init_modules()
    return MappingProxyType({type(getattr(registry, m)): m for m in MODULE_NAMES})


def for_method(module_name: str, method_name: str) -> TRSpec:
    """``api.<module_name>.<method_name>`` 이 부르는 TR 의 명세."""
    try:
        api_id = endpoint_index()[(module_name, method_name)]
    except KeyError:
        raise KeyError(f"REST 엔드포인트 메서드가 아니다: {module_name}.{method_name}") from None
    return get(api_id)


def method_for(api_id: str) -> tuple[str, str] | None:
    """api_id 를 부르는 ``(모듈 이름, 메서드 이름)`` — 감싼 메서드가 없으면 ``None``."""
    for key, value in endpoint_index().items():
        if value == api_id:
            return key
    return None


def resolve(target: Any) -> TRSpec:
    """api_id(``"ka10001"``), ``"stock_info.basic_stock_info"``, 또는 바운드 메서드
    (``api.stock_info.basic_stock_info``) → TR 명세."""
    if isinstance(target, str):
        if "." in target:
            module, _, method = target.removeprefix("api.").partition(".")
            return for_method(module, method.removesuffix("()"))
        return get(target)
    name = getattr(target, "__name__", None)
    owner = getattr(target, "__self__", None)
    owner_module = _module_classes().get(type(owner)) if owner is not None else None
    if name and owner_module:
        return for_method(owner_module, name)
    raise KeyError(f"api_id·'모듈.메서드'·엔드포인트 메서드 중 하나여야 한다: {target!r}")


def describe(target: Any) -> str:
    """TR 하나의 사람이 읽을 도움말 — 호출 예, 요청 필드(필수·코드값), 응답 필드.

    ``target`` 은 :func:`resolve` 가 받는 것 무엇이든. ``print(spec.describe("ka10001"))``.
    """
    tr = resolve(target)
    where = method_for(tr.api_id)
    lines = [f"{tr.api_id} {tr.name} — {tr.method} {tr.url}"]
    if where is not None:
        args = ", ".join(f'{fid}="..."' for fid in tr.required_fields)
        lines.append(f"  api.{where[0]}.{where[1]}({args})")
    if tr.source != "official":
        lines.append(f"  (출처 {tr.source}: {tr.note})")
    lines += ["", "요청 필드:"]
    if not tr.request_fields:
        lines.append("  (없음)")
    for f in tr.request_fields:
        mark = "*" if f.required else " "
        lines.append(f" {mark}{f.id:<16} {f.name}")
        if f.codes:
            codes = ", ".join(f"{k}={v}" for k, v in f.codes.items())
            lines.append(f"  {'':<16} 코드: {codes}")
        elif f.desc:
            lines.append(f"  {'':<16} {' '.join(f.desc.split())}")
    lines += ["  (* 필수)", "", "응답 필드:"]
    if not tr.response:
        lines.append("  (미확인)")
    for f in tr.response:
        label = f"{f.parent}[].{f.id}" if f.parent else f.id
        suffix = " (list)" if f.type == "list" else ""
        lines.append(f"  {label:<24} {f.name}{suffix}")
    return "\n".join(lines)
