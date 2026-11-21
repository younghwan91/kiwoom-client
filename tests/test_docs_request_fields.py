"""문서 예제의 요청 필드명이 TR 카탈로그(키움 공식 명세)에 있는지 본다.

``api.<모듈>.<메서드>(필드=...)`` 호출의 키워드 인자를 ``kiwoom_client.spec`` 과 대조한다.
예제는 필드를 일부만 보여 줄 수 있어 **빠진 필수 필드는 보지 않고**, 없는 필드명만 잡는다
(README 의 순위 예제가 공식 명세에 없는 필드명을 쓰고 있던 것을 이 검사로 찾았다).
블록 하나를 빼려면 바로 위에 ``<!-- docs-test: skip -->``.
"""

from __future__ import annotations

import pytest

from kiwoom_client import spec
from kiwoom_client.spec.validation import check_params
from tests.test_docs_code_blocks import PY_BLOCKS, _attribute_calls, _tree

_PAGING = {"cont_yn", "next_key"}


def _calls_with_fields(block):
    for node, chain in _attribute_calls(_tree(block)):
        if chain[0] != "api" or len(chain) != 3:
            continue
        try:
            tr = spec.for_method(chain[1], chain[2])
        except KeyError:
            continue  # 엔드포인트 메서드가 아님 (이름 검사는 test_docs_code_blocks)
        fields = {kw.arg: "" for kw in node.keywords if kw.arg and kw.arg not in _PAGING}
        if fields:
            yield block.line + node.lineno - 1, ".".join(chain), tr.api_id, fields


@pytest.mark.parametrize("block", PY_BLOCKS, ids=str)
def test_example_request_fields_exist_in_catalog(block):
    bad = []
    for line, call, api_id, fields in _calls_with_fields(block):
        for problem in check_params(api_id, fields):
            if problem.kind == "unknown":
                bad.append(f"line {line} {call} ({api_id}): {problem}")
    assert not bad, f"{block}: 공식 명세에 없는 요청 필드 —\n" + "\n".join(bad)


def test_some_examples_were_checked():
    assert sum(1 for b in PY_BLOCKS for _ in _calls_with_fields(b)) >= 10
