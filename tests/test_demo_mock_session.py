"""README 데모 GIF 의 원본(scripts/demo_mock_session.py)이 지금 코드로 같은 흐름을 내는지.

GIF 는 이 스크립트 출력을 그대로 녹화한 것이다
(데모 모드: 포트폴리오 요약 → 리밸런싱 계산 → 주문 미리보기).
도구 이름·인자·응답 필드가 바뀌면 여기서 깨지고, 그때 GIF 를 다시 만든다
(스크립트 docstring 의 명령).
데모 시세는 날짜마다 달라지므로 값이 아니라 흐름과 표시를 본다.
"""

from __future__ import annotations

import importlib.util
from pathlib import Path

import pytest

from tests.demo_support import no_network  # noqa: F401

SCRIPT = Path(__file__).resolve().parent.parent / "scripts" / "demo_mock_session.py"


def _load():
    spec = importlib.util.spec_from_file_location("demo_mock_session", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


@pytest.mark.usefixtures("no_network")
async def test_demo_session_output(capsys):
    demo = _load()
    rec = demo.Recorder()
    results = await demo.run(rec)
    out = capsys.readouterr().out

    assert [tool for _u, tool, *_ in demo.SESSION] == [
        "get_portfolio",
        "rebalance_plan",
        "order_preview",
    ]
    assert "[데모]" in out and "kiwoom-client-mcp --demo" in out
    assert out.count('"_demo": "가상 데이터') == 3  # every tool result shows the marker

    assert results["get_portfolio"]["holdings"]
    plan = results["rebalance_plan"]
    assert plan["sent"] is False
    assert plan["orders"][0]["action"] == "sell" and plan["orders"][0]["name"] == "카카오"

    preview = results["order_preview"]
    assert preview["sent"] is False and preview["would_call"] == "order_sell_order"
    assert not preview.get("errors") and preview["confirm_token"]
    assert "아직 주문은 나가지 않았습니다" in out
    assert rec.events and rec.events[-1][0] > 10  # 녹화용 타임라인
