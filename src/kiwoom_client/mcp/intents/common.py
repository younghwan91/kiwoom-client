"""Small helpers several intent modules share: today's date in Korea, date
arguments, and following Kiwoom's continuation headers."""

from __future__ import annotations

import re
from collections.abc import Awaitable, Callable
from datetime import datetime, timedelta, timezone
from typing import Any

#: Korea Standard Time. Fixed offset (no DST), so no tz database is needed.
KST = timezone(timedelta(hours=9))

#: Pages followed at most for one intent call, whatever ``count`` asks for.
MAX_PAGES = 10

_DATE_ARG = re.compile(r"^(\d{4})-?(\d{2})-?(\d{2})$")


def today_kst() -> str:
    """Today in Korea as ``YYYYMMDD`` (Kiwoom's date format)."""
    return datetime.now(KST).strftime("%Y%m%d")


def date_arg(value: Any, name: str = "date") -> str | None:
    """``"2026-11-24"`` or ``"20261124"`` → ``"20261124"``; ``None`` if unset.

    Raises:
        ValueError: anything else.
    """
    if value is None or not str(value).strip():
        return None
    match = _DATE_ARG.match(str(value).strip())
    if match is None:
        raise ValueError(f"{name} 는 YYYY-MM-DD 또는 YYYYMMDD 형식이어야 합니다: {value!r}")
    return "".join(match.groups())


async def fetch_rows(
    method: Callable[..., Awaitable[dict[str, Any]]],
    key: str,
    params: dict[str, Any],
    *,
    want: int,
    max_pages: int = MAX_PAGES,
) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    """Call ``method`` page after page until ``want`` rows of ``key`` are in.

    Returns ``(first_page, rows)``. Stops early when Kiwoom says there is no
    next page (``cont-yn`` not ``Y``). Each page goes through the client's
    per-TR rate limiter like any other call.
    """
    first: dict[str, Any] | None = None
    rows: list[dict[str, Any]] = []
    cont_yn, next_key = "N", ""
    for _ in range(max_pages):
        resp = await method(cont_yn=cont_yn, next_key=next_key, **params)
        if first is None:
            first = resp
        rows.extend(row for row in resp.get(key) or [] if isinstance(row, dict))
        next_key = str(resp.get("next-key") or "")
        if len(rows) >= want or resp.get("cont-yn") != "Y" or not next_key:
            break
        cont_yn = "Y"
    return first or {}, rows
