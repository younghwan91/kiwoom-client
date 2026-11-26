"""Keep the command-line tools from crashing on a legacy console encoding.

Windows uses the ANSI code page for piped or redirected output: cp949 on
Korean Windows (Hangul, but no ``—`` or ``✓``) and cp1252 elsewhere (no
Hangul at all). Python's default ``errors="strict"`` then turns ``--help``
into a ``UnicodeEncodeError`` traceback. Swapping in ``errors="replace"``
prints ``?`` for the few characters the code page lacks instead.
"""

from __future__ import annotations

import codecs
import io
import sys


def tolerate_legacy_encoding() -> None:
    """Make ``sys.stdout``/``sys.stderr`` replace characters they cannot encode.

    UTF-8 streams and streams that are not text wrappers are left alone, so
    the MCP stdio transport (which writes to ``sys.stdout.buffer``) and test
    capture are unaffected.
    """
    for stream in (sys.stdout, sys.stderr):
        if not isinstance(stream, io.TextIOWrapper):
            continue
        try:
            if codecs.lookup(stream.encoding).name == "utf-8":
                continue
            stream.reconfigure(errors="replace")
        except (LookupError, ValueError, OSError):
            continue
