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
            stk_cd: 종목코드 (필수) — M04020000 금 99.99_1kg, M04020100 미니금 99.99_100g
            base_dt: 기준일자 (필수) — YYYYMMDD
            upd_stkpc_tp: 수정주가구분 (필수) — 0 or 1
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
            stk_cd: 종목코드 (필수) — M04020000 금 99.99_1kg, M04020100 미니금 99.99_100g
            tic_scope: 틱범위 (필수) — 1:1분, 3:3분, 5:5분, 10:10분, 15:15분, 30:30분, 45:45분,
                60:60분
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
            stk_cd: 종목코드 (필수) — M04020000 금 99.99_1kg, M04020100 미니금 99.99_100g
            tic_scope: 틱범위 (필수) — 1:1틱, 3:3틱, 5:5틱, 10:10틱, 30:30틱
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
            stk_cd: 종목코드 (필수) — M04020000 금 99.99_1kg, M04020100 미니금 99.99_100g
            tic_scope: 틱범위 (필수) — 1:1분, 3:3분, 5:5분, 10:10분, 15:15분, 30:30분, 45:45분,
                60:60분
            upd_stkpc_tp: 수정주가구분 — 0 or 1
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
            stk_cd: 종목코드 (필수) — M04020000 금 99.99_1kg, M04020100 미니금 99.99_100g
            base_dt: 기준일자 (필수) — YYYYMMDD
            upd_stkpc_tp: 수정주가구분 (필수) — 0 or 1
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
            stk_cd: 종목코드 (필수) — M04020000 금 99.99_1kg, M04020100 미니금 99.99_100g
            tic_scope: 틱범위 (필수) — 1:1틱, 3:3틱, 5:5틱, 10:10틱, 30:30틱
            upd_stkpc_tp: 수정주가구분 (필수) — 0 or 1
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
            stk_cd: 종목코드 (필수) — M04020000 금 99.99_1kg, M04020100 미니금 99.99_100g
            base_dt: 기준일자 (필수) — YYYYMMDD
            upd_stkpc_tp: 수정주가구분 (필수) — 0 or 1
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
            inds_cd: 업종코드 (필수) — 001:종합(KOSPI), 002:대형주, 003:중형주, 004:소형주
                101:종합(KOSDAQ), 201:KOSPI200, 302:KOSTAR, 701: KRX100 나머지 ※ 업종코드 참고
            base_dt: 기준일자 (필수) — YYYYMMDD
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
            inds_cd: 업종코드 (필수) — 001:종합(KOSPI), 002:대형주, 003:중형주, 004:소형주
                101:종합(KOSDAQ), 201:KOSPI200, 302:KOSTAR, 701: KRX100 나머지 ※ 업종코드 참고
            tic_scope: 틱범위 (필수) — 1:1분, 3:3분, 5:5분, 10:10분, 15:15분, 30:30분, 45:45분,
                60:60분
            base_dt: 기준일자 — YYYYMMDD
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
            inds_cd: 업종코드 (필수) — 001:종합(KOSPI), 002:대형주, 003:중형주, 004:소형주
                101:종합(KOSDAQ), 201:KOSPI200, 302:KOSTAR, 701: KRX100 나머지 ※ 업종코드 참고
            base_dt: 기준일자 (필수) — YYYYMMDD
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
            inds_cd: 업종코드 (필수) — 001:종합(KOSPI), 002:대형주, 003:중형주, 004:소형주
                101:종합(KOSDAQ), 201:KOSPI200, 302:KOSTAR, 701: KRX100 나머지 ※ 업종코드 참고
            tic_scope: 틱범위 (필수) — 1:1틱, 3:3틱, 5:5틱, 10:10틱, 30:30틱
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
            inds_cd: 업종코드 (필수) — 001:종합(KOSPI), 002:대형주, 003:중형주, 004:소형주
                101:종합(KOSDAQ), 201:KOSPI200, 302:KOSTAR, 701: KRX100 나머지 ※ 업종코드 참고
            base_dt: 기준일자 (필수) — YYYYMMDD
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
            inds_cd: 업종코드 (필수) — 001:종합(KOSPI), 002:대형주, 003:중형주, 004:소형주
                101:종합(KOSDAQ), 201:KOSPI200, 302:KOSTAR, 701: KRX100 나머지 ※ 업종코드 참고
            base_dt: 기준일자 (필수) — YYYYMMDD
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
            mrkt_tp: 시장구분 (필수) — 000:전체, 001:코스피, 101:코스닥
            amt_qty_tp: 금액수량구분 (필수) — 1:금액, 2:수량
            trde_tp: 매매구분 (필수) — 0:순매수, 1:매수, 2:매도
            stk_cd: 종목코드 (필수) — 거래소별 종목코드 (KRX:039490,NXT:039490_NX,SOR:039490_AL)
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
            dt: 일자 (필수) — YYYYMMDD
            stk_cd: 종목코드 (필수) — 거래소별 종목코드 (KRX:039490,NXT:039490_NX,SOR:039490_AL)
            amt_qty_tp: 금액수량구분 (필수) — 1:금액, 2:수량
            trde_tp: 매매구분 (필수) — 0:순매수, 1:매수, 2:매도
            unit_tp: 단위구분 (필수) — 1000:천주, 1:단주
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
            stk_cd: 종목코드 (필수) — 거래소별 종목코드 (KRX:039490,NXT:039490_NX,SOR:039490_AL)
            base_dt: 기준일자 (필수) — YYYYMMDD
            upd_stkpc_tp: 수정주가구분 (필수) — 0 or 1 / 수정주가 적용을 원하시는 경우, 권리발생일
                이후 일자를 base_dt에 넣어 조회 또는 연속조회해주시기 바랍니다. 예를 들어 삼성전자
                2018년 05월 04일 (액면분할 권리발생일)을 base_dt에 넣고 수정주가적용(1)로 조회하면
                2018년 05월 04일 이전 데이터는 수정주가 적용된 3만원대 가격이 나옵니다. 연속조회도
                동일합니다. 권리 발생일 이전인 2018년 05월 03일 이전 일자로 base_dt 조회 시 수정주가
                적용되지 않아 200만원 이상 가격대가 나옵니다. 수정주가 적용을 원하는 과거 차트
                데이터 조회를 위해서는 해당 권리발생일 이후로 base_dt를 세팅하고, 수정주가 적용(1)로
                세팅하고 조회 및 연속조회하여야합니다.
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
            stk_cd: 종목코드 (필수) — 거래소별 종목코드 (KRX:039490,NXT:039490_NX,SOR:039490_AL)
            tic_scope: 틱범위 (필수) — 1:1분, 3:3분, 5:5분, 10:10분, 15:15분, 30:30분, 45:45분,
                60:60분
            upd_stkpc_tp: 수정주가구분 (필수) — 0 or 1
            base_dt: 기준일자 — YYYYMMDD
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
            stk_cd: 종목코드 (필수) — 거래소별 종목코드 (KRX:039490,NXT:039490_NX,SOR:039490_AL)
            base_dt: 기준일자 (필수) — YYYYMMDD
            upd_stkpc_tp: 수정주가구분 (필수) — 0 or 1
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
            stk_cd: 종목코드 (필수) — 거래소별 종목코드 (KRX:039490,NXT:039490_NX,SOR:039490_AL)
            tic_scope: 틱범위 (필수) — 1:1틱, 3:3틱, 5:5틱, 10:10틱, 30:30틱
            upd_stkpc_tp: 수정주가구분 (필수) — 0 or 1
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
            stk_cd: 종목코드 (필수) — 거래소별 종목코드 (KRX:039490,NXT:039490_NX,SOR:039490_AL)
            base_dt: 기준일자 (필수) — YYYYMMDD
            upd_stkpc_tp: 수정주가구분 (필수) — 0 or 1
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
            stk_cd: 종목코드 (필수) — 거래소별 종목코드 (KRX:039490,NXT:039490_NX,SOR:039490_AL)
            base_dt: 기준일자 (필수) — YYYYMMDD
            upd_stkpc_tp: 수정주가구분 (필수) — 0 or 1
        """
        ...
