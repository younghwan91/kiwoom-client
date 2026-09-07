"""Tests for reflection-based REST tool discovery."""

from __future__ import annotations

import inspect

from kiwoom_client._registry import MODULE_NAMES, ModuleRegistry
from kiwoom_client.mcp.tools import GUARDED_MODULES, RestToolSpec, discover_rest_tools


def _expected_method_count() -> int:
    """condition_search 를 제외한 14개 모듈의 public 메서드 총합."""
    registry = ModuleRegistry()
    registry._client = object()
    registry._init_modules()
    total = 0
    for name in MODULE_NAMES:
        if name == "condition_search":
            continue
        module_obj = getattr(registry, name)
        total += sum(
            1
            for method_name, _ in inspect.getmembers(module_obj, inspect.ismethod)
            if not method_name.startswith("_")
        )
    return total


class TestDiscoverRestTools:
    def test_covers_every_public_method(self):
        specs = discover_rest_tools()
        assert len(specs) == _expected_method_count()

    def test_excludes_condition_search(self):
        specs = discover_rest_tools()
        assert all(spec.module_name != "condition_search" for spec in specs)

    def test_tool_name_is_module_underscore_method(self):
        specs = discover_rest_tools()
        by_name = {spec.tool_name: spec for spec in specs}
        assert "order_buy_order" in by_name
        spec = by_name["order_buy_order"]
        assert spec.module_name == "order"
        assert spec.method_name == "buy_order"

    def test_description_comes_from_docstring(self):
        specs = discover_rest_tools()
        buy = next(s for s in specs if s.tool_name == "order_buy_order")
        assert "매수" in buy.description

    def test_order_and_credit_order_are_guarded(self):
        specs = discover_rest_tools()
        for spec in specs:
            assert spec.guarded == (spec.module_name in GUARDED_MODULES)

    def test_guarded_modules_is_order_and_credit_order(self):
        assert frozenset({"order", "credit_order"}) == GUARDED_MODULES

    def test_returns_rest_tool_spec_instances(self):
        specs = discover_rest_tools()
        assert all(isinstance(spec, RestToolSpec) for spec in specs)
