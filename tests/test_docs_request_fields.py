"""문서·예제의 요청 필드가 TR 카탈로그(키움 공식 명세)와 맞는지 본다.

``api.<모듈>.<메서드>(필드=...)`` 호출의 키워드 인자를 ``kiwoom_client.spec`` 과 대조한다.

1. 없는 필드명 — README 의 순위 예제가 공식 명세에 없는 필드명을 쓰고 있던 것을 이 검사로 찾았다.
2. 빠진 필수 필드 — 일봉 예제들이 ``upd_stkpc_tp``(수정주가구분)를 빼먹고 있었다. 복사해 돌리면
   서버가 거절하거나 다른 데이터를 준다. 자리표시 호출(``api.x.y(...)``)과 ``**fields`` 로 넘기는
   호출은 필드를 다 볼 수 없어 이 검사에서 뺀다.

대상: 문서의 ```python 블록(``test_docs_code_blocks`` 와 같은 목록) + ``examples/*.py``.
블록 하나를 빼려면 바로 위에 ``<!-- docs-test: skip -->``.
"""

from __future__ import annotations

import ast

import pytest

from kiwoom_client import spec
from kiwoom_client.spec.validation import check_params
from tests.test_docs_code_blocks import PY_BLOCKS, ROOT, Block, _attribute_calls, _tree

_PAGING = {"cont_yn", "next_key"}

EXAMPLE_FILES = [
    Block(p.relative_to(ROOT).as_posix(), 1, "python", p.read_text(encoding="utf-8"))
    for p in sorted((ROOT / "examples").glob("*.py"))
]
CHECKED = PY_BLOCKS + EXAMPLE_FILES


def _is_placeholder(node: ast.Call) -> bool:
    """``api.x.y(...)`` 나 ``api.x.y(**fields)`` — 필드 전체가 글에 드러나지 않은 호출."""
    return bool(node.args) or any(kw.arg is None for kw in node.keywords)


def _calls_with_fields(block):
    for node, chain in _attribute_calls(_tree(block)):
        if chain[0] != "api" or len(chain) != 3:
            continue
        try:
            tr = spec.for_method(chain[1], chain[2])
        except KeyError:
            continue  # 엔드포인트 메서드가 아님 (이름 검사는 test_docs_code_blocks)
        fields = {kw.arg: "" for kw in node.keywords if kw.arg and kw.arg not in _PAGING}
        line = block.line + node.lineno - 1
        yield line, ".".join(chain), tr.api_id, fields, _is_placeholder(node)


def _problems(block, kind):
    bad = []
    for line, call, api_id, fields, placeholder in _calls_with_fields(block):
        if kind == "missing" and placeholder:
            continue
        if kind == "unknown" and not fields:
            continue
        for problem in check_params(api_id, fields):
            if problem.kind == kind:
                bad.append(f"line {line} {call} ({api_id}): {problem}")
    return bad


@pytest.mark.parametrize("block", CHECKED, ids=str)
def test_example_request_fields_exist_in_catalog(block):
    bad = _problems(block, "unknown")
    assert not bad, f"{block}: 공식 명세에 없는 요청 필드 —\n" + "\n".join(bad)


@pytest.mark.parametrize("block", CHECKED, ids=str)
def test_example_requests_have_required_fields(block):
    bad = _problems(block, "missing")
    head = f"{block}: 공식 명세의 필수 요청 필드가 빠졌다 (api.describe(api_id) 로 확인) —\n"
    assert not bad, head + "\n".join(bad)


def test_some_examples_were_checked():
    assert sum(1 for b in CHECKED for c in _calls_with_fields(b) if c[3]) >= 10
    assert EXAMPLE_FILES, "examples/*.py 를 못 찾았다"


def test_placeholder_calls_are_recognized():
    tree = ast.parse(
        "api.ranking.top_volume_today(...)\napi.chart.stock_daily_chart(**f)\napi.a.b(x='1')"
    )
    calls = [n for n in ast.walk(tree) if isinstance(n, ast.Call)]
    assert [_is_placeholder(c) for c in calls] == [True, True, False]
