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
            stk_cd: 종목코드 (필수)
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
            sort_tp: 정렬구분 (필수)
            trde_qty_cnd: 거래량조건 (필수)
            mrkt_tp: 시장구분 (필수)
            updown_incls: 상하한포함 (필수)
            stk_cnd: 종목조건 (필수)
            crd_cnd: 신용조건 (필수)
            trde_prica_cnd: 거래대금조건 (필수)
            flu_cnd: 등락조건 (필수)
            stex_tp: 거래소구분 (필수)
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
            stk_cd: 종목코드 (필수)
            dt: 일자 (필수)
            qry_tp: 조회구분 (필수)
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
            strt_dt: 시작일자 (필수)
            end_dt: 종료일자 (필수)
            trde_tp: 매매구분 (필수)
            mrkt_tp: 시장구분 (필수)
            invsr_tp: 투자자구분 (필수)
            stex_tp: 거래소구분 (필수)
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
            stk_cd: 종목코드 (필수)
            strt_dt: 시작일자 (필수)
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
            stk_cd: 종목코드 (필수)
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
            pertp: PER구분 (필수)
            stex_tp: 거래소구분 (필수)
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
            mrkt_tp: 시장구분 (필수)
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
            stk_cd: 종목코드 (필수)
            strt_dt: 시작일자 (필수)
            end_dt: 종료일자 (필수)
            amt_qty_tp: 금액수량구분 (필수)
            trde_tp: 매매구분 (필수)
            unit_tp: 단위구분 (필수)
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
            dt: 일자 (필수)
            stk_cd: 종목코드 (필수)
            amt_qty_tp: 금액수량구분 (필수)
            trde_tp: 매매구분 (필수)
            unit_tp: 단위구분 (필수)
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
            crd_stk_grde_tp: 신용종목등급구분
            mrkt_deal_tp: 시장거래구분 (필수)
            stk_cd: 종목코드
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
            stk_cd: 종목코드 (필수)
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
            high_low_tp: 고저구분 (필수)
            alacc_rt: 근접율 (필수)
            mrkt_tp: 시장구분 (필수)
            trde_qty_tp: 거래량구분 (필수)
            stk_cnd: 종목조건 (필수)
            crd_cnd: 신용조건 (필수)
            stex_tp: 거래소구분 (필수)
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
            mrkt_tp: 시장구분 (필수)
            ntl_tp: 신고저구분 (필수)
            high_low_close_tp: 고저종구분 (필수)
            stk_cnd: 종목조건 (필수)
            trde_qty_tp: 거래량구분 (필수)
            crd_cnd: 신용조건 (필수)
            updown_incls: 상하한포함 (필수)
            dt: 기간 (필수)
            stex_tp: 거래소구분 (필수)
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
            trde_upper_tp: 매매상위구분 (필수)
            amt_qty_tp: 금액수량구분 (필수)
            mrkt_tp: 시장구분 (필수)
            stex_tp: 거래소구분 (필수)
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
            dt: 일자 (필수)
            mrkt_tp: 시장구분 (필수)
            stex_tp: 거래소구분 (필수)
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
            mrkt_tp: 시장구분 (필수)
            flu_tp: 등락구분 (필수)
            tm_tp: 시간구분 (필수)
            tm: 시간 (필수)
            trde_qty_tp: 거래량구분 (필수)
            stk_cnd: 종목조건 (필수)
            crd_cnd: 신용조건 (필수)
            pric_cnd: 가격조건 (필수)
            updown_incls: 상하한포함 (필수)
            stex_tp: 거래소구분 (필수)
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
            qry_tp: 구분 (필수)
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
            stk_cd: 종목코드 (필수)
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
            mrkt_tp: 시장구분 (필수)
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
            stk_cd: 종목코드 (필수)
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
            stk_cd: 종목코드 (필수)
            tdy_pred: 당일전일 (필수)
            tic_min: 틱분 (필수)
            tm: 시간
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
            stk_cd: 종목코드 (필수)
            tdy_pred: 당일전일 (필수)
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
            mmcm_cd: 회원사코드 (필수)
            stk_cd: 종목코드
            mrkt_tp: 시장구분 (필수)
            qty_tp: 수량구분 (필수)
            pric_tp: 가격구분 (필수)
            stex_tp: 거래소구분 (필수)
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
            stk_cd: 종목코드 (필수)
            strt_dt: 시작일자 (필수)
            end_dt: 종료일자 (필수)
            qry_dt_tp: 조회기간구분 (필수)
            pot_tp: 시점구분 (필수)
            dt: 기간 (필수)
            sort_base: 정렬기준 (필수)
            mmcm_cd: 회원사코드 (필수)
            stex_tp: 거래소구분 (필수)
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
            mrkt_tp: 시장구분 (필수)
            cycle_tp: 주기구분 (필수)
            trde_qty_tp: 거래량구분 (필수)
            stex_tp: 거래소구분 (필수)
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
            mrkt_tp: 시장구분 (필수)
            updown_tp: 상하한구분 (필수)
            sort_tp: 정렬구분 (필수)
            stk_cnd: 종목조건 (필수)
            trde_qty_tp: 거래량구분 (필수)
            crd_cnd: 신용조건 (필수)
            trde_gold_tp: 매매금구분 (필수)
            stex_tp: 거래소구분 (필수)
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
            mrkt_tp: 시장구분 (필수)
            bf_mkrt_tp: 장전구분 (필수)
            stk_cd: 종목코드
            motn_tp: 발동구분 (필수)
            skip_stk: 제외종목 (필수)
            trde_qty_tp: 거래량구분 (필수)
            min_trde_qty: 최소거래량 (필수)
            max_trde_qty: 최대거래량 (필수)
            trde_prica_tp: 거래대금구분 (필수)
            min_trde_prica: 최소거래대금 (필수)
            max_trde_prica: 최대거래대금 (필수)
            motn_drc: 발동방향 (필수)
            stex_tp: 거래소구분 (필수)
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
            mrkt_tp: 시장구분 (필수)
            prps_cnctr_rt: 매물집중비율 (필수)
            cur_prc_entry: 현재가진입 (필수)
            prpscnt: 매물대수 (필수)
            cycle_tp: 주기구분 (필수)
            stex_tp: 거래소구분 (필수)
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
            stk_cd: 종목코드 (필수)
        """
        ...
