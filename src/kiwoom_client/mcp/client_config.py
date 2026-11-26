"""Copy-paste install snippets for popular MCP clients.

``kiwoom-client-mcp config <client>`` prints one of these. Keys are always
placeholders — this module never reads real credentials — and the snippets
never turn on ``KIWOOM_MCP_ALLOW_LIVE_ORDERS``: enabling live orders stays a
deliberate, manual edit.

``demo=True`` gives a snippet with no key at all: the server starts with
``--demo`` (synthetic data, connects nowhere).
"""

from __future__ import annotations

import json
import shlex
from collections.abc import Sequence
from dataclasses import dataclass

#: Supported ``config`` targets. Formats follow each client's own docs:
#: Claude Code ``claude mcp add``; Claude Desktop ``claude_desktop_config.json``;
#: Cursor ``mcp.json``; Codex ``config.toml`` ``[mcp_servers.*]``; VS Code
#: (GitHub Copilot) portable ``.mcp.json``/``~/.copilot/mcp-config.json``
#: (``mcpServers`` with ``type: "stdio"``); Gemini CLI ``settings.json``.
CLIENTS: tuple[str, ...] = (
    "claude-code",
    "claude-desktop",
    "cursor",
    "codex",
    "vscode",
    "gemini-cli",
)

#: Release page with the one-click Claude Desktop bundle (.mcpb).
RELEASES_URL = "https://github.com/younghwan91/kiwoom-client/releases"

#: Name the server is registered under in every snippet. Short on purpose:
#: some clients prefix every tool name with it.
SERVER_NAME = "kiwoom"

APP_KEY_PLACEHOLDER = "YOUR_APP_KEY"
APP_SECRET_PLACEHOLDER = "YOUR_APP_SECRET"

#: How the client should start the server.
#: ``uvx`` needs nothing pre-installed but uv; ``installed`` assumes
#: ``pip install 'kiwoom-client[mcp]'`` put ``kiwoom-client-mcp`` on PATH.
LAUNCHERS: tuple[str, ...] = ("uvx", "installed")


def launch_command(launcher: str, *, demo: bool = False) -> list[str]:
    """argv that starts the server, e.g. ``["uvx", "--from", ..., "kiwoom-client-mcp"]``."""
    flags = ["--demo"] if demo else []
    if launcher == "uvx":
        return ["uvx", "--from", "kiwoom-client[mcp]", "kiwoom-client-mcp", *flags]
    if launcher == "installed":
        return ["kiwoom-client-mcp", *flags]
    raise ValueError(f"unknown launcher: {launcher!r} (choose from {', '.join(LAUNCHERS)})")


def server_env(
    *,
    mock: bool,
    toolsets: Sequence[str] | None = None,
    discovery: bool = False,
    mode: str | None = None,
    demo: bool = False,
) -> dict[str, str]:
    """Environment block for the snippet — placeholders only.

    ``mode`` (``"full"``/``"discovery"``) is written as ``KIWOOM_MCP_MODE``;
    ``None`` leaves it out so the server uses its default (smart).
    ``discovery=True`` is the older spelling of ``mode="discovery"``.
    ``demo=True`` leaves the key and server out (``--demo`` needs neither).
    """
    env: dict[str, str] = (
        {}
        if demo
        else {
            "KIWOOM_APP_KEY": APP_KEY_PLACEHOLDER,
            "KIWOOM_APP_SECRET": APP_SECRET_PLACEHOLDER,
            "KIWOOM_IS_MOCK": "true" if mock else "false",
        }
    )
    if toolsets:
        env["KIWOOM_MCP_TOOLSETS"] = ",".join(toolsets)
    if discovery:
        mode = "discovery"
    if mode:
        env["KIWOOM_MCP_MODE"] = mode
    return env


def _mcp_servers_json(
    argv: list[str], env: dict[str, str], extra: dict[str, object] | None = None
) -> str:
    server: dict[str, object] = dict(extra or {})
    server.update({"command": argv[0], "args": argv[1:], "env": env})
    config = {"mcpServers": {SERVER_NAME: server}}
    return json.dumps(config, ensure_ascii=False, indent=2)


def _toml_str(value: str) -> str:
    return json.dumps(value, ensure_ascii=False)  # TOML basic strings share JSON escaping


def _codex_toml(argv: list[str], env: dict[str, str]) -> str:
    args = ", ".join(_toml_str(a) for a in argv[1:])
    env_items = ", ".join(f"{k} = {_toml_str(v)}" for k, v in env.items())
    text = f"[mcp_servers.{SERVER_NAME}]\ncommand = {_toml_str(argv[0])}\nargs = [{args}]\n"
    return text + (f"env = {{ {env_items} }}\n" if env else "")


@dataclass(frozen=True)
class Snippet:
    """``body`` is what to paste (valid JSON/TOML/shell); ``note`` says where."""

    note: str
    body: str


def render(
    client: str,
    *,
    mock: bool = True,
    toolsets: Sequence[str] | None = None,
    launcher: str = "uvx",
    discovery: bool = False,
    mode: str | None = None,
    demo: bool = False,
) -> Snippet:
    """Return the snippet for ``client`` (one of :data:`CLIENTS`)."""
    snippet = _render(
        client, mock=mock, toolsets=toolsets, launcher=launcher, discovery=discovery,
        mode=mode, demo=demo,
    )  # fmt: skip
    if demo:
        note = (
            f"{snippet.note}\n데모 모드: 키 없이 가상 데이터로 동작하고 키움에 연결하지 않습니다 "
            "(시세·계좌는 실제가 아님). 실제로 쓰려면 --demo 없이 다시 출력해 키를 넣으세요."
        )
        return Snippet(note=note, body=snippet.body)
    return snippet


def _render(
    client: str,
    *,
    mock: bool,
    toolsets: Sequence[str] | None,
    launcher: str,
    discovery: bool,
    mode: str | None,
    demo: bool,
) -> Snippet:
    argv = launch_command(launcher, demo=demo)
    env = server_env(mock=mock, toolsets=toolsets, discovery=discovery, mode=mode, demo=demo)

    if client == "claude-code":
        env_flags = "".join(f"-e {shlex.quote(f'{k}={v}')} " for k, v in env.items())
        command = " ".join(shlex.quote(a) for a in argv)
        return Snippet(
            note="터미널에서 실행하세요. 팀과 공유하려면 --scope project (→ .mcp.json).",
            body=f"claude mcp add {SERVER_NAME} {env_flags}-- {command}\n",
        )
    if client == "claude-desktop":
        return Snippet(
            note=(
                "가장 쉬운 방법: Releases 의 kiwoom-client-<버전>.mcpb 를 더블클릭해 설치하면\n"
                f"  키를 입력 화면에서 받습니다 (JSON 편집 불필요). {RELEASES_URL}\n"
                "직접 설정하려면 claude_desktop_config.json 의 mcpServers 에 병합하세요.\n"
                "  macOS:   ~/Library/Application Support/Claude/claude_desktop_config.json\n"
                "  Windows: %APPDATA%\\Claude\\claude_desktop_config.json"
            ),
            body=_mcp_servers_json(argv, env) + "\n",
        )
    if client == "cursor":
        return Snippet(
            note="~/.cursor/mcp.json (전역) 또는 <프로젝트>/.cursor/mcp.json 에 병합하세요.",
            body=_mcp_servers_json(argv, env) + "\n",
        )
    if client == "codex":
        return Snippet(note="~/.codex/config.toml 에 추가하세요.", body=_codex_toml(argv, env))
    if client == "vscode":
        return Snippet(
            note=(
                "VS Code (GitHub Copilot): 워크스페이스 루트 .mcp.json 또는 "
                "~/.copilot/mcp-config.json 의 mcpServers 에 병합하세요.\n"
                '  키를 파일에 두기 싫으면 값을 "${KIWOOM_APP_KEY}" 처럼 '
                "환경변수 참조로 바꿉니다."
            ),
            body=_mcp_servers_json(argv, env, extra={"type": "stdio"}) + "\n",
        )
    if client == "gemini-cli":
        return Snippet(
            note=(
                "~/.gemini/settings.json (사용자) 또는 <프로젝트>/.gemini/settings.json 의 "
                "mcpServers 에 병합하세요."
            ),
            body=_mcp_servers_json(argv, env) + "\n",
        )
    raise ValueError(f"unknown client: {client!r} (choose from {', '.join(CLIENTS)})")
