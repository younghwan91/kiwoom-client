"""Mask account numbers in data the MCP server writes or returns.

Which keys hold an account number comes from the TR catalog — every request
or response field whose name is 계좌번호 (``acnt_no``, ``acctNo``,
``acnt_print``, real-time ``9201`` ...) — so a TR added later is covered
without a list to maintain here.
"""

from __future__ import annotations

import os
from collections.abc import Mapping
from functools import lru_cache
from typing import Any

from kiwoom_client import spec
from kiwoom_client._env import parse_bool

#: ``false`` returns account numbers in MCP responses unmasked (default: masked).
ENV_VAR = "KIWOOM_MCP_MASK_ACCOUNTS"


def mask_from_env(env: Mapping[str, str] | None = None) -> bool:
    """``KIWOOM_MCP_MASK_ACCOUNTS`` (unset = true).

    Raises:
        ValueError: a value that is not a recognised boolean.
    """
    source = os.environ if env is None else env
    value = source.get(ENV_VAR, "")
    return parse_bool(value, ENV_VAR) if value.strip() else True

#: Always masked, whatever the catalog says.
_ALWAYS = frozenset({"acnt_no", "acctNo", "acnt_print", "9201"})


@lru_cache(maxsize=1)
def account_fields() -> frozenset[str]:
    """Keys that carry an account number."""
    found = set(_ALWAYS)
    for api_id in spec.api_ids():
        tr = spec.get(api_id)
        for field in (*tr.request, *tr.response):
            if field.name.replace(" ", "") == "계좌번호":
                found.add(field.id)
    return frozenset(found)


def mask_account(value: Any) -> Any:
    """``"1234567890"`` → ``"******7890"``. Non-strings and blanks pass through."""
    if not isinstance(value, str) or not value.strip():
        return value
    account = value.strip()
    return "*" * max(len(account) - 4, 0) + account[-4:]


def mask_accounts(value: Any) -> Any:
    """A copy of ``value`` (dicts/lists, any depth) with account numbers masked."""
    if isinstance(value, dict):
        keys = account_fields()
        return {
            k: mask_account(v) if k in keys else mask_accounts(v) for k, v in value.items()
        }
    if isinstance(value, list):
        return [mask_accounts(v) for v in value]
    return value
