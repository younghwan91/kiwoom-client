"""Theme (테마) endpoints for the Kiwoom REST API."""

from __future__ import annotations

from typing import Any

from kiwoom_rest_api.base import BaseClient


class Theme:
    """Wraps all Theme (테마) endpoints under /api/dostk/thme.

    Args:
        client: Authenticated BaseClient instance.
    """

    RESOURCE_URL = "/api/dostk/thme"

    def __init__(self, client: BaseClient) -> None:
        self._client = client

    def theme_group_list(
        self, cont_yn: str = "N", next_key: str = "", **kwargs: Any
    ) -> dict[str, Any]:
        """테마그룹별요청 (Theme Group List)"""
        return self._client.request(self.RESOURCE_URL, "ka90001", kwargs, cont_yn, next_key)

    def theme_component_stocks(
        self, cont_yn: str = "N", next_key: str = "", **kwargs: Any
    ) -> dict[str, Any]:
        """테마구성종목요청 (Theme Component Stocks)"""
        return self._client.request(self.RESOURCE_URL, "ka90002", kwargs, cont_yn, next_key)
