"""Default and maximum row counts for intent tool responses.

Every list an intent tool returns is bounded, so one call can never flood
the agent's context. A tool reads its ``count`` argument through
:func:`row_count`, which clamps it into ``[1, maximum]``.
"""

from __future__ import annotations

from typing import Any

#: Rows returned when the caller doesn't ask for a number.
DEFAULT_ROWS = 20

#: Hard ceiling for any single list in an intent response.
MAX_ROWS = 500


def row_count(value: Any, *, default: int = DEFAULT_ROWS, maximum: int = MAX_ROWS) -> int:
    """``value`` as a row count in ``[1, maximum]``; ``default`` when unset.

    Raises:
        ValueError: if ``value`` is not an integer.
    """
    if value is None or (isinstance(value, str) and not value.strip()):
        return default
    if isinstance(value, bool):
        raise ValueError(f"count 는 정수여야 합니다: {value!r}")
    try:
        number = int(str(value).strip())
    except ValueError as exc:
        raise ValueError(f"count 는 정수여야 합니다: {value!r}") from exc
    return max(1, min(number, maximum))


def count_schema(default: int = DEFAULT_ROWS, maximum: int = MAX_ROWS) -> dict[str, Any]:
    """JSON schema for a ``count`` argument."""
    return {
        "type": "integer",
        "minimum": 1,
        "maximum": maximum,
        "default": default,
        "description": f"돌려줄 행 수 (기본 {default}, 최대 {maximum})",
    }
