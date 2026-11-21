"""Read Kiwoom credentials from the environment or a ``.env`` file.

Backs ``KiwoomAPI.from_env()`` / ``AsyncKiwoomAPI.from_env()``. The variable
names match the MCP server (``KIWOOM_APP_KEY``, ``KIWOOM_APP_SECRET``,
``KIWOOM_IS_MOCK``) so one ``.env`` drives both.

The ``.env`` parser is deliberately small — ``KEY=VALUE`` lines, optional
``export`` prefix, single/double quotes, ``#`` comments — so the package keeps
its two runtime dependencies.
"""

from __future__ import annotations

import logging
import os
from collections.abc import Mapping
from pathlib import Path
from typing import NamedTuple

logger = logging.getLogger("kiwoom_client")

ENV_APP_KEY = "KIWOOM_APP_KEY"
ENV_APP_SECRET = "KIWOOM_APP_SECRET"
ENV_IS_MOCK = "KIWOOM_IS_MOCK"

_TRUE = frozenset({"1", "true", "yes", "y", "on"})
_FALSE = frozenset({"0", "false", "no", "n", "off"})


class EnvCredentials(NamedTuple):
    app_key: str
    app_secret: str
    is_mock: bool


def read_env_file(path: str | os.PathLike[str]) -> dict[str, str]:
    """Parse a ``.env`` file into a dict.

    Supports ``KEY=VALUE``, ``export KEY=VALUE``, values wrapped in single or
    double quotes, full-line ``#`` comments and `` #`` trailing comments on
    unquoted values. Variable expansion (``${OTHER}``) is not performed.

    Raises:
        FileNotFoundError: If ``path`` does not exist.
    """
    values: dict[str, str] = {}
    text = Path(path).read_text(encoding="utf-8-sig")
    for raw in text.splitlines():
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        if line.startswith("export "):
            line = line[len("export ") :].lstrip()
        key, sep, value = line.partition("=")
        key = key.strip()
        if not sep or not key:
            continue
        value = value.strip()
        if len(value) >= 2 and value[0] == value[-1] and value[0] in ("'", '"'):
            value = value[1:-1]
        else:
            comment = value.find(" #")
            if comment != -1:
                value = value[:comment].rstrip()
        values[key] = value
    return values


def parse_bool(value: str, name: str = ENV_IS_MOCK) -> bool:
    """Parse a boolean environment value strictly.

    Accepts ``true/false``, ``1/0``, ``yes/no``, ``y/n``, ``on/off`` (any case).
    Anything else raises instead of silently meaning "live trading".

    Raises:
        ValueError: If the value is not a recognised boolean.
    """
    lowered = value.strip().lower()
    if lowered in _TRUE:
        return True
    if lowered in _FALSE:
        return False
    raise ValueError(
        f"{name}={value!r} 를 해석할 수 없습니다. true/false (또는 1/0, yes/no) 로 지정하세요."
    )


def resolve_credentials(
    env_file: str | os.PathLike[str] | None = None,
    *,
    is_mock: bool | None = None,
    environ: Mapping[str, str] | None = None,
) -> EnvCredentials:
    """Collect app key, secret and the mock flag.

    Process environment variables win over the ``.env`` file (same rule as
    python-dotenv), and an explicit ``is_mock`` argument wins over both.

    When ``KIWOOM_IS_MOCK`` is set nowhere and ``is_mock`` is not passed, the
    result is ``is_mock=False`` — the **live** server, the same default as the
    ``KiwoomAPI`` constructor and the MCP server — and a warning is logged.

    Raises:
        FileNotFoundError: If ``env_file`` is given but does not exist.
        ValueError: If the key/secret are missing or ``KIWOOM_IS_MOCK`` is not
            a recognised boolean.
    """
    source = os.environ if environ is None else environ
    file_values = read_env_file(env_file) if env_file is not None else {}

    def lookup(name: str) -> str | None:
        value = source.get(name)
        if value is None or not value.strip():
            value = file_values.get(name)
        if value is None or not value.strip():
            return None
        return value.strip()

    app_key = lookup(ENV_APP_KEY)
    app_secret = lookup(ENV_APP_SECRET)
    missing = [
        name
        for name, value in ((ENV_APP_KEY, app_key), (ENV_APP_SECRET, app_secret))
        if value is None
    ]
    if missing:
        where = "환경변수" + (f" 또는 {os.fspath(env_file)}" if env_file is not None else "")
        raise ValueError(f"{', '.join(missing)} 가 {where} 에 없습니다.")
    assert app_key is not None and app_secret is not None

    if is_mock is None:
        raw_mock = lookup(ENV_IS_MOCK)
        if raw_mock is None:
            logger.warning(
                "%s 가 설정되지 않아 실전투자 서버(api.kiwoom.com)에 연결합니다. "
                "모의투자라면 %s=true 로 지정하세요.",
                ENV_IS_MOCK,
                ENV_IS_MOCK,
            )
            is_mock = False
        else:
            is_mock = parse_bool(raw_mock)

    return EnvCredentials(app_key, app_secret, is_mock)
