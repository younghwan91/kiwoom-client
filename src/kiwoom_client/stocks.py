"""Stock name <-> code lookup on top of 종목정보 리스트 (ka10099).

``api.find_stock("삼성전자")`` fetches the KOSPI and KOSDAQ listings once
(``api.stock_info.stock_info_list``, paginated with ``request_all``), caches
them on the client, and searches them locally. Each hit is the raw ka10099
record — ``code``, ``name``, ``marketName``, ``state``, ``nxtEnable``, ...::

    >>> [s["code"] for s in api.find_stock("삼성전자")][:1]
    ['005930']
    >>> api.stock_code("SK하이닉스")
    '000660'

The cache lives as long as the client; pass ``refresh=True`` to refetch (the
listing changes when stocks list or delist), or ``cache_ttl`` seconds to the
lookup methods to refetch automatically.
"""

from __future__ import annotations

import time
from collections.abc import Iterable, Mapping, Sequence
from typing import Any

from kiwoom_client.codes import StockListMarket

__all__ = ["DEFAULT_MARKETS", "StockCache", "pick_stock_code", "search_stocks"]

#: Markets fetched by default: 코스피, 코스닥.
DEFAULT_MARKETS: tuple[StockListMarket, ...] = (StockListMarket.KOSPI, StockListMarket.KOSDAQ)

STOCK_LIST_URL = "/api/dostk/stkinfo"
STOCK_LIST_API_ID = "ka10099"
STOCK_LIST_KEY = "list"


def _fold(text: Any) -> str:
    """Case- and whitespace-insensitive form used for matching."""
    return "".join(str(text).split()).casefold()


def search_stocks(
    records: Iterable[Mapping[str, Any]],
    query: str,
    limit: int | None = 10,
) -> list[dict[str, Any]]:
    """Rank ka10099 records against a name or code query.

    Order: exact code, exact name, name prefix, code prefix, name substring.
    Ties go to the shorter name, then the code. Matching ignores case and
    spaces (``"sk 하이닉스"`` finds ``"SK하이닉스"``).

    Args:
        records: ka10099 ``list`` records (dicts with ``code`` and ``name``).
        query: Part of a name, or a (partial) 6-digit code.
        limit: Maximum hits; None for all.

    Returns:
        Matching records, best first. Empty if nothing matches.
    """
    needle = _fold(query)
    if not needle:
        return []
    ranked: list[tuple[int, int, str, dict[str, Any]]] = []
    for record in records:
        code = str(record.get("code", "")).strip()
        name = _fold(record.get("name", ""))
        folded_code = code.casefold()
        if folded_code == needle:
            rank = 0
        elif name == needle:
            rank = 1
        elif name.startswith(needle):
            rank = 2
        elif folded_code.startswith(needle):
            rank = 3
        elif needle in name:
            rank = 4
        else:
            continue
        ranked.append((rank, len(name), code, dict(record)))
    ranked.sort(key=lambda item: item[:3])
    hits = [record for *_, record in ranked]
    return hits if limit is None else hits[:limit]


def pick_stock_code(records: Iterable[Mapping[str, Any]], name: str) -> str:
    """The code of the one stock whose name (or code) is exactly ``name``.

    Raises:
        LookupError: If no stock, or more than one, matches exactly. The
            message lists close candidates.
    """
    hits = search_stocks(records, name, limit=None)
    exact = [hit for hit in hits if _fold(hit.get("name", "")) == _fold(name)]
    exact = exact or [hit for hit in hits if _fold(hit.get("code", "")) == _fold(name)]
    if len(exact) == 1:
        return str(exact[0]["code"])
    if not exact:
        near = ", ".join(f"{h.get('name')}({h.get('code')})" for h in hits[:5])
        raise LookupError(
            f"'{name}' 와 이름이 정확히 같은 종목이 없습니다."
            + (f" 비슷한 종목: {near}" if near else "")
        )
    both = ", ".join(f"{h.get('name')}({h.get('code')}, {h.get('marketName')})" for h in exact)
    raise LookupError(f"'{name}' 이 여러 종목과 일치합니다: {both}")


class StockCache:
    """Per-client cache of ka10099 listings, keyed by market code."""

    def __init__(self) -> None:
        self._records: dict[str, list[dict[str, Any]]] = {}
        self._fetched_at: dict[str, float] = {}

    def stale(
        self,
        markets: Sequence[StockListMarket | str],
        refresh: bool = False,
        cache_ttl: float | None = None,
    ) -> list[str]:
        """Market codes that need fetching."""
        now = time.monotonic()
        out = []
        for market in markets:
            key = str(market)
            fetched = self._fetched_at.get(key)
            if (
                refresh
                or fetched is None
                or (cache_ttl is not None and now - fetched >= cache_ttl)
            ):
                out.append(key)
        return out

    def store(self, market: str, records: Iterable[Mapping[str, Any]]) -> None:
        self._records[market] = [dict(r) for r in records if isinstance(r, Mapping)]
        self._fetched_at[market] = time.monotonic()

    def records(self, markets: Sequence[StockListMarket | str]) -> list[dict[str, Any]]:
        """Cached records for ``markets``, de-duplicated by code (first wins)."""
        seen: set[str] = set()
        out = []
        for market in markets:
            for record in self._records.get(str(market), []):
                code = str(record.get("code", ""))
                if code in seen:
                    continue
                seen.add(code)
                out.append(record)
        return out

    def clear(self) -> None:
        self._records.clear()
        self._fetched_at.clear()
