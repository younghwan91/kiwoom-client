"""OAuth2 authentication for Kiwoom REST API."""

from __future__ import annotations

from typing import Any

import httpx


class KiwoomAuth:
    """Handles OAuth2 token issuance and revocation.

    Args:
        app_key: API app key.
        app_secret: API app secret.
        base_url: API base URL.
    """

    def __init__(self, app_key: str, app_secret: str, base_url: str):
        self.app_key = app_key
        self.app_secret = app_secret
        self.base_url = base_url.rstrip("/")
        self._client = httpx.Client(base_url=self.base_url, timeout=30.0)

    def close(self) -> None:
        self._client.close()

    def issue_token(self) -> dict[str, Any]:
        """접근토큰발급 (Access Token Issuance).

        POST /oauth2/token

        Returns:
            Dict with 'token' (access token string), 'token_type', 'expires_in'.
        """
        resp = self._client.post(
            "/oauth2/token",
            json={
                "grant_type": "client_credentials",
                "appkey": self.app_key,
                "appsecretkey": self.app_secret,
            },
            headers={"Content-Type": "application/json;charset=UTF-8"},
        )
        resp.raise_for_status()
        return resp.json()

    def revoke_token(self, token: str) -> dict[str, Any]:
        """접근토큰폐기 (Access Token Revocation).

        POST /oauth2/revoke

        Args:
            token: The access token to revoke.

        Returns:
            API response dict.
        """
        resp = self._client.post(
            "/oauth2/revoke",
            json={
                "appkey": self.app_key,
                "appsecretkey": self.app_secret,
                "token": token,
            },
            headers={"Content-Type": "application/json;charset=UTF-8"},
        )
        resp.raise_for_status()
        return resp.json()
