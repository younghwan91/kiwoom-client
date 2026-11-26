"""OAuth2 authentication for Kiwoom REST API."""

from __future__ import annotations

import asyncio
import os
import threading
import time
from datetime import datetime
from pathlib import Path
from typing import Any, Protocol, runtime_checkable

import httpx

from kiwoom_client import _token_file
from kiwoom_client._errors import KiwoomError, error_hint, parse_error_code
from kiwoom_client._redact import mask_secret, token_state


class KiwoomAuthError(KiwoomError):
    """Token issuance or revocation failed.

    Attributes:
        error_code: Kiwoom's 4-digit code from the message (``[8030:...]``),
            or None.
        hint: One-line next step (e.g. which ``is_mock`` to use), or None.
            Also appended to ``str(exc)``.
    """

    def __init__(self, *args: object, hint: str | None = None) -> None:
        self.error_code: int | None = parse_error_code(args[0]) if args else None
        self.hint = hint
        if hint and args:
            args = (f"{args[0]}\n  힌트: {hint}", *args[1:])
        super().__init__(*args)


def _auth_failure(
    prefix: str, detail: str, return_code: object, base_url: str | None
) -> KiwoomAuthError:
    """Build a KiwoomAuthError with a hint derived from Kiwoom's error code."""
    hint = error_hint(parse_error_code(detail), return_code, base_url)
    return KiwoomAuthError(f"{prefix}: {detail}", hint=hint)


def _http_failure(prefix: str, exc: httpx.HTTPError, base_url: str | None) -> KiwoomAuthError:
    """Like :func:`_auth_failure` for transport/status errors.

    For an HTTP error status the body's ``return_msg`` (if any) is added to the
    message, since httpx's own text doesn't include it.
    """
    detail = str(exc)
    return_code: object = None
    if isinstance(exc, httpx.HTTPStatusError):
        try:
            body = exc.response.json()
        except ValueError:
            body = None
        if isinstance(body, dict) and body.get("return_msg"):
            detail = f"{detail} — {body['return_msg']}"
            return_code = body.get("return_code")
    return _auth_failure(prefix, detail, return_code, base_url)


@runtime_checkable
class TokenProvider(Protocol):
    """Anything that can hand :class:`BaseClient` a usable access token.

    :class:`KiwoomAuth` implements this. Supply your own to share a single
    token across processes (Redis, a file, a sidecar service).
    """

    def get_valid_token(self) -> str:
        """Return a token that is valid now, issuing one if needed."""

    def refresh_token(self) -> str:
        """Discard the cached token and issue a fresh one."""


@runtime_checkable
class AsyncTokenProvider(Protocol):
    """Async counterpart of :class:`TokenProvider`."""

    async def get_valid_token(self) -> str:
        """Return a token that is valid now, issuing one if needed."""

    async def refresh_token(self) -> str:
        """Discard the cached token and issue a fresh one."""


class _TokenCache:
    """Token + expiry bookkeeping shared by the sync and async auth clients."""

    DEFAULT_EXPIRY_MARGIN = 60.0

    def __init__(
        self,
        expiry_margin: float = DEFAULT_EXPIRY_MARGIN,
        token_cache: str | os.PathLike[str] | None = None,
    ) -> None:
        self.expiry_margin = expiry_margin
        self._token: str | None = None
        self._expires_at: float | None = None
        self.token_cache: Path | None = Path(token_cache) if token_cache is not None else None

    def _cache_key(self) -> str:
        return _token_file.entry_id(getattr(self, "base_url", ""), getattr(self, "app_key", ""))

    def _load_cached(self) -> bool:
        """Adopt a still-valid token from ``token_cache``; True if one was found."""
        if self.token_cache is None or self._token is not None:
            return False
        found = _token_file.load(self.token_cache, self._cache_key())
        if found is None:
            return False
        self._token, self._expires_at = found
        if self._is_expiring():
            self._token = self._expires_at = None
            return False
        return True

    def __repr__(self) -> str:
        # Never the secret or the token: see kiwoom_client._redact.
        return (
            f"{type(self).__name__}(base_url={getattr(self, 'base_url', None)!r}, "
            f"app_key={mask_secret(getattr(self, 'app_key', None))!r}, "
            f"app_secret={mask_secret(getattr(self, 'app_secret', None), 0)!r}, "
            f"token={token_state(self._token)!r}, expires_at={self._expires_at!r})"
        )

    @property
    def token(self) -> str | None:
        """The cached access token, or None if never issued / revoked."""
        return self._token

    @property
    def expires_at(self) -> float | None:
        """Unix timestamp of token expiry, or None if the API didn't say."""
        return self._expires_at

    def _store(self, data: dict[str, Any]) -> str:
        """Cache the token from a token response, or raise if there isn't one."""
        token = data.get("token") or data.get("access_token")
        if not token:
            msg = data.get("return_msg") or "응답에 토큰이 없습니다"
            raise _auth_failure(
                "토큰 발급 실패", msg, data.get("return_code"), getattr(self, "base_url", None)
            )
        self._token = token
        self._expires_at = self._parse_expiry(data)
        if self.token_cache is not None:
            if self._expires_at is None:
                # Without an expiry a later process could not tell if it is still good.
                _token_file.drop(self.token_cache, self._cache_key())
            else:
                _token_file.save(self.token_cache, self._cache_key(), token, self._expires_at)
        return token

    def _forget(self, token: str) -> None:
        """After revoking ``token``: drop it from memory and from ``token_cache``."""
        if token == self._token:
            self._clear()
        elif self.token_cache is not None:
            found = _token_file.load(self.token_cache, self._cache_key())
            if found is not None and found[0] == token:
                _token_file.drop(self.token_cache, self._cache_key())

    def _clear(self) -> None:
        self._token = None
        self._expires_at = None
        if self.token_cache is not None:
            _token_file.drop(self.token_cache, self._cache_key())

    def _is_expiring(self) -> bool:
        """True if the token is within the margin of expiry.

        An unknown expiry (the API returned no expiry field) counts as *not*
        expiring — we let a 401 drive the refresh instead of reissuing blindly.
        """
        if self._expires_at is None:
            return False
        return time.time() >= self._expires_at - self.expiry_margin

    @staticmethod
    def _parse_expiry(data: dict[str, Any]) -> float | None:
        """Turn Kiwoom's expiry field into a unix timestamp.

        Kiwoom returns ``expires_dt`` as local-time ``yyyyMMddHHmmss``; some
        responses carry a plain ``expires_in`` in seconds instead. Anything
        unparseable yields None (expiry unknown).
        """
        expires_dt = data.get("expires_dt")
        if expires_dt:
            try:
                return datetime.strptime(str(expires_dt), "%Y%m%d%H%M%S").timestamp()
            except (ValueError, TypeError):
                pass

        expires_in = data.get("expires_in")
        if expires_in is not None:
            try:
                return time.time() + float(expires_in)
            except (ValueError, TypeError):
                pass

        return None


def _token_request_body(app_key: str, app_secret: str) -> dict[str, str]:
    return {
        "grant_type": "client_credentials",
        "appkey": app_key,
        "secretkey": app_secret,
    }


def _revoke_request_body(app_key: str, app_secret: str, token: str) -> dict[str, str]:
    return {"appkey": app_key, "secretkey": app_secret, "token": token}


_JSON_HEADERS = {"Content-Type": "application/json;charset=UTF-8"}


class KiwoomAuth(_TokenCache):
    """Handles OAuth2 token issuance, caching, expiry tracking and revocation.

    The issued token is cached together with its expiry. ``get_valid_token()``
    reissues automatically once the token is within ``expiry_margin`` seconds
    of expiring, so long-running processes don't die on an expired token.

    Args:
        app_key: API app key.
        app_secret: API app secret.
        base_url: API base URL.
        expiry_margin: Reissue this many seconds before actual expiry.
        timeout: HTTP timeout for the token endpoints (default 30s).
        token_cache: Optional path of a JSON file to keep the token in, so the
            next process with the same app key reuses it instead of asking
            Kiwoom for a new one. Written with mode 0600; holds the token but
            never the app key or secret. None (default) keeps it in memory only.
    """

    def __init__(
        self,
        app_key: str,
        app_secret: str,
        base_url: str,
        expiry_margin: float = _TokenCache.DEFAULT_EXPIRY_MARGIN,
        *,
        timeout: float | httpx.Timeout = 30.0,
        token_cache: str | os.PathLike[str] | None = None,
    ):
        super().__init__(expiry_margin, token_cache)
        self.app_key = app_key
        self.app_secret = app_secret
        self.base_url = base_url.rstrip("/")
        self._client = httpx.Client(base_url=self.base_url, timeout=timeout)
        self._lock = threading.Lock()

    def close(self) -> None:
        self._client.close()

    def __enter__(self) -> KiwoomAuth:
        return self

    def __exit__(self, *args: Any) -> None:
        self.close()

    def issue_token(self) -> dict[str, Any]:
        """접근토큰발급 (Access Token Issuance).

        POST /oauth2/token

        Returns:
            Dict with 'token' (access token string), 'token_type', and an
            expiry field ('expires_dt' or 'expires_in').

        Raises:
            KiwoomAuthError: If the request fails or carries no token.
        """
        try:
            resp = self._client.post(
                "/oauth2/token",
                json=_token_request_body(self.app_key, self.app_secret),
                headers=_JSON_HEADERS,
            )
            resp.raise_for_status()
            data = resp.json()
        except httpx.HTTPError as exc:
            raise _http_failure("토큰 발급 요청 실패", exc, self.base_url) from exc

        self._store(data)
        return data

    def revoke_token(self, token: str) -> dict[str, Any]:
        """접근토큰폐기 (Access Token Revocation).

        Args:
            token: The access token to revoke.

        Returns:
            API response dict.

        Raises:
            KiwoomAuthError: If the request fails.
        """
        try:
            resp = self._client.post(
                "/oauth2/revoke",
                json=_revoke_request_body(self.app_key, self.app_secret, token),
                headers=_JSON_HEADERS,
            )
            resp.raise_for_status()
            data = resp.json()
        except httpx.HTTPError as exc:
            raise _http_failure("토큰 폐기 요청 실패", exc, self.base_url) from exc

        self._forget(token)
        return data

    # --- TokenProvider protocol ---

    def get_valid_token(self) -> str:
        """Return a currently-valid token, issuing or reissuing as needed."""
        with self._lock:
            if self._token is not None and not self._is_expiring():
                return self._token
            if self._load_cached():
                assert self._token is not None
                return self._token
            self.issue_token()
            assert self._token is not None  # issue_token raises otherwise
            return self._token

    def refresh_token(self) -> str:
        """Force a new token even if the cached one still looks valid."""
        with self._lock:
            self._clear()
            self.issue_token()
            assert self._token is not None
            return self._token


class AsyncKiwoomAuth(_TokenCache):
    """Asyncio counterpart of :class:`KiwoomAuth`.

    Concurrent callers awaiting ``get_valid_token()`` share a single issuance:
    the first one through issues, the rest await it and reuse the result.

    Args:
        app_key: API app key.
        app_secret: API app secret.
        base_url: API base URL.
        expiry_margin: Reissue this many seconds before actual expiry.
        timeout: HTTP timeout for the token endpoints (default 30s).
        token_cache: Optional path of a JSON file to keep the token in, so the
            next process with the same app key reuses it instead of asking
            Kiwoom for a new one. Written with mode 0600; holds the token but
            never the app key or secret. None (default) keeps it in memory only.
    """

    def __init__(
        self,
        app_key: str,
        app_secret: str,
        base_url: str,
        expiry_margin: float = _TokenCache.DEFAULT_EXPIRY_MARGIN,
        *,
        timeout: float | httpx.Timeout = 30.0,
        token_cache: str | os.PathLike[str] | None = None,
    ):
        super().__init__(expiry_margin, token_cache)
        self.app_key = app_key
        self.app_secret = app_secret
        self.base_url = base_url.rstrip("/")
        self._client = httpx.AsyncClient(base_url=self.base_url, timeout=timeout)
        self._lock = asyncio.Lock()

    async def aclose(self) -> None:
        await self._client.aclose()

    async def __aenter__(self) -> AsyncKiwoomAuth:
        return self

    async def __aexit__(self, *args: Any) -> None:
        await self.aclose()

    async def issue_token(self) -> dict[str, Any]:
        """접근토큰발급 (Access Token Issuance).

        Raises:
            KiwoomAuthError: If the request fails or carries no token.
        """
        try:
            resp = await self._client.post(
                "/oauth2/token",
                json=_token_request_body(self.app_key, self.app_secret),
                headers=_JSON_HEADERS,
            )
            resp.raise_for_status()
            data = resp.json()
        except httpx.HTTPError as exc:
            raise _http_failure("토큰 발급 요청 실패", exc, self.base_url) from exc

        self._store(data)
        return data

    async def revoke_token(self, token: str) -> dict[str, Any]:
        """접근토큰폐기 (Access Token Revocation).

        Raises:
            KiwoomAuthError: If the request fails.
        """
        try:
            resp = await self._client.post(
                "/oauth2/revoke",
                json=_revoke_request_body(self.app_key, self.app_secret, token),
                headers=_JSON_HEADERS,
            )
            resp.raise_for_status()
            data = resp.json()
        except httpx.HTTPError as exc:
            raise _http_failure("토큰 폐기 요청 실패", exc, self.base_url) from exc

        self._forget(token)
        return data

    # --- AsyncTokenProvider protocol ---

    async def get_valid_token(self) -> str:
        """Return a currently-valid token, issuing or reissuing as needed."""
        async with self._lock:
            if self._token is not None and not self._is_expiring():
                return self._token
            if self._load_cached():
                assert self._token is not None
                return self._token
            await self.issue_token()
            assert self._token is not None
            return self._token

    async def refresh_token(self) -> str:
        """Force a new token even if the cached one still looks valid."""
        async with self._lock:
            self._clear()
            await self.issue_token()
            assert self._token is not None
            return self._token
