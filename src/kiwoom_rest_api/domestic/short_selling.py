"""Short Selling (공매도) endpoints for the Kiwoom REST API."""

from __future__ import annotations

from typing import Any

from kiwoom_rest_api.base import BaseClient


class ShortSelling:
    """Wraps all Short Selling (공매도) endpoints under /api/dostk/shsa.

    Args:
        client: Authenticated BaseClient instance.
    """

    RESOURCE_URL = "/api/dostk/shsa"

    def __init__(self, client: BaseClient) -> None:
        self._client = client

    def short_selling_trend(
        self, cont_yn: str = "N", next_key: str = "", **kwargs: Any
    ) -> dict[str, Any]:
        """공매도추이요청 (Short Selling Trend)"""
        return self._client.request(self.RESOURCE_URL, "ka10014", kwargs, cont_yn, next_key)
