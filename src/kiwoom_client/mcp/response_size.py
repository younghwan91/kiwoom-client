"""Opt-in truncation of large list responses, to protect the agent's context.

Many Kiwoom TRs return hundreds of rows (차트, 순위, 종목 리스트). Every row
lands in the agent's context. A tool call may pass ``max_rows`` (or the
server may set a default via ``KIWOOM_MCP_MAX_ROWS`` / ``--max-rows``) to
keep only the first N rows of each top-level list. Nothing is cut unless one
of them is set — the default response is exactly what Kiwoom returned.

When rows are cut the response says so, under ``"_truncated"``, so the agent
never mistakes a partial list for the whole one.
"""

from __future__ import annotations

import os
from collections.abc import Mapping
from typing import Any

#: Server-wide default for ``max_rows`` (positive integer). Unset = no limit.
ENV_VAR = "KIWOOM_MCP_MAX_ROWS"

#: Name of the per-call argument. Removed before the request is sent.
ARGUMENT = "max_rows"

#: Key added to a truncated response.
MARKER = "_truncated"

ARGUMENT_SCHEMA: dict[str, Any] = {
    "type": "integer",
    "minimum": 1,
    "description": (
        "응답의 리스트 항목을 앞에서 N개만 남긴다(컨텍스트 절약). 잘리면 "
        "_truncated 에 원래 개수가 표시된다. 생략하면 서버 기본값(없으면 전부)."
    ),
}


def parse_max_rows(value: Any) -> int | None:
    """``None``/``""`` → ``None``; otherwise a positive int.

    Raises:
        ValueError: for zero, negatives or non-integers.
    """
    if value is None or (isinstance(value, str) and not value.strip()):
        return None
    if isinstance(value, bool):
        raise ValueError(f"max_rows 는 양의 정수여야 합니다: {value!r}")
    try:
        number = int(str(value).strip())
    except ValueError as exc:
        raise ValueError(f"max_rows 는 양의 정수여야 합니다: {value!r}") from exc
    if number < 1:
        raise ValueError(f"max_rows 는 양의 정수여야 합니다: {value!r}")
    return number


def max_rows_from_env(env: Mapping[str, str] | None = None) -> int | None:
    source = os.environ if env is None else env
    return parse_max_rows(source.get(ENV_VAR))


def limit_rows(result: Any, max_rows: int | None) -> Any:
    """Cut every top-level list in ``result`` to ``max_rows`` items.

    Non-dict results and ``max_rows=None`` pass through untouched. The input
    is not modified; a shallow copy is returned when anything is cut.
    """
    if max_rows is None or not isinstance(result, dict):
        return result
    cut = {
        key: len(value)
        for key, value in result.items()
        if isinstance(value, list) and len(value) > max_rows
    }
    if not cut:
        return result
    limited = dict(result)
    for key in cut:
        limited[key] = result[key][:max_rows]
    limited[MARKER] = {key: {"total": total, "returned": max_rows} for key, total in cut.items()}
    return limited


def with_max_rows_argument(schema: dict[str, Any]) -> dict[str, Any]:
    """Copy of an object input schema with the ``max_rows`` property added."""
    properties = dict(schema.get("properties", {}))
    properties.setdefault(ARGUMENT, ARGUMENT_SCHEMA)
    return {**schema, "properties": properties}
