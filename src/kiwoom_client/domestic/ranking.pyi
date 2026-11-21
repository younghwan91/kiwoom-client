# 자동 생성 — 고치지 말 것. scripts/build_stubs.py 가 spec/catalog.json 으로 만든다.
# 런타임은 .py 그대로(**kwargs). 스텁은 요청 필드를 IDE·mypy 에 알려 줄 뿐이다.
from typing import Any, Generic

from kiwoom_client.base import ClientProtocol, ResponseT

class Ranking(Generic[ResponseT]):
    """Wraps all Ranking (순위) endpoints under /api/dostk/rkinfo.

    Args:
        client: An authenticated BaseClient (sync) or AsyncBaseClient.
    """

    RESOURCE_URL: str

    def __init__(self, client: ClientProtocol[ResponseT]) -> None: ...

    def after_hours_change_rate_rank(
        self,
        cont_yn: str = "N",
        next_key: str = "",
        *,
        mrkt_tp: str = ...,
        sort_base: str = ...,
        stk_cnd: str = ...,
        trde_qty_cnd: str = ...,
        crd_cnd: str = ...,
        trde_prica: str = ...,
        **kwargs: Any,
    ) -> ResponseT:
        """시간외단일가등락율순위요청 (After Hours Change Rate Rank)

        api_id ``ka10098`` · 시간외단일가등락율순위요청 · ``POST /api/dostk/rkinfo``

        Args:
            mrkt_tp: 시장구분 (필수) — 000:전체,001:코스피,101:코스닥
            sort_base: 정렬기준 (필수) — 1:상승률, 2:상승폭, 3:하락률, 4:하락폭, 5:보합
            stk_cnd: 종목조건 (필수) —
                0:전체조회,1:관리종목제외,2:정리매매종목제외,3:우선주제외,4:관리종목우선주제외,5:증100제외,6:증100만보기,7:증40만보기,8:증30만보기,9:증20만보기,12:증50만보기,13:증60만보기,14:ETF제외,15:스팩제외,16:ETF+ETN제외,17:ETN제외
            trde_qty_cnd: 거래량조건 (필수) — 0:전체조회, 10:백주이상,50:5백주이상,100;천주이상,
                500:5천주이상, 1000:만주이상, 5000:5만주이상, 10000:10만주이상
            crd_cnd: 신용조건 (필수) — 0:전체조회, 9:신용융자전체, 1:신용융자A군, 2:신용융자B군,
                3:신용융자C군, 4:신용융자D군, 7:신용융자E군, 8:신용대주, 5:신용한도초과제외
            trde_prica: 거래대금 (필수) — 0:전체조회, 5:5백만원이상,10:1천만원이상, 30:3천만원이상,
                50:5천만원이상, 100:1억원이상, 300:3억원이상, 500:5억원이상, 1000:10억원이상,
                3000:30억원이상, 5000:50억원이상, 10000:100억원이상
        """
        ...

    def broker_ranking_by_stock(
        self,
        cont_yn: str = "N",
        next_key: str = "",
        *,
        stk_cd: str = ...,
        strt_dt: str = ...,
        end_dt: str = ...,
        qry_tp: str = ...,
        dt: str = ...,
        **kwargs: Any,
    ) -> ResponseT:
        """종목별증권사순위요청 (Broker Ranking by Stock)

        api_id ``ka10038`` · 종목별증권사순위요청 · ``POST /api/dostk/rkinfo``

        Args:
            stk_cd: 종목코드 (필수) — 거래소별 종목코드 (KRX:039490,NXT:039490_NX,SOR:039490_AL)
            strt_dt: 시작일자 — YYYYMMDD (연도4자리, 월 2자리, 일 2자리 형식)
            end_dt: 종료일자 — YYYYMMDD (연도4자리, 월 2자리, 일 2자리 형식)
            qry_tp: 조회구분 (필수) — 1:순매도순위정렬, 2:순매수순위정렬
            dt: 기간 — 1:전일, 4:5일, 9:10일, 19:20일, 39:40일, 59:60일, 119:120일 ※ 시작일자와
                종료일자로 조회를 원하는 경우 기간(dt)값은 빈값('')으로 설정
        """
        ...

    def departed_brokers_today(
        self,
        cont_yn: str = "N",
        next_key: str = "",
        *,
        stk_cd: str = ...,
        **kwargs: Any,
    ) -> ResponseT:
        """당일상위이탈원요청 (Departed Brokers Today)

        api_id ``ka10053`` · 당일상위이탈원요청 · ``POST /api/dostk/rkinfo``

        Args:
            stk_cd: 종목코드 (필수) — 거래소별 종목코드 (KRX:039490,NXT:039490_NX,SOR:039490_AL)
        """
        ...

    def main_brokers_today(
        self,
        cont_yn: str = "N",
        next_key: str = "",
        *,
        stk_cd: str = ...,
        **kwargs: Any,
    ) -> ResponseT:
        """당일주요거래원요청 (Main Brokers Today)

        api_id ``ka10040`` · 당일주요거래원요청 · ``POST /api/dostk/rkinfo``

        Args:
            stk_cd: 종목코드 (필수) — 거래소별 종목코드 (KRX:039490,NXT:039490_NX,SOR:039490_AL)
        """
        ...

    def same_day_net_buying_rank(
        self,
        cont_yn: str = "N",
        next_key: str = "",
        *,
        strt_dt: str = ...,
        end_dt: str = ...,
        mrkt_tp: str = ...,
        trde_tp: str = ...,
        sort_cnd: str = ...,
        unit_tp: str = ...,
        stex_tp: str = ...,
        **kwargs: Any,
    ) -> ResponseT:
        """동일순매매순위요청 (Same Day Net Buying Rank)

        api_id ``ka10062`` · 동일순매매순위요청 · ``POST /api/dostk/rkinfo``

        Args:
            strt_dt: 시작일자 (필수) — YYYYMMDD (연도4자리, 월 2자리, 일 2자리 형식)
            end_dt: 종료일자 — YYYYMMDD (연도4자리, 월 2자리, 일 2자리 형식)
            mrkt_tp: 시장구분 (필수) — 000:전체, 001: 코스피, 101:코스닥
            trde_tp: 매매구분 (필수) — 1:순매수, 2:순매도
            sort_cnd: 정렬조건 (필수) — 1:수량, 2:금액
            unit_tp: 단위구분 (필수) — 1:단주, 1000:천주
            stex_tp: 거래소구분 (필수) — 1:KRX, 2:NXT 3.통합
        """
        ...

    def sudden_order_book_increase(
        self,
        cont_yn: str = "N",
        next_key: str = "",
        *,
        mrkt_tp: str = ...,
        trde_tp: str = ...,
        sort_tp: str = ...,
        tm_tp: str = ...,
        trde_qty_tp: str = ...,
        stk_cnd: str = ...,
        stex_tp: str = ...,
        **kwargs: Any,
    ) -> ResponseT:
        """호가잔량급증요청 (Sudden Order Book Increase)

        api_id ``ka10021`` · 호가잔량급증요청 · ``POST /api/dostk/rkinfo``

        Args:
            mrkt_tp: 시장구분 (필수) — 001:코스피, 101:코스닥
            trde_tp: 매매구분 (필수) — 1:매수잔량, 2:매도잔량
            sort_tp: 정렬구분 (필수) — 1:급증량, 2:급증률
            tm_tp: 시간구분 (필수) — 분 입력
            trde_qty_tp: 거래량구분 (필수) — 1:천주이상, 5:5천주이상, 10:만주이상, 50:5만주이상,
                100:10만주이상
            stk_cnd: 종목조건 (필수) — 0:전체조회, 1:관리종목제외, 5:증100제외, 6:증100만보기,
                7:증40만보기, 8:증30만보기, 9:증20만보기
            stex_tp: 거래소구분 (필수) — 1:KRX, 2:NXT 3.통합
        """
        ...

    def sudden_order_ratio_increase(
        self,
        cont_yn: str = "N",
        next_key: str = "",
        *,
        mrkt_tp: str = ...,
        rt_tp: str = ...,
        tm_tp: str = ...,
        trde_qty_tp: str = ...,
        stk_cnd: str = ...,
        stex_tp: str = ...,
        **kwargs: Any,
    ) -> ResponseT:
        """잔량율급증요청 (Sudden Order Ratio Increase)

        api_id ``ka10022`` · 잔량율급증요청 · ``POST /api/dostk/rkinfo``

        Args:
            mrkt_tp: 시장구분 (필수) — 001:코스피, 101:코스닥
            rt_tp: 비율구분 (필수) — 1:매수/매도비율, 2:매도/매수비율
            tm_tp: 시간구분 (필수) — 분 입력
            trde_qty_tp: 거래량구분 (필수) — 5:5천주이상, 10:만주이상, 50:5만주이상, 100:10만주이상
            stk_cnd: 종목조건 (필수) — 0:전체조회, 1:관리종목제외, 5:증100제외, 6:증100만보기,
                7:증40만보기, 8:증30만보기, 9:증20만보기
            stex_tp: 거래소구분 (필수) — 1:KRX, 2:NXT 3.통합
        """
        ...

    def sudden_volume_increase(
        self,
        cont_yn: str = "N",
        next_key: str = "",
        *,
        mrkt_tp: str = ...,
        sort_tp: str = ...,
        tm_tp: str = ...,
        trde_qty_tp: str = ...,
        tm: str = ...,
        stk_cnd: str = ...,
        pric_tp: str = ...,
        stex_tp: str = ...,
        **kwargs: Any,
    ) -> ResponseT:
        """거래량급증요청 (Sudden Volume Increase)

        api_id ``ka10023`` · 거래량급증요청 · ``POST /api/dostk/rkinfo``

        Args:
            mrkt_tp: 시장구분 (필수) — 000:전체, 001:코스피, 101:코스닥
            sort_tp: 정렬구분 (필수) — 1:급증량, 2:급증률, 3:급감량, 4:급감률
            tm_tp: 시간구분 (필수) — 1:분, 2:전일
            trde_qty_tp: 거래량구분 (필수) — 5:5천주이상, 10:만주이상, 50:5만주이상, 100:10만주이상,
                200:20만주이상, 300:30만주이상, 500:50만주이상, 1000:백만주이상
            tm: 시간 — 분 입력
            stk_cnd: 종목조건 (필수) — 0:전체조회, 1:관리종목제외, 3:우선주제외,
                11:정리매매종목제외, 4:관리종목,우선주제외, 5:증100제외, 6:증100만보기,
                13:증60만보기, 12:증50만보기, 7:증40만보기, 8:증30만보기, 9:증20만보기, 17:ETN제외,
                14:ETF제외, 18:ETF+ETN제외, 15:스팩제외, 20:ETF+ETN+스팩제외
            pric_tp: 가격구분 (필수) — 0:전체조회, 2:5만원이상, 5:1만원이상, 6:5천원이상,
                8:1천원이상, 9:10만원이상
            stex_tp: 거래소구분 (필수) — 1:KRX, 2:NXT 3.통합
        """
        ...

    def top_broker_by_stock(
        self,
        cont_yn: str = "N",
        next_key: str = "",
        *,
        mmcm_cd: str = ...,
        trde_qty_tp: str = ...,
        trde_tp: str = ...,
        dt: str = ...,
        stex_tp: str = ...,
        **kwargs: Any,
    ) -> ResponseT:
        """증권사별매매상위요청 (Top Broker by Stock)

        api_id ``ka10039`` · 증권사별매매상위요청 · ``POST /api/dostk/rkinfo``

        Args:
            mmcm_cd: 회원사코드 (필수) — 회원사 코드는 ka10102 조회
            trde_qty_tp: 거래량구분 (필수) — 0:전체, 5:5000주, 10:1만주, 50:5만주, 100:10만주,
                500:50만주, 1000: 100만주
            trde_tp: 매매구분 (필수) — 1:순매수, 2:순매도
            dt: 기간 (필수) — 0:당일, 1:전일, 5:5일, 10:10일, 60:60일
            stex_tp: 거래소구분 (필수) — 1:KRX, 2:NXT 3.통합
        """
        ...

    def top_change_rate(
        self,
        cont_yn: str = "N",
        next_key: str = "",
        *,
        mrkt_tp: str = ...,
        sort_tp: str = ...,
        trde_qty_cnd: str = ...,
        stk_cnd: str = ...,
        crd_cnd: str = ...,
        updown_incls: str = ...,
        pric_cnd: str = ...,
        trde_prica_cnd: str = ...,
        stex_tp: str = ...,
        **kwargs: Any,
    ) -> ResponseT:
        """전일대비등락률상위요청 (Top Change Rate vs Previous Day)

        api_id ``ka10027`` · 전일대비등락률상위요청 · ``POST /api/dostk/rkinfo``

        Args:
            mrkt_tp: 시장구분 (필수) — 000:전체, 001:코스피, 101:코스닥
            sort_tp: 정렬구분 (필수) — 1:상승률, 2:상승폭, 3:하락률, 4:하락폭, 5:보합
            trde_qty_cnd: 거래량조건 (필수) — 0000:전체조회, 0010:만주이상, 0050:5만주이상,
                0100:10만주이상, 0150:15만주이상, 0200:20만주이상, 0300:30만주이상, 0500:50만주이상,
                1000:백만주이상
            stk_cnd: 종목조건 (필수) — 0:전체조회, 1:관리종목제외, 4:우선주+관리주제외,
                3:우선주제외, 5:증100제외, 6:증100만보기, 7:증40만보기, 8:증30만보기, 9:증20만보기,
                11:정리매매종목제외, 12:증50만보기, 13:증60만보기, 14:ETF제외, 15:스펙제외,
                16:ETF+ETN제외
            crd_cnd: 신용조건 (필수) — 0:전체조회, 1:신용융자A군, 2:신용융자B군, 3:신용융자C군,
                4:신용융자D군, 7:신용융자E군, 9:신용융자전체
            updown_incls: 상하한포함 (필수) — 0:불 포함, 1:포함
            pric_cnd: 가격조건 (필수) — 0:전체조회, 1:1천원미만, 2:1천원~2천원, 3:2천원~5천원,
                4:5천원~1만원, 5:1만원이상, 8:1천원이상, 10: 1만원미만
            trde_prica_cnd: 거래대금조건 (필수) — 0:전체조회, 3:3천만원이상, 5:5천만원이상,
                10:1억원이상, 30:3억원이상, 50:5억원이상, 100:10억원이상, 300:30억원이상,
                500:50억원이상, 1000:100억원이상, 3000:300억원이상, 5000:500억원이상
            stex_tp: 거래소구분 (필수) — 1:KRX, 2:NXT 3.통합
        """
        ...

    def top_credit_ratio(
        self,
        cont_yn: str = "N",
        next_key: str = "",
        *,
        mrkt_tp: str = ...,
        trde_qty_tp: str = ...,
        stk_cnd: str = ...,
        updown_incls: str = ...,
        crd_cnd: str = ...,
        stex_tp: str = ...,
        **kwargs: Any,
    ) -> ResponseT:
        """신용비율상위요청 (Top Credit Ratio)

        api_id ``ka10033`` · 신용비율상위요청 · ``POST /api/dostk/rkinfo``

        Args:
            mrkt_tp: 시장구분 (필수) — 000:전체, 001:코스피, 101:코스닥
            trde_qty_tp: 거래량구분 (필수) — 0:전체조회, 10:만주이상, 50:5만주이상, 100:10만주이상,
                200:20만주이상, 300:30만주이상, 500:50만주이상, 1000:백만주이상
            stk_cnd: 종목조건 (필수) — 0:전체조회, 1:관리종목제외, 5:증100제외, 6:증100만보기,
                7:증40만보기, 8:증30만보기, 9:증20만보기
            updown_incls: 상하한포함 (필수) — 0:상하한 미포함, 1:상하한포함
            crd_cnd: 신용조건 (필수) — 0:전체조회, 1:신용융자A군, 2:신용융자B군, 3:신용융자C군,
                4:신용융자D군, 7:신용융자E군, 9:신용융자전체
            stex_tp: 거래소구분 (필수) — 1:KRX, 2:NXT 3.통합
        """
        ...

    def top_expected_change_rate(
        self,
        cont_yn: str = "N",
        next_key: str = "",
        *,
        mrkt_tp: str = ...,
        sort_tp: str = ...,
        trde_qty_cnd: str = ...,
        stk_cnd: str = ...,
        crd_cnd: str = ...,
        pric_cnd: str = ...,
        stex_tp: str = ...,
        **kwargs: Any,
    ) -> ResponseT:
        """예상체결등락률상위요청 (Top Expected Execution Change Rate)

        api_id ``ka10029`` · 예상체결등락률상위요청 · ``POST /api/dostk/rkinfo``

        Args:
            mrkt_tp: 시장구분 (필수) — 000:전체, 001:코스피, 101:코스닥
            sort_tp: 정렬구분 (필수) — 1:상승률, 2:상승폭, 3:보합, 4:하락률, 5:하락폭, 6:체결량,
                7:상한, 8:하한
            trde_qty_cnd: 거래량조건 (필수) — 0:전체조회, 1;천주이상, 3:3천주, 5:5천주, 10:만주이상,
                50:5만주이상, 100:10만주이상
            stk_cnd: 종목조건 (필수) — 0:전체조회, 1:관리종목제외, 3:우선주제외,
                4:관리종목,우선주제외, 5:증100제외, 6:증100만보기, 7:증40만보기, 8:증30만보기,
                9:증20만보기, 11:정리매매종목제외, 12:증50만보기, 13:증60만보기, 14:ETF제외,
                15:스팩제외, 16:ETF+ETN제외
            crd_cnd: 신용조건 (필수) — 0:전체조회, 1:신용융자A군, 2:신용융자B군, 3:신용융자C군,
                4:신용융자D군, 5:신용한도초과제외, 7:신용융자E군, 8:신용대주, 9:신용융자전체
            pric_cnd: 가격조건 (필수) — 0:전체조회, 1:1천원미만, 2:1천원~2천원, 3:2천원~5천원,
                4:5천원~1만원, 5:1만원이상, 8:1천원이상, 10:1만원미만
            stex_tp: 거래소구분 (필수) — 1:KRX, 2:NXT 3.통합
        """
        ...

    def top_foreign_broker_trading(
        self,
        cont_yn: str = "N",
        next_key: str = "",
        *,
        mrkt_tp: str = ...,
        dt: str = ...,
        trde_tp: str = ...,
        sort_tp: str = ...,
        stex_tp: str = ...,
        **kwargs: Any,
    ) -> ResponseT:
        """외국계창구매매상위요청 (Top Foreign Holding Broker Trading)

        api_id ``ka10037`` · 외국계창구매매상위요청 · ``POST /api/dostk/rkinfo``

        Args:
            mrkt_tp: 시장구분 (필수) — 000:전체, 001:코스피, 101:코스닥
            dt: 기간 (필수) — 0:당일, 1:전일, 5:5일, 10;10일, 20:20일, 60:60일
            trde_tp: 매매구분 (필수) — 1:순매수, 2:순매도, 3:매수, 4:매도
            sort_tp: 정렬구분 (필수) — 1:금액, 2:수량
            stex_tp: 거래소구분 (필수) — 1:KRX, 2:NXT, 3:통합
        """
        ...

    def top_foreign_consecutive_buy(
        self,
        cont_yn: str = "N",
        next_key: str = "",
        *,
        mrkt_tp: str = ...,
        trde_tp: str = ...,
        base_dt_tp: str = ...,
        stex_tp: str = ...,
        **kwargs: Any,
    ) -> ResponseT:
        """외인연속순매매상위요청 (Top Foreign Consecutive Net Buy)

        api_id ``ka10035`` · 외인연속순매매상위요청 · ``POST /api/dostk/rkinfo``

        Args:
            mrkt_tp: 시장구분 (필수) — 000:전체, 001:코스피, 101:코스닥
            trde_tp: 매매구분 (필수) — 1:연속순매도, 2:연속순매수
            base_dt_tp: 기준일구분 (필수) — 0:당일기준, 1:전일기준
            stex_tp: 거래소구분 (필수) — 1:KRX, 2:NXT, 3:통합
        """
        ...

    def top_foreign_institution_trades(
        self,
        cont_yn: str = "N",
        next_key: str = "",
        *,
        mrkt_tp: str = ...,
        amt_qty_tp: str = ...,
        qry_dt_tp: str = ...,
        date: str = ...,
        stex_tp: str = ...,
        **kwargs: Any,
    ) -> ResponseT:
        """외국인기관매매상위요청 (Top Foreign Institution Trades)

        api_id ``ka90009`` · 외국인기관매매상위요청 · ``POST /api/dostk/rkinfo``

        Args:
            mrkt_tp: 시장구분 (필수) — 000:전체, 001:코스피, 101:코스닥
            amt_qty_tp: 금액수량구분 (필수) — 1:금액(천만), 2:수량(천)
            qry_dt_tp: 조회일자구분 (필수) — 0:조회일자 미포함, 1:조회일자 포함
            date: 날짜 — YYYYMMDD (연도4자리, 월 2자리, 일 2자리 형식)
            stex_tp: 거래소구분 (필수) — 1:KRX, 2:NXT, 3:통합
        """
        ...

    def top_foreign_limit_increase(
        self,
        cont_yn: str = "N",
        next_key: str = "",
        *,
        mrkt_tp: str = ...,
        dt: str = ...,
        stex_tp: str = ...,
        **kwargs: Any,
    ) -> ResponseT:
        """외인한도소진율증가상위 (Top Foreign Limit Exhaustion Rate Increase)

        api_id ``ka10036`` · 외인한도소진율증가상위 · ``POST /api/dostk/rkinfo``

        Args:
            mrkt_tp: 시장구분 (필수) — 000:전체, 001:코스피, 101:코스닥
            dt: 기간 (필수) — 0:당일, 1:전일, 5:5일, 10;10일, 20:20일, 60:60일
            stex_tp: 거래소구분 (필수) — 1:KRX, 2:NXT, 3:통합
        """
        ...

    def top_foreign_trades_by_period(
        self,
        cont_yn: str = "N",
        next_key: str = "",
        *,
        mrkt_tp: str = ...,
        trde_tp: str = ...,
        dt: str = ...,
        stex_tp: str = ...,
        **kwargs: Any,
    ) -> ResponseT:
        """외인기간별매매상위요청 (Top Foreign Trades by Period)

        api_id ``ka10034`` · 외인기간별매매상위요청 · ``POST /api/dostk/rkinfo``

        Args:
            mrkt_tp: 시장구분 (필수) — 000:전체, 001:코스피, 101:코스닥
            trde_tp: 매매구분 (필수) — 1:순매도, 2:순매수, 3:순매매
            dt: 기간 (필수) — 0:당일, 1:전일, 5:5일, 10;10일, 20:20일, 60:60일
            stex_tp: 거래소구분 (필수) — 1:KRX, 2:NXT, 3:통합
        """
        ...

    def top_intraday_investor_trading(
        self,
        cont_yn: str = "N",
        next_key: str = "",
        *,
        trde_tp: str = ...,
        mrkt_tp: str = ...,
        orgn_tp: str = ...,
        amt_qty_tp: str = ...,
        **kwargs: Any,
    ) -> ResponseT:
        """장중투자자별매매상위요청 (Top Intraday Investor Trading by Time)

        api_id ``ka10065`` · 장중투자자별매매상위요청 · ``POST /api/dostk/rkinfo``

        Args:
            trde_tp: 매매구분 (필수) — 1:순매수, 2:순매도
            mrkt_tp: 시장구분 (필수) — 000:전체, 001:코스피, 101:코스닥
            orgn_tp: 기관구분 (필수) — 9000:외국인, 9100:외국계, 1000:금융투자, 3000:투신,
                5000:기타금융, 4000:은행, 2000:보험, 6000:연기금, 7000:국가, 7100:기타법인,
                9999:기관계
            amt_qty_tp: 금액수량구분 — 1:금액, 2:수량
        """
        ...

    def top_net_buying_brokers(
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
        **kwargs: Any,
    ) -> ResponseT:
        """순매수거래원순위요청 (Top Net Buying Brokers)

        api_id ``ka10042`` · 순매수거래원순위요청 · ``POST /api/dostk/rkinfo``

        Args:
            stk_cd: 종목코드 (필수) — 거래소별 종목코드 (KRX:039490,NXT:039490_NX,SOR:039490_AL)
            strt_dt: 시작일자 — YYYYMMDD (연도4자리, 월 2자리, 일 2자리 형식)
            end_dt: 종료일자 — YYYYMMDD (연도4자리, 월 2자리, 일 2자리 형식)
            qry_dt_tp: 조회기간구분 (필수) — 0:기간으로 조회, 1:시작일자, 종료일자로 조회
            pot_tp: 시점구분 (필수) — 0:당일, 1:전일
            dt: 기간 — 5:5일, 10:10일, 20:20일, 40:40일, 60:60일, 120:120일
            sort_base: 정렬기준 (필수) — 1:종가순, 2:날짜순
        """
        ...

    def top_order_book_volume(
        self,
        cont_yn: str = "N",
        next_key: str = "",
        *,
        mrkt_tp: str = ...,
        sort_tp: str = ...,
        trde_qty_tp: str = ...,
        stk_cnd: str = ...,
        crd_cnd: str = ...,
        stex_tp: str = ...,
        **kwargs: Any,
    ) -> ResponseT:
        """호가잔량상위요청 (Top Order Book Volume)

        api_id ``ka10020`` · 호가잔량상위요청 · ``POST /api/dostk/rkinfo``

        Args:
            mrkt_tp: 시장구분 (필수) — 001:코스피, 101:코스닥
            sort_tp: 정렬구분 (필수) — 1:순매수잔량순, 2:순매도잔량순, 3:매수비율순, 4:매도비율순
            trde_qty_tp: 거래량구분 (필수) — 0000:장시작전(0주이상), 0010:만주이상, 0050:5만주이상,
                00100:10만주이상
            stk_cnd: 종목조건 (필수) — 0:전체조회, 1:관리종목제외, 5:증100제외, 6:증100만보기,
                7:증40만보기, 8:증30만보기, 9:증20만보기
            crd_cnd: 신용조건 (필수) — 0:전체조회, 1:신용융자A군, 2:신용융자B군, 3:신용융자C군,
                4:신용융자D군, 7:신용융자E군, 9:신용융자전체
            stex_tp: 거래소구분 (필수) — 1:KRX, 2:NXT 3.통합
        """
        ...

    def top_trading_value(
        self,
        cont_yn: str = "N",
        next_key: str = "",
        *,
        mrkt_tp: str = ...,
        mang_stk_incls: str = ...,
        stex_tp: str = ...,
        **kwargs: Any,
    ) -> ResponseT:
        """거래대금상위요청 (Top Trading Value)

        api_id ``ka10032`` · 거래대금상위요청 · ``POST /api/dostk/rkinfo``

        Args:
            mrkt_tp: 시장구분 (필수) — 000:전체, 001:코스피, 101:코스닥
            mang_stk_incls: 관리종목포함 (필수) — 0:관리종목 미포함, 1:관리종목 포함
            stex_tp: 거래소구분 (필수) — 1:KRX, 2:NXT 3.통합
        """
        ...

    def top_volume_today(
        self,
        cont_yn: str = "N",
        next_key: str = "",
        *,
        mrkt_tp: str = ...,
        sort_tp: str = ...,
        mang_stk_incls: str = ...,
        crd_tp: str = ...,
        trde_qty_tp: str = ...,
        pric_tp: str = ...,
        trde_prica_tp: str = ...,
        mrkt_open_tp: str = ...,
        stex_tp: str = ...,
        **kwargs: Any,
    ) -> ResponseT:
        """당일거래량상위요청 (Top Volume Today)

        api_id ``ka10030`` · 당일거래량상위요청 · ``POST /api/dostk/rkinfo``

        Args:
            mrkt_tp: 시장구분 (필수) — 000:전체, 001:코스피, 101:코스닥
            sort_tp: 정렬구분 (필수) — 1:거래량, 2:거래회전율, 3:거래대금
            mang_stk_incls: 관리종목포함 (필수) — 0:관리종목 포함, 1:관리종목 미포함, 3:우선주제외,
                11:정리매매종목제외, 4:관리종목, 우선주제외, 5:증100제외, 6:증100마나보기,
                13:증60만보기, 12:증50만보기, 7:증40만보기, 8:증30만보기, 9:증20만보기, 14:ETF제외,
                15:스팩제외, 16:ETF+ETN제외
            crd_tp: 신용구분 (필수) — 0:전체조회, 9:신용융자전체, 1:신용융자A군, 2:신용융자B군,
                3:신용융자C군, 4:신용융자D군, 8:신용대주
            trde_qty_tp: 거래량구분 (필수) — 0:전체조회, 5:5천주이상, 10:1만주이상, 50:5만주이상,
                100:10만주이상, 200:20만주이상, 300:30만주이상, 500:500만주이상, 1000:백만주이상
            pric_tp: 가격구분 (필수) — 0:전체조회, 1:1천원미만, 2:1천원이상, 3:1천원~2천원,
                4:2천원~5천원, 5:5천원이상, 6:5천원~1만원, 10:1만원미만, 7:1만원이상, 8:5만원이상,
                9:10만원이상
            trde_prica_tp: 거래대금구분 (필수) — 0:전체조회, 1:1천만원이상, 3:3천만원이상,
                4:5천만원이상, 10:1억원이상, 30:3억원이상, 50:5억원이상, 100:10억원이상,
                300:30억원이상, 500:50억원이상, 1000:100억원이상, 3000:300억원이상, 5000:500억원이상
            mrkt_open_tp: 장운영구분 (필수) — 0:전체조회, 1:장중, 2:장전시간외, 3:장후시간외
            stex_tp: 거래소구분 (필수) — 1:KRX, 2:NXT 3.통합
        """
        ...

    def top_volume_yesterday(
        self,
        cont_yn: str = "N",
        next_key: str = "",
        *,
        mrkt_tp: str = ...,
        qry_tp: str = ...,
        rank_strt: str = ...,
        rank_end: str = ...,
        stex_tp: str = ...,
        **kwargs: Any,
    ) -> ResponseT:
        """전일거래량상위요청 (Top Volume Yesterday)

        api_id ``ka10031`` · 전일거래량상위요청 · ``POST /api/dostk/rkinfo``

        Args:
            mrkt_tp: 시장구분 (필수) — 000:전체, 001:코스피, 101:코스닥
            qry_tp: 조회구분 (필수) — 1:전일거래량 상위100종목, 2:전일거래대금 상위100종목
            rank_strt: 순위시작 (필수) — 0 ~ 100 값 중에 조회를 원하는 순위 시작값
            rank_end: 순위끝 (필수) — 0 ~ 100 값 중에 조회를 원하는 순위 끝값
            stex_tp: 거래소구분 (필수) — 1:KRX, 2:NXT 3.통합
        """
        ...
