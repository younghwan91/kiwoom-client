"""Base HTTP client for Kiwoom REST API with auth, pagination, and error handling."""

from __future__ import annotations

from typing import Any

import httpx

from kiwoom_rest_api.rate_limiter import RateLimiter


class KiwoomAPIError(Exception):
    """Kiwoom API error with return_code and return_msg."""

    def __init__(self, code: int, message: str, response: dict[str, Any] | None = None):
        self.code = code
        self.message = message
        self.response = response
        super().__init__(f"[{code}] {message}")


class BaseClient:
    """Base client handling authentication, requests, and pagination.

    Args:
        app_key: API app key from Kiwoom developer portal.
        app_secret: API app secret from Kiwoom developer portal.
        base_url: API base URL. Defaults to production.
        is_mock: Use mock trading server if True.
    """

    PROD_URL = "https://api.kiwoom.com"
    MOCK_URL = "https://mockapi.kiwoom.com"

    def __init__(
        self,
        app_key: str,
        app_secret: str,
        base_url: str | None = None,
        is_mock: bool = False,
        rate_limit: float | None = None,
    ):
        self.app_key = app_key
        self.app_secret = app_secret
        if base_url:
            self.base_url = base_url.rstrip("/")
        else:
            self.base_url = self.MOCK_URL if is_mock else self.PROD_URL
        self._access_token: str | None = None
        self._client = httpx.Client(base_url=self.base_url, timeout=30.0)
        self._rate_limiter: RateLimiter | None = RateLimiter(rate_limit) if rate_limit is not None else None

    def close(self) -> None:
        self._client.close()

    def __enter__(self) -> BaseClient:
        return self

    def __exit__(self, *args: Any) -> None:
        self.close()

    @property
    def access_token(self) -> str | None:
        return self._access_token

    @access_token.setter
    def access_token(self, token: str | None) -> None:
        self._access_token = token

    def _build_headers(
        self,
        api_id: str,
        cont_yn: str = "N",
        next_key: str = "",
        extra_headers: dict[str, str] | None = None,
    ) -> dict[str, str]:
        headers = {
            "Content-Type": "application/json;charset=UTF-8",
            "api-id": api_id,
            "cont-yn": cont_yn,
            "next-key": next_key,
        }
        if self._access_token:
            headers["authorization"] = f"Bearer {self._access_token}"
        if extra_headers:
            headers.update(extra_headers)
        return headers

    def request(
        self,
        resource_url: str,
        api_id: str,
        body: dict[str, Any] | None = None,
        cont_yn: str = "N",
        next_key: str = "",
        extra_headers: dict[str, str] | None = None,
    ) -> dict[str, Any]:
        """Send a POST request to a Kiwoom REST API endpoint.

        Args:
            resource_url: API resource path (e.g., /api/dostk/acnt).
            api_id: API endpoint identifier (e.g., ka10001).
            body: Request body parameters.
            cont_yn: Continuation flag ("N" or "Y").
            next_key: Pagination key for continuation queries.
            extra_headers: Additional headers to include.

        Returns:
            Parsed JSON response as a dictionary.

        Raises:
            KiwoomAPIError: If the API returns a non-zero return_code.
        """
        if self._rate_limiter is not None:
            self._rate_limiter.acquire()
        headers = self._build_headers(api_id, cont_yn, next_key, extra_headers)
        resp = self._client.post(resource_url, headers=headers, json=body or {})
        resp.raise_for_status()
        data = resp.json()

        return_code = data.get("return_code", 0)
        if return_code != 0:
            raise KiwoomAPIError(
                code=return_code,
                message=data.get("return_msg", "Unknown error"),
                response=data,
            )
        return data

    def request_all(
        self,
        resource_url: str,
        api_id: str,
        body: dict[str, Any] | None = None,
        data_key: str | None = None,
        max_pages: int = 100,
    ) -> list[dict[str, Any]]:
        """Auto-paginate through all pages of a Kiwoom API endpoint.

        Args:
            resource_url: API resource path.
            api_id: API endpoint identifier.
            body: Request body parameters.
            data_key: Key in response containing the list data to accumulate.
            max_pages: Safety limit on number of pages to fetch.

        Returns:
            Accumulated list of all data items across pages.
        """
        all_items: list[dict[str, Any]] = []
        cont_yn = "N"
        next_key = ""

        for _ in range(max_pages):
            resp = self.request(resource_url, api_id, body, cont_yn, next_key)

            if data_key and data_key in resp:
                items = resp[data_key]
                if isinstance(items, list):
                    all_items.extend(items)
            else:
                all_items.append(resp)

            resp_cont = resp.get("cont_yn") or resp.get("cont-yn", "N")
            resp_next = resp.get("next_key") or resp.get("next-key", "")

            if resp_cont != "Y" or not resp_next:
                break
            cont_yn = "Y"
            next_key = resp_next

        return all_items
