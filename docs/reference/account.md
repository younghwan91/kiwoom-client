<!-- 자동 생성 파일 — 손으로 고치지 마세요. `python scripts/gen_docs.py` 가 TR 카탈로그(kiwoom_client.spec)로 다시 만듭니다. -->

# `api.account` — 계좌 (Account)

요청·응답 필드는 키움 공식 REST API 명세에서 만든 TR 카탈로그([출처·라이선스](https://github.com/younghwan91/kiwoom-client/blob/main/src/kiwoom_client/spec/SOURCE.md))를 그대로 옮긴 것입니다. 뜻이 애매하면 [키움 REST API 포털](https://openapi.kiwoom.com)이 기준입니다. 값은 모두 문자열로 넘깁니다.

공통 헤더(`api-id`·`cont-yn`·`next-key`·`authorization`)는 라이브러리가 채웁니다 — 연속조회는 메서드의 `cont_yn`·`next_key` 인자나 `request_all()` 을 쓰세요.

| api_id | 메서드 | 이름 |
|---|---|---|
| [`ka00001`](#ka00001) | `account_number_inquiry()` | 계좌번호조회 |
| [`ka01690`](#ka01690) | `daily_balance_return_rate()` | 일별잔고수익률 |
| [`ka10072`](#ka10072) | `realized_profit_by_date()` | 일자별종목별실현손익요청_일자 |
| [`ka10073`](#ka10073) | `realized_profit_by_period()` | 일자별종목별실현손익요청_기간 |
| [`ka10074`](#ka10074) | `daily_realized_profit()` | 일자별실현손익요청 |
| [`ka10075`](#ka10075) | `unfilled_orders()` | 미체결요청 |
| [`ka10076`](#ka10076) | `filled_orders()` | 체결요청 |
| [`ka10077`](#ka10077) | `today_realized_profit_detail()` | 당일실현손익상세요청 |
| [`ka10085`](#ka10085) | `account_return_rate()` | 계좌수익률요청 |
| [`ka10088`](#ka10088) | `unfilled_split_order_detail()` | 미체결 분할주문 상세 |
| [`ka10170`](#ka10170) | `today_trading_journal()` | 당일매매일지요청 |
| [`kt00001`](#kt00001) | `deposit_detail()` | 예수금상세현황요청 |
| [`kt00002`](#kt00002) | `daily_estimated_deposit()` | 일별추정예탁자산현황요청 |
| [`kt00003`](#kt00003) | `estimated_asset()` | 추정자산조회요청 |
| [`kt00004`](#kt00004) | `account_evaluation()` | 계좌평가현황요청 |
| [`kt00005`](#kt00005) | `filled_position()` | 체결잔고요청 |
| [`kt00007`](#kt00007) | `order_execution_detail()` | 계좌별주문체결내역상세요청 |
| [`kt00008`](#kt00008) | `next_day_settlement()` | 계좌별익일결제예정내역요청 |
| [`kt00009`](#kt00009) | `order_execution_status()` | 계좌별주문체결현황요청 |
| [`kt00010`](#kt00010) | `withdrawable_amount()` | 주문인출가능금액요청 |
| [`kt00011`](#kt00011) | `orderable_qty_by_margin()` | 증거금율별주문가능수량조회요청 |
| [`kt00012`](#kt00012) | `orderable_qty_by_credit()` | 신용보증금율별주문가능수량조회요청 |
| [`kt00013`](#kt00013) | `margin_detail()` | 증거금세부내역조회요청 |
| [`kt00015`](#kt00015) | `comprehensive_transaction_history()` | 위탁종합거래내역요청 |
| [`kt00016`](#kt00016) | `daily_return_detail()` | 일별계좌수익률상세현황요청 |
| [`kt00017`](#kt00017) | `today_account_status()` | 계좌별당일현황요청 |
| [`kt00018`](#kt00018) | `evaluation_balance_detail()` | 계좌평가잔고내역요청 |
| [`kt50020`](#kt50020) | `gold_spot_balance()` | 금현물 잔고확인 |
| [`kt50021`](#kt50021) | `gold_spot_deposit()` | 금현물 예수금 |
| [`kt50030`](#kt50030) | `gold_spot_order_execution_all()` | 금현물 주문체결전체조회 |
| [`kt50031`](#kt50031) | `gold_spot_order_execution()` | 금현물 주문체결조회 |
| [`kt50032`](#kt50032) | `gold_spot_transaction_history()` | 금현물 거래내역조회 |
| [`kt50075`](#kt50075) | `gold_spot_unfilled_orders()` | 금현물 미체결조회 |

<a id="ka00001"></a>

## `ka00001` · `account_number_inquiry()` — 계좌번호조회

계좌번호조회 (Account Number Inquiry) · `POST /api/dostk/acnt`

```python
api.account.account_number_inquiry()
```

**요청**

요청 필드 없음.

**응답**

| 필드 | 한글명 | 길이 | 설명 |
|---|---|---:|---|
| `acctNo` | 계좌번호 | 20 | 10자리 숫자가 출력됩니다. 뒤에 2자리는 당사에서 계좌를 분류하기 위한 값입니다. |

<a id="ka01690"></a>

## `ka01690` · `daily_balance_return_rate()` — 일별잔고수익률

일별잔고수익률 (Daily Balance Return Rate) · `POST /api/dostk/acnt`

```python
api.account.daily_balance_return_rate(qry_dt=...)
```

**요청**

| 필드 | 한글명 | 필수 | 길이 | 설명 |
|---|---|:---:|---:|---|
| `qry_dt` | 조회일자 | Y | 8 | YYYYMMDD |

**응답**

| 필드 | 한글명 | 길이 | 설명 |
|---|---|---:|---|
| `dt` | 일자 | 20 | YYYYMMDD |
| `tot_buy_amt` | 총 매입가 | 20 | 단위 : 원 |
| `tot_evlt_amt` | 총 평가금액 | 20 | 단위 : 원 |
| `tot_evltv_prft` | 총 평가손익 | 20 | 단위 : 원 |
| `tot_prft_rt` | 수익률 | 20 | 단위: %, 소수점 둘째 자리까지 포맷된 백분율 |
| `dbst_bal` | 예수금 | 20 | 단위 : 원 |
| `day_stk_asst` | 추정자산 | 20 | 단위 : 원 |
| `buy_wght` | 현금비중 | 20 | 단위: %, 소수점 둘째 자리까지 포맷된 백분율 |
| `day_bal_rt` (list) | 일별잔고수익률 |  |   |
| `day_bal_rt[].cur_prc` | 현재가 | 20 | 단위 : 원 |
| `day_bal_rt[].stk_cd` | 종목코드 | 20 |   |
| `day_bal_rt[].stk_nm` | 종목명 | 20 |   |
| `day_bal_rt[].rmnd_qty` | 보유 수량 | 20 | 단위 : 1주 |
| `day_bal_rt[].buy_uv` | 매입 단가 | 20 | 단위 : 원 |
| `day_bal_rt[].buy_wght` | 매수비중 | 20 | 단위: %, 소수점 첫째 자리까지 포맷된 백분율 |
| `day_bal_rt[].evltv_prft` | 평가손익 | 20 | 단위 : 원 |
| `day_bal_rt[].prft_rt` | 수익률 | 20 | 단위: %, 소수점 둘째 자리까지 포맷된 백분율 |
| `day_bal_rt[].evlt_amt` | 평가금액 | 20 | 단위 : 원 |
| `day_bal_rt[].evlt_wght` | 평가비중 | 20 | 단위: %, 소수점 첫째 자리까지 포맷된 백분율 |

<a id="ka10072"></a>

## `ka10072` · `realized_profit_by_date()` — 일자별종목별실현손익요청_일자

일자별종목별실현손익요청_일자 (Realized Profit by Date per Stock) · `POST /api/dostk/acnt`

```python
api.account.realized_profit_by_date(strt_dt=...)
```

**요청**

| 필드 | 한글명 | 필수 | 길이 | 설명 |
|---|---|:---:|---:|---|
| `stk_cd` | 종목코드 |  | 6 | 종목코드 6자리 |
| `strt_dt` | 시작일자 | Y | 8 | YYYYMMDD |

**응답**

| 필드 | 한글명 | 길이 | 설명 |
|---|---|---:|---|
| `dt_stk_div_rlzt_pl` (list) | 일자별종목별실현손익 |  |   |
| `dt_stk_div_rlzt_pl[].stk_nm` | 종목명 | 40 |   |
| `dt_stk_div_rlzt_pl[].cntr_qty` | 체결량 | 20 | 단위: 1주 |
| `dt_stk_div_rlzt_pl[].buy_uv` | 매입단가 | 20 | 단위: 원 |
| `dt_stk_div_rlzt_pl[].cntr_pric` | 체결가 | 20 | 단위: 원 |
| `dt_stk_div_rlzt_pl[].tdy_sel_pl` | 당일매도손익 | 20 | 단위: 원 |
| `dt_stk_div_rlzt_pl[].pl_rt` | 손익율 | 20 | 단위: %, 소수점 둘째 자리까지 포맷된 백분율 |
| `dt_stk_div_rlzt_pl[].stk_cd` | 종목코드 | 20 | 종목코드 6자리 |
| `dt_stk_div_rlzt_pl[].tdy_trde_cmsn` | 당일매매수수료 | 20 | 단위: 원 |
| `dt_stk_div_rlzt_pl[].tdy_trde_tax` | 당일매매세금 | 20 | 단위: 원 |
| `dt_stk_div_rlzt_pl[].wthd_alowa` | 인출가능금액 | 20 | 단위: 원 |
| `dt_stk_div_rlzt_pl[].loan_dt` | 대출일 | 20 | YYYYMMDD |
| `dt_stk_div_rlzt_pl[].crd_tp` | 신용구분 | 20 |   |
| `dt_stk_div_rlzt_pl[].stk_cd_1` | 종목코드1 | 20 |   |
| `dt_stk_div_rlzt_pl[].tdy_sel_pl_1` | 당일매도손익1 | 20 |   |

<a id="ka10073"></a>

## `ka10073` · `realized_profit_by_period()` — 일자별종목별실현손익요청_기간

일자별종목별실현손익요청_기간 (Realized Profit by Period per Stock) · `POST /api/dostk/acnt`

```python
api.account.realized_profit_by_period(strt_dt=..., end_dt=...)
```

**요청**

| 필드 | 한글명 | 필수 | 길이 | 설명 |
|---|---|:---:|---:|---|
| `stk_cd` | 종목코드 |  | 6 | 종목코드 6자리 |
| `strt_dt` | 시작일자 | Y | 8 | YYYYMMDD |
| `end_dt` | 종료일자 | Y | 8 | YYYYMMDD |

**응답**

| 필드 | 한글명 | 길이 | 설명 |
|---|---|---:|---|
| `dt_stk_rlzt_pl` (list) | 일자별종목별실현손익 |  |   |
| `dt_stk_rlzt_pl[].dt` | 일자 | 20 | YYYYMMDD |
| `dt_stk_rlzt_pl[].tdy_htssel_cmsn` | 당일hts매도수수료 | 20 | 단위: 원 |
| `dt_stk_rlzt_pl[].stk_nm` | 종목명 | 40 |   |
| `dt_stk_rlzt_pl[].cntr_qty` | 체결량 | 20 | 단위: 1주 |
| `dt_stk_rlzt_pl[].buy_uv` | 매입단가 | 20 | 단위: 원 |
| `dt_stk_rlzt_pl[].cntr_pric` | 체결가 | 20 | 단위: 원 |
| `dt_stk_rlzt_pl[].tdy_sel_pl` | 당일매도손익 | 20 | 단위: 원 |
| `dt_stk_rlzt_pl[].pl_rt` | 손익율 | 20 | 단위: %, 소수점 둘째 자리까지 포맷된 백분율 |
| `dt_stk_rlzt_pl[].stk_cd` | 종목코드 | 20 | 종목코드 6자리 |
| `dt_stk_rlzt_pl[].tdy_trde_cmsn` | 당일매매수수료 | 20 | 단위: 원 |
| `dt_stk_rlzt_pl[].tdy_trde_tax` | 당일매매세금 | 20 | 단위: 원 |
| `dt_stk_rlzt_pl[].wthd_alowa` | 인출가능금액 | 20 | 단위: 원 |
| `dt_stk_rlzt_pl[].loan_dt` | 대출일 | 20 | YYYYMMDD |
| `dt_stk_rlzt_pl[].crd_tp` | 신용구분 | 20 |   |

<a id="ka10074"></a>

## `ka10074` · `daily_realized_profit()` — 일자별실현손익요청

일별실현손익요청 (Daily Realized Profit) · `POST /api/dostk/acnt`

```python
api.account.daily_realized_profit(strt_dt=..., end_dt=...)
```

**요청**

| 필드 | 한글명 | 필수 | 길이 | 설명 |
|---|---|:---:|---:|---|
| `strt_dt` | 시작일자 | Y | 8 | YYYYMMDD |
| `end_dt` | 종료일자 | Y | 8 | YYYYMMDD |

**응답**

| 필드 | 한글명 | 길이 | 설명 |
|---|---|---:|---|
| `tot_buy_amt` | 총매수금액 |  | 단위: 원 |
| `tot_sell_amt` | 총매도금액 |  | 단위: 원 |
| `rlzt_pl` | 실현손익 |  | 단위: 원 |
| `trde_cmsn` | 매매수수료 |  | 단위: 원 |
| `trde_tax` | 매매세금 |  | 단위: 원 |
| `dt_rlzt_pl` (list) | 일자별실현손익 |  |   |
| `dt_rlzt_pl[].dt` | 일자 | 20 | YYYYMMDD |
| `dt_rlzt_pl[].buy_amt` | 매수금액 | 20 | 단위: 원 |
| `dt_rlzt_pl[].sell_amt` | 매도금액 | 20 | 단위: 원 |
| `dt_rlzt_pl[].tdy_sel_pl` | 당일매도손익 | 20 | 단위: 원 |
| `dt_rlzt_pl[].tdy_trde_cmsn` | 당일매매수수료 | 20 | 단위: 원 |
| `dt_rlzt_pl[].tdy_trde_tax` | 당일매매세금 | 20 | 단위: 원 |

<a id="ka10075"></a>

## `ka10075` · `unfilled_orders()` — 미체결요청

미체결요청 (Unfilled Orders) · `POST /api/dostk/acnt`

```python
api.account.unfilled_orders(all_stk_tp=..., trde_tp=..., stex_tp=...)
```

**요청**

| 필드 | 한글명 | 필수 | 길이 | 설명 |
|---|---|:---:|---:|---|
| `all_stk_tp` | 전체종목구분 | Y | 1 | 0:전체, 1:종목 |
| `trde_tp` | 매매구분 | Y | 1 | 0:전체, 1:매도, 2:매수 |
| `stk_cd` | 종목코드 |  | 6 | 종목코드 6자리 |
| `stex_tp` | 거래소구분 | Y | 1 | 0 : 통합, 1 : KRX, 2 : NXT |

**응답**

| 필드 | 한글명 | 길이 | 설명 |
|---|---|---:|---|
| `oso` (list) | 미체결 |  |   |
| `oso[].acnt_no` | 계좌번호 | 20 | 고유 계좌번호 10자리 숫자 |
| `oso[].ord_no` | 주문번호 | 20 | 고유 주문번호 7자리 숫자 |
| `oso[].mang_empno` | 관리사번 | 20 |   |
| `oso[].stk_cd` | 종목코드 | 20 |   |
| `oso[].tsk_tp` | 업무구분 | 20 |   |
| `oso[].ord_stt` | 주문상태 | 20 |   |
| `oso[].stk_nm` | 종목명 | 40 |   |
| `oso[].ord_qty` | 주문수량 | 20 | 단위: 1주 |
| `oso[].ord_pric` | 주문가격 | 20 | 단위: 원 |
| `oso[].oso_qty` | 미체결수량 | 20 | 단위: 1주 |
| `oso[].cntr_tot_amt` | 체결누계금액 | 20 | 단위: 원 |
| `oso[].orig_ord_no` | 원주문번호 | 20 | 원 주문이 없는 경우 '0000000'으로 출력 |
| `oso[].io_tp_nm` | 주문구분 | 20 |   |
| `oso[].trde_tp` | 매매구분 | 20 |   |
| `oso[].tm` | 시간 | 20 | 주문 시간, HHmmss |
| `oso[].cntr_no` | 체결번호 | 20 |   |
| `oso[].cntr_pric` | 체결가 | 20 | 단위: 원 |
| `oso[].cntr_qty` | 체결량 | 20 | 단위: 1주 |
| `oso[].cur_prc` | 현재가 | 20 |   |
| `oso[].sel_bid` | 매도호가 | 20 | 단위: 원, 현재 첫번째 매도호가 |
| `oso[].buy_bid` | 매수호가 | 20 | 단위: 원, 현재 첫번째 매수호가 |
| `oso[].unit_cntr_pric` | 단위체결가 | 20 | 단위: 원 |
| `oso[].unit_cntr_qty` | 단위체결량 | 20 | 단위: 1주 |
| `oso[].tdy_trde_cmsn` | 당일매매수수료 | 20 | 단위: 원 |
| `oso[].tdy_trde_tax` | 당일매매세금 | 20 | 단위: 원 |
| `oso[].ind_invsr` | 개인투자자 | 20 |   |
| `oso[].stex_tp` | 거래소구분 | 20 | 0 : 통합, 1 : KRX, 2 : NXT |
| `oso[].stex_tp_txt` | 거래소구분텍스트 | 20 | 통합,KRX,NXT |
| `oso[].sor_yn` | SOR 여부값 | 20 | Y,N |
| `oso[].stop_pric` | 스톱가 | 20 | 스톱지정가주문 스톱가 |

<a id="ka10076"></a>

## `ka10076` · `filled_orders()` — 체결요청

체결요청 (Filled Orders History) · `POST /api/dostk/acnt`

```python
api.account.filled_orders(qry_tp=..., sell_tp=..., stex_tp=...)
```

**요청**

| 필드 | 한글명 | 필수 | 길이 | 설명 |
|---|---|:---:|---:|---|
| `stk_cd` | 종목코드 |  | 6 | 종목코드 6자리 |
| `qry_tp` | 조회구분 | Y | 1 | 0:전체, 1:종목 |
| `sell_tp` | 매도수구분 | Y | 1 | 0:전체, 1:매도, 2:매수 |
| `ord_no` | 주문번호 |  | 10 | 검색 기준 값으로 입력한 주문번호 보다 과거에 체결된 내역이 조회됩니다. |
| `stex_tp` | 거래소구분 | Y | 1 | 0 : 통합, 1 : KRX, 2 : NXT |

**응답**

| 필드 | 한글명 | 길이 | 설명 |
|---|---|---:|---|
| `cntr` (list) | 체결 |  |   |
| `cntr[].ord_no` | 주문번호 | 20 | 주문번호 7자리 |
| `cntr[].stk_nm` | 종목명 | 40 |   |
| `cntr[].io_tp_nm` | 주문구분 | 20 |   |
| `cntr[].ord_pric` | 주문가격 | 20 | 단위: 원 |
| `cntr[].ord_qty` | 주문수량 | 20 | 단위: 1주 |
| `cntr[].cntr_pric` | 체결가 | 20 | 단위: 원 |
| `cntr[].cntr_qty` | 체결량 | 20 | 단위: 1주 |
| `cntr[].oso_qty` | 미체결수량 | 20 | 단위: 1주 |
| `cntr[].tdy_trde_cmsn` | 당일매매수수료 | 20 | 단위: 원 |
| `cntr[].tdy_trde_tax` | 당일매매세금 | 20 | 단위: 원 |
| `cntr[].ord_stt` | 주문상태 | 20 |   |
| `cntr[].trde_tp` | 매매구분 | 20 |   |
| `cntr[].orig_ord_no` | 원주문번호 | 20 | 원 주문이 없는 경우 '0000000'으로 출력 |
| `cntr[].ord_tm` | 주문시간 | 20 | HHmmss |
| `cntr[].stk_cd` | 종목코드 | 20 | 종목코드 6자리 |
| `cntr[].stex_tp` | 거래소구분 | 20 | 0 : 통합, 1 : KRX, 2 : NXT |
| `cntr[].stex_tp_txt` | 거래소구분텍스트 | 20 | 통합,KRX,NXT |
| `cntr[].sor_yn` | SOR 여부값 | 20 | Y,N |
| `cntr[].stop_pric` | 스톱가 | 20 | 스톱지정가주문 스톱가 |

<a id="ka10077"></a>

## `ka10077` · `today_realized_profit_detail()` — 당일실현손익상세요청

당일실현손익상세요청 (Today Realized Profit Detail) · `POST /api/dostk/acnt`

```python
api.account.today_realized_profit_detail(stk_cd=...)
```

**요청**

| 필드 | 한글명 | 필수 | 길이 | 설명 |
|---|---|:---:|---:|---|
| `stk_cd` | 종목코드 | Y | 6 | 종목코드 6자리 |

**응답**

| 필드 | 한글명 | 길이 | 설명 |
|---|---|---:|---|
| `tdy_rlzt_pl` | 당일실현손익 |  | 단위: 원 |
| `tdy_rlzt_pl_dtl` (list) | 당일실현손익상세 |  |   |
| `tdy_rlzt_pl_dtl[].stk_nm` | 종목명 | 40 |   |
| `tdy_rlzt_pl_dtl[].cntr_qty` | 체결량 | 20 | 단위: 1주 |
| `tdy_rlzt_pl_dtl[].buy_uv` | 매입단가 | 20 | 단위: 원 |
| `tdy_rlzt_pl_dtl[].cntr_pric` | 체결가 | 20 | 단위: 원 |
| `tdy_rlzt_pl_dtl[].tdy_sel_pl` | 당일매도손익 | 20 | 단위: 원 |
| `tdy_rlzt_pl_dtl[].pl_rt` | 손익율 | 20 | 단위: %, 소수점 둘째 자리까지 포맷된 백분율 |
| `tdy_rlzt_pl_dtl[].tdy_trde_cmsn` | 당일매매수수료 | 20 | 단위: 원 |
| `tdy_rlzt_pl_dtl[].tdy_trde_tax` | 당일매매세금 | 20 | 단위: 원 |
| `tdy_rlzt_pl_dtl[].stk_cd` | 종목코드 | 20 |   |

<a id="ka10085"></a>

## `ka10085` · `account_return_rate()` — 계좌수익률요청

계좌수익률요청 (Account Return Rate) · `POST /api/dostk/acnt`

```python
api.account.account_return_rate(stex_tp=...)
```

**요청**

| 필드 | 한글명 | 필수 | 길이 | 설명 |
|---|---|:---:|---:|---|
| `stex_tp` | 거래소구분 | Y | 1 | 0 : 통합, 1 : KRX, 2 : NXT |

**응답**

| 필드 | 한글명 | 길이 | 설명 |
|---|---|---:|---|
| `acnt_prft_rt` (list) | 계좌수익률 |  |   |
| `acnt_prft_rt[].dt` | 일자 | 20 | YYYYMMDD |
| `acnt_prft_rt[].stk_cd` | 종목코드 | 20 |   |
| `acnt_prft_rt[].stk_nm` | 종목명 | 40 |   |
| `acnt_prft_rt[].cur_prc` | 현재가 | 20 | 단위: 원 |
| `acnt_prft_rt[].pur_pric` | 매입가 | 20 | 단위: 원 |
| `acnt_prft_rt[].pur_amt` | 매입금액 | 20 | 단위: 원 |
| `acnt_prft_rt[].rmnd_qty` | 보유수량 | 20 | 단위: 1주 |
| `acnt_prft_rt[].tdy_sel_pl` | 당일매도손익 | 20 | 단위: 원 |
| `acnt_prft_rt[].tdy_trde_cmsn` | 당일매매수수료 | 20 | 단위: 원 |
| `acnt_prft_rt[].tdy_trde_tax` | 당일매매세금 | 20 | 단위: 원 |
| `acnt_prft_rt[].crd_tp` | 신용구분 | 20 |   |
| `acnt_prft_rt[].loan_dt` | 대출일 | 20 | YYYYMMDD, 대출일이 없는 경우 '00000000'로 출력 |
| `acnt_prft_rt[].setl_remn` | 결제잔고 | 20 | 단위: 원 |
| `acnt_prft_rt[].clrn_alow_qty` | 청산가능수량 | 20 | 단위: 1주 |
| `acnt_prft_rt[].crd_amt` | 신용금액 | 20 | 단위: 원 |
| `acnt_prft_rt[].crd_int` | 신용이자 | 20 | 단위: 원 |
| `acnt_prft_rt[].expr_dt` | 만기일 | 20 | YYYYMMDD, 만기일이 없는 경우 '00000000'로 출력 |

<a id="ka10088"></a>

## `ka10088` · `unfilled_split_order_detail()` — 미체결 분할주문 상세

미체결 분할주문 상세 (Unfilled Split Order Detail) · `POST /api/dostk/acnt`

```python
api.account.unfilled_split_order_detail(ord_no=...)
```

**요청**

| 필드 | 한글명 | 필수 | 길이 | 설명 |
|---|---|:---:|---:|---|
| `ord_no` | 주문번호 | Y | 20 | 주문번호 7자리 |

**응답**

| 필드 | 한글명 | 길이 | 설명 |
|---|---|---:|---|
| `osop` (list) | 미체결분할주문리스트 |  |   |
| `osop[].stk_cd` | 종목코드 | 20 |   |
| `osop[].stk_nm` | 종목명 | 40 |   |
| `osop[].ord_no` | 주문번호 | 20 | 주문번호 7자리 |
| `osop[].ord_qty` | 주문수량 | 20 | 단위: 1주 |
| `osop[].ord_pric` | 주문가격 | 20 | 단위: 원 |
| `osop[].osop_qty` | 미체결수량 | 20 | 단위: 1주 |
| `osop[].io_tp_nm` | 주문구분 | 20 |   |
| `osop[].trde_tp` | 매매구분 | 20 |   |
| `osop[].sell_tp` | 매도/수 구분 | 20 |   |
| `osop[].cntr_qty` | 체결량 | 20 | 단위: 1주 |
| `osop[].ord_stt` | 주문상태 | 20 |   |
| `osop[].cur_prc` | 현재가 | 20 | 단위: 원 |
| `osop[].stex_tp` | 거래소구분 | 20 | 0 : 통합, 1 : KRX, 2 : NXT |
| `osop[].stex_tp_txt` | 거래소구분텍스트 | 20 | 통합,KRX,NXT |

<a id="ka10170"></a>

## `ka10170` · `today_trading_journal()` — 당일매매일지요청

당일매매일지요청 (Today Trading Journal) · `POST /api/dostk/acnt`

```python
api.account.today_trading_journal(ottks_tp=..., ch_crd_tp=...)
```

**요청**

| 필드 | 한글명 | 필수 | 길이 | 설명 |
|---|---|:---:|---:|---|
| `base_dt` | 기준일자 |  | 8 | YYYYMMDD(공백입력시 금일데이터,최근 2개월까지 제공) |
| `ottks_tp` | 단주구분 | Y | 1 | 1:당일매수에 대한 당일매도,2:당일매도 전체 |
| `ch_crd_tp` | 현금신용구분 | Y | 1 | 0:전체, 1:현금매매만, 2:신용매매만 |

**응답**

| 필드 | 한글명 | 길이 | 설명 |
|---|---|---:|---|
| `tot_sell_amt` | 총매도금액 |  | 단위: 원 |
| `tot_buy_amt` | 총매수금액 |  | 단위: 원 |
| `tot_cmsn_tax` | 총수수료_세금 |  | 단위: 원 |
| `tot_exct_amt` | 총정산금액 |  | 단위: 원 |
| `tot_pl_amt` | 총손익금액 |  | 단위: 원 |
| `tot_prft_rt` | 총수익률 |  | 단위: %, 소수점 둘째 자리까지 포맷된 백분율 |
| `tdy_trde_diary` (list) | 당일매매일지 |  |   |
| `tdy_trde_diary[].stk_nm` | 종목명 | 40 |   |
| `tdy_trde_diary[].buy_avg_pric` | 매수평균가 |  | 단위: 원 |
| `tdy_trde_diary[].buy_qty` | 매수수량 |  | 단위: 1주 |
| `tdy_trde_diary[].sel_avg_pric` | 매도평균가 |  | 단위: 원 |
| `tdy_trde_diary[].sell_qty` | 매도수량 |  | 단위: 1주 |
| `tdy_trde_diary[].cmsn_alm_tax` | 수수료_제세금 |  | 단위: 원 |
| `tdy_trde_diary[].pl_amt` | 손익금액 |  | 단위: 원 |
| `tdy_trde_diary[].sell_amt` | 매도금액 |  | 단위: 원 |
| `tdy_trde_diary[].buy_amt` | 매수금액 |  | 단위: 원 |
| `tdy_trde_diary[].prft_rt` | 수익률 |  | 단위: %, 소수점 둘째 자리까지 포맷된 백분율 |
| `tdy_trde_diary[].stk_cd` | 종목코드 | 6 |   |

<a id="kt00001"></a>

## `kt00001` · `deposit_detail()` — 예수금상세현황요청

예수금상세현황요청 (Deposit Detail Status) · `POST /api/dostk/acnt`

```python
api.account.deposit_detail(qry_tp=...)
```

**요청**

| 필드 | 한글명 | 필수 | 길이 | 설명 |
|---|---|:---:|---:|---|
| `qry_tp` | 조회구분 | Y | 1 | 3:추정조회, 2:일반조회 |

**응답**

| 필드 | 한글명 | 길이 | 설명 |
|---|---|---:|---|
| `entr` | 예수금 | 15 | 단위: 원, 좌측 0-padding 처리된 부호 포함 15자리 숫자 |
| `profa_ch` | 주식증거금현금 | 15 | 단위: 원, 좌측 0-padding 처리된 부호 포함 15자리 숫자 |
| `bncr_profa_ch` | 수익증권증거금현금 | 15 | 단위: 원, 좌측 0-padding 처리된 부호 포함 15자리 숫자 |
| `nxdy_bncr_sell_exct` | 익일수익증권매도정산대금 | 15 | 단위: 원, 좌측 0-padding 처리된 부호 포함 15자리 숫자 |
| `fc_stk_krw_repl_set_amt` | 해외주식원화대용설정금 | 15 | 단위: 원, 좌측 0-padding 처리된 부호 포함 15자리 숫자 |
| `crd_grnta_ch` | 신용보증금현금 | 15 | 단위: 원, 좌측 0-padding 처리된 부호 포함 15자리 숫자 |
| `crd_grnt_ch` | 신용담보금현금 | 15 | 단위: 원, 좌측 0-padding 처리된 부호 포함 15자리 숫자 |
| `add_grnt_ch` | 추가담보금현금 | 15 | 단위: 원, 좌측 0-padding 처리된 부호 포함 15자리 숫자 |
| `etc_profa` | 기타증거금 | 15 | 단위: 원, 좌측 0-padding 처리된 부호 포함 15자리 숫자 |
| `uncl_stk_amt` | 미수확보금 | 15 | 단위: 원, 좌측 0-padding 처리된 부호 포함 15자리 숫자 |
| `shrts_prica` | 공매도대금 | 15 | 단위: 원, 좌측 0-padding 처리된 부호 포함 15자리 숫자 |
| `crd_set_grnta` | 신용설정평가금 | 15 | 단위: 원, 좌측 0-padding 처리된 부호 포함 15자리 숫자 |
| `chck_ina_amt` | 수표입금액 | 15 | 단위: 원, 좌측 0-padding 처리된 부호 포함 15자리 숫자 |
| `etc_chck_ina_amt` | 기타수표입금액 | 15 | 단위: 원, 좌측 0-padding 처리된 부호 포함 15자리 숫자 |
| `crd_grnt_ruse` | 신용담보재사용 | 15 | 단위: 원, 좌측 0-padding 처리된 부호 포함 15자리 숫자 |
| `knx_asset_evltv` | 코넥스기본예탁금 | 15 | 단위: 원, 좌측 0-padding 처리된 부호 포함 15자리 숫자 |
| `elwdpst_evlta` | ELW예탁평가금 | 15 | 단위: 원, 좌측 0-padding 처리된 부호 포함 15자리 숫자 |
| `crd_ls_rght_frcs_amt` | 신용대주권리예정금액 | 15 | 단위: 원, 좌측 0-padding 처리된 부호 포함 15자리 숫자 |
| `lvlh_join_amt` | 생계형가입금액 | 15 | 단위: 원, 좌측 0-padding 처리된 부호 포함 15자리 숫자 |
| `lvlh_trns_alowa` | 생계형입금가능금액 | 15 | 단위: 원, 좌측 0-padding 처리된 부호 포함 15자리 숫자 |
| `repl_amt` | 대용금평가금액(합계) | 15 | 단위: 원, 좌측 0-padding 처리된 부호 포함 15자리 숫자 |
| `remn_repl_evlta` | 잔고대용평가금액 | 15 | 단위: 원, 좌측 0-padding 처리된 부호 포함 15자리 숫자 |
| `trst_remn_repl_evlta` | 위탁대용잔고평가금액 | 15 | 단위: 원, 좌측 0-padding 처리된 부호 포함 15자리 숫자 |
| `bncr_remn_repl_evlta` | 수익증권대용평가금액 | 15 | 단위: 원, 좌측 0-padding 처리된 부호 포함 15자리 숫자 |
| `profa_repl` | 위탁증거금대용 | 15 | 단위: 원, 좌측 0-padding 처리된 부호 포함 15자리 숫자 |
| `crd_grnta_repl` | 신용보증금대용 | 15 | 단위: 원, 좌측 0-padding 처리된 부호 포함 15자리 숫자 |
| `crd_grnt_repl` | 신용담보금대용 | 15 | 단위: 원, 좌측 0-padding 처리된 부호 포함 15자리 숫자 |
| `add_grnt_repl` | 추가담보금대용 | 15 | 단위: 원, 좌측 0-padding 처리된 부호 포함 15자리 숫자 |
| `rght_repl_amt` | 권리대용금 | 15 | 단위: 원, 좌측 0-padding 처리된 부호 포함 15자리 숫자 |
| `pymn_alow_amt` | 출금가능금액 | 15 | 단위: 원, 좌측 0-padding 처리된 부호 포함 15자리 숫자 |
| `wrap_pymn_alow_amt` | 랩출금가능금액 | 15 | 단위: 원, 좌측 0-padding 처리된 부호 포함 15자리 숫자 |
| `ord_alow_amt` | 주문가능금액 | 15 | 단위: 원, 좌측 0-padding 처리된 부호 포함 15자리 숫자 |
| `bncr_buy_alowa` | 수익증권매수가능금액 | 15 | 단위: 원, 좌측 0-padding 처리된 부호 포함 15자리 숫자 |
| `20stk_ord_alow_amt` | 20%종목주문가능금액 | 15 | 단위: 원, 좌측 0-padding 처리된 부호 포함 15자리 숫자 |
| `30stk_ord_alow_amt` | 30%종목주문가능금액 | 15 | 단위: 원, 좌측 0-padding 처리된 부호 포함 15자리 숫자 |
| `40stk_ord_alow_amt` | 40%종목주문가능금액 | 15 | 단위: 원, 좌측 0-padding 처리된 부호 포함 15자리 숫자 |
| `100stk_ord_alow_amt` | 100%종목주문가능금액 | 15 | 단위: 원, 좌측 0-padding 처리된 부호 포함 15자리 숫자 |
| `ch_uncla` | 현금미수금 | 15 | 단위: 원, 좌측 0-padding 처리된 부호 포함 15자리 숫자 |
| `ch_uncla_dlfe` | 현금미수연체료 | 15 | 단위: 원, 좌측 0-padding 처리된 부호 포함 15자리 숫자 |
| `ch_uncla_tot` | 현금미수금합계 | 15 | 단위: 원, 좌측 0-padding 처리된 부호 포함 15자리 숫자 |
| `crd_int_npay` | 신용이자미납 | 15 | 단위: 원, 좌측 0-padding 처리된 부호 포함 15자리 숫자 |
| `int_npay_amt_dlfe` | 신용이자미납연체료 | 15 | 단위: 원, 좌측 0-padding 처리된 부호 포함 15자리 숫자 |
| `int_npay_amt_tot` | 신용이자미납합계 | 15 | 단위: 원, 좌측 0-padding 처리된 부호 포함 15자리 숫자 |
| `etc_loana` | 기타대여금 | 15 | 단위: 원, 좌측 0-padding 처리된 부호 포함 15자리 숫자 |
| `etc_loana_dlfe` | 기타대여금연체료 | 15 | 단위: 원, 좌측 0-padding 처리된 부호 포함 15자리 숫자 |
| `etc_loan_tot` | 기타대여금합계 | 15 | 단위: 원, 좌측 0-padding 처리된 부호 포함 15자리 숫자 |
| `nrpy_loan` | 미상환융자금 | 15 | 단위: 원, 좌측 0-padding 처리된 부호 포함 15자리 숫자 |
| `loan_sum` | 융자금합계 | 15 | 단위: 원, 좌측 0-padding 처리된 부호 포함 15자리 숫자 |
| `ls_sum` | 대주금합계 | 15 | 단위: 원, 좌측 0-padding 처리된 부호 포함 15자리 숫자 |
| `crd_grnt_rt` | 신용담보비율 | 15 | 단위: %, 소수점 둘째 자리까지 포맷된 백분율 |
| `mdstrm_usfe` | 중도이용료 | 15 | 단위: 원, 좌측 0-padding 처리된 부호 포함 15자리 숫자 |
| `min_ord_alow_yn` | 최소주문가능금액 | 15 | 단위: 원, 좌측 0-padding 처리된 부호 포함 15자리 숫자 |
| `loan_remn_evlt_amt` | 대출총평가금액 | 15 | 단위: 원, 좌측 0-padding 처리된 부호 포함 15자리 숫자 |
| `dpst_grntl_remn` | 예탁담보대출잔고 | 15 | 단위: 원, 좌측 0-padding 처리된 부호 포함 15자리 숫자 |
| `sell_grntl_remn` | 매도담보대출잔고 | 15 | 단위: 원, 좌측 0-padding 처리된 부호 포함 15자리 숫자 |
| `d1_entra` | d+1추정예수금 | 15 | 단위: 원, 좌측 0-padding 처리된 부호 포함 15자리 숫자 |
| `d1_slby_exct_amt` | d+1매도매수정산금 | 15 | 단위: 원, 좌측 0-padding 처리된 부호 포함 15자리 숫자 |
| `d1_buy_exct_amt` | d+1매수정산금 | 15 | 단위: 원, 좌측 0-padding 처리된 부호 포함 15자리 숫자 |
| `d1_out_rep_mor` | d+1미수변제소요금 | 15 | 단위: 원, 좌측 0-padding 처리된 부호 포함 15자리 숫자 |
| `d1_sel_exct_amt` | d+1매도정산금 | 15 | 단위: 원, 좌측 0-padding 처리된 부호 포함 15자리 숫자 |
| `d1_pymn_alow_amt` | d+1출금가능금액 | 15 | 단위: 원, 좌측 0-padding 처리된 부호 포함 15자리 숫자 |
| `d2_entra` | d+2추정예수금 | 15 | 단위: 원, 좌측 0-padding 처리된 부호 포함 15자리 숫자 |
| `d2_slby_exct_amt` | d+2매도매수정산금 | 15 | 단위: 원, 좌측 0-padding 처리된 부호 포함 15자리 숫자 |
| `d2_buy_exct_amt` | d+2매수정산금 | 15 | 단위: 원, 좌측 0-padding 처리된 부호 포함 15자리 숫자 |
| `d2_out_rep_mor` | d+2미수변제소요금 | 15 | 단위: 원, 좌측 0-padding 처리된 부호 포함 15자리 숫자 |
| `d2_sel_exct_amt` | d+2매도정산금 | 15 | 단위: 원, 좌측 0-padding 처리된 부호 포함 15자리 숫자 |
| `d2_pymn_alow_amt` | d+2출금가능금액 | 15 | 단위: 원, 좌측 0-padding 처리된 부호 포함 15자리 숫자 |
| `50stk_ord_alow_amt` | 50%종목주문가능금액 | 15 | 단위: 원, 좌측 0-padding 처리된 부호 포함 15자리 숫자 |
| `60stk_ord_alow_amt` | 60%종목주문가능금액 | 15 | 단위: 원, 좌측 0-padding 처리된 부호 포함 15자리 숫자 |
| `stk_entr_prst` (list) | 종목별예수금 |  |   |
| `stk_entr_prst[].crnc_cd` | 통화코드 | 3 | 통화코드 3자리 |
| `stk_entr_prst[].fx_entr` | 외화예수금 | 15 | 단위: 원, 좌측 0-padding 처리된 부호 포함 15자리 숫자 |
| `stk_entr_prst[].fc_krw_repl_evlta` | 원화대용평가금 | 15 | 단위: 원, 좌측 0-padding 처리된 부호 포함 15자리 숫자 |
| `stk_entr_prst[].fc_trst_profa` | 해외주식증거금 | 15 | 단위: 원, 좌측 0-padding 처리된 부호 포함 15자리 숫자 |
| `stk_entr_prst[].pymn_alow_amt` | 출금가능금액 | 15 | 단위: 원, 좌측 0-padding 처리된 부호 포함 15자리 숫자 |
| `stk_entr_prst[].pymn_alow_amt_entr` | 출금가능금액(예수금) | 15 | 단위: 원, 좌측 0-padding 처리된 부호 포함 15자리 숫자 |
| `stk_entr_prst[].ord_alow_amt_entr` | 주문가능금액(예수금) | 15 | 단위: 원, 좌측 0-padding 처리된 부호 포함 15자리 숫자 |
| `stk_entr_prst[].fc_uncla` | 외화미수(합계) | 15 | 단위: 원, 좌측 0-padding 처리된 부호 포함 15자리 숫자 |
| `stk_entr_prst[].fc_ch_uncla` | 외화현금미수금 | 15 | 단위: 원, 좌측 0-padding 처리된 부호 포함 15자리 숫자 |
| `stk_entr_prst[].dly_amt` | 연체료 | 15 | 단위: 원, 좌측 0-padding 처리된 부호 포함 15자리 숫자 |
| `stk_entr_prst[].d1_fx_entr` | d+1외화예수금 | 15 | 단위: 원, 좌측 0-padding 처리된 부호 포함 15자리 숫자 |
| `stk_entr_prst[].d2_fx_entr` | d+2외화예수금 | 15 | 단위: 원, 좌측 0-padding 처리된 부호 포함 15자리 숫자 |
| `stk_entr_prst[].d3_fx_entr` | d+3외화예수금 | 15 | 단위: 원, 좌측 0-padding 처리된 부호 포함 15자리 숫자 |
| `stk_entr_prst[].d4_fx_entr` | d+4외화예수금 | 15 | 단위: 원, 좌측 0-padding 처리된 부호 포함 15자리 숫자 |

<a id="kt00002"></a>

## `kt00002` · `daily_estimated_deposit()` — 일별추정예탁자산현황요청

일별추정예탁자산현황요청 (Daily Estimated Deposit Asset Status) · `POST /api/dostk/acnt`

```python
api.account.daily_estimated_deposit(start_dt=..., end_dt=...)
```

**요청**

| 필드 | 한글명 | 필수 | 길이 | 설명 |
|---|---|:---:|---:|---|
| `start_dt` | 시작조회기간 | Y | 8 | YYYYMMDD |
| `end_dt` | 종료조회기간 | Y | 8 | YYYYMMDD |

**응답**

| 필드 | 한글명 | 길이 | 설명 |
|---|---|---:|---|
| `daly_prsm_dpst_aset_amt_prst` (list) | 일별추정예탁자산현황 |  |   |
| `daly_prsm_dpst_aset_amt_prst[].dt` | 일자 | 8 | YYYYMMDD |
| `daly_prsm_dpst_aset_amt_prst[].entr` | 예수금 | 12 | 단위: 원, 좌측 0-padding 처리된 부호 포함 12자리 숫자 |
| `daly_prsm_dpst_aset_amt_prst[].grnt_use_amt` | 담보대출금 | 12 | 단위: 원, 좌측 0-padding 처리된 부호 포함 12자리 숫자 |
| `daly_prsm_dpst_aset_amt_prst[].crd_loan` | 신용융자금 | 12 | 단위: 원, 좌측 0-padding 처리된 부호 포함 12자리 숫자 |
| `daly_prsm_dpst_aset_amt_prst[].ls_grnt` | 대주담보금 | 12 | 단위: 원, 좌측 0-padding 처리된 부호 포함 12자리 숫자 |
| `daly_prsm_dpst_aset_amt_prst[].repl_amt` | 대용금 | 12 | 단위: 원, 좌측 0-padding 처리된 부호 포함 12자리 숫자 |
| `daly_prsm_dpst_aset_amt_prst[].prsm_dpst_aset_amt` | 추정예탁자산 | 12 | 단위: 원, 좌측 0-padding 처리된 부호 포함 12자리 숫자 |
| `daly_prsm_dpst_aset_amt_prst[].prsm_dpst_aset_amt_bncr_skip` | 추정예탁자산수익증권제외 | 12 | 단위: 원, 좌측 0-padding 처리된 부호 포함 12자리 숫자 |

<a id="kt00003"></a>

## `kt00003` · `estimated_asset()` — 추정자산조회요청

추정자산조회요청 (Estimated Asset Inquiry) · `POST /api/dostk/acnt`

```python
api.account.estimated_asset(qry_tp=...)
```

**요청**

| 필드 | 한글명 | 필수 | 길이 | 설명 |
|---|---|:---:|---:|---|
| `qry_tp` | 상장폐지조회구분 | Y | 1 | 0:전체, 1:상장폐지종목제외 |

**응답**

| 필드 | 한글명 | 길이 | 설명 |
|---|---|---:|---|
| `prsm_dpst_aset_amt` | 추정예탁자산 | 12 | 단위: 원, 좌측 0-padding 처리된 부호 포함 12자리 숫자 |

<a id="kt00004"></a>

## `kt00004` · `account_evaluation()` — 계좌평가현황요청

계좌평가현황요청 (Account Evaluation Status) · `POST /api/dostk/acnt`

```python
api.account.account_evaluation(qry_tp=..., dmst_stex_tp=...)
```

**요청**

| 필드 | 한글명 | 필수 | 길이 | 설명 |
|---|---|:---:|---:|---|
| `qry_tp` | 상장폐지조회구분 | Y | 1 | 0:전체, 1:상장폐지종목제외 |
| `dmst_stex_tp` | 국내거래소구분 | Y | 6 | KRX:한국거래소,NXT:넥스트트레이드 |

**응답**

| 필드 | 한글명 | 길이 | 설명 |
|---|---|---:|---|
| `acnt_nm` | 계좌명 | 30 |   |
| `brch_nm` | 지점명 | 30 |   |
| `entr` | 예수금 | 12 | 단위: 원, 좌측 0-padding 처리된 부호 포함 12자리 숫자 |
| `d2_entra` | D+2추정예수금 | 12 | 단위: 원, 좌측 0-padding 처리된 부호 포함 12자리 숫자 |
| `tot_est_amt` | 유가잔고평가액 | 12 | 단위: 원, 좌측 0-padding 처리된 부호 포함 12자리 숫자 |
| `aset_evlt_amt` | 예탁자산평가액 | 12 | 단위: 원, 좌측 0-padding 처리된 부호 포함 12자리 숫자 |
| `tot_pur_amt` | 총매입금액 | 12 | 단위: 원, 좌측 0-padding 처리된 부호 포함 12자리 숫자 |
| `prsm_dpst_aset_amt` | 추정예탁자산 | 12 | 단위: 원, 좌측 0-padding 처리된 부호 포함 12자리 숫자 |
| `tot_grnt_sella` | 매도담보대출금 | 12 | 단위: 원, 좌측 0-padding 처리된 부호 포함 12자리 숫자 |
| `tdy_lspft_amt` | 당일투자원금 | 12 | 단위: 원, 좌측 0-padding 처리된 부호 포함 12자리 숫자 |
| `invt_bsamt` | 당월투자원금 | 12 | 단위: 원, 좌측 0-padding 처리된 부호 포함 12자리 숫자 |
| `lspft_amt` | 누적투자원금 | 12 | 단위: 원, 좌측 0-padding 처리된 부호 포함 12자리 숫자 |
| `tdy_lspft` | 당일투자손익 | 12 | 단위: 원, 좌측 0-padding 처리된 부호 포함 12자리 숫자 |
| `lspft2` | 당월투자손익 | 12 | 단위: 원, 좌측 0-padding 처리된 부호 포함 12자리 숫자 |
| `lspft` | 누적투자손익 | 12 | 단위: 원, 좌측 0-padding 처리된 부호 포함 12자리 숫자 |
| `tdy_lspft_rt` | 당일손익율 | 12 | 단위: %, 소수점 둘째 자리까지 포맷된 백분율 |
| `lspft_ratio` | 당월손익율 | 12 | 단위: %, 소수점 둘째 자리까지 포맷된 백분율 |
| `lspft_rt` | 누적손익율 | 12 | 단위: %, 소수점 둘째 자리까지 포맷된 백분율 |
| `stk_acnt_evlt_prst` (list) | 종목별계좌평가현황 |  |   |
| `stk_acnt_evlt_prst[].stk_cd` | 종목코드 | 12 | 접두어 1자리 + 종목코드 6자리, 접두어(A: 주식 / J: ELW / Q: ETN) |
| `stk_acnt_evlt_prst[].stk_nm` | 종목명 | 30 |   |
| `stk_acnt_evlt_prst[].rmnd_qty` | 보유수량 | 12 | 단위: 1주, 좌측 0-padding 처리된 부호 포함 12자리 숫자 |
| `stk_acnt_evlt_prst[].avg_prc` | 평균단가 | 12 | 단위: 원, 좌측 0-padding 처리된 부호 포함 12자리 숫자 |
| `stk_acnt_evlt_prst[].cur_prc` | 현재가 | 12 | 단위: 원, 좌측 0-padding 처리된 부호 포함 12자리 숫자 |
| `stk_acnt_evlt_prst[].evlt_amt` | 평가금액 | 12 | 단위: 원, 좌측 0-padding 처리된 부호 포함 12자리 숫자 |
| `stk_acnt_evlt_prst[].pl_amt` | 손익금액 | 12 | 단위: 원, 좌측 0-padding 처리된 부호 포함 12자리 숫자 |
| `stk_acnt_evlt_prst[].pl_rt` | 손익율 | 12 | 단위: %, 소수점 넷째 자리까지 포맷된 백분율 |
| `stk_acnt_evlt_prst[].loan_dt` | 대출일 | 10 | YYYYMMDD |
| `stk_acnt_evlt_prst[].pur_amt` | 매입금액 | 12 | 단위: 원, 좌측 0-padding 처리된 부호 포함 12자리 숫자 |
| `stk_acnt_evlt_prst[].setl_remn` | 결제잔고 | 12 | 단위: 1주, 좌측 0-padding 처리된 부호 포함 12자리 숫자 |
| `stk_acnt_evlt_prst[].pred_buyq` | 전일매수수량 | 12 | 단위: 1주, 좌측 0-padding 처리된 부호 포함 12자리 숫자 |
| `stk_acnt_evlt_prst[].pred_sellq` | 전일매도수량 | 12 | 단위: 1주, 좌측 0-padding 처리된 부호 포함 12자리 숫자 |
| `stk_acnt_evlt_prst[].tdy_buyq` | 금일매수수량 | 12 | 단위: 1주, 좌측 0-padding 처리된 부호 포함 12자리 숫자 |
| `stk_acnt_evlt_prst[].tdy_sellq` | 금일매도수량 | 12 | 단위: 1주, 좌측 0-padding 처리된 부호 포함 12자리 숫자 |

<a id="kt00005"></a>

## `kt00005` · `filled_position()` — 체결잔고요청

체결잔고요청 (Filled Position Balance) · `POST /api/dostk/acnt`

```python
api.account.filled_position(dmst_stex_tp=...)
```

**요청**

| 필드 | 한글명 | 필수 | 길이 | 설명 |
|---|---|:---:|---:|---|
| `dmst_stex_tp` | 국내거래소구분 | Y | 6 | KRX:한국거래소,NXT:넥스트트레이드 |

**응답**

| 필드 | 한글명 | 길이 | 설명 |
|---|---|---:|---|
| `entr` | 예수금 | 12 | 단위: 원, 좌측 0-padding 처리된 부호 포함 12자리 숫자 |
| `entr_d1` | 예수금D+1 | 12 | 단위: 원, 좌측 0-padding 처리된 부호 포함 12자리 숫자 |
| `entr_d2` | 예수금D+2 | 12 | 단위: 원, 좌측 0-padding 처리된 부호 포함 12자리 숫자 |
| `pymn_alow_amt` | 출금가능금액 | 12 | 단위: 원, 좌측 0-padding 처리된 부호 포함 12자리 숫자 |
| `uncl_stk_amt` | 미수확보금 | 12 | 단위: 원, 좌측 0-padding 처리된 부호 포함 12자리 숫자 |
| `repl_amt` | 대용금 | 12 | 단위: 원, 좌측 0-padding 처리된 부호 포함 12자리 숫자 |
| `rght_repl_amt` | 권리대용금 | 12 | 단위: 원, 좌측 0-padding 처리된 부호 포함 12자리 숫자 |
| `ord_alowa` | 주문가능현금 | 12 | 단위: 원, 좌측 0-padding 처리된 부호 포함 12자리 숫자 |
| `ch_uncla` | 현금미수금 | 12 | 단위: 원, 좌측 0-padding 처리된 부호 포함 12자리 숫자 |
| `crd_int_npay_gold` | 신용이자미납금 | 12 | 단위: 원, 좌측 0-padding 처리된 부호 포함 12자리 숫자 |
| `etc_loana` | 기타대여금 | 12 | 단위: 원, 좌측 0-padding 처리된 부호 포함 12자리 숫자 |
| `nrpy_loan` | 미상환융자금 | 12 | 단위: 원, 좌측 0-padding 처리된 부호 포함 12자리 숫자 |
| `profa_ch` | 증거금현금 | 12 | 단위: 원, 좌측 0-padding 처리된 부호 포함 12자리 숫자 |
| `repl_profa` | 증거금대용 | 12 | 단위: 원, 좌측 0-padding 처리된 부호 포함 12자리 숫자 |
| `stk_buy_tot_amt` | 주식매수총액 | 12 | 단위: 원, 좌측 0-padding 처리된 부호 포함 12자리 숫자 |
| `evlt_amt_tot` | 평가금액합계 | 12 | 단위: 원, 좌측 0-padding 처리된 부호 포함 12자리 숫자 |
| `tot_pl_tot` | 총손익합계 | 12 | 단위: 원, 좌측 0-padding 처리된 부호 포함 12자리 숫자 |
| `tot_pl_rt` | 총손익률 | 12 | 단위: %, 소수점 넷째 자리까지 포맷된 백분율 |
| `tot_re_buy_alowa` | 총재매수가능금액 | 12 | 단위: 원, 좌측 0-padding 처리된 부호 포함 12자리 숫자 |
| `20ord_alow_amt` | 20%주문가능금액 | 12 | 단위: 원, 좌측 0-padding 처리된 부호 포함 12자리 숫자 |
| `30ord_alow_amt` | 30%주문가능금액 | 12 | 단위: 원, 좌측 0-padding 처리된 부호 포함 12자리 숫자 |
| `40ord_alow_amt` | 40%주문가능금액 | 12 | 단위: 원, 좌측 0-padding 처리된 부호 포함 12자리 숫자 |
| `50ord_alow_amt` | 50%주문가능금액 | 12 | 단위: 원, 좌측 0-padding 처리된 부호 포함 12자리 숫자 |
| `60ord_alow_amt` | 60%주문가능금액 | 12 | 단위: 원, 좌측 0-padding 처리된 부호 포함 12자리 숫자 |
| `100ord_alow_amt` | 100%주문가능금액 | 12 | 단위: 원, 좌측 0-padding 처리된 부호 포함 12자리 숫자 |
| `crd_loan_tot` | 신용융자합계 | 12 | 단위: 원, 좌측 0-padding 처리된 부호 포함 12자리 숫자 |
| `crd_loan_ls_tot` | 신용융자대주합계 | 12 | 단위: 원, 좌측 0-padding 처리된 부호 포함 12자리 숫자 |
| `crd_grnt_rt` | 신용담보비율 | 12 | 단위: %, 소수점 둘째 자리까지 포맷된 백분율 |
| `dpst_grnt_use_amt_amt` | 예탁담보대출금액 | 12 | 단위: 원, 좌측 0-padding 처리된 부호 포함 12자리 숫자 |
| `grnt_loan_amt` | 매도담보대출금액 | 12 | 단위: 원, 좌측 0-padding 처리된 부호 포함 12자리 숫자 |
| `stk_cntr_remn` (list) | 종목별체결잔고 |  |   |
| `stk_cntr_remn[].crd_tp` | 신용구분 | 2 |   |
| `stk_cntr_remn[].loan_dt` | 대출일 | 8 | YYYMMDD |
| `stk_cntr_remn[].expr_dt` | 만기일 | 8 | YYYMMDD |
| `stk_cntr_remn[].stk_cd` | 종목번호 | 12 | 접두어 1자리 + 종목코드 6자리, 접두어(A: 주식 / J: ELW / Q: ETN) |
| `stk_cntr_remn[].stk_nm` | 종목명 | 30 |   |
| `stk_cntr_remn[].setl_remn` | 결제잔고 | 12 | 단위: 1주, 좌측 0-padding 처리된 부호 포함 12자리 숫자 |
| `stk_cntr_remn[].cur_qty` | 현재잔고 | 12 | 단위: 1주, 좌측 0-padding 처리된 부호 포함 12자리 숫자 |
| `stk_cntr_remn[].cur_prc` | 현재가 | 12 | 단위: 원, 좌측 0-padding 처리된 부호 포함 12자리 숫자 |
| `stk_cntr_remn[].buy_uv` | 매입단가 | 12 | 단위: 원, 좌측 0-padding 처리된 부호 포함 12자리 숫자 |
| `stk_cntr_remn[].pur_amt` | 매입금액 | 12 | 단위: 원, 좌측 0-padding 처리된 부호 포함 12자리 숫자 |
| `stk_cntr_remn[].evlt_amt` | 평가금액 | 12 | 단위: 원, 좌측 0-padding 처리된 부호 포함 12자리 숫자 |
| `stk_cntr_remn[].evltv_prft` | 평가손익 | 12 | 단위: 원, 좌측 0-padding 처리된 부호 포함 12자리 숫자 |
| `stk_cntr_remn[].pl_rt` | 손익률 | 12 | 단위: %, 소수점 넷째 자리까지 포맷된 백분율 |

<a id="kt00007"></a>

## `kt00007` · `order_execution_detail()` — 계좌별주문체결내역상세요청

계좌별주문체결내역상세요청 (Account Order Execution Detail) · `POST /api/dostk/acnt`

```python
api.account.order_execution_detail(qry_tp=..., stk_bond_tp=..., sell_tp=..., dmst_stex_tp=...)
```

**요청**

| 필드 | 한글명 | 필수 | 길이 | 설명 |
|---|---|:---:|---:|---|
| `ord_dt` | 주문일자 |  | 8 | YYYYMMDD |
| `qry_tp` | 조회구분 | Y | 1 | 1:주문순, 2:역순, 3:미체결, 4:체결내역만 |
| `stk_bond_tp` | 주식채권구분 | Y | 1 | 0:전체, 1:주식, 2:채권 |
| `sell_tp` | 매도수구분 | Y | 1 | 0:전체, 1:매도, 2:매수 |
| `stk_cd` | 종목코드 |  | 12 | 전체 종목 조회는 빈값('')으로 설정 |
| `fr_ord_no` | 시작주문번호 |  | 7 | 시작주문번호 입력 시 이전 주문은 조회되지 않음, 전체 조회는 빈값('')으로 설정 |
| `dmst_stex_tp` | 국내거래소구분 | Y | 6 | %:(전체),KRX:한국거래소,NXT:넥스트트레이드,SOR:최선주문집행 |

**응답**

| 필드 | 한글명 | 길이 | 설명 |
|---|---|---:|---|
| `acnt_ord_cntr_prps_dtl` (list) | 계좌별주문체결내역상세 |  |   |
| `acnt_ord_cntr_prps_dtl[].ord_no` | 주문번호 | 7 | 고유 주문번호 7자리 |
| `acnt_ord_cntr_prps_dtl[].stk_cd` | 종목번호 | 12 | 접두어 1자리 + 종목코드 6자리, 접두어(A: 주식 / J: ELW / Q: ETN) |
| `acnt_ord_cntr_prps_dtl[].trde_tp` | 매매구분 | 20 |   |
| `acnt_ord_cntr_prps_dtl[].crd_tp` | 신용구분 | 20 |   |
| `acnt_ord_cntr_prps_dtl[].ord_qty` | 주문수량 | 10 | 단위: 1주, 좌측 0-padding 처리된 부호 포함 10자리 숫자 |
| `acnt_ord_cntr_prps_dtl[].ord_uv` | 주문단가 | 10 | 단위: 원, 좌측 0-padding 처리된 부호 포함 10자리 숫자 |
| `acnt_ord_cntr_prps_dtl[].cnfm_qty` | 확인수량 | 10 | 단위: 1주, 좌측 0-padding 처리된 부호 포함 10자리 숫자 |
| `acnt_ord_cntr_prps_dtl[].acpt_tp` | 접수구분 | 20 |   |
| `acnt_ord_cntr_prps_dtl[].rsrv_tp` | 반대여부 | 20 |   |
| `acnt_ord_cntr_prps_dtl[].ord_tm` | 주문시간 | 8 | HH:mm:ss |
| `acnt_ord_cntr_prps_dtl[].ori_ord` | 원주문 | 7 |   |
| `acnt_ord_cntr_prps_dtl[].stk_nm` | 종목명 | 40 |   |
| `acnt_ord_cntr_prps_dtl[].io_tp_nm` | 주문구분 | 20 |   |
| `acnt_ord_cntr_prps_dtl[].loan_dt` | 대출일 | 8 | YYYYMMDD |
| `acnt_ord_cntr_prps_dtl[].cntr_qty` | 체결수량 | 10 | 단위: 1주, 좌측 0-padding 처리된 부호 포함 10자리 숫자 |
| `acnt_ord_cntr_prps_dtl[].cntr_uv` | 체결단가 | 10 | 단위: 원, 좌측 0-padding 처리된 부호 포함 10자리 숫자 |
| `acnt_ord_cntr_prps_dtl[].ord_remnq` | 주문잔량 | 10 | 단위: 1주, 좌측 0-padding 처리된 부호 포함 10자리 숫자 |
| `acnt_ord_cntr_prps_dtl[].comm_ord_tp` | 통신구분 | 20 |   |
| `acnt_ord_cntr_prps_dtl[].mdfy_cncl` | 정정취소 | 20 |   |
| `acnt_ord_cntr_prps_dtl[].cnfm_tm` | 확인시간 | 8 | HH:mm:ss |
| `acnt_ord_cntr_prps_dtl[].dmst_stex_tp` | 국내거래소구분 | 8 |   |
| `acnt_ord_cntr_prps_dtl[].cond_uv` | 스톱가 | 10 | 단위: 원, 좌측 0-padding 처리된 부호 포함 10자리 숫자 |

<a id="kt00008"></a>

## `kt00008` · `next_day_settlement()` — 계좌별익일결제예정내역요청

계좌별익일결제예정내역요청 (Next Day Settlement Schedule) · `POST /api/dostk/acnt`

```python
api.account.next_day_settlement()
```

**요청**

| 필드 | 한글명 | 필수 | 길이 | 설명 |
|---|---|:---:|---:|---|
| `strt_dcd_seq` | 시작결제번호 |  | 7 |   |

**응답**

| 필드 | 한글명 | 길이 | 설명 |
|---|---|---:|---|
| `trde_dt` | 매매일자 | 8 | YYYYMMDD |
| `setl_dt` | 결제일자 | 8 | YYYYMMDD |
| `sell_amt_sum` | 매도정산합 | 12 | 단위: 원, 좌측 0-padding 처리된 부호 포함 12자리 숫자 |
| `buy_amt_sum` | 매수정산합 | 12 | 단위: 원, 좌측 0-padding 처리된 부호 포함 12자리 숫자 |
| `acnt_nxdy_setl_frcs_prps_array` (list) | 계좌별익일결제예정내역배열 |  |   |
| `acnt_nxdy_setl_frcs_prps_array[].seq` | 일련번호 | 7 | 7자리 숫자 |
| `acnt_nxdy_setl_frcs_prps_array[].stk_cd` | 종목번호 | 12 | 접두어 1자리 + 종목코드 6자리, 접두어(A: 주식 / J: ELW / Q: ETN) |
| `acnt_nxdy_setl_frcs_prps_array[].loan_dt` | 대출일 | 8 |   |
| `acnt_nxdy_setl_frcs_prps_array[].qty` | 수량 | 12 | 단위: 1주, 좌측 0-padding 처리된 부호 포함 12자리 숫자 |
| `acnt_nxdy_setl_frcs_prps_array[].engg_amt` | 약정금액 | 12 | 단위: 원, 좌측 0-padding 처리된 부호 포함 12자리 숫자 |
| `acnt_nxdy_setl_frcs_prps_array[].cmsn` | 수수료 | 12 | 단위: 원, 좌측 0-padding 처리된 부호 포함 12자리 숫자 |
| `acnt_nxdy_setl_frcs_prps_array[].incm_tax` | 소득세 | 12 | 단위: 원, 좌측 0-padding 처리된 부호 포함 12자리 숫자 |
| `acnt_nxdy_setl_frcs_prps_array[].rstx` | 농특세 | 12 | 단위: 원, 좌측 0-padding 처리된 부호 포함 12자리 숫자 |
| `acnt_nxdy_setl_frcs_prps_array[].stk_nm` | 종목명 | 40 |   |
| `acnt_nxdy_setl_frcs_prps_array[].sell_tp` | 매도수구분 | 10 |   |
| `acnt_nxdy_setl_frcs_prps_array[].unp` | 단가 | 12 | 단위: 원, 좌측 0-padding 처리된 부호 포함 12자리 숫자 |
| `acnt_nxdy_setl_frcs_prps_array[].exct_amt` | 정산금액 | 12 | 단위: 원, 좌측 0-padding 처리된 부호 포함 12자리 숫자 |
| `acnt_nxdy_setl_frcs_prps_array[].trde_tax` | 거래세 | 12 | 단위: 원, 좌측 0-padding 처리된 부호 포함 12자리 숫자 |
| `acnt_nxdy_setl_frcs_prps_array[].resi_tax` | 주민세 | 12 | 단위: 원, 좌측 0-padding 처리된 부호 포함 12자리 숫자 |
| `acnt_nxdy_setl_frcs_prps_array[].crd_tp` | 신용구분 | 20 |   |

<a id="kt00009"></a>

## `kt00009` · `order_execution_status()` — 계좌별주문체결현황요청

계좌별주문체결현황요청 (Account Order Execution Status) · `POST /api/dostk/acnt`

```python
api.account.order_execution_status(stk_bond_tp=..., mrkt_tp=..., sell_tp=..., qry_tp=..., dmst_stex_tp=...)
```

**요청**

| 필드 | 한글명 | 필수 | 길이 | 설명 |
|---|---|:---:|---:|---|
| `ord_dt` | 주문일자 |  | 8 | YYYYMMDD |
| `stk_bond_tp` | 주식채권구분 | Y | 1 | 0:전체, 1:주식, 2:채권 |
| `mrkt_tp` | 시장구분 | Y | 1 | 0:전체, 1:코스피, 2:코스닥, 3:OTCBB, 4:ECN |
| `sell_tp` | 매도수구분 | Y | 1 | 0:전체, 1:매도, 2:매수 |
| `qry_tp` | 조회구분 | Y | 1 | 0:전체, 1:체결 |
| `stk_cd` | 종목코드 |  | 12 | 전문 조회할 종목코드 |
| `fr_ord_no` | 시작주문번호 |  | 7 | 시작주문번호의 이전 주문은 조회 되지 않으며 약정금액에도 포함 되지 않음 |
| `dmst_stex_tp` | 국내거래소구분 | Y | 6 | %:(전체),KRX:한국거래소,NXT:넥스트트레이드,SOR:최선주문집행 |

**응답**

| 필드 | 한글명 | 길이 | 설명 |
|---|---|---:|---|
| `sell_grntl_engg_amt` | 매도약정금액 | 12 | 단위: 원, 좌측 0-padding 처리된 부호 포함 12자리 숫자 |
| `buy_engg_amt` | 매수약정금액 | 12 | 단위: 원, 좌측 0-padding 처리된 부호 포함 12자리 숫자 |
| `engg_amt` | 약정금액 | 12 | 단위: 원, 좌측 0-padding 처리된 부호 포함 12자리 숫자 |
| `acnt_ord_cntr_prst_array` (list) | 계좌별주문체결현황배열 |  |   |
| `acnt_ord_cntr_prst_array[].stk_bond_tp` | 주식채권구분 | 1 |   |
| `acnt_ord_cntr_prst_array[].ord_no` | 주문번호 | 7 | 고유 주문번호 7자리 |
| `acnt_ord_cntr_prst_array[].stk_cd` | 종목번호 | 12 | 접두어 1자리 + 종목코드 6자리, 접두어(A: 주식 / J: ELW / Q: ETN) |
| `acnt_ord_cntr_prst_array[].trde_tp` | 매매구분 | 15 |   |
| `acnt_ord_cntr_prst_array[].io_tp_nm` | 주문유형구분 | 20 |   |
| `acnt_ord_cntr_prst_array[].ord_qty` | 주문수량 | 10 | 단위: 1주, 좌측 0-padding 처리된 부호 포함 10자리 숫자 |
| `acnt_ord_cntr_prst_array[].ord_uv` | 주문단가 | 10 | 단위: 원, 좌측 0-padding 처리된 부호 포함 10자리 숫자 |
| `acnt_ord_cntr_prst_array[].cnfm_qty` | 확인수량 | 10 | 단위: 1주, 좌측 0-padding 처리된 부호 포함 10자리 숫자 |
| `acnt_ord_cntr_prst_array[].rsrv_oppo` | 예약/반대 | 4 |   |
| `acnt_ord_cntr_prst_array[].cntr_no` | 체결번호 | 7 | 체결번호 7자리 |
| `acnt_ord_cntr_prst_array[].acpt_tp` | 접수구분 | 8 |   |
| `acnt_ord_cntr_prst_array[].orig_ord_no` | 원주문번호 | 7 | 원 주문이 없는 경우 '0000000'으로 출력 |
| `acnt_ord_cntr_prst_array[].stk_nm` | 종목명 | 20 |   |
| `acnt_ord_cntr_prst_array[].setl_tp` | 결제구분 | 8 |   |
| `acnt_ord_cntr_prst_array[].crd_deal_tp` | 신용거래구분 | 20 |   |
| `acnt_ord_cntr_prst_array[].cntr_qty` | 체결수량 | 10 | 단위: 1주, 좌측 0-padding 처리된 부호 포함 10자리 숫자 |
| `acnt_ord_cntr_prst_array[].cntr_uv` | 체결단가 | 10 | 단위: 원, 좌측 0-padding 처리된 부호 포함 10자리 숫자 |
| `acnt_ord_cntr_prst_array[].comm_ord_tp` | 통신구분 | 8 |   |
| `acnt_ord_cntr_prst_array[].mdfy_cncl_tp` | 정정/취소구분 | 12 |   |
| `acnt_ord_cntr_prst_array[].cntr_tm` | 체결시간 | 8 | HH:mm:ss |
| `acnt_ord_cntr_prst_array[].dmst_stex_tp` | 국내거래소구분 | 6 |   |
| `acnt_ord_cntr_prst_array[].cond_uv` | 스톱가 | 10 | 단위: 원, 좌측 0-padding 처리된 부호 포함 10자리 숫자 |

<a id="kt00010"></a>

## `kt00010` · `withdrawable_amount()` — 주문인출가능금액요청

주문인출가능금액요청 (Withdrawable Order Amount) · `POST /api/dostk/acnt`

```python
api.account.withdrawable_amount(stk_cd=..., trde_tp=..., uv=...)
```

**요청**

| 필드 | 한글명 | 필수 | 길이 | 설명 |
|---|---|:---:|---:|---|
| `io_amt` | 입출금액 |  | 12 | 단위: 원 |
| `stk_cd` | 종목번호 | Y | 12 | 종목 코드 입력 |
| `trde_tp` | 매매구분 | Y | 1 | 1:매도, 2:매수 |
| `trde_qty` | 매매수량 |  | 10 | 단위: 1주 |
| `uv` | 매수가격 | Y | 10 | 단위: 원 |
| `exp_buy_unp` | 예상매수단가 |  | 10 | 단위: 원 |

**응답**

| 필드 | 한글명 | 길이 | 설명 |
|---|---|---:|---|
| `profa_20ord_alow_amt` | 증거금20%주문가능금액 | 12 | 단위: 원, 좌측 0-padding 처리된 부호 포함 12자리 숫자 |
| `profa_20ord_alowq` | 증거금20%주문가능수량 | 10 | 단위: 1주, 좌측 0-padding 처리된 부호 포함 10자리 숫자 |
| `profa_30ord_alow_amt` | 증거금30%주문가능금액 | 12 | 단위: 원, 좌측 0-padding 처리된 부호 포함 12자리 숫자 |
| `profa_30ord_alowq` | 증거금30%주문가능수량 | 10 | 단위: 1주, 좌측 0-padding 처리된 부호 포함 10자리 숫자 |
| `profa_40ord_alow_amt` | 증거금40%주문가능금액 | 12 | 단위: 원, 좌측 0-padding 처리된 부호 포함 12자리 숫자 |
| `profa_40ord_alowq` | 증거금40%주문가능수량 | 10 | 단위: 1주, 좌측 0-padding 처리된 부호 포함 10자리 숫자 |
| `profa_50ord_alow_amt` | 증거금50%주문가능금액 | 12 | 단위: 원, 좌측 0-padding 처리된 부호 포함 12자리 숫자 |
| `profa_50ord_alowq` | 증거금50%주문가능수량 | 10 | 단위: 1주, 좌측 0-padding 처리된 부호 포함 10자리 숫자 |
| `profa_60ord_alow_amt` | 증거금60%주문가능금액 | 12 | 단위: 원, 좌측 0-padding 처리된 부호 포함 12자리 숫자 |
| `profa_60ord_alowq` | 증거금60%주문가능수량 | 10 | 단위: 1주, 좌측 0-padding 처리된 부호 포함 10자리 숫자 |
| `profa_rdex_60ord_alow_amt` | 증거금감면60%주문가능금 | 12 | 단위: 원, 좌측 0-padding 처리된 부호 포함 12자리 숫자 |
| `profa_rdex_60ord_alowq` | 증거금감면60%주문가능수 | 10 | 단위: 1주, 좌측 0-padding 처리된 부호 포함 10자리 숫자 |
| `profa_100ord_alow_amt` | 증거금100%주문가능금액 | 12 | 단위: 원, 좌측 0-padding 처리된 부호 포함 12자리 숫자 |
| `profa_100ord_alowq` | 증거금100%주문가능수량 | 10 | 단위: 1주, 좌측 0-padding 처리된 부호 포함 10자리 숫자 |
| `pred_reu_alowa` | 전일재사용가능금액 | 12 | 단위: 원, 좌측 0-padding 처리된 부호 포함 12자리 숫자 |
| `tdy_reu_alowa` | 금일재사용가능금액 | 12 | 단위: 원, 좌측 0-padding 처리된 부호 포함 12자리 숫자 |
| `entr` | 예수금 | 12 | 단위: 원, 좌측 0-padding 처리된 부호 포함 12자리 숫자 |
| `repl_amt` | 대용금 | 12 | 단위: 원, 좌측 0-padding 처리된 부호 포함 12자리 숫자 |
| `uncla` | 미수금 | 12 | 단위: 원, 좌측 0-padding 처리된 부호 포함 12자리 숫자 |
| `ord_pos_repl` | 주문가능대용 | 12 | 단위: 원, 좌측 0-padding 처리된 부호 포함 12자리 숫자 |
| `ord_alowa` | 주문가능현금 | 12 | 단위: 원, 좌측 0-padding 처리된 부호 포함 12자리 숫자 |
| `wthd_alowa` | 인출가능금액 | 12 | 단위: 원, 좌측 0-padding 처리된 부호 포함 12자리 숫자 |
| `nxdy_wthd_alowa` | 익일인출가능금액 | 12 | 단위: 원, 좌측 0-padding 처리된 부호 포함 12자리 숫자 |
| `pur_amt` | 매입금액 | 12 | 단위: 원, 좌측 0-padding 처리된 부호 포함 12자리 숫자 |
| `cmsn` | 수수료 | 12 | 단위: 원, 좌측 0-padding 처리된 부호 포함 12자리 숫자 |
| `pur_exct_amt` | 매입정산금 | 12 | 단위: 원, 좌측 0-padding 처리된 부호 포함 12자리 숫자 |
| `d2entra` | D2추정예수금 | 12 | 단위: 원, 좌측 0-padding 처리된 부호 포함 12자리 숫자 |
| `profa_rdex_aplc_tp` | 증거금감면적용구분 | 1 | 0:일반,1:60%감면 |

<a id="kt00011"></a>

## `kt00011` · `orderable_qty_by_margin()` — 증거금율별주문가능수량조회요청

증거금율별주문가능수량조회요청 (Orderable Quantity by Margin Rate) · `POST /api/dostk/acnt`

```python
api.account.orderable_qty_by_margin(stk_cd=...)
```

**요청**

| 필드 | 한글명 | 필수 | 길이 | 설명 |
|---|---|:---:|---:|---|
| `stk_cd` | 종목번호 | Y | 12 | 종목 코드 입력 |
| `uv` | 매수가격 |  | 10 | 단위: 원 |

**응답**

| 필드 | 한글명 | 길이 | 설명 |
|---|---|---:|---|
| `stk_profa_rt` | 종목증거금율 | 15 | %가 포함된 백분율 값 |
| `profa_rt` | 계좌증거금율 | 15 | %가 포함된 백분율 값 |
| `aplc_rt` | 적용증거금율 | 15 | %가 포함된 백분율 값 |
| `profa_20ord_alow_amt` | 증거금20%주문가능금액 | 12 | 단위: 원, 좌측 0-padding 처리된 부호 포함 12자리 숫자 |
| `profa_20ord_alowq` | 증거금20%주문가능수량 | 12 | 단위: 1주, 좌측 0-padding 처리된 부호 포함 12자리 숫자 |
| `profa_20pred_reu_amt` | 증거금20%전일재사용금액 | 12 | 단위: 원, 좌측 0-padding 처리된 부호 포함 12자리 숫자 |
| `profa_20tdy_reu_amt` | 증거금20%금일재사용금액 | 12 | 단위: 원, 좌측 0-padding 처리된 부호 포함 12자리 숫자 |
| `profa_30ord_alow_amt` | 증거금30%주문가능금액 | 12 | 단위: 원, 좌측 0-padding 처리된 부호 포함 12자리 숫자 |
| `profa_30ord_alowq` | 증거금30%주문가능수량 | 12 | 단위: 1주, 좌측 0-padding 처리된 부호 포함 12자리 숫자 |
| `profa_30pred_reu_amt` | 증거금30%전일재사용금액 | 12 | 단위: 원, 좌측 0-padding 처리된 부호 포함 12자리 숫자 |
| `profa_30tdy_reu_amt` | 증거금30%금일재사용금액 | 12 | 단위: 원, 좌측 0-padding 처리된 부호 포함 12자리 숫자 |
| `profa_40ord_alow_amt` | 증거금40%주문가능금액 | 12 | 단위: 원, 좌측 0-padding 처리된 부호 포함 12자리 숫자 |
| `profa_40ord_alowq` | 증거금40%주문가능수량 | 12 | 단위: 1주, 좌측 0-padding 처리된 부호 포함 12자리 숫자 |
| `profa_40pred_reu_amt` | 증거금40전일재사용금액 | 12 | 단위: 원, 좌측 0-padding 처리된 부호 포함 12자리 숫자 |
| `profa_40tdy_reu_amt` | 증거금40%금일재사용금액 | 12 | 단위: 원, 좌측 0-padding 처리된 부호 포함 12자리 숫자 |
| `profa_50ord_alow_amt` | 증거금50%주문가능금액 | 12 | 단위: 원, 좌측 0-padding 처리된 부호 포함 12자리 숫자 |
| `profa_50ord_alowq` | 증거금50%주문가능수량 | 12 | 단위: 1주, 좌측 0-padding 처리된 부호 포함 12자리 숫자 |
| `profa_50pred_reu_amt` | 증거금50%전일재사용금액 | 12 | 단위: 원, 좌측 0-padding 처리된 부호 포함 12자리 숫자 |
| `profa_50tdy_reu_amt` | 증거금50%금일재사용금액 | 12 | 단위: 원, 좌측 0-padding 처리된 부호 포함 12자리 숫자 |
| `profa_60ord_alow_amt` | 증거금60%주문가능금액 | 12 | 단위: 원, 좌측 0-padding 처리된 부호 포함 12자리 숫자 |
| `profa_60ord_alowq` | 증거금60%주문가능수량 | 12 | 단위: 1주, 좌측 0-padding 처리된 부호 포함 12자리 숫자 |
| `profa_60pred_reu_amt` | 증거금60%전일재사용금액 | 12 | 단위: 원, 좌측 0-padding 처리된 부호 포함 12자리 숫자 |
| `profa_60tdy_reu_amt` | 증거금60%금일재사용금액 | 12 | 단위: 원, 좌측 0-padding 처리된 부호 포함 12자리 숫자 |
| `profa_100ord_alow_amt` | 증거금100%주문가능금액 | 12 | 단위: 원, 좌측 0-padding 처리된 부호 포함 12자리 숫자 |
| `profa_100ord_alowq` | 증거금100%주문가능수량 | 12 | 단위: 1주, 좌측 0-padding 처리된 부호 포함 12자리 숫자 |
| `profa_100pred_reu_amt` | 증거금100%전일재사용금액 | 12 | 단위: 원, 좌측 0-padding 처리된 부호 포함 12자리 숫자 |
| `profa_100tdy_reu_amt` | 증거금100%금일재사용금액 | 12 | 단위: 원, 좌측 0-padding 처리된 부호 포함 12자리 숫자 |
| `min_ord_alow_amt` | 미수불가주문가능금액 | 12 | 단위: 원, 좌측 0-padding 처리된 부호 포함 12자리 숫자 |
| `min_ord_alowq` | 미수불가주문가능수량 | 12 | 단위: 1주, 좌측 0-padding 처리된 부호 포함 12자리 숫자 |
| `min_pred_reu_amt` | 미수불가전일재사용금액 | 12 | 단위: 원, 좌측 0-padding 처리된 부호 포함 12자리 숫자 |
| `min_tdy_reu_amt` | 미수불가금일재사용금액 | 12 | 단위: 원, 좌측 0-padding 처리된 부호 포함 12자리 숫자 |
| `entr` | 예수금 | 12 | 단위: 원, 좌측 0-padding 처리된 부호 포함 12자리 숫자 |
| `repl_amt` | 대용금 | 12 | 단위: 원, 좌측 0-padding 처리된 부호 포함 12자리 숫자 |
| `uncla` | 미수금 | 12 | 단위: 원, 좌측 0-padding 처리된 부호 포함 12자리 숫자 |
| `ord_pos_repl` | 주문가능대용 | 12 | 단위: 원, 좌측 0-padding 처리된 부호 포함 12자리 숫자 |
| `ord_alowa` | 주문가능현금 | 12 | 단위: 원, 좌측 0-padding 처리된 부호 포함 12자리 숫자 |

<a id="kt00012"></a>

## `kt00012` · `orderable_qty_by_credit()` — 신용보증금율별주문가능수량조회요청

신용보증금율별주문가능수량조회요청 (Orderable Quantity by Credit Margin Rate) · `POST /api/dostk/acnt`

```python
api.account.orderable_qty_by_credit(stk_cd=...)
```

**요청**

| 필드 | 한글명 | 필수 | 길이 | 설명 |
|---|---|:---:|---:|---|
| `stk_cd` | 종목번호 | Y | 12 | 종목 코드 입력 |
| `uv` | 매수가격 |  | 10 | 단위: 원 |

**응답**

| 필드 | 한글명 | 길이 | 설명 |
|---|---|---:|---|
| `stk_assr_rt` | 종목보증금율 | 1 |   |
| `stk_assr_rt_nm` | 종목보증금율명 | 4 |   |
| `assr_30ord_alow_amt` | 보증금30%주문가능금액 | 12 | 단위: 원, 좌측 0-padding 처리된 부호 포함 12자리 숫자 |
| `assr_30ord_alowq` | 보증금30%주문가능수량 | 12 | 단위: 1주, 좌측 0-padding 처리된 부호 포함 12자리 숫자 |
| `assr_30pred_reu_amt` | 보증금30%전일재사용금액 | 12 | 단위: 원, 좌측 0-padding 처리된 부호 포함 12자리 숫자 |
| `assr_30tdy_reu_amt` | 보증금30%금일재사용금액 | 12 | 단위: 원, 좌측 0-padding 처리된 부호 포함 12자리 숫자 |
| `assr_40ord_alow_amt` | 보증금40%주문가능금액 | 12 | 단위: 원, 좌측 0-padding 처리된 부호 포함 12자리 숫자 |
| `assr_40ord_alowq` | 보증금40%주문가능수량 | 12 | 단위: 1주, 좌측 0-padding 처리된 부호 포함 12자리 숫자 |
| `assr_40pred_reu_amt` | 보증금40%전일재사용금액 | 12 | 단위: 원, 좌측 0-padding 처리된 부호 포함 12자리 숫자 |
| `assr_40tdy_reu_amt` | 보증금40%금일재사용금액 | 12 | 단위: 원, 좌측 0-padding 처리된 부호 포함 12자리 숫자 |
| `assr_50ord_alow_amt` | 보증금50%주문가능금액 | 12 | 단위: 원, 좌측 0-padding 처리된 부호 포함 12자리 숫자 |
| `assr_50ord_alowq` | 보증금50%주문가능수량 | 12 | 단위: 1주, 좌측 0-padding 처리된 부호 포함 12자리 숫자 |
| `assr_50pred_reu_amt` | 보증금50%전일재사용금액 | 12 | 단위: 원, 좌측 0-padding 처리된 부호 포함 12자리 숫자 |
| `assr_50tdy_reu_amt` | 보증금50%금일재사용금액 | 12 | 단위: 원, 좌측 0-padding 처리된 부호 포함 12자리 숫자 |
| `assr_60ord_alow_amt` | 보증금60%주문가능금액 | 12 | 단위: 원, 좌측 0-padding 처리된 부호 포함 12자리 숫자 |
| `assr_60ord_alowq` | 보증금60%주문가능수량 | 12 | 단위: 1주, 좌측 0-padding 처리된 부호 포함 12자리 숫자 |
| `assr_60pred_reu_amt` | 보증금60%전일재사용금액 | 12 | 단위: 원, 좌측 0-padding 처리된 부호 포함 12자리 숫자 |
| `assr_60tdy_reu_amt` | 보증금60%금일재사용금액 | 12 | 단위: 원, 좌측 0-padding 처리된 부호 포함 12자리 숫자 |
| `entr` | 예수금 | 12 | 단위: 원, 좌측 0-padding 처리된 부호 포함 12자리 숫자 |
| `repl_amt` | 대용금 | 12 | 단위: 원, 좌측 0-padding 처리된 부호 포함 12자리 숫자 |
| `uncla` | 미수금 | 12 | 단위: 원, 좌측 0-padding 처리된 부호 포함 12자리 숫자 |
| `ord_pos_repl` | 주문가능대용 | 12 | 단위: 원, 좌측 0-padding 처리된 부호 포함 12자리 숫자 |
| `ord_alowa` | 주문가능현금 | 12 | 단위: 원, 좌측 0-padding 처리된 부호 포함 12자리 숫자 |
| `out_alowa` | 미수가능금액 | 12 | 단위: 원, 좌측 0-padding 처리된 부호 포함 12자리 숫자 |
| `out_pos_qty` | 미수가능수량 | 12 | 단위: 1주, 좌측 0-padding 처리된 부호 포함 12자리 숫자 |
| `min_amt` | 미수불가금액 | 12 | 단위: 원, 좌측 0-padding 처리된 부호 포함 12자리 숫자 |
| `min_qty` | 미수불가수량 | 12 | 단위: 1주, 좌측 0-padding 처리된 부호 포함 12자리 숫자 |

<a id="kt00013"></a>

## `kt00013` · `margin_detail()` — 증거금세부내역조회요청

증거금세부내역조회요청 (Margin Detail Inquiry) · `POST /api/dostk/acnt`

```python
api.account.margin_detail()
```

**요청**

요청 필드 없음.

**응답**

| 필드 | 한글명 | 길이 | 설명 |
|---|---|---:|---|
| `tdy_reu_objt_amt` | 금일재사용대상금액 | 15 | 단위: 원, 좌측 0-padding 처리된 부호 포함 15자리 숫자 |
| `tdy_reu_use_amt` | 금일재사용사용금액 | 15 | 단위: 원, 좌측 0-padding 처리된 부호 포함 15자리 숫자 |
| `tdy_reu_alowa` | 금일재사용가능금액 | 15 | 단위: 원, 좌측 0-padding 처리된 부호 포함 15자리 숫자 |
| `tdy_reu_lmtt_amt` | 금일재사용제한금액 | 15 | 단위: 원, 좌측 0-padding 처리된 부호 포함 15자리 숫자 |
| `tdy_reu_alowa_fin` | 금일재사용가능금액최종 | 15 | 단위: 원, 좌측 0-padding 처리된 부호 포함 15자리 숫자 |
| `pred_reu_objt_amt` | 전일재사용대상금액 | 15 | 단위: 원, 좌측 0-padding 처리된 부호 포함 15자리 숫자 |
| `pred_reu_use_amt` | 전일재사용사용금액 | 15 | 단위: 원, 좌측 0-padding 처리된 부호 포함 15자리 숫자 |
| `pred_reu_alowa` | 전일재사용가능금액 | 15 | 단위: 원, 좌측 0-padding 처리된 부호 포함 15자리 숫자 |
| `pred_reu_lmtt_amt` | 전일재사용제한금액 | 15 | 단위: 원, 좌측 0-padding 처리된 부호 포함 15자리 숫자 |
| `pred_reu_alowa_fin` | 전일재사용가능금액최종 | 15 | 단위: 원, 좌측 0-padding 처리된 부호 포함 15자리 숫자 |
| `ch_amt` | 현금금액 | 15 | 단위: 원, 좌측 0-padding 처리된 부호 포함 15자리 숫자 |
| `ch_profa` | 현금증거금 | 15 | 단위: 원, 좌측 0-padding 처리된 부호 포함 15자리 숫자 |
| `use_pos_ch` | 사용가능현금 | 15 | 단위: 원, 좌측 0-padding 처리된 부호 포함 15자리 숫자 |
| `ch_use_lmtt_amt` | 현금사용제한금액 | 15 | 단위: 원, 좌측 0-padding 처리된 부호 포함 15자리 숫자 |
| `use_pos_ch_fin` | 사용가능현금최종 | 15 | 단위: 원, 좌측 0-padding 처리된 부호 포함 15자리 숫자 |
| `repl_amt_amt` | 대용금액 | 15 | 단위: 원, 좌측 0-padding 처리된 부호 포함 15자리 숫자 |
| `repl_profa` | 대용증거금 | 15 | 단위: 원, 좌측 0-padding 처리된 부호 포함 15자리 숫자 |
| `use_pos_repl` | 사용가능대용 | 15 | 단위: 원, 좌측 0-padding 처리된 부호 포함 15자리 숫자 |
| `repl_use_lmtt_amt` | 대용사용제한금액 | 15 | 단위: 원, 좌측 0-padding 처리된 부호 포함 15자리 숫자 |
| `use_pos_repl_fin` | 사용가능대용최종 | 15 | 단위: 원, 좌측 0-padding 처리된 부호 포함 15자리 숫자 |
| `crd_grnta_ch` | 신용보증금현금 | 15 | 단위: 원, 좌측 0-padding 처리된 부호 포함 15자리 숫자 |
| `crd_grnta_repl` | 신용보증금대용 | 15 | 단위: 원, 좌측 0-padding 처리된 부호 포함 15자리 숫자 |
| `crd_grnt_ch` | 신용담보금현금 | 15 | 단위: 원, 좌측 0-padding 처리된 부호 포함 15자리 숫자 |
| `crd_grnt_repl` | 신용담보금대용 | 15 | 단위: 원, 좌측 0-padding 처리된 부호 포함 15자리 숫자 |
| `uncla` | 미수금 | 12 | 단위: 원, 좌측 0-padding 처리된 부호 포함 15자리 숫자 |
| `ls_grnt_reu_gold` | 대주담보금재사용금 | 15 | 단위: 원, 좌측 0-padding 처리된 부호 포함 15자리 숫자 |
| `20ord_alow_amt` | 20%주문가능금액 | 15 | 단위: 원, 좌측 0-padding 처리된 부호 포함 15자리 숫자 |
| `30ord_alow_amt` | 30%주문가능금액 | 15 | 단위: 원, 좌측 0-padding 처리된 부호 포함 15자리 숫자 |
| `40ord_alow_amt` | 40%주문가능금액 | 15 | 단위: 원, 좌측 0-padding 처리된 부호 포함 15자리 숫자 |
| `50ord_alow_amt` | 50%주문가능금액 | 15 | 단위: 원, 좌측 0-padding 처리된 부호 포함 15자리 숫자 |
| `60ord_alow_amt` | 60%주문가능금액 | 15 | 단위: 원, 좌측 0-padding 처리된 부호 포함 15자리 숫자 |
| `100ord_alow_amt` | 100%주문가능금액 | 15 | 단위: 원, 좌측 0-padding 처리된 부호 포함 15자리 숫자 |
| `tdy_crd_rpya_loss_amt` | 금일신용상환손실금액 | 15 | 단위: 원, 좌측 0-padding 처리된 부호 포함 15자리 숫자 |
| `pred_crd_rpya_loss_amt` | 전일신용상환손실금액 | 15 | 단위: 원, 좌측 0-padding 처리된 부호 포함 15자리 숫자 |
| `tdy_ls_rpya_loss_repl_profa` | 금일대주상환손실대용증거금 | 15 | 단위: 원, 좌측 0-padding 처리된 부호 포함 15자리 숫자 |
| `pred_ls_rpya_loss_repl_profa` | 전일대주상환손실대용증거금 | 15 | 단위: 원, 좌측 0-padding 처리된 부호 포함 15자리 숫자 |
| `evlt_repl_amt_spg_use_skip` | 평가대용금(현물사용제외) | 15 | 단위: 원, 좌측 0-padding 처리된 부호 포함 15자리 숫자 |
| `evlt_repl_rt` | 평가대용비율 | 15 | 단위: %, 소수점 일곱번째 자리까지 포맷된 백분율 |
| `crd_repl_profa` | 신용대용증거금 | 15 | 단위: 원, 좌측 0-padding 처리된 부호 포함 15자리 숫자 |
| `ch_ord_repl_profa` | 현금주문대용증거금 | 15 | 단위: 원, 좌측 0-padding 처리된 부호 포함 15자리 숫자 |
| `crd_ord_repl_profa` | 신용주문대용증거금 | 15 | 단위: 원, 좌측 0-padding 처리된 부호 포함 15자리 숫자 |
| `crd_repl_conv_gold` | 신용대용환산금 | 15 | 단위: 원, 좌측 0-padding 처리된 부호 포함 15자리 숫자 |
| `repl_alowa` | 대용가능금액(현금제한) | 15 | 단위: 원, 좌측 0-padding 처리된 부호 포함 15자리 숫자 |
| `repl_alowa_2` | 대용가능금액2(신용제한) | 15 | 단위: 원, 좌측 0-padding 처리된 부호 포함 15자리 숫자 |
| `ch_repl_lck_gold` | 현금대용부족금 | 15 | 단위: 원, 좌측 0-padding 처리된 부호 포함 15자리 숫자 |
| `crd_repl_lck_gold` | 신용대용부족금 | 15 | 단위: 원, 좌측 0-padding 처리된 부호 포함 15자리 숫자 |
| `ch_ord_alow_repla` | 현금주문가능대용금 | 15 | 단위: 원, 좌측 0-padding 처리된 부호 포함 15자리 숫자 |
| `crd_ord_alow_repla` | 신용주문가능대용금 | 15 | 단위: 원, 좌측 0-padding 처리된 부호 포함 15자리 숫자 |
| `d2vexct_entr` | D2가정산예수금 | 15 | 단위: 원, 좌측 0-padding 처리된 부호 포함 15자리 숫자 |
| `d2ch_ord_alow_amt` | D2현금주문가능금액 | 15 | 단위: 원, 좌측 0-padding 처리된 부호 포함 15자리 숫자 |

<a id="kt00015"></a>

## `kt00015` · `comprehensive_transaction_history()` — 위탁종합거래내역요청

위탁종합거래내역요청 (Comprehensive Transaction History) · `POST /api/dostk/acnt`

```python
api.account.comprehensive_transaction_history(strt_dt=..., end_dt=..., tp=..., gds_tp=..., dmst_stex_tp=...)
```

**요청**

| 필드 | 한글명 | 필수 | 길이 | 설명 |
|---|---|:---:|---:|---|
| `strt_dt` | 시작일자 | Y | 8 | YYYYMMDD |
| `end_dt` | 종료일자 | Y | 8 | YYYYMMDD |
| `tp` | 구분 | Y | 1 | 0:전체,1:입출금,2:입출고,3:매매,4:매수,5:매도,6:입금,7:출금,A:예탁담보대출입금,B:매도담보대출입금,C:현금상환(융자,담보상환),F:환전,M:입출금+환전,G:외화매수,H:외화매도,I:환전정산입금,J:환전정산출금 |
| `stk_cd` | 종목코드 |  | 12 | 종목 코드 입력 |
| `crnc_cd` | 통화코드 |  | 3 | 통화코드 3자리 |
| `gds_tp` | 상품구분 | Y | 1 | 0:전체, 1:국내주식, 2:수익증권, 3:해외주식, 4:금융상품 |
| `frgn_stex_code` | 해외거래소코드 |  | 10 |   |
| `dmst_stex_tp` | 국내거래소구분 | Y | 6 | %:(전체),KRX:한국거래소,NXT:넥스트트레이드 |
| `qry_sort_tp` | 조회정렬구분 |  | 1 | 1:최근거래순, 2:과거거래순(미입력시 과거거래순) |

**응답**

| 필드 | 한글명 | 길이 | 설명 |
|---|---|---:|---|
| `trst_ovrl_trde_prps_array` (list) | 위탁종합거래내역배열 |  |   |
| `trst_ovrl_trde_prps_array[].trde_dt` | 거래일자 | 8 | YYYYMMDD |
| `trst_ovrl_trde_prps_array[].trde_no` | 거래번호 | 9 | 거래번호 9자리 |
| `trst_ovrl_trde_prps_array[].rmrk_nm` | 적요명 | 60 |   |
| `trst_ovrl_trde_prps_array[].crd_deal_tp_nm` | 신용거래구분명 | 20 |   |
| `trst_ovrl_trde_prps_array[].exct_amt` | 정산금액 | 15 | 단위: 원, 좌측 0-padding 처리된 부호 포함 15자리 숫자 |
| `trst_ovrl_trde_prps_array[].loan_amt_rpya` | 대출금상환 | 15 | 단위: 원, 좌측 0-padding 처리된 부호 포함 15자리 숫자 |
| `trst_ovrl_trde_prps_array[].fc_trde_amt` | 거래금액(외) | 15 |   |
| `trst_ovrl_trde_prps_array[].fc_exct_amt` | 정산금액(외) | 15 |   |
| `trst_ovrl_trde_prps_array[].entra_remn` | 예수금잔고 | 15 | 단위: 원, 좌측 0-padding 처리된 부호 포함 15자리 숫자 |
| `trst_ovrl_trde_prps_array[].crnc_cd` | 통화코드 | 3 |   |
| `trst_ovrl_trde_prps_array[].trde_ocr_tp` | 거래종류구분 | 2 | 1:입출금, 2:펀드, 3:ELS, 4:채권, 5:해외채권, 6:외화RP, 7:외화발행어음 |
| `trst_ovrl_trde_prps_array[].trde_kind_nm` | 거래종류명 | 20 | 거래종류구분자(trde_ocr_tp)의 한글명 |
| `trst_ovrl_trde_prps_array[].stk_nm` | 종목명 | 40 |   |
| `trst_ovrl_trde_prps_array[].trde_amt` | 거래금액 | 15 | 단위: 원, 좌측 0-padding 처리된 부호 포함 15자리 숫자 |
| `trst_ovrl_trde_prps_array[].trde_agri_tax` | 거래및농특세 | 15 | 단위: 원, 좌측 0-padding 처리된 부호 포함 15자리 숫자 |
| `trst_ovrl_trde_prps_array[].rpy_diffa` | 상환차금 | 15 | 단위: 원, 좌측 0-padding 처리된 부호 포함 15자리 숫자 |
| `trst_ovrl_trde_prps_array[].fc_trde_tax` | 거래세(외) | 15 |   |
| `trst_ovrl_trde_prps_array[].dly_sum` | 연체합 | 15 | 단위: 원, 좌측 0-padding 처리된 부호 포함 15자리 숫자 |
| `trst_ovrl_trde_prps_array[].fc_entra` | 외화예수금잔고 | 15 |   |
| `trst_ovrl_trde_prps_array[].mdia_tp_nm` | 매체구분명 | 20 |   |
| `trst_ovrl_trde_prps_array[].io_tp` | 입출구분 | 1 |   |
| `trst_ovrl_trde_prps_array[].io_tp_nm` | 입출구분명 | 10 |   |
| `trst_ovrl_trde_prps_array[].orig_deal_no` | 원거래번호 | 9 | 원 거래가 없는 경우 '000000000'으로 출력 |
| `trst_ovrl_trde_prps_array[].stk_cd` | 종목코드 | 12 | 접두어 1자리 + 종목코드 6자리, 접두어(A: 주식 / J: ELW / Q: ETN) |
| `trst_ovrl_trde_prps_array[].trde_qty_jwa_cnt` | 거래수량/좌수 | 30 |   |
| `trst_ovrl_trde_prps_array[].cmsn` | 수수료 | 15 | 단위: 원, 좌측 0-padding 처리된 부호 포함 15자리 숫자 |
| `trst_ovrl_trde_prps_array[].int_ls_usfe` | 이자/대주이용 | 15 | 단위: 원, 좌측 0-padding 처리된 부호 포함 15자리 숫자 |
| `trst_ovrl_trde_prps_array[].fc_cmsn` | 수수료(외) | 15 |   |
| `trst_ovrl_trde_prps_array[].fc_dly_sum` | 연체합(외) | 15 |   |
| `trst_ovrl_trde_prps_array[].vlbl_nowrm` | 유가금잔 | 30 |   |
| `trst_ovrl_trde_prps_array[].proc_tm` | 처리시간 | 111 | HH:mm:ss |
| `trst_ovrl_trde_prps_array[].isin_cd` | ISIN코드 | 12 |   |
| `trst_ovrl_trde_prps_array[].stex_cd` | 거래소코드 | 10 |   |
| `trst_ovrl_trde_prps_array[].stex_nm` | 거래소명 | 20 |   |
| `trst_ovrl_trde_prps_array[].trde_unit` | 거래단가/환율 | 20 |   |
| `trst_ovrl_trde_prps_array[].incm_resi_tax` | 소득/주민세 | 15 | 단위: 원, 좌측 0-padding 처리된 부호 포함 15자리 숫자 |
| `trst_ovrl_trde_prps_array[].loan_dt` | 대출일 | 8 | YYYYMMDD |
| `trst_ovrl_trde_prps_array[].uncl_ocr` | 미수(원/주) | 30 |   |
| `trst_ovrl_trde_prps_array[].rpym_sum` | 변제합 | 30 |   |
| `trst_ovrl_trde_prps_array[].cntr_dt` | 체결일 | 8 | YYYYMMDD |
| `trst_ovrl_trde_prps_array[].rcpy_no` | 출납번호 | 20 |   |
| `trst_ovrl_trde_prps_array[].prcsr` | 처리자 | 20 |   |
| `trst_ovrl_trde_prps_array[].proc_brch` | 처리점 | 20 |   |
| `trst_ovrl_trde_prps_array[].trde_stle` | 매매형태 | 40 |   |
| `trst_ovrl_trde_prps_array[].txon_base_pric` | 과세기준가 | 15 |   |
| `trst_ovrl_trde_prps_array[].tax_sum_cmsn` | 세금수수료합 | 15 |   |
| `trst_ovrl_trde_prps_array[].frgn_pay_txam` | 외국납부세액(외) | 15 |   |
| `trst_ovrl_trde_prps_array[].fc_uncl_ocr` | 미수(외) | 15 |   |
| `trst_ovrl_trde_prps_array[].rpym_sum_fr` | 변제합(외) | 30 |   |
| `trst_ovrl_trde_prps_array[].rcpmnyer` | 입금자 | 20 |   |
| `trst_ovrl_trde_prps_array[].trde_prtc_tp` | 거래내역구분 | 2 |   |

<a id="kt00016"></a>

## `kt00016` · `daily_return_detail()` — 일별계좌수익률상세현황요청

일별계좌수익률상세현황요청 (Daily Account Return Rate Detail) · `POST /api/dostk/acnt`

```python
api.account.daily_return_detail(fr_dt=..., to_dt=...)
```

**요청**

| 필드 | 한글명 | 필수 | 길이 | 설명 |
|---|---|:---:|---:|---|
| `fr_dt` | 평가시작일 | Y | 8 | YYYYMMDD |
| `to_dt` | 평가종료일 | Y | 8 | YYYYMMDD |

**응답**

| 필드 | 한글명 | 길이 | 설명 |
|---|---|---:|---|
| `mang_empno` | 관리사원번호 | 8 |   |
| `mngr_nm` | 관리자명 | 8 |   |
| `dept_nm` | 관리자지점 | 30 |   |
| `entr_fr` | 예수금_초 | 30 | 단위: 원, 좌측 0-padding 처리된 부호 포함 12자리 숫자 |
| `entr_to` | 예수금_말 | 12 | 단위: 원, 좌측 0-padding 처리된 부호 포함 12자리 숫자 |
| `scrt_evlt_amt_fr` | 유가증권평가금액_초 | 12 | 단위: 원, 좌측 0-padding 처리된 부호 포함 12자리 숫자 |
| `scrt_evlt_amt_to` | 유가증권평가금액_말 | 12 | 단위: 원, 좌측 0-padding 처리된 부호 포함 12자리 숫자 |
| `ls_grnt_fr` | 대주담보금_초 | 12 | 단위: 원, 좌측 0-padding 처리된 부호 포함 12자리 숫자 |
| `ls_grnt_to` | 대주담보금_말 | 12 | 단위: 원, 좌측 0-padding 처리된 부호 포함 12자리 숫자 |
| `crd_loan_fr` | 신용융자금_초 | 12 | 단위: 원, 좌측 0-padding 처리된 부호 포함 12자리 숫자 |
| `crd_loan_to` | 신용융자금_말 | 12 | 단위: 원, 좌측 0-padding 처리된 부호 포함 12자리 숫자 |
| `ch_uncla_fr` | 현금미수금_초 | 12 | 단위: 원, 좌측 0-padding 처리된 부호 포함 12자리 숫자 |
| `ch_uncla_to` | 현금미수금_말 | 12 | 단위: 원, 좌측 0-padding 처리된 부호 포함 12자리 숫자 |
| `krw_asgna_fr` | 원화대용금_초 | 12 | 단위: 원, 좌측 0-padding 처리된 부호 포함 12자리 숫자 |
| `krw_asgna_to` | 원화대용금_말 | 12 | 단위: 원, 좌측 0-padding 처리된 부호 포함 12자리 숫자 |
| `ls_evlta_fr` | 대주평가금_초 | 12 | 단위: 원, 좌측 0-padding 처리된 부호 포함 12자리 숫자 |
| `ls_evlta_to` | 대주평가금_말 | 12 | 단위: 원, 좌측 0-padding 처리된 부호 포함 12자리 숫자 |
| `rght_evlta_fr` | 권리평가금_초 | 12 | 단위: 원, 좌측 0-padding 처리된 부호 포함 12자리 숫자 |
| `rght_evlta_to` | 권리평가금_말 | 12 | 단위: 원, 좌측 0-padding 처리된 부호 포함 12자리 숫자 |
| `loan_amt_fr` | 대출금_초 | 12 | 단위: 원, 좌측 0-padding 처리된 부호 포함 12자리 숫자 |
| `loan_amt_to` | 대출금_말 | 12 | 단위: 원, 좌측 0-padding 처리된 부호 포함 12자리 숫자 |
| `etc_loana_fr` | 기타대여금_초 | 12 | 단위: 원, 좌측 0-padding 처리된 부호 포함 12자리 숫자 |
| `etc_loana_to` | 기타대여금_말 | 12 | 단위: 원, 좌측 0-padding 처리된 부호 포함 12자리 숫자 |
| `crd_int_npay_gold_fr` | 신용이자미납금_초 | 12 | 단위: 원, 좌측 0-padding 처리된 부호 포함 12자리 숫자 |
| `crd_int_npay_gold_to` | 신용이자미납금_말 | 12 | 단위: 원, 좌측 0-padding 처리된 부호 포함 12자리 숫자 |
| `crd_int_fr` | 신용이자_초 | 12 | 단위: 원, 좌측 0-padding 처리된 부호 포함 12자리 숫자 |
| `crd_int_to` | 신용이자_말 | 12 | 단위: 원, 좌측 0-padding 처리된 부호 포함 12자리 숫자 |
| `tot_amt_fr` | 순자산액계_초 | 12 | 단위: 원, 좌측 0-padding 처리된 부호 포함 12자리 숫자 |
| `tot_amt_to` | 순자산액계_말 | 12 | 단위: 원, 좌측 0-padding 처리된 부호 포함 12자리 숫자 |
| `invt_bsamt` | 투자원금평잔 | 12 | 단위: 원, 좌측 0-padding 처리된 부호 포함 12자리 숫자 |
| `evltv_prft` | 평가손익 | 12 | 단위: 원, 좌측 0-padding 처리된 부호 포함 12자리 숫자 |
| `prft_rt` | 수익률 | 12 | 단위: %, 소수점 둘째 자리까지 포맷된 백분율 |
| `tern_rt` | 회전율 | 12 | 단위: %, 소수점 둘째 자리까지 포맷된 백분율 |
| `termin_tot_trns` | 기간내총입금 | 12 | 단위: 원, 좌측 0-padding 처리된 부호 포함 12자리 숫자 |
| `termin_tot_pymn` | 기간내총출금 | 12 | 단위: 원, 좌측 0-padding 처리된 부호 포함 12자리 숫자 |
| `termin_tot_inq` | 기간내총입고 | 12 | 단위: 원, 좌측 0-padding 처리된 부호 포함 12자리 숫자 |
| `termin_tot_outq` | 기간내총출고 | 12 | 단위: 원, 좌측 0-padding 처리된 부호 포함 12자리 숫자 |
| `futr_repl_sella` | 선물대용매도금액 | 12 | 단위: 원, 좌측 0-padding 처리된 부호 포함 12자리 숫자 |
| `trst_repl_sella` | 위탁대용매도금액 | 12 | 단위: 원, 좌측 0-padding 처리된 부호 포함 12자리 숫자 |

<a id="kt00017"></a>

## `kt00017` · `today_account_status()` — 계좌별당일현황요청

계좌별당일현황요청 (Today Account Status by Account) · `POST /api/dostk/acnt`

```python
api.account.today_account_status()
```

**요청**

요청 필드 없음.

**응답**

| 필드 | 한글명 | 길이 | 설명 |
|---|---|---:|---|
| `d2_entra` | D+2추정예수금 | 12 | 단위: 원, 좌측 0-padding 처리된 부호 포함 12자리 숫자 |
| `crd_int_npay_gold` | 신용이자미납금 | 12 | 단위: 원, 좌측 0-padding 처리된 부호 포함 12자리 숫자 |
| `etc_loana` | 기타대여금 | 12 | 단위: 원, 좌측 0-padding 처리된 부호 포함 12자리 숫자 |
| `gnrl_stk_evlt_amt_d2` | 일반주식평가금액D+2 | 12 | 단위: 원, 좌측 0-padding 처리된 부호 포함 12자리 숫자 |
| `dpst_grnt_use_amt_d2` | 예탁담보대출금D+2 | 12 | 단위: 원, 좌측 0-padding 처리된 부호 포함 12자리 숫자 |
| `crd_stk_evlt_amt_d2` | 예탁담보주식평가금액D+2 | 12 | 단위: 원, 좌측 0-padding 처리된 부호 포함 12자리 숫자 |
| `crd_loan_d2` | 신용융자금D+2 | 12 | 단위: 원, 좌측 0-padding 처리된 부호 포함 12자리 숫자 |
| `crd_loan_evlta_d2` | 신용융자평가금D+2 | 12 | 단위: 원, 좌측 0-padding 처리된 부호 포함 12자리 숫자 |
| `crd_ls_grnt_d2` | 신용대주담보금D+2 | 12 | 단위: 원, 좌측 0-padding 처리된 부호 포함 12자리 숫자 |
| `crd_ls_evlta_d2` | 신용대주평가금D+2 | 12 | 단위: 원, 좌측 0-padding 처리된 부호 포함 12자리 숫자 |
| `ina_amt` | 입금금액 | 12 | 단위: 원, 좌측 0-padding 처리된 부호 포함 12자리 숫자 |
| `outa` | 출금금액 | 12 | 단위: 원, 좌측 0-padding 처리된 부호 포함 12자리 숫자 |
| `inq_amt` | 입고금액 | 12 | 단위: 원, 좌측 0-padding 처리된 부호 포함 12자리 숫자 |
| `outq_amt` | 출고금액 | 12 | 단위: 원, 좌측 0-padding 처리된 부호 포함 12자리 숫자 |
| `sell_amt` | 매도금액 | 12 | 단위: 원, 좌측 0-padding 처리된 부호 포함 12자리 숫자 |
| `buy_amt` | 매수금액 | 12 | 단위: 원, 좌측 0-padding 처리된 부호 포함 12자리 숫자 |
| `cmsn` | 수수료 | 12 | 단위: 원, 좌측 0-padding 처리된 부호 포함 12자리 숫자 |
| `tax` | 세금 | 12 | 단위: 원, 좌측 0-padding 처리된 부호 포함 12자리 숫자 |
| `stk_pur_cptal_loan_amt` | 주식매입자금대출금 | 12 | 단위: 원, 좌측 0-padding 처리된 부호 포함 12자리 숫자 |
| `rp_evlt_amt` | RP평가금액 | 12 | 단위: 원, 좌측 0-padding 처리된 부호 포함 12자리 숫자 |
| `bd_evlt_amt` | 채권평가금액 | 12 | 단위: 원, 좌측 0-padding 처리된 부호 포함 12자리 숫자 |
| `elsevlt_amt` | ELS평가금액 | 12 | 단위: 원, 좌측 0-padding 처리된 부호 포함 12자리 숫자 |
| `crd_int_amt` | 신용이자금액 | 12 | 단위: 원, 좌측 0-padding 처리된 부호 포함 12자리 숫자 |
| `sel_prica_grnt_loan_int_amt_amt` | 매도대금담보대출이자금액 | 12 | 단위: 원, 좌측 0-padding 처리된 부호 포함 12자리 숫자 |
| `dvida_amt` | 배당금액 | 12 | 단위: 원, 좌측 0-padding 처리된 부호 포함 12자리 숫자 |

<a id="kt00018"></a>

## `kt00018` · `evaluation_balance_detail()` — 계좌평가잔고내역요청

계좌평가잔고내역요청 (Account Evaluation Balance Detail) · `POST /api/dostk/acnt`

```python
api.account.evaluation_balance_detail(qry_tp=..., dmst_stex_tp=...)
```

**요청**

| 필드 | 한글명 | 필수 | 길이 | 설명 |
|---|---|:---:|---:|---|
| `qry_tp` | 조회구분 | Y | 1 | 1:합산, 2:개별 |
| `dmst_stex_tp` | 국내거래소구분 | Y | 6 | KRX:한국거래소,NXT:넥스트트레이드 |

**응답**

| 필드 | 한글명 | 길이 | 설명 |
|---|---|---:|---|
| `tot_pur_amt` | 총매입금액 | 15 | 단위: 원, 좌측 0-padding 처리된 부호 포함 15자리 숫자 |
| `tot_evlt_amt` | 총평가금액 | 15 | 단위: 원, 좌측 0-padding 처리된 부호 포함 15자리 숫자 |
| `tot_evlt_pl` | 총평가손익금액 | 15 | 단위: 원, 좌측 0-padding 처리된 부호 포함 15자리 숫자 |
| `tot_prft_rt` | 총수익률(%) | 12 | 단위: %, 소수점 둘째 자리까지 포맷된 백분율 |
| `prsm_dpst_aset_amt` | 추정예탁자산 | 15 | 단위: 원, 좌측 0-padding 처리된 부호 포함 15자리 숫자 |
| `tot_loan_amt` | 총대출금 | 15 | 단위: 원, 좌측 0-padding 처리된 부호 포함 15자리 숫자 |
| `tot_crd_loan_amt` | 총융자금액 | 15 | 단위: 원, 좌측 0-padding 처리된 부호 포함 15자리 숫자 |
| `tot_crd_ls_amt` | 총대주금액 | 15 | 단위: 원, 좌측 0-padding 처리된 부호 포함 15자리 숫자 |
| `acnt_evlt_remn_indv_tot` (list) | 계좌평가잔고개별합산 |  |   |
| `acnt_evlt_remn_indv_tot[].stk_cd` | 종목번호 | 12 | 접두어 1자리 + 종목코드 6자리, 접두어(A: 주식 / J: ELW / Q: ETN) |
| `acnt_evlt_remn_indv_tot[].stk_nm` | 종목명 | 40 |   |
| `acnt_evlt_remn_indv_tot[].evltv_prft` | 평가손익 | 15 | 단위: 원, 좌측 0-padding 처리된 부호 포함 15자리 숫자 |
| `acnt_evlt_remn_indv_tot[].prft_rt` | 수익률(%) | 12 | 단위: %, 소수점 둘째 자리까지 포맷된 백분율 |
| `acnt_evlt_remn_indv_tot[].pur_pric` | 매입가 | 15 | 단위: 원, 좌측 0-padding 처리된 부호 포함 15자리 숫자 |
| `acnt_evlt_remn_indv_tot[].pred_close_pric` | 전일종가 | 12 | 단위: 원, 좌측 0-padding 처리된 부호 포함 12자리 숫자 |
| `acnt_evlt_remn_indv_tot[].rmnd_qty` | 보유수량 | 15 | 단위: 1주, 좌측 0-padding 처리된 부호 포함 15자리 숫자 |
| `acnt_evlt_remn_indv_tot[].trde_able_qty` | 매매가능수량 | 15 | 단위: 1주, 좌측 0-padding 처리된 부호 포함 15자리 숫자 |
| `acnt_evlt_remn_indv_tot[].cur_prc` | 현재가 | 12 | 단위: 원, 좌측 0-padding 처리된 부호 포함 12자리 숫자 |
| `acnt_evlt_remn_indv_tot[].pred_buyq` | 전일매수수량 | 15 | 단위: 1주, 좌측 0-padding 처리된 부호 포함 15자리 숫자 |
| `acnt_evlt_remn_indv_tot[].pred_sellq` | 전일매도수량 | 15 | 단위: 1주, 좌측 0-padding 처리된 부호 포함 15자리 숫자 |
| `acnt_evlt_remn_indv_tot[].tdy_buyq` | 금일매수수량 | 15 | 단위: 1주, 좌측 0-padding 처리된 부호 포함 15자리 숫자 |
| `acnt_evlt_remn_indv_tot[].tdy_sellq` | 금일매도수량 | 15 | 단위: 1주, 좌측 0-padding 처리된 부호 포함 15자리 숫자 |
| `acnt_evlt_remn_indv_tot[].pur_amt` | 매입금액 | 15 | 단위: 원, 좌측 0-padding 처리된 부호 포함 15자리 숫자 |
| `acnt_evlt_remn_indv_tot[].pur_cmsn` | 매입수수료 | 15 | 단위: 원, 좌측 0-padding 처리된 부호 포함 15자리 숫자 |
| `acnt_evlt_remn_indv_tot[].evlt_amt` | 평가금액 | 15 | 단위: 원, 좌측 0-padding 처리된 부호 포함 15자리 숫자 |
| `acnt_evlt_remn_indv_tot[].sell_cmsn` | 평가수수료 | 15 | 단위: 원, 좌측 0-padding 처리된 부호 포함 15자리 숫자 |
| `acnt_evlt_remn_indv_tot[].tax` | 세금 | 15 | 단위: 원, 좌측 0-padding 처리된 부호 포함 15자리 숫자 |
| `acnt_evlt_remn_indv_tot[].sum_cmsn` | 수수료합 | 15 | 매입수수료 + 평가수수료 |
| `acnt_evlt_remn_indv_tot[].poss_rt` | 보유비중(%) | 12 | 단위: %, 소수점 둘째 자리까지 포맷된 백분율 |
| `acnt_evlt_remn_indv_tot[].crd_tp` | 신용구분 | 2 |   |
| `acnt_evlt_remn_indv_tot[].crd_tp_nm` | 신용구분명 | 4 |   |
| `acnt_evlt_remn_indv_tot[].crd_loan_dt` | 대출일 | 8 | YYYYMMDD |

<a id="kt50020"></a>

## `kt50020` · `gold_spot_balance()` — 금현물 잔고확인

금현물 잔고확인 (Gold Spot Balance) · `POST /api/dostk/acnt`

```python
api.account.gold_spot_balance()
```

**요청**

요청 필드 없음.

**응답**

| 필드 | 한글명 | 길이 | 설명 |
|---|---|---:|---|
| `tot_entr` | 예수금 | 12 | 단위: 원, 좌측 0-padding 처리된 부호 포함 12자리 숫자 |
| `net_entr` | 추정예수금 | 12 | 단위: 원, 좌측 0-padding 처리된 부호 포함 12자리 숫자 |
| `tot_est_amt` | 잔고평가액 | 12 | 단위: 원, 좌측 0-padding 처리된 부호 포함 12자리 숫자 |
| `net_amt` | 예탁자산평가액 | 12 | 단위: 원, 좌측 0-padding 처리된 부호 포함 12자리 숫자 |
| `tot_book_amt2` | 총매입금액 | 12 | 단위: 원, 좌측 0-padding 처리된 부호 포함 12자리 숫자 |
| `tot_dep_amt` | 추정예탁자산 | 12 | 단위: 원, 좌측 0-padding 처리된 부호 포함 12자리 숫자 |
| `paym_alowa` | 출금가능금액 | 12 | 단위: 원, 좌측 0-padding 처리된 부호 포함 12자리 숫자 |
| `pl_amt` | 실현손익 | 12 | 단위: 원, 좌측 0-padding 처리된 부호 포함 12자리 숫자 |
| `gold_acnt_evlt_prst` (list) | 금현물계좌평가현황 |  |   |
| `gold_acnt_evlt_prst[].stk_cd` | 종목코드 | 30 | 금 종목 코드 |
| `gold_acnt_evlt_prst[].stk_nm` | 종목명 | 12 | 금 종목 코드 설명 |
| `gold_acnt_evlt_prst[].real_qty` | 보유수량 | 12 | 단위: 1주, 좌측 0-padding 처리된 부호 포함 12자리 숫자 |
| `gold_acnt_evlt_prst[].avg_prc` | 평균단가 | 12 | 단위: 원, 좌측 0-padding 처리된 부호 포함 12자리 숫자 |
| `gold_acnt_evlt_prst[].cur_prc` | 현재가 | 12 | 단위: 원, 좌측 0-padding 처리된 부호 포함 12자리 숫자 |
| `gold_acnt_evlt_prst[].est_amt` | 평가금액 | 12 | 단위: 원, 좌측 0-padding 처리된 부호 포함 12자리 숫자 |
| `gold_acnt_evlt_prst[].est_lspft` | 손익금액 | 12 | 단위: 원, 좌측 0-padding 처리된 부호 포함 12자리 숫자 |
| `gold_acnt_evlt_prst[].est_ratio` | 손익율 | 12 | 단위: %, 소수점 넷째 자리까지 포맷된 백분율 |
| `gold_acnt_evlt_prst[].cmsn` | 수수료 | 12 | 단위: 원, 좌측 0-padding 처리된 부호 포함 12자리 숫자 |
| `gold_acnt_evlt_prst[].vlad_tax` | 부가가치세 | 12 | 단위: 원, 좌측 0-padding 처리된 부호 포함 12자리 숫자 |
| `gold_acnt_evlt_prst[].book_amt2` | 매입금액 | 12 | 단위: 원, 좌측 0-padding 처리된 부호 포함 12자리 숫자 |
| `gold_acnt_evlt_prst[].pl_prch_prc` | 손익분기매입가 | 12 | 단위: 원, 좌측 0-padding 처리된 부호 포함 12자리 숫자 |
| `gold_acnt_evlt_prst[].qty` | 결제잔고 | 12 | 단위: 1주, 좌측 0-padding 처리된 부호 포함 12자리 숫자 |
| `gold_acnt_evlt_prst[].buy_qty` | 매수수량 | 12 | 단위: 1주, 좌측 0-padding 처리된 부호 포함 12자리 숫자 |
| `gold_acnt_evlt_prst[].sell_qty` | 매도수량 | 12 | 단위: 1주, 좌측 0-padding 처리된 부호 포함 12자리 숫자 |
| `gold_acnt_evlt_prst[].able_qty` | 가능수량 | 12 | 단위: 1주, 좌측 0-padding 처리된 부호 포함 12자리 숫자 |

<a id="kt50021"></a>

## `kt50021` · `gold_spot_deposit()` — 금현물 예수금

금현물 예수금 (Gold Spot Deposit) · `POST /api/dostk/acnt`

```python
api.account.gold_spot_deposit()
```

**요청**

요청 필드 없음.

**응답**

| 필드 | 한글명 | 길이 | 설명 |
|---|---|---:|---|
| `entra` | 예수금 | 15 | 단위: 원, 좌측 0-padding 처리된 부호 포함 15자리 숫자 |
| `profa_ch` | 증거금현금 | 15 | 단위: 원, 좌측 0-padding 처리된 부호 포함 15자리 숫자 |
| `chck_ina_amt` | 수표입금액 | 15 | 단위: 원, 좌측 0-padding 처리된 부호 포함 15자리 숫자 |
| `etc_loan` | 기타대여금 | 15 | 단위: 원, 좌측 0-padding 처리된 부호 포함 15자리 숫자 |
| `etc_loan_dlfe` | 기타대여금연체료 | 15 | 단위: 원, 좌측 0-padding 처리된 부호 포함 15자리 숫자 |
| `etc_loan_tot` | 기타대여금합계 | 15 | 단위: 원, 좌측 0-padding 처리된 부호 포함 15자리 숫자 |
| `prsm_entra` | 추정예수금 | 15 | 단위: 원, 좌측 0-padding 처리된 부호 포함 15자리 숫자 |
| `buy_exct_amt` | 매수정산금 | 15 | 단위: 원, 좌측 0-padding 처리된 부호 포함 15자리 숫자 |
| `sell_exct_amt` | 매도정산금 | 15 | 단위: 원, 좌측 0-padding 처리된 부호 포함 15자리 숫자 |
| `sell_buy_exct_amt` | 매도매수정산금 | 15 | 단위: 원, 좌측 0-padding 처리된 부호 포함 15자리 숫자 |
| `dly_amt` | 미수변제소요금 | 15 | 단위: 원, 좌측 0-padding 처리된 부호 포함 15자리 숫자 |
| `prsm_pymn_alow_amt` | 추정출금가능금액 | 15 | 단위: 원, 좌측 0-padding 처리된 부호 포함 15자리 숫자 |
| `pymn_alow_amt` | 출금가능금액 | 15 | 단위: 원, 좌측 0-padding 처리된 부호 포함 15자리 숫자 |
| `ord_alow_amt` | 주문가능금액 | 15 | 단위: 원, 좌측 0-padding 처리된 부호 포함 15자리 숫자 |

<a id="kt50030"></a>

## `kt50030` · `gold_spot_order_execution_all()` — 금현물 주문체결전체조회

금현물 주문체결전체조회 (Gold Spot All Order Execution) · `POST /api/dostk/acnt`

```python
api.account.gold_spot_order_execution_all(ord_dt=..., mrkt_deal_tp=..., stk_bond_tp=..., slby_tp=...)
```

**요청**

| 필드 | 한글명 | 필수 | 길이 | 설명 |
|---|---|:---:|---:|---|
| `ord_dt` | 주문일자 | Y | 8 | YYYYMMDD |
| `qry_tp` | 조회구분 |  | 1 | 1: 주문순, 2: 역순 |
| `mrkt_deal_tp` | 시장구분 | Y | 1 | 5:KRX금현물, 5값으로 고정 |
| `stk_bond_tp` | 주식채권구분 | Y | 1 | 0:전체, 1:주식, 2:채권 |
| `slby_tp` | 매도수구분 | Y | 1 | 0:전체, 1:매도, 2:매수 |
| `stk_cd` | 종목코드 |  | 12 | M04020000: 금 99.99_1kg, M04020100: 미니금 99.99_100g, 전체 조회는 빈값('')으로 설정 |
| `fr_ord_no` | 시작주문번호 |  | 7 | 시작주문번호 입력 시 이전 주문은 조회되지 않음, 전체 조회는 빈값('')으로 설정 |
| `dmst_stex_tp` | 국내거래소구분 |  | 6 | %:(전체), KRX, NXT, SOR |

**응답**

| 필드 | 한글명 | 길이 | 설명 |
|---|---|---:|---|
| `acnt_ord_cntr_prst` (list) | 계좌별주문체결현황 |  |   |
| `acnt_ord_cntr_prst[].stk_bond_tp` | 주식채권구분 | 1 |   |
| `acnt_ord_cntr_prst[].ord_no` | 주문번호 | 7 | 주문번호 7자리 |
| `acnt_ord_cntr_prst[].stk_cd` | 상품코드 | 12 | 금 종목코드 9자리 |
| `acnt_ord_cntr_prst[].trde_tp` | 매매구분 | 12 |   |
| `acnt_ord_cntr_prst[].io_tp_nm` | 주문유형구분 | 20 |   |
| `acnt_ord_cntr_prst[].ord_qty` | 주문수량 | 10 | 단위: 1주, 좌측 0-padding 처리된 부호 포함 10자리 숫자 |
| `acnt_ord_cntr_prst[].ord_uv` | 주문단가 | 10 | 단위: 원, 좌측 0-padding 처리된 부호 포함 10자리 숫자 |
| `acnt_ord_cntr_prst[].cnfm_qty` | 확인수량 | 10 | 단위: 1주, 좌측 0-padding 처리된 부호 포함 10자리 숫자 |
| `acnt_ord_cntr_prst[].data_send_end_tp` | 접수구분 | 12 |   |
| `acnt_ord_cntr_prst[].mrkt_deal_tp` | 시장구분 | 1 |   |
| `acnt_ord_cntr_prst[].rsrv_tp` | 예약/반대여부 | 4 |   |
| `acnt_ord_cntr_prst[].orig_ord_no` | 원주문번호 | 7 | 원 주문이 없는 경우 '0000000'으로 출력 |
| `acnt_ord_cntr_prst[].stk_nm` | 종목명 | 40 |   |
| `acnt_ord_cntr_prst[].dcd_tp_nm` | 결제구분 | 4 |   |
| `acnt_ord_cntr_prst[].crd_deal_tp` | 신용거래구분 | 20 |   |
| `acnt_ord_cntr_prst[].cntr_qty` | 체결수량 | 10 | 단위: 1주, 좌측 0-padding 처리된 부호 포함 10자리 숫자 |
| `acnt_ord_cntr_prst[].cntr_uv` | 체결단가 | 10 | 단위: 원, 좌측 0-padding 처리된 부호 포함 10자리 숫자 |
| `acnt_ord_cntr_prst[].ord_remnq` | 미체결수량 | 10 | 단위: 1주, 좌측 0-padding 처리된 부호 포함 10자리 숫자 |
| `acnt_ord_cntr_prst[].comm_ord_tp` | 통신구분 | 10 |   |
| `acnt_ord_cntr_prst[].mdfy_cncl_tp` | 정정취소구분 | 20 |   |
| `acnt_ord_cntr_prst[].dmst_stex_tp` | 국내거래소구분 | 6 |   |
| `acnt_ord_cntr_prst[].cond_uv` | 스톱가 | 10 | 단위: 원, 좌측 0-padding 처리된 부호 포함 10자리 숫자 |

<a id="kt50031"></a>

## `kt50031` · `gold_spot_order_execution()` — 금현물 주문체결조회

금현물 주문체결조회 (Gold Spot Order Execution) · `POST /api/dostk/acnt`

```python
api.account.gold_spot_order_execution(qry_tp=..., stk_bond_tp=..., sell_tp=..., dmst_stex_tp=...)
```

**요청**

| 필드 | 한글명 | 필수 | 길이 | 설명 |
|---|---|:---:|---:|---|
| `ord_dt` | 주문일자 |  | 8 | YYYYMMDD |
| `qry_tp` | 조회구분 | Y | 1 | 1:주문순, 2:역순, 3:미체결, 4:체결내역만 |
| `stk_bond_tp` | 주식채권구분 | Y | 1 | 0:전체, 1:주식, 2:채권 |
| `sell_tp` | 매도수구분 | Y | 1 | 0:전체, 1:매도, 2:매수 |
| `stk_cd` | 종목코드 |  | 12 | M04020000: 금 99.99_1kg, M04020100: 미니금 99.99_100g, 전체 조회는 빈값('')으로 설정 |
| `fr_ord_no` | 시작주문번호 |  | 7 | 시작주문번호 입력 시 이전 주문은 조회되지 않음, 전체 조회는 빈값('')으로 설정 |
| `dmst_stex_tp` | 국내거래소구분 | Y | 6 | %:(전체),KRX:한국거래소,NXT:넥스트트레이드,SOR:최선주문집행 |

**응답**

| 필드 | 한글명 | 길이 | 설명 |
|---|---|---:|---|
| `acnt_ord_cntr_prps_dtl` (list) | 계좌별주문체결내역상세 |  |   |
| `acnt_ord_cntr_prps_dtl[].ord_no` | 주문번호 | 7 | 주문번호 7자리 |
| `acnt_ord_cntr_prps_dtl[].stk_cd` | 종목번호 | 12 | 금 종목코드 9자리 |
| `acnt_ord_cntr_prps_dtl[].trde_tp` | 매매구분 | 20 |   |
| `acnt_ord_cntr_prps_dtl[].crd_tp` | 신용구분 | 20 |   |
| `acnt_ord_cntr_prps_dtl[].ord_qty` | 주문수량 | 10 | 단위: 1주, 좌측 0-padding 처리된 부호 포함 10자리 숫자 |
| `acnt_ord_cntr_prps_dtl[].ord_uv` | 주문단가 | 10 | 단위: 원, 좌측 0-padding 처리된 부호 포함 10자리 숫자 |
| `acnt_ord_cntr_prps_dtl[].cnfm_qty` | 확인수량 | 10 | 단위: 1주, 좌측 0-padding 처리된 부호 포함 10자리 숫자 |
| `acnt_ord_cntr_prps_dtl[].acpt_tp` | 접수구분 | 20 |   |
| `acnt_ord_cntr_prps_dtl[].rsrv_tp` | 반대여부 | 20 |   |
| `acnt_ord_cntr_prps_dtl[].ord_tm` | 주문시간 | 8 | HH:mm:ss |
| `acnt_ord_cntr_prps_dtl[].ori_ord` | 원주문 | 7 | 원 주문이 없는 경우 '0000000'으로 출력 |
| `acnt_ord_cntr_prps_dtl[].stk_nm` | 종목명 | 40 |   |
| `acnt_ord_cntr_prps_dtl[].io_tp_nm` | 주문구분 | 20 |   |
| `acnt_ord_cntr_prps_dtl[].loan_dt` | 대출일 | 8 | YYYYMMDD |
| `acnt_ord_cntr_prps_dtl[].cntr_qty` | 체결수량 | 10 | 단위: 1주, 좌측 0-padding 처리된 부호 포함 10자리 숫자 |
| `acnt_ord_cntr_prps_dtl[].cntr_uv` | 체결단가 | 10 | 단위: 원, 좌측 0-padding 처리된 부호 포함 10자리 숫자 |
| `acnt_ord_cntr_prps_dtl[].ord_remnq` | 주문잔량 | 10 | 단위: 1주, 좌측 0-padding 처리된 부호 포함 10자리 숫자 |
| `acnt_ord_cntr_prps_dtl[].comm_ord_tp` | 통신구분 | 20 |   |
| `acnt_ord_cntr_prps_dtl[].mdfy_cncl` | 정정취소 | 20 |   |
| `acnt_ord_cntr_prps_dtl[].cnfm_tm` | 확인시간 | 8 | HH:mm:ss |
| `acnt_ord_cntr_prps_dtl[].dmst_stex_tp` | 국내거래소구분 | 8 |   |
| `acnt_ord_cntr_prps_dtl[].cond_uv` | 스톱가 | 10 | 단위: 원, 좌측 0-padding 처리된 부호 포함 10자리 숫자 |

<a id="kt50032"></a>

## `kt50032` · `gold_spot_transaction_history()` — 금현물 거래내역조회

금현물 거래내역조회 (Gold Spot Transaction History) · `POST /api/dostk/acnt`

```python
api.account.gold_spot_transaction_history()
```

**요청**

| 필드 | 한글명 | 필수 | 길이 | 설명 |
|---|---|:---:|---:|---|
| `strt_dt` | 시작일자 |  | 8 | YYYYMMDD |
| `end_dt` | 종료일자 |  | 8 | YYYYMMDD |
| `tp` | 구분 |  | 1 | 0:전체, 1:입출금, 2:출고, 3:매매, 4:매수, 5:매도, 6:입금, 7:출금 |
| `stk_cd` | 종목코드 |  | 12 | M04020000: 금 99.99_1kg, M04020100: 미니금 99.99_100g, 전체 조회는 빈값('')으로 설정 |

**응답**

| 필드 | 한글명 | 길이 | 설명 |
|---|---|---:|---|
| `acnt_print` | 계좌번호 | 62 | 계좌번호 출력용 |
| `gold_trde_hist` (list) | 금현물거래내역 |  |   |
| `gold_trde_hist[].deal_dt` | 거래일자 | 8 | YYYYMMDD |
| `gold_trde_hist[].deal_no` | 거래번호 | 9 | 거래번호 9자리 |
| `gold_trde_hist[].rmrk_nm` | 적요명 | 60 |   |
| `gold_trde_hist[].deal_qty` | 거래수량 | 15 | 단위: 1주, 좌측 0-padding 처리된 부호 포함 15자리 숫자 |
| `gold_trde_hist[].gold_spot_vat` | 금현물부가가치세 | 15 | 단위: 원, 좌측 0-padding 처리된 부호 포함 15자리 숫자 |
| `gold_trde_hist[].exct_amt` | 정산금액 | 15 | 단위: 원, 좌측 0-padding 처리된 부호 포함 15자리 숫자 |
| `gold_trde_hist[].dly_sum` | 연체합 | 15 | 단위: 원, 좌측 0-padding 처리된 부호 포함 15자리 숫자 |
| `gold_trde_hist[].entra_remn` | 예수금잔고 | 15 | 단위: 원, 좌측 0-padding 처리된 부호 포함 15자리 숫자 |
| `gold_trde_hist[].mdia_nm` | 메체구분명 | 20 |   |
| `gold_trde_hist[].orig_deal_no` | 원거래번호 | 7 | 원 주문이 없는 경우 '0000000'으로 출력 |
| `gold_trde_hist[].stk_nm` | 종목명 | 40 |   |
| `gold_trde_hist[].uv_exrt` | 거래단가 | 15 |   |
| `gold_trde_hist[].cmsn` | 수수료 | 15 | 단위: 원, 좌측 0-padding 처리된 부호 포함 15자리 숫자 |
| `gold_trde_hist[].uncl_ocr` | 미수(원/g) | 15 | 단위: 원, 좌측 0-padding 처리된 부호 포함 15자리 숫자 |
| `gold_trde_hist[].rpym_sum` | 변제합 | 15 | 단위: 원, 좌측 0-padding 처리된 부호 포함 15자리 숫자 |
| `gold_trde_hist[].spot_remn` | 현물잔고 | 15 | 단위: 1주, 좌측 0-padding 처리된 부호 포함 15자리 숫자 |
| `gold_trde_hist[].proc_time` | 처리시간 | 8 | HH:mm:ss |
| `gold_trde_hist[].rcpy_no` | 출납번호 | 9 | 출납번호 9자리 |
| `gold_trde_hist[].stk_cd` | 종목코드 | 12 | 금 종목 코드 |
| `gold_trde_hist[].deal_amt` | 거래금액 | 15 | 단위: 원, 좌측 0-padding 처리된 부호 포함 15자리 숫자 |
| `gold_trde_hist[].tax_tot_amt` | 소득/주민세 | 15 | 단위: 원, 좌측 0-padding 처리된 부호 포함 15자리 숫자 |
| `gold_trde_hist[].cntr_dt` | 체결일 | 8 | YYYYMMDD |
| `gold_trde_hist[].proc_brch_nm` | 처리점 | 20 |   |
| `gold_trde_hist[].prcsr` | 처리자 | 20 |   |

<a id="kt50075"></a>

## `kt50075` · `gold_spot_unfilled_orders()` — 금현물 미체결조회

금현물 미체결조회 (Gold Spot Unfilled Orders) · `POST /api/dostk/acnt`

```python
api.account.gold_spot_unfilled_orders(ord_dt=..., mrkt_deal_tp=..., stk_bond_tp=..., sell_tp=...)
```

**요청**

| 필드 | 한글명 | 필수 | 길이 | 설명 |
|---|---|:---:|---:|---|
| `ord_dt` | 주문일자 | Y | 8 | YYYYMMDD |
| `qry_tp` | 조회구분 |  | 1 | 1: 주문순, 2: 역순 |
| `mrkt_deal_tp` | 시장구분 | Y | 1 | 5:KRW금현물, 5값으로 고정 |
| `stk_bond_tp` | 주식채권구분 | Y | 1 | 0:전체, 1:주식, 2:채권 |
| `sell_tp` | 매도수구분 | Y | 1 | 0:전체, 1:매도, 2:매수 |
| `stk_cd` | 종목코드 |  | 12 | M04020000: 금 99.99_1kg, M04020100: 미니금 99.99_100g, 전체 조회는 빈값('')으로 설정 |
| `fr_ord_no` | 시작주문번호 |  | 7 | 시작주문번호 입력 시 이전 주문은 조회되지 않음, 전체 조회는 빈값('')으로 설정 |
| `dmst_stex_tp` | 국내거래소구분 |  | 6 | %:(전체), KRX, NXT, SOR |

**응답**

| 필드 | 한글명 | 길이 | 설명 |
|---|---|---:|---|
| `acnt_ord_oso_prst` (list) | 계좌별주문미체결현황 |  |   |
| `acnt_ord_oso_prst[].stk_bond_tp` | 주식채권구분 | 1 |   |
| `acnt_ord_oso_prst[].ord_no` | 주문번호 | 7 | 주문번호 7자리 |
| `acnt_ord_oso_prst[].stk_cd` | 상품코드 | 12 | 금 종목코드 9자리 |
| `acnt_ord_oso_prst[].trde_tp` | 매매구분 | 12 |   |
| `acnt_ord_oso_prst[].io_tp_nm` | 주문유형구분 | 20 |   |
| `acnt_ord_oso_prst[].ord_qty` | 주문수량 | 10 | 단위: 1주, 좌측 0-padding 처리된 부호 포함 10자리 숫자 |
| `acnt_ord_oso_prst[].ord_uv` | 주문단가 | 10 | 단위: 1주, 좌측 0-padding 처리된 부호 포함 10자리 숫자 |
| `acnt_ord_oso_prst[].cnfm_qty` | 확인수량 | 10 | 단위: 1주, 좌측 0-padding 처리된 부호 포함 10자리 숫자 |
| `acnt_ord_oso_prst[].data_send_end_tp` | 접수구분 | 12 |   |
| `acnt_ord_oso_prst[].mrkt_deal_tp` | 시장구분 | 1 |   |
| `acnt_ord_oso_prst[].rsrv_tp` | 예약/반대여부 | 4 |   |
| `acnt_ord_oso_prst[].orig_ord_no` | 원주문번호 | 7 | 원 주문이 없는 경우 '0000000'으로 출력 |
| `acnt_ord_oso_prst[].stk_nm` | 종목명 | 40 |   |
| `acnt_ord_oso_prst[].dcd_tp_nm` | 결제구분 | 4 |   |
| `acnt_ord_oso_prst[].crd_deal_tp` | 신용거래구분 | 20 |   |
| `acnt_ord_oso_prst[].cntr_qty` | 체결수량 | 10 | 단위: 1주, 좌측 0-padding 처리된 부호 포함 10자리 숫자 |
| `acnt_ord_oso_prst[].cntr_uv` | 체결단가 | 10 | 단위: 원, 좌측 0-padding 처리된 부호 포함 10자리 숫자 |
| `acnt_ord_oso_prst[].ord_remnq` | 미체결수량 | 10 | 단위: 1주, 좌측 0-padding 처리된 부호 포함 10자리 숫자 |
| `acnt_ord_oso_prst[].comm_ord_tp` | 통신구분 | 10 |   |
| `acnt_ord_oso_prst[].mdfy_cncl_tp` | 정정취소구분 | 20 |   |
| `acnt_ord_oso_prst[].dmst_stex_tp` | 국내거래소구분 | 6 |   |
| `acnt_ord_oso_prst[].cond_uv` | 스톱가 | 10 | 단위: 원, 좌측 0-padding 처리된 부호 포함 10자리 숫자 |
