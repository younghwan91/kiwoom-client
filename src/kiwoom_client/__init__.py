"""Kiwoom REST API Python Wrapper (키움 REST API).

A comprehensive Python client for Kiwoom Securities REST API,
covering all domestic stock (국내주식) endpoints.

Usage:
    from kiwoom_client import KiwoomAPI

    api = KiwoomAPI(app_key="YOUR_KEY", app_secret="YOUR_SECRET")

    # Get stock info — the token is issued and refreshed for you
    info = api.stock_info.basic_stock_info(stk_cd="005930")

    # Place order
    result = api.order.buy_order(stk_cd="005930", ord_qty=10, ord_uv=70000, ...)

Asyncio:
    from kiwoom_client import AsyncKiwoomAPI

    async with AsyncKiwoomAPI(app_key="...", app_secret="...") as api:
        info = await api.stock_info.basic_stock_info(stk_cd="005930")
"""

from __future__ import annotations

from collections.abc import Awaitable
from importlib.metadata import PackageNotFoundError
from importlib.metadata import version as _package_version
from typing import Any

from kiwoom_client._registry import ModuleRegistry
from kiwoom_client.auth import AsyncKiwoomAuth, KiwoomAuth, KiwoomAuthError
from kiwoom_client.base import AsyncBaseClient, BaseClient, KiwoomAPIError
from kiwoom_client.parsing import extract_records, normalize, to_dataframe, to_number
from kiwoom_client.websocket import KiwoomWebSocket

try:
    # Single source of truth is pyproject.toml — never hardcode it here.
    __version__ = _package_version("kiwoom-client")
except PackageNotFoundError:  # pragma: no cover - source tree without install
    __version__ = "0.0.0"

__all__ = [
    "AsyncKiwoomAPI",
    "KiwoomAPI",
    "KiwoomAPIError",
    "KiwoomAuthError",
    "KiwoomWebSocket",
    "__version__",
    "extract_records",
    "normalize",
    "to_dataframe",
    "to_number",
]


class KiwoomAPI(ModuleRegistry[dict[str, Any]]):
    """Unified facade for all Kiwoom REST API endpoints.

    Rate limiting (per-TR token bucket, ~1 req/s + burst 2) and automatic 429
    retry are enabled by default; pass ``rate_limit=None`` to disable.

    The access token is managed for you: it is issued on first use, reissued
    before it expires, and reissued again if the API answers 401. Calling
    ``login()`` explicitly is optional and simply issues the first token.

    Args:
        app_key: API app key from Kiwoom developer portal.
        app_secret: API app secret from Kiwoom developer portal.
        base_url: Override API base URL.
        is_mock: Use mock trading server if True.
        rate_limit: Per-TR sustained request rate (req/s). None disables.
        rate_burst: Per-TR burst capacity (max instantaneous requests).
        max_retries: Automatic retries on HTTP 429 / return_code 5.
        retry_backoff: Base seconds to wait before a retry (grows per attempt).
        expiry_margin: Reissue the token this many seconds before it expires.
    """

    def __init__(
        self,
        app_key: str,
        app_secret: str,
        base_url: str | None = None,
        is_mock: bool = False,
        rate_limit: float | None = BaseClient.DEFAULT_RATE_LIMIT,
        rate_burst: int = BaseClient.DEFAULT_RATE_BURST,
        max_retries: int = 3,
        retry_backoff: float = 1.1,
        expiry_margin: float = KiwoomAuth.DEFAULT_EXPIRY_MARGIN,
    ):
        self._base_client = BaseClient(
            app_key, app_secret, base_url, is_mock,
            rate_limit=rate_limit, rate_burst=rate_burst, max_retries=max_retries,
            retry_backoff=retry_backoff,
        )
        self._client = self._base_client
        self._auth = KiwoomAuth(
            app_key, app_secret, self._base_client.base_url, expiry_margin=expiry_margin
        )
        # Token lifecycle is delegated to the auth object from the start.
        self._base_client.token_provider = self._auth
        self._is_mock = is_mock
        self._init_modules()

    def login(self) -> dict[str, Any]:
        """Authenticate and obtain an access token.

        Optional — the first API call issues a token on its own. Call this
        when you want to fail fast on bad credentials.

        Returns:
            Token response dict from the API.
        """
        result = self._auth.issue_token()
        self._base_client.access_token = self._auth.token
        return result

    def logout(self) -> dict[str, Any]:
        """Revoke the current access token."""
        token = self._auth.token
        if not token:
            raise RuntimeError("Not logged in")
        result = self._auth.revoke_token(token)
        self._base_client.access_token = None
        return result

    def close(self) -> None:
        """Close all connections."""
        self._base_client.close()
        self._auth.close()

    def __enter__(self) -> KiwoomAPI:
        return self

    def __exit__(self, *args: Any) -> None:
        self.close()

    def create_websocket(self) -> KiwoomWebSocket:
        """Create a WebSocket client for real-time data.

        Returns:
            KiwoomWebSocket instance configured with current auth.
        """
        return KiwoomWebSocket(self._auth.get_valid_token(), self._is_mock)


class AsyncKiwoomAPI(ModuleRegistry[Awaitable[dict[str, Any]]]):
    """Asyncio facade for all Kiwoom REST API endpoints.

    Identical surface to :class:`KiwoomAPI`, except every endpoint call is
    awaited. Calls to *different* TRs run concurrently; the per-TR limiter
    still serializes calls to the same TR, matching Kiwoom's own limit.

    Args:
        app_key: API app key from Kiwoom developer portal.
        app_secret: API app secret from Kiwoom developer portal.
        base_url: Override API base URL.
        is_mock: Use mock trading server if True.
        rate_limit: Per-TR sustained request rate (req/s). None disables.
        rate_burst: Per-TR burst capacity (max instantaneous requests).
        max_retries: Automatic retries on HTTP 429 / return_code 5.
        retry_backoff: Base seconds to wait before a retry (grows per attempt).
        expiry_margin: Reissue the token this many seconds before it expires.
    """

    def __init__(
        self,
        app_key: str,
        app_secret: str,
        base_url: str | None = None,
        is_mock: bool = False,
        rate_limit: float | None = AsyncBaseClient.DEFAULT_RATE_LIMIT,
        rate_burst: int = AsyncBaseClient.DEFAULT_RATE_BURST,
        max_retries: int = 3,
        retry_backoff: float = 1.1,
        expiry_margin: float = AsyncKiwoomAuth.DEFAULT_EXPIRY_MARGIN,
    ):
        self._base_client = AsyncBaseClient(
            app_key, app_secret, base_url, is_mock,
            rate_limit=rate_limit, rate_burst=rate_burst, max_retries=max_retries,
            retry_backoff=retry_backoff,
        )
        self._client = self._base_client
        self._auth = AsyncKiwoomAuth(
            app_key, app_secret, self._base_client.base_url, expiry_margin=expiry_margin
        )
        self._base_client.token_provider = self._auth
        self._is_mock = is_mock
        self._init_modules()

    async def login(self) -> dict[str, Any]:
        """Authenticate and obtain an access token (optional — see KiwoomAPI)."""
        result = await self._auth.issue_token()
        self._base_client.access_token = self._auth.token
        return result

    async def logout(self) -> dict[str, Any]:
        """Revoke the current access token."""
        token = self._auth.token
        if not token:
            raise RuntimeError("Not logged in")
        result = await self._auth.revoke_token(token)
        self._base_client.access_token = None
        return result

    async def close(self) -> None:
        """Close all connections."""
        await self._base_client.aclose()
        await self._auth.aclose()

    async def __aenter__(self) -> AsyncKiwoomAPI:
        return self

    async def __aexit__(self, *args: Any) -> None:
        await self.close()

    async def create_websocket(self) -> KiwoomWebSocket:
        """Create a WebSocket client for real-time data.

        Returns:
            KiwoomWebSocket instance configured with current auth.
        """
        return KiwoomWebSocket(await self._auth.get_valid_token(), self._is_mock)
