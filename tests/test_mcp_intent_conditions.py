"""condition_search_run: pick a condition by name or number, run it, normalise rows."""

from __future__ import annotations

import contextlib
import json

import pytest
import websockets

from kiwoom_client import spec
from kiwoom_client.mcp.condition_search_session import ConditionSearchSession
from kiwoom_client.mcp.intents.conditions import ROW_FIELDS, parse_condition_list, pick_condition
from kiwoom_client.mcp.server import build_server
from kiwoom_client.websocket import KiwoomWebSocket

from .intent_support import call

CONDITIONS = [["0", "급등주 조건"], ["1", "거래량 급증"], ["2", "급등 눌림목"]]


def _hit(code, name, price):
    return {"9001": f"A{code}", "302": name, "10": price, "11": "+500", "12": "+1.20",
            "13": "000123456", "16": "+69000", "17": "+71000", "18": "-68500"}  # fmt: skip


class FakeConditionServer:
    """CNSRLST answers CONDITIONS; CNSRREQ seq 1 answers two pages."""

    def __init__(self) -> None:
        self.received: list[dict] = []
        self._server = None

    async def __aenter__(self):
        self._server = await websockets.serve(self._handler, "127.0.0.1", 0)
        return self

    async def __aexit__(self, *args):
        self._server.close()
        await self._server.wait_closed()

    @property
    def url(self) -> str:
        host, port = self._server.sockets[0].getsockname()[:2]
        return f"ws://{host}:{port}"

    async def _handler(self, conn) -> None:
        with contextlib.suppress(websockets.ConnectionClosed):
            async for raw in conn:
                msg = json.loads(raw)
                self.received.append(msg)
                trnm = msg.get("trnm")
                if trnm == "LOGIN":
                    reply = {"trnm": "LOGIN", "return_code": 0}
                elif trnm == "CNSRLST":
                    reply = {"trnm": "CNSRLST", "return_code": 0, "data": CONDITIONS}
                elif trnm == "CNSRREQ" and msg["cont_yn"] == "N":
                    reply = {"trnm": "CNSRREQ", "seq": msg["seq"], "return_code": 0,
                             "cont_yn": "Y", "next_key": "k2",
                             "data": [_hit("005930", "삼성전자", "-070000")]}  # fmt: skip
                else:
                    reply = {"trnm": "CNSRREQ", "seq": msg["seq"], "return_code": 0,
                             "cont_yn": "N", "next_key": "",
                             "data": [_hit("000660", "SK하이닉스", "+180000")]}  # fmt: skip
                await conn.send(json.dumps(reply))

    def sent(self, trnm):
        return [m for m in self.received if m.get("trnm") == trnm]


@contextlib.asynccontextmanager
async def _app(server):
    async def connect():
        ws = KiwoomWebSocket("tok", ws_url=server.url)
        await ws.connect()
        return ws

    session = ConditionSearchSession(connect=connect)
    app, _specs = build_server(api=None, allow_live_orders=False, session=session)
    try:
        yield app
    finally:
        await session.close()


def test_row_fields_come_from_the_ka10172_spec():
    ids = {f.id for f in spec.get("ka10172").response}
    assert {source for source, _ in ROW_FIELDS.values()} <= ids


def test_parse_both_list_shapes():
    reply = {"data": [["0", "a"], {"seq": "1", "name": "b"}, ["bad"]]}
    assert parse_condition_list(reply) == [{"seq": "0", "name": "a"}, {"seq": "1", "name": "b"}]


def test_pick_condition():
    conditions = parse_condition_list({"data": CONDITIONS})
    assert pick_condition(conditions, "1")["name"] == "거래량 급증"
    assert pick_condition(conditions, "거래량급증")["seq"] == "1"  # 공백 무시
    assert pick_condition(conditions, "눌림")["seq"] == "2"
    with pytest.raises(ValueError, match="여러 개"):
        pick_condition(conditions, "급등")
    with pytest.raises(ValueError, match="저장된 조건식"):
        pick_condition(conditions, "없는조건")
    with pytest.raises(ValueError, match="없습니다"):
        pick_condition([], "x")


async def test_runs_by_name_and_follows_pages():
    async with FakeConditionServer() as server, _app(server) as app:
        is_error, out = await call(app, "condition_search_run", {"name_or_seq": "거래량"})
    assert is_error is False, out
    assert out["condition"] == {"seq": "1", "name": "거래량 급증"}
    assert [r["code"] for r in out["rows"]] == ["005930", "000660"]
    first = out["rows"][0]
    assert (first["price"], first["change"], first["change_pct"], first["volume"]) == (
        70000, 500, 1.2, 123456,
    )  # fmt: skip
    assert out["more_available"] is False
    first_req, second_req = server.sent("CNSRREQ")
    assert first_req["search_type"] == "0" and first_req["seq"] == "1"
    assert (second_req["cont_yn"], second_req["next_key"]) == ("Y", "k2")


async def test_count_stops_paging():
    async with FakeConditionServer() as server, _app(server) as app:
        args = {"name_or_seq": "1", "count": 1}
        is_error, out = await call(app, "condition_search_run", args)
    assert is_error is False, out
    assert out["count"] == 1 and out["more_available"] is True
    assert len(server.sent("CNSRREQ")) == 1


async def test_ambiguous_name_is_an_error():
    async with FakeConditionServer() as server, _app(server) as app:
        is_error, text = await call(app, "condition_search_run", {"name_or_seq": "급등"})
    assert is_error is True and "0:급등주 조건" in text
    assert not server.sent("CNSRREQ")


async def test_without_a_session_it_refuses():
    app, _specs = build_server(api=None, allow_live_orders=False)
    is_error, text = await call(app, "condition_search_run", {"name_or_seq": "1"})
    assert is_error is True and "WebSocket" in text
