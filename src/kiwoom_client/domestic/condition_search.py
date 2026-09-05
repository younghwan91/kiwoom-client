"""Condition Search (조건검색) WebSocket payloads for the Kiwoom REST API.

Condition search does not travel over REST — it rides the same WebSocket as
real-time data, keyed by ``trnm`` rather than ``api_id``. These methods build
the request payloads; hand them to ``KiwoomWebSocket.send()``.
"""

from __future__ import annotations

from typing import Any


class ConditionSearch:
    """Builds all Condition Search (조건검색) WebSocket request payloads.

    Usage:
        ws = api.create_websocket()
        await ws.connect()
        ws.on_trnm("CNSRLST", print)
        await ws.send(api.condition_search.condition_list())

    Args:
        client: Unused — kept so the module lines up with the REST modules.
    """

    def __init__(self, client: Any = None) -> None:
        self._client = client

    def condition_list(self) -> dict[str, Any]:
        """조건검색 목록조회 (Condition List).

        Must be called before any search: the ``seq`` values it returns are
        what the other calls take.
        """
        return {"trnm": "CNSRLST"}

    def condition_search(
        self,
        seq: str,
        search_type: str = "0",
        stex_tp: str = "K",
        cont_yn: str = "N",
        next_key: str = "",
    ) -> dict[str, Any]:
        """조건검색 요청 일반 (Condition Search).

        Args:
            seq: 조건검색식 일련번호, from ``condition_list()``.
            search_type: "0" 조건검색, "1" 조건검색 + 실시간.
            stex_tp: 거래소 구분 (K: KRX).
            cont_yn: 연속조회 여부.
            next_key: 연속조회 키.
        """
        return {
            "trnm": "CNSRREQ",
            "seq": seq,
            "search_type": search_type,
            "stex_tp": stex_tp,
            "cont_yn": cont_yn,
            "next_key": next_key,
        }

    def condition_search_realtime(
        self,
        seq: str,
        stex_tp: str = "K",
        cont_yn: str = "N",
        next_key: str = "",
    ) -> dict[str, Any]:
        """조건검색 요청 실시간 (Condition Search + Realtime).

        Same as :meth:`condition_search` with ``search_type="1"``: results
        keep arriving as stocks enter or leave the condition.
        """
        return self.condition_search(
            seq, search_type="1", stex_tp=stex_tp, cont_yn=cont_yn, next_key=next_key
        )

    def condition_search_cancel(self, seq: str) -> dict[str, Any]:
        """조건검색 실시간 해제 (Cancel Realtime Condition Search).

        Args:
            seq: 조건검색식 일련번호.
        """
        return {"trnm": "CNSRCLR", "seq": seq}
