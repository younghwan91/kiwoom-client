"""``kiwoom-client-mcp`` command line.

::

    kiwoom-client-mcp                      # stdio MCP 서버 실행 (기본)
    kiwoom-client-mcp --demo               # 키 없이 가상 데이터로 (연결 없음)
    kiwoom-client-mcp --mock --toolsets market,chart
    kiwoom-client-mcp config claude-code   # 클라이언트 설정 스니펫 출력
    kiwoom-client-mcp doctor               # 설정 점검 (키·네트워크 없이)
    kiwoom-client-mcp --version

``--help``, ``--version`` and ``config`` need neither API keys nor the ``mcp``
extra, so they work right after ``pip install kiwoom-client`` or via ``uvx``.
The ``mcp`` package is imported only when the server actually starts (or
``doctor`` counts the tools). ``doctor`` needs no keys and makes no network
call unless ``--check-auth`` is given.
"""

from __future__ import annotations

import argparse
import os
import sys
from collections.abc import Mapping, Sequence

from kiwoom_client import __version__
from kiwoom_client._console import tolerate_legacy_encoding
from kiwoom_client._env import ENV_IS_MOCK, parse_bool
from kiwoom_client.mcp.client_config import CLIENTS, LAUNCHERS, render
from kiwoom_client.mcp.demo import ENV_VAR as DEMO_ENV_VAR
from kiwoom_client.mcp.demo import demo_from_env
from kiwoom_client.mcp.guard import ENV_VAR as LIVE_ORDERS_ENV_VAR
from kiwoom_client.mcp.guard import READ_ONLY_ENV, read_only
from kiwoom_client.mcp.masking import ENV_VAR as MASK_ENV_VAR
from kiwoom_client.mcp.masking import mask_from_env
from kiwoom_client.mcp.modes import DISCOVERY, FULL, mode_from_env
from kiwoom_client.mcp.modes import ENV_VAR as MODE_ENV_VAR
from kiwoom_client.mcp.orders.policy import REQUIRE_CONFIRM_ENV, OrderPolicy
from kiwoom_client.mcp.response_size import ENV_VAR as MAX_ROWS_ENV_VAR
from kiwoom_client.mcp.response_size import max_rows_from_env, parse_max_rows
from kiwoom_client.mcp.toolsets import ENV_VAR as TOOLSETS_ENV_VAR
from kiwoom_client.mcp.toolsets import TOOLSET_NAMES, parse_toolsets, toolsets_from_env

_EPILOG = f"""\
환경변수:
  KIWOOM_APP_KEY / KIWOOM_APP_SECRET   앱키·시크릿 (서버 실행 시 필수)
  KIWOOM_IS_MOCK=true                  모의투자 서버 (--mock 과 같음, 기본 false = 실전;
                                       true/false·1/0·yes/no 외의 값은 시작 시 에러)
  {DEMO_ENV_VAR}=true              데모 모드 (--demo 와 같음): 키 불필요, 가상 데이터,
                                       어디에도 연결하지 않음, 주문은 메모리 안 종이 거래
  {TOOLSETS_ENV_VAR}=market,chart     노출할 모듈 (--toolsets 와 같음, 기본 전부)
  {MODE_ENV_VAR}=smart                기본. 고수준 도구 + 메타 도구 3개(search_tools 등)
  {MODE_ENV_VAR}=full                 TR 도구 ~180개 전부 노출 (--full 과 같음, 0.5.x 기본)
  {MODE_ENV_VAR}=discovery            메타 도구 3개만 노출 (--discovery 와 같음)
  {MAX_ROWS_ENV_VAR}=50                리스트 응답 기본 행 수 제한 (--max-rows 와 같음)
  {LIVE_ORDERS_ENV_VAR}=true  실전 계좌에서 주문 도구 노출 (기본 false)
  {REQUIRE_CONFIRM_ENV}=true    TR 주문 도구에 order_preview 의 confirm_token 요구
                                       (기본: 실전 true, 모의 false)
  KIWOOM_MCP_MAX_ORDER_AMOUNT=1000000  주문 1건 금액 한도(원)  ┐
  KIWOOM_MCP_MAX_ORDER_QTY=100         주문 1건 수량 한도(주)  │ 미설정 = 제한 없음.
  KIWOOM_MCP_ALLOWED_STOCKS=005930,... 주문 가능 종목코드      │ 미리보기와 전송 직전
  KIWOOM_MCP_DAILY_ORDER_LIMIT=20      하루 주문 수(프로세스)  ┘ 둘 다에서 강제
  KIWOOM_MCP_DUPLICATE_WINDOW=10       같은 주문을 N초 안에 다시 보내면 거부 (기본 10, 0 = 끔)
  KIWOOM_MCP_AUDIT_LOG=PATH            주문 감사 로그 JSONL (기본 ~/.kiwoom-client/mcp-audit.jsonl,
                                       off = 끔. 키·토큰 없음, 계좌번호 마스킹)
  {READ_ONLY_ENV}=true          주문 도구를 하나도 등록하지 않음 (모의투자 포함)
  {MASK_ENV_VAR}=false      응답의 계좌번호를 가리지 않음 (기본 true = 끝 4자리만)

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


def _max_rows_arg(value: str) -> int:
    try:
        parsed = parse_max_rows(value)
    except ValueError as exc:
        raise argparse.ArgumentTypeError(str(exc)) from exc
    if parsed is None:
        raise argparse.ArgumentTypeError("max-rows 는 양의 정수여야 합니다")
    return parsed


def resolve_is_mock(*, flag: bool, env: Mapping[str, str] | None = None) -> bool:
    """``--mock`` wins; else ``KIWOOM_IS_MOCK`` parsed like ``KiwoomAPI.from_env()``.

    Unset or empty means live (``False``), the same default as everywhere else.
    A value that is not a recognised boolean (e.g. ``"ture"``) raises instead
    of silently connecting to the live server.
    """
    if flag:
        return True
    source = os.environ if env is None else env
    value = source.get(ENV_IS_MOCK, "")
    return parse_bool(value) if value.strip() else False


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
        "--demo",
        action="store_true",
        help=(
            f"키 없이 가상 데이터로 체험 ({DEMO_ENV_VAR}=true 와 같음). 어디에도 연결하지 않고 "
            "주문은 메모리 안의 종이 거래. 키가 설정돼 있어도 쓰지 않는다"
        ),
    )
    parser.add_argument(
        "--toolsets",
        type=_toolsets_arg,
        metavar="LIST",
        help=f"노출할 모듈, 쉼표 구분 ({TOOLSETS_ENV_VAR} 보다 우선). 예: market,chart,account",
    )

    listing = parser.add_mutually_exclusive_group()
    listing.add_argument(
        "--full",
        action="store_const",
        const=FULL,
        dest="mode",
        help=(
            "TR 도구 ~180개를 전부 목록에 올린다 "
            f"({MODE_ENV_VAR}=full 과 같음). 기본(smart)은 고수준 도구 + 메타 도구 3개"
        ),
    )
    listing.add_argument(
        "--discovery",
        action="store_const",
        const=DISCOVERY,
        dest="mode",
        help=(
            "search_tools/describe_tool/call_tool 3개만 노출 "
            f"({MODE_ENV_VAR}=discovery 와 같음). 컨텍스트 최소"
        ),
    )
    parser.add_argument(
        "--max-rows",
        type=_max_rows_arg,
        metavar="N",
        help=(
            f"리스트 응답을 기본 N행으로 자른다 ({MAX_ROWS_ENV_VAR} 와 같음, 기본 무제한). "
            "도구 호출마다 max_rows 로 바꿀 수 있다"
        ),
    )

    sub = parser.add_subparsers(dest="command", metavar="{config,doctor}")
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
    config_listing = config.add_mutually_exclusive_group()
    config_listing.add_argument(
        "--full",
        dest="config_mode",
        action="store_const",
        const=FULL,
        help=f"{MODE_ENV_VAR}=full 을 넣는다 (TR 도구 전부)",
    )
    config_listing.add_argument(
        "--discovery",
        dest="config_mode",
        action="store_const",
        const=DISCOVERY,
        help=f"{MODE_ENV_VAR}=discovery 를 넣는다",
    )
    config.add_argument(
        "--launcher",
        choices=LAUNCHERS,
        default="uvx",
        help="uvx: 설치 없이 실행 (기본) / installed: PATH 의 kiwoom-client-mcp",
    )
    doctor = sub.add_parser(
        "doctor",
        help="설정 점검 — 버전·환경변수(값은 안 보임)·모드·가드·도구 수 (키·네트워크 불필요)",
        description=(
            "서버를 띄우지 않고 설정을 점검합니다. 환경변수는 있는지만 보여 주고 값은 출력하지 "
            "않습니다. 기본은 네트워크 호출이 없습니다. 서버 옵션(--mock, --toolsets, --full, "
            "--discovery, --max-rows)은 doctor 앞에 씁니다: kiwoom-client-mcp --mock doctor"
        ),
    )
    doctor.add_argument(
        "--check-auth",
        action="store_true",
        help="앱키로 토큰을 한 번 발급해 본다 (키움 서버에 요청 1회, 토큰 폐기는 하지 않음)",
    )
    return parser


def _doctor(args: argparse.Namespace) -> None:
    from kiwoom_client.mcp.doctor import Overrides, run

    flags = Overrides(
        mock=args.mock,
        toolsets=None if args.toolsets == set(TOOLSET_NAMES) else args.toolsets,
        toolsets_all=args.toolsets == set(TOOLSET_NAMES),
        mode=args.mode,
        max_rows=args.max_rows,
    )
    sys.exit(run(env=os.environ, flags=flags, check_auth=args.check_auth))


def _print_config(args: argparse.Namespace) -> None:
    chosen = args.config_toolsets
    toolsets = None if chosen is None or chosen == set(TOOLSET_NAMES) else sorted(chosen)
    snippet = render(
        args.client,
        mock=args.config_mock,
        toolsets=toolsets,
        launcher=args.launcher,
        mode=args.config_mode,
    )
    print(snippet.note, file=sys.stderr)
    sys.stdout.write(snippet.body)


def main(argv: Sequence[str] | None = None) -> None:
    """Entry point for the ``kiwoom-client-mcp`` console script."""
    tolerate_legacy_encoding()
    args = build_parser().parse_args(argv)

    if args.command == "config":
        _print_config(args)
        return
    if args.command == "doctor":
        _doctor(args)

    try:
        demo = args.demo or demo_from_env()
    except ValueError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        sys.exit(1)

    app_key = os.environ.get("KIWOOM_APP_KEY")
    app_secret = os.environ.get("KIWOOM_APP_SECRET")
    if demo:
        if app_key or app_secret:
            print(
                "kiwoom-client-mcp: 데모 모드라 설정된 앱키는 쓰지 않습니다 (데모가 우선, "
                "키움에 연결하지 않음).",
                file=sys.stderr,
            )
        app_key = app_secret = ""
        is_mock = True  # paper semantics; the demo client connects nowhere
    else:
        if not app_key or not app_secret:
            print(
                "Error: KIWOOM_APP_KEY and KIWOOM_APP_SECRET environment variables must be set.\n"
                "설정 예시는 `kiwoom-client-mcp config claude-code` 로 볼 수 있습니다.\n"
                "키 없이 가상 데이터로 체험하려면: kiwoom-client-mcp --demo",
                file=sys.stderr,
            )
            sys.exit(1)

        try:
            is_mock = resolve_is_mock(flag=args.mock)
        except ValueError as exc:
            print(f"Error: {exc}", file=sys.stderr)
            sys.exit(1)
    toolsets: frozenset[str] | None
    if args.toolsets is not None:
        toolsets = None if args.toolsets == set(TOOLSET_NAMES) else args.toolsets
    else:
        try:
            toolsets = toolsets_from_env()
        except ValueError as exc:
            print(f"Error: {exc}", file=sys.stderr)
            sys.exit(1)

    mode = args.mode
    if mode is None:
        try:
            mode = mode_from_env()
        except ValueError as exc:
            print(f"Error: {exc}", file=sys.stderr)
            sys.exit(1)

    try:
        # run_server reads these again; fail fast here on a bad value
        OrderPolicy.from_env(is_mock=is_mock)
        read_only()
        mask_from_env()
    except ValueError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        sys.exit(1)

    max_rows = args.max_rows
    if max_rows is None:
        try:
            max_rows = max_rows_from_env()
        except ValueError as exc:
            print(f"Error: {MAX_ROWS_ENV_VAR}: {exc}", file=sys.stderr)
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

    run_server(
        app_key=app_key,
        app_secret=app_secret,
        is_mock=is_mock,
        toolsets=toolsets,
        max_rows=max_rows,
        mode=mode,
        **({"demo": True} if demo else {}),
    )
