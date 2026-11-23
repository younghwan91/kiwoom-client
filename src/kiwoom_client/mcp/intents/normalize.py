"""Shared normalisation for intent tool responses.

Kiwoom sends every value as a string, in several shapes:

- signed and grouped: ``"+70000"``, ``"-1,200"``
- zero-padded, sign first: ``"000000070000"``, ``"-00000001200"``
- a price whose sign is the *direction* of the move, not a negative price
  (``cur_prc="-70000"`` on a falling stock)

Intent tools return plain numbers with readable keys, so the agent never
parses these itself. Identifiers (codes, order numbers) stay strings.
"""

from __future__ import annotations

import re
from collections.abc import Mapping
from typing import Any

_NUMBER = re.compile(r"^[+-]?\d+(\.\d+)?$")


def num(value: Any) -> int | float | None:
    """Kiwoom numeric string → int/float, sign kept; ``None`` if blank or not a number.

    ``"+70,000"`` → 70000, ``"-00000001200"`` → -1200, ``"000000070000"`` → 70000,
    ``"-1.25"`` → -1.25, ``"12.50%"`` → 12.5.
    """
    if value is None or isinstance(value, bool):
        return None
    if isinstance(value, (int, float)):
        return value
    text = str(value).strip().replace(",", "").rstrip("%").strip()
    if not _NUMBER.match(text):
        return None
    if "." in text:
        return float(text)
    return int(text)


def price(value: Any) -> int | float | None:
    """A price or a volume: never negative, so a direction sign is dropped."""
    number = num(value)
    return None if number is None else abs(number)


def pct(value: Any) -> float | None:
    """A percentage as a float (``"+1.25"`` → 1.25, ``"-0.50"`` → -0.5)."""
    number = num(value)
    return None if number is None else float(number)


def date(value: Any) -> str | None:
    """Kiwoom date/time text → ISO 8601.

    ``"20261124"`` → ``"2026-11-24"``, ``"202611241530"`` → ``"2026-11-24T15:30"``,
    ``"20261124153000"`` → ``"2026-11-24T15:30:00"``, ``"153000"`` → ``"15:30:00"``.
    Anything else is returned stripped (``None`` if blank).
    """
    if value is None:
        return None
    text = str(value).strip()
    if not text:
        return None
    if not text.isdigit():
        return text
    if len(text) == 8:
        return f"{text[:4]}-{text[4:6]}-{text[6:]}"
    if len(text) == 12:
        return f"{text[:4]}-{text[4:6]}-{text[6:8]}T{text[8:10]}:{text[10:]}"
    if len(text) == 14:
        return f"{text[:4]}-{text[4:6]}-{text[6:8]}T{text[8:10]}:{text[10:12]}:{text[12:]}"
    if len(text) == 6:
        return f"{text[:2]}:{text[2:4]}:{text[4:]}"
    return text


def text(value: Any) -> str | None:
    """A string field, stripped; ``None`` if blank."""
    if value is None:
        return None
    stripped = str(value).strip()
    return stripped or None


def stock_code(value: Any) -> str | None:
    """Plain 6-character stock code.

    Account and condition-search TRs prefix the code with its instrument
    type (``"A005930"`` stock, ``"J"`` ELW, ``"Q"`` ETN); that prefix is dropped.
    Exchange suffixes (``"_NX"``, ``"_AL"``) are dropped too.
    """
    code = text(value)
    if code is None:
        return None
    code = code.split("_", 1)[0]
    if len(code) == 7 and code[0] in "AJQ":
        code = code[1:]
    return code


def mask_account(value: Any) -> str | None:
    """Account number with all but the last 4 characters masked."""
    account = text(value)
    if account is None:
        return None
    return "*" * max(len(account) - 4, 0) + account[-4:]


def pick(record: Mapping[str, Any], fields: Mapping[str, tuple[str, Any]]) -> dict[str, Any]:
    """Build an output row: ``{out_key: (source_field, converter)}``.

    Source fields absent from ``record`` are left out of the row, so a TR
    that doesn't send a field never shows a made-up ``None`` for it.
    """
    row: dict[str, Any] = {}
    for key, (source, convert) in fields.items():
        if source in record:
            row[key] = convert(record[source])
    return row
