"""Masking for anything that might end up in a repr, a log line or a traceback.

App secrets and access tokens are never shown, not even partially. App keys
show their last four characters (enough to tell two keys apart) only when
they are long enough that four characters reveal little.
"""

from __future__ import annotations

__all__ = ["mask_secret", "server_label", "token_state"]

_MASK = "****"


def mask_secret(value: str | None, visible: int = 4) -> str:
    """``"****AbCd"`` for a long value, ``"****"`` for a short one, ``"None"`` if unset.

    Pass ``visible=0`` for secrets and tokens — nothing is revealed.
    """
    if value is None:
        return "None"
    if not value:
        return "''"
    if visible <= 0 or len(value) < 16:
        return _MASK
    return _MASK + value[-visible:]


def token_state(token: str | None) -> str:
    """``"set"`` or ``"none"`` — the token itself is never shown."""
    return "set" if token else "none"


def server_label(base_url: str) -> str:
    """``"mock"``, ``"live"`` or ``"custom"`` for a REST base URL."""
    if "mockapi.kiwoom.com" in base_url:
        return "mock"
    if "api.kiwoom.com" in base_url:
        return "live"
    return "custom"
