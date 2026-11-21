# 자동 생성 — 고치지 말 것. scripts/build_stubs.py 가 spec/catalog.json 으로 만든다.
# 런타임은 .py 그대로(**kwargs). 스텁은 요청 필드를 IDE·mypy 에 알려 줄 뿐이다.
from typing import Any, Generic

from kiwoom_client.base import ClientProtocol, ResponseT

class SLB(Generic[ResponseT]):
    """Wraps all SLB (대차거래) endpoints under /api/dostk/slb.

    Args:
        client: An authenticated BaseClient (sync) or AsyncBaseClient.
    """

    RESOURCE_URL: str

    def __init__(self, client: ClientProtocol[ResponseT]) -> None: ...

    def lending_details(
        self,
        cont_yn: str = "N",
        next_key: str = "",
        *,
        dt: str = ...,
        mrkt_tp: str = ...,
        **kwargs: Any,
    ) -> ResponseT:
        """대차거래내역요청 (Lending Details)

        api_id ``ka90012`` · 대차거래내역요청 · ``POST /api/dostk/slb``

        Args:
            dt: 일자 (필수) — YYYYMMDD
            mrkt_tp: 시장구분 (필수) — 001:코스피, 101:코스닥
        """
        ...

    def lending_trend(
        self,
        cont_yn: str = "N",
        next_key: str = "",
        *,
        strt_dt: str = ...,
        end_dt: str = ...,
        all_tp: str = ...,
        **kwargs: Any,
    ) -> ResponseT:
        """대차거래추이요청 (Lending Trend)

        api_id ``ka10068`` · 대차거래추이요청 · ``POST /api/dostk/slb``

        Args:
            strt_dt: 시작일자 — YYYYMMDD
            end_dt: 종료일자 — YYYYMMDD
            all_tp: 전체구분 (필수) — 1: 전체표시
        """
        ...

    def lending_trend_by_stock(
        self,
        cont_yn: str = "N",
        next_key: str = "",
        *,
        strt_dt: str = ...,
        end_dt: str = ...,
        all_tp: str = ...,
        stk_cd: str = ...,
        **kwargs: Any,
    ) -> ResponseT:
        """대차거래추이요청종목별 (Lending Trend by Stock)

        api_id ``ka20068`` · 대차거래추이요청(종목별) · ``POST /api/dostk/slb``

        Args:
            strt_dt: 시작일자 — YYYYMMDD
            end_dt: 종료일자 — YYYYMMDD
            all_tp: 전체구분 — 0:종목코드 입력종목만 표시
            stk_cd: 종목코드 (필수)
        """
        ...

    def top10_lending(
        self,
        cont_yn: str = "N",
        next_key: str = "",
        *,
        strt_dt: str = ...,
        end_dt: str = ...,
        mrkt_tp: str = ...,
        **kwargs: Any,
    ) -> ResponseT:
        """대차거래상위10종목요청 (Top 10 Lending Stocks)

        api_id ``ka10069`` · 대차거래상위10종목요청 · ``POST /api/dostk/slb``

        Args:
            strt_dt: 시작일자 (필수) — YYYYMMDD (연도4자리, 월 2자리, 일 2자리 형식)
            end_dt: 종료일자 — YYYYMMDD (연도4자리, 월 2자리, 일 2자리 형식)
            mrkt_tp: 시장구분 (필수) — 001:코스피, 101:코스닥
        """
        ...
