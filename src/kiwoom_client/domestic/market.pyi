# 자동 생성 — 고치지 말 것. scripts/build_stubs.py 가 spec/catalog.json 으로 만든다.
# 런타임은 .py 그대로(**kwargs). 스텁은 요청 필드를 IDE·mypy 에 알려 줄 뿐이다.
from typing import Any, Generic

from kiwoom_client.base import ClientProtocol, ResponseT

class Market(Generic[ResponseT]):
    """Wraps all Market (시세) endpoints under /api/dostk/mrkcond.

    Args:
        client: An authenticated BaseClient (sync) or AsyncBaseClient.
    """

    RESOURCE_URL: str

    def __init__(self, client: ClientProtocol[ResponseT]) -> None: ...

    def after_hours_investor_trading(
        self,
        cont_yn: str = "N",
        next_key: str = "",
        *,
        mrkt_tp: str = ...,
        amt_qty_tp: str = ...,
        trde_tp: str = ...,
        stex_tp: str = ...,
        **kwargs: Any,
    ) -> ResponseT:
        """장마감후투자자별매매요청 (After-Hours Investor Trading)

        api_id ``ka10066`` · 장마감후투자자별매매요청 · ``POST /api/dostk/mrkcond``

        Args:
            mrkt_tp: 시장구분 (필수) — 000:전체, 001:코스피, 101:코스닥
            amt_qty_tp: 금액수량구분 (필수) — 1:금액, 2:수량
            trde_tp: 매매구분 (필수) — 0:순매수, 1:매수, 2:매도
            stex_tp: 거래소구분 (필수) — 1:KRX, 2:NXT 3.통합
        """
        ...

    def after_hours_single_price(
        self,
        cont_yn: str = "N",
        next_key: str = "",
        *,
        stk_cd: str = ...,
        **kwargs: Any,
    ) -> ResponseT:
        """시간외단일가요청 (After-Hours Single Price)

        api_id ``ka10087`` · 시간외단일가요청 · ``POST /api/dostk/mrkcond``

        Args:
            stk_cd: 종목코드 (필수)
        """
        ...

    def broker_stock_trading_trend(
        self,
        cont_yn: str = "N",
        next_key: str = "",
        *,
        mmcm_cd: str = ...,
        stk_cd: str = ...,
        strt_dt: str = ...,
        end_dt: str = ...,
        **kwargs: Any,
    ) -> ResponseT:
        """증권사별종목매매동향요청 (Broker Stock Trading Trend)

        api_id ``ka10078`` · 증권사별종목매매동향요청 · ``POST /api/dostk/mrkcond``

        Args:
            mmcm_cd: 회원사코드 (필수) — 회원사 코드는 ka10102 조회
            stk_cd: 종목코드 (필수) — 거래소별 종목코드 (KRX:039490,NXT:039490_NX,SOR:039490_AL)
            strt_dt: 시작일자 (필수) — YYYYMMDD
            end_dt: 종료일자 (필수) — YYYYMMDD
        """
        ...

    def cumulative_program_trading(
        self,
        cont_yn: str = "N",
        next_key: str = "",
        *,
        date: str = ...,
        amt_qty_tp: str = ...,
        mrkt_tp: str = ...,
        stex_tp: str = ...,
        **kwargs: Any,
    ) -> ResponseT:
        """프로그램매매누적추이요청 (Cumulative Program Trading Trend)

        api_id ``ka90007`` · 프로그램매매누적추이요청 · ``POST /api/dostk/mrkcond``

        Args:
            date: 날짜 (필수) — YYYYMMDD (종료일기준 1년간 데이터만 조회가능)
            amt_qty_tp: 금액수량구분 (필수) — 1:금액, 2:수량
            mrkt_tp: 시장구분 (필수) — 0:코스피 , 1:코스닥
            stex_tp: 거래소구분 (필수) — 1:KRX, 2:NXT, 3:통합
        """
        ...

    def daily_execution_strength(
        self,
        cont_yn: str = "N",
        next_key: str = "",
        *,
        stk_cd: str = ...,
        **kwargs: Any,
    ) -> ResponseT:
        """체결강도추이일별요청 (Daily Execution Strength)

        api_id ``ka10047`` · 체결강도추이일별요청 · ``POST /api/dostk/mrkcond``

        Args:
            stk_cd: 종목코드 (필수) — 거래소별 종목코드 (KRX:039490,NXT:039490_NX,SOR:039490_AL)
        """
        ...

    def daily_institutional_trading(
        self,
        cont_yn: str = "N",
        next_key: str = "",
        *,
        strt_dt: str = ...,
        end_dt: str = ...,
        trde_tp: str = ...,
        mrkt_tp: str = ...,
        stex_tp: str = ...,
        **kwargs: Any,
    ) -> ResponseT:
        """일별기관매매종목요청 (Daily Institutional Trading by Stock)

        api_id ``ka10044`` · 일별기관매매종목요청 · ``POST /api/dostk/mrkcond``

        Args:
            strt_dt: 시작일자 (필수) — YYYYMMDD
            end_dt: 종료일자 (필수) — YYYYMMDD
            trde_tp: 매매구분 (필수) — 1:순매도, 2:순매수
            mrkt_tp: 시장구분 (필수) — 001:코스피, 101:코스닥
            stex_tp: 거래소구분 (필수) — 1:KRX, 2:NXT 3.통합
        """
        ...

    def daily_stock_price(
        self,
        cont_yn: str = "N",
        next_key: str = "",
        *,
        stk_cd: str = ...,
        qry_dt: str = ...,
        indc_tp: str = ...,
        **kwargs: Any,
    ) -> ResponseT:
        """일자별주가요청 (Daily Stock Price)

        api_id ``ka10086`` · 일별주가요청 · ``POST /api/dostk/mrkcond``

        Args:
            stk_cd: 종목코드 (필수) — 거래소별 종목코드 (KRX:039490,NXT:039490_NX,SOR:039490_AL)
            qry_dt: 조회일자 (필수) — YYYYMMDD
            indc_tp: 표시구분 (필수) — 0:수량, 1:금액(백만원)
        """
        ...

    def gold_spot_daily_trend(
        self,
        cont_yn: str = "N",
        next_key: str = "",
        *,
        stk_cd: str = ...,
        base_dt: str = ...,
        **kwargs: Any,
    ) -> ResponseT:
        """금현물일별추이 (Gold Spot Daily Trend)

        api_id ``ka50012`` · 금현물일별추이 · ``POST /api/dostk/mrkcond``

        Args:
            stk_cd: 종목코드 (필수) — M04020000 금 99.99_1kg, M04020100 미니금 99.99_100g
            base_dt: 기준일자 (필수) — YYYYMMDD
        """
        ...

    def gold_spot_execution_trend(
        self,
        cont_yn: str = "N",
        next_key: str = "",
        *,
        stk_cd: str = ...,
        **kwargs: Any,
    ) -> ResponseT:
        """금현물체결추이 (Gold Spot Execution Trend)

        api_id ``ka50010`` · 금현물체결추이 · ``POST /api/dostk/mrkcond``

        Args:
            stk_cd: 종목코드 (필수) — M04020000 금 99.99_1kg, M04020100 미니금 99.99_100g
        """
        ...

    def gold_spot_expected_execution(
        self,
        cont_yn: str = "N",
        next_key: str = "",
        *,
        stk_cd: str = ...,
        **kwargs: Any,
    ) -> ResponseT:
        """금현물예상체결 (Gold Spot Expected Execution)

        api_id ``ka50087`` · 금현물예상체결 · ``POST /api/dostk/mrkcond``

        Args:
            stk_cd: 종목코드 (필수) — M04020000 금 99.99_1kg, M04020100 미니금 99.99_100g
        """
        ...

    def gold_spot_order_book(
        self,
        cont_yn: str = "N",
        next_key: str = "",
        *,
        stk_cd: str = ...,
        tic_scope: str = ...,
        **kwargs: Any,
    ) -> ResponseT:
        """금현물 호가 (Gold Spot Order Book)

        api_id ``ka50101`` · 금현물 호가 · ``POST /api/dostk/mrkcond``

        Args:
            stk_cd: 종목코드 (필수) — M04020000 금 99.99_1kg, M04020100 미니금 99.99_100g
            tic_scope: 틱범위 (필수) — 1:1틱, 3:3틱, 5:5틱, 10:10틱, 30:30틱
        """
        ...

    def gold_spot_price_info(
        self,
        cont_yn: str = "N",
        next_key: str = "",
        *,
        stk_cd: str = ...,
        **kwargs: Any,
    ) -> ResponseT:
        """금현물 시세정보 (Gold Spot Price Info)

        api_id ``ka50100`` · 금현물 시세정보 · ``POST /api/dostk/mrkcond``

        Args:
            stk_cd: 종목코드 (필수) — M04020000: 금 99.99_1kg, M04020100: 미니금 99.99_100g
        """
        ...

    def hourly_execution_strength(
        self,
        cont_yn: str = "N",
        next_key: str = "",
        *,
        stk_cd: str = ...,
        **kwargs: Any,
    ) -> ResponseT:
        """체결강도추이시간별요청 (Hourly Execution Strength)

        api_id ``ka10046`` · 체결강도추이시간별요청 · ``POST /api/dostk/mrkcond``

        Args:
            stk_cd: 종목코드 (필수) — 거래소별 종목코드 (KRX:039490,NXT:039490_NX,SOR:039490_AL)
        """
        ...

    def institutional_trading_trend(
        self,
        cont_yn: str = "N",
        next_key: str = "",
        *,
        stk_cd: str = ...,
        strt_dt: str = ...,
        end_dt: str = ...,
        orgn_prsm_unp_tp: str = ...,
        for_prsm_unp_tp: str = ...,
        **kwargs: Any,
    ) -> ResponseT:
        """종목별기관매매추이요청 (Institutional Trading Trend by Stock)

        api_id ``ka10045`` · 종목별기관매매추이요청 · ``POST /api/dostk/mrkcond``

        Args:
            stk_cd: 종목코드 (필수) — 거래소별 종목코드 (KRX:039490,NXT:039490_NX,SOR:039490_AL)
            strt_dt: 시작일자 (필수) — YYYYMMDD
            end_dt: 종료일자 (필수) — YYYYMMDD
            orgn_prsm_unp_tp: 기관추정단가구분 (필수) — 1:매수단가, 2:매도단가
            for_prsm_unp_tp: 외인추정단가구분 (필수) — 1:매수단가, 2:매도단가
        """
        ...

    def intraday_investor_trading(
        self,
        cont_yn: str = "N",
        next_key: str = "",
        *,
        mrkt_tp: str = ...,
        amt_qty_tp: str = ...,
        invsr: str = ...,
        frgn_all: str = ...,
        smtm_netprps_tp: str = ...,
        stex_tp: str = ...,
        **kwargs: Any,
    ) -> ResponseT:
        """장중투자자별매매요청 (Intraday Investor Trading by Time Slot)

        api_id ``ka10063`` · 장중투자자별매매요청 · ``POST /api/dostk/mrkcond``

        Args:
            mrkt_tp: 시장구분 (필수) — 000:전체, 001:코스피, 101:코스닥
            amt_qty_tp: 금액수량구분 (필수) — 1: 금액&수량
            invsr: 투자자별 (필수) — 6:외국인, 7:기관계, 1:투신, 0:보험, 2:은행, 3:연기금, 4:국가,
                5:기타법인
            frgn_all: 외국계전체 (필수) — 1:체크, 0:미체크
            smtm_netprps_tp: 동시순매수구분 (필수) — 1:체크, 0:미체크
            stex_tp: 거래소구분 (필수) — 1:KRX, 2:NXT 3.통합
        """
        ...

    def order_book_info(
        self,
        cont_yn: str = "N",
        next_key: str = "",
        *,
        stk_cd: str = ...,
        **kwargs: Any,
    ) -> ResponseT:
        """시세표성정보요청 (Order Book Info)

        api_id ``ka10007`` · 시세표성정보요청 · ``POST /api/dostk/mrkcond``

        Args:
            stk_cd: 종목코드 (필수) — 거래소별 종목코드 (KRX:039490,NXT:039490_NX,SOR:039490_AL)
        """
        ...

    def program_arbitrage_balance(
        self,
        cont_yn: str = "N",
        next_key: str = "",
        *,
        date: str = ...,
        stex_tp: str = ...,
        **kwargs: Any,
    ) -> ResponseT:
        """프로그램매매차익잔고추이요청 (Program Arbitrage Balance Trend)

        api_id ``ka90006`` · 프로그램매매차익잔고추이요청 · ``POST /api/dostk/mrkcond``

        Args:
            date: 날짜 (필수) — YYYYMMDD
            stex_tp: 거래소구분 (필수) — 1:KRX, 2:NXT 3.통합
        """
        ...

    def program_trading_by_date(
        self,
        cont_yn: str = "N",
        next_key: str = "",
        *,
        date: str = ...,
        amt_qty_tp: str = ...,
        mrkt_tp: str = ...,
        min_tic_tp: str = ...,
        stex_tp: str = ...,
        **kwargs: Any,
    ) -> ResponseT:
        """프로그램매매추이요청 일자별 (Program Trading by Date)

        api_id ``ka90010`` · 프로그램매매추이요청 일자별 · ``POST /api/dostk/mrkcond``

        Args:
            date: 날짜 (필수) — YYYYMMDD
            amt_qty_tp: 금액수량구분 (필수) — 1:금액(백만원), 2:수량(천주)
            mrkt_tp: 시장구분 (필수) — 코스피- 거래소구분값 1일경우:P00101, 2일경우:P001_NX01,
                3일경우:P001_AL01 코스닥- 거래소구분값 1일경우:P10102, 2일경우:P101_NX02,
                3일경우:P001_AL02
            min_tic_tp: 분틱구분 (필수) — 0:틱, 1:분
            stex_tp: 거래소구분 (필수) — 1:KRX, 2:NXT 3.통합
        """
        ...

    def program_trading_by_stock_day(
        self,
        cont_yn: str = "N",
        next_key: str = "",
        *,
        amt_qty_tp: str = ...,
        stk_cd: str = ...,
        date: str = ...,
        **kwargs: Any,
    ) -> ResponseT:
        """종목일별프로그램매매추이요청 (Program Trading by Stock and Day)

        api_id ``ka90013`` · 종목일별프로그램매매추이요청 · ``POST /api/dostk/mrkcond``

        Args:
            amt_qty_tp: 금액수량구분 — 1:금액, 2:수량
            stk_cd: 종목코드 (필수) — 거래소별 종목코드 (KRX:039490,NXT:039490_NX,SOR:039490_AL)
            date: 날짜 — YYYYMMDD
        """
        ...

    def program_trading_by_stock_time(
        self,
        cont_yn: str = "N",
        next_key: str = "",
        *,
        amt_qty_tp: str = ...,
        stk_cd: str = ...,
        date: str = ...,
        **kwargs: Any,
    ) -> ResponseT:
        """종목시간별프로그램매매추이요청 (Program Trading by Stock and Time Slot)

        api_id ``ka90008`` · 종목시간별프로그램매매추이요청 · ``POST /api/dostk/mrkcond``

        Args:
            amt_qty_tp: 금액수량구분 (필수) — 1:금액, 2:수량
            stk_cd: 종목코드 (필수) — 거래소별 종목코드 (KRX:039490,NXT:039490_NX,SOR:039490_AL)
            date: 날짜 (필수) — YYYYMMDD
        """
        ...

    def program_trading_by_time(
        self,
        cont_yn: str = "N",
        next_key: str = "",
        *,
        date: str = ...,
        amt_qty_tp: str = ...,
        mrkt_tp: str = ...,
        min_tic_tp: str = ...,
        stex_tp: str = ...,
        **kwargs: Any,
    ) -> ResponseT:
        """프로그램매매추이요청 시간대별 (Program Trading by Time Slot)

        api_id ``ka90005`` · 프로그램매매추이요청 시간대별 · ``POST /api/dostk/mrkcond``

        Args:
            date: 날짜 (필수) — YYYYMMDD
            amt_qty_tp: 금액수량구분 (필수) — 1:금액(백만원), 2:수량(천주)
            mrkt_tp: 시장구분 (필수) — 코스피- 거래소구분값 1일경우:P00101, 2일경우:P001_NX01,
                3일경우:P001_AL01 코스닥- 거래소구분값 1일경우:P10102, 2일경우:P101_NX02,
                3일경우:P101_AL02
            min_tic_tp: 분틱구분 (필수) — 0:틱, 1:분
            stex_tp: 거래소구분 (필수) — 1:KRX, 2:NXT 3.통합
        """
        ...

    def rights_issue_price(
        self,
        cont_yn: str = "N",
        next_key: str = "",
        *,
        newstk_recvrht_tp: str = ...,
        **kwargs: Any,
    ) -> ResponseT:
        """신주인수권전체시세요청 (Rights Issue Price)

        api_id ``ka10011`` · 신주인수권전체시세요청 · ``POST /api/dostk/mrkcond``

        Args:
            newstk_recvrht_tp: 신주인수권구분 (필수) — 00:전체, 05:신주인수권증권, 07:신주인수권증서
        """
        ...

    def stock_daily_weekly_monthly(
        self,
        cont_yn: str = "N",
        next_key: str = "",
        *,
        stk_cd: str = ...,
        **kwargs: Any,
    ) -> ResponseT:
        """주식일주월시분요청 (Stock Daily/Weekly/Monthly by Time)

        api_id ``ka10005`` · 주식일주월시분요청 · ``POST /api/dostk/mrkcond``

        Args:
            stk_cd: 종목코드 (필수) — 거래소별 종목코드 (KRX:039490,NXT:039490_NX,SOR:039490_AL)
        """
        ...

    def stock_minute_price(
        self,
        cont_yn: str = "N",
        next_key: str = "",
        *,
        stk_cd: str = ...,
        **kwargs: Any,
    ) -> ResponseT:
        """주식시분요청 (Stock Minute Price)

        api_id ``ka10006`` · 주식시분요청 · ``POST /api/dostk/mrkcond``

        Args:
            stk_cd: 종목코드 (필수) — 거래소별 종목코드 (KRX:039490,NXT:039490_NX,SOR:039490_AL)
        """
        ...

    def stock_quote(
        self,
        cont_yn: str = "N",
        next_key: str = "",
        *,
        stk_cd: str = ...,
        **kwargs: Any,
    ) -> ResponseT:
        """주식호가요청 (Stock Quote)

        api_id ``ka10004`` · 주식호가요청 · ``POST /api/dostk/mrkcond``

        Args:
            stk_cd: 종목코드 (필수) — 거래소별 종목코드 (KRX:039490,NXT:039490_NX,SOR:039490_AL)
        """
        ...
