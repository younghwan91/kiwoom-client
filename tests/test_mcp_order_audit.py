"""Order audit log: every preview, refusal and send as one JSONL line —
without keys or tokens, with account numbers masked."""

from __future__ import annotations

import json
import stat
import sys

import pytest

from kiwoom_client import AsyncKiwoomAPI
from kiwoom_client.mcp.masking import account_fields, mask_accounts
from kiwoom_client.mcp.orders.audit import AuditLog
from kiwoom_client.mcp.orders.policy import AUDIT_LOG_ENV, DEFAULT_AUDIT_LOG, OrderPolicy
from kiwoom_client.mcp.server import build_server
from tests.mcp_order_helpers import (
    BUY,
    BUY_PARAMS,
    ORDR,
    mock_lookups,
    mock_token,
    ok,
    order_requests,
    refused,
)

APP_KEY, APP_SECRET = "app-key-AUDIT-TEST", "app-secret-AUDIT-TEST"


def _lines(path) -> list[dict]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines()]


class TestPolicy:
    def test_default_path_when_unset(self):
        assert OrderPolicy.from_env(is_mock=True, env={}).audit_log == DEFAULT_AUDIT_LOG

    @pytest.mark.parametrize("value", ["off", "OFF", "false", "0", "none", "no"])
    def test_can_be_turned_off(self, value):
        assert OrderPolicy.from_env(is_mock=False, env={AUDIT_LOG_ENV: value}).audit_log is None

    def test_custom_path(self):
        env = {AUDIT_LOG_ENV: "/var/log/kiwoom.jsonl"}
        assert OrderPolicy.from_env(is_mock=False, env=env).audit_log == "/var/log/kiwoom.jsonl"

    def test_bare_policy_writes_nothing(self):
        assert OrderPolicy().audit_log is None


class TestMasking:
    def test_catalog_account_fields(self):
        assert {"acnt_no", "acctNo", "acnt_print", "9201"} <= account_fields()

    def test_nested(self):
        masked = mask_accounts({"acnt_no": "1234567890", "rows": [{"acctNo": "5555-6666"}],
                                "stk_cd": "005930"})  # fmt: skip
        assert masked == {"acnt_no": "******7890", "rows": [{"acctNo": "*****6666"}],
                          "stk_cd": "005930"}  # fmt: skip


@pytest.fixture
async def api(httpx_mock):
    mock_token(httpx_mock)
    mock_lookups(httpx_mock)
    api = AsyncKiwoomAPI(APP_KEY, APP_SECRET, is_mock=True)
    await api.login()
    yield api
    await api.close()


def _app(api, path, **policy):
    order_policy = OrderPolicy(audit_log=str(path), **policy)
    app, _ = build_server(api, allow_live_orders=True, order_policy=order_policy)
    return app


class TestEvents:
    async def test_preview_send_and_refusal(self, httpx_mock, api, tmp_path):
        reply = {"return_code": 0, "return_msg": "OK", "ord_no": "0000123", "acnt_no": "1234567890"}
        httpx_mock.add_response(url=ORDR, json=reply)
        log = tmp_path / "audit" / "mcp-audit.jsonl"
        app = _app(api, log)
        preview = await ok(app, "order_preview", BUY)
        token = preview["confirm_token"]
        await ok(app, "order_buy_order", {"params": BUY_PARAMS, "confirm_token": token})
        await refused(app, "order_buy_order", {"params": BUY_PARAMS, "confirm_token": token})

        events = _lines(log)
        assert [e["event"] for e in events] == ["preview", "sent", "rejected"]
        assert events[0]["token_issued"] is True and events[0]["tool"] == "order_buy_order"
        assert events[1]["result"] == {"return_code": 0, "return_msg": "OK", "ord_no": "0000123"}
        assert events[1]["params"] == BUY_PARAMS and events[1]["via"] == "order_buy_order"
        assert events[2]["reasons"] and events[2]["token_given"] is True
        assert all(e["ts"].endswith("+09:00") for e in events)

        text = log.read_text(encoding="utf-8")
        for secret in (token, APP_KEY, APP_SECRET, "test_token", "1234567890"):
            assert secret not in text
        if sys.platform != "win32":  # Windows has no POSIX permission bits
            assert stat.S_IMODE(log.stat().st_mode) == 0o600
            assert stat.S_IMODE(log.parent.stat().st_mode) == 0o700

    async def test_high_level_tool_is_logged_with_its_own_name(self, httpx_mock, api, tmp_path):
        log = tmp_path / "a.jsonl"
        app = _app(api, log)
        args = {"stock": "005930", "side": "buy", "qty": 10, "price": 70000}
        await refused(app, "place_order", args)
        (event,) = _lines(log)
        assert event == {**event, "event": "rejected", "via": "place_order",
                         "tool": "order_buy_order", "token_given": False}  # fmt: skip

    async def test_failed_send_is_logged(self, httpx_mock, api, tmp_path):
        httpx_mock.add_response(url=ORDR, json={"return_code": 20, "return_msg": "주문 실패"})
        log = tmp_path / "a.jsonl"
        app = _app(api, log, require_confirm=False)
        await refused(app, "order_buy_order", {"params": BUY_PARAMS})
        (event,) = _lines(log)
        assert event["event"] == "failed" and "주문 실패" in event["error"]

    async def test_account_numbers_in_params_are_masked(self, api, tmp_path):
        log = tmp_path / "a.jsonl"
        app = _app(api, log, require_confirm=False)
        await refused(app, "order_buy_order", {"params": {**BUY_PARAMS, "acnt_no": "1234567890"}})
        (event,) = _lines(log)
        assert event["params"]["acnt_no"] == "******7890"

    async def test_off_writes_nothing(self, api, tmp_path, monkeypatch):
        monkeypatch.setenv("HOME", str(tmp_path))
        app, _ = build_server(api, allow_live_orders=True, order_policy=OrderPolicy())
        await refused(app, "order_buy_order", {"params": BUY_PARAMS})
        assert list(tmp_path.iterdir()) == []

    async def test_write_failure_never_blocks_an_order(self, httpx_mock, api, tmp_path, caplog):
        httpx_mock.add_response(url=ORDR, json={"return_code": 0, "ord_no": "1"})
        blocker = tmp_path / "not-a-dir"
        blocker.write_text("x")
        app = _app(api, blocker / "audit.jsonl", require_confirm=False)
        await ok(app, "order_buy_order", {"params": BUY_PARAMS})
        assert len(order_requests(httpx_mock)) == 1
        assert "감사 로그" in caplog.text


class TestAuditLog:
    def test_skips_none_fields(self, tmp_path):
        log = AuditLog(tmp_path / "x.jsonl")
        log.record("preview", tool="t", errors=None)
        (line,) = _lines(tmp_path / "x.jsonl")
        assert "errors" not in line
