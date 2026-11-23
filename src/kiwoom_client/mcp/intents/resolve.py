"""Turn a stock argument — a name or a code — into a stock code.

Intent tools take ``stock`` as either ``"005930"`` or ``"삼성전자"``. A code
is used as-is (no request). A name is looked up in the cached ka10099
listing (:meth:`AsyncKiwoomAPI.find_stock`): an exact name wins, a single
partial match is accepted, and several matches are an error listing the
candidates so the agent can ask the person which one they meant.
"""

from __future__ import annotations

import re
from collections.abc import Sequence
from dataclasses import dataclass
from typing import Any

from kiwoom_client.mcp.intents.normalize import stock_code

#: ka10099 mrkt_tp values searched for names: 코스피, 코스닥, ETF.
NAME_MARKETS: tuple[str, ...] = ("0", "10", "8")

#: How many candidates an ambiguity error lists.
MAX_CANDIDATES = 8

#: A KRX short code: 6 characters, digits and (for newer listings) capitals.
_CODE = re.compile(r"^[0-9][0-9A-Z]{5}$")


class StockNotFound(ValueError):
    """No listed stock matches the argument."""


class AmbiguousStock(ValueError):
    """Several stocks match a name; ``candidates`` lists them."""

    def __init__(self, query: str, candidates: list[dict[str, Any]]) -> None:
        self.query = query
        self.candidates = candidates
        listed = ", ".join(f"{c['name']}({c['code']})" for c in candidates)
        super().__init__(
            f"'{query}' 에 맞는 종목이 여러 개입니다 — 종목코드나 정확한 이름으로 다시 "
            f"호출하세요. 후보: {listed}"
        )


@dataclass(frozen=True)
class Stock:
    code: str
    name: str | None = None

    def as_dict(self) -> dict[str, Any]:
        return {"code": self.code, "name": self.name}


def _fold(value: Any) -> str:
    return "".join(str(value).split()).casefold()


def looks_like_code(value: str) -> bool:
    return bool(_CODE.match(value.strip().upper()))


async def resolve_stock(api: Any, stock: Any, *, markets: Sequence[str] = NAME_MARKETS) -> Stock:
    """Resolve one ``stock`` argument.

    Raises:
        ValueError: blank argument.
        StockNotFound: nothing matches the name.
        AmbiguousStock: several stocks match and none exactly.
    """
    query = str(stock if stock is not None else "").strip()
    if not query:
        raise ValueError("stock(종목명 또는 종목코드)이 필요합니다")
    code = stock_code(query.upper())
    if code is not None and looks_like_code(code):
        return Stock(code=code)

    hits = await api.find_stock(query, markets=tuple(markets), limit=None)
    exact = [hit for hit in hits if _fold(hit.get("name", "")) == _fold(query)]
    if len(exact) == 1:
        return Stock(code=str(exact[0]["code"]), name=exact[0].get("name"))
    chosen = exact or hits
    if len(chosen) == 1:
        return Stock(code=str(chosen[0]["code"]), name=chosen[0].get("name"))
    if not chosen:
        raise StockNotFound(
            f"'{query}' 에 맞는 종목을 찾지 못했습니다 — stock_search 로 확인하세요"
        )
    candidates = [
        {"code": str(hit.get("code")), "name": hit.get("name"), "market": hit.get("marketName")}
        for hit in chosen[:MAX_CANDIDATES]
    ]
    raise AmbiguousStock(query, candidates)


STOCK_DESCRIPTION = "종목명 또는 종목코드 (예: '삼성전자', '005930')"


def stock_schema(description: str = STOCK_DESCRIPTION) -> dict[str, Any]:
    return {"type": "string", "description": description}
