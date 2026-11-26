"""``kiwoom-client-mcp doctor`` — check an MCP setup without starting the server.

By default it makes **no network call** and needs no keys: Python and ``mcp``
versions, which environment variables are set (never their values), how the
server would resolve mock/live, mode, toolsets and the live-order guard, and
how many tools ``tools/list`` would show and how big that list is.

``--check-auth`` additionally issues one access token with the configured
keys (no tool call, no revoke), to tell a bad key from a client problem.
"""

from __future__ import annotations

import asyncio
import importlib.metadata
import json
import platform
import sys
from collections.abc import Callable, Collection, Mapping
from dataclasses import dataclass, field
from typing import Any

from kiwoom_client import __version__
from kiwoom_client._env import ENV_APP_KEY, ENV_APP_SECRET, ENV_IS_MOCK, parse_bool
from kiwoom_client.mcp.demo import ENV_VAR as DEMO_ENV_VAR
from kiwoom_client.mcp.demo import demo_from_env
from kiwoom_client.mcp.guard import ENV_VAR as LIVE_ORDERS_ENV_VAR
from kiwoom_client.mcp.guard import READ_ONLY_ENV, order_tools_allowed, read_only
from kiwoom_client.mcp.modes import ENV_VAR as MODE_ENV_VAR
from kiwoom_client.mcp.modes import parse_mode
from kiwoom_client.mcp.response_size import ENV_VAR as MAX_ROWS_ENV_VAR
from kiwoom_client.mcp.response_size import parse_max_rows
from kiwoom_client.mcp.toolsets import ENV_VAR as TOOLSETS_ENV_VAR
from kiwoom_client.mcp.toolsets import parse_toolsets

#: Variables reported as set/unset — values are never printed.
ENV_VARS: tuple[str, ...] = (
    ENV_APP_KEY,
    ENV_APP_SECRET,
    ENV_IS_MOCK,
    MODE_ENV_VAR,
    TOOLSETS_ENV_VAR,
    MAX_ROWS_ENV_VAR,
    LIVE_ORDERS_ENV_VAR,
    READ_ONLY_ENV,
    DEMO_ENV_VAR,
)

#: The ``mcp`` major version the server is written for (pyproject ``mcp>=2.0,<3``).
MCP_MAJOR = 2

OK, WARN, ERROR, INFO = "ok", "warn", "error", "info"
_MARK = {OK: "[ok]  ", WARN: "[warn]", ERROR: "[err] ", INFO: "[--]  "}


@dataclass
class Report:
    lines: list[tuple[str, str]] = field(default_factory=list)

    def add(self, level: str, text: str) -> None:
        self.lines.append((level, text))

    @property
    def failed(self) -> bool:
        return any(level == ERROR for level, _ in self.lines)

    def render(self) -> str:
        return "\n".join(f"{_MARK[level]} {text}" for level, text in self.lines) + "\n"


@dataclass(frozen=True)
class Overrides:
    """CLI flags that win over the environment (``None`` = not given)."""

    mock: bool = False
    toolsets: frozenset[str] | None = None
    toolsets_all: bool = False
    mode: str | None = None
    max_rows: int | None = None
    demo: bool = False


def _mcp_version() -> str | None:
    try:
        return importlib.metadata.version("mcp")
    except importlib.metadata.PackageNotFoundError:
        return None


def _resolve(report: Report, env: Mapping[str, str], flags: Overrides) -> dict[str, Any] | None:
    """Resolve settings like the server does; report and return ``None`` on a bad value."""
    settings: dict[str, Any] = {}
    try:
        raw = env.get(ENV_IS_MOCK, "")
        settings["is_mock"] = True if flags.mock else (parse_bool(raw) if raw.strip() else False)
    except ValueError as exc:
        report.add(ERROR, f"{ENV_IS_MOCK}: {exc}")
        return None
    try:
        settings["mode"] = flags.mode or parse_mode(env.get(MODE_ENV_VAR))
    except ValueError as exc:
        report.add(ERROR, str(exc))
        return None
    try:
        if flags.toolsets_all:
            settings["toolsets"] = None
        elif flags.toolsets is not None:
            settings["toolsets"] = flags.toolsets
        else:
            settings["toolsets"] = parse_toolsets(env.get(TOOLSETS_ENV_VAR))
    except ValueError as exc:
        report.add(ERROR, str(exc))
        return None
    try:
        rows = flags.max_rows
        settings["max_rows"] = (
            rows if rows is not None else parse_max_rows(env.get(MAX_ROWS_ENV_VAR))
        )
    except ValueError as exc:
        report.add(ERROR, f"{MAX_ROWS_ENV_VAR}: {exc}")
        return None
    return settings


def _tool_listing(
    *, allow_live_orders: bool, mode: str, toolsets: Collection[str] | None
) -> tuple[int, int]:
    """(tool count, characters) of ``tools/list`` — built offline, ``api=None``."""
    from mcp import types

    from kiwoom_client.mcp.server import build_server

    app, _specs = build_server(
        api=None, allow_live_orders=allow_live_orders, toolsets=toolsets, mode=mode
    )
    handler = app.get_request_handler("tools/list")
    assert handler is not None

    async def listed() -> Any:
        # The handlers registered by build_server ignore the request context.
        return await handler.handler(None, types.PaginatedRequestParams())  # type: ignore[arg-type]

    result = asyncio.run(listed())
    assert isinstance(result, types.ListToolsResult)
    tools = [t.model_dump(mode="json", by_alias=True, exclude_none=True) for t in result.tools]
    return len(tools), len(json.dumps(tools, ensure_ascii=False))


async def _issue_token(app_key: str, app_secret: str, *, is_mock: bool) -> None:
    from kiwoom_client import AsyncKiwoomAPI

    api = AsyncKiwoomAPI(app_key, app_secret, is_mock=is_mock)
    try:
        await api.login()  # one token; never logout/revoke — the key may be shared
    finally:
        await api.close()


def diagnose(
    *,
    env: Mapping[str, str],
    flags: Overrides = Overrides(),
    check_auth: bool = False,
    issue_token: Callable[..., Any] = _issue_token,
) -> Report:
    report = Report()

    report.add(INFO, f"kiwoom-client {__version__} · Python {platform.python_version()}")
    mcp_version = _mcp_version()
    mcp_ok = False
    if mcp_version is None:
        report.add(ERROR, "mcp 패키지 없음 — pip install 'kiwoom-client[mcp]'")
    elif not mcp_version.split(".")[0].isdigit() or int(mcp_version.split(".")[0]) != MCP_MAJOR:
        report.add(
            ERROR, f"mcp {mcp_version} — {MCP_MAJOR}.x 가 필요합니다: pip install -U 'mcp>=2.0,<3'"
        )
    else:
        mcp_ok = True
        report.add(OK, f"mcp {mcp_version}")

    keys_present = all(env.get(name, "").strip() for name in (ENV_APP_KEY, ENV_APP_SECRET))
    try:
        demo = flags.demo or demo_from_env(env, have_keys=keys_present)
    except ValueError as exc:
        report.add(ERROR, str(exc))
        demo = False
    for name in ENV_VARS:
        present = bool(env.get(name, "").strip())
        required = name in (ENV_APP_KEY, ENV_APP_SECRET) and not demo
        level = (OK if present else ERROR) if required else INFO
        report.add(level, f"{name}: {'설정됨' if present else '없음'}")
    if demo:
        report.add(
            OK,
            "데모 모드 — 키 불필요, 가상 데이터, 어디에도 연결하지 않음"
            + (" (설정된 앱키는 쓰지 않음)" if keys_present else ""),
        )
    elif not keys_present:
        report.add(
            ERROR,
            "앱키·시크릿이 없으면 서버가 시작하지 않습니다 — "
            "`kiwoom-client-mcp config <클라이언트>` 참고",
        )

    settings = _resolve(report, env, flags)
    if settings is None:
        return report

    is_mock = settings["is_mock"] or demo  # demo orders are paper trades
    try:
        locked = read_only(dict(env))
    except ValueError as exc:
        report.add(ERROR, str(exc))
        return report
    allow = order_tools_allowed(is_mock=is_mock, env=dict(env))
    server = "모의투자 (mockapi.kiwoom.com)" if is_mock else "실전 (api.kiwoom.com)"
    report.add(OK, f"서버: {'데모 (프로세스 안 가짜 서버, 연결 없음)' if demo else server}")
    toolsets = settings["toolsets"]
    chosen = ", ".join(sorted(toolsets)) if toolsets else "전부"
    report.add(OK, f"모드: {settings['mode']} · toolset: {chosen}")
    if settings["max_rows"] is not None:
        report.add(OK, f"리스트 응답 기본 {settings['max_rows']}행")
    if locked:
        report.add(OK, f"주문 도구: 등록 안 됨 (읽기 전용 {READ_ONLY_ENV}=true)")
    elif demo:
        report.add(OK, "주문 도구: 등록 (데모 — 메모리 안의 종이 거래, 전송 없음)")
    elif is_mock:
        report.add(OK, "주문 도구: 등록 (모의투자 — 실제 체결 없음)")
    elif allow:
        report.add(
            WARN,
            f"주문 도구: 실전 계좌에 등록됨 ({LIVE_ORDERS_ENV_VAR}=true) — 실제 주문이 나갑니다",
        )
    else:
        report.add(OK, f"주문 도구: 등록 안 됨 (실전 + {LIVE_ORDERS_ENV_VAR} 미설정)")

    if mcp_ok:
        count, size = _tool_listing(
            allow_live_orders=allow, mode=settings["mode"], toolsets=toolsets
        )
        report.add(OK, f"tools/list: 도구 {count}개, 약 {size / 1000:.1f} K 글자")

    if demo:
        report.add(INFO, "인증: 데모 모드라 확인하지 않습니다 (네트워크 호출 없음)")
    elif not check_auth:
        report.add(INFO, "인증: 확인 안 함 (네트워크 호출 없음). 토큰 발급을 보려면 --check-auth")
    elif not keys_present:
        report.add(ERROR, "인증: 앱키·시크릿이 없어 확인할 수 없습니다")
    else:
        try:
            asyncio.run(issue_token(env[ENV_APP_KEY], env[ENV_APP_SECRET], is_mock=is_mock))
        except Exception as exc:  # report any failure; the message never holds the keys
            report.add(ERROR, f"인증: 토큰 발급 실패 — {type(exc).__name__}: {exc}")
        else:
            report.add(OK, "인증: 토큰 발급 성공")
    return report


def run(*, env: Mapping[str, str], flags: Overrides = Overrides(), check_auth: bool = False) -> int:
    report = diagnose(env=env, flags=flags, check_auth=check_auth)
    sys.stdout.write(report.render())
    return 1 if report.failed else 0
