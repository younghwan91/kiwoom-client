"""REST 엔드포인트 모듈의 ``.pyi`` 스텁을 TR 카탈로그로 만든다.

런타임 메서드는 그대로 ``(self, cont_yn="N", next_key="", **kwargs)`` 다. 스텁은 같은 시그니처에
카탈로그의 요청 필드를 키워드 전용 인자로 더해, IDE 자동완성과 mypy 가 필드명을 알게 한다.
``**kwargs: Any`` 는 남겨서 카탈로그에 없는 필드도 지금처럼 넘길 수 있다. 필드는 모두
선택(``= ...``)이다 — 필수 여부는 독스트링과 ``validate_params`` 가 알려 준다.

실행 (레포 루트):

    uv run python scripts/build_stubs.py          # src/kiwoom_client/domestic/*.pyi 를 쓴다
    uv run python scripts/build_stubs.py --check  # 다르면 1 (tests/test_stubs.py 도 같은 검사)
"""

from __future__ import annotations

import argparse
import inspect
import sys
import textwrap
import unicodedata
from pathlib import Path

from kiwoom_client import spec
from kiwoom_client._registry import MODULE_NAMES, ModuleRegistry

ROOT = Path(__file__).resolve().parent.parent
DOMESTIC = ROOT / "src" / "kiwoom_client" / "domestic"

HEADER = (
    "# 자동 생성 — 고치지 말 것. scripts/build_stubs.py 가 spec/catalog.json 으로 만든다.\n"
    "# 런타임은 .py 그대로(**kwargs). 스텁은 요청 필드를 IDE·mypy 에 알려 줄 뿐이다.\n"
)

_RESERVED = {"self", "cont_yn", "next_key", "kwargs"}


def _width(text: str) -> int:
    # ruff 의 E501 은 표시 폭으로 센다 — 한글(전각)은 2칸.
    return sum(2 if unicodedata.east_asian_width(ch) in "WF" else 1 for ch in text)


def _wrap(text: str, first: str, rest: str, width: int = 100) -> list[str]:
    """한 필드 설명을 표시 폭 ``width`` 안으로 접는다 (스텁도 ruff E501 을 받는다)."""
    lines: list[str] = []
    line = ""
    for word in text.split():
        prefix = rest if lines else first
        joined = f"{line} {word}" if line else word
        if line and _width(prefix + joined) > width:
            lines.append(prefix + line)
            line = word
        else:
            line = joined
    lines.append((rest if lines else first) + line)
    return lines


def _docstring(summary: str, tr: spec.TRSpec, indent: str) -> str:
    lines = [summary, "", f"api_id ``{tr.api_id}`` · {tr.name} · ``{tr.method} {tr.url}``"]
    if tr.source != "official":
        note = _wrap(f"출처: {tr.source} — {tr.note}", indent, indent)
        lines += [ln[len(indent):] for ln in note]
    fields = tr.request_fields
    if fields:
        lines += ["", "Args:"]
        for f in fields:
            mark = " (필수)" if f.required else ""
            desc = f" — {f.desc}" if f.desc else ""
            # 폭은 독스트링 들여쓰기까지 넣고 재고, 줄에는 Args 아래 들여쓰기만 남긴다.
            wrapped = _wrap(f"{f.id}: {f.name}{mark}{desc}", indent + "    ", indent + "        ")
            lines += [ln[len(indent):] for ln in wrapped]
    body = "\n".join(lines).replace("\\", "\\\\").replace('"""', '\\"\\"\\"')
    return textwrap.indent(f'"""{body}\n"""', indent)


def _method_stub(method_name: str, summary: str, tr: spec.TRSpec) -> str:
    params = ["self", 'cont_yn: str = "N"', 'next_key: str = ""']
    fields = [f for f in tr.request_fields if f.id not in _RESERVED]
    if fields:
        params.append("*")
        params += [f"{f.id}: str = ..." for f in fields]
    params.append("**kwargs: Any")
    args = "".join(f"        {p},\n" for p in params)
    return (
        f"    def {method_name}(\n{args}    ) -> ResponseT:\n"
        f"{_docstring(summary, tr, '        ')}\n"
        f"        ...\n"
    )


def render_module(module_name: str) -> tuple[Path, str]:
    registry: ModuleRegistry = ModuleRegistry()
    registry._client = object()  # type: ignore[assignment]
    registry._init_modules()
    module_obj = getattr(registry, module_name)
    cls = type(module_obj)
    path = Path(inspect.getfile(cls)).with_suffix(".pyi")

    parts = [
        HEADER,
        "from typing import Any, Generic\n\n",
        "from kiwoom_client.base import ClientProtocol, ResponseT\n\n",
        f"class {cls.__name__}(Generic[ResponseT]):\n",
        textwrap.indent(f'"""{inspect.getdoc(cls)}\n"""', "    ") + "\n\n",
        "    RESOURCE_URL: str\n\n",
        "    def __init__(self, client: ClientProtocol[ResponseT]) -> None: ...\n",
    ]
    index = spec.endpoint_index()
    for method_name, method in inspect.getmembers(module_obj, inspect.ismethod):
        if method_name.startswith("_"):
            continue
        tr = spec.get(index[(module_name, method_name)])
        summary = (inspect.getdoc(method) or tr.name).splitlines()[0]
        parts.append("\n" + _method_stub(method_name, summary, tr))
    return path, "".join(parts)


def render_all() -> dict[Path, str]:
    return dict(render_module(m) for m in MODULE_NAMES if m != "condition_search")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--check", action="store_true", help="쓰지 않고 다르면 1 로 끝낸다")
    args = parser.parse_args(argv)

    stale = []
    for path, text in render_all().items():
        current = path.read_text(encoding="utf-8") if path.exists() else None
        if current == text:
            continue
        stale.append(path)
        if not args.check:
            path.write_text(text, encoding="utf-8")
    if args.check and stale:
        names = ", ".join(p.name for p in stale)
        print(f"스텁이 카탈로그와 다르다: {names} — build_stubs.py 를 돌릴 것", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
