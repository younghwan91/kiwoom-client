"""TR 카탈로그(kiwoom_client.spec)와 코드의 대응.

새 엔드포인트 메서드의 api_id 가 카탈로그에 없거나 URL 이 공식 명세와 다르면 여기서 깨진다.
그때는 ``scripts/build_spec_catalog.py`` 로 카탈로그를 다시 만들거나(공식 명세에 있으면)
``scripts/spec_supplement.json`` 에 근거와 함께 적는다(없으면).
"""

from __future__ import annotations

import json
from importlib import resources

import pytest

from kiwoom_client import spec
from kiwoom_client._registry import MODULE_NAMES, ModuleRegistry
from kiwoom_client.websocket import REALTIME_TYPES

#: 조건검색 WebSocket trnm ↔ 공식 명세 api_id.
CONDITION_SEARCH_IDS = {"CNSRLST": "ka10171", "CNSRREQ": "ka10172", "CNSRCLR": "ka10174"}


def _resource_urls() -> dict[str, str]:
    registry: ModuleRegistry = ModuleRegistry()
    registry._client = object()  # type: ignore[assignment]
    registry._init_modules()
    return {
        name: getattr(registry, name).RESOURCE_URL
        for name in MODULE_NAMES
        if name != "condition_search"
    }


def test_every_rest_method_is_indexed():
    index = spec.endpoint_index()
    # 182 = README 의 REST 엔드포인트 수. 메서드를 더하면 이 숫자도 함께 바뀐다.
    assert len(index) == len(set(index.values())) == 182


def test_every_code_api_id_has_a_catalog_entry():
    missing = sorted(set(spec.endpoint_index().values()) - set(spec.api_ids()))
    assert missing == [], f"카탈로그에 없는 api_id: {missing}"


def test_catalog_url_matches_module_resource_url():
    urls = _resource_urls()
    wrong = {
        f"{module}.{method}": (urls[module], spec.get(api_id).url)
        for (module, method), api_id in spec.endpoint_index().items()
        if spec.get(api_id).url != urls[module]
    }
    assert wrong == {}


def test_rest_methods_point_at_rest_trs():
    for api_id in spec.endpoint_index().values():
        assert spec.get(api_id).transport == "rest", api_id


def test_realtime_types_and_condition_search_are_cataloged():
    for real_type in REALTIME_TYPES:
        assert spec.get(real_type).transport == "websocket"
    for api_id in CONDITION_SEARCH_IDS.values():
        assert spec.get(api_id).transport == "websocket"


def test_catalog_schema():
    raw = json.loads(
        resources.files("kiwoom_client.spec").joinpath("catalog.json").read_text("utf-8")
    )
    assert raw["schema_version"] == 1
    assert len(raw["source"]["commit"]) == 40
    for api_id, tr in raw["trs"].items():
        assert tr["api_id"] == api_id
        assert tr["source"] in {"official", "repo"}
        assert tr["source"] == "official" or tr.get("note"), f"{api_id}: repo 출처면 근거 note 필수"
        for side in ("request", "response"):
            ids = set()
            for f in tr[side]:
                assert f["type"] in {"string", "list", "object"}, (api_id, f)
                assert isinstance(f["required"], bool)
                if "parent" in f:
                    assert f["parent"] in ids, (api_id, side, f["id"])
                ids.add(f["id"])


def test_get_and_required_fields():
    tr = spec.get("ka10001")
    assert tr.name == "주식기본정보요청"
    assert tr.url == "/api/dostk/stkinfo"
    assert tr.required_fields == ("stk_cd",)
    assert tr.request_field("stk_cd") is not None
    assert tr.request_field("nope") is None


def test_list_children_are_not_request_fields():
    tr = spec.get("ka10030")
    response_lists = [f for f in tr.response if f.type == "list"]
    assert response_lists, "당일거래량상위 응답은 list 를 갖는다"
    child = next(f for f in tr.response if f.parent == response_lists[0].id)
    assert child.id == "stk_cd"


def test_catalog_carries_no_field_descriptions_or_code_lists():
    # 키움 명세의 필드 설명 원문·코드값은 싣지 않는다 (SOURCE.md).
    # 속성은 하위 호환으로 남아 비어 있다.
    raw = json.loads(
        resources.files("kiwoom_client.spec").joinpath("catalog.json").read_text(encoding="utf-8")
    )
    for api_id, tr in raw["trs"].items():
        for f in (*tr["request"], *tr["response"]):
            assert not {"desc", "codes"} & set(f), f"{api_id}.{f['id']}"
    sort_tp = spec.get("ka10030").request_field("sort_tp")
    assert sort_tp is not None
    assert sort_tp.name == "정렬구분"
    assert sort_tp.desc == ""
    assert dict(sort_tp.codes) == {}


def test_for_method_and_unknown():
    assert spec.for_method("stock_info", "basic_stock_info").api_id == "ka10001"
    with pytest.raises(KeyError):
        spec.get("zz99999")
    with pytest.raises(KeyError):
        spec.for_method("stock_info", "nope")


def test_repo_sourced_entry_is_marked():
    tr = spec.get("ka10009")
    assert tr.source == "repo"
    assert tr.note


def test_search():
    ids = [tr.api_id for tr in spec.search("주식기본정보")]
    assert "ka10001" in ids
    assert [tr.api_id for tr in spec.search("KA10001")] == ["ka10001"]


class TestDescribe:
    def test_resolve_forms(self):
        from kiwoom_client import KiwoomAPI

        api = KiwoomAPI("k", "s", is_mock=True)
        assert spec.resolve("ka10001").api_id == "ka10001"
        assert spec.resolve("stock_info.basic_stock_info").api_id == "ka10001"
        assert spec.resolve("api.stock_info.basic_stock_info()").api_id == "ka10001"
        assert spec.resolve(api.stock_info.basic_stock_info).api_id == "ka10001"
        with pytest.raises(KeyError):
            spec.resolve(len)

    def test_method_for(self):
        assert spec.method_for("ka10001") == ("stock_info", "basic_stock_info")
        assert spec.method_for("0B") is None

    def test_describe_text(self):
        text = spec.describe("ka10030")
        assert text.splitlines()[0] == "ka10030 당일거래량상위요청 — POST /api/dostk/rkinfo"
        assert 'api.ranking.top_volume_today(mrkt_tp="...",' in text
        assert " *sort_tp" in text
        assert "코드:" not in text  # 카탈로그는 코드값을 싣지 않는다
        assert "tdy_trde_qty_upper[].stk_cd" in text

    def test_describe_on_both_facades_needs_no_network(self, httpx_mock):
        from kiwoom_client import AsyncKiwoomAPI, KiwoomAPI

        sync = KiwoomAPI("k", "s", is_mock=True)
        assert sync.describe("ka10001") == spec.describe("ka10001")
        assert AsyncKiwoomAPI("k", "s", is_mock=True).describe(sync.order.buy_order).startswith(
            "kt10000"
        )
        assert httpx_mock.get_requests() == []
class TestFieldNames:
    def test_realtime_fids(self):
        names = spec.field_names("0B")
        assert names["10"] == "현재가"
        assert names["20"] == "체결시간"

    def test_rest_response_fields(self):
        names = spec.field_names("ka10081")
        assert names["cur_prc"] == "현재가"
        assert names["stk_cd"] == "종목코드"

    def test_label_renames_and_keeps_unknown_keys(self):
        assert spec.label("0B", {"10": "-20800", "20": "165208", "zz": "1"}) == {
            "현재가": "-20800",
            "체결시간": "165208",
            "zz": "1",
        }

    def test_label_keeps_both_values_when_names_collide(self):
        # 0D(주식호가잔량)는 FID 23 과 291 이 둘 다 "예상체결가" 다 (공식 명세 기준).
        names = spec.field_names("0D")
        assert names["23"] == names["291"] == "예상체결가"
        assert spec.label("0D", {"23": "1", "291": "2"}) == {
            "예상체결가": "1",
            "예상체결가(291)": "2",
        }

    def test_unknown_api_id(self):
        with pytest.raises(KeyError):
            spec.field_names("zz99999")
