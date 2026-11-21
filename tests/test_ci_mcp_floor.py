"""CI 의 최저 mcp 잡(test-mcp-min)이 pyproject 의 ``[mcp]`` 하한과 같은 버전을 까는지 본다.

하한만 올리고 CI 핀을 그대로 두면, 실제로는 지원하지 않는 옛 mcp 를 계속 시험하거나
(반대로 핀만 올리면) 하한 버전이 시험되지 않는다.
"""

from __future__ import annotations

import re
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent


def _floor() -> tuple[int, ...]:
    # tomllib 은 3.11+ 라 3.10 CI 를 위해 글자로 읽는다: [mcp] extra 의 "mcp>=X,<Y".
    text = (ROOT / "pyproject.toml").read_text(encoding="utf-8")
    m = re.search(r'^mcp\s*=\s*\[\s*"mcp\s*>=\s*([\d.]+)', text, flags=re.M)
    assert m, "pyproject 의 [mcp] extra 에 mcp 하한(>=)이 없다"
    return tuple(int(x) for x in m.group(1).split("."))


def _norm(v: tuple[int, ...]) -> tuple[int, ...]:
    return (*v, 0, 0, 0)[:3]


def test_ci_pins_the_mcp_floor():
    ci = (ROOT / ".github" / "workflows" / "ci.yml").read_text(encoding="utf-8")
    pins = re.findall(r'^\s*MCP_MIN:\s*"([\d.]+)"', ci, flags=re.M)
    if len(pins) != 1:
        pytest.fail(f'ci.yml 에 최저 mcp 잡의 MCP_MIN: "X" 가 하나여야 한다 (찾은 것: {pins})')
    assert '--with "mcp==$MCP_MIN"' in ci, "최저 mcp 잡이 MCP_MIN 을 쓰지 않는다"
    (pin,) = pins
    assert _norm(tuple(int(x) for x in pin.split("."))) == _norm(_floor())
