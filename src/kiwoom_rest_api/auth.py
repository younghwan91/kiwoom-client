"""OAuth2 authentication for Kiwoom REST API."""

from __future__ import annotations

import asyncio
import threading
import time
from datetime import datetime
from typing import Any, Protocol, runtime_checkable

import httpx


class KiwoomAuthError(Exception):
    """Token issuance or revocation failed."""


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

    def __init__(self, expiry_margin: float = DEFAULT_EXPIRY_MARGIN) -> None:
        self.expiry_margin = expiry_margin
        self._token: str | None = None
        self._expires_at: float | None = None

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
            raise KiwoomAuthError(f"토큰 발급 실패: {msg}")
        self._token = token
        self._expires_at = self._parse_expiry(data)
        return token

    def _clear(self) -> None:
        self._token = None
        self._expires_at = None

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
    """

    def __init__(
        self,
        app_key: str,
        app_secret: str,
        base_url: str,
        expiry_margin: float = _TokenCache.DEFAULT_EXPIRY_MARGIN,
    ):
        super().__init__(expiry_margin)
        self.app_key = app_key
        self.app_secret = app_secret
        self.base_url = base_url.rstrip("/")
        self._client = httpx.Client(base_url=self.base_url, timeout=30.0)
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
            raise KiwoomAuthError(f"토큰 발급 요청 실패: {exc}") from exc

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
            raise KiwoomAuthError(f"토큰 폐기 요청 실패: {exc}") from exc

        if token == self._token:
            self._clear()
        return data

    # --- TokenProvider protocol ---

    def get_valid_token(self) -> str:
        """Return a currently-valid token, issuing or reissuing as needed."""
        with self._lock:
            if self._token is not None and not self._is_expiring():
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
    """

    def __init__(
        self,
        app_key: str,
        app_secret: str,
        base_url: str,
        expiry_margin: float = _TokenCache.DEFAULT_EXPIRY_MARGIN,
    ):
        super().__init__(expiry_margin)
        self.app_key = app_key
        self.app_secret = app_secret
        self.base_url = base_url.rstrip("/")
        self._client = httpx.AsyncClient(base_url=self.base_url, timeout=30.0)
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
            raise KiwoomAuthError(f"토큰 발급 요청 실패: {exc}") from exc

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
            raise KiwoomAuthError(f"토큰 폐기 요청 실패: {exc}") from exc

        if token == self._token:
            self._clear()
        return data

    # --- AsyncTokenProvider protocol ---

    async def get_valid_token(self) -> str:
        """Return a currently-valid token, issuing or reissuing as needed."""
        async with self._lock:
            if self._token is not None and not self._is_expiring():
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
