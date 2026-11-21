"""domestic/*.pyi 스텁 — 카탈로그와 같고, 런타임 시그니처와 호환되고, mypy 가 실제로 읽는다."""

from __future__ import annotations

import ast
import importlib.util
import inspect
import sys
from pathlib import Path

import pytest

from kiwoom_client._registry import MODULE_NAMES, ModuleRegistry

_SCRIPT = Path(__file__).resolve().parent.parent / "scripts" / "build_stubs.py"
REST_MODULES = [m for m in MODULE_NAMES if m != "condition_search"]


@pytest.fixture(scope="module")
def build_stubs():
    spec = importlib.util.spec_from_file_location("build_stubs", _SCRIPT)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules["build_stubs"] = module
    spec.loader.exec_module(module)
    return module


def _module_obj(name: str):
    registry: ModuleRegistry = ModuleRegistry()
    registry._client = object()  # type: ignore[assignment]
    registry._init_modules()
    return getattr(registry, name)


def test_stubs_are_up_to_date(build_stubs):
    stale = [
        path.name
        for path, text in build_stubs.render_all().items()
        if not path.exists() or path.read_text(encoding="utf-8") != text
    ]
    assert stale == [], f"`uv run python scripts/build_stubs.py` 로 다시 만들 것: {stale}"


@pytest.mark.parametrize("module_name", REST_MODULES)
def test_stub_matches_runtime_signature(module_name):
    module_obj = _module_obj(module_name)
    stub = Path(inspect.getfile(type(module_obj))).with_suffix(".pyi")
    tree = ast.parse(stub.read_text(encoding="utf-8"))
    cls = next(n for n in tree.body if isinstance(n, ast.ClassDef))
    stub_methods = {
        n.name: n for n in cls.body if isinstance(n, ast.FunctionDef) and not n.name.startswith("_")
    }
    runtime = {
        name for name, _ in inspect.getmembers(module_obj, inspect.ismethod)
        if not name.startswith("_")
    }
    assert set(stub_methods) == runtime

    for name, fn in stub_methods.items():
        # 런타임과 같은 위치 인자 (self, cont_yn, next_key) + **kwargs 를 그대로 둔다.
        assert [a.arg for a in fn.args.args] == ["self", "cont_yn", "next_key"], name
        assert fn.args.kwarg is not None and fn.args.kwarg.arg == "kwargs", name
        # 요청 필드는 모두 키워드 전용이고 기본값이 있다 — 기존 호출이 mypy 에서 깨지지 않는다.
        assert len(fn.args.kw_defaults) == len(fn.args.kwonlyargs), name
        assert all(d is not None for d in fn.args.kw_defaults), name


def test_mypy_sees_request_fields(tmp_path):
    api = pytest.importorskip("mypy.api")
    snippet = tmp_path / "snippet.py"
    snippet.write_text(
        "from kiwoom_client import AsyncKiwoomAPI, KiwoomAPI\n"
        "\n"
        "def sync(api: KiwoomAPI, body: dict[str, str]) -> None:\n"
        "    api.stock_info.basic_stock_info(stk_cd='005930')\n"
        "    api.order.buy_order(**body)\n"
        "    api.ranking.top_volume_today(mrkt_tp='000', not_in_catalog='x')\n"
        "    api.stock_info.basic_stock_info(stk_cd=5930)  # E: int 는 str 이 아니다\n"
        "\n"
        "async def run(api: AsyncKiwoomAPI) -> None:\n"
        "    info = await api.stock_info.basic_stock_info(stk_cd='005930', cont_yn='Y')\n"
        "    reveal_type(info)\n",
        encoding="utf-8",
    )
    stdout, _, status = api.run([str(snippet), "--no-error-summary", "--hide-error-context"])
    lines = [ln for ln in stdout.splitlines() if ln.strip()]
    errors = [ln for ln in lines if ": error:" in ln]
    assert len(errors) == 1, stdout
    assert ":7:" in errors[0] and '"stk_cd"' in errors[0]
    assert any("dict[str, Any]" in ln for ln in lines if "note: Revealed type" in ln), stdout
    assert status == 1
