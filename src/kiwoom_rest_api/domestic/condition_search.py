"""Condition Search (조건검색) WebSocket endpoints for the Kiwoom REST API."""

from __future__ import annotations

from typing import Any


class ConditionSearch:
    """Wraps all Condition Search (조건검색) WebSocket endpoints.

    These methods return a dict with api_id and body for use with the
    WebSocket client rather than making direct REST calls.

    Args:
        client: Authenticated BaseClient instance (reserved for future use).
    """

    RESOURCE_URL = "/api/dostk/websocket"

    def __init__(self, client: Any) -> None:
        self._client = client

    def condition_list(self, **kwargs: Any) -> dict[str, Any]:
        """조건검색목록조회 (Condition List)"""
        return {"api_id": "ka10171", "body": kwargs}

    def condition_search(self, **kwargs: Any) -> dict[str, Any]:
        """조건검색요청일반 (Condition Search General)"""
        return {"api_id": "ka10172", "body": kwargs}

    def condition_search_realtime(self, **kwargs: Any) -> dict[str, Any]:
        """조건검색요청실시간 (Condition Search Realtime)"""
        return {"api_id": "ka10173", "body": kwargs}

    def condition_search_cancel(self, **kwargs: Any) -> dict[str, Any]:
        """조건검색실시간해제 (Condition Search Realtime Cancel)"""
        return {"api_id": "ka10174", "body": kwargs}
