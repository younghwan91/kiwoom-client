# 자동 생성 — 고치지 말 것. scripts/build_stubs.py 가 spec/catalog.json 으로 만든다.
# 런타임은 .py 그대로(**kwargs). 스텁은 요청 필드를 IDE·mypy 에 알려 줄 뿐이다.
from typing import Any, Generic

from kiwoom_client.base import ClientProtocol, ResponseT

class ShortSelling(Generic[ResponseT]):
    """Wraps all Short Selling (공매도) endpoints under /api/dostk/shsa.

    Args:
        client: An authenticated BaseClient (sync) or AsyncBaseClient.
    """

    RESOURCE_URL: str

    def __init__(self, client: ClientProtocol[ResponseT]) -> None: ...

    def short_selling_trend(
        self,
        cont_yn: str = "N",
        next_key: str = "",
        *,
        stk_cd: str = ...,
        tm_tp: str = ...,
        strt_dt: str = ...,
        end_dt: str = ...,
        **kwargs: Any,
    ) -> ResponseT:
        """공매도추이요청 (Short Selling Trend)

        api_id ``ka10014`` · 공매도추이요청 · ``POST /api/dostk/shsa``

        Args:
            stk_cd: 종목코드 (필수) — 거래소별 종목코드 (KRX:039490,NXT:039490_NX,SOR:039490_AL)
            tm_tp: 시간구분 — 0:시작일, 1:기간
            strt_dt: 시작일자 (필수) — YYYYMMDD
            end_dt: 종료일자 (필수) — YYYYMMDD
        """
        ...
