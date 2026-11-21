"""TR 카탈로그로 ``docs/reference/`` 필드 레퍼런스를 만든다 — 모듈마다 한 페이지.

``scripts/gen_docs.py`` 가 이 모듈의 :func:`targets` 를 자기 ``TARGETS`` 에 합치므로 따로 돌릴 일은
없다 (``python scripts/gen_docs.py`` 가 같이 쓰고, ``--check``·``tests/test_generated_docs.py`` 가
같이 본다). 데이터는 ``kiwoom_client.spec`` (출처: ``src/kiwoom_client/spec/SOURCE.md``).
"""

from __future__ import annotations

import inspect
import json
import sys
from collections.abc import Callable
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))

from kiwoom_client import spec  # noqa: E402
from kiwoom_client._registry import MODULE_NAMES, ModuleRegistry  # noqa: E402

REFERENCE_DIR = "docs/reference"
OFFICIAL_PORTAL = "https://openapi.kiwoom.com"
SOURCE_DOC = (
    "https://github.com/younghwan91/kiwoom-client/blob/main/src/kiwoom_client/spec/SOURCE.md"
)
GENERATED_NOTE = (
    "<!-- 자동 생성 파일 — 손으로 고치지 마세요. "
    "`python scripts/gen_docs.py` 가 TR 카탈로그(kiwoom_client.spec)로 다시 만듭니다. -->"
)
ORDER_MODULES = frozenset({"order", "credit_order"})


def rest_modules() -> list[str]:
    return [m for m in MODULE_NAMES if m != "condition_search"]


def module_title(module: str) -> str:
    """모듈 프로퍼티 독스트링 ``"계좌 (Account) endpoints."`` → ``"계좌 (Account)"``"""
    doc = inspect.getdoc(getattr(ModuleRegistry, module)) or module
    return doc.splitlines()[0].removesuffix(".").removesuffix(" endpoints").strip()


def page_path(module: str) -> str:
    return f"{REFERENCE_DIR}/{module}.md"


def anchor_link(module: str, api_id: str, *, from_dir: str = "docs") -> str:
    """``from_dir`` 기준 상대 링크 (``reference/account.md#kt00004``)."""
    rel = Path(page_path(module)).relative_to(from_dir)
    return f"{rel.as_posix()}#{api_id.lower()}"


def front_matter(seo_title: str, description: str) -> list[str]:
    """검색 결과용 제목·설명 front matter (overrides/main.html 이 <title>·meta description 에 쓴다).

    값은 JSON 문자열로 — 콜론·따옴표가 들어가도 YAML 이 깨지지 않는다.
    """
    return [
        "---",
        f"seo_title: {json.dumps(seo_title, ensure_ascii=False)}",
        f"description: {json.dumps(description, ensure_ascii=False)}",
        "---",
        "",
    ]


def _cell(text: str) -> str:
    return " ".join(text.split()).replace("|", "\\|") or " "


def _methods(module: str) -> list[tuple[str, str, spec.TRSpec]]:
    """(메서드 이름, 독스트링 첫 줄, TR) — api_id 순."""
    registry: ModuleRegistry = ModuleRegistry()
    registry._client = object()  # type: ignore[assignment]
    registry._init_modules()
    module_obj = getattr(registry, module)
    index = spec.endpoint_index()
    out = []
    for name, method in inspect.getmembers(module_obj, inspect.ismethod):
        if name.startswith("_"):
            continue
        first = (inspect.getdoc(method) or name).splitlines()[0]
        out.append((name, first, spec.get(index[(module, name)])))
    return sorted(out, key=lambda item: (item[2].api_id, item[0]))


def _field_rows(fields: tuple[spec.Field, ...], *, request: bool) -> list[str]:
    if request:
        rows = ["| 필드 | 한글명 | 필수 | 길이 |", "|---|---|:---:|---:|"]
    else:
        rows = ["| 필드 | 한글명 | 길이 |", "|---|---|---:|"]
    for f in fields:
        name = f"`{f.parent}[].{f.id}`" if f.parent else f"`{f.id}`"
        if f.type == "list":
            name += " (list)"
        length = str(f.length) if f.length is not None else ""
        if request:
            rows.append(f"| {name} | {_cell(f.name)} | {'Y' if f.required else ''} | {length} |")
        else:
            rows.append(f"| {name} | {_cell(f.name)} | {length} |")
    return rows


def render_module(module: str) -> str:
    title = module_title(module)
    short = title.split(" (")[0]  # "차트 (Chart)" → "차트"
    methods = _methods(module)
    ids = "·".join(tr.api_id for _name, _first, tr in methods[:3])
    more = " 등" if len(methods) > 3 else ""
    lines = [
        *front_matter(
            f"키움 REST API {short} TR 요청·응답 필드 — api.{module}",
            f"키움증권 REST API {short} TR {len(methods)}개({ids}{more})의 "
            "요청·응답 필드 ID·한글명·필수·길이와 kiwoom-client 파이썬 호출 예.",
        ),
        GENERATED_NOTE,
        "",
        f"# `api.{module}` — {title}",
        "",
        "요청·응답 필드는 키움 공식 REST API 명세에서 만든 TR 카탈로그"
        f"([출처·라이선스]({SOURCE_DOC}))에서 옮긴 필드 ID·한글명·필수·길이입니다. "
        f"필드 설명·코드값은 싣지 않으니 [키움 REST API 포털]({OFFICIAL_PORTAL}) 문서를 보세요"
        "(자주 쓰는 코드값은 `kiwoom_client.codes`). 값은 모두 문자열로 넘깁니다.",
        "",
        "공통 헤더(`api-id`·`cont-yn`·`next-key`·`authorization`)는 라이브러리가 채웁니다 — "
        "연속조회는 메서드의 `cont_yn`·`next_key` 인자나 `request_all()` 을 쓰세요.",
        "",
    ]
    if module in ORDER_MODULES:
        lines += [
            "> ⚠️ **실주문 모듈입니다.** `is_mock=False`(기본값)면 실계좌에 주문이 나갑니다.",
            "",
        ]
    lines += ["| api_id | 메서드 | 이름 |", "|---|---|---|"]
    for name, _first, tr in methods:
        lines.append(f"| [`{tr.api_id}`](#{tr.api_id.lower()}) | `{name}()` | {_cell(tr.name)} |")
    lines.append("")

    for name, first, tr in methods:
        required = ", ".join(f"{fid}=..." for fid in tr.required_fields)
        lines += [
            f'<a id="{tr.api_id.lower()}"></a>',
            "",
            f"## `{tr.api_id}` · `{name}()` — {_cell(tr.name)}",
            "",
            f"{_cell(first)} · `{tr.method} {tr.url}`",
            "",
            "```python",
            f"api.{module}.{name}({required})",
            "```",
            "",
        ]
        if tr.source != "official":
            lines += [f"> 출처 `{tr.source}`: {_cell(tr.note)}", ""]
        lines += ["**요청**", ""]
        lines += _field_rows(tr.request, request=True) if tr.request else ["요청 필드 없음."]
        lines += ["", "**응답**", ""]
        lines += _field_rows(tr.response, request=False) if tr.response else ["응답 필드 미확인."]
        lines.append("")
    return "\n".join(lines)


def render_index() -> str:
    source = spec.catalog_source()
    total = sum(len(_methods(m)) for m in rest_modules())
    lines = [
        *front_matter(
            "키움 REST API 필드 레퍼런스 — TR별 요청·응답 필드",
            f"키움증권 REST API TR {total}개의 요청·응답 필드(필드 ID·한글명·필수·길이)를 "
            "모듈별로 모은 레퍼런스. 키움 공식 명세에서 만든 TR 카탈로그 기준입니다.",
        ),
        GENERATED_NOTE,
        "",
        "# 필드 레퍼런스 (Field reference)",
        "",
        "REST 엔드포인트마다 요청·응답 필드(필드명·한글명·필수·길이)를 모은 페이지입니다. "
        "모듈별 표에서 api_id 를 누르면 그 TR 로 갑니다.",
        "",
        f"- 데이터: 키움 공식 명세 [`{source['repository'].removeprefix('https://github.com/')}`]"
        f"({source['repository']}) 커밋 `{source['commit'][:7]}` 을 변환한 TR 카탈로그 "
        f"([출처·라이선스]({SOURCE_DOC}))",
        "- 코드에서: `kiwoom_client.spec.get(\"ka10001\")`, IDE 에서는 메서드 키워드 인자 자동완성",
        "- 보내기 전에 검사하려면 `KiwoomAPI(..., validate_params=\"warn\")`",
        "",
        "| 모듈 | 이름 | 개수 |",
        "|---|---|---:|",
    ]
    for module in rest_modules():
        lines.append(
            f"| [`api.{module}`]({module}.md) | {module_title(module)} | {len(_methods(module))} |"
        )
    lines.append("")
    return "\n".join(lines)


def targets() -> dict[str, Callable[[], str]]:
    """레포 안 경로 → 생성 함수 (gen_docs.TARGETS 에 합친다)."""
    out: dict[str, Callable[[], str]] = {f"{REFERENCE_DIR}/index.md": render_index}
    for module in rest_modules():
        out[page_path(module)] = lambda m=module: render_module(m)  # type: ignore[misc]
    return out
