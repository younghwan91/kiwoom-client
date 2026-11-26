"""CLIs must not crash on a non-UTF-8 console (Windows cp949 / cp1252).

On Windows, output that is piped or redirected uses the ANSI code page. Korean
Windows is cp949, which has Hangul but not ``—`` or ``✓``; an English runner is
cp1252, which has no Hangul. ``PYTHONIOENCODING`` reproduces both on any OS.
"""

from __future__ import annotations

import os
import subprocess
import sys

import pytest

COMMANDS = [
    ["-m", "kiwoom_client", "--help"],
    ["-m", "kiwoom_client", "endpoints", "체결"],
    ["-m", "kiwoom_client.mcp", "--help"],
    ["-m", "kiwoom_client.mcp", "config", "claude-desktop"],
]


@pytest.mark.parametrize("encoding", ["cp949", "cp1252"])
@pytest.mark.parametrize("argv", COMMANDS, ids=" ".join)
def test_cli_survives_legacy_console_encoding(argv, encoding):
    env = {**os.environ, "PYTHONIOENCODING": encoding}
    proc = subprocess.run(
        [sys.executable, *argv], capture_output=True, env=env, timeout=60, check=False
    )
    assert proc.returncode == 0, proc.stderr.decode(encoding, "replace")
    assert proc.stdout.strip()
