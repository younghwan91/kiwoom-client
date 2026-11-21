# 자동 생성 — 고치지 말 것. scripts/build_stubs.py 가 spec/catalog.json 으로 만든다.
# 런타임은 .py 그대로(**kwargs). 스텁은 요청 필드를 IDE·mypy 에 알려 줄 뿐이다.
from typing import Any, Generic

from kiwoom_client.base import ClientProtocol, ResponseT

class StockInfo(Generic[ResponseT]):
    """Wraps all Stock Info (종목정보) endpoints under /api/dostk/stkinfo.

    Args:
        client: An authenticated BaseClient (sync) or AsyncBaseClient.
    """

    RESOURCE_URL: str

    def __init__(self, client: ClientProtocol[ResponseT]) -> None: ...

    def basic_stock_info(
        self,
        cont_yn: str = "N",
        next_key: str = "",
        *,
        stk_cd: str = ...,
        **kwargs: Any,
    ) -> ResponseT:
        """종목기본정보요청 (Basic Stock Info)

        api_id ``ka10001`` · 주식기본정보요청 · ``POST /api/dostk/stkinfo``

        Args:
            stk_cd: 종목코드 (필수) — 거래소별 종목코드 (KRX:039490,NXT:039490_NX,SOR:039490_AL)
        """
        ...

    def change_rate_vs_opening(
        self,
        cont_yn: str = "N",
        next_key: str = "",
        *,
        sort_tp: str = ...,
        trde_qty_cnd: str = ...,
        mrkt_tp: str = ...,
        updown_incls: str = ...,
        stk_cnd: str = ...,
        crd_cnd: str = ...,
        trde_prica_cnd: str = ...,
        flu_cnd: str = ...,
        stex_tp: str = ...,
        **kwargs: Any,
    ) -> ResponseT:
        """시가대비등락률요청 (Change Rate vs Opening Price)

        api_id ``ka10028`` · 시가대비등락률요청 · ``POST /api/dostk/stkinfo``

        Args:
            sort_tp: 정렬구분 (필수) — 1:시가, 2:고가, 3:저가, 4:기준가
            trde_qty_cnd: 거래량조건 (필수) — 0000:전체조회, 0010:만주이상, 0050:5만주이상,
                0100:10만주이상, 0500:50만주이상, 1000:백만주이상
            mrkt_tp: 시장구분 (필수) — 000:전체, 001:코스피, 101:코스닥
            updown_incls: 상하한포함 (필수) — 0:불 포함, 1:포함
            stk_cnd: 종목조건 (필수) — 0:전체조회, 1:관리종목제외, 4:우선주+관리주제외,
                3:우선주제외, 5:증100제외, 6:증100만보기, 7:증40만보기, 8:증30만보기, 9:증20만보기
            crd_cnd: 신용조건 (필수) — 0:전체조회, 1:신용융자A군, 2:신용융자B군, 3:신용융자C군,
                4:신용융자D군, 7:신용융자E군, 9:신용융자전체
            trde_prica_cnd: 거래대금조건 (필수) — 0:전체조회, 3:3천만원이상, 5:5천만원이상,
                10:1억원이상, 30:3억원이상, 50:5억원이상, 100:10억원이상, 300:30억원이상,
                500:50억원이상, 1000:100억원이상, 3000:300억원이상, 5000:500억원이상
            flu_cnd: 등락조건 (필수) — 1:상위, 2:하위
            stex_tp: 거래소구분 (필수) — 1:KRX, 2:NXT 3.통합
        """
        ...

    def credit_trading_trend(
        self,
        cont_yn: str = "N",
        next_key: str = "",
        *,
        stk_cd: str = ...,
        dt: str = ...,
        qry_tp: str = ...,
        **kwargs: Any,
    ) -> ResponseT:
        """신용매매동향요청 (Credit Trading Trend)

        api_id ``ka10013`` · 신용매매동향요청 · ``POST /api/dostk/stkinfo``

        Args:
            stk_cd: 종목코드 (필수) — 거래소별 종목코드 (KRX:039490,NXT:039490_NX,SOR:039490_AL)
            dt: 일자 (필수) — YYYYMMDD
            qry_tp: 조회구분 (필수) — 1:융자, 2:대주
        """
        ...

    def daily_trading_by_investor(
        self,
        cont_yn: str = "N",
        next_key: str = "",
        *,
        strt_dt: str = ...,
        end_dt: str = ...,
        trde_tp: str = ...,
        mrkt_tp: str = ...,
        invsr_tp: str = ...,
        stex_tp: str = ...,
        **kwargs: Any,
    ) -> ResponseT:
        """투자자별일별매매종목요청 (Daily Trading by Investor)

        api_id ``ka10058`` · 투자자별일별매매종목요청 · ``POST /api/dostk/stkinfo``

        Args:
            strt_dt: 시작일자 (필수) — YYYYMMDD
            end_dt: 종료일자 (필수) — YYYYMMDD
            trde_tp: 매매구분 (필수) — 순매도:1, 순매수:2
            mrkt_tp: 시장구분 (필수) — 001:코스피, 101:코스닥
            invsr_tp: 투자자구분 (필수) — 8000:개인, 9000:외국인, 1000:금융투자, 3000:투신,
                3100:사모펀드, 5000:기타금융, 4000:은행, 2000:보험, 6000:연기금, 7000:국가,
                7100:기타법인, 9999:기관계
            stex_tp: 거래소구분 (필수) — 1:KRX, 2:NXT 3.통합
        """
        ...

    def daily_transaction_detail(
        self,
        cont_yn: str = "N",
        next_key: str = "",
        *,
        stk_cd: str = ...,
        strt_dt: str = ...,
        **kwargs: Any,
    ) -> ResponseT:
        """일별거래상세요청 (Daily Transaction Detail)

        api_id ``ka10015`` · 일별거래상세요청 · ``POST /api/dostk/stkinfo``

        Args:
            stk_cd: 종목코드 (필수) — 거래소별 종목코드 (KRX:039490,NXT:039490_NX,SOR:039490_AL)
            strt_dt: 시작일자 (필수) — YYYMMDD, 시작일자 기준으로 이전 일별 거래 정보를 조회
        """
        ...

    def execution_info(
        self,
        cont_yn: str = "N",
        next_key: str = "",
        *,
        stk_cd: str = ...,
        **kwargs: Any,
    ) -> ResponseT:
        """체결정보요청 (Execution Info)

        api_id ``ka10003`` · 체결정보요청 · ``POST /api/dostk/stkinfo``

        Args:
            stk_cd: 종목코드 (필수) — 거래소별 종목코드 (KRX:039490,NXT:039490_NX,SOR:039490_AL)
        """
        ...

    def high_low_per(
        self,
        cont_yn: str = "N",
        next_key: str = "",
        *,
        pertp: str = ...,
        stex_tp: str = ...,
        **kwargs: Any,
    ) -> ResponseT:
        """고저PER요청 (High/Low PER)

        api_id ``ka10026`` · 고저PER요청 · ``POST /api/dostk/stkinfo``

        Args:
            pertp: PER구분 (필수) — 1:저PBR, 2:고PBR, 3:저PER, 4:고PER, 5:저ROE, 6:고ROE
            stex_tp: 거래소구분 (필수) — 1:KRX, 2:NXT 3.통합
        """
        ...

    def industry_code_list(
        self,
        cont_yn: str = "N",
        next_key: str = "",
        *,
        mrkt_tp: str = ...,
        **kwargs: Any,
    ) -> ResponseT:
        """업종코드 리스트 (Industry Code List)

        api_id ``ka10101`` · 업종코드 리스트 · ``POST /api/dostk/stkinfo``

        Args:
            mrkt_tp: 시장구분 (필수) —
                0:코스피(거래소),1:코스닥,2:KOSPI200,4:KOSPI100,7:KRX100(통합지수)
        """
        ...

    def investor_institution_aggregate(
        self,
        cont_yn: str = "N",
        next_key: str = "",
        *,
        stk_cd: str = ...,
        strt_dt: str = ...,
        end_dt: str = ...,
        amt_qty_tp: str = ...,
        trde_tp: str = ...,
        unit_tp: str = ...,
        **kwargs: Any,
    ) -> ResponseT:
        """종목별투자자기관별합계요청 (Investor/Institution by Stock Aggregate)

        api_id ``ka10061`` · 종목별투자자기관별합계요청 · ``POST /api/dostk/stkinfo``

        Args:
            stk_cd: 종목코드 (필수) — 거래소별 종목코드 (KRX:039490,NXT:039490_NX,SOR:039490_AL)
            strt_dt: 시작일자 (필수) — YYYYMMDD
            end_dt: 종료일자 (필수) — YYYYMMDD
            amt_qty_tp: 금액수량구분 (필수) — 1:금액, 2:수량
            trde_tp: 매매구분 (필수) — 0:순매수
            unit_tp: 단위구분 (필수) — 1000:천주, 1:단주
        """
        ...

    def investor_institution_by_stock(
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
        """투자자기관별종목별요청 (Investor/Institution by Stock)

        api_id ``ka10059`` · 종목별투자자기관별요청 · ``POST /api/dostk/stkinfo``

        Args:
            dt: 일자 (필수) — YYYYMMDD
            stk_cd: 종목코드 (필수) — 거래소별 종목코드 (KRX:039490,NXT:039490_NX,SOR:039490_AL)
            amt_qty_tp: 금액수량구분 (필수) — 1:금액, 2:수량
            trde_tp: 매매구분 (필수) — 0:순매수, 1:매수, 2:매도
            unit_tp: 단위구분 (필수) — 1000:천주, 1:단주
        """
        ...

    def margin_loan_available_stocks(
        self,
        cont_yn: str = "N",
        next_key: str = "",
        *,
        crd_stk_grde_tp: str = ...,
        mrkt_deal_tp: str = ...,
        stk_cd: str = ...,
        **kwargs: Any,
    ) -> ResponseT:
        """신용융자 가능종목요청 (Margin Loan Available Stocks)

        api_id ``kt20016`` · 신용융자 가능종목요청 · ``POST /api/dostk/stkinfo``

        Args:
            crd_stk_grde_tp: 신용종목등급구분 — %:전체, A:A군, B:B군, C:C군, D:D군, E:E군
            mrkt_deal_tp: 시장거래구분 (필수) — %:전체, 1:코스피, 0:코스닥
            stk_cd: 종목코드 — 종목 코드 입력
        """
        ...

    def margin_loan_inquiry(
        self,
        cont_yn: str = "N",
        next_key: str = "",
        *,
        stk_cd: str = ...,
        **kwargs: Any,
    ) -> ResponseT:
        """신용융자 가능문의 (Margin Loan Inquiry)

        api_id ``kt20017`` · 신용융자 가능문의 · ``POST /api/dostk/stkinfo``

        Args:
            stk_cd: 종목코드 (필수) — 종목 코드 입력
        """
        ...

    def member_company_list(
        self,
        cont_yn: str = "N",
        next_key: str = "",
        **kwargs: Any,
    ) -> ResponseT:
        """회원사 리스트 (Member Company List)

        api_id ``ka10102`` · 회원사 리스트 · ``POST /api/dostk/stkinfo``
        """
        ...

    def near_high_low(
        self,
        cont_yn: str = "N",
        next_key: str = "",
        *,
        high_low_tp: str = ...,
        alacc_rt: str = ...,
        mrkt_tp: str = ...,
        trde_qty_tp: str = ...,
        stk_cnd: str = ...,
        crd_cnd: str = ...,
        stex_tp: str = ...,
        **kwargs: Any,
    ) -> ResponseT:
        """고저근접요청 (Near High/Low)

        api_id ``ka10018`` · 고저가근접요청 · ``POST /api/dostk/stkinfo``

        Args:
            high_low_tp: 고저구분 (필수) — 1:고가, 2:저가
            alacc_rt: 근접율 (필수) — 05:0.5 10:1.0, 15:1.5, 20:2.0. 25:2.5, 30:3.0
            mrkt_tp: 시장구분 (필수) — 000:전체, 001:코스피, 101:코스닥
            trde_qty_tp: 거래량구분 (필수) — 00000:전체조회, 00010:만주이상, 00050:5만주이상,
                00100:10만주이상, 00150:15만주이상, 00200:20만주이상, 00300:30만주이상,
                00500:50만주이상, 01000:백만주이상
            stk_cnd: 종목조건 (필수) — 0:전체조회,1:관리종목제외, 3:우선주제외, 5:증100제외,
                6:증100만보기, 7:증40만보기, 8:증30만보기
            crd_cnd: 신용조건 (필수) — 0:전체조회, 1:신용융자A군, 2:신용융자B군, 3:신용융자C군,
                4:신용융자D군, 7:신용융자E군, 9:신용융자전체
            stex_tp: 거래소구분 (필수) — 1:KRX, 2:NXT 3.통합
        """
        ...

    def new_high_low(
        self,
        cont_yn: str = "N",
        next_key: str = "",
        *,
        mrkt_tp: str = ...,
        ntl_tp: str = ...,
        high_low_close_tp: str = ...,
        stk_cnd: str = ...,
        trde_qty_tp: str = ...,
        crd_cnd: str = ...,
        updown_incls: str = ...,
        dt: str = ...,
        stex_tp: str = ...,
        **kwargs: Any,
    ) -> ResponseT:
        """신고저가요청 (New High/Low)

        api_id ``ka10016`` · 신고저가요청 · ``POST /api/dostk/stkinfo``

        Args:
            mrkt_tp: 시장구분 (필수) — 000:전체, 001:코스피, 101:코스닥
            ntl_tp: 신고저구분 (필수) — 1:신고가,2:신저가
            high_low_close_tp: 고저종구분 (필수) — 1:고저기준, 2:종가기준
            stk_cnd: 종목조건 (필수) — 0:전체조회,1:관리종목제외, 3:우선주제외, 5:증100제외,
                6:증100만보기, 7:증40만보기, 8:증30만보기
            trde_qty_tp: 거래량구분 (필수) — 00000:전체조회, 00010:만주이상, 00050:5만주이상,
                00100:10만주이상, 00150:15만주이상, 00200:20만주이상, 00300:30만주이상,
                00500:50만주이상, 01000:백만주이상
            crd_cnd: 신용조건 (필수) — 0:전체조회, 1:신용융자A군, 2:신용융자B군, 3:신용융자C군,
                4:신용융자D군, 7:신용융자E군, 9:신용융자전체
            updown_incls: 상하한포함 (필수) — 0:미포함, 1:포함
            dt: 기간 (필수) — 5:5일, 10:10일, 20:20일, 60:60일, 250:250일, 250일까지 입력가능
            stex_tp: 거래소구분 (필수) — 1:KRX, 2:NXT 3.통합
        """
        ...

    def program_buy_top50(
        self,
        cont_yn: str = "N",
        next_key: str = "",
        *,
        trde_upper_tp: str = ...,
        amt_qty_tp: str = ...,
        mrkt_tp: str = ...,
        stex_tp: str = ...,
        **kwargs: Any,
    ) -> ResponseT:
        """프로그램순매수상위50요청 (Program Buy Top 50)

        api_id ``ka90003`` · 프로그램순매수상위50요청 · ``POST /api/dostk/stkinfo``

        Args:
            trde_upper_tp: 매매상위구분 (필수) — 1:순매도상위, 2:순매수상위
            amt_qty_tp: 금액수량구분 (필수) — 1:금액, 2:수량
            mrkt_tp: 시장구분 (필수) — P00101:코스피, P10102:코스닥
            stex_tp: 거래소구분 (필수) — 1:KRX, 2:NXT 3.통합
        """
        ...

    def program_trading_by_stock(
        self,
        cont_yn: str = "N",
        next_key: str = "",
        *,
        dt: str = ...,
        mrkt_tp: str = ...,
        stex_tp: str = ...,
        **kwargs: Any,
    ) -> ResponseT:
        """종목별프로그램매매현황요청 (Program Trading by Stock)

        api_id ``ka90004`` · 종목별프로그램매매현황요청 · ``POST /api/dostk/stkinfo``

        Args:
            dt: 일자 (필수) — YYYYMMDD
            mrkt_tp: 시장구분 (필수) — P00101:코스피, P10102:코스닥
            stex_tp: 거래소구분 (필수) — 1:KRX, 2:NXT 3.통합
        """
        ...

    def rapid_price_change(
        self,
        cont_yn: str = "N",
        next_key: str = "",
        *,
        mrkt_tp: str = ...,
        flu_tp: str = ...,
        tm_tp: str = ...,
        tm: str = ...,
        trde_qty_tp: str = ...,
        stk_cnd: str = ...,
        crd_cnd: str = ...,
        pric_cnd: str = ...,
        updown_incls: str = ...,
        stex_tp: str = ...,
        **kwargs: Any,
    ) -> ResponseT:
        """급등락요청 (Rapid Price Change)

        api_id ``ka10019`` · 가격급등락요청 · ``POST /api/dostk/stkinfo``

        Args:
            mrkt_tp: 시장구분 (필수) — 000:전체, 001:코스피, 101:코스닥, 201:코스피200
            flu_tp: 등락구분 (필수) — 1:급등, 2:급락
            tm_tp: 시간구분 (필수) — 1:분전, 2:일전
            tm: 시간 (필수) — 분 혹은 일입력
            trde_qty_tp: 거래량구분 (필수) — 00000:전체조회, 00010:만주이상, 00050:5만주이상,
                00100:10만주이상, 00150:15만주이상, 00200:20만주이상, 00300:30만주이상,
                00500:50만주이상, 01000:백만주이상
            stk_cnd: 종목조건 (필수) — 0:전체조회,1:관리종목제외, 3:우선주제외, 5:증100제외,
                6:증100만보기, 7:증40만보기, 8:증30만보기
            crd_cnd: 신용조건 (필수) — 0:전체조회, 1:신용융자A군, 2:신용융자B군, 3:신용융자C군,
                4:신용융자D군, 7:신용융자E군, 9:신용융자전체
            pric_cnd: 가격조건 (필수) — 0:전체조회, 1:1천원미만, 2:1천원~2천원, 3:2천원~3천원,
                4:5천원~1만원, 5:1만원이상, 8:1천원이상
            updown_incls: 상하한포함 (필수) — 0:미포함, 1:포함
            stex_tp: 거래소구분 (필수) — 1:KRX, 2:NXT 3.통합
        """
        ...

    def realtime_stock_inquiry_rank(
        self,
        cont_yn: str = "N",
        next_key: str = "",
        *,
        qry_tp: str = ...,
        **kwargs: Any,
    ) -> ResponseT:
        """실시간종목조회순위 (Real-time Stock Inquiry Ranking)

        api_id ``ka00198`` · 실시간종목조회순위 · ``POST /api/dostk/stkinfo``

        Args:
            qry_tp: 구분 (필수) — 1:1분, 2:10분, 3:1시간, 4:당일 누적, 5:30초
        """
        ...

    def stock_info_inquiry(
        self,
        cont_yn: str = "N",
        next_key: str = "",
        *,
        stk_cd: str = ...,
        **kwargs: Any,
    ) -> ResponseT:
        """종목정보 조회 (Stock Info Inquiry)

        api_id ``ka10100`` · 종목정보 조회 · ``POST /api/dostk/stkinfo``

        Args:
            stk_cd: 종목코드 (필수) — 종목코드 6자리
        """
        ...

    def stock_info_list(
        self,
        cont_yn: str = "N",
        next_key: str = "",
        *,
        mrkt_tp: str = ...,
        **kwargs: Any,
    ) -> ResponseT:
        """종목정보 리스트 (Stock Info List)

        api_id ``ka10099`` · 종목정보 리스트 · ``POST /api/dostk/stkinfo``

        Args:
            mrkt_tp: 시장구분 (필수) — 0 : 코스피, 10 : 코스닥, 30 : K-OTC, 50 : 코넥스, 60 : ETN,
                70 : 손실제한 ETN, 80 : 금현물, 90 : 변동성 ETN, 2 : 인프라투융자, 3 : ELW, 4 :
                뮤추얼펀드, 5 : 신주인수권, 6 : 리츠종목, 7 : 신주인수권증서, 8 : ETF, 9 :
                하이일드펀드
        """
        ...

    def stock_trading_agent(
        self,
        cont_yn: str = "N",
        next_key: str = "",
        *,
        stk_cd: str = ...,
        **kwargs: Any,
    ) -> ResponseT:
        """종목거래원요청 (Stock Trading Agent)

        api_id ``ka10002`` · 주식거래원요청 · ``POST /api/dostk/stkinfo``

        Args:
            stk_cd: 종목코드 (필수) — 거래소별 종목코드 (KRX:039490,NXT:039490_NX,SOR:039490_AL)
        """
        ...

    def today_vs_yesterday_execution(
        self,
        cont_yn: str = "N",
        next_key: str = "",
        *,
        stk_cd: str = ...,
        tdy_pred: str = ...,
        tic_min: str = ...,
        tm: str = ...,
        **kwargs: Any,
    ) -> ResponseT:
        """당일전일체결요청 (Today vs Yesterday Execution)

        api_id ``ka10084`` · 당일전일체결요청 · ``POST /api/dostk/stkinfo``

        Args:
            stk_cd: 종목코드 (필수) — 거래소별 종목코드 (KRX:039490,NXT:039490_NX,SOR:039490_AL)
            tdy_pred: 당일전일 (필수) — 당일 : 1, 전일 : 2
            tic_min: 틱분 (필수) — 0:틱, 1:분
            tm: 시간 — 조회시간 4자리, 오전 9시일 경우 0900, 오후 2시 30분일 경우 1430, 빈값('')
                입력 시 현재시간으로 자동 설정
        """
        ...

    def today_vs_yesterday_volume(
        self,
        cont_yn: str = "N",
        next_key: str = "",
        *,
        stk_cd: str = ...,
        tdy_pred: str = ...,
        **kwargs: Any,
    ) -> ResponseT:
        """당일전일체결량요청 (Today vs Yesterday Execution Volume)

        api_id ``ka10055`` · 당일전일체결량요청 · ``POST /api/dostk/stkinfo``

        Args:
            stk_cd: 종목코드 (필수) — 거래소별 종목코드 (KRX:039490,NXT:039490_NX,SOR:039490_AL)
            tdy_pred: 당일전일 (필수) — 1:당일, 2:전일
        """
        ...

    def trading_agent_instant_volume(
        self,
        cont_yn: str = "N",
        next_key: str = "",
        *,
        mmcm_cd: str = ...,
        stk_cd: str = ...,
        mrkt_tp: str = ...,
        qty_tp: str = ...,
        pric_tp: str = ...,
        stex_tp: str = ...,
        **kwargs: Any,
    ) -> ResponseT:
        """거래원순간거래량요청 (Trading Agent Instant Volume)

        api_id ``ka10052`` · 거래원순간거래량요청 · ``POST /api/dostk/stkinfo``

        Args:
            mmcm_cd: 회원사코드 (필수) — 회원사 코드는 ka10102 조회
            stk_cd: 종목코드 — 거래소별 종목코드 (KRX:039490,NXT:039490_NX,SOR:039490_AL)
            mrkt_tp: 시장구분 (필수) — 0:전체, 1:코스피, 2:코스닥, 3:종목
            qty_tp: 수량구분 (필수) — 0:전체, 1:1000주, 2:2000주, 3:, 5:, 10:10000주, 30: 30000주,
                50: 50000주, 100: 100000주
            pric_tp: 가격구분 (필수) — 0:전체, 1:1천원 미만, 8:1천원 이상, 2:1천원 ~ 2천원, 3:2천원
                ~ 5천원, 4:5천원 ~ 1만원, 5:1만원 이상
            stex_tp: 거래소구분 (필수) — 1:KRX, 2:NXT 3.통합
        """
        ...

    def trading_agent_supply_demand(
        self,
        cont_yn: str = "N",
        next_key: str = "",
        *,
        stk_cd: str = ...,
        strt_dt: str = ...,
        end_dt: str = ...,
        qry_dt_tp: str = ...,
        pot_tp: str = ...,
        dt: str = ...,
        sort_base: str = ...,
        mmcm_cd: str = ...,
        stex_tp: str = ...,
        **kwargs: Any,
    ) -> ResponseT:
        """거래원매물대분석요청 (Trading Agent Supply/Demand Trend Analysis)

        api_id ``ka10043`` · 거래원매물대분석요청 · ``POST /api/dostk/stkinfo``

        Args:
            stk_cd: 종목코드 (필수) — 거래소별 종목코드 (KRX:039490,NXT:039490_NX,SOR:039490_AL)
            strt_dt: 시작일자 (필수) — YYYYMMDD
            end_dt: 종료일자 (필수) — YYYYMMDD
            qry_dt_tp: 조회기간구분 (필수) — 0:기간으로 조회, 1:시작일자, 종료일자로 조회
            pot_tp: 시점구분 (필수) — 0:당일, 1:전일
            dt: 기간 (필수) — 5:5일, 10:10일, 20:20일, 40:40일, 60:60일, 120:120일
            sort_base: 정렬기준 (필수) — 1:종가순, 2:날짜순
            mmcm_cd: 회원사코드 (필수) — 회원사 코드는 ka10102 조회
            stex_tp: 거래소구분 (필수) — 1:KRX, 2:NXT 3.통합
        """
        ...

    def trading_volume_update(
        self,
        cont_yn: str = "N",
        next_key: str = "",
        *,
        mrkt_tp: str = ...,
        cycle_tp: str = ...,
        trde_qty_tp: str = ...,
        stex_tp: str = ...,
        **kwargs: Any,
    ) -> ResponseT:
        """거래량갱신요청 (Trading Volume Update)

        api_id ``ka10024`` · 거래량갱신요청 · ``POST /api/dostk/stkinfo``

        Args:
            mrkt_tp: 시장구분 (필수) — 000:전체, 001:코스피, 101:코스닥
            cycle_tp: 주기구분 (필수) — 5:5일, 10:10일, 20:20일, 60:60일, 250:250일
            trde_qty_tp: 거래량구분 (필수) — 5:5천주이상, 10:만주이상, 50:5만주이상, 100:10만주이상,
                200:20만주이상, 300:30만주이상, 500:50만주이상, 1000:백만주이상
            stex_tp: 거래소구분 (필수) — 1:KRX, 2:NXT 3.통합
        """
        ...

    def upper_lower_limit(
        self,
        cont_yn: str = "N",
        next_key: str = "",
        *,
        mrkt_tp: str = ...,
        updown_tp: str = ...,
        sort_tp: str = ...,
        stk_cnd: str = ...,
        trde_qty_tp: str = ...,
        crd_cnd: str = ...,
        trde_gold_tp: str = ...,
        stex_tp: str = ...,
        **kwargs: Any,
    ) -> ResponseT:
        """상하한가요청 (Upper/Lower Limit Price)

        api_id ``ka10017`` · 상하한가요청 · ``POST /api/dostk/stkinfo``

        Args:
            mrkt_tp: 시장구분 (필수) — 000:전체, 001:코스피, 101:코스닥
            updown_tp: 상하한구분 (필수) — 1:상한, 2:상승, 3:보합, 4: 하한, 5:하락, 6:전일상한,
                7:전일하한
            sort_tp: 정렬구분 (필수) — 1:종목코드순, 2:연속횟수순(상위100개), 3:등락률순
            stk_cnd: 종목조건 (필수) — 0:전체조회,1:관리종목제외, 3:우선주제외,
                4:우선주+관리종목제외, 5:증100제외, 6:증100만 보기, 7:증40만 보기, 8:증30만 보기,
                9:증20만 보기, 10:우선주+관리종목+환기종목제외
            trde_qty_tp: 거래량구분 (필수) — 00000:전체조회, 00010:만주이상, 00050:5만주이상,
                00100:10만주이상, 00150:15만주이상, 00200:20만주이상, 00300:30만주이상,
                00500:50만주이상, 01000:백만주이상
            crd_cnd: 신용조건 (필수) — 0:전체조회, 1:신용융자A군, 2:신용융자B군, 3:신용융자C군,
                4:신용융자D군, 7:신용융자E군, 9:신용융자전체
            trde_gold_tp: 매매금구분 (필수) — 0:전체조회, 1:1천원미만, 2:1천원~2천원, 3:2천원~3천원,
                4:5천원~1만원, 5:1만원이상, 8:1천원이상
            stex_tp: 거래소구분 (필수) — 1:KRX, 2:NXT 3.통합
        """
        ...

    def vi_triggered_stocks(
        self,
        cont_yn: str = "N",
        next_key: str = "",
        *,
        mrkt_tp: str = ...,
        bf_mkrt_tp: str = ...,
        stk_cd: str = ...,
        motn_tp: str = ...,
        skip_stk: str = ...,
        trde_qty_tp: str = ...,
        min_trde_qty: str = ...,
        max_trde_qty: str = ...,
        trde_prica_tp: str = ...,
        min_trde_prica: str = ...,
        max_trde_prica: str = ...,
        motn_drc: str = ...,
        stex_tp: str = ...,
        **kwargs: Any,
    ) -> ResponseT:
        """변동성완화장치발동종목요청 (VI Triggered Stocks)

        api_id ``ka10054`` · 변동성완화장치발동종목요청 · ``POST /api/dostk/stkinfo``

        Args:
            mrkt_tp: 시장구분 (필수) — 000:전체, 001: 코스피, 101:코스닥
            bf_mkrt_tp: 장전구분 (필수) — 0:전체, 1:정규시장,2:시간외단일가
            stk_cd: 종목코드 — 거래소별 종목코드 (KRX:039490,NXT:039490_NX,SOR:039490_AL) 공백입력시
                시장구분으로 설정한 전체종목조회
            motn_tp: 발동구분 (필수) — 0:전체, 1:정적VI, 2:동적VI, 3:동적VI + 정적VI
            skip_stk: 제외종목 (필수) — 전종목포함 조회시 9개 0으로 설정(000000000),전종목제외
                조회시 9개 1으로 설정(111111111),9개 종목조회여부를 조회포함(0), 조회제외(1)로
                설정하며 종목순서는
                우선주,관리종목,투자경고/위험,투자주의,환기종목,단기과열종목,증거금100%,ETF,ETN가
                됨.우선주만 조회시"011111111"", 관리종목만 조회시 ""101111111"" 설정"
            trde_qty_tp: 거래량구분 (필수) — 0:사용안함, 1:사용
            min_trde_qty: 최소거래량 (필수) — 0 주 이상, 거래량구분이 1일때만 입력(공백허용)
            max_trde_qty: 최대거래량 (필수) — 100000000 주 이하, 거래량구분이 1일때만 입력(공백허용)
            trde_prica_tp: 거래대금구분 (필수) — 0:사용안함, 1:사용
            min_trde_prica: 최소거래대금 (필수) — 0 백만원 이상, 거래대금구분 1일때만 입력(공백허용)
            max_trde_prica: 최대거래대금 (필수) — 100000000 백만원 이하, 거래대금구분 1일때만
                입력(공백허용)
            motn_drc: 발동방향 (필수) — 0:전체, 1:상승, 2:하락
            stex_tp: 거래소구분 (필수) — 1:KRX, 2:NXT 3.통합
        """
        ...

    def volume_concentration(
        self,
        cont_yn: str = "N",
        next_key: str = "",
        *,
        mrkt_tp: str = ...,
        prps_cnctr_rt: str = ...,
        cur_prc_entry: str = ...,
        prpscnt: str = ...,
        cycle_tp: str = ...,
        stex_tp: str = ...,
        **kwargs: Any,
    ) -> ResponseT:
        """매물대집중요청 (Volume Concentration)

        api_id ``ka10025`` · 매물대집중요청 · ``POST /api/dostk/stkinfo``

        Args:
            mrkt_tp: 시장구분 (필수) — 000:전체, 001:코스피, 101:코스닥
            prps_cnctr_rt: 매물집중비율 (필수) — 0~100 입력
            cur_prc_entry: 현재가진입 (필수) — 0:현재가 매물대 진입 포함안함, 1:현재가 매물대
                진입포함
            prpscnt: 매물대수 (필수) — 숫자입력
            cycle_tp: 주기구분 (필수) — 50:50일, 100:100일, 150:150일, 200:200일, 250:250일,
                300:300일
            stex_tp: 거래소구분 (필수) — 1:KRX, 2:NXT 3.통합
        """
        ...

    def watchlist_stock_info(
        self,
        cont_yn: str = "N",
        next_key: str = "",
        *,
        stk_cd: str = ...,
        **kwargs: Any,
    ) -> ResponseT:
        """관심종목정보요청 (Watchlist Stock Info)

        api_id ``ka10095`` · 지정종목 정보요청 · ``POST /api/dostk/stkinfo``

        Args:
            stk_cd: 종목코드 (필수) — 거래소별 종목코드 (KRX:039490,NXT:039490_NX,SOR:039490_AL)
                여러개의 종목코드 입력시 | 로 구분
        """
        ...
