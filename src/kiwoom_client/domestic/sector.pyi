# 자동 생성 — 고치지 말 것. scripts/build_stubs.py 가 spec/catalog.json 으로 만든다.
# 런타임은 .py 그대로(**kwargs). 스텁은 요청 필드를 IDE·mypy 에 알려 줄 뿐이다.
from typing import Any, Generic

from kiwoom_client.base import ClientProtocol, ResponseT

class Sector(Generic[ResponseT]):
    """Wraps all Sector (업종) endpoints under /api/dostk/sect.

    Args:
        client: An authenticated BaseClient (sync) or AsyncBaseClient.
    """

    RESOURCE_URL: str

    def __init__(self, client: ClientProtocol[ResponseT]) -> None: ...

    def all_industry_index(
        self,
        cont_yn: str = "N",
        next_key: str = "",
        *,
        inds_cd: str = ...,
        **kwargs: Any,
    ) -> ResponseT:
        """전업종지수요청 (All Industry Index)

        api_id ``ka20003`` · 전업종지수요청 · ``POST /api/dostk/sect``

        Args:
            inds_cd: 업종코드 (필수)
        """
        ...

    def industry_current_price(
        self,
        cont_yn: str = "N",
        next_key: str = "",
        *,
        mrkt_tp: str = ...,
        inds_cd: str = ...,
        **kwargs: Any,
    ) -> ResponseT:
        """업종현재가요청 (Industry Current Price)

        api_id ``ka20001`` · 업종현재가요청 · ``POST /api/dostk/sect``

        Args:
            mrkt_tp: 시장구분 (필수)
            inds_cd: 업종코드 (필수)
        """
        ...

    def industry_daily_price(
        self,
        cont_yn: str = "N",
        next_key: str = "",
        *,
        mrkt_tp: str = ...,
        inds_cd: str = ...,
        **kwargs: Any,
    ) -> ResponseT:
        """업종현재가일별요청 (Industry Daily Price)

        api_id ``ka20009`` · 업종현재가일별요청 · ``POST /api/dostk/sect``

        Args:
            mrkt_tp: 시장구분 (필수)
            inds_cd: 업종코드 (필수)
        """
        ...

    def industry_investor_net_buy(
        self,
        cont_yn: str = "N",
        next_key: str = "",
        *,
        mrkt_tp: str = ...,
        amt_qty_tp: str = ...,
        base_dt: str = ...,
        stex_tp: str = ...,
        **kwargs: Any,
    ) -> ResponseT:
        """업종별투자자순매수요청 (Industry Investor Net Buy)

        api_id ``ka10051`` · 업종별투자자순매수요청 · ``POST /api/dostk/sect``

        Args:
            mrkt_tp: 시장구분 (필수)
            amt_qty_tp: 금액수량구분 (필수)
            base_dt: 기준일자
            stex_tp: 거래소구분 (필수)
        """
        ...

    def industry_program_trading(
        self,
        cont_yn: str = "N",
        next_key: str = "",
        *,
        stk_cd: str = ...,
        **kwargs: Any,
    ) -> ResponseT:
        """업종프로그램매매요청 (Industry Program Trading)

        api_id ``ka10010`` · 업종프로그램요청 · ``POST /api/dostk/sect``

        Args:
            stk_cd: 종목코드 (필수)
        """
        ...

    def industry_stock_price(
        self,
        cont_yn: str = "N",
        next_key: str = "",
        *,
        mrkt_tp: str = ...,
        inds_cd: str = ...,
        stex_tp: str = ...,
        **kwargs: Any,
    ) -> ResponseT:
        """업종별주가요청 (Industry Stock Price)

        api_id ``ka20002`` · 업종별주가요청 · ``POST /api/dostk/sect``

        Args:
            mrkt_tp: 시장구분 (필수)
            inds_cd: 업종코드 (필수)
            stex_tp: 거래소구분 (필수)
        """
        ...
