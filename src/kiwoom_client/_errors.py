"""Root of the library's exception hierarchy (no imports, so anyone can use it).

The public view of the whole hierarchy is :mod:`kiwoom_client.errors`.
"""

from __future__ import annotations

import re

__all__ = ["KiwoomError", "parse_error_code"]


class KiwoomError(Exception):
    """Base class of every error kiwoom-client raises on purpose.

    ``except KiwoomError`` catches API errors, token errors and WebSocket
    errors alike. Subclassing it changes nothing for code that already
    catches ``KiwoomAPIError``, ``KiwoomAuthError`` or ``Exception``.
    """


# Kiwoom puts its 4-digit error code inside return_msg, e.g.
#   "인증에 실패했습니다[8005:Token이 유효하지 않습니다]"
_ERROR_CODE = re.compile(r"\[\s*(\d{4})\s*:")


def parse_error_code(message: object) -> int | None:
    """Pull Kiwoom's 4-digit error code (``[8005:...]``) out of a message."""
    if not isinstance(message, str):
        return None
    match = _ERROR_CODE.search(message)
    return int(match.group(1)) if match else None
