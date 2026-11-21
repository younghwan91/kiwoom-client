"""코드에서 문서를 생성한다 — 엔드포인트 표처럼 손으로 쓰면 코드와 어긋나는 파일들.

실행 (레포 루트):
    python scripts/gen_docs.py           # 생성 파일을 다시 쓴다
    python scripts/gen_docs.py --check   # 어긋난 파일이 있으면 목록을 찍고 1 로 끝난다

목록은 네트워크 없이 코드에서만 뽑는다:
- REST: ``kiwoom_client._registry.MODULE_NAMES`` 의 각 모듈 메서드를 기록용 가짜 클라이언트로
  불러 ``(resource_url, api_id)`` 를 받아 적는다. 이름은 docstring 첫 줄
  ``"한글명 (English Name)"`` 에서 나눈다.
- 조건검색: ``ConditionSearch`` 메서드가 만드는 페이로드의 ``trnm``
- 실시간: ``kiwoom_client.websocket.REALTIME_TYPES``

``tests/test_generated_docs.py`` 가 생성 결과와 커밋된 파일이 같은지 본다 — 엔드포인트를 더하거나
이름을 바꾸면 이 스크립트를 다시 돌려 같이 커밋한다.
"""

from __future__ import annotations

import argparse
import inspect
import re
import sys
from collections.abc import Callable
from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from string import Template
from typing import Any

ROOT = Path(__file__).resolve().parent.parent
TEMPLATES = Path(__file__).resolve().parent / "templates"
sys.path.insert(0, str(ROOT / "src"))

from kiwoom_client._registry import MODULE_NAMES, ModuleRegistry  # noqa: E402
from kiwoom_client.domestic.condition_search import ConditionSearch  # noqa: E402
from kiwoom_client.websocket import REALTIME_TYPES  # noqa: E402

sys.path.insert(0, str(Path(__file__).resolve().parent))
import gen_reference  # noqa: E402  (scripts/gen_reference.py — 필드 레퍼런스)

REPO_URL = "https://github.com/younghwan91/kiwoom-client"
OFFICIAL_GUIDE = "https://openapi.kiwoom.com/guide/apiguide"

#: WebSocket 으로 가는 모듈 — REST 표에서 빼고 따로 적는다.
WS_MODULES = frozenset({"condition_search"})

#: 실주문 모듈. MCP 서버는 실전 계좌에서 opt-in 없이는 이 도구들을 등록하지 않는다
#: (``kiwoom_client.mcp.tools.GUARDED_MODULES`` 와 같아야 한다 — 테스트가 본다).
ORDER_MODULES = frozenset({"order", "credit_order"})

#: 모듈 제목 (한글, English). 표의 순서는 MODULE_NAMES 를 따른다.
MODULE_TITLES: dict[str, tuple[str, str]] = {
    "account": ("계좌", "Account"),
    "stock_info": ("종목정보", "Stock info"),
    "market": ("시세", "Market"),
    "chart": ("차트", "Chart"),
    "order": ("주문", "Order"),
    "credit_order": ("신용주문", "Credit order"),
    "ranking": ("순위정보", "Ranking"),
    "sector": ("업종", "Sector"),
    "foreign_institution": ("기관/외국인", "Foreign / institution"),
    "short_selling": ("공매도", "Short selling"),
    "slb": ("대차거래", "Stock lending & borrowing"),
    "theme": ("테마", "Theme"),
    "condition_search": ("조건검색", "Condition search"),
    "elw": ("ELW", "ELW"),
    "etf": ("ETF", "ETF"),
}

_DOC_NAME = re.compile(r"^(?P<ko>.*?)\s*\((?P<en>[^()]*(?:\([^()]*\)[^()]*)*)\)\s*\.?$")


@dataclass(frozen=True)
class Endpoint:
    """REST 엔드포인트 하나 = 모듈 메서드 하나."""

    module: str
    method: str
    api_id: str
    url: str
    name_ko: str
    name_en: str

    @property
    def call(self) -> str:
        return f"api.{self.module}.{self.method}"

    @property
    def tool(self) -> str:
        """MCP 도구 이름 (``kiwoom_client.mcp.tools`` 와 같은 규칙)."""
        return f"{self.module}_{self.method}"

    @property
    def is_order(self) -> bool:
        return self.module in ORDER_MODULES


@dataclass(frozen=True)
class WsCall:
    """조건검색처럼 WebSocket 으로 보내는 페이로드 빌더 하나."""

    module: str
    method: str
    trnm: str
    name_ko: str
    name_en: str

    @property
    def call(self) -> str:
        return f"api.{self.module}.{self.method}"


class _Recorder:
    """``ClientProtocol`` 자리에 끼워 요청을 보내는 대신 (url, api_id) 를 돌려준다."""

    def request(
        self,
        resource_url: str,
        api_id: str,
        body: dict[str, Any] | None = None,
        cont_yn: str = "N",
        next_key: str = "",
        extra_headers: dict[str, str] | None = None,
    ) -> tuple[str, str]:
        return resource_url, api_id


def split_doc_name(method: Callable[..., Any]) -> tuple[str, str]:
    """docstring 첫 줄 ``"한글명 (English)"`` → ``("한글명", "English")``."""
    first = (inspect.getdoc(method) or "").strip().splitlines()
    line = first[0].strip() if first else ""
    m = _DOC_NAME.match(line)
    if not m:
        return line, ""
    return m.group("ko").strip(), m.group("en").strip()


def _public_methods(obj: object) -> list[tuple[str, Callable[..., Any]]]:
    return [
        (name, fn)
        for name, fn in inspect.getmembers(obj, inspect.ismethod)
        if not name.startswith("_")
    ]


def _registry() -> ModuleRegistry[Any]:
    registry: ModuleRegistry[Any] = ModuleRegistry()
    registry._client = _Recorder()  # type: ignore[assignment]
    registry._init_modules()
    return registry


def rest_endpoints() -> list[Endpoint]:
    """REST 엔드포인트 전부, MODULE_NAMES 순서·모듈 안에서는 api_id 순."""
    registry = _registry()
    out: list[Endpoint] = []
    for module in MODULE_NAMES:
        if module in WS_MODULES:
            continue
        found = []
        for name, fn in _public_methods(getattr(registry, module)):
            url, api_id = fn()
            ko, en = split_doc_name(fn)
            found.append(Endpoint(module, name, api_id, url, ko, en))
        out.extend(sorted(found, key=lambda e: (e.api_id, e.method)))
    return out


def ws_calls() -> list[WsCall]:
    """조건검색 페이로드 빌더 전부 (``seq`` 는 아무 값이나 넣어 trnm 만 본다)."""
    cs = ConditionSearch()
    out = []
    for name, fn in _public_methods(cs):
        params = inspect.signature(fn).parameters
        payload = fn(seq="1") if "seq" in params else fn()
        ko, en = split_doc_name(fn)
        out.append(WsCall("condition_search", name, payload["trnm"], ko, en))
    order = {"CNSRLST": 0, "CNSRREQ": 1, "CNSRCLR": 2}
    return sorted(out, key=lambda c: (order.get(c.trnm, 9), c.method))


def _md_escape(text: str) -> str:
    return text.replace("|", "\\|")


def module_title(module: str) -> str:
    """``"계좌 (Account)"`` — 한글과 영어가 같으면 한 번만."""
    ko, en = MODULE_TITLES.get(module, (module, module))
    return ko if ko == en else f"{ko} ({en})"


# --------------------------------------------------------------------------- endpoints.md

ENDPOINTS_PATH = "docs/endpoints.md"
GENERATED_NOTE = (
    "<!-- 자동 생성 파일 — 손으로 고치지 마세요. "
    "`python scripts/gen_docs.py` 로 다시 만듭니다. -->"
)


def _api_id_link(ep: Endpoint) -> str:
    """api_id 칸 — 필드 레퍼런스(docs/reference/<모듈>.md)의 그 TR 로 링크."""
    return f"[`{ep.api_id}`]({gen_reference.anchor_link(ep.module, ep.api_id)})"


def render_endpoints() -> str:
    eps = rest_endpoints()
    calls = ws_calls()
    by_module: dict[str, list[Endpoint]] = {}
    for ep in eps:
        by_module.setdefault(ep.module, []).append(ep)

    lines: list[str] = [
        GENERATED_NOTE,
        "",
        "# 엔드포인트 전체 목록 (Endpoint reference)",
        "",
        f"kiwoom-client 가 감싼 키움 REST API **{len(eps)}개**, 조건검색 **{len(calls)}종**, "
        f"실시간 시세 **{len(REALTIME_TYPES)}종**을 코드에서 그대로 뽑은 표입니다.",
        "",
        "- **api_id** 는 키움 공식 가이드의 TR 코드(`ka10001` 등)와 같습니다. 이 페이지에서 "
        "`Ctrl+F` 로 api_id·한글 TR 이름·메서드 이름 어느 것으로든 찾을 수 있습니다.",
        "- 모든 REST 메서드는 시그니처가 같습니다: `(cont_yn=\"N\", next_key=\"\", **요청필드)`. "
        "요청 필드는 키워드 인자로 그대로 넘기면 본문(JSON)이 됩니다 — api_id 를 누르면 그 TR 의 "
        "요청·응답 필드가 있는 [필드 레퍼런스](reference/index.md)로 갑니다 "
        f"(원문: [키움 REST API 가이드]({OFFICIAL_GUIDE})).",
        "- **MCP 도구 이름**은 `<모듈>_<메서드>` 입니다 (예: `stock_info_basic_stock_info`).",
        "- ⚠️ 표시는 **실주문**입니다. `is_mock=False`(기본값) 로 부르면 실계좌에서 체결됩니다.",
        "",
        "```python",
        "from kiwoom_client import KiwoomAPI",
        "",
        'api = KiwoomAPI(app_key="...", app_secret="...", is_mock=True)',
        'info = api.stock_info.basic_stock_info(stk_cd="005930")  # ka10001',
        "```",
        "",
        "## 모듈 요약",
        "",
        "| 모듈 | 이름 | 개수 | URL |",
        "|---|---|---:|---|",
    ]
    for module in MODULE_NAMES:
        title = module_title(module)
        if module in WS_MODULES:
            lines.append(
                f"| [`api.{module}`](#{module}) | {title} | {len(calls)} | WebSocket (`trnm`) |"
            )
            continue
        group = by_module.get(module, [])
        urls = sorted({ep.url for ep in group})
        lines.append(
            f"| [`api.{module}`](#{module}) | {title} | {len(group)} | "
            + ", ".join(f"`{u}`" for u in urls)
            + " |"
        )
    lines.append(
        f"| [`api.create_websocket()`](#realtime) | 실시간 시세 (Real-time) | "
        f"{len(REALTIME_TYPES)} | WebSocket (`REG`) |"
    )
    lines.append("")

    for module in MODULE_NAMES:
        lines += [f'<a id="{module}"></a>', "", f"## `api.{module}` — {module_title(module)}", ""]
        if module in WS_MODULES:
            lines += [
                "REST 가 아니라 WebSocket 으로 보냅니다. 메서드는 요청 페이로드(dict)만 만들고, "
                "`ws.send()` 로 보낸 뒤 `ws.on_trnm()` 으로 응답을 받습니다.",
                "",
                "| 메서드 | trnm | 이름 | English |",
                "|---|---|---|---|",
            ]
            for c in calls:
                lines.append(
                    f"| `{c.call}()` | `{c.trnm}` | {_md_escape(c.name_ko)} | "
                    f"{_md_escape(c.name_en)} |"
                )
            lines.append("")
            continue
        group = by_module.get(module, [])
        urls = sorted({ep.url for ep in group})
        lines.append("URL: " + ", ".join(f"`POST {u}`" for u in urls))
        if module in ORDER_MODULES:
            lines += [
                "",
                "> ⚠️ **실주문 모듈입니다.** `is_mock=False`(기본값)면 실계좌에 주문이 나갑니다. "
                "MCP 서버는 실전 계좌에서 `KIWOOM_MCP_ALLOW_LIVE_ORDERS=true` 가 아니면 "
                "이 도구들을 등록하지 않지만, 파이썬에서 직접 부르는 호출은 막지 않습니다.",
            ]
        lines += ["", "| api_id | 메서드 | 이름 | English |", "|---|---|---|---|"]
        for ep in group:
            mark = "⚠️ " if ep.is_order else ""
            lines.append(
                f"| {_api_id_link(ep)} | {mark}`{ep.call}()` | {_md_escape(ep.name_ko)} | "
                f"{_md_escape(ep.name_en)} |"
            )
        lines.append("")

    lines += [
        '<a id="realtime"></a>',
        "",
        "## 실시간 시세 — `api.create_websocket()`",
        "",
        "`ws.subscribe(<타입>, <종목코드>)` 로 등록하고 `ws.on(<타입>, 콜백)` 으로 받습니다. "
        "콜백이 받는 `values` 의 키는 키움 FID 번호입니다.",
        "",
        "| 타입 | 이름 |",
        "|---|---|",
    ]
    for code, name in REALTIME_TYPES.items():
        lines.append(f"| `{code}` | {_md_escape(name)} |")
    lines.append("")

    lines += [
        "## api_id 색인",
        "",
        "api_id 순으로 정렬한 같은 목록입니다.",
        "",
        "| api_id | 메서드 | 이름 |",
        "|---|---|---|",
    ]
    for ep in sorted(eps, key=lambda e: (e.api_id, e.module, e.method)):
        mark = "⚠️ " if ep.is_order else ""
        lines.append(f"| {_api_id_link(ep)} | {mark}`{ep.call}()` | {_md_escape(ep.name_ko)} |")
    lines.append("")
    return "\n".join(lines)


# --------------------------------------------------------------------------- llms.txt

LLMS_PATH = "llms.txt"
LLMS_FULL_PATH = "llms-full.txt"
RAW_URL = "https://raw.githubusercontent.com/younghwan91/kiwoom-client/main"

#: llms.txt 의 링크 목록: (섹션, 레포 안 경로 또는 URL, 제목, 설명).
#: 레포 안 경로는 raw URL 로 바뀌고, 테스트가 파일이 실제로 있는지 본다.
LLMS_LINKS: list[tuple[str, str, str, str]] = [
    ("Docs", "docs/endpoints.md", "Endpoint reference",
     "every REST method with api_id, URL and Korean/English TR name; condition search; "
     "real-time types"),
    ("Docs", "README_EN.md", "README (English)",
     "install, quick start, accounts and orders, asyncio, DataFrame parsing, WebSocket, "
     "pagination, rate limits, MCP server"),
    ("Docs", "README.md", "README (한국어)", "the same, in Korean"),
    ("Docs", "AGENTS.md", "AGENTS.md",
     "rules for AI agents using or working on this library: safety, lookups, tests"),
    ("Docs", "docs/migration-from-openapi-plus.md", "Migrating from OpenAPI+ (OCX) / pykiwoom",
     "OpenAPI+ functions, SendOrder codes, real-time types and TR codes mapped to REST"),
    ("Optional", LLMS_FULL_PATH, "llms-full.txt",
     "public API signatures and docstrings plus the full endpoint list in one file"),
    ("Optional", "CHANGELOG.md", "Changelog", "release history"),
    ("Optional", OFFICIAL_GUIDE, "Kiwoom REST API guide (official)",
     "request/response field definitions for each api_id"),
    ("Optional", "https://github.com/Kiwoom-Securities/Kiwoom-REST-API",
     "Kiwoom REST API spec (official GitHub)", "machine-readable spec and error codes"),
]


def link_url(target: str) -> str:
    return target if "://" in target else f"{RAW_URL}/{target}"


def template(name: str, **values: object) -> str:
    """``scripts/templates/<name>`` 을 읽어 ``$이름`` 자리를 채운다.

    사람이 쓰는 문장은 코드가 아니라 마크다운 원본에 둔다 — 고치기 쉽고, AGENTS.md·
    Cursor·Copilot 규칙처럼 여러 생성물이 같은 원본을 쓸 수 있다.
    """
    text = (TEMPLATES / name).read_text(encoding="utf-8")
    return Template(text).substitute(values).rstrip("\n")


def _counts() -> dict[str, int]:
    return {"n_rest": len(rest_endpoints()), "n_cs": len(ws_calls()), "n_rt": len(REALTIME_TYPES)}


def usage_rules() -> str:
    """이 라이브러리로 코드를 쓸 때의 규칙 — llms.txt·AGENTS.md·편집기 규칙이 같이 쓰는 원본."""
    return template("usage-rules.md")


def _llms_summary() -> list[str]:
    return template("llms-summary.md", usage_rules=usage_rules(), **_counts()).splitlines()


# --------------------------------------------------------------------------- AGENTS.md

AGENTS_PATH = "AGENTS.md"


def render_agents() -> str:
    note = (
        "<!-- 자동 생성 파일 — scripts/templates/AGENTS.md (와 usage-rules.md) 를 고치고 "
        "`python scripts/gen_docs.py` 로 다시 만듭니다. -->"
    )
    body = template("AGENTS.md", usage_rules=usage_rules(), **_counts())
    return f"{note}\n\n{body}\n"


def render_llms_txt() -> str:
    lines = [*_llms_summary()]
    section = None
    for sec, target, title, desc in LLMS_LINKS:
        if sec != section:
            lines += ["", f"## {sec}", ""]
            section = sec
        lines.append(f"- [{title}]({link_url(target)}): {desc}")
    lines.append("")
    return "\n".join(lines)


def _format_annotation(ann: Any) -> str:
    if ann is inspect.Parameter.empty:
        return ""
    if isinstance(ann, str):
        return ann
    return inspect.formatannotation(ann)


def format_signature(name: str, fn: Callable[..., Any]) -> str:
    """``str(inspect.signature)`` 는 파이썬 버전마다 다르게 찍힐 수 있어 직접 만든다."""
    sig = inspect.signature(fn)
    parts: list[str] = []
    star_done = False
    for i, p in enumerate(sig.parameters.values()):
        if i == 0 and p.name in {"self", "cls"}:
            continue
        if p.kind is p.KEYWORD_ONLY and not star_done:
            parts.append("*")
            star_done = True
        text = p.name
        if p.kind is p.VAR_POSITIONAL:
            text, star_done = "*" + p.name, True
        elif p.kind is p.VAR_KEYWORD:
            text = "**" + p.name
        ann = _format_annotation(p.annotation)
        if ann:
            text += f": {ann}"
        if p.default is not inspect.Parameter.empty:
            text += f" = {p.default!r}" if ann else f"={p.default!r}"
        parts.append(text)
    ret = _format_annotation(sig.return_annotation)
    prefix = "async def" if inspect.iscoroutinefunction(fn) else "def"
    return f"{prefix} {name}({', '.join(parts)})" + (f" -> {ret}" if ret else "")


Entry = tuple[str, str, str]
"""(표시 이름, 시그니처, docstring)."""

#: 공개 함수가 정의된 모듈 → llms-full.txt 섹션 제목. 없는 모듈은 모듈 이름을 그대로 쓴다.
FUNCTION_SECTIONS = {
    "kiwoom_client.parsing": "Response parsing",
    "kiwoom_client.tick_size": "KRX tick size",
}


def _entry(label: str, fn: Callable[..., Any]) -> Entry:
    return label, format_signature(label.split(".")[-1], fn), inspect.getdoc(fn) or ""


def _class_entry(label: str, cls: type) -> Entry:
    bases = ", ".join(b.__name__ for b in cls.__bases__ if b is not object)
    return label, f"class {cls.__name__}({bases})" if bases else f"class {cls.__name__}", (
        inspect.getdoc(cls) or ""
    )


def _is_function(obj: object) -> bool:
    """함수 또는 ``lru_cache`` 같은 래퍼로 감싼 함수 (클래스는 아님)."""
    return callable(obj) and not isinstance(obj, type)


def _public_methods_of(cls: type, skip: frozenset[str] = frozenset()) -> list[str]:
    """클래스에 정의된 공개 메서드 이름 (모듈 프로퍼티처럼 함수가 아닌 것은 뺀다)."""
    names = []
    for name in sorted(vars(cls)):
        if name.startswith("_") or name in skip:
            continue
        raw = inspect.getattr_static(cls, name)
        if isinstance(raw, (staticmethod, classmethod)) or inspect.isfunction(raw):
            names.append(name)
    return names


def _api_sections() -> list[tuple[str, str, list[Entry]]]:
    """llms-full.txt 에 적을 공개 API: (제목, 머리말, [Entry]).

    ``kiwoom_client.__all__``·``codes.__all__``·``errors.__all__``·``spec.__all__`` 에서 뽑으므로
    새로 공개한 이름은 다시 생성하기만 하면 들어간다.
    """
    import kiwoom_client as kc
    from kiwoom_client import codes, errors, spec
    from kiwoom_client.base import BaseClient
    from kiwoom_client.websocket import KiwoomWebSocket

    def facade(cls: type) -> list[Entry]:
        name = cls.__name__
        init = format_signature("__init__", cls.__init__)  # type: ignore[misc]
        out = [(name, init.replace("def __init__(", f"class {name}(", 1).split(" -> ")[0],
                inspect.getdoc(cls) or "")]
        for meth in _public_methods_of(cls):
            label, sig, doc = _entry(f"{name}.{meth}", getattr(cls, meth))
            # from_env 의 반환형은 TypeVar(_SyncT 등) — 읽는 쪽엔 클래스 이름이 맞다.
            out.append((label, re.sub(r"-> _\w+T$", f"-> {name}", sig), doc))
        return out

    sections: list[tuple[str, str, list[Entry]]] = [
        ("KiwoomAPI (sync facade)", "", facade(kc.KiwoomAPI)),
        ("AsyncKiwoomAPI (asyncio facade)", "Same endpoints as `KiwoomAPI`; every call is awaited.",
         facade(kc.AsyncKiwoomAPI)),
        ("Low-level client (`api._client`)", "",
         [_entry(f"api._client.{m}", getattr(BaseClient, m)) for m in ["request", "request_all"]]),
        ("KiwoomWebSocket (`ws = api.create_websocket()`)", "",
         [_entry(f"ws.{m}", getattr(KiwoomWebSocket, m))
          for m in _public_methods_of(KiwoomWebSocket)]),
    ]

    grouped: dict[str, list[Entry]] = {}
    for name in kc.__all__:
        obj = getattr(kc, name)
        if _is_function(obj):
            grouped.setdefault(obj.__module__, []).append(_entry(name, obj))
    for module, entries in grouped.items():
        sections.append((FUNCTION_SECTIONS.get(module, f"`{module}`"), "", entries))

    code_entries: list[Entry] = []
    for name in codes.__all__:
        obj = getattr(codes, name)
        if isinstance(obj, type) and issubclass(obj, Enum):
            members = "\n".join(f'{m.name} = "{m.value}"' for m in obj)
            label, _, doc = _class_entry(name, obj)
            code_entries.append((label, f"class {name}(str, Enum)\n{members}", doc))
        elif _is_function(obj):
            code_entries.append(_entry(name, obj))
    sections.append(("Named codes (`kiwoom_client.codes`)", inspect.getdoc(codes) or "",
                     code_entries))

    error_entries: list[Entry] = []
    for name in errors.__all__:
        obj = getattr(errors, name)
        if isinstance(obj, type) and issubclass(obj, BaseException):
            error_entries.append(_class_entry(name, obj))
        elif _is_function(obj):
            error_entries.append(_entry(name, obj))
    sections.append(("Errors (`kiwoom_client.errors`)", inspect.getdoc(errors) or "",
                     error_entries))

    spec_entries: list[Entry] = []
    for name in spec.__all__:
        obj = getattr(spec, name)
        if isinstance(obj, type):
            spec_entries.append(_class_entry(f"spec.{name}", obj))
        elif _is_function(obj):
            spec_entries.append(_entry(f"spec.{name}", obj))
    sections.append(("TR field catalog (`kiwoom_client.spec`)", "", spec_entries))
    return sections


def render_llms_full() -> str:
    lines = [
        *_llms_summary(),
        "",
        "This file is generated from the code by `scripts/gen_docs.py`; the signatures and "
        "docstrings below are the library's own.",
        "",
    ]
    for title, intro, entries in _api_sections():
        lines += [f"## {title}", ""]
        if intro:
            lines += [intro, ""]
        for label, sig, doc in entries:
            lines += [f"### `{label}`", "", "```", sig, "```", ""]
            if doc:
                lines += [doc, ""]
    while lines and lines[-1] == "":
        lines.pop()

    eps = rest_endpoints()
    lines += [
        "",
        f"## REST endpoints ({len(eps)})",
        "",
        "Format: `api_id` `api.<module>.<method>()` — 한글 TR 이름 (English) [POST url]. "
        "⚠️ = places a real order when `is_mock=False`.",
    ]
    current = None
    for ep in eps:
        if ep.module != current:
            lines += ["", f"### api.{ep.module} — {module_title(ep.module)}", ""]
            current = ep.module
        mark = "⚠️ " if ep.is_order else ""
        lines.append(
            f"- {mark}`{ep.api_id}` `{ep.call}()` — {ep.name_ko} ({ep.name_en}) [POST {ep.url}]"
        )
    lines += ["", "## Condition search (WebSocket payload builders)", ""]
    for c in ws_calls():
        lines.append(f"- `{c.trnm}` `{c.call}()` — {c.name_ko} ({c.name_en})")
    lines += ["", "## Real-time types (`await ws.subscribe(type, item)`)", ""]
    for code, name in REALTIME_TYPES.items():
        lines.append(f"- `{code}` {name}")
    lines.append("")
    return "\n".join(lines)


# --------------------------------------------------------------------------- 진입점

#: 생성 파일 경로(레포 루트 기준) → 렌더 함수.
TARGETS: dict[str, Callable[[], str]] = {
    ENDPOINTS_PATH: render_endpoints,
    LLMS_PATH: render_llms_txt,
    LLMS_FULL_PATH: render_llms_full,
    AGENTS_PATH: render_agents,
    **gen_reference.targets(),
}


def stale_targets() -> list[str]:
    """커밋된 내용이 생성 결과와 다른 파일 목록."""
    stale = []
    for rel, render in TARGETS.items():
        path = ROOT / rel
        if not path.exists() or path.read_text(encoding="utf-8") != render():
            stale.append(rel)
    return stale


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--check", action="store_true", help="쓰지 않고 어긋난 파일만 알린다")
    args = parser.parse_args(argv)

    if args.check:
        stale = stale_targets()
        for rel in stale:
            print(f"stale: {rel}  (python scripts/gen_docs.py 로 다시 생성)")
        return 1 if stale else 0

    for rel, render in TARGETS.items():
        path = ROOT / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(render(), encoding="utf-8")
        print(f"wrote {rel}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
