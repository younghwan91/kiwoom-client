"""`.claude/hooks/live_order_guard.py`(PreToolUse) 의 차단 범위를 고정한다.

훅은 에이전트가 실계좌 키를 불러 주문·토큰 폐기를 실행하지 못하게 막는다. 여기 적힌 차단 케이스는
하나도 통과로 바뀌면 안 된다. 통과 케이스는 평범한 개발 명령이 오탐으로 막히지 않는지 본다
(워크트리에서 `cd <wt> && uv run pytest tests/x.py` 가 세션 cwd 의 옛 파일 때문에 막히던 것).

훅을 서브프로세스로 돌려 stdin JSON → stdout 결정만 본다. 아무것도 실행하지 않는다.
키 로드 표시(ENV·KEY·SECRET·ENV_FILE)는 조각을 이어 만든다 — 이 파일을 경로로 넘겨
`uv run pytest tests/test_live_order_guard_hook.py` 를 돌릴 때 훅이 이 파일 글자에 걸리지 않게.
"""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import pytest

ENV = "." + "env"
KEY = "KIWOOM_APP" + "_KEY"
SECRET = "KIWOOM_APP" + "_SECRET"
ENV_FILE = "--env" + "-file"

HOOK = Path(__file__).resolve().parent.parent / ".claude" / "hooks" / "live_order_guard.py"

# 키 로드 + 토큰 폐기/주문이 같이 든 스크립트 (실행되지 않는다 — 훅이 글자만 읽는다).
DANGEROUS = f'load_dotenv("{ENV}")\napi = KiwoomAPI.from_env()\napi.logout()\n'
ORDERING = f'import os\nos.environ["{KEY}"]\napi.order.buy_order(stk_cd="005930")\n'
BENIGN = "def test_ok():\n    assert 1 + 1 == 2\n"


def run_hook(payload: dict) -> str:
    return subprocess.run(
        [sys.executable, str(HOOK)], input=json.dumps(payload), capture_output=True,
        text=True, timeout=10, check=True,
    ).stdout


def decide(command: str, cwd: Path) -> str:
    out = run_hook({"tool_name": "Bash", "tool_input": {"command": command}, "cwd": str(cwd)})
    if not out.strip():
        return "allow"
    return json.loads(out)["hookSpecificOutput"]["permissionDecision"]


@pytest.fixture
def tree(tmp_path: Path) -> Path:
    """세션 cwd(main) 와 워크트리(wt) 두 체크아웃."""
    for name in ("main", "wt"):
        (tmp_path / name / "tests").mkdir(parents=True)
    return tmp_path


def write(path: Path, text: str) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
    return path


# --- 계속 막혀야 하는 것 -------------------------------------------------------------


@pytest.mark.parametrize(
    "command",
    [
        f"{KEY}=x python -c 'api.order.buy_order(stk_cd=\"005930\")'",
        f"set -a; . ./{ENV}; set +a; python -c 'api.logout()'",
        f"uv run python -c 'import dotenv; dotenv.load_dotenv(\"{ENV}\"); api.order.sell_order()'",
        f"python -c 'api.credit_order.margin_buy_order()' {ENV_FILE} ~/x/{ENV}",
        f"uv run python -c '{SECRET}; c.request(\"/api/dostk/ordr\", \"kt10000\", {{}})'",
        f"python -c 'auth.revoke_token()'  # {KEY}",
    ],
)
def test_inline_key_load_with_order_or_logout_is_denied(command, tree):
    assert decide(command, tree / "main") == "deny"


@pytest.mark.parametrize(
    "command",
    [
        "KIWOOM_MCP_ALLOW_LIVE_ORDERS=true kiwoom-client-mcp",
        "export KIWOOM_MCP_ALLOW_LIVE_ORDERS=true",
        "env KIWOOM_MCP_ALLOW_LIVE_ORDERS=TRUE uvx kiwoom-client-mcp",
        "FOO=1 KIWOOM_MCP_ALLOW_LIVE_ORDERS='true' kiwoom-client-mcp",
        "KIWOOM_MCP_ALLOW_LIVE_ORDERS=\"true\" kiwoom-client-mcp",
        "ls; KIWOOM_MCP_ALLOW_LIVE_ORDERS=true kiwoom-client-mcp",
    ],
)
def test_mcp_live_order_opt_in_is_denied(command, tree):
    assert decide(command, tree / "main") == "deny"


@pytest.mark.parametrize(
    "command",
    [
        f"set -a; . ./{ENV}; curl -X POST https://api.kiwoom.com/api/dostk/ordr -d '{{}}'",
        f"curl -H \"${KEY}\" https://api.kiwoom.com/oauth2/revoke",
        f"source {ENV} && wget --post-data x https://api.kiwoom.com/api/dostk/crdordr",
    ],
)
def test_direct_http_order_or_revoke_with_keys_is_denied(command, tree):
    assert decide(command, tree / "main") == "deny"


def test_script_in_cwd_is_read(tree):
    write(tree / "main" / "run_live.py", DANGEROUS)
    assert decide("uv run python run_live.py", tree / "main") == "deny"
    assert decide("python3 ./run_live.py --flag", tree / "main") == "deny"


def test_cd_then_relative_script_is_read_in_cd_target(tree):
    write(tree / "wt" / "scripts" / "live.py", ORDERING)
    assert decide(f"cd {tree / 'wt'} && python scripts/live.py", tree / "main") == "deny"
    assert decide("cd ../wt && uv run python scripts/live.py", tree / "main") == "deny"


def test_relative_cd_chain_is_followed(tree):
    write(tree / "wt" / "sub" / "live.py", DANGEROUS)
    assert decide("cd ../wt && cd sub && python live.py", tree / "main") == "deny"


def test_falls_back_to_cwd_when_cd_target_lacks_the_file(tree):
    write(tree / "main" / "live.py", DANGEROUS)
    assert decide(f"cd {tree / 'wt'} && python live.py", tree / "main") == "deny"


def test_absolute_script_path_is_read(tree):
    script = write(tree / "elsewhere" / "live.py", DANGEROUS)
    assert decide(f"python {script}", tree / "main") == "deny"


def test_dangerous_wt_file_denied_even_if_cwd_copy_is_benign(tree):
    write(tree / "main" / "tests" / "test_x.py", BENIGN)
    write(tree / "wt" / "tests" / "test_x.py", DANGEROUS)
    assert decide(f"cd {tree / 'wt'} && uv run pytest tests/test_x.py", tree / "main") == "deny"


# --- 막히면 안 되는 것 -----------------------------------------------------------------


def test_worktree_file_wins_over_stale_session_cwd_copy(tree):
    """세션 cwd 의 옛 파일이 위험해 보여도, 실제로 실행되는 건 cd 대상의 파일이다."""
    write(tree / "main" / "tests" / "test_x.py", DANGEROUS)
    write(tree / "wt" / "tests" / "test_x.py", BENIGN)
    command = f"cd {tree / 'wt'} && uv run --extra dev pytest tests/test_x.py -q"
    assert decide(command, tree / "main") == "allow"


@pytest.mark.parametrize(
    "command",
    [
        "uv run --extra dev --extra mcp pytest tests/ -q",
        "uv run --extra dev --extra mcp ruff check src tests examples",
        f"grep -rn 'logout(' src/ {ENV}.example",
        "git commit -m 'KIWOOM_MCP_ALLOW_LIVE_ORDERS=true 문서화'",
        "cat > notes.md <<'EOF'\nKIWOOM_MCP_ALLOW_LIVE_ORDERS=true\nEOF",
        "python -c 'print(1)'",
    ],
)
def test_ordinary_commands_are_allowed(command, tree):
    assert decide(command, tree / "main") == "allow"


def test_non_bash_tools_are_ignored(tree):
    out = run_hook({"tool_name": "Read", "tool_input": {"file_path": ENV}, "cwd": str(tree)})
    assert out.strip() == ""


@pytest.mark.parametrize("encoding", ["cp1252", "cp949"])
def test_deny_survives_legacy_console_encoding(encoding):
    """The deny reason is Korean. On a cp1252 console printing it used to raise, the
    hook's catch-all swallowed the error and the command was allowed (fail-open)."""
    import os

    payload = {
        "tool_name": "Bash",
        # Hangul in the command too: stdin must be read as UTF-8 whatever the locale.
        "tool_input": {"command": "echo 주문 && export KIWOOM_MCP_ALLOW_LIVE_ORDERS=true"},
        "cwd": ".",
    }
    proc = subprocess.run(
        [sys.executable, str(HOOK)], input=json.dumps(payload, ensure_ascii=False).encode(),
        capture_output=True, timeout=10, check=True,
        env={**os.environ, "PYTHONIOENCODING": encoding},
    )
    assert json.loads(proc.stdout)["hookSpecificOutput"]["permissionDecision"] == "deny"
