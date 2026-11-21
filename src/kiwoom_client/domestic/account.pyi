# 자동 생성 — 고치지 말 것. scripts/build_stubs.py 가 spec/catalog.json 으로 만든다.
# 런타임은 .py 그대로(**kwargs). 스텁은 요청 필드를 IDE·mypy 에 알려 줄 뿐이다.
from typing import Any, Generic

from kiwoom_client.base import ClientProtocol, ResponseT

class Account(Generic[ResponseT]):
    """Wraps all Account (계좌) endpoints under /api/dostk/acnt.

    Args:
        client: An authenticated BaseClient (sync) or AsyncBaseClient.
    """

    RESOURCE_URL: str

    def __init__(self, client: ClientProtocol[ResponseT]) -> None: ...

    def account_evaluation(
        self,
        cont_yn: str = "N",
        next_key: str = "",
        *,
        qry_tp: str = ...,
        dmst_stex_tp: str = ...,
        **kwargs: Any,
    ) -> ResponseT:
        """계좌평가현황요청 (Account Evaluation Status)

        api_id ``kt00004`` · 계좌평가현황요청 · ``POST /api/dostk/acnt``

        Args:
            qry_tp: 상장폐지조회구분 (필수) — 0:전체, 1:상장폐지종목제외
            dmst_stex_tp: 국내거래소구분 (필수) — KRX:한국거래소,NXT:넥스트트레이드
        """
        ...

    def account_number_inquiry(
        self,
        cont_yn: str = "N",
        next_key: str = "",
        **kwargs: Any,
    ) -> ResponseT:
        """계좌번호조회 (Account Number Inquiry)

        api_id ``ka00001`` · 계좌번호조회 · ``POST /api/dostk/acnt``
        """
        ...

    def account_return_rate(
        self,
        cont_yn: str = "N",
        next_key: str = "",
        *,
        stex_tp: str = ...,
        **kwargs: Any,
    ) -> ResponseT:
        """계좌수익률요청 (Account Return Rate)

        api_id ``ka10085`` · 계좌수익률요청 · ``POST /api/dostk/acnt``

        Args:
            stex_tp: 거래소구분 (필수) — 0 : 통합, 1 : KRX, 2 : NXT
        """
        ...

    def comprehensive_transaction_history(
        self,
        cont_yn: str = "N",
        next_key: str = "",
        *,
        strt_dt: str = ...,
        end_dt: str = ...,
        tp: str = ...,
        stk_cd: str = ...,
        crnc_cd: str = ...,
        gds_tp: str = ...,
        frgn_stex_code: str = ...,
        dmst_stex_tp: str = ...,
        qry_sort_tp: str = ...,
        **kwargs: Any,
    ) -> ResponseT:
        """위탁종합거래내역요청 (Comprehensive Transaction History)

        api_id ``kt00015`` · 위탁종합거래내역요청 · ``POST /api/dostk/acnt``

        Args:
            strt_dt: 시작일자 (필수) — YYYYMMDD
            end_dt: 종료일자 (필수) — YYYYMMDD
            tp: 구분 (필수) —
                0:전체,1:입출금,2:입출고,3:매매,4:매수,5:매도,6:입금,7:출금,A:예탁담보대출입금,B:매도담보대출입금,C:현금상환(융자,담보상환),F:환전,M:입출금+환전,G:외화매수,H:외화매도,I:환전정산입금,J:환전정산출금
            stk_cd: 종목코드 — 종목 코드 입력
            crnc_cd: 통화코드 — 통화코드 3자리
            gds_tp: 상품구분 (필수) — 0:전체, 1:국내주식, 2:수익증권, 3:해외주식, 4:금융상품
            frgn_stex_code: 해외거래소코드
            dmst_stex_tp: 국내거래소구분 (필수) — %:(전체),KRX:한국거래소,NXT:넥스트트레이드
            qry_sort_tp: 조회정렬구분 — 1:최근거래순, 2:과거거래순(미입력시 과거거래순)
        """
        ...

    def daily_balance_return_rate(
        self,
        cont_yn: str = "N",
        next_key: str = "",
        *,
        qry_dt: str = ...,
        **kwargs: Any,
    ) -> ResponseT:
        """일별잔고수익률 (Daily Balance Return Rate)

        api_id ``ka01690`` · 일별잔고수익률 · ``POST /api/dostk/acnt``

        Args:
            qry_dt: 조회일자 (필수) — YYYYMMDD
        """
        ...

    def daily_estimated_deposit(
        self,
        cont_yn: str = "N",
        next_key: str = "",
        *,
        start_dt: str = ...,
        end_dt: str = ...,
        **kwargs: Any,
    ) -> ResponseT:
        """일별추정예탁자산현황요청 (Daily Estimated Deposit Asset Status)

        api_id ``kt00002`` · 일별추정예탁자산현황요청 · ``POST /api/dostk/acnt``

        Args:
            start_dt: 시작조회기간 (필수) — YYYYMMDD
            end_dt: 종료조회기간 (필수) — YYYYMMDD
        """
        ...

    def daily_realized_profit(
        self,
        cont_yn: str = "N",
        next_key: str = "",
        *,
        strt_dt: str = ...,
        end_dt: str = ...,
        **kwargs: Any,
    ) -> ResponseT:
        """일별실현손익요청 (Daily Realized Profit)

        api_id ``ka10074`` · 일자별실현손익요청 · ``POST /api/dostk/acnt``

        Args:
            strt_dt: 시작일자 (필수) — YYYYMMDD
            end_dt: 종료일자 (필수) — YYYYMMDD
        """
        ...

    def daily_return_detail(
        self,
        cont_yn: str = "N",
        next_key: str = "",
        *,
        fr_dt: str = ...,
        to_dt: str = ...,
        **kwargs: Any,
    ) -> ResponseT:
        """일별계좌수익률상세현황요청 (Daily Account Return Rate Detail)

        api_id ``kt00016`` · 일별계좌수익률상세현황요청 · ``POST /api/dostk/acnt``

        Args:
            fr_dt: 평가시작일 (필수) — YYYYMMDD
            to_dt: 평가종료일 (필수) — YYYYMMDD
        """
        ...

    def deposit_detail(
        self,
        cont_yn: str = "N",
        next_key: str = "",
        *,
        qry_tp: str = ...,
        **kwargs: Any,
    ) -> ResponseT:
        """예수금상세현황요청 (Deposit Detail Status)

        api_id ``kt00001`` · 예수금상세현황요청 · ``POST /api/dostk/acnt``

        Args:
            qry_tp: 조회구분 (필수) — 3:추정조회, 2:일반조회
        """
        ...

    def estimated_asset(
        self,
        cont_yn: str = "N",
        next_key: str = "",
        *,
        qry_tp: str = ...,
        **kwargs: Any,
    ) -> ResponseT:
        """추정자산조회요청 (Estimated Asset Inquiry)

        api_id ``kt00003`` · 추정자산조회요청 · ``POST /api/dostk/acnt``

        Args:
            qry_tp: 상장폐지조회구분 (필수) — 0:전체, 1:상장폐지종목제외
        """
        ...

    def evaluation_balance_detail(
        self,
        cont_yn: str = "N",
        next_key: str = "",
        *,
        qry_tp: str = ...,
        dmst_stex_tp: str = ...,
        **kwargs: Any,
    ) -> ResponseT:
        """계좌평가잔고내역요청 (Account Evaluation Balance Detail)

        api_id ``kt00018`` · 계좌평가잔고내역요청 · ``POST /api/dostk/acnt``

        Args:
            qry_tp: 조회구분 (필수) — 1:합산, 2:개별
            dmst_stex_tp: 국내거래소구분 (필수) — KRX:한국거래소,NXT:넥스트트레이드
        """
        ...

    def filled_orders(
        self,
        cont_yn: str = "N",
        next_key: str = "",
        *,
        stk_cd: str = ...,
        qry_tp: str = ...,
        sell_tp: str = ...,
        ord_no: str = ...,
        stex_tp: str = ...,
        **kwargs: Any,
    ) -> ResponseT:
        """체결요청 (Filled Orders History)

        api_id ``ka10076`` · 체결요청 · ``POST /api/dostk/acnt``

        Args:
            stk_cd: 종목코드 — 종목코드 6자리
            qry_tp: 조회구분 (필수) — 0:전체, 1:종목
            sell_tp: 매도수구분 (필수) — 0:전체, 1:매도, 2:매수
            ord_no: 주문번호 — 검색 기준 값으로 입력한 주문번호 보다 과거에 체결된 내역이
                조회됩니다.
            stex_tp: 거래소구분 (필수) — 0 : 통합, 1 : KRX, 2 : NXT
        """
        ...

    def filled_position(
        self,
        cont_yn: str = "N",
        next_key: str = "",
        *,
        dmst_stex_tp: str = ...,
        **kwargs: Any,
    ) -> ResponseT:
        """체결잔고요청 (Filled Position Balance)

        api_id ``kt00005`` · 체결잔고요청 · ``POST /api/dostk/acnt``

        Args:
            dmst_stex_tp: 국내거래소구분 (필수) — KRX:한국거래소,NXT:넥스트트레이드
        """
        ...

    def gold_spot_balance(
        self,
        cont_yn: str = "N",
        next_key: str = "",
        **kwargs: Any,
    ) -> ResponseT:
        """금현물 잔고확인 (Gold Spot Balance)

        api_id ``kt50020`` · 금현물 잔고확인 · ``POST /api/dostk/acnt``
        """
        ...

    def gold_spot_deposit(
        self,
        cont_yn: str = "N",
        next_key: str = "",
        **kwargs: Any,
    ) -> ResponseT:
        """금현물 예수금 (Gold Spot Deposit)

        api_id ``kt50021`` · 금현물 예수금 · ``POST /api/dostk/acnt``
        """
        ...

    def gold_spot_order_execution(
        self,
        cont_yn: str = "N",
        next_key: str = "",
        *,
        ord_dt: str = ...,
        qry_tp: str = ...,
        stk_bond_tp: str = ...,
        sell_tp: str = ...,
        stk_cd: str = ...,
        fr_ord_no: str = ...,
        dmst_stex_tp: str = ...,
        **kwargs: Any,
    ) -> ResponseT:
        """금현물 주문체결조회 (Gold Spot Order Execution)

        api_id ``kt50031`` · 금현물 주문체결조회 · ``POST /api/dostk/acnt``

        Args:
            ord_dt: 주문일자 — YYYYMMDD
            qry_tp: 조회구분 (필수) — 1:주문순, 2:역순, 3:미체결, 4:체결내역만
            stk_bond_tp: 주식채권구분 (필수) — 0:전체, 1:주식, 2:채권
            sell_tp: 매도수구분 (필수) — 0:전체, 1:매도, 2:매수
            stk_cd: 종목코드 — M04020000: 금 99.99_1kg, M04020100: 미니금 99.99_100g, 전체 조회는
                빈값('')으로 설정
            fr_ord_no: 시작주문번호 — 시작주문번호 입력 시 이전 주문은 조회되지 않음, 전체 조회는
                빈값('')으로 설정
            dmst_stex_tp: 국내거래소구분 (필수) —
                %:(전체),KRX:한국거래소,NXT:넥스트트레이드,SOR:최선주문집행
        """
        ...

    def gold_spot_order_execution_all(
        self,
        cont_yn: str = "N",
        next_key: str = "",
        *,
        ord_dt: str = ...,
        qry_tp: str = ...,
        mrkt_deal_tp: str = ...,
        stk_bond_tp: str = ...,
        slby_tp: str = ...,
        stk_cd: str = ...,
        fr_ord_no: str = ...,
        dmst_stex_tp: str = ...,
        **kwargs: Any,
    ) -> ResponseT:
        """금현물 주문체결전체조회 (Gold Spot All Order Execution)

        api_id ``kt50030`` · 금현물 주문체결전체조회 · ``POST /api/dostk/acnt``

        Args:
            ord_dt: 주문일자 (필수) — YYYYMMDD
            qry_tp: 조회구분 — 1: 주문순, 2: 역순
            mrkt_deal_tp: 시장구분 (필수) — 5:KRX금현물, 5값으로 고정
            stk_bond_tp: 주식채권구분 (필수) — 0:전체, 1:주식, 2:채권
            slby_tp: 매도수구분 (필수) — 0:전체, 1:매도, 2:매수
            stk_cd: 종목코드 — M04020000: 금 99.99_1kg, M04020100: 미니금 99.99_100g, 전체 조회는
                빈값('')으로 설정
            fr_ord_no: 시작주문번호 — 시작주문번호 입력 시 이전 주문은 조회되지 않음, 전체 조회는
                빈값('')으로 설정
            dmst_stex_tp: 국내거래소구분 — %:(전체), KRX, NXT, SOR
        """
        ...

    def gold_spot_transaction_history(
        self,
        cont_yn: str = "N",
        next_key: str = "",
        *,
        strt_dt: str = ...,
        end_dt: str = ...,
        tp: str = ...,
        stk_cd: str = ...,
        **kwargs: Any,
    ) -> ResponseT:
        """금현물 거래내역조회 (Gold Spot Transaction History)

        api_id ``kt50032`` · 금현물 거래내역조회 · ``POST /api/dostk/acnt``

        Args:
            strt_dt: 시작일자 — YYYYMMDD
            end_dt: 종료일자 — YYYYMMDD
            tp: 구분 — 0:전체, 1:입출금, 2:출고, 3:매매, 4:매수, 5:매도, 6:입금, 7:출금
            stk_cd: 종목코드 — M04020000: 금 99.99_1kg, M04020100: 미니금 99.99_100g, 전체 조회는
                빈값('')으로 설정
        """
        ...

    def gold_spot_unfilled_orders(
        self,
        cont_yn: str = "N",
        next_key: str = "",
        *,
        ord_dt: str = ...,
        qry_tp: str = ...,
        mrkt_deal_tp: str = ...,
        stk_bond_tp: str = ...,
        sell_tp: str = ...,
        stk_cd: str = ...,
        fr_ord_no: str = ...,
        dmst_stex_tp: str = ...,
        **kwargs: Any,
    ) -> ResponseT:
        """금현물 미체결조회 (Gold Spot Unfilled Orders)

        api_id ``kt50075`` · 금현물 미체결조회 · ``POST /api/dostk/acnt``

        Args:
            ord_dt: 주문일자 (필수) — YYYYMMDD
            qry_tp: 조회구분 — 1: 주문순, 2: 역순
            mrkt_deal_tp: 시장구분 (필수) — 5:KRW금현물, 5값으로 고정
            stk_bond_tp: 주식채권구분 (필수) — 0:전체, 1:주식, 2:채권
            sell_tp: 매도수구분 (필수) — 0:전체, 1:매도, 2:매수
            stk_cd: 종목코드 — M04020000: 금 99.99_1kg, M04020100: 미니금 99.99_100g, 전체 조회는
                빈값('')으로 설정
            fr_ord_no: 시작주문번호 — 시작주문번호 입력 시 이전 주문은 조회되지 않음, 전체 조회는
                빈값('')으로 설정
            dmst_stex_tp: 국내거래소구분 — %:(전체), KRX, NXT, SOR
        """
        ...

    def margin_detail(
        self,
        cont_yn: str = "N",
        next_key: str = "",
        **kwargs: Any,
    ) -> ResponseT:
        """증거금세부내역조회요청 (Margin Detail Inquiry)

        api_id ``kt00013`` · 증거금세부내역조회요청 · ``POST /api/dostk/acnt``
        """
        ...

    def next_day_settlement(
        self,
        cont_yn: str = "N",
        next_key: str = "",
        *,
        strt_dcd_seq: str = ...,
        **kwargs: Any,
    ) -> ResponseT:
        """계좌별익일결제예정내역요청 (Next Day Settlement Schedule)

        api_id ``kt00008`` · 계좌별익일결제예정내역요청 · ``POST /api/dostk/acnt``

        Args:
            strt_dcd_seq: 시작결제번호
        """
        ...

    def order_execution_detail(
        self,
        cont_yn: str = "N",
        next_key: str = "",
        *,
        ord_dt: str = ...,
        qry_tp: str = ...,
        stk_bond_tp: str = ...,
        sell_tp: str = ...,
        stk_cd: str = ...,
        fr_ord_no: str = ...,
        dmst_stex_tp: str = ...,
        **kwargs: Any,
    ) -> ResponseT:
        """계좌별주문체결내역상세요청 (Account Order Execution Detail)

        api_id ``kt00007`` · 계좌별주문체결내역상세요청 · ``POST /api/dostk/acnt``

        Args:
            ord_dt: 주문일자 — YYYYMMDD
            qry_tp: 조회구분 (필수) — 1:주문순, 2:역순, 3:미체결, 4:체결내역만
            stk_bond_tp: 주식채권구분 (필수) — 0:전체, 1:주식, 2:채권
            sell_tp: 매도수구분 (필수) — 0:전체, 1:매도, 2:매수
            stk_cd: 종목코드 — 전체 종목 조회는 빈값('')으로 설정
            fr_ord_no: 시작주문번호 — 시작주문번호 입력 시 이전 주문은 조회되지 않음, 전체 조회는
                빈값('')으로 설정
            dmst_stex_tp: 국내거래소구분 (필수) —
                %:(전체),KRX:한국거래소,NXT:넥스트트레이드,SOR:최선주문집행
        """
        ...

    def order_execution_status(
        self,
        cont_yn: str = "N",
        next_key: str = "",
        *,
        ord_dt: str = ...,
        stk_bond_tp: str = ...,
        mrkt_tp: str = ...,
        sell_tp: str = ...,
        qry_tp: str = ...,
        stk_cd: str = ...,
        fr_ord_no: str = ...,
        dmst_stex_tp: str = ...,
        **kwargs: Any,
    ) -> ResponseT:
        """계좌별주문체결현황요청 (Account Order Execution Status)

        api_id ``kt00009`` · 계좌별주문체결현황요청 · ``POST /api/dostk/acnt``

        Args:
            ord_dt: 주문일자 — YYYYMMDD
            stk_bond_tp: 주식채권구분 (필수) — 0:전체, 1:주식, 2:채권
            mrkt_tp: 시장구분 (필수) — 0:전체, 1:코스피, 2:코스닥, 3:OTCBB, 4:ECN
            sell_tp: 매도수구분 (필수) — 0:전체, 1:매도, 2:매수
            qry_tp: 조회구분 (필수) — 0:전체, 1:체결
            stk_cd: 종목코드 — 전문 조회할 종목코드
            fr_ord_no: 시작주문번호 — 시작주문번호의 이전 주문은 조회 되지 않으며 약정금액에도 포함
                되지 않음
            dmst_stex_tp: 국내거래소구분 (필수) —
                %:(전체),KRX:한국거래소,NXT:넥스트트레이드,SOR:최선주문집행
        """
        ...

    def orderable_qty_by_credit(
        self,
        cont_yn: str = "N",
        next_key: str = "",
        *,
        stk_cd: str = ...,
        uv: str = ...,
        **kwargs: Any,
    ) -> ResponseT:
        """신용보증금율별주문가능수량조회요청 (Orderable Quantity by Credit Margin Rate)

        api_id ``kt00012`` · 신용보증금율별주문가능수량조회요청 · ``POST /api/dostk/acnt``

        Args:
            stk_cd: 종목번호 (필수) — 종목 코드 입력
            uv: 매수가격 — 단위: 원
        """
        ...

    def orderable_qty_by_margin(
        self,
        cont_yn: str = "N",
        next_key: str = "",
        *,
        stk_cd: str = ...,
        uv: str = ...,
        **kwargs: Any,
    ) -> ResponseT:
        """증거금율별주문가능수량조회요청 (Orderable Quantity by Margin Rate)

        api_id ``kt00011`` · 증거금율별주문가능수량조회요청 · ``POST /api/dostk/acnt``

        Args:
            stk_cd: 종목번호 (필수) — 종목 코드 입력
            uv: 매수가격 — 단위: 원
        """
        ...

    def realized_profit_by_date(
        self,
        cont_yn: str = "N",
        next_key: str = "",
        *,
        stk_cd: str = ...,
        strt_dt: str = ...,
        **kwargs: Any,
    ) -> ResponseT:
        """일자별종목별실현손익요청_일자 (Realized Profit by Date per Stock)

        api_id ``ka10072`` · 일자별종목별실현손익요청_일자 · ``POST /api/dostk/acnt``

        Args:
            stk_cd: 종목코드 — 종목코드 6자리
            strt_dt: 시작일자 (필수) — YYYYMMDD
        """
        ...

    def realized_profit_by_period(
        self,
        cont_yn: str = "N",
        next_key: str = "",
        *,
        stk_cd: str = ...,
        strt_dt: str = ...,
        end_dt: str = ...,
        **kwargs: Any,
    ) -> ResponseT:
        """일자별종목별실현손익요청_기간 (Realized Profit by Period per Stock)

        api_id ``ka10073`` · 일자별종목별실현손익요청_기간 · ``POST /api/dostk/acnt``

        Args:
            stk_cd: 종목코드 — 종목코드 6자리
            strt_dt: 시작일자 (필수) — YYYYMMDD
            end_dt: 종료일자 (필수) — YYYYMMDD
        """
        ...

    def today_account_status(
        self,
        cont_yn: str = "N",
        next_key: str = "",
        **kwargs: Any,
    ) -> ResponseT:
        """계좌별당일현황요청 (Today Account Status by Account)

        api_id ``kt00017`` · 계좌별당일현황요청 · ``POST /api/dostk/acnt``
        """
        ...

    def today_realized_profit_detail(
        self,
        cont_yn: str = "N",
        next_key: str = "",
        *,
        stk_cd: str = ...,
        **kwargs: Any,
    ) -> ResponseT:
        """당일실현손익상세요청 (Today Realized Profit Detail)

        api_id ``ka10077`` · 당일실현손익상세요청 · ``POST /api/dostk/acnt``

        Args:
            stk_cd: 종목코드 (필수) — 종목코드 6자리
        """
        ...

    def today_trading_journal(
        self,
        cont_yn: str = "N",
        next_key: str = "",
        *,
        base_dt: str = ...,
        ottks_tp: str = ...,
        ch_crd_tp: str = ...,
        **kwargs: Any,
    ) -> ResponseT:
        """당일매매일지요청 (Today Trading Journal)

        api_id ``ka10170`` · 당일매매일지요청 · ``POST /api/dostk/acnt``

        Args:
            base_dt: 기준일자 — YYYYMMDD(공백입력시 금일데이터,최근 2개월까지 제공)
            ottks_tp: 단주구분 (필수) — 1:당일매수에 대한 당일매도,2:당일매도 전체
            ch_crd_tp: 현금신용구분 (필수) — 0:전체, 1:현금매매만, 2:신용매매만
        """
        ...

    def unfilled_orders(
        self,
        cont_yn: str = "N",
        next_key: str = "",
        *,
        all_stk_tp: str = ...,
        trde_tp: str = ...,
        stk_cd: str = ...,
        stex_tp: str = ...,
        **kwargs: Any,
    ) -> ResponseT:
        """미체결요청 (Unfilled Orders)

        api_id ``ka10075`` · 미체결요청 · ``POST /api/dostk/acnt``

        Args:
            all_stk_tp: 전체종목구분 (필수) — 0:전체, 1:종목
            trde_tp: 매매구분 (필수) — 0:전체, 1:매도, 2:매수
            stk_cd: 종목코드 — 종목코드 6자리
            stex_tp: 거래소구분 (필수) — 0 : 통합, 1 : KRX, 2 : NXT
        """
        ...

    def unfilled_split_order_detail(
        self,
        cont_yn: str = "N",
        next_key: str = "",
        *,
        ord_no: str = ...,
        **kwargs: Any,
    ) -> ResponseT:
        """미체결 분할주문 상세 (Unfilled Split Order Detail)

        api_id ``ka10088`` · 미체결 분할주문 상세 · ``POST /api/dostk/acnt``

        Args:
            ord_no: 주문번호 (필수) — 주문번호 7자리
        """
        ...

    def withdrawable_amount(
        self,
        cont_yn: str = "N",
        next_key: str = "",
        *,
        io_amt: str = ...,
        stk_cd: str = ...,
        trde_tp: str = ...,
        trde_qty: str = ...,
        uv: str = ...,
        exp_buy_unp: str = ...,
        **kwargs: Any,
    ) -> ResponseT:
        """주문인출가능금액요청 (Withdrawable Order Amount)

        api_id ``kt00010`` · 주문인출가능금액요청 · ``POST /api/dostk/acnt``

        Args:
            io_amt: 입출금액 — 단위: 원
            stk_cd: 종목번호 (필수) — 종목 코드 입력
            trde_tp: 매매구분 (필수) — 1:매도, 2:매수
            trde_qty: 매매수량 — 단위: 1주
            uv: 매수가격 (필수) — 단위: 원
            exp_buy_unp: 예상매수단가 — 단위: 원
        """
        ...
