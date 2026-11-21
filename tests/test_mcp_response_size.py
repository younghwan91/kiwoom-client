"""Tests for opt-in max_rows truncation of list responses."""

from __future__ import annotations

import json

import pytest
from mcp import types

from kiwoom_client import AsyncKiwoomAPI
from kiwoom_client.mcp import cli
from kiwoom_client.mcp.response_size import (
    ENV_VAR,
    MARKER,
    limit_rows,
    max_rows_from_env,
    parse_max_rows,
    with_max_rows_argument,
)
from kiwoom_client.mcp.server import build_server

CHART_URL = "https://mockapi.kiwoom.com/api/dostk/chart"
ROWS = [{"dt": f"2026{i:04d}", "cur_prc": str(1000 + i)} for i in range(30)]


@pytest.fixture
async def api(httpx_mock):
    httpx_mock.add_response(
        url="https://mockapi.kiwoom.com/oauth2/token",
        json={"token": "test_token", "token_type": "Bearer", "expires_in": 86400},
    )
    api = AsyncKiwoomAPI("key", "secret", is_mock=True)
    await api.login()
    yield api
    await api.close()


async def _call(app, name, arguments):
    result = await app.get_request_handler("tools/call").handler(
        None, types.CallToolRequestParams(name=name, arguments=arguments)
    )
    assert result.is_error is False, result.content[0].text
    return json.loads(result.content[0].text)


class TestLimitRows:
    def test_none_passes_through_untouched(self):
        data = {"rows": list(range(10))}
        assert limit_rows(data, None) is data

    def test_cuts_every_long_top_level_list_and_marks_it(self):
        data = {"a": list(range(10)), "b": list(range(3)), "return_code": 0}
        out = limit_rows(data, 5)
        assert out["a"] == [0, 1, 2, 3, 4]
        assert out["b"] == [0, 1, 2]
        assert out[MARKER] == {"a": {"total": 10, "returned": 5}}
        assert data["a"] == list(range(10))  # input not modified

    def test_nothing_to_cut_means_no_marker(self):
        data = {"a": [1, 2]}
        assert limit_rows(data, 5) is data

    def test_non_dict_results_pass_through(self):
        assert limit_rows(None, 1) is None

    @pytest.mark.parametrize("value", [0, -3, "x", "1.5", True])
    def test_parse_rejects_non_positive_integers(self, value):
        with pytest.raises(ValueError):
            parse_max_rows(value)

    def test_parse_and_env(self):
        assert parse_max_rows("20") == 20
        assert parse_max_rows(None) is None
        assert max_rows_from_env({ENV_VAR: "50"}) == 50
        assert max_rows_from_env({}) is None

    def test_schema_helper_adds_property_without_mutating(self):
        schema = {"type": "object", "properties": {"params": {"type": "object"}}}
        out = with_max_rows_argument(schema)
        assert "max_rows" in out["properties"]
        assert "max_rows" not in schema["properties"]


class TestServerTruncation:
    async def test_default_returns_everything(self, httpx_mock, api):
        httpx_mock.add_response(url=CHART_URL, json={"return_code": 0, "rows": ROWS})
        app, _specs = build_server(api, allow_live_orders=False)
        out = await _call(app, "chart_stock_daily_chart", {"params": {"stk_cd": "005930"}})
        assert len(out["rows"]) == 30
        assert MARKER not in out

    async def test_per_call_max_rows_is_not_sent_to_kiwoom(self, httpx_mock, api):
        httpx_mock.add_response(url=CHART_URL, json={"return_code": 0, "rows": ROWS})
        app, _specs = build_server(api, allow_live_orders=False)
        out = await _call(
            app, "chart_stock_daily_chart", {"params": {"stk_cd": "005930"}, "max_rows": 5}
        )
        assert len(out["rows"]) == 5
        assert out[MARKER] == {"rows": {"total": 30, "returned": 5}}
        sent = json.loads(httpx_mock.get_requests(url=CHART_URL)[0].content)
        assert sent == {"stk_cd": "005930"}

    async def test_server_default_and_per_call_override(self, httpx_mock, api):
        httpx_mock.add_response(url=CHART_URL, json={"return_code": 0, "rows": ROWS})
        httpx_mock.add_response(url=CHART_URL, json={"return_code": 0, "rows": ROWS})
        app, _specs = build_server(api, allow_live_orders=False, max_rows=10)
        default = await _call(app, "chart_stock_daily_chart", {"params": {}})
        assert len(default["rows"]) == 10
        override = await _call(app, "chart_stock_daily_chart", {"params": {}, "max_rows": 25})
        assert len(override["rows"]) == 25

    async def test_bad_max_rows_is_a_tool_error(self, api):
        app, _specs = build_server(api, allow_live_orders=False)
        result = await app.get_request_handler("tools/call").handler(
            None,
            types.CallToolRequestParams(
                name="chart_stock_daily_chart", arguments={"params": {}, "max_rows": 0}
            ),
        )
        assert result.is_error is True

    async def test_lookup_schemas_advertise_max_rows_but_order_schemas_do_not(self):
        app, _specs = build_server(api=None, allow_live_orders=True)
        listed = await app.get_request_handler("tools/list").handler(
            None, types.PaginatedRequestParams()
        )
        tools = {t.name: t for t in listed.tools}
        assert "max_rows" in tools["chart_stock_daily_chart"].input_schema["properties"]
        assert "max_rows" not in tools["order_buy_order"].input_schema["properties"]

    async def test_works_through_discovery_call_tool(self, httpx_mock, api):
        httpx_mock.add_response(url=CHART_URL, json={"return_code": 0, "rows": ROWS})
        app, _specs = build_server(api, allow_live_orders=False, discovery=True)
        out = await _call(
            app,
            "call_tool",
            {"name": "chart_stock_daily_chart", "arguments": {"params": {}, "max_rows": 2}},
        )
        assert len(out["rows"]) == 2


class TestCli:
    def _run(self, monkeypatch, argv, env=None):
        calls = []
        import kiwoom_client.mcp.server as server

        monkeypatch.setattr(server, "run_server", lambda **kw: calls.append(kw))
        monkeypatch.setenv("KIWOOM_APP_KEY", "k")
        monkeypatch.setenv("KIWOOM_APP_SECRET", "s")
        monkeypatch.delenv(ENV_VAR, raising=False)
        for key, value in (env or {}).items():
            monkeypatch.setenv(key, value)
        cli.main(argv)
        return calls[0]["max_rows"]

    def test_flag_env_and_default(self, monkeypatch):
        assert self._run(monkeypatch, []) is None
        assert self._run(monkeypatch, [], {ENV_VAR: "40"}) == 40
        assert self._run(monkeypatch, ["--max-rows", "7"], {ENV_VAR: "40"}) == 7

    def test_bad_flag_is_usage_error(self, monkeypatch):
        with pytest.raises(SystemExit) as exc:
            self._run(monkeypatch, ["--max-rows", "0"])
        assert exc.value.code == 2
