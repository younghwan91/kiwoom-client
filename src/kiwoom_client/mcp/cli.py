"""``kiwoom-client-mcp`` command line.

::

    kiwoom-client-mcp                      # stdio MCP 서버 실행 (기본)
    kiwoom-client-mcp --mock --toolsets market,chart
    kiwoom-client-mcp config claude-code   # 클라이언트 설정 스니펫 출력
    kiwoom-client-mcp --version

``--help``, ``--version`` and ``config`` need neither API keys nor the ``mcp``
extra, so they work right after ``pip install kiwoom-client`` or via ``uvx``.
The ``mcp`` package is imported only when the server actually starts.
"""

from __future__ import annotations

import argparse
import os
import sys
from collections.abc import Sequence

from kiwoom_client import __version__
from kiwoom_client.mcp.client_config import CLIENTS, LAUNCHERS, render
from kiwoom_client.mcp.guard import ENV_VAR as LIVE_ORDERS_ENV_VAR
from kiwoom_client.mcp.toolsets import ENV_VAR as TOOLSETS_ENV_VAR
from kiwoom_client.mcp.toolsets import TOOLSET_NAMES, parse_toolsets, toolsets_from_env

_EPILOG = f"""\
환경변수:
  KIWOOM_APP_KEY / KIWOOM_APP_SECRET   앱키·시크릿 (서버 실행 시 필수)
  KIWOOM_IS_MOCK=true                  모의투자 서버 (--mock 과 같음, 기본 false = 실전)
  {TOOLSETS_ENV_VAR}=market,chart     노출할 모듈 (--toolsets 와 같음, 기본 전부)
  {LIVE_ORDERS_ENV_VAR}=true  실전 계좌에서 주문 도구 노출 (기본 false)

toolset 이름: {", ".join(TOOLSET_NAMES)}

실전 계좌(KIWOOM_IS_MOCK=false)에서는 {LIVE_ORDERS_ENV_VAR}=true 를 켜기 전까지
주문 도구가 등록되지 않습니다. 이 CLI 에는 그 가드를 켜는 옵션이 없습니다.
"""


def _toolsets_arg(value: str) -> frozenset[str]:
    """Like :func:`parse_toolsets`, but "all" is spelled out so that an explicit
    ``--toolsets all`` still overrides the environment variable."""
    try:
        parsed = parse_toolsets(value)
    except ValueError as exc:
        raise argparse.ArgumentTypeError(str(exc)) from exc
    return frozenset(TOOLSET_NAMES) if parsed is None else parsed


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="kiwoom-client-mcp",
        description="키움증권 REST API MCP 서버 (stdio). 인자 없이 실행하면 서버를 띄웁니다.",
        epilog=_EPILOG,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("--version", action="version", version=f"%(prog)s {__version__}")
    parser.add_argument(
        "--mock",
        action="store_true",
        help="모의투자 서버에 연결 (KIWOOM_IS_MOCK=true 와 같음)",
    )
    parser.add_argument(
        "--toolsets",
        type=_toolsets_arg,
        metavar="LIST",
        help=f"노출할 모듈, 쉼표 구분 ({TOOLSETS_ENV_VAR} 보다 우선). 예: market,chart,account",
    )

    sub = parser.add_subparsers(dest="command", metavar="{config}")
    config = sub.add_parser(
        "config",
        help="MCP 클라이언트 설정 스니펫 출력 (키는 placeholder)",
        description=(
            "붙여넣을 설정을 stdout 에, 넣을 위치 안내를 stderr 에 출력합니다. "
            "키는 placeholder 이고, 실주문 opt-in 은 넣지 않습니다."
        ),
    )
    config.add_argument("client", choices=CLIENTS)
    mode = config.add_mutually_exclusive_group()
    mode.add_argument(
        "--mock",
        dest="config_mock",
        action="store_true",
        default=True,
        help="KIWOOM_IS_MOCK=true 로 출력 (기본)",
    )
    mode.add_argument(
        "--live",
        dest="config_mock",
        action="store_false",
        help="KIWOOM_IS_MOCK=false (실전 조회용) 로 출력. 주문 도구는 여전히 꺼진 상태",
    )
    config.add_argument(
        "--toolsets",
        dest="config_toolsets",
        type=_toolsets_arg,
        metavar="LIST",
        help="KIWOOM_MCP_TOOLSETS 값으로 넣을 모듈 목록",
    )
    config.add_argument(
        "--launcher",
        choices=LAUNCHERS,
        default="uvx",
        help="uvx: 설치 없이 실행 (기본) / installed: PATH 의 kiwoom-client-mcp",
    )
    return parser


def _print_config(args: argparse.Namespace) -> None:
    chosen = args.config_toolsets
    toolsets = None if chosen is None or chosen == set(TOOLSET_NAMES) else sorted(chosen)
    snippet = render(args.client, mock=args.config_mock, toolsets=toolsets, launcher=args.launcher)
    print(snippet.note, file=sys.stderr)
    sys.stdout.write(snippet.body)


def main(argv: Sequence[str] | None = None) -> None:
    """Entry point for the ``kiwoom-client-mcp`` console script."""
    args = build_parser().parse_args(argv)

    if args.command == "config":
        _print_config(args)
        return

    app_key = os.environ.get("KIWOOM_APP_KEY")
    app_secret = os.environ.get("KIWOOM_APP_SECRET")
    if not app_key or not app_secret:
        print(
            "Error: KIWOOM_APP_KEY and KIWOOM_APP_SECRET environment variables must be set.\n"
            "설정 예시는 `kiwoom-client-mcp config claude-code` 로 볼 수 있습니다.",
            file=sys.stderr,
        )
        sys.exit(1)

    is_mock = args.mock or os.environ.get("KIWOOM_IS_MOCK", "false").strip().lower() == "true"
    toolsets: frozenset[str] | None
    if args.toolsets is not None:
        toolsets = None if args.toolsets == set(TOOLSET_NAMES) else args.toolsets
    else:
        try:
            toolsets = toolsets_from_env()
        except ValueError as exc:
            print(f"Error: {exc}", file=sys.stderr)
            sys.exit(1)

    try:
        from kiwoom_client.mcp.server import run_server
    except ImportError as exc:
        print(
            f"Error: MCP 서버에는 mcp 패키지가 필요합니다 ({exc}).\n"
            "  pip install 'kiwoom-client[mcp]'\n"
            "  또는 uvx --from 'kiwoom-client[mcp]' kiwoom-client-mcp",
            file=sys.stderr,
        )
        sys.exit(1)

    run_server(app_key=app_key, app_secret=app_secret, is_mock=is_mock, toolsets=toolsets)
