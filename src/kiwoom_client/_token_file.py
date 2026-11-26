"""Opt-in on-disk token cache shared by processes that use the same file.

Backs ``token_cache=`` on :class:`~kiwoom_client.auth.KiwoomAuth`,
:class:`~kiwoom_client.KiwoomAPI` and their async twins, and the
``KIWOOM_TOKEN_CACHE`` variable read by ``from_env()``.

File layout (JSON, mode 0600 where the OS supports it)::

    {"v": 1, "tokens": {"<id>": {"token": "...", "expires_at": 1767225600.0}}}

``<id>`` is a SHA-256 of the server URL and the app key, so one file can hold
tokens for several keys and for the live and mock servers without storing the
app key itself. The app secret never touches the file.

Every failure here (unreadable, corrupt, read-only location) is logged and
swallowed: the cache is a convenience and must never stop a request.
"""

from __future__ import annotations

import contextlib
import hashlib
import json
import logging
import os
import tempfile
import time
from pathlib import Path
from typing import Any

logger = logging.getLogger("kiwoom_client")

ENV_TOKEN_CACHE = "KIWOOM_TOKEN_CACHE"

_VERSION = 1


def entry_id(base_url: str, app_key: str) -> str:
    return hashlib.sha256(f"{base_url.rstrip('/')}\n{app_key}".encode()).hexdigest()[:32]


def _read(path: Path) -> dict[str, dict[str, Any]]:
    """The live entries in ``path``; anything unusable reads as empty."""
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        return {}
    except (OSError, ValueError) as exc:
        logger.warning("토큰 캐시를 읽지 못해 무시합니다 (%s): %s", path, exc)
        return {}
    tokens = data.get("tokens") if isinstance(data, dict) else None
    if not isinstance(tokens, dict):
        return {}
    now = time.time()
    live: dict[str, dict[str, Any]] = {}
    for key, entry in tokens.items():
        if not isinstance(entry, dict):
            continue
        token, expires_at = entry.get("token"), entry.get("expires_at")
        if not (isinstance(token, str) and token and isinstance(expires_at, (int, float))):
            continue
        if expires_at > now:
            live[str(key)] = {"token": token, "expires_at": float(expires_at)}
    return live


def _write(path: Path, tokens: dict[str, dict[str, Any]]) -> None:
    """Replace ``path`` atomically with a private (0600) file."""
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        fd, tmp = tempfile.mkstemp(prefix=".token-", suffix=".tmp", dir=path.parent)
        try:
            with os.fdopen(fd, "w", encoding="utf-8") as fh:
                json.dump({"v": _VERSION, "tokens": tokens}, fh)
            os.chmod(tmp, 0o600)  # mkstemp already uses 0600; be explicit
            os.replace(tmp, path)
        except BaseException:
            with contextlib.suppress(OSError):
                os.unlink(tmp)
            raise
    except OSError as exc:
        logger.warning("토큰 캐시를 쓰지 못했습니다 (%s): %s", path, exc)


def load(path: Path, key: str) -> tuple[str, float] | None:
    entry = _read(path).get(key)
    if entry is None:
        return None
    return entry["token"], entry["expires_at"]


def save(path: Path, key: str, token: str, expires_at: float) -> None:
    tokens = _read(path)
    tokens[key] = {"token": token, "expires_at": expires_at}
    _write(path, tokens)


def drop(path: Path, key: str) -> None:
    tokens = _read(path)
    if key in tokens or path.exists():
        tokens.pop(key, None)
        _write(path, tokens)
