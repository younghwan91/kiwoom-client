# 자동 생성 — 고치지 말 것. scripts/build_stubs.py 가 spec/catalog.json 으로 만든다.
# 런타임은 .py 그대로(**kwargs). 스텁은 요청 필드를 IDE·mypy 에 알려 줄 뿐이다.
from typing import Any, Generic

from kiwoom_client.base import ClientProtocol, ResponseT

class ForeignInstitution(Generic[ResponseT]):
    """Wraps all Foreign Institution (외국인/기관) endpoints under /api/dostk/frgnistt.

    Args:
        client: An authenticated BaseClient (sync) or AsyncBaseClient.
    """

    RESOURCE_URL: str

    def __init__(self, client: ClientProtocol[ResponseT]) -> None: ...

    def consecutive_trading_status(
        self,
        cont_yn: str = "N",
        next_key: str = "",
        *,
        dt: str = ...,
        strt_dt: str = ...,
        end_dt: str = ...,
        mrkt_tp: str = ...,
        netslmt_tp: str = ...,
        stk_inds_tp: str = ...,
        amt_qty_tp: str = ...,
        stex_tp: str = ...,
        **kwargs: Any,
    ) -> ResponseT:
        """기관외국인연속매매현황요청 (Institution and Foreign Consecutive Trading Status)

        api_id ``ka10131`` · 기관외국인연속매매현황요청 · ``POST /api/dostk/frgnistt``

        Args:
            dt: 기간 (필수) — 1:최근일, 3:3일, 5:5일, 10:10일, 20:20일, 120:120일,
                0:시작일자/종료일자로 조회
            strt_dt: 시작일자 — YYYYMMDD
            end_dt: 종료일자 — YYYYMMDD
            mrkt_tp: 장구분 (필수) — 001:코스피, 101:코스닥
            netslmt_tp: 순매도수구분 (필수) — 2:순매수(고정값)
            stk_inds_tp: 종목업종구분 (필수) — 0:종목(주식),1:업종
            amt_qty_tp: 금액수량구분 (필수) — 0:금액, 1:수량
            stex_tp: 거래소구분 (필수) — 1:KRX, 2:NXT, 3:통합
        """
        ...

    def foreign_trading_trend(
        self,
        cont_yn: str = "N",
        next_key: str = "",
        *,
        stk_cd: str = ...,
        **kwargs: Any,
    ) -> ResponseT:
        """주식외국인종목별매매동향 (Foreign Trading Trend by Stock)

        api_id ``ka10008`` · 주식외국인종목별매매동향 · ``POST /api/dostk/frgnistt``

        Args:
            stk_cd: 종목코드 (필수) — 거래소별 종목코드 (KRX:039490,NXT:039490_NX,SOR:039490_AL)
        """
        ...

    def gold_spot_investor_status(
        self,
        cont_yn: str = "N",
        next_key: str = "",
        **kwargs: Any,
    ) -> ResponseT:
        """금현물투자자현황 (Gold Spot Investor Status)

        api_id ``ka52301`` · 금현물투자자현황 · ``POST /api/dostk/frgnistt``
        """
        ...

    def institutional_stock(
        self,
        cont_yn: str = "N",
        next_key: str = "",
        *,
        stk_cd: str = ...,
        **kwargs: Any,
    ) -> ResponseT:
        """주식기관요청 (Institutional Stock)

        api_id ``ka10009`` · 주식기관요청 · ``POST /api/dostk/frgnistt``
        출처: repo — 현재 공식 명세(SOURCE_COMMIT)에 없다. 요청 필드는
        tests/integration_api_smoke.py 표 기준이고 응답 필드는 미확인.

        Args:
            stk_cd: 종목코드 (필수) — 거래소별 종목코드 (KRX:039490,NXT:039490_NX,SOR:039490_AL)
        """
        ...
