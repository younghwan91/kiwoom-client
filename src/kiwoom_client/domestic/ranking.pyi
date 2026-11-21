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
            mrkt_tp: 시장구분 (필수)
            sort_base: 정렬기준 (필수)
            stk_cnd: 종목조건 (필수)
            trde_qty_cnd: 거래량조건 (필수)
            crd_cnd: 신용조건 (필수)
            trde_prica: 거래대금 (필수)
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
            stk_cd: 종목코드 (필수)
            strt_dt: 시작일자
            end_dt: 종료일자
            qry_tp: 조회구분 (필수)
            dt: 기간
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
            stk_cd: 종목코드 (필수)
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
            stk_cd: 종목코드 (필수)
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
            strt_dt: 시작일자 (필수)
            end_dt: 종료일자
            mrkt_tp: 시장구분 (필수)
            trde_tp: 매매구분 (필수)
            sort_cnd: 정렬조건 (필수)
            unit_tp: 단위구분 (필수)
            stex_tp: 거래소구분 (필수)
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
            mrkt_tp: 시장구분 (필수)
            trde_tp: 매매구분 (필수)
            sort_tp: 정렬구분 (필수)
            tm_tp: 시간구분 (필수)
            trde_qty_tp: 거래량구분 (필수)
            stk_cnd: 종목조건 (필수)
            stex_tp: 거래소구분 (필수)
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
            mrkt_tp: 시장구분 (필수)
            rt_tp: 비율구분 (필수)
            tm_tp: 시간구분 (필수)
            trde_qty_tp: 거래량구분 (필수)
            stk_cnd: 종목조건 (필수)
            stex_tp: 거래소구분 (필수)
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
            mrkt_tp: 시장구분 (필수)
            sort_tp: 정렬구분 (필수)
            tm_tp: 시간구분 (필수)
            trde_qty_tp: 거래량구분 (필수)
            tm: 시간
            stk_cnd: 종목조건 (필수)
            pric_tp: 가격구분 (필수)
            stex_tp: 거래소구분 (필수)
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
            mmcm_cd: 회원사코드 (필수)
            trde_qty_tp: 거래량구분 (필수)
            trde_tp: 매매구분 (필수)
            dt: 기간 (필수)
            stex_tp: 거래소구분 (필수)
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
            mrkt_tp: 시장구분 (필수)
            sort_tp: 정렬구분 (필수)
            trde_qty_cnd: 거래량조건 (필수)
            stk_cnd: 종목조건 (필수)
            crd_cnd: 신용조건 (필수)
            updown_incls: 상하한포함 (필수)
            pric_cnd: 가격조건 (필수)
            trde_prica_cnd: 거래대금조건 (필수)
            stex_tp: 거래소구분 (필수)
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
            mrkt_tp: 시장구분 (필수)
            trde_qty_tp: 거래량구분 (필수)
            stk_cnd: 종목조건 (필수)
            updown_incls: 상하한포함 (필수)
            crd_cnd: 신용조건 (필수)
            stex_tp: 거래소구분 (필수)
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
            mrkt_tp: 시장구분 (필수)
            sort_tp: 정렬구분 (필수)
            trde_qty_cnd: 거래량조건 (필수)
            stk_cnd: 종목조건 (필수)
            crd_cnd: 신용조건 (필수)
            pric_cnd: 가격조건 (필수)
            stex_tp: 거래소구분 (필수)
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
            mrkt_tp: 시장구분 (필수)
            dt: 기간 (필수)
            trde_tp: 매매구분 (필수)
            sort_tp: 정렬구분 (필수)
            stex_tp: 거래소구분 (필수)
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
            mrkt_tp: 시장구분 (필수)
            trde_tp: 매매구분 (필수)
            base_dt_tp: 기준일구분 (필수)
            stex_tp: 거래소구분 (필수)
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
            mrkt_tp: 시장구분 (필수)
            amt_qty_tp: 금액수량구분 (필수)
            qry_dt_tp: 조회일자구분 (필수)
            date: 날짜
            stex_tp: 거래소구분 (필수)
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
            mrkt_tp: 시장구분 (필수)
            dt: 기간 (필수)
            stex_tp: 거래소구분 (필수)
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
            mrkt_tp: 시장구분 (필수)
            trde_tp: 매매구분 (필수)
            dt: 기간 (필수)
            stex_tp: 거래소구분 (필수)
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
            trde_tp: 매매구분 (필수)
            mrkt_tp: 시장구분 (필수)
            orgn_tp: 기관구분 (필수)
            amt_qty_tp: 금액수량구분
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
            stk_cd: 종목코드 (필수)
            strt_dt: 시작일자
            end_dt: 종료일자
            qry_dt_tp: 조회기간구분 (필수)
            pot_tp: 시점구분 (필수)
            dt: 기간
            sort_base: 정렬기준 (필수)
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
            mrkt_tp: 시장구분 (필수)
            sort_tp: 정렬구분 (필수)
            trde_qty_tp: 거래량구분 (필수)
            stk_cnd: 종목조건 (필수)
            crd_cnd: 신용조건 (필수)
            stex_tp: 거래소구분 (필수)
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
            mrkt_tp: 시장구분 (필수)
            mang_stk_incls: 관리종목포함 (필수)
            stex_tp: 거래소구분 (필수)
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
            mrkt_tp: 시장구분 (필수)
            sort_tp: 정렬구분 (필수)
            mang_stk_incls: 관리종목포함 (필수)
            crd_tp: 신용구분 (필수)
            trde_qty_tp: 거래량구분 (필수)
            pric_tp: 가격구분 (필수)
            trde_prica_tp: 거래대금구분 (필수)
            mrkt_open_tp: 장운영구분 (필수)
            stex_tp: 거래소구분 (필수)
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
            mrkt_tp: 시장구분 (필수)
            qry_tp: 조회구분 (필수)
            rank_strt: 순위시작 (필수)
            rank_end: 순위끝 (필수)
            stex_tp: 거래소구분 (필수)
        """
        ...
