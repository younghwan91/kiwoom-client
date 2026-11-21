"""docs/cookbook/ 의 REST 예제를 실제로 실행해 본다 — 공식 스펙으로 만든 가짜 응답에 대고.

문법·이름 검사(test_docs_code_blocks.py)로는 ``KeyError``·잘못된 pandas 호출 같은
실행 오류를 못 잡는다.
여기서는 페이지마다 python 블록을 위에서부터 한 이름공간에서 돌리고, HTTP 는 pytest-httpx 가 받아
``kiwoom_client.spec`` 의 응답 필드 정의대로 채운 JSON 을 돌려준다. 네트워크·실키는 쓰지 않는다.

- WebSocket 을 여는 블록(``create_websocket``)은 실행하지 않는다 — 문법·이름 검사만.
- 실행에서 빼려면 블록 바로 위 줄에 ``<!-- docs-test: no-exec -->``
  (예: 추가 패키지가 필요한 저장 예제).
"""

from __future__ import annotations

import json
import re
import textwrap
from pathlib import Path

import httpx
import pytest

from kiwoom_client import rate_limiter, spec

ROOT = Path(__file__).resolve().parent.parent
COOKBOOK = ROOT / "docs" / "cookbook"

_FENCE = re.compile(r"^\s*```(?P<lang>\w*)\s*$")
_NO_EXEC = {"<!-- docs-test: no-exec -->", "<!-- docs-test: skip -->"}


def runnable_blocks(path: Path) -> list[tuple[int, str]]:
    lines = path.read_text(encoding="utf-8").splitlines()
    out, i = [], 0
    while i < len(lines):
        m = _FENCE.match(lines[i])
        if not m or not m.group("lang"):
            i += 1
            continue
        j = i + 1
        while j < len(lines) and not lines[j].strip().startswith("```"):
            j += 1
        code = textwrap.dedent("\n".join(lines[i + 1 : j]))
        marked = i > 0 and lines[i - 1].strip() in _NO_EXEC
        if m.group("lang") == "python" and not marked and "create_websocket" not in code:
            out.append((i + 2, code))
        i = j + 1
    return out


PAGES = [p for p in sorted(COOKBOOK.glob("*.md")) if runnable_blocks(p)]


def _value(field_id: str, row: int) -> str:
    """필드 이름으로 그럴듯한 문자열 값. 날짜는 행마다 하루씩 과거로."""
    fid = field_id.lower()
    if fid in {"dt", "date"} or fid.endswith(("_dt", "_date")):
        return f"202603{26 - row:02d}"
    if fid in {"stk_cd", "code"} or fid.endswith("_cd"):
        return "005930"
    if fid.endswith(("_nm", "name")) or fid == "nm":
        return "삼성전자"
    if fid.endswith("_no"):
        return f"{row + 1:07d}"
    if fid.endswith(("_rt", "_ratio")):
        return "+1.25"
    return "+1000"


def _fake_body(api_id: str) -> dict:
    """공식 스펙의 응답 필드로 채운 본문. list 필드는 레코드 3개."""
    tr = spec.get(api_id)
    body: dict = {"return_code": 0, "return_msg": ""}
    children: dict[str, list] = {}
    for f in tr.response:
        if f.parent is not None:
            children.setdefault(f.parent, []).append(f)
    for f in tr.response:
        if f.parent is not None:
            continue
        if f.type == "list":
            kids = children.get(f.id, [])
            body[f.id] = [{k.id: _value(k.id, row) for k in kids} for row in range(3)]
        elif f.type == "object":
            body[f.id] = {k.id: _value(k.id, 0) for k in children.get(f.id, [])}
        else:
            body[f.id] = _value(f.id, 0)
    return body


@pytest.fixture
def fake_kiwoom(httpx_mock, monkeypatch, tmp_path):
    monkeypatch.setenv("KIWOOM_APP_KEY", "test-key")
    monkeypatch.setenv("KIWOOM_APP_SECRET", "test-secret")
    monkeypatch.setenv("KIWOOM_IS_MOCK", "true")
    monkeypatch.chdir(tmp_path)  # 예제가 파일을 쓰면 여기에
    # 같은 TR 을 여러 번 부르는 예제가 Rate Limiter 때문에 몇 초씩 걸리지 않게.
    monkeypatch.setattr(rate_limiter.RateLimiter, "acquire", lambda self: None)

    async def _no_wait(self):
        return None

    monkeypatch.setattr(rate_limiter.AsyncRateLimiter, "acquire", _no_wait)

    calls: list[str] = []

    def respond(request: httpx.Request) -> httpx.Response:
        assert request.url.host == "mockapi.kiwoom.com", "예제는 모의투자 서버만 불러야 한다"
        if request.url.path == "/oauth2/token":
            return httpx.Response(200, json={
                "return_code": 0, "token": "fake-token", "token_type": "bearer",
                "expires_dt": "20991231235959",
            })
        api_id = request.headers["api-id"]
        calls.append(api_id)
        return httpx.Response(
            200, json=_fake_body(api_id), headers={"cont-yn": "N", "next-key": ""},
        )

    httpx_mock.add_callback(respond, is_reusable=True, is_optional=True)
    return calls


def test_pages_were_found():
    assert len(PAGES) >= 5


@pytest.mark.parametrize("page", PAGES, ids=lambda p: p.name)
def test_cookbook_page_runs(page, fake_kiwoom):
    namespace: dict = {"__name__": "__cookbook__"}
    for line, code in runnable_blocks(page):
        try:
            exec(compile(code, f"{page.relative_to(ROOT)}:{line}", "exec"), namespace)
        except Exception as exc:  # pragma: no cover - 실패 메시지용
            pytest.fail(f"{page.name}:{line} 실행 실패 — {type(exc).__name__}: {exc}")
    assert fake_kiwoom, f"{page.name}: 키움 API 를 한 번도 부르지 않았다"


def test_fake_body_follows_spec_shape():
    body = _fake_body("ka10081")
    assert isinstance(body["stk_dt_pole_chart_qry"], list)
    assert {"dt", "cur_prc"} <= set(body["stk_dt_pole_chart_qry"][0])
    json.dumps(body)
