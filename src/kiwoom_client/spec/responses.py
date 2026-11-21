"""자주 쓰는 TR 의 응답 TypedDict — ``cast`` 해서 IDE 자동완성·mypy 를 받는다.

자동 생성 — 고치지 말 것. ``scripts/build_response_types.py`` 가 TR 카탈로그로 만든다.

엔드포인트 메서드의 반환 타입은 그대로 ``dict[str, Any]`` 다 (응답에 필드가 빠지거나 더해질 수
있어서). 필요한 곳에서만 좁혀 쓴다::

    from typing import cast
    from kiwoom_client.spec.responses import StockDailyChartResponse

    resp = cast(StockDailyChartResponse, api.chart.stock_daily_chart(stk_cd="005930"))
    for bar in resp.get("stk_dt_pole_chart_qry", []):
        bar["cur_prc"]   # str — 숫자는 kiwoom_client.to_number() 로

모든 키는 선택(``total=False``)이고 값은 키움이 보내는 그대로 문자열이다
(``return_code`` 만 정수). 키 이름이 숫자로 시작하는 필드가 있어 함수형 문법을 쓴다.
"""

from __future__ import annotations

from typing import TypedDict

# ka10001 주식기본정보요청 — ``api.stock_info.basic_stock_info()`` 응답.
BasicStockInfoResponse = TypedDict(
    "BasicStockInfoResponse",
    {
        "return_code": int,  # 결과코드 (0 = 정상)
        "return_msg": str,  # 결과메시지
        "stk_cd": str,  # 종목코드
        "stk_nm": str,  # 종목명
        "setl_mm": str,  # 결산월
        "fav": str,  # 액면가
        "cap": str,  # 자본금
        "flo_stk": str,  # 상장주식
        "crd_rt": str,  # 신용비율
        "oyr_hgst": str,  # 연중최고
        "oyr_lwst": str,  # 연중최저
        "mac": str,  # 시가총액
        "mac_wght": str,  # 시가총액비중
        "for_exh_rt": str,  # 외인소진률
        "repl_pric": str,  # 대용가
        "per": str,  # PER
        "eps": str,  # EPS
        "roe": str,  # ROE
        "pbr": str,  # PBR
        "ev": str,  # EV
        "bps": str,  # BPS
        "sale_amt": str,  # 매출액
        "bus_pro": str,  # 영업이익
        "cup_nga": str,  # 당기순이익
        "250hgst": str,  # 250최고
        "250lwst": str,  # 250최저
        "high_pric": str,  # 고가
        "open_pric": str,  # 시가
        "low_pric": str,  # 저가
        "upl_pric": str,  # 상한가
        "lst_pric": str,  # 하한가
        "base_pric": str,  # 기준가
        "exp_cntr_pric": str,  # 예상체결가
        "exp_cntr_qty": str,  # 예상체결수량
        "250hgst_pric_dt": str,  # 250최고가일
        "250hgst_pric_pre_rt": str,  # 250최고가대비율
        "250lwst_pric_dt": str,  # 250최저가일
        "250lwst_pric_pre_rt": str,  # 250최저가대비율
        "cur_prc": str,  # 현재가
        "pre_sig": str,  # 대비기호
        "pred_pre": str,  # 전일대비
        "flu_rt": str,  # 등락율
        "trde_qty": str,  # 거래량
        "trde_pre": str,  # 거래대비
        "fav_unit": str,  # 액면가단위
        "dstr_stk": str,  # 유통주식
        "dstr_rt": str,  # 유통비율
    },
    total=False,
)


class StockQuoteResponse(TypedDict, total=False):
    """ka10004 주식호가요청 — ``api.market.stock_quote()`` 응답."""

    return_code: int
    """결과코드 (0 = 정상)"""
    return_msg: str
    """결과메시지"""
    bid_req_base_tm: str
    """호가잔량기준시간"""
    sel_10th_pre_req_pre: str
    """매도10차선잔량대비"""
    sel_10th_pre_req: str
    """매도10차선잔량"""
    sel_10th_pre_bid: str
    """매도10차선호가"""
    sel_9th_pre_req_pre: str
    """매도9차선잔량대비"""
    sel_9th_pre_req: str
    """매도9차선잔량"""
    sel_9th_pre_bid: str
    """매도9차선호가"""
    sel_8th_pre_req_pre: str
    """매도8차선잔량대비"""
    sel_8th_pre_req: str
    """매도8차선잔량"""
    sel_8th_pre_bid: str
    """매도8차선호가"""
    sel_7th_pre_req_pre: str
    """매도7차선잔량대비"""
    sel_7th_pre_req: str
    """매도7차선잔량"""
    sel_7th_pre_bid: str
    """매도7차선호가"""
    sel_6th_pre_req_pre: str
    """매도6차선잔량대비"""
    sel_6th_pre_req: str
    """매도6차선잔량"""
    sel_6th_pre_bid: str
    """매도6차선호가"""
    sel_5th_pre_req_pre: str
    """매도5차선잔량대비"""
    sel_5th_pre_req: str
    """매도5차선잔량"""
    sel_5th_pre_bid: str
    """매도5차선호가"""
    sel_4th_pre_req_pre: str
    """매도4차선잔량대비"""
    sel_4th_pre_req: str
    """매도4차선잔량"""
    sel_4th_pre_bid: str
    """매도4차선호가"""
    sel_3th_pre_req_pre: str
    """매도3차선잔량대비"""
    sel_3th_pre_req: str
    """매도3차선잔량"""
    sel_3th_pre_bid: str
    """매도3차선호가"""
    sel_2th_pre_req_pre: str
    """매도2차선잔량대비"""
    sel_2th_pre_req: str
    """매도2차선잔량"""
    sel_2th_pre_bid: str
    """매도2차선호가"""
    sel_1th_pre_req_pre: str
    """매도1차선잔량대비"""
    sel_fpr_req: str
    """매도최우선잔량"""
    sel_fpr_bid: str
    """매도최우선호가"""
    buy_fpr_bid: str
    """매수최우선호가"""
    buy_fpr_req: str
    """매수최우선잔량"""
    buy_1th_pre_req_pre: str
    """매수1차선잔량대비"""
    buy_2th_pre_bid: str
    """매수2차선호가"""
    buy_2th_pre_req: str
    """매수2차선잔량"""
    buy_2th_pre_req_pre: str
    """매수2차선잔량대비"""
    buy_3th_pre_bid: str
    """매수3차선호가"""
    buy_3th_pre_req: str
    """매수3차선잔량"""
    buy_3th_pre_req_pre: str
    """매수3차선잔량대비"""
    buy_4th_pre_bid: str
    """매수4차선호가"""
    buy_4th_pre_req: str
    """매수4차선잔량"""
    buy_4th_pre_req_pre: str
    """매수4차선잔량대비"""
    buy_5th_pre_bid: str
    """매수5차선호가"""
    buy_5th_pre_req: str
    """매수5차선잔량"""
    buy_5th_pre_req_pre: str
    """매수5차선잔량대비"""
    buy_6th_pre_bid: str
    """매수6차선호가"""
    buy_6th_pre_req: str
    """매수6차선잔량"""
    buy_6th_pre_req_pre: str
    """매수6차선잔량대비"""
    buy_7th_pre_bid: str
    """매수7차선호가"""
    buy_7th_pre_req: str
    """매수7차선잔량"""
    buy_7th_pre_req_pre: str
    """매수7차선잔량대비"""
    buy_8th_pre_bid: str
    """매수8차선호가"""
    buy_8th_pre_req: str
    """매수8차선잔량"""
    buy_8th_pre_req_pre: str
    """매수8차선잔량대비"""
    buy_9th_pre_bid: str
    """매수9차선호가"""
    buy_9th_pre_req: str
    """매수9차선잔량"""
    buy_9th_pre_req_pre: str
    """매수9차선잔량대비"""
    buy_10th_pre_bid: str
    """매수10차선호가"""
    buy_10th_pre_req: str
    """매수10차선잔량"""
    buy_10th_pre_req_pre: str
    """매수10차선잔량대비"""
    tot_sel_req_jub_pre: str
    """총매도잔량직전대비"""
    tot_sel_req: str
    """총매도잔량"""
    tot_buy_req: str
    """총매수잔량"""
    tot_buy_req_jub_pre: str
    """총매수잔량직전대비"""
    ovt_sel_req_pre: str
    """시간외매도잔량대비"""
    ovt_sel_req: str
    """시간외매도잔량"""
    ovt_buy_req: str
    """시간외매수잔량"""
    ovt_buy_req_pre: str
    """시간외매수잔량대비"""


class StockMinuteChartItem(TypedDict, total=False):
    """ka10080 주식분봉차트조회요청 — ``stk_min_pole_chart_qry`` 목록의 한 줄."""

    cur_prc: str
    """현재가(종가)"""
    trde_qty: str
    """거래량"""
    cntr_tm: str
    """체결시간"""
    open_pric: str
    """시가"""
    high_pric: str
    """고가"""
    low_pric: str
    """저가"""
    pred_pre: str
    """전일대비"""
    pred_pre_sig: str
    """전일대비 기호"""


class StockMinuteChartResponse(TypedDict, total=False):
    """ka10080 주식분봉차트조회요청 — ``api.chart.stock_minute_chart()`` 응답."""

    return_code: int
    """결과코드 (0 = 정상)"""
    return_msg: str
    """결과메시지"""
    stk_cd: str
    """종목코드"""
    stk_min_pole_chart_qry: list[StockMinuteChartItem]
    """주식분봉차트조회"""


class StockDailyChartItem(TypedDict, total=False):
    """ka10081 주식일봉차트조회요청 — ``stk_dt_pole_chart_qry`` 목록의 한 줄."""

    cur_prc: str
    """현재가"""
    trde_qty: str
    """거래량"""
    trde_prica: str
    """거래대금"""
    dt: str
    """일자"""
    open_pric: str
    """시가"""
    high_pric: str
    """고가"""
    low_pric: str
    """저가"""
    pred_pre: str
    """전일대비"""
    pred_pre_sig: str
    """전일대비기호"""
    trde_tern_rt: str
    """거래회전율"""


class StockDailyChartResponse(TypedDict, total=False):
    """ka10081 주식일봉차트조회요청 — ``api.chart.stock_daily_chart()`` 응답."""

    return_code: int
    """결과코드 (0 = 정상)"""
    return_msg: str
    """결과메시지"""
    stk_cd: str
    """종목코드"""
    stk_dt_pole_chart_qry: list[StockDailyChartItem]
    """주식일봉차트조회"""


class TopVolumeTodayItem(TypedDict, total=False):
    """ka10030 당일거래량상위요청 — ``tdy_trde_qty_upper`` 목록의 한 줄."""

    stk_cd: str
    """종목코드"""
    stk_nm: str
    """종목명"""
    cur_prc: str
    """현재가"""
    pred_pre_sig: str
    """전일대비기호"""
    pred_pre: str
    """전일대비"""
    flu_rt: str
    """등락률"""
    trde_qty: str
    """거래량"""
    pred_rt: str
    """전일비"""
    trde_tern_rt: str
    """거래회전율"""
    trde_amt: str
    """거래금액"""
    opmr_trde_qty: str
    """장중거래량"""
    opmr_pred_rt: str
    """장중전일비"""
    opmr_trde_rt: str
    """장중거래회전율"""
    opmr_trde_amt: str
    """장중거래금액"""
    af_mkrt_trde_qty: str
    """장후거래량"""
    af_mkrt_pred_rt: str
    """장후전일비"""
    af_mkrt_trde_rt: str
    """장후거래회전율"""
    af_mkrt_trde_amt: str
    """장후거래금액"""
    bf_mkrt_trde_qty: str
    """장전거래량"""
    bf_mkrt_pred_rt: str
    """장전전일비"""
    bf_mkrt_trde_rt: str
    """장전거래회전율"""
    bf_mkrt_trde_amt: str
    """장전거래금액"""


class TopVolumeTodayResponse(TypedDict, total=False):
    """ka10030 당일거래량상위요청 — ``api.ranking.top_volume_today()`` 응답."""

    return_code: int
    """결과코드 (0 = 정상)"""
    return_msg: str
    """결과메시지"""
    tdy_trde_qty_upper: list[TopVolumeTodayItem]
    """당일거래량상위"""


class DepositDetailItem(TypedDict, total=False):
    """kt00001 예수금상세현황요청 — ``stk_entr_prst`` 목록의 한 줄."""

    crnc_cd: str
    """통화코드"""
    fx_entr: str
    """외화예수금"""
    fc_krw_repl_evlta: str
    """원화대용평가금"""
    fc_trst_profa: str
    """해외주식증거금"""
    pymn_alow_amt: str
    """출금가능금액"""
    pymn_alow_amt_entr: str
    """출금가능금액(예수금)"""
    ord_alow_amt_entr: str
    """주문가능금액(예수금)"""
    fc_uncla: str
    """외화미수(합계)"""
    fc_ch_uncla: str
    """외화현금미수금"""
    dly_amt: str
    """연체료"""
    d1_fx_entr: str
    """d+1외화예수금"""
    d2_fx_entr: str
    """d+2외화예수금"""
    d3_fx_entr: str
    """d+3외화예수금"""
    d4_fx_entr: str
    """d+4외화예수금"""


# kt00001 예수금상세현황요청 — ``api.account.deposit_detail()`` 응답.
DepositDetailResponse = TypedDict(
    "DepositDetailResponse",
    {
        "return_code": int,  # 결과코드 (0 = 정상)
        "return_msg": str,  # 결과메시지
        "entr": str,  # 예수금
        "profa_ch": str,  # 주식증거금현금
        "bncr_profa_ch": str,  # 수익증권증거금현금
        "nxdy_bncr_sell_exct": str,  # 익일수익증권매도정산대금
        "fc_stk_krw_repl_set_amt": str,  # 해외주식원화대용설정금
        "crd_grnta_ch": str,  # 신용보증금현금
        "crd_grnt_ch": str,  # 신용담보금현금
        "add_grnt_ch": str,  # 추가담보금현금
        "etc_profa": str,  # 기타증거금
        "uncl_stk_amt": str,  # 미수확보금
        "shrts_prica": str,  # 공매도대금
        "crd_set_grnta": str,  # 신용설정평가금
        "chck_ina_amt": str,  # 수표입금액
        "etc_chck_ina_amt": str,  # 기타수표입금액
        "crd_grnt_ruse": str,  # 신용담보재사용
        "knx_asset_evltv": str,  # 코넥스기본예탁금
        "elwdpst_evlta": str,  # ELW예탁평가금
        "crd_ls_rght_frcs_amt": str,  # 신용대주권리예정금액
        "lvlh_join_amt": str,  # 생계형가입금액
        "lvlh_trns_alowa": str,  # 생계형입금가능금액
        "repl_amt": str,  # 대용금평가금액(합계)
        "remn_repl_evlta": str,  # 잔고대용평가금액
        "trst_remn_repl_evlta": str,  # 위탁대용잔고평가금액
        "bncr_remn_repl_evlta": str,  # 수익증권대용평가금액
        "profa_repl": str,  # 위탁증거금대용
        "crd_grnta_repl": str,  # 신용보증금대용
        "crd_grnt_repl": str,  # 신용담보금대용
        "add_grnt_repl": str,  # 추가담보금대용
        "rght_repl_amt": str,  # 권리대용금
        "pymn_alow_amt": str,  # 출금가능금액
        "wrap_pymn_alow_amt": str,  # 랩출금가능금액
        "ord_alow_amt": str,  # 주문가능금액
        "bncr_buy_alowa": str,  # 수익증권매수가능금액
        "20stk_ord_alow_amt": str,  # 20%종목주문가능금액
        "30stk_ord_alow_amt": str,  # 30%종목주문가능금액
        "40stk_ord_alow_amt": str,  # 40%종목주문가능금액
        "100stk_ord_alow_amt": str,  # 100%종목주문가능금액
        "ch_uncla": str,  # 현금미수금
        "ch_uncla_dlfe": str,  # 현금미수연체료
        "ch_uncla_tot": str,  # 현금미수금합계
        "crd_int_npay": str,  # 신용이자미납
        "int_npay_amt_dlfe": str,  # 신용이자미납연체료
        "int_npay_amt_tot": str,  # 신용이자미납합계
        "etc_loana": str,  # 기타대여금
        "etc_loana_dlfe": str,  # 기타대여금연체료
        "etc_loan_tot": str,  # 기타대여금합계
        "nrpy_loan": str,  # 미상환융자금
        "loan_sum": str,  # 융자금합계
        "ls_sum": str,  # 대주금합계
        "crd_grnt_rt": str,  # 신용담보비율
        "mdstrm_usfe": str,  # 중도이용료
        "min_ord_alow_yn": str,  # 최소주문가능금액
        "loan_remn_evlt_amt": str,  # 대출총평가금액
        "dpst_grntl_remn": str,  # 예탁담보대출잔고
        "sell_grntl_remn": str,  # 매도담보대출잔고
        "d1_entra": str,  # d+1추정예수금
        "d1_slby_exct_amt": str,  # d+1매도매수정산금
        "d1_buy_exct_amt": str,  # d+1매수정산금
        "d1_out_rep_mor": str,  # d+1미수변제소요금
        "d1_sel_exct_amt": str,  # d+1매도정산금
        "d1_pymn_alow_amt": str,  # d+1출금가능금액
        "d2_entra": str,  # d+2추정예수금
        "d2_slby_exct_amt": str,  # d+2매도매수정산금
        "d2_buy_exct_amt": str,  # d+2매수정산금
        "d2_out_rep_mor": str,  # d+2미수변제소요금
        "d2_sel_exct_amt": str,  # d+2매도정산금
        "d2_pymn_alow_amt": str,  # d+2출금가능금액
        "50stk_ord_alow_amt": str,  # 50%종목주문가능금액
        "60stk_ord_alow_amt": str,  # 60%종목주문가능금액
        "stk_entr_prst": list[DepositDetailItem],  # 종목별예수금
    },
    total=False,
)


class AccountEvaluationItem(TypedDict, total=False):
    """kt00004 계좌평가현황요청 — ``stk_acnt_evlt_prst`` 목록의 한 줄."""

    stk_cd: str
    """종목코드"""
    stk_nm: str
    """종목명"""
    rmnd_qty: str
    """보유수량"""
    avg_prc: str
    """평균단가"""
    cur_prc: str
    """현재가"""
    evlt_amt: str
    """평가금액"""
    pl_amt: str
    """손익금액"""
    pl_rt: str
    """손익율"""
    loan_dt: str
    """대출일"""
    pur_amt: str
    """매입금액"""
    setl_remn: str
    """결제잔고"""
    pred_buyq: str
    """전일매수수량"""
    pred_sellq: str
    """전일매도수량"""
    tdy_buyq: str
    """금일매수수량"""
    tdy_sellq: str
    """금일매도수량"""


class AccountEvaluationResponse(TypedDict, total=False):
    """kt00004 계좌평가현황요청 — ``api.account.account_evaluation()`` 응답."""

    return_code: int
    """결과코드 (0 = 정상)"""
    return_msg: str
    """결과메시지"""
    acnt_nm: str
    """계좌명"""
    brch_nm: str
    """지점명"""
    entr: str
    """예수금"""
    d2_entra: str
    """D+2추정예수금"""
    tot_est_amt: str
    """유가잔고평가액"""
    aset_evlt_amt: str
    """예탁자산평가액"""
    tot_pur_amt: str
    """총매입금액"""
    prsm_dpst_aset_amt: str
    """추정예탁자산"""
    tot_grnt_sella: str
    """매도담보대출금"""
    tdy_lspft_amt: str
    """당일투자원금"""
    invt_bsamt: str
    """당월투자원금"""
    lspft_amt: str
    """누적투자원금"""
    tdy_lspft: str
    """당일투자손익"""
    lspft2: str
    """당월투자손익"""
    lspft: str
    """누적투자손익"""
    tdy_lspft_rt: str
    """당일손익율"""
    lspft_ratio: str
    """당월손익율"""
    lspft_rt: str
    """누적손익율"""
    stk_acnt_evlt_prst: list[AccountEvaluationItem]
    """종목별계좌평가현황"""


class EvaluationBalanceDetailItem(TypedDict, total=False):
    """kt00018 계좌평가잔고내역요청 — ``acnt_evlt_remn_indv_tot`` 목록의 한 줄."""

    stk_cd: str
    """종목번호"""
    stk_nm: str
    """종목명"""
    evltv_prft: str
    """평가손익"""
    prft_rt: str
    """수익률(%)"""
    pur_pric: str
    """매입가"""
    pred_close_pric: str
    """전일종가"""
    rmnd_qty: str
    """보유수량"""
    trde_able_qty: str
    """매매가능수량"""
    cur_prc: str
    """현재가"""
    pred_buyq: str
    """전일매수수량"""
    pred_sellq: str
    """전일매도수량"""
    tdy_buyq: str
    """금일매수수량"""
    tdy_sellq: str
    """금일매도수량"""
    pur_amt: str
    """매입금액"""
    pur_cmsn: str
    """매입수수료"""
    evlt_amt: str
    """평가금액"""
    sell_cmsn: str
    """평가수수료"""
    tax: str
    """세금"""
    sum_cmsn: str
    """수수료합"""
    poss_rt: str
    """보유비중(%)"""
    crd_tp: str
    """신용구분"""
    crd_tp_nm: str
    """신용구분명"""
    crd_loan_dt: str
    """대출일"""


class EvaluationBalanceDetailResponse(TypedDict, total=False):
    """kt00018 계좌평가잔고내역요청 — ``api.account.evaluation_balance_detail()`` 응답."""

    return_code: int
    """결과코드 (0 = 정상)"""
    return_msg: str
    """결과메시지"""
    tot_pur_amt: str
    """총매입금액"""
    tot_evlt_amt: str
    """총평가금액"""
    tot_evlt_pl: str
    """총평가손익금액"""
    tot_prft_rt: str
    """총수익률(%)"""
    prsm_dpst_aset_amt: str
    """추정예탁자산"""
    tot_loan_amt: str
    """총대출금"""
    tot_crd_loan_amt: str
    """총융자금액"""
    tot_crd_ls_amt: str
    """총대주금액"""
    acnt_evlt_remn_indv_tot: list[EvaluationBalanceDetailItem]
    """계좌평가잔고개별합산"""


class UnfilledOrdersItem(TypedDict, total=False):
    """ka10075 미체결요청 — ``oso`` 목록의 한 줄."""

    acnt_no: str
    """계좌번호"""
    ord_no: str
    """주문번호"""
    mang_empno: str
    """관리사번"""
    stk_cd: str
    """종목코드"""
    tsk_tp: str
    """업무구분"""
    ord_stt: str
    """주문상태"""
    stk_nm: str
    """종목명"""
    ord_qty: str
    """주문수량"""
    ord_pric: str
    """주문가격"""
    oso_qty: str
    """미체결수량"""
    cntr_tot_amt: str
    """체결누계금액"""
    orig_ord_no: str
    """원주문번호"""
    io_tp_nm: str
    """주문구분"""
    trde_tp: str
    """매매구분"""
    tm: str
    """시간"""
    cntr_no: str
    """체결번호"""
    cntr_pric: str
    """체결가"""
    cntr_qty: str
    """체결량"""
    cur_prc: str
    """현재가"""
    sel_bid: str
    """매도호가"""
    buy_bid: str
    """매수호가"""
    unit_cntr_pric: str
    """단위체결가"""
    unit_cntr_qty: str
    """단위체결량"""
    tdy_trde_cmsn: str
    """당일매매수수료"""
    tdy_trde_tax: str
    """당일매매세금"""
    ind_invsr: str
    """개인투자자"""
    stex_tp: str
    """거래소구분"""
    stex_tp_txt: str
    """거래소구분텍스트"""
    sor_yn: str
    """SOR 여부값"""
    stop_pric: str
    """스톱가"""


class UnfilledOrdersResponse(TypedDict, total=False):
    """ka10075 미체결요청 — ``api.account.unfilled_orders()`` 응답."""

    return_code: int
    """결과코드 (0 = 정상)"""
    return_msg: str
    """결과메시지"""
    oso: list[UnfilledOrdersItem]
    """미체결"""


class BuyOrderResponse(TypedDict, total=False):
    """kt10000 주식 매수주문 — ``api.order.buy_order()`` 응답."""

    return_code: int
    """결과코드 (0 = 정상)"""
    return_msg: str
    """결과메시지"""
    ord_no: str
    """주문번호"""
    dmst_stex_tp: str
    """국내거래소구분"""


__all__ = [
    "AccountEvaluationItem",
    "AccountEvaluationResponse",
    "BasicStockInfoResponse",
    "BuyOrderResponse",
    "DepositDetailItem",
    "DepositDetailResponse",
    "EvaluationBalanceDetailItem",
    "EvaluationBalanceDetailResponse",
    "StockDailyChartItem",
    "StockDailyChartResponse",
    "StockMinuteChartItem",
    "StockMinuteChartResponse",
    "StockQuoteResponse",
    "TopVolumeTodayItem",
    "TopVolumeTodayResponse",
    "UnfilledOrdersItem",
    "UnfilledOrdersResponse",
]
