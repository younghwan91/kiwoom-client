"""spec/responses.py (scripts/build_response_types.py) — 카탈로그와 같고 mypy 가 읽는다."""

from __future__ import annotations

import importlib.util
import re
import sys
from pathlib import Path
from typing import get_type_hints

import pytest

from kiwoom_client import spec
from kiwoom_client.spec import responses

_SCRIPT = Path(__file__).resolve().parent.parent / "scripts" / "build_response_types.py"


@pytest.fixture(scope="module")
def build():
    module_spec = importlib.util.spec_from_file_location("build_response_types", _SCRIPT)
    assert module_spec is not None and module_spec.loader is not None
    module = importlib.util.module_from_spec(module_spec)
    sys.modules["build_response_types"] = module
    module_spec.loader.exec_module(module)
    return module


def test_responses_module_is_up_to_date(build):
    assert Path(responses.__file__).read_text(encoding="utf-8") == build.render(), (
        "`uv run python scripts/build_response_types.py` 로 다시 만들 것"
    )


def test_every_selected_tr_has_a_response_type(build):
    for api_id in build.SELECTED:
        _, method = spec.method_for(api_id) or ("", "")
        name = build._camel(method) + "Response"
        cls = getattr(responses, name)
        hints = get_type_hints(cls)
        assert hints["return_code"] is int
        top = {f.id for f in spec.get(api_id).response if f.parent is None}
        assert top <= set(hints), api_id


def test_list_field_points_at_item_type():
    hints = get_type_hints(responses.StockDailyChartResponse)
    assert hints["stk_dt_pole_chart_qry"] == list[responses.StockDailyChartItem]
    assert get_type_hints(responses.StockDailyChartItem)["cur_prc"] is str


def test_non_identifier_keys_use_functional_syntax():
    assert "250hgst" in get_type_hints(responses.BasicStockInfoResponse)


def test_mypy_reads_the_types(tmp_path):
    api = pytest.importorskip("mypy.api")
    snippet = tmp_path / "snippet.py"
    snippet.write_text(
        "from typing import cast\n"
        "from kiwoom_client import KiwoomAPI\n"
        "from kiwoom_client.spec.responses import StockDailyChartResponse\n"
        "\n"
        "def f(api: KiwoomAPI) -> None:\n"
        "    resp = cast(StockDailyChartResponse, api.chart.stock_daily_chart(stk_cd='005930'))\n"
        "    for bar in resp.get('stk_dt_pole_chart_qry', []):\n"
        "        reveal_type(bar['cur_prc'])\n"
        "        bar['no_such_field']\n",
        encoding="utf-8",
    )
    stdout, _, _ = api.run([str(snippet), "--no-error-summary", "--hide-error-context"])
    # mypy 버전에 따라 "builtins.str" 또는 "str" 로 찍는다.
    assert re.search(r'Revealed type is "(builtins\.)?str"', stdout), stdout
    errors = [ln for ln in stdout.splitlines() if ": error:" in ln]
    assert len(errors) == 1 and "no_such_field" in errors[0], stdout
