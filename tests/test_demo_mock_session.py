"""README 모의 데모 GIF 의 원본(scripts/demo_mock_session.py)이 지금 코드로 같은 화면을 내는지.

GIF 는 이 스크립트 출력을 그대로 녹화한 것이다. 도구 이름·인자·응답 필드가 바뀌면 여기서 깨지고,
그때 GIF 를 다시 만든다(스크립트 docstring 의 명령).
"""

from __future__ import annotations

import importlib.util
from pathlib import Path

import httpx

SCRIPT = Path(__file__).resolve().parent.parent / "scripts" / "demo_mock_session.py"


def _load():
    spec = importlib.util.spec_from_file_location("demo_mock_session", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


async def test_demo_session_output(capsys):
    demo = _load()
    real = httpx.AsyncClient
    rec = demo.Recorder()
    await demo.run(rec)
    assert httpx.AsyncClient is real  # 가짜 전송은 데모 클라이언트에만
    out = capsys.readouterr().out
    assert "[MOCK DEMO]" in out
    assert '"price": 70100' in out and '"price": 181500' in out
    assert '"sent": false' in out and '"adjusted": "70000"' in out
    assert '"orderable_qty": 142' in out and "confirm_token" in out
    assert "not faked" not in out
    assert rec.events and rec.events[-1][0] > 10  # 녹화용 타임라인
