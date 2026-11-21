# 자동 생성 — 고치지 말 것. scripts/build_stubs.py 가 spec/catalog.json 으로 만든다.
# 런타임은 .py 그대로(**kwargs). 스텁은 요청 필드를 IDE·mypy 에 알려 줄 뿐이다.
from typing import Any, Generic

from kiwoom_client.base import ClientProtocol, ResponseT

class Chart(Generic[ResponseT]):
    """Wraps all Chart (차트) endpoints under /api/dostk/chart.

    Args:
        client: An authenticated BaseClient (sync) or AsyncBaseClient.
    """

    RESOURCE_URL: str

    def __init__(self, client: ClientProtocol[ResponseT]) -> None: ...

    def gold_spot_daily_chart(
        self,
        cont_yn: str = "N",
        next_key: str = "",
        *,
        stk_cd: str = ...,
        base_dt: str = ...,
        upd_stkpc_tp: str = ...,
        **kwargs: Any,
    ) -> ResponseT:
        """금현물일봉차트조회요청 (Gold Spot Daily Chart)

        api_id ``ka50081`` · 금현물일봉차트조회요청 · ``POST /api/dostk/chart``

        Args:
            stk_cd: 종목코드 (필수)
            base_dt: 기준일자 (필수)
            upd_stkpc_tp: 수정주가구분 (필수)
        """
        ...

    def gold_spot_intraday_minute_chart(
        self,
        cont_yn: str = "N",
        next_key: str = "",
        *,
        stk_cd: str = ...,
        tic_scope: str = ...,
        **kwargs: Any,
    ) -> ResponseT:
        """금현물당일분봉차트조회요청 (Gold Spot Intraday Minute Chart)

        api_id ``ka50092`` · 금현물당일분봉차트조회요청 · ``POST /api/dostk/chart``

        Args:
            stk_cd: 종목코드 (필수)
            tic_scope: 틱범위 (필수)
        """
        ...

    def gold_spot_intraday_tick_chart(
        self,
        cont_yn: str = "N",
        next_key: str = "",
        *,
        stk_cd: str = ...,
        tic_scope: str = ...,
        **kwargs: Any,
    ) -> ResponseT:
        """금현물당일틱차트조회요청 (Gold Spot Intraday Tick Chart)

        api_id ``ka50091`` · 금현물당일틱차트조회요청 · ``POST /api/dostk/chart``

        Args:
            stk_cd: 종목코드 (필수)
            tic_scope: 틱범위 (필수)
        """
        ...

    def gold_spot_minute_chart(
        self,
        cont_yn: str = "N",
        next_key: str = "",
        *,
        stk_cd: str = ...,
        tic_scope: str = ...,
        upd_stkpc_tp: str = ...,
        **kwargs: Any,
    ) -> ResponseT:
        """금현물분봉차트조회요청 (Gold Spot Minute Chart)

        api_id ``ka50080`` · 금현물분봉차트조회요청 · ``POST /api/dostk/chart``

        Args:
            stk_cd: 종목코드 (필수)
            tic_scope: 틱범위 (필수)
            upd_stkpc_tp: 수정주가구분
        """
        ...

    def gold_spot_monthly_chart(
        self,
        cont_yn: str = "N",
        next_key: str = "",
        *,
        stk_cd: str = ...,
        base_dt: str = ...,
        upd_stkpc_tp: str = ...,
        **kwargs: Any,
    ) -> ResponseT:
        """금현물월봉차트조회요청 (Gold Spot Monthly Chart)

        api_id ``ka50083`` · 금현물월봉차트조회요청 · ``POST /api/dostk/chart``

        Args:
            stk_cd: 종목코드 (필수)
            base_dt: 기준일자 (필수)
            upd_stkpc_tp: 수정주가구분 (필수)
        """
        ...

    def gold_spot_tick_chart(
        self,
        cont_yn: str = "N",
        next_key: str = "",
        *,
        stk_cd: str = ...,
        tic_scope: str = ...,
        upd_stkpc_tp: str = ...,
        **kwargs: Any,
    ) -> ResponseT:
        """금현물틱차트조회요청 (Gold Spot Tick Chart)

        api_id ``ka50079`` · 금현물틱차트조회요청 · ``POST /api/dostk/chart``

        Args:
            stk_cd: 종목코드 (필수)
            tic_scope: 틱범위 (필수)
            upd_stkpc_tp: 수정주가구분 (필수)
        """
        ...

    def gold_spot_weekly_chart(
        self,
        cont_yn: str = "N",
        next_key: str = "",
        *,
        stk_cd: str = ...,
        base_dt: str = ...,
        upd_stkpc_tp: str = ...,
        **kwargs: Any,
    ) -> ResponseT:
        """금현물주봉차트조회요청 (Gold Spot Weekly Chart)

        api_id ``ka50082`` · 금현물주봉차트조회요청 · ``POST /api/dostk/chart``

        Args:
            stk_cd: 종목코드 (필수)
            base_dt: 기준일자 (필수)
            upd_stkpc_tp: 수정주가구분 (필수)
        """
        ...

    def industry_daily_chart(
        self,
        cont_yn: str = "N",
        next_key: str = "",
        *,
        inds_cd: str = ...,
        base_dt: str = ...,
        **kwargs: Any,
    ) -> ResponseT:
        """업종일봉차트요청 (Industry Daily Chart)

        api_id ``ka20006`` · 업종일봉조회요청 · ``POST /api/dostk/chart``

        Args:
            inds_cd: 업종코드 (필수)
            base_dt: 기준일자 (필수)
        """
        ...

    def industry_minute_chart(
        self,
        cont_yn: str = "N",
        next_key: str = "",
        *,
        inds_cd: str = ...,
        tic_scope: str = ...,
        base_dt: str = ...,
        **kwargs: Any,
    ) -> ResponseT:
        """업종분봉차트요청 (Industry Minute Chart)

        api_id ``ka20005`` · 업종분봉조회요청 · ``POST /api/dostk/chart``

        Args:
            inds_cd: 업종코드 (필수)
            tic_scope: 틱범위 (필수)
            base_dt: 기준일자
        """
        ...

    def industry_monthly_chart(
        self,
        cont_yn: str = "N",
        next_key: str = "",
        *,
        inds_cd: str = ...,
        base_dt: str = ...,
        **kwargs: Any,
    ) -> ResponseT:
        """업종월봉차트요청 (Industry Monthly Chart)

        api_id ``ka20008`` · 업종월봉조회요청 · ``POST /api/dostk/chart``

        Args:
            inds_cd: 업종코드 (필수)
            base_dt: 기준일자 (필수)
        """
        ...

    def industry_tick_chart(
        self,
        cont_yn: str = "N",
        next_key: str = "",
        *,
        inds_cd: str = ...,
        tic_scope: str = ...,
        **kwargs: Any,
    ) -> ResponseT:
        """업종틱차트요청 (Industry Tick Chart)

        api_id ``ka20004`` · 업종틱차트조회요청 · ``POST /api/dostk/chart``

        Args:
            inds_cd: 업종코드 (필수)
            tic_scope: 틱범위 (필수)
        """
        ...

    def industry_weekly_chart(
        self,
        cont_yn: str = "N",
        next_key: str = "",
        *,
        inds_cd: str = ...,
        base_dt: str = ...,
        **kwargs: Any,
    ) -> ResponseT:
        """업종주봉차트요청 (Industry Weekly Chart)

        api_id ``ka20007`` · 업종주봉조회요청 · ``POST /api/dostk/chart``

        Args:
            inds_cd: 업종코드 (필수)
            base_dt: 기준일자 (필수)
        """
        ...

    def industry_yearly_chart(
        self,
        cont_yn: str = "N",
        next_key: str = "",
        *,
        inds_cd: str = ...,
        base_dt: str = ...,
        **kwargs: Any,
    ) -> ResponseT:
        """업종년봉차트요청 (Industry Yearly Chart)

        api_id ``ka20019`` · 업종년봉조회요청 · ``POST /api/dostk/chart``

        Args:
            inds_cd: 업종코드 (필수)
            base_dt: 기준일자 (필수)
        """
        ...

    def intraday_investor_chart(
        self,
        cont_yn: str = "N",
        next_key: str = "",
        *,
        mrkt_tp: str = ...,
        amt_qty_tp: str = ...,
        trde_tp: str = ...,
        stk_cd: str = ...,
        **kwargs: Any,
    ) -> ResponseT:
        """시간대별투자자매매차트요청 (Intraday Investor Trading Chart by Time Slot)

        api_id ``ka10064`` · 장중투자자별매매차트요청 · ``POST /api/dostk/chart``

        Args:
            mrkt_tp: 시장구분 (필수)
            amt_qty_tp: 금액수량구분 (필수)
            trde_tp: 매매구분 (필수)
            stk_cd: 종목코드 (필수)
        """
        ...

    def investor_institution_chart(
        self,
        cont_yn: str = "N",
        next_key: str = "",
        *,
        dt: str = ...,
        stk_cd: str = ...,
        amt_qty_tp: str = ...,
        trde_tp: str = ...,
        unit_tp: str = ...,
        **kwargs: Any,
    ) -> ResponseT:
        """종목별투자자기관별차트요청 (Investor/Institution Chart by Stock)

        api_id ``ka10060`` · 종목별투자자기관별차트요청 · ``POST /api/dostk/chart``

        Args:
            dt: 일자 (필수)
            stk_cd: 종목코드 (필수)
            amt_qty_tp: 금액수량구분 (필수)
            trde_tp: 매매구분 (필수)
            unit_tp: 단위구분 (필수)
        """
        ...

    def stock_daily_chart(
        self,
        cont_yn: str = "N",
        next_key: str = "",
        *,
        stk_cd: str = ...,
        base_dt: str = ...,
        upd_stkpc_tp: str = ...,
        **kwargs: Any,
    ) -> ResponseT:
        """주식일봉차트요청 (Stock Daily Chart)

        api_id ``ka10081`` · 주식일봉차트조회요청 · ``POST /api/dostk/chart``

        Args:
            stk_cd: 종목코드 (필수)
            base_dt: 기준일자 (필수)
            upd_stkpc_tp: 수정주가구분 (필수)
        """
        ...

    def stock_minute_chart(
        self,
        cont_yn: str = "N",
        next_key: str = "",
        *,
        stk_cd: str = ...,
        tic_scope: str = ...,
        upd_stkpc_tp: str = ...,
        base_dt: str = ...,
        **kwargs: Any,
    ) -> ResponseT:
        """주식분봉차트요청 (Stock Minute Chart)

        api_id ``ka10080`` · 주식분봉차트조회요청 · ``POST /api/dostk/chart``

        Args:
            stk_cd: 종목코드 (필수)
            tic_scope: 틱범위 (필수)
            upd_stkpc_tp: 수정주가구분 (필수)
            base_dt: 기준일자
        """
        ...

    def stock_monthly_chart(
        self,
        cont_yn: str = "N",
        next_key: str = "",
        *,
        stk_cd: str = ...,
        base_dt: str = ...,
        upd_stkpc_tp: str = ...,
        **kwargs: Any,
    ) -> ResponseT:
        """주식월봉차트요청 (Stock Monthly Chart)

        api_id ``ka10083`` · 주식월봉차트조회요청 · ``POST /api/dostk/chart``

        Args:
            stk_cd: 종목코드 (필수)
            base_dt: 기준일자 (필수)
            upd_stkpc_tp: 수정주가구분 (필수)
        """
        ...

    def stock_tick_chart(
        self,
        cont_yn: str = "N",
        next_key: str = "",
        *,
        stk_cd: str = ...,
        tic_scope: str = ...,
        upd_stkpc_tp: str = ...,
        **kwargs: Any,
    ) -> ResponseT:
        """주식틱차트요청 (Stock Tick Chart)

        api_id ``ka10079`` · 주식틱차트조회요청 · ``POST /api/dostk/chart``

        Args:
            stk_cd: 종목코드 (필수)
            tic_scope: 틱범위 (필수)
            upd_stkpc_tp: 수정주가구분 (필수)
        """
        ...

    def stock_weekly_chart(
        self,
        cont_yn: str = "N",
        next_key: str = "",
        *,
        stk_cd: str = ...,
        base_dt: str = ...,
        upd_stkpc_tp: str = ...,
        **kwargs: Any,
    ) -> ResponseT:
        """주식주봉차트요청 (Stock Weekly Chart)

        api_id ``ka10082`` · 주식주봉차트조회요청 · ``POST /api/dostk/chart``

        Args:
            stk_cd: 종목코드 (필수)
            base_dt: 기준일자 (필수)
            upd_stkpc_tp: 수정주가구분 (필수)
        """
        ...

    def stock_yearly_chart(
        self,
        cont_yn: str = "N",
        next_key: str = "",
        *,
        stk_cd: str = ...,
        base_dt: str = ...,
        upd_stkpc_tp: str = ...,
        **kwargs: Any,
    ) -> ResponseT:
        """주식년봉차트요청 (Stock Yearly Chart)

        api_id ``ka10094`` · 주식년봉차트조회요청 · ``POST /api/dostk/chart``

        Args:
            stk_cd: 종목코드 (필수)
            base_dt: 기준일자 (필수)
            upd_stkpc_tp: 수정주가구분 (필수)
        """
        ...
