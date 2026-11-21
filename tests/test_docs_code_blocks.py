"""문서 속 코드 블록이 최소한 '맞는 코드' 인지 본다 — 서버에는 아무것도 보내지 않는다.

검사 대상: README(한·영), CONTRIBUTING, examples/README, AGENTS.md, llms*.txt, docs/**/*.md,
skills/**/*.md. (docs/superpowers/ 는 작업 기록이라 뺀다.)

1. ```python 블록은 문법이 맞아야 한다 (최상위 ``await`` 허용 — 노트북·REPL 조각이 많다).
2. ```json 블록은 JSON 으로 읽혀야 한다.
3. ``api.<모듈>.<메서드>(`` / ``api.<메서드>(`` / ``ws.<메서드>(`` 는 실제로 있는 이름이어야 한다
   — AI 가 문서를 보고 없는 메서드를 부르는 일을 막는다.
4. ``from kiwoom_client... import X`` 의 X 는 실제로 있어야 한다.
5. docs/·skills/·AGENTS.md 안의 ``KiwoomAPI(...)``/``AsyncKiwoomAPI(...)``/``*.from_env(...)`` 는
   ``is_mock=True`` 를 넘겨야 한다 — 기본값이 실서버라 복사해 돌리면 실계좌에 닿는다.
6. 코드 블록 밖 본문(표·인라인 코드)의 ``api.<모듈>.<메서드>(`` 도 실제 이름이어야 하고,
   api_id(``ka10001`` 꼴)는 이 라이브러리나 공식 카탈로그(``kiwoom_client.spec``)에 있어야 한다.

블록 하나를 일부러 빼려면 바로 위 줄에 ``<!-- docs-test: skip -->`` 를 둔다.
"""

from __future__ import annotations

import ast
import importlib
import json
import re
import textwrap
from dataclasses import dataclass
from pathlib import Path

import pytest

from kiwoom_client import AsyncKiwoomAPI, KiwoomAPI, KiwoomWebSocket
from kiwoom_client._registry import MODULE_NAMES, ModuleRegistry
from kiwoom_client.base import BaseClient

ROOT = Path(__file__).resolve().parent.parent

_FENCE = re.compile(r"^(?P<indent>\s*)(?P<fence>`{3,}|~{3,})\s*(?P<lang>[\w+-]*)")
_SKIP_MARK = "<!-- docs-test: skip -->"

#: is_mock=True 를 강제하는 곳 (README 는 첫 화면 담당 레인이 따로 관리한다).
_MOCK_ONLY_PREFIXES = ("docs/", "skills/", "AGENTS.md")


@dataclass(frozen=True)
class Block:
    path: str
    line: int
    lang: str
    code: str

    def __str__(self) -> str:
        return f"{self.path}:{self.line}"


def doc_files() -> list[Path]:
    files = [
        ROOT / "README.md",
        ROOT / "README_EN.md",
        ROOT / "CONTRIBUTING.md",
        ROOT / "AGENTS.md",
        ROOT / "examples" / "README.md",
        *sorted(ROOT.glob("llms*.txt")),
        *sorted((ROOT / "docs").rglob("*.md")),
        *sorted((ROOT / "skills").rglob("*.md")),
    ]
    return [
        f for f in files
        if f.exists() and "superpowers" not in f.relative_to(ROOT).parts
    ]


def extract_blocks(path: Path) -> list[Block]:
    rel = path.relative_to(ROOT).as_posix()
    lines = path.read_text(encoding="utf-8").splitlines()
    blocks: list[Block] = []
    i = 0
    while i < len(lines):
        m = _FENCE.match(lines[i])
        if not m:
            i += 1
            continue
        fence, lang = m.group("fence"), m.group("lang").lower()
        skip = i > 0 and lines[i - 1].strip() == _SKIP_MARK
        start = i + 1
        j = start
        while j < len(lines) and not lines[j].strip().startswith(fence):
            j += 1
        if not skip:
            code = textwrap.dedent("\n".join(lines[start:j]))
            blocks.append(Block(rel, start, lang, code))
        i = j + 1
    return blocks


ALL_BLOCKS = [b for f in doc_files() for b in extract_blocks(f)]
PY_BLOCKS = [b for b in ALL_BLOCKS if b.lang in {"python", "py", "pycon"}]
JSON_BLOCKS = [b for b in ALL_BLOCKS if b.lang == "json"]


def _parse(block: Block) -> ast.Module:
    return compile(
        block.code, str(block), "exec",
        flags=ast.PyCF_ONLY_AST | ast.PyCF_ALLOW_TOP_LEVEL_AWAIT,
        dont_inherit=True,
    )


def _tree(block: Block) -> ast.Module:
    """문법 오류는 test_python_block_compiles 가 한 번만 알린다."""
    try:
        return _parse(block)
    except SyntaxError:
        pytest.skip("문법 오류 — test_python_block_compiles 참고")


def test_blocks_were_found():
    """수집이 조용히 0건이 되면 아래 검사가 전부 공짜로 통과한다."""
    assert len(PY_BLOCKS) >= 10


@pytest.mark.parametrize("block", PY_BLOCKS, ids=str)
def test_python_block_compiles(block):
    try:
        _parse(block)
    except SyntaxError as exc:
        pytest.fail(f"{block}: 문법 오류 — {exc}")


@pytest.mark.parametrize("block", JSON_BLOCKS, ids=str)
def test_json_block_parses(block):
    try:
        json.loads(block.code)
    except json.JSONDecodeError as exc:
        pytest.fail(f"{block}: JSON 오류 — {exc}")


def _module_methods() -> dict[str, set[str]]:
    registry: ModuleRegistry = ModuleRegistry()
    registry._client = object()  # type: ignore[assignment]
    registry._init_modules()
    out = {}
    for name in MODULE_NAMES:
        obj = getattr(registry, name)
        out[name] = {m for m in dir(obj) if not m.startswith("_")}
    # README 가 연속조회에 쓰는 저수준 클라이언트.
    out["_client"] = {m for m in dir(BaseClient) if not m.startswith("_")}
    return out


_METHODS = _module_methods()
_FACADE = {m for m in dir(KiwoomAPI) if not m.startswith("_")}
_FACADE |= {m for m in dir(AsyncKiwoomAPI) if not m.startswith("_")}
_WS = {m for m in dir(KiwoomWebSocket) if not m.startswith("_")}


def _attribute_calls(tree: ast.AST):
    """``api.x.y(...)`` → ("api", "x", "y"), ``api.x(...)`` → ("api", "x")."""
    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue
        parts: list[str] = []
        func = node.func
        while isinstance(func, ast.Attribute):
            parts.append(func.attr)
            func = func.value
        if isinstance(func, ast.Name):
            parts.append(func.id)
            yield node, tuple(reversed(parts))


@pytest.mark.parametrize("block", PY_BLOCKS, ids=str)
def test_referenced_api_names_exist(block):
    tree = _tree(block)
    unknown = []
    for _, chain in _attribute_calls(tree):
        if chain[0] == "api" and len(chain) == 3:
            module, method = chain[1], chain[2]
            if module not in _METHODS or method not in _METHODS[module]:
                unknown.append(".".join(chain))
        elif chain[0] == "api" and len(chain) == 2:
            if chain[1] not in _FACADE and chain[1] not in _METHODS:
                unknown.append(".".join(chain))
        elif chain[0] == "ws" and len(chain) == 2 and chain[1] not in _WS:
            unknown.append(".".join(chain))
    assert not unknown, f"{block}: 없는 이름을 부릅니다 — {unknown}"


@pytest.mark.parametrize("block", PY_BLOCKS, ids=str)
def test_imports_from_kiwoom_client_exist(block):
    tree = _tree(block)
    missing = []
    for node in ast.walk(tree):
        if not isinstance(node, ast.ImportFrom) or not node.module:
            continue
        if node.module.split(".")[0] != "kiwoom_client":
            continue
        module = importlib.import_module(node.module)
        missing += [
            f"{node.module}.{alias.name}"
            for alias in node.names
            if alias.name != "*" and not hasattr(module, alias.name)
        ]
    assert not missing, f"{block}: 없는 이름을 import 합니다 — {missing}"


def _is_mock_true(call: ast.Call) -> bool:
    for kw in call.keywords:
        if kw.arg == "is_mock":
            return isinstance(kw.value, ast.Constant) and kw.value.value is True
    return False


@pytest.mark.parametrize(
    "block", [b for b in PY_BLOCKS if b.path.startswith(_MOCK_ONLY_PREFIXES)], ids=str
)
def test_examples_construct_clients_in_mock_mode(block):
    tree = _tree(block)
    live = []
    for node in ast.walk(tree):
        if (
            isinstance(node, ast.Call)
            and isinstance(node.func, ast.Name)
            and node.func.id in {"KiwoomAPI", "AsyncKiwoomAPI"}
            and not _is_mock_true(node)
        ) or (
            isinstance(node, ast.Call)
            and isinstance(node.func, ast.Attribute)
            and node.func.attr == "from_env"
            and isinstance(node.func.value, ast.Name)
            and node.func.value.id in {"KiwoomAPI", "AsyncKiwoomAPI"}
            and not _is_mock_true(node)
        ):
            live.append(f"line {block.line + node.lineno - 1}")
    assert not live, (
        f"{block}: KiwoomAPI/AsyncKiwoomAPI 는 is_mock=True 로 만들어야 합니다 "
        f"(기본값은 실서버) — {live}"
    )


_INLINE_CALL = re.compile(r"\bapi\.([a-z_]+)\.([a-z_0-9]+)\(")
_API_ID = re.compile(r"\bk[at]\d{5}\b")


def _known_api_ids() -> set[str]:
    from kiwoom_client import spec

    ids = set(spec.api_ids())
    registry: ModuleRegistry = ModuleRegistry()

    class _Recorder:
        def request(self, url, api_id, *args, **kwargs):
            return api_id

    registry._client = _Recorder()  # type: ignore[assignment]
    registry._init_modules()
    for name in MODULE_NAMES:
        if name == "condition_search":
            continue
        obj = getattr(registry, name)
        methods = [getattr(obj, m) for m in dir(obj) if not m.startswith("_")]
        ids |= {fn() for fn in methods if callable(fn)}
    return ids


_KNOWN_IDS = _known_api_ids()
DOC_PATHS = [f.relative_to(ROOT).as_posix() for f in doc_files()]


@pytest.mark.parametrize("rel", DOC_PATHS)
def test_inline_method_references_exist(rel):
    text = (ROOT / rel).read_text(encoding="utf-8")
    unknown = sorted({
        f"api.{m}.{f}" for m, f in _INLINE_CALL.findall(text)
        if m not in _METHODS or f not in _METHODS[m]
    })
    assert not unknown, f"{rel}: 없는 메서드를 가리킵니다 — {unknown}"


@pytest.mark.parametrize("rel", DOC_PATHS)
def test_api_ids_in_docs_exist(rel):
    text = (ROOT / rel).read_text(encoding="utf-8")
    unknown = sorted(set(_API_ID.findall(text)) - _KNOWN_IDS)
    assert not unknown, f"{rel}: 라이브러리·공식 카탈로그에 없는 api_id — {unknown}"
