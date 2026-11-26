"""``kiwoom --demo``: every read command offline, a banner first, keys ignored."""

from __future__ import annotations

import json

import pytest

from kiwoom_client import cli
from tests.demo_support import no_network  # noqa: F401

pytestmark = pytest.mark.usefixtures("no_network")


@pytest.mark.parametrize(
    "argv",
    [
        ["--demo", "quote", "삼성전자"],
        ["quote", "005930", "--demo"],
        ["--demo", "chart", "SK하이닉스", "-n", "3"],
        ["--demo", "chart", "005930", "--weekly"],
        ["--demo", "chart", "005930", "--minute", "--scope", "5", "-n", "3"],
        ["--demo", "balance"],
        ["--demo", "find", "삼성"],
    ],
)
def test_banner_is_the_first_line(argv, capsys, monkeypatch):
    for name in ("KIWOOM_APP_KEY", "KIWOOM_APP_SECRET", "KIWOOM_IS_MOCK"):
        monkeypatch.delenv(name, raising=False)
    assert cli.main(argv) == 0
    out, err = capsys.readouterr()
    assert out.splitlines()[0] == cli.DEMO_BANNER
    assert err == ""


def test_quote_shows_the_demo_stock(capsys):
    assert cli.main(["--demo", "quote", "삼성전자"]) == 0
    out = capsys.readouterr().out
    assert "삼성전자 (005930)" in out and "현재가" in out


def test_json_stays_parseable_and_carries_the_marker(capsys):
    assert cli.main(["--demo", "--json", "quote", "005930"]) == 0
    out, err = capsys.readouterr()
    assert json.loads(out)["_demo"]
    assert cli.DEMO_BANNER in err


def test_real_keys_are_ignored_with_a_warning(capsys, monkeypatch):
    monkeypatch.setenv("KIWOOM_APP_KEY", "a-real-looking-key")
    monkeypatch.setenv("KIWOOM_APP_SECRET", "a-real-looking-secret")
    assert cli.main(["--demo", "quote", "005930"]) == 0  # no network: the key is never used
    out, err = capsys.readouterr()
    assert "쓰지 않습니다" in err and out.startswith(cli.DEMO_BANNER)


def test_demo_excludes_mock_and_live():
    with pytest.raises(SystemExit):
        cli.main(["--demo", "--live", "quote", "005930"])
