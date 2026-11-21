"""MCP REST 도구 입력 스키마가 TR 카탈로그에서 나오고, 예전 호출 형태도 계속 받는지."""

from __future__ import annotations

import json

import pytest
from mcp import types

from kiwoom_client import AsyncKiwoomAPI, spec
from kiwoom_client.mcp.schema import (
    generic_rest_input_schema,
    rest_input_schema,
    split_arguments,
)
from kiwoom_client.mcp.server import build_server, dispatch_tool
from kiwoom_client.mcp.tools import discover_rest_tools


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


def test_params_schema_lists_catalog_fields_and_required():
    schema = rest_input_schema("ranking", "top_volume_today")
    params = schema["properties"]["params"]
    tr = spec.get("ka10030")
    assert list(params["properties"]) == [f.id for f in tr.request_fields]
    assert params["required"] == list(tr.required_fields)
    assert params["additionalProperties"] is True
    assert schema["required"] == ["params"]
    sort_tp = params["properties"]["sort_tp"]
    assert sort_tp["type"] == "string"
    assert sort_tp["description"].startswith("정렬구분 (필수).")
    assert "1:거래량" in sort_tp["description"]
    assert "enum" not in sort_tp  # 휴리스틱 코드값이라 강제하지 않는다


def test_paging_arguments_stay_at_top_level():
    props = rest_input_schema("stock_info", "basic_stock_info")["properties"]
    assert props["cont_yn"]["default"] == "N"
    assert props["next_key"]["default"] == ""


def test_every_rest_tool_gets_a_catalog_schema():
    generic = generic_rest_input_schema()
    for tool in discover_rest_tools():
        schema = rest_input_schema(tool.module_name, tool.method_name)
        assert schema != generic, tool.tool_name
        json.dumps(schema)  # JSON 으로 직렬화된다


def test_unknown_method_falls_back_to_generic_schema():
    assert rest_input_schema("stock_info", "nope") == generic_rest_input_schema()


@pytest.mark.parametrize(
    ("arguments", "expected"),
    [
        ({"params": {"stk_cd": "005930"}}, ({"stk_cd": "005930"}, "N", "")),
        ({"stk_cd": "005930", "cont_yn": "Y", "next_key": "k"}, ({"stk_cd": "005930"}, "Y", "k")),
        ({"stk_cd": "A", "params": {"stk_cd": "B"}}, ({"stk_cd": "B"}, "N", "")),
        ({}, ({}, "N", "")),
        ({"params": None}, ({}, "N", "")),
    ],
)
def test_split_arguments(arguments, expected):
    assert split_arguments(arguments) == expected


def test_split_arguments_rejects_non_object_params():
    with pytest.raises(ValueError, match="params"):
        split_arguments({"params": "stk_cd=005930"})


async def test_list_tools_carries_catalog_schema():
    app, _specs = build_server(api=None, allow_live_orders=False)
    handler = app.get_request_handler("tools/list").handler
    result = await handler(None, types.PaginatedRequestParams())
    tool = next(t for t in result.tools if t.name == "stock_info_basic_stock_info")
    assert tool.input_schema["properties"]["params"]["required"] == ["stk_cd"]


async def test_flat_fields_are_forwarded(httpx_mock, api):
    httpx_mock.add_response(
        url="https://mockapi.kiwoom.com/api/dostk/stkinfo",
        match_json={"stk_cd": "005930"},
        json={"return_code": 0, "return_msg": "OK", "stk_cd": "005930"},
    )
    specs = {s.tool_name: s for s in discover_rest_tools()}
    result = await dispatch_tool(
        api, None, specs, "stock_info_basic_stock_info", {"stk_cd": "005930"}
    )
    assert result is not None and result["stk_cd"] == "005930"
