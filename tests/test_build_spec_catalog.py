"""scripts/build_spec_catalog.py 의 변환 규칙 (네트워크 없이 작은 표본으로)."""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

import pytest

_SCRIPT = Path(__file__).resolve().parent.parent / "scripts" / "build_spec_catalog.py"


@pytest.fixture(scope="module")
def build():
    spec = importlib.util.spec_from_file_location("build_spec_catalog", _SCRIPT)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules["build_spec_catalog"] = module
    spec.loader.exec_module(module)
    return module


@pytest.mark.parametrize(
    ("desc", "codes"),
    [
        ("0:보통 , 3:시장가 , 5:조건부지정가", {"0": "보통", "3": "시장가", "5": "조건부지정가"}),
        ("1:KRX, 2:NXT 3.통합", {"1": "KRX", "2": "NXT", "3": "통합"}),
        ("Y:연속조회요청,N:연속조회미요청", {"Y": "연속조회요청", "N": "연속조회미요청"}),
        ("코스피:0, 코스닥:1", {"0": "코스피", "1": "코스닥"}),
        ("0:조건검색", {"0": "조건검색"}),
        ("단위: 원", {}),
        ("거래소별 종목코드\n(KRX:039490,NXT:039490_NX,SOR:039490_AL)", {}),
        ("", {}),
    ],
)
def test_parse_codes(build, desc, codes):
    assert build.parse_codes(desc) == codes


def test_convert_fields_links_list_children(build):
    rows = [
        {"element": "items", "depth": 0, "is_section": False, "한글명": "목록", "type": "LIST",
         "required": "N", "length": "", "description": ""},
        {"element": "stk_cd", "depth": 1, "is_section": False, "한글명": "종목코드",
         "type": "String", "required": "N", "length": "20", "description": ""},
        {"element": "구분", "depth": 0, "is_section": True, "한글명": "", "type": "",
         "required": "", "length": "", "description": ""},
        {"element": "qry_tp", "depth": 0, "is_section": False, "한글명": "조회구분",
         "type": "String", "required": "Y", "length": "1", "description": "0:전체, 1:일부"},
    ]
    assert build.convert_fields(rows) == [
        {"id": "items", "name": "목록", "type": "list", "required": False},
        {"id": "stk_cd", "name": "종목코드", "type": "string", "length": 20, "required": False,
         "parent": "items"},
        {"id": "qry_tp", "name": "조회구분", "type": "string", "length": 1, "required": True,
         "desc": "0:전체, 1:일부", "codes": {"0": "전체", "1": "일부"}},
    ]


def test_convert_keeps_only_domestic_and_oauth(build):
    def entry(api_id, menu, url):
        return {"meta": {"API ID": api_id, "API 명": api_id, "메뉴 위치": menu, "URL": url},
                "request": {"body": []}, "response": {"body": []}}

    spec = {"apis": {
        "a": entry("ka10001", "국내주식 > 종목정보 > 주식기본정보(ka10001)", "/api/dostk/stkinfo"),
        "b": entry("usa10100", "미국주식 > 종목정보 > 종목 조회(usa10100)", "/api/us/stkinfo"),
        "c": entry("0B", "국내주식 > 실시간시세 > 주식체결(0B)", "/api/dostk/websocket"),
    }}
    trs = build.convert(spec)
    assert sorted(trs) == ["0B", "ka10001"]
    assert trs["ka10001"]["menu"] == ["국내주식", "종목정보"]
    assert trs["0B"]["transport"] == "websocket"
