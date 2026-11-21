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
            dt: 기간 (필수)
            strt_dt: 시작일자
            end_dt: 종료일자
            mrkt_tp: 장구분 (필수)
            netslmt_tp: 순매도수구분 (필수)
            stk_inds_tp: 종목업종구분 (필수)
            amt_qty_tp: 금액수량구분 (필수)
            stex_tp: 거래소구분 (필수)
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
            stk_cd: 종목코드 (필수)
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
            stk_cd: 종목코드 (필수)
        """
        ...
