# MCP 서버 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** `kiwoom-client`에 stdio MCP 서버를 추가해, 15개 도메인 모듈의 REST 엔드포인트 전부와 condition_search(WebSocket) 4종을 Claude Code/Cursor 등에서 도구로 직접 호출할 수 있게 한다.

**Architecture:** `ModuleRegistry.MODULE_NAMES`를 리플렉션으로 훑어 REST 도구 스펙을 동적 생성하고(하드코딩 없음), `AsyncKiwoomAPI` 인스턴스 하나로 실제 호출을 디스패치한다. condition_search는 WebSocket 요청/응답을 trnm+seq로 상관시키는 별도 세션 객체로 감싸 같은 도구 인터페이스에 맞춘다. 주문/신용주문 도구는 실전투자일 때 환경변수 opt-in이 없으면 도구 목록 자체에서 제외된다.

**Tech Stack:** Python 3.10+, `mcp>=1.0`(MCP Python SDK, stdio), 기존 `AsyncKiwoomAPI`/`KiwoomWebSocket`, pytest/pytest-asyncio/pytest-httpx(기존 테스트 스택 재사용).

**Spec:** `docs/superpowers/specs/2026-09-07-mcp-server-design.md`

## Global Constraints

- 기존 15개 도메인 모듈(`src/kiwoom_client/domestic/*.py`)과 `_registry.py`는 수정하지 않는다 — MCP 서버는 순수 추가(additive) 레이어.
- REST 도구의 TR 필드를 손으로 나열하지 않는다 — `inspect`로 얻은 메서드 목록만 사용한다.
- 주문 계열(`order`, `credit_order` 모듈) 도구는 `is_mock=False`이고 `KIWOOM_MCP_ALLOW_LIVE_ORDERS`가 `"true"`(대소문자 무관)가 아니면 도구 목록에서 제외한다. 모의투자(`is_mock=True`)는 항상 포함한다.
- condition_search 응답 대기 타임아웃은 15초.
- 신규 의존성은 `mcp` extra로만 추가한다 — 기본 설치(`pip install kiwoom-client`)에는 영향 없음.

---

## 파일 구조

```
src/kiwoom_client/mcp/
    __init__.py                    # 빈 마커 (패키지 표시용)
    tools.py                       # REST 엔드포인트 리플렉션 스캔 → RestToolSpec 목록
    guard.py                       # 실주문 opt-in 가드
    condition_search_session.py    # WebSocket 요청/응답 상관 (trnm/seq)
    server.py                      # MCP Server 조립, 도구 등록/디스패치, main()
tests/
    test_mcp_tools.py
    test_mcp_guard.py
    test_mcp_condition_search_session.py
    test_mcp_server.py
```

---

### Task 1: 패키지 배포 설정 (`mcp` extra, 콘솔 스크립트, keywords)

**Files:**
- Modify: `pyproject.toml`
- Create: `src/kiwoom_client/mcp/__init__.py`

**Interfaces:**
- Produces: `kiwoom-client-mcp` 콘솔 스크립트(엔트리포인트 `kiwoom_client.mcp.server:main` — Task 5에서 정의)가 참조할 모듈 경로.

- [ ] **Step 1: `src/kiwoom_client/mcp/__init__.py` 생성**

```python
"""MCP (Model Context Protocol) stdio server for the Kiwoom REST API."""
```

- [ ] **Step 2: `pyproject.toml`에 `mcp` extra 추가**

`pyproject.toml`의 `[project.optional-dependencies]` 블록(현재 `pandas = [...]`, `dev = [...]`가 있는 곳)에 아래를 추가:

```toml
mcp = [
    "mcp>=1.0",
]
```

- [ ] **Step 3: `[project.scripts]` 섹션 추가**

`[project.urls]` 섹션 바로 앞에 아래 섹션을 새로 추가:

```toml
[project.scripts]
kiwoom-client-mcp = "kiwoom_client.mcp.server:main"
```

- [ ] **Step 4: `keywords`에 MCP 관련 태그 추가**

`pyproject.toml`의 `keywords` 리스트 끝(`"자동주문",` 다음)에 추가:

```toml
    "mcp", "model-context-protocol", "ai-agents", "claude-code", "cursor",
```

- [ ] **Step 5: 설치 확인**

Run: `uv pip install -e '.[mcp,dev]'` (또는 `pip install -e '.[mcp,dev]'`)
Expected: `mcp` 패키지가 설치되고 에러 없이 끝난다.

- [ ] **Step 6: Commit**

```bash
git add pyproject.toml src/kiwoom_client/mcp/__init__.py
git commit -m "$(cat <<'EOF'
build: MCP 서버용 mcp extra·콘솔 스크립트 추가

Co-Authored-By: Claude Sonnet 5 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_019bMMMry1G4gSG6VSnkay27
EOF
)"
```

---

### Task 2: REST 엔드포인트 리플렉션 스캔 (`tools.py`)

**Files:**
- Create: `src/kiwoom_client/mcp/tools.py`
- Test: `tests/test_mcp_tools.py`

**Interfaces:**
- Consumes: `kiwoom_client._registry.MODULE_NAMES`(튜플), `kiwoom_client._registry.ModuleRegistry`(생성자 인자 없음, `_client`/`_init_modules()`로 초기화).
- Produces:
  - `@dataclass(frozen=True) class RestToolSpec`: 필드 `module_name: str`, `method_name: str`, `tool_name: str`, `description: str`, `guarded: bool`.
  - `def discover_rest_tools() -> list[RestToolSpec]` — condition_search를 제외한 14개 모듈의 public 메서드를 전부 스캔해 반환.
  - `GUARDED_MODULES: frozenset[str]` — `{"order", "credit_order"}`.

- [ ] **Step 1: 실패하는 테스트 작성**

`tests/test_mcp_tools.py`:

```python
"""Tests for reflection-based REST tool discovery."""

from __future__ import annotations

import inspect

from kiwoom_client._registry import MODULE_NAMES, ModuleRegistry
from kiwoom_client.mcp.tools import GUARDED_MODULES, RestToolSpec, discover_rest_tools


def _expected_method_count() -> int:
    """condition_search 를 제외한 14개 모듈의 public 메서드 총합."""
    registry = ModuleRegistry()
    registry._client = object()
    registry._init_modules()
    total = 0
    for name in MODULE_NAMES:
        if name == "condition_search":
            continue
        module_obj = getattr(registry, name)
        total += sum(
            1
            for method_name, _ in inspect.getmembers(module_obj, inspect.ismethod)
            if not method_name.startswith("_")
        )
    return total


class TestDiscoverRestTools:
    def test_covers_every_public_method(self):
        specs = discover_rest_tools()
        assert len(specs) == _expected_method_count()

    def test_excludes_condition_search(self):
        specs = discover_rest_tools()
        assert all(spec.module_name != "condition_search" for spec in specs)

    def test_tool_name_is_module_underscore_method(self):
        specs = discover_rest_tools()
        by_name = {spec.tool_name: spec for spec in specs}
        assert "order_buy_order" in by_name
        spec = by_name["order_buy_order"]
        assert spec.module_name == "order"
        assert spec.method_name == "buy_order"

    def test_description_comes_from_docstring(self):
        specs = discover_rest_tools()
        buy = next(s for s in specs if s.tool_name == "order_buy_order")
        assert "매수" in buy.description

    def test_order_and_credit_order_are_guarded(self):
        specs = discover_rest_tools()
        for spec in specs:
            assert spec.guarded == (spec.module_name in GUARDED_MODULES)

    def test_guarded_modules_is_order_and_credit_order(self):
        assert GUARDED_MODULES == frozenset({"order", "credit_order"})

    def test_returns_rest_tool_spec_instances(self):
        specs = discover_rest_tools()
        assert all(isinstance(spec, RestToolSpec) for spec in specs)
```

- [ ] **Step 2: 테스트가 실패하는지 확인**

Run: `pytest tests/test_mcp_tools.py -v`
Expected: FAIL — `ModuleNotFoundError: No module named 'kiwoom_client.mcp.tools'`

- [ ] **Step 3: `src/kiwoom_client/mcp/tools.py` 구현**

```python
"""Reflection-based discovery of MCP tools from the REST endpoint modules.

Every public method on the 15 endpoint modules follows the same signature —
``(self, cont_yn="N", next_key="", **kwargs)`` — so no per-endpoint mapping is
maintained here; the module list comes straight from
:data:`kiwoom_client._registry.MODULE_NAMES`.
"""

from __future__ import annotations

import inspect
from dataclasses import dataclass

from kiwoom_client._registry import MODULE_NAMES, ModuleRegistry

#: Modules whose methods place live orders. Gated by the opt-in guard in
#: :mod:`kiwoom_client.mcp.guard` when the client is not in mock mode.
GUARDED_MODULES: frozenset[str] = frozenset({"order", "credit_order"})

#: condition_search rides the WebSocket, not REST — handled separately by
#: :mod:`kiwoom_client.mcp.condition_search_session`.
_SKIP_MODULES = frozenset({"condition_search"})


@dataclass(frozen=True)
class RestToolSpec:
    """One discovered REST endpoint method, ready to become an MCP tool."""

    module_name: str
    method_name: str
    tool_name: str
    description: str
    guarded: bool


def discover_rest_tools() -> list[RestToolSpec]:
    """Scan the REST endpoint modules and list their public methods.

    A throwaway ``ModuleRegistry`` (client=``object()``) is enough — module
    ``__init__`` only stores the client, it never calls it during discovery.
    """
    registry: ModuleRegistry = ModuleRegistry()
    registry._client = object()  # type: ignore[assignment]
    registry._init_modules()

    specs: list[RestToolSpec] = []
    for module_name in MODULE_NAMES:
        if module_name in _SKIP_MODULES:
            continue
        module_obj = getattr(registry, module_name)
        for method_name, method in inspect.getmembers(module_obj, inspect.ismethod):
            if method_name.startswith("_"):
                continue
            specs.append(
                RestToolSpec(
                    module_name=module_name,
                    method_name=method_name,
                    tool_name=f"{module_name}_{method_name}",
                    description=(inspect.getdoc(method) or "").strip(),
                    guarded=module_name in GUARDED_MODULES,
                )
            )
    return specs
```

- [ ] **Step 4: 테스트 통과 확인**

Run: `pytest tests/test_mcp_tools.py -v`
Expected: PASS (7 tests)

- [ ] **Step 5: Commit**

```bash
git add src/kiwoom_client/mcp/tools.py tests/test_mcp_tools.py
git commit -m "$(cat <<'EOF'
feat(mcp): REST 엔드포인트 리플렉션 스캔 추가

Co-Authored-By: Claude Sonnet 5 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_019bMMMry1G4gSG6VSnkay27
EOF
)"
```

---

### Task 3: 실주문 opt-in 가드 (`guard.py`)

**Files:**
- Create: `src/kiwoom_client/mcp/guard.py`
- Test: `tests/test_mcp_guard.py`

**Interfaces:**
- Produces:
  - `ENV_VAR: str` — `"KIWOOM_MCP_ALLOW_LIVE_ORDERS"`.
  - `def live_orders_allowed(*, is_mock: bool, env: dict[str, str] | None = None) -> bool`.

- [ ] **Step 1: 실패하는 테스트 작성**

`tests/test_mcp_guard.py`:

```python
"""Tests for the live-order opt-in guard."""

from __future__ import annotations

from kiwoom_client.mcp.guard import ENV_VAR, live_orders_allowed


class TestLiveOrdersAllowed:
    def test_mock_is_always_allowed_even_without_env(self):
        assert live_orders_allowed(is_mock=True, env={}) is True

    def test_live_without_env_is_blocked(self):
        assert live_orders_allowed(is_mock=False, env={}) is False

    def test_live_with_env_true_is_allowed(self):
        assert live_orders_allowed(is_mock=False, env={ENV_VAR: "true"}) is True

    def test_env_value_is_case_insensitive(self):
        assert live_orders_allowed(is_mock=False, env={ENV_VAR: "TRUE"}) is True

    def test_live_with_env_false_is_blocked(self):
        assert live_orders_allowed(is_mock=False, env={ENV_VAR: "false"}) is False

    def test_live_with_unrelated_env_value_is_blocked(self):
        assert live_orders_allowed(is_mock=False, env={ENV_VAR: "1"}) is False

    def test_env_defaults_to_os_environ(self, monkeypatch):
        monkeypatch.delenv(ENV_VAR, raising=False)
        assert live_orders_allowed(is_mock=False) is False
        monkeypatch.setenv(ENV_VAR, "true")
        assert live_orders_allowed(is_mock=False) is True
```

- [ ] **Step 2: 테스트 실패 확인**

Run: `pytest tests/test_mcp_guard.py -v`
Expected: FAIL — `ModuleNotFoundError: No module named 'kiwoom_client.mcp.guard'`

- [ ] **Step 3: `src/kiwoom_client/mcp/guard.py` 구현**

```python
"""Opt-in guard for live (실전투자) order tools on the MCP server.

Applies only to the MCP tool-registration path — direct use of
``KiwoomAPI``/``AsyncKiwoomAPI`` from Python code is never gated.
"""

from __future__ import annotations

import os

#: Set to "true" (case-insensitive) to register order/credit_order tools
#: when the server is running against a live (non-mock) account.
ENV_VAR = "KIWOOM_MCP_ALLOW_LIVE_ORDERS"


def live_orders_allowed(*, is_mock: bool, env: dict[str, str] | None = None) -> bool:
    """Whether guarded (order/credit_order) tools should be registered.

    Mock trading (``is_mock=True``) is always allowed — nothing actually
    executes. Live trading requires the opt-in environment variable.
    """
    if is_mock:
        return True
    source = os.environ if env is None else env
    return source.get(ENV_VAR, "").strip().lower() == "true"
```

- [ ] **Step 4: 테스트 통과 확인**

Run: `pytest tests/test_mcp_guard.py -v`
Expected: PASS (7 tests)

- [ ] **Step 5: Commit**

```bash
git add src/kiwoom_client/mcp/guard.py tests/test_mcp_guard.py
git commit -m "$(cat <<'EOF'
feat(mcp): 실주문 opt-in 가드 추가

Co-Authored-By: Claude Sonnet 5 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_019bMMMry1G4gSG6VSnkay27
EOF
)"
```

---

### Task 4: condition_search WebSocket 요청/응답 상관 (`condition_search_session.py`)

**Files:**
- Create: `src/kiwoom_client/mcp/condition_search_session.py`
- Test: `tests/test_mcp_condition_search_session.py`

**Interfaces:**
- Consumes: `kiwoom_client.websocket.KiwoomWebSocket`(`on_trnm(trnm, callback)`, `async send(payload)`, `async listen()` — 백그라운드 태스크로 돌려야 프레임 수신이 됨).
- Produces:
  - `class ConditionSearchSession`:
    - `__init__(self, connect: Callable[[], Awaitable[KiwoomWebSocket]])`.
    - `async def request(self, payload: dict[str, Any], *, expect_reply: bool = True) -> dict[str, Any] | None`.
  - `RESPONSE_TIMEOUT: float = 15.0`.
  - `class ConditionSearchTimeout(Exception)`.

- [ ] **Step 1: 실패하는 테스트 작성**

`tests/test_mcp_condition_search_session.py` — `tests/test_websocket.py`의 `FakeKiwoomServer` 패턴을 재사용해, CNSRLST/CNSRREQ/CNSRCLR 응답을 흉내내는 로컬 서버로 검증한다:

```python
"""Tests for ConditionSearchSession's WebSocket request/response correlation."""

from __future__ import annotations

import asyncio
import contextlib
import json

import pytest
import websockets

from kiwoom_client.mcp.condition_search_session import (
    ConditionSearchSession,
    ConditionSearchTimeout,
)
from kiwoom_client.websocket import KiwoomWebSocket


class FakeConditionServer:
    """LOGIN + CNSRLST/CNSRREQ/CNSRCLR 을 흉내내는 로컬 WebSocket 서버."""

    def __init__(self) -> None:
        self.received: list[dict] = []
        self._server: websockets.asyncio.server.Server | None = None
        self._conns: list = []

    async def __aenter__(self) -> "FakeConditionServer":
        self._server = await websockets.serve(self._handler, "127.0.0.1", 0)
        return self

    async def __aexit__(self, *args) -> None:
        assert self._server is not None
        self._server.close()
        await self._server.wait_closed()

    @property
    def url(self) -> str:
        assert self._server is not None
        host, port = self._server.sockets[0].getsockname()[:2]
        return f"ws://{host}:{port}"

    async def _handler(self, conn) -> None:
        self._conns.append(conn)
        try:
            async for raw in conn:
                msg = json.loads(raw)
                self.received.append(msg)
                if msg.get("trnm") == "LOGIN":
                    await conn.send(json.dumps({"trnm": "LOGIN", "return_code": 0, "return_msg": ""}))
                elif msg.get("trnm") == "CNSRLST":
                    await conn.send(json.dumps({
                        "trnm": "CNSRLST",
                        "data": [["0", "급등주 조건"], ["1", "거래량 급증"]],
                    }))
                elif msg.get("trnm") == "CNSRREQ":
                    await conn.send(json.dumps({
                        "trnm": "CNSRREQ", "seq": msg["seq"], "data": [{"jmcode": "005930"}],
                    }))
                # CNSRCLR: 키움 프로토콜상 ack 프레임 없음 — 응답하지 않는다.
        except websockets.ConnectionClosed:
            pass

    async def close_all_connections(self) -> None:
        for conn in list(self._conns):
            with contextlib.suppress(websockets.ConnectionClosed):
                await conn.close()


async def _connect(url: str) -> KiwoomWebSocket:
    ws = KiwoomWebSocket("tok-123", ws_url=url)
    await ws.connect()
    return ws


class TestConditionSearchSession:
    async def test_condition_list_returns_matching_reply(self):
        async with FakeConditionServer() as server:
            session = ConditionSearchSession(connect=lambda: _connect(server.url))
            result = await session.request({"trnm": "CNSRLST"})
            assert result["trnm"] == "CNSRLST"
            assert result["data"][0] == ["0", "급등주 조건"]

    async def test_condition_search_matches_by_seq(self):
        async with FakeConditionServer() as server:
            session = ConditionSearchSession(connect=lambda: _connect(server.url))
            result = await session.request(
                {"trnm": "CNSRREQ", "seq": "3", "search_type": "0", "stex_tp": "K",
                 "cont_yn": "N", "next_key": ""}
            )
            assert result["seq"] == "3"
            assert result["data"] == [{"jmcode": "005930"}]

    async def test_reuses_the_same_connection_across_calls(self):
        async with FakeConditionServer() as server:
            connect_calls = 0

            async def counted_connect() -> KiwoomWebSocket:
                nonlocal connect_calls
                connect_calls += 1
                return await _connect(server.url)

            session = ConditionSearchSession(connect=counted_connect)
            await session.request({"trnm": "CNSRLST"})
            await session.request(
                {"trnm": "CNSRREQ", "seq": "1", "search_type": "0", "stex_tp": "K",
                 "cont_yn": "N", "next_key": ""}
            )
            assert connect_calls == 1

    async def test_expect_reply_false_sends_without_waiting(self):
        async with FakeConditionServer() as server:
            session = ConditionSearchSession(connect=lambda: _connect(server.url))
            result = await session.request({"trnm": "CNSRCLR", "seq": "3"}, expect_reply=False)
            assert result is None

            async def _sent() -> bool:
                return any(m.get("trnm") == "CNSRCLR" for m in server.received)

            for _ in range(50):
                if await _sent():
                    break
                await asyncio.sleep(0.01)
            assert await _sent()

    async def test_times_out_when_no_reply_arrives(self, monkeypatch):
        import kiwoom_client.mcp.condition_search_session as mod

        monkeypatch.setattr(mod, "RESPONSE_TIMEOUT", 0.05)
        async with FakeConditionServer() as server:
            session = ConditionSearchSession(connect=lambda: _connect(server.url))
            with pytest.raises(ConditionSearchTimeout):
                # seq "999" 는 서버가 응답하지 않는 값이 아니라, CNSRREQ 자체는
                # 응답하지만 seq 불일치로 매칭되지 않는 상황을 흉내낸다.
                await session.request(
                    {"trnm": "CNSRREQ", "seq": "999", "search_type": "0", "stex_tp": "K",
                     "cont_yn": "N", "next_key": ""}
                )
```

- [ ] **Step 2: 테스트 실패 확인**

Run: `pytest tests/test_mcp_condition_search_session.py -v`
Expected: FAIL — `ModuleNotFoundError: No module named 'kiwoom_client.mcp.condition_search_session'`

- [ ] **Step 3: `src/kiwoom_client/mcp/condition_search_session.py` 구현**

```python
"""Correlates condition_search WebSocket requests with their replies.

condition_search rides the same WebSocket as real-time data: a request is
sent as one frame (``trnm`` + optionally ``seq``) and the reply arrives later
as a separate frame carrying the same ``trnm``/``seq``. This wraps that in an
async request/response call so each MCP tool call can simply await one.
"""

from __future__ import annotations

import asyncio
from collections.abc import Awaitable, Callable
from typing import Any

from kiwoom_client.websocket import KiwoomWebSocket

#: How long to wait for a matching reply frame before giving up.
RESPONSE_TIMEOUT = 15.0


class ConditionSearchTimeout(Exception):
    """No matching reply arrived within RESPONSE_TIMEOUT."""


class ConditionSearchSession:
    """Lazily-connected KiwoomWebSocket shared by all condition_search tools.

    Args:
        connect: Called once, lazily, to obtain a connected KiwoomWebSocket
            (e.g. ``lambda: api.create_websocket()`` followed by ``connect()``
            — see server.py for the concrete factory).
    """

    def __init__(self, connect: Callable[[], Awaitable[KiwoomWebSocket]]) -> None:
        self._connect = connect
        self._ws: KiwoomWebSocket | None = None
        self._listen_task: asyncio.Task[None] | None = None
        self._pending: dict[tuple[str, str | None], asyncio.Future[dict[str, Any]]] = {}
        self._dispatched_trnms: set[str] = set()

    async def _ensure_connected(self) -> KiwoomWebSocket:
        if self._ws is None:
            self._ws = await self._connect()
            self._listen_task = asyncio.create_task(self._ws.listen())
        return self._ws

    def _ensure_dispatcher(self, ws: KiwoomWebSocket, trnm: str) -> None:
        """Register one on_trnm callback per trnm that resolves pending futures.

        Registered once and reused across calls — KiwoomWebSocket has no
        ``off()``, so a callback-per-call would leak.
        """
        if trnm in self._dispatched_trnms:
            return
        self._dispatched_trnms.add(trnm)

        def _dispatch(data: dict[str, Any]) -> None:
            seq = data.get("seq")
            for key in ((trnm, seq), (trnm, None)):
                future = self._pending.pop(key, None)
                if future is not None and not future.done():
                    future.set_result(data)
                    return

        ws.on_trnm(trnm, _dispatch)

    async def request(
        self, payload: dict[str, Any], *, expect_reply: bool = True
    ) -> dict[str, Any] | None:
        """Send a condition_search payload and await its matching reply.

        Args:
            payload: One of the dicts built by ``api.condition_search.*``.
            expect_reply: False for CNSRCLR, which the protocol never acks.
        """
        ws = await self._ensure_connected()
        trnm = payload["trnm"]

        if not expect_reply:
            await ws.send(payload)
            return None

        self._ensure_dispatcher(ws, trnm)
        seq = payload.get("seq")
        key = (trnm, seq)
        loop = asyncio.get_running_loop()
        future: asyncio.Future[dict[str, Any]] = loop.create_future()
        self._pending[key] = future

        await ws.send(payload)
        try:
            return await asyncio.wait_for(future, RESPONSE_TIMEOUT)
        except asyncio.TimeoutError as exc:
            self._pending.pop(key, None)
            raise ConditionSearchTimeout(
                f"{trnm} 응답을 {RESPONSE_TIMEOUT}초 안에 받지 못했습니다"
            ) from exc

    async def close(self) -> None:
        if self._listen_task is not None:
            self._listen_task.cancel()
        if self._ws is not None:
            await self._ws.disconnect()
```

- [ ] **Step 4: 테스트 통과 확인**

Run: `pytest tests/test_mcp_condition_search_session.py -v`
Expected: PASS (5 tests)

- [ ] **Step 5: Commit**

```bash
git add src/kiwoom_client/mcp/condition_search_session.py tests/test_mcp_condition_search_session.py
git commit -m "$(cat <<'EOF'
feat(mcp): condition_search WebSocket 요청/응답 상관 세션 추가

Co-Authored-By: Claude Sonnet 5 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_019bMMMry1G4gSG6VSnkay27
EOF
)"
```

---

### Task 5: MCP 서버 조립 (`server.py`)

**Files:**
- Create: `src/kiwoom_client/mcp/server.py`
- Test: `tests/test_mcp_server.py`

**Interfaces:**
- Consumes:
  - `kiwoom_client.mcp.tools.discover_rest_tools() -> list[RestToolSpec]` (Task 2).
  - `kiwoom_client.mcp.guard.live_orders_allowed(*, is_mock, env=None) -> bool` (Task 3).
  - `kiwoom_client.mcp.condition_search_session.ConditionSearchSession` (Task 4).
  - `kiwoom_client.AsyncKiwoomAPI`, `kiwoom_client.base.KiwoomAPIError`.
- Produces:
  - `def build_server(api: AsyncKiwoomAPI, *, allow_live_orders: bool) -> tuple[Server, list[RestToolSpec]]` — 순수 조립 함수, stdio 연결 없이 단위 테스트 가능.
  - `async def dispatch_tool(api: AsyncKiwoomAPI, session: ConditionSearchSession, spec_by_name: dict[str, RestToolSpec], name: str, arguments: dict[str, Any]) -> dict[str, Any]` — 실제 호출 로직, `call_tool` 핸들러가 이걸 감싸기만 한다.
  - `def main() -> None` — 환경변수 읽고 stdio로 서버 실행.

- [ ] **Step 1: 실패하는 테스트 작성**

`tests/test_mcp_server.py` — `dispatch_tool`(순수 async 함수, MCP SDK 없이도 테스트 가능)과 `build_server`의 도구 필터링을 검증한다. `httpx_mock`으로 `AsyncKiwoomAPI`를 실제로 붙여 REST 호출이 제대로 전달되는지 확인한다:

```python
"""Tests for MCP server tool assembly and dispatch."""

from __future__ import annotations

import pytest

from kiwoom_client import AsyncKiwoomAPI
from kiwoom_client.base import KiwoomAPIError
from kiwoom_client.mcp.condition_search_session import ConditionSearchSession
from kiwoom_client.mcp.server import build_server, dispatch_tool
from kiwoom_client.mcp.tools import discover_rest_tools


@pytest.fixture
async def api(httpx_mock):
    httpx_mock.add_response(
        url="https://mockapi.kiwoom.com/oauth2/token",
        json={"token": "test_token", "token_type": "Bearer", "expires_in": 86400},
    )
    api = AsyncKiwoomAPI("key", "secret", is_mock=True)
    await api.login()
    yield api
    await api.close()


class TestBuildServer:
    def test_mock_registers_guarded_tools(self):
        _app, specs = build_server(api=None, allow_live_orders=True)
        names = {s.tool_name for s in specs}
        assert "order_buy_order" in names

    def test_live_without_opt_in_excludes_guarded_tools(self):
        _app, specs = build_server(api=None, allow_live_orders=False)
        names = {s.tool_name for s in specs}
        assert "order_buy_order" not in names
        assert "credit_order_margin_buy_order" not in names
        # 조회성 도구는 그대로 남는다
        assert "stock_info_basic_stock_info" in names

    def test_condition_search_tools_are_always_present(self):
        for allow in (True, False):
            _app, specs = build_server(api=None, allow_live_orders=allow)
            names = {s.tool_name for s in specs}
            assert {"condition_search_condition_list", "condition_search_condition_search",
                    "condition_search_condition_search_realtime",
                    "condition_search_condition_search_cancel"} <= names

    def test_tool_count_matches_discovery_when_allowed(self):
        _app, specs = build_server(api=None, allow_live_orders=True)
        rest_specs = [s for s in specs if not s.tool_name.startswith("condition_search_")]
        assert len(rest_specs) == len(discover_rest_tools())


class TestDispatchToolRest:
    async def test_forwards_params_to_the_underlying_method(self, httpx_mock, api):
        httpx_mock.add_response(
            url="https://mockapi.kiwoom.com/api/dostk/stkinfo",
            json={"return_code": 0, "return_msg": "OK", "stk_cd": "005930"},
        )
        specs = {s.tool_name: s for s in discover_rest_tools()}
        result = await dispatch_tool(
            api=api,
            session=None,
            spec_by_name=specs,
            name="stock_info_basic_stock_info",
            arguments={"params": {"stk_cd": "005930"}},
        )
        assert result["return_code"] == 0
        assert result["stk_cd"] == "005930"

    async def test_propagates_kiwoom_api_errors(self, httpx_mock, api):
        httpx_mock.add_response(
            url="https://mockapi.kiwoom.com/api/dostk/stkinfo",
            status_code=200,
            json={"return_code": 5, "return_msg": "종목코드 오류"},
        )
        specs = {s.tool_name: s for s in discover_rest_tools()}
        with pytest.raises(KiwoomAPIError):
            await dispatch_tool(
                api=api,
                session=None,
                spec_by_name=specs,
                name="stock_info_basic_stock_info",
                arguments={"params": {"stk_cd": "BAD"}},
            )

    async def test_unknown_tool_name_raises_value_error(self, api):
        with pytest.raises(ValueError, match="Unknown tool"):
            await dispatch_tool(
                api=api, session=None, spec_by_name={}, name="nope", arguments={}
            )
```

Note: `KiwoomAPIError`는 `return_code != 0`을 이미 예외로 올리는 기존 `BaseClient`/`AsyncBaseClient` 동작을 그대로 씀 — 별도 raise 로직을 `dispatch_tool`에 추가하지 않는다(기존 `tests/test_modules.py`가 성공 케이스만 다루는 것과 대칭으로, 실패 케이스는 `AsyncBaseClient.request`가 이미 처리한다는 걸 이 테스트로 확인한다).

- [ ] **Step 2: 테스트 실패 확인**

Run: `pytest tests/test_mcp_server.py -v`
Expected: FAIL — `ModuleNotFoundError: No module named 'kiwoom_client.mcp.server'`

- [ ] **Step 3: `src/kiwoom_client/mcp/server.py` 구현**

```python
"""MCP stdio server exposing every kiwoom-client REST endpoint as a tool.

Tool list is generated at startup by reflection (see :mod:`.tools`) — no
per-endpoint mapping is maintained here. Order/credit_order tools are
registered only when :func:`kiwoom_client.mcp.guard.live_orders_allowed`
says so.
"""

from __future__ import annotations

import asyncio
import json
import logging
import os
import sys
from typing import Any

from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import TextContent, Tool

from kiwoom_client import AsyncKiwoomAPI
from kiwoom_client.domestic.condition_search import ConditionSearch
from kiwoom_client.mcp.condition_search_session import ConditionSearchSession
from kiwoom_client.mcp.guard import live_orders_allowed
from kiwoom_client.mcp.tools import RestToolSpec, discover_rest_tools

logger = logging.getLogger(__name__)

#: The 4 condition_search tools don't fit the generic **kwargs pattern (they
#: have real, non-passthrough parameters), so they're spelled out here.
_CONDITION_SEARCH_SPECS: list[RestToolSpec] = [
    RestToolSpec(
        module_name="condition_search", method_name="condition_list",
        tool_name="condition_search_condition_list",
        description="조건검색 목록조회 — 다른 condition_search 도구를 쓰기 전에 먼저 호출해 seq 값을 얻는다.",
        guarded=False,
    ),
    RestToolSpec(
        module_name="condition_search", method_name="condition_search",
        tool_name="condition_search_condition_search",
        description="조건검색 요청 일반. seq: condition_list 로 얻은 조건검색식 일련번호.",
        guarded=False,
    ),
    RestToolSpec(
        module_name="condition_search", method_name="condition_search_realtime",
        tool_name="condition_search_condition_search_realtime",
        description=(
            "조건검색 요청 실시간. 최초 응답 프레임만 반환한다 — 이후 조건 "
            "편입/이탈에 따라 계속 도착하는 후속 프레임은 이 도구로 받을 수 없다."
        ),
        guarded=False,
    ),
    RestToolSpec(
        module_name="condition_search", method_name="condition_search_cancel",
        tool_name="condition_search_condition_search_cancel",
        description="조건검색 실시간 해제. 키움 프로토콜상 ack 프레임이 없어 전송만 하고 반환한다.",
        guarded=False,
    ),
]


def build_server(api: AsyncKiwoomAPI | None, *, allow_live_orders: bool) -> tuple[Server, list[RestToolSpec]]:
    """Assemble the MCP Server and the filtered list of tool specs.

    Pure assembly — no stdio, no network. ``api`` may be ``None`` here since
    this only reads tool metadata, not credentials.
    """
    rest_specs = [
        spec for spec in discover_rest_tools() if not spec.guarded or allow_live_orders
    ]
    all_specs = rest_specs + _CONDITION_SEARCH_SPECS
    app: Server = Server("kiwoom-client")
    return app, all_specs


async def dispatch_tool(
    api: AsyncKiwoomAPI,
    session: ConditionSearchSession | None,
    spec_by_name: dict[str, RestToolSpec],
    name: str,
    arguments: dict[str, Any],
) -> dict[str, Any] | None:
    """Run one tool call and return the raw response dict.

    REST tools call straight through to the matching ``AsyncKiwoomAPI``
    module method. condition_search tools build their WebSocket payload and
    send it through ``session``.
    """
    spec = spec_by_name.get(name)
    if spec is None:
        raise ValueError(f"Unknown tool: {name}")

    if spec.module_name == "condition_search":
        assert session is not None
        cs = ConditionSearch()
        if spec.method_name == "condition_list":
            return await session.request(cs.condition_list())
        if spec.method_name == "condition_search":
            payload = cs.condition_search(
                seq=arguments["seq"],
                search_type=arguments.get("search_type", "0"),
                stex_tp=arguments.get("stex_tp", "K"),
                cont_yn=arguments.get("cont_yn", "N"),
                next_key=arguments.get("next_key", ""),
            )
            return await session.request(payload)
        if spec.method_name == "condition_search_realtime":
            payload = cs.condition_search_realtime(
                seq=arguments["seq"],
                stex_tp=arguments.get("stex_tp", "K"),
                cont_yn=arguments.get("cont_yn", "N"),
                next_key=arguments.get("next_key", ""),
            )
            return await session.request(payload)
        if spec.method_name == "condition_search_cancel":
            payload = cs.condition_search_cancel(seq=arguments["seq"])
            await session.request(payload, expect_reply=False)
            return {"trnm": "CNSRCLR", "seq": arguments["seq"], "status": "sent"}
        raise ValueError(f"Unknown condition_search tool: {name}")

    module_obj = getattr(api, spec.module_name)
    method = getattr(module_obj, spec.method_name)
    params = arguments.get("params") or {}
    cont_yn = arguments.get("cont_yn", "N")
    next_key = arguments.get("next_key", "")
    return await method(cont_yn=cont_yn, next_key=next_key, **params)


def _rest_input_schema() -> dict[str, Any]:
    return {
        "type": "object",
        "properties": {
            "cont_yn": {"type": "string", "default": "N", "description": "연속조회 여부"},
            "next_key": {"type": "string", "default": "", "description": "연속조회 키"},
            "params": {"type": "object", "description": "TR 요청 필드 (키움 API 가이드 참고)"},
        },
    }


def _condition_search_input_schema(method_name: str) -> dict[str, Any]:
    if method_name == "condition_list":
        return {"type": "object", "properties": {}}
    if method_name == "condition_search_cancel":
        return {
            "type": "object",
            "properties": {"seq": {"type": "string", "description": "조건검색식 일련번호"}},
            "required": ["seq"],
        }
    return {
        "type": "object",
        "properties": {
            "seq": {"type": "string", "description": "조건검색식 일련번호"},
            "search_type": {"type": "string", "default": "0"},
            "stex_tp": {"type": "string", "default": "K"},
            "cont_yn": {"type": "string", "default": "N"},
            "next_key": {"type": "string", "default": ""},
        },
        "required": ["seq"],
    }


def _input_schema(spec: RestToolSpec) -> dict[str, Any]:
    if spec.module_name == "condition_search":
        return _condition_search_input_schema(spec.method_name)
    return _rest_input_schema()


def main() -> None:
    """Entry point for the ``kiwoom-client-mcp`` console script."""
    logging.basicConfig(level=logging.INFO)

    app_key = os.environ.get("KIWOOM_APP_KEY")
    app_secret = os.environ.get("KIWOOM_APP_SECRET")
    if not app_key or not app_secret:
        print(
            "Error: KIWOOM_APP_KEY and KIWOOM_APP_SECRET environment variables must be set.",
            file=sys.stderr,
        )
        sys.exit(1)
    is_mock = os.environ.get("KIWOOM_IS_MOCK", "false").strip().lower() == "true"

    api = AsyncKiwoomAPI(app_key, app_secret, is_mock=is_mock)
    allow_live_orders = live_orders_allowed(is_mock=is_mock)
    app, specs = build_server(api, allow_live_orders=allow_live_orders)
    spec_by_name = {spec.tool_name: spec for spec in specs}
    excluded = len(discover_rest_tools()) - len([s for s in specs if s.module_name != "condition_search"])
    if excluded:
        logger.info("실주문 opt-in 미설정 — 주문 도구 %d개를 등록하지 않았습니다.", excluded)

    session = ConditionSearchSession(connect=lambda: _connect_condition_search(api))

    @app.list_tools()  # type: ignore[misc]
    async def list_tools() -> list[Tool]:
        return [
            Tool(name=spec.tool_name, description=spec.description, inputSchema=_input_schema(spec))
            for spec in specs
        ]

    @app.call_tool()  # type: ignore[misc]
    async def call_tool(name: str, arguments: dict[str, Any]) -> list[TextContent]:
        result = await dispatch_tool(api, session, spec_by_name, name, arguments)
        return [TextContent(type="text", text=json.dumps(result, ensure_ascii=False))]

    async def _run() -> None:
        async with stdio_server() as (read_stream, write_stream):
            await app.run(read_stream, write_stream, app.create_initialization_options())

    try:
        asyncio.run(_run())
    finally:
        asyncio.run(session.close())
        asyncio.run(api.close())


async def _connect_condition_search(api: AsyncKiwoomAPI):
    ws = await api.create_websocket()
    await ws.connect()
    return ws


if __name__ == "__main__":
    main()
```

- [ ] **Step 4: 테스트 통과 확인**

Run: `pytest tests/test_mcp_server.py -v`
Expected: PASS (7 tests). `TestBuildServer` 테스트는 `mcp` 패키지가 Task 1에서 설치되어 있어야 통과한다.

- [ ] **Step 5: 전체 스위트 + 정적 분석**

Run: `pytest -q && ruff check src/kiwoom_client/mcp tests/test_mcp_*.py && mypy src/kiwoom_client/mcp`
Expected: 전부 통과. `mypy`가 `mcp` 패키지에 타입 스텁이 없다는 에러를 내면 `pyproject.toml`의 `[tool.mypy]`(있다면) 또는 `server.py` 상단에 `# type: ignore[import-untyped]`를 `from mcp...` import 줄에 붙여 해결한다 — 이건 실제 실행 시 `mypy` 출력에 따라 결정한다.

- [ ] **Step 6: Commit**

```bash
git add src/kiwoom_client/mcp/server.py tests/test_mcp_server.py
git commit -m "$(cat <<'EOF'
feat(mcp): MCP stdio 서버 조립 — 182개 REST 도구 + condition_search 4종

Co-Authored-By: Claude Sonnet 5 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_019bMMMry1G4gSG6VSnkay27
EOF
)"
```

---

### Task 6: 문서화 (README.md, README_EN.md)

**Files:**
- Modify: `README.md`
- Modify: `README_EN.md`

**Interfaces:**
- Consumes: 없음 (문서만).

- [ ] **Step 1: README.md 목차에 항목 추가**

`README.md`의 `## 목차` 블록에서 `- [환경 설정](#환경-설정)` 다음 줄에 추가:

```markdown
- [MCP 서버로 사용하기](#mcp-서버로-사용하기)
```

- [ ] **Step 2: README.md에 섹션 추가**

`## 환경 설정` 섹션이 끝나는 지점(`## 지원 API 목록` 바로 앞)에 새 섹션 삽입:

```markdown
## MCP 서버로 사용하기

Claude Code, Cursor 등 MCP(Model Context Protocol)를 지원하는 도구에서 이 라이브러리를 직접 호출할 수 있습니다. 15개 도메인 모듈의 REST 엔드포인트 전부와 조건검색(condition_search) 4종이 MCP 도구로 노출됩니다.

```bash
pip install 'kiwoom-client[mcp]'
```

MCP 클라이언트 설정(예: Claude Code `.mcp.json`)에 추가:

```json
{
  "mcpServers": {
    "kiwoom-client": {
      "command": "kiwoom-client-mcp",
      "env": {
        "KIWOOM_APP_KEY": "발급받은_앱키",
        "KIWOOM_APP_SECRET": "발급받은_시크릿키",
        "KIWOOM_IS_MOCK": "true"
      }
    }
  }
}
```

| 환경변수 | 설명 | 기본값 |
|---|---|---|
| `KIWOOM_APP_KEY` | 앱키 (필수) | — |
| `KIWOOM_APP_SECRET` | 시크릿키 (필수) | — |
| `KIWOOM_IS_MOCK` | 모의투자 서버 사용 여부 | `false` |
| `KIWOOM_MCP_ALLOW_LIVE_ORDERS` | 실전투자 계좌에서 주문 도구(매수/매도/정정/취소·신용주문)를 노출할지 여부 | `false` |

**실주문 가드**: `KIWOOM_IS_MOCK=false`(실전투자)이고 `KIWOOM_MCP_ALLOW_LIVE_ORDERS`가 `true`가 아니면, 주문 관련 도구는 서버 시작 시점에 아예 등록되지 않습니다 — MCP 클라이언트(AI 에이전트)가 그 도구의 존재 자체를 모릅니다. 모의투자(`KIWOOM_IS_MOCK=true`)는 이 가드 없이 항상 사용 가능합니다. 이 가드는 MCP 서버 경로에만 적용되며, 파이썬 코드에서 `KiwoomAPI`/`AsyncKiwoomAPI`를 직접 쓰는 기존 방식에는 영향이 없습니다.

조회성 도구는 `{"params": {...}}` 형태로 TR 요청 필드를 그대로 전달합니다(필드 목록은 [키움 REST API 가이드](https://openapi.kiwoom.com) 참고). 예: `stock_info_basic_stock_info` 도구에 `{"params": {"stk_cd": "005930"}}`.
```

- [ ] **Step 3: README_EN.md에 대응 섹션 추가**

`README_EN.md`에서 동일한 위치(환경설정 관련 섹션 다음)에 영문으로 같은 내용을 추가한다:

```markdown
## Using as an MCP Server

This library can be called directly from MCP (Model Context Protocol) clients such as Claude Code and Cursor. Every REST endpoint across all 15 domain modules, plus the 4 condition_search tools, is exposed as an MCP tool.

```bash
pip install 'kiwoom-client[mcp]'
```

Add to your MCP client config (e.g. Claude Code `.mcp.json`):

```json
{
  "mcpServers": {
    "kiwoom-client": {
      "command": "kiwoom-client-mcp",
      "env": {
        "KIWOOM_APP_KEY": "your_app_key",
        "KIWOOM_APP_SECRET": "your_app_secret",
        "KIWOOM_IS_MOCK": "true"
      }
    }
  }
}
```

| Env var | Description | Default |
|---|---|---|
| `KIWOOM_APP_KEY` | App key (required) | — |
| `KIWOOM_APP_SECRET` | App secret (required) | — |
| `KIWOOM_IS_MOCK` | Use the mock trading server | `false` |
| `KIWOOM_MCP_ALLOW_LIVE_ORDERS` | Expose order tools (buy/sell/modify/cancel, credit orders) against a live account | `false` |

**Live-order guard**: when `KIWOOM_IS_MOCK=false` (live account) and `KIWOOM_MCP_ALLOW_LIVE_ORDERS` is not `true`, order-related tools are not registered at server startup at all — the MCP client (AI agent) never sees they exist. Mock trading (`KIWOOM_IS_MOCK=true`) always has them available, no guard. This guard applies only to the MCP path — direct use of `KiwoomAPI`/`AsyncKiwoomAPI` from Python code is unaffected.

Query-style tools take `{"params": {...}}`, passed straight through as the TR request body (see the [Kiwoom REST API guide](https://openapi.kiwoom.com) for field names). Example: `stock_info_basic_stock_info` with `{"params": {"stk_cd": "005930"}}`.
```

- [ ] **Step 4: Commit**

```bash
git add README.md README_EN.md
git commit -m "$(cat <<'EOF'
docs(readme): MCP 서버 사용법 섹션 추가

Co-Authored-By: Claude Sonnet 5 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_019bMMMry1G4gSG6VSnkay27
EOF
)"
```

---

### Task 7: CHANGELOG 갱신 및 마무리 검증

**Files:**
- Modify: `CHANGELOG.md`

**Interfaces:**
- Consumes: 없음.

- [ ] **Step 1: `CHANGELOG.md` 최상단에 새 항목 추가**

기존 항목들의 형식(버전 헤더 + bullet)을 따라, 아직 릴리스되지 않은 변경사항 섹션(있으면 그 아래, 없으면 최상단에 `## [Unreleased]`)에 추가:

```markdown
### Added

- **MCP 서버.** `pip install 'kiwoom-client[mcp]'` 후 `kiwoom-client-mcp`로
  실행하면 Claude Code/Cursor 등에서 182개 REST 엔드포인트 + condition_search
  4종을 도구로 직접 호출할 수 있습니다. 주문/신용주문 도구는 실전투자 계좌에서
  `KIWOOM_MCP_ALLOW_LIVE_ORDERS=true`를 명시해야 노출됩니다.
```

- [ ] **Step 2: 전체 테스트 스위트 실행**

Run: `pytest -q`
Expected: 전부 PASS, 실패 0.

- [ ] **Step 3: 린트 + 타입체크**

Run: `ruff check src tests && mypy src`
Expected: 에러 없음.

- [ ] **Step 4: 로컬 stdio 스모크 테스트**

Run:
```bash
KIWOOM_APP_KEY=dummy KIWOOM_APP_SECRET=dummy KIWOOM_IS_MOCK=true timeout 3 kiwoom-client-mcp <<< '' ; echo "exit: $?"
```
Expected: 타임아웃(124)으로 종료 — 크래시 없이 stdio에서 입력을 기다리며 떠 있었다는 뜻. `ModuleNotFoundError`나 `AttributeError`(예: `mcp.server.Server`/`mcp.server.stdio.stdio_server`/`mcp.types.Tool` API가 설치된 `mcp` 버전과 다를 경우)가 나오면, 설치된 `mcp` 패키지의 실제 API를 `python -c "import mcp.server, mcp.types; help(mcp.server.Server)"`로 확인해 `server.py`를 그 버전에 맞게 고친다.

- [ ] **Step 5: Commit**

```bash
git add CHANGELOG.md
git commit -m "$(cat <<'EOF'
docs(changelog): MCP 서버 추가 기록

Co-Authored-By: Claude Sonnet 5 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_019bMMMry1G4gSG6VSnkay27
EOF
)"
```
</content>
