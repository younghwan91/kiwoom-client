"""examples/*.py 를 **실행하지 않고** 정적으로 검사한다.

레포 규칙(CLAUDE.md "실계좌 위험"): 예제는 전부 모의투자(``is_mock=True``)로만 돈다.
라이브러리 기본값은 ``is_mock=False`` = 실서버라, 예제에서 이 인자가 빠지거나 바뀌면 예제를
따라 한 사용자의 주문이 실계좌로 나간다. 사람의 리뷰 대신 이 테스트가 그 규칙을 지킨다.
"""

from __future__ import annotations

import ast
from pathlib import Path

import pytest

EXAMPLES_DIR = Path(__file__).resolve().parent.parent / "examples"
EXAMPLES = sorted(EXAMPLES_DIR.glob("*.py"))

#: 서버를 고르는 생성자·팩토리. 전부 ``is_mock`` 를 받고 기본은 실서버다.
CLIENT_CLASSES = {"KiwoomAPI", "AsyncKiwoomAPI", "KiwoomWebSocket"}
CLIENT_FACTORIES = {"from_env"}

LIVE_HOSTS = ("://api.kiwoom.com", "://api.kiwoom.com:")


def _call_name(node: ast.Call) -> tuple[str | None, str | None]:
    """``Foo(...)`` → (None, "Foo"), ``Foo.bar(...)`` → ("Foo", "bar")."""
    func = node.func
    if isinstance(func, ast.Name):
        return None, func.id
    if isinstance(func, ast.Attribute):
        owner = func.value.id if isinstance(func.value, ast.Name) else None
        return owner, func.attr
    return None, None


def _client_calls(tree: ast.AST) -> list[ast.Call]:
    calls = []
    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue
        owner, name = _call_name(node)
        is_ctor = owner is None and name in CLIENT_CLASSES
        is_factory = owner in CLIENT_CLASSES and name in CLIENT_FACTORIES
        if is_ctor or is_factory:
            calls.append(node)
    return calls


def _is_mock_true(call: ast.Call) -> bool:
    for kw in call.keywords:
        if kw.arg == "is_mock":
            return isinstance(kw.value, ast.Constant) and kw.value.value is True
    return False


def test_examples_exist():
    assert EXAMPLES, f"{EXAMPLES_DIR} 에 예제가 없다"


@pytest.mark.parametrize("path", EXAMPLES, ids=lambda p: p.name)
def test_example_compiles(path: Path):
    source = path.read_text(encoding="utf-8")
    compile(source, str(path), "exec")


@pytest.mark.parametrize("path", EXAMPLES, ids=lambda p: p.name)
def test_example_clients_are_mock_only(path: Path):
    tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    bad = [
        f"{path.name}:{call.lineno} {ast.unparse(call.func)}(...)"
        for call in _client_calls(tree)
        if not _is_mock_true(call)
    ]
    assert not bad, (
        "예제의 클라이언트는 전부 is_mock=True 리터럴로 만들어야 한다 "
        "(기본값은 실서버): " + ", ".join(bad)
    )


@pytest.mark.parametrize("path", EXAMPLES, ids=lambda p: p.name)
def test_example_has_no_live_host(path: Path):
    tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    hits = [
        f"{path.name}:{node.lineno}"
        for node in ast.walk(tree)
        if isinstance(node, ast.Constant)
        and isinstance(node.value, str)
        and any(h in node.value for h in LIVE_HOSTS)
    ]
    assert not hits, "예제에 실서버 주소가 들어 있다: " + ", ".join(hits)


def test_every_client_example_is_checked():
    """API 를 쓰는 예제는 클라이언트를 직접 만든다 — 다른 경로로 만들면 위 검사가 눈이 먼다."""
    blind = []
    for path in EXAMPLES:
        source = path.read_text(encoding="utf-8")
        if "kiwoom_client" in source and not _client_calls(ast.parse(source)):
            blind.append(path.name)
    assert not blind, (
        f"kiwoom_client 를 쓰지만 검사할 클라이언트 생성이 없는 예제: {blind} — "
        "CLIENT_CLASSES/CLIENT_FACTORIES 를 늘려라"
    )


# ── 검사기 자체가 잡는지 (가짜 소스로) ───────────────────────────────────────


@pytest.mark.parametrize(
    "src",
    [
        "KiwoomAPI('k', 's')",
        "KiwoomAPI('k', 's', is_mock=False)",
        "AsyncKiwoomAPI(app_key='k', app_secret='s', is_mock=flag)",
        "KiwoomAPI.from_env()",
        "KiwoomWebSocket(token)",
    ],
)
def test_checker_flags_live_clients(src: str):
    calls = _client_calls(ast.parse(src))
    assert calls and not all(_is_mock_true(c) for c in calls)


@pytest.mark.parametrize(
    "src",
    [
        "KiwoomAPI('k', 's', is_mock=True)",
        "AsyncKiwoomAPI.from_env(is_mock=True)",
        "KiwoomWebSocket(token, is_mock=True)",
    ],
)
def test_checker_accepts_mock_clients(src: str):
    calls = _client_calls(ast.parse(src))
    assert calls and all(_is_mock_true(c) for c in calls)
