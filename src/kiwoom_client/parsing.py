"""Helpers for turning Kiwoom's raw string responses into usable Python values.

Kiwoom returns every field as a string, signed and comma-grouped: a price
arrives as ``"+70000"``, a change rate as ``"-1.23"``, a volume as
``"1,234,567"``. Left alone, every caller writes the same parsing code.

Two things must survive parsing untouched: identifiers whose leading zero
carries meaning (``"005930"``) and date-like fields that only look numeric
(``"20260815"``). The first is caught by value shape, the second by field name.
"""

from __future__ import annotations

import re
from collections.abc import Iterable, Mapping, Sequence
from typing import Any

__all__ = ["extract_records", "normalize", "to_dataframe", "to_number", "to_ohlcv"]

_NUMERIC = re.compile(r"^[+-]?\d+(\.\d+)?$")

# Field-name suffixes whose values are identifiers or dates, not quantities.
# Matched against the whole name too, so a bare "dt" or "cd" is covered.
_TEXTUAL_SUFFIXES = (
    "_dt",
    "_date",
    "_ymd",
    "_cd",
    "_code",
    "_no",
    "_id",
    "_nm",
    "_name",
    "_tm",
    "_time",
)
_TEXTUAL_NAMES = frozenset(
    {"dt", "date", "ymd", "cd", "code", "no", "id", "nm", "name", "tm", "time"}
)


def is_textual_key(key: str) -> bool:
    """True if a field name marks its value as an identifier or date.

    Such values are kept as strings even when they parse as numbers — turning
    ``base_dt="20260815"`` into an int loses nothing but gains confusion, and
    an account number is not an amount.
    """
    lowered = key.lower()
    return lowered in _TEXTUAL_NAMES or lowered.endswith(_TEXTUAL_SUFFIXES)


def to_number(value: Any) -> Any:
    """Convert a Kiwoom numeric string to int/float, leaving anything else.

    Handles a leading ``+``/``-``, comma grouping and surrounding whitespace.
    Blank strings become None. Strings with a meaningful leading zero
    (``"005930"``) and any non-numeric text are returned unchanged.

    Args:
        value: A raw field value of any type.

    Returns:
        int, float, None for blanks, or the original value untouched.
    """
    if not isinstance(value, str):
        return value

    stripped = value.strip()
    if not stripped:
        return None

    candidate = stripped.replace(",", "")
    if not _NUMERIC.match(candidate):
        return value

    digits = candidate.lstrip("+-")
    # "005930" is a code, not five thousand nine hundred thirty. "0" and
    # "0.5" are genuine numbers, so only a zero followed by another digit
    # marks a padded identifier.
    if len(digits) > 1 and digits[0] == "0" and digits[1] != ".":
        return value

    if "." in candidate:
        return float(candidate)
    return int(candidate)


def normalize(
    data: Any,
    exclude: Iterable[str] | None = None,
) -> Any:
    """Recursively convert numeric strings in an API response.

    Args:
        data: A response dict, a list of records, or a single value.
        exclude: Field names to leave untouched, on top of the built-in
            identifier/date detection.

    Returns:
        A new structure of the same shape; the input is not mutated.
    """
    skip = frozenset(exclude or ())

    def _walk(node: Any, key: str | None = None) -> Any:
        if isinstance(node, Mapping):
            return {k: _walk(v, k) for k, v in node.items()}
        if isinstance(node, (list, tuple)):
            return [_walk(item, key) for item in node]
        if key is not None and (key in skip or is_textual_key(key)):
            return node
        return to_number(node)

    return _walk(data)


def extract_records(
    response: Any,
    key: str | None = None,
) -> tuple[str | None, list[dict[str, Any]]]:
    """Locate the list of records inside a Kiwoom response.

    Kiwoom names the payload key differently per endpoint (``stk_infr``,
    ``acnt_evlt_remn_indv_tot``, …), so callers otherwise hunt for it by hand.

    Args:
        response: A response dict, or the list returned by ``request_all()``.
        key: Payload key to use. Auto-detected when omitted — the longest
            list of dicts in the response wins.

    Returns:
        ``(key, records)``. The key is None when the response was already a
        list or held no record list.

    Raises:
        KeyError: If an explicit key is absent from the response.
    """
    if isinstance(response, list):
        return None, [item for item in response if isinstance(item, dict)]

    if not isinstance(response, Mapping):
        return None, []

    if key is not None:
        if key not in response:
            raise KeyError(
                f"응답에 '{key}' 키가 없습니다. 사용 가능한 키: {sorted(response)}"
            )
        value = response[key]
        return key, list(value) if isinstance(value, Sequence) else []

    best_key: str | None = None
    best: list[dict[str, Any]] = []
    for candidate, value in response.items():
        if not isinstance(value, list) or not value:
            continue
        if not all(isinstance(item, dict) for item in value):
            continue  # a list of scalars is not a record set
        if len(value) > len(best):
            best_key, best = candidate, value

    return best_key, list(best)


def to_dataframe(
    response: Any,
    key: str | None = None,
    numeric: bool = True,
) -> Any:
    """Turn a Kiwoom response into a pandas DataFrame.

    Args:
        response: A response dict, or the list returned by ``request_all()``.
        key: Payload key to use. Auto-detected when omitted.
        numeric: Convert numeric strings to int/float. Identifier and date
            fields stay strings regardless.

    Returns:
        A pandas DataFrame — empty if the response held no records.

    Raises:
        ImportError: If pandas is not installed.
        KeyError: If an explicit key is absent from the response.
    """
    pd = _import_pandas()
    _, records = extract_records(response, key)
    if numeric:
        records = [normalize(record) for record in records]
    return pd.DataFrame(records)


# Field names across Kiwoom's chart TRs (stock ka10079-ka10094, sector
# ka20004-ka20019, gold spot ka50079-ka50092), per the official spec.
_TIME_FIELDS = ("cntr_tm", "dt")
_OHLCV_FIELDS: dict[str, tuple[str, ...]] = {
    "open": ("open_pric",),
    "high": ("high_pric",),
    "low": ("low_pric",),
    "close": ("cur_prc", "cntr_pric"),
    "volume": ("trde_qty", "acc_trde_qty"),
}
_TIME_FORMATS = {8: "%Y%m%d", 12: "%Y%m%d%H%M", 14: "%Y%m%d%H%M%S"}


def _unsigned_number(value: Any) -> Any:
    """Parse a chart price/volume, dropping the direction sign.

    Minute/tick charts send ``"-70000"`` for a price that is *down*, not
    negative; an OHLC price or a volume is never below zero. Zero-padded
    values (``"000070000"``) are numbers here, unlike in :func:`to_number`.
    """
    if not isinstance(value, str):
        return value
    text = value.strip().replace(",", "").lstrip("+-")
    if not text:
        return None
    try:
        return int(text)
    except ValueError:
        try:
            return float(text)
        except ValueError:
            return None


def _pick(record: Mapping[str, Any], names: tuple[str, ...]) -> str | None:
    for name in names:
        if name in record:
            return name
    return None


def to_ohlcv(
    response: Any,
    key: str | None = None,
    keep: Iterable[str] = (),
) -> Any:
    """Turn a chart response into an OHLCV DataFrame indexed by time.

    Works for the stock, sector and gold-spot chart TRs (tick, minute, daily,
    weekly, monthly, yearly), single page or the list from ``request_all()``.

    The result has columns ``open``, ``high``, ``low``, ``close``, ``volume``
    and a ``DatetimeIndex`` named ``date`` (daily and longer) or ``datetime``
    (intraday), sorted oldest first — Kiwoom sends newest first.

    Notes:
        - Prices lose their direction sign (``"-70000"`` -> ``70000``).
        - Sector (업종) index values come as Kiwoom sends them, i.e. with the
          decimal point removed (``"265012"`` for 2650.12).
        - :func:`to_dataframe` is unchanged and still returns every raw field.

    Args:
        response: A chart response dict, or the list from ``request_all()``.
        key: Payload key (e.g. ``"stk_dt_pole_chart_qry"``). Auto-detected
            when omitted.
        keep: Extra fields to carry over as columns, numeric-converted with
            :func:`to_number` (e.g. ``["trde_prica"]`` for 거래대금 — its unit
            differs per TR: 백만원 for daily, 원 for weekly/monthly).

    Returns:
        A pandas DataFrame; empty (with the OHLCV columns) for no records.

    Raises:
        ImportError: If pandas is not installed.
        KeyError: If the records have no time or price fields, i.e. the
            response is not a chart.
    """
    pd = _import_pandas()
    _, records = extract_records(response, key)
    columns = list(_OHLCV_FIELDS)
    extra = list(keep)
    if not records:
        empty = pd.DataFrame(columns=columns + extra)
        empty.index = pd.DatetimeIndex([], name="datetime")
        return empty

    first = records[0]
    time_field = _pick(first, _TIME_FIELDS)
    if time_field is None:
        raise KeyError(
            f"차트 응답이 아닙니다: 시간 필드({', '.join(_TIME_FIELDS)})가 없습니다. "
            f"필드: {sorted(first)}"
        )
    source = {}
    for column, names in _OHLCV_FIELDS.items():
        name = _pick(first, names)
        if name is None:
            raise KeyError(
                f"차트 응답이 아닙니다: {column} 필드({', '.join(names)})가 없습니다. "
                f"필드: {sorted(first)}"
            )
        source[column] = name

    stamps = [str(record.get(time_field, "")).strip() for record in records]
    widths = {len(stamp) for stamp in stamps}
    fmt = _TIME_FORMATS.get(widths.pop()) if len(widths) == 1 else None
    if fmt is None:
        raise ValueError(f"{time_field} 형식을 알 수 없습니다: {stamps[:3]}")

    data = {
        column: [_unsigned_number(record.get(name)) for record in records]
        for column, name in source.items()
    }
    for name in extra:
        data[name] = [to_number(record.get(name)) for record in records]

    index = pd.DatetimeIndex(
        pd.to_datetime(stamps, format=fmt), name="date" if fmt == "%Y%m%d" else "datetime"
    )
    frame = pd.DataFrame(data, index=index, columns=columns + extra)
    return frame.sort_index(kind="stable")


def _import_pandas() -> Any:
    try:
        import pandas
    except ImportError as exc:  # pragma: no cover - exercised via sys.modules
        raise ImportError(
            "to_dataframe() 에는 pandas 가 필요합니다. "
            "설치: pip install 'kiwoom-client[pandas]'"
        ) from exc
    if pandas is None:  # sys.modules sentinel used by the tests
        raise ImportError(
            "to_dataframe() 에는 pandas 가 필요합니다. "
            "설치: pip install 'kiwoom-client[pandas]'"
        )
    return pandas
