<!-- 자동 생성 파일 — 손으로 고치지 마세요. `python scripts/gen_docs.py` 가 TR 카탈로그(kiwoom_client.spec)로 다시 만듭니다. -->

# `api.stock_info` — 종목정보 (Stock Information)

요청·응답 필드는 키움 공식 REST API 명세에서 만든 TR 카탈로그([출처·라이선스](https://github.com/younghwan91/kiwoom-client/blob/main/src/kiwoom_client/spec/SOURCE.md))에서 옮긴 필드 ID·한글명·필수·길이입니다. 필드 설명·코드값은 싣지 않으니 [키움 REST API 포털](https://openapi.kiwoom.com) 문서를 보세요(자주 쓰는 코드값은 `kiwoom_client.codes`). 값은 모두 문자열로 넘깁니다.

공통 헤더(`api-id`·`cont-yn`·`next-key`·`authorization`)는 라이브러리가 채웁니다 — 연속조회는 메서드의 `cont_yn`·`next_key` 인자나 `request_all()` 을 쓰세요.

| api_id | 메서드 | 이름 |
|---|---|---|
| [`ka00198`](#ka00198) | `realtime_stock_inquiry_rank()` | 실시간종목조회순위 |
| [`ka10001`](#ka10001) | `basic_stock_info()` | 주식기본정보요청 |
| [`ka10002`](#ka10002) | `stock_trading_agent()` | 주식거래원요청 |
| [`ka10003`](#ka10003) | `execution_info()` | 체결정보요청 |
| [`ka10013`](#ka10013) | `credit_trading_trend()` | 신용매매동향요청 |
| [`ka10015`](#ka10015) | `daily_transaction_detail()` | 일별거래상세요청 |
| [`ka10016`](#ka10016) | `new_high_low()` | 신고저가요청 |
| [`ka10017`](#ka10017) | `upper_lower_limit()` | 상하한가요청 |
| [`ka10018`](#ka10018) | `near_high_low()` | 고저가근접요청 |
| [`ka10019`](#ka10019) | `rapid_price_change()` | 가격급등락요청 |
| [`ka10024`](#ka10024) | `trading_volume_update()` | 거래량갱신요청 |
| [`ka10025`](#ka10025) | `volume_concentration()` | 매물대집중요청 |
| [`ka10026`](#ka10026) | `high_low_per()` | 고저PER요청 |
| [`ka10028`](#ka10028) | `change_rate_vs_opening()` | 시가대비등락률요청 |
| [`ka10043`](#ka10043) | `trading_agent_supply_demand()` | 거래원매물대분석요청 |
| [`ka10052`](#ka10052) | `trading_agent_instant_volume()` | 거래원순간거래량요청 |
| [`ka10054`](#ka10054) | `vi_triggered_stocks()` | 변동성완화장치발동종목요청 |
| [`ka10055`](#ka10055) | `today_vs_yesterday_volume()` | 당일전일체결량요청 |
| [`ka10058`](#ka10058) | `daily_trading_by_investor()` | 투자자별일별매매종목요청 |
| [`ka10059`](#ka10059) | `investor_institution_by_stock()` | 종목별투자자기관별요청 |
| [`ka10061`](#ka10061) | `investor_institution_aggregate()` | 종목별투자자기관별합계요청 |
| [`ka10084`](#ka10084) | `today_vs_yesterday_execution()` | 당일전일체결요청 |
| [`ka10095`](#ka10095) | `watchlist_stock_info()` | 지정종목 정보요청 |
| [`ka10099`](#ka10099) | `stock_info_list()` | 종목정보 리스트 |
| [`ka10100`](#ka10100) | `stock_info_inquiry()` | 종목정보 조회 |
| [`ka10101`](#ka10101) | `industry_code_list()` | 업종코드 리스트 |
| [`ka10102`](#ka10102) | `member_company_list()` | 회원사 리스트 |
| [`ka90003`](#ka90003) | `program_buy_top50()` | 프로그램순매수상위50요청 |
| [`ka90004`](#ka90004) | `program_trading_by_stock()` | 종목별프로그램매매현황요청 |
| [`kt20016`](#kt20016) | `margin_loan_available_stocks()` | 신용융자 가능종목요청 |
| [`kt20017`](#kt20017) | `margin_loan_inquiry()` | 신용융자 가능문의 |

<a id="ka00198"></a>

## `ka00198` · `realtime_stock_inquiry_rank()` — 실시간종목조회순위

실시간종목조회순위 (Real-time Stock Inquiry Ranking) · `POST /api/dostk/stkinfo`

```python
api.stock_info.realtime_stock_inquiry_rank(qry_tp=...)
```

**요청**

| 필드 | 한글명 | 필수 | 길이 |
|---|---|:---:|---:|
| `qry_tp` | 구분 | Y | 1 |

**응답**

| 필드 | 한글명 | 길이 |
|---|---|---:|
| `item_inq_rank` (list) | 실시간종목조회순위 |  |
| `item_inq_rank[].stk_nm` | 종목명 | 40 |
| `item_inq_rank[].bigd_rank` | 빅데이터 순위 | 20 |
| `item_inq_rank[].rank_chg` | 순위 등락 | 20 |
| `item_inq_rank[].rank_chg_sign` | 순위 등락 부호 | 20 |
| `item_inq_rank[].past_curr_prc` | 과거 현재가 | 20 |
| `item_inq_rank[].base_comp_sign` | 기준가 대비 부호 | 20 |
| `item_inq_rank[].base_comp_chgr` | 기준가 대비 등락율 | 20 |
| `item_inq_rank[].prev_base_sign` | 직전 기준 대비 부호 | 20 |
| `item_inq_rank[].prev_base_chgr` | 직전 기준 대비 등락율 | 20 |
| `item_inq_rank[].dt` | 일자 | 20 |
| `item_inq_rank[].tm` | 시간 | 20 |
| `item_inq_rank[].stk_cd` | 종목코드 | 20 |

<a id="ka10001"></a>

## `ka10001` · `basic_stock_info()` — 주식기본정보요청

종목기본정보요청 (Basic Stock Info) · `POST /api/dostk/stkinfo`

```python
api.stock_info.basic_stock_info(stk_cd=...)
```

**요청**

| 필드 | 한글명 | 필수 | 길이 |
|---|---|:---:|---:|
| `stk_cd` | 종목코드 | Y | 20 |

**응답**

| 필드 | 한글명 | 길이 |
|---|---|---:|
| `stk_cd` | 종목코드 | 20 |
| `stk_nm` | 종목명 | 40 |
| `setl_mm` | 결산월 | 20 |
| `fav` | 액면가 | 20 |
| `cap` | 자본금 | 20 |
| `flo_stk` | 상장주식 | 20 |
| `crd_rt` | 신용비율 | 20 |
| `oyr_hgst` | 연중최고 | 20 |
| `oyr_lwst` | 연중최저 | 20 |
| `mac` | 시가총액 | 20 |
| `mac_wght` | 시가총액비중 | 20 |
| `for_exh_rt` | 외인소진률 | 20 |
| `repl_pric` | 대용가 | 20 |
| `per` | PER | 20 |
| `eps` | EPS | 20 |
| `roe` | ROE | 20 |
| `pbr` | PBR | 20 |
| `ev` | EV | 20 |
| `bps` | BPS | 20 |
| `sale_amt` | 매출액 | 20 |
| `bus_pro` | 영업이익 | 20 |
| `cup_nga` | 당기순이익 | 20 |
| `250hgst` | 250최고 | 20 |
| `250lwst` | 250최저 | 20 |
| `high_pric` | 고가 | 20 |
| `open_pric` | 시가 | 20 |
| `low_pric` | 저가 | 20 |
| `upl_pric` | 상한가 | 20 |
| `lst_pric` | 하한가 | 20 |
| `base_pric` | 기준가 | 20 |
| `exp_cntr_pric` | 예상체결가 | 20 |
| `exp_cntr_qty` | 예상체결수량 | 20 |
| `250hgst_pric_dt` | 250최고가일 | 20 |
| `250hgst_pric_pre_rt` | 250최고가대비율 | 20 |
| `250lwst_pric_dt` | 250최저가일 | 20 |
| `250lwst_pric_pre_rt` | 250최저가대비율 | 20 |
| `cur_prc` | 현재가 | 20 |
| `pre_sig` | 대비기호 | 20 |
| `pred_pre` | 전일대비 | 20 |
| `flu_rt` | 등락율 | 20 |
| `trde_qty` | 거래량 | 20 |
| `trde_pre` | 거래대비 | 20 |
| `fav_unit` | 액면가단위 | 20 |
| `dstr_stk` | 유통주식 | 20 |
| `dstr_rt` | 유통비율 | 20 |

<a id="ka10002"></a>

## `ka10002` · `stock_trading_agent()` — 주식거래원요청

종목거래원요청 (Stock Trading Agent) · `POST /api/dostk/stkinfo`

```python
api.stock_info.stock_trading_agent(stk_cd=...)
```

**요청**

| 필드 | 한글명 | 필수 | 길이 |
|---|---|:---:|---:|
| `stk_cd` | 종목코드 | Y | 20 |

**응답**

| 필드 | 한글명 | 길이 |
|---|---|---:|
| `stk_cd` | 종목코드 | 20 |
| `stk_nm` | 종목명 | 40 |
| `cur_prc` | 현재가 | 20 |
| `flu_smbol` | 등락부호 | 20 |
| `base_pric` | 기준가 | 20 |
| `pred_pre` | 전일대비 | 20 |
| `flu_rt` | 등락율 | 20 |
| `sel_trde_ori_nm_1` | 매도거래원명1 | 20 |
| `sel_trde_ori_1` | 매도거래원1 | 20 |
| `sel_trde_qty_1` | 매도거래량1 | 20 |
| `buy_trde_ori_nm_1` | 매수거래원명1 | 20 |
| `buy_trde_ori_1` | 매수거래원1 | 20 |
| `buy_trde_qty_1` | 매수거래량1 | 20 |
| `sel_trde_ori_nm_2` | 매도거래원명2 | 20 |
| `sel_trde_ori_2` | 매도거래원2 | 20 |
| `sel_trde_qty_2` | 매도거래량2 | 20 |
| `buy_trde_ori_nm_2` | 매수거래원명2 | 20 |
| `buy_trde_ori_2` | 매수거래원2 | 20 |
| `buy_trde_qty_2` | 매수거래량2 | 20 |
| `sel_trde_ori_nm_3` | 매도거래원명3 | 20 |
| `sel_trde_ori_3` | 매도거래원3 | 20 |
| `sel_trde_qty_3` | 매도거래량3 | 20 |
| `buy_trde_ori_nm_3` | 매수거래원명3 | 20 |
| `buy_trde_ori_3` | 매수거래원3 | 20 |
| `buy_trde_qty_3` | 매수거래량3 | 20 |
| `sel_trde_ori_nm_4` | 매도거래원명4 | 20 |
| `sel_trde_ori_4` | 매도거래원4 | 20 |
| `sel_trde_qty_4` | 매도거래량4 | 20 |
| `buy_trde_ori_nm_4` | 매수거래원명4 | 20 |
| `buy_trde_ori_4` | 매수거래원4 | 20 |
| `buy_trde_qty_4` | 매수거래량4 | 20 |
| `sel_trde_ori_nm_5` | 매도거래원명5 | 20 |
| `sel_trde_ori_5` | 매도거래원5 | 20 |
| `sel_trde_qty_5` | 매도거래량5 | 20 |
| `buy_trde_ori_nm_5` | 매수거래원명5 | 20 |
| `buy_trde_ori_5` | 매수거래원5 | 20 |
| `buy_trde_qty_5` | 매수거래량5 | 20 |

<a id="ka10003"></a>

## `ka10003` · `execution_info()` — 체결정보요청

체결정보요청 (Execution Info) · `POST /api/dostk/stkinfo`

```python
api.stock_info.execution_info(stk_cd=...)
```

**요청**

| 필드 | 한글명 | 필수 | 길이 |
|---|---|:---:|---:|
| `stk_cd` | 종목코드 | Y | 20 |

**응답**

| 필드 | 한글명 | 길이 |
|---|---|---:|
| `cntr_infr` (list) | 체결정보 |  |
| `cntr_infr[].tm` | 시간 | 20 |
| `cntr_infr[].cur_prc` | 현재가 | 20 |
| `cntr_infr[].pred_pre` | 전일대비 | 20 |
| `cntr_infr[].pre_rt` | 대비율 | 20 |
| `cntr_infr[].pri_sel_bid_unit` | 우선매도호가단위 | 20 |
| `cntr_infr[].pri_buy_bid_unit` | 우선매수호가단위 | 20 |
| `cntr_infr[].cntr_trde_qty` | 체결거래량 | 20 |
| `cntr_infr[].sign` | sign | 20 |
| `cntr_infr[].acc_trde_qty` | 누적거래량 | 20 |
| `cntr_infr[].acc_trde_prica` | 누적거래대금 | 20 |
| `cntr_infr[].cntr_str` | 체결강도 | 20 |
| `cntr_infr[].stex_tp` | 거래소구분 | 20 |

<a id="ka10013"></a>

## `ka10013` · `credit_trading_trend()` — 신용매매동향요청

신용매매동향요청 (Credit Trading Trend) · `POST /api/dostk/stkinfo`

```python
api.stock_info.credit_trading_trend(stk_cd=..., dt=..., qry_tp=...)
```

**요청**

| 필드 | 한글명 | 필수 | 길이 |
|---|---|:---:|---:|
| `stk_cd` | 종목코드 | Y | 20 |
| `dt` | 일자 | Y | 8 |
| `qry_tp` | 조회구분 | Y | 1 |

**응답**

| 필드 | 한글명 | 길이 |
|---|---|---:|
| `crd_trde_trend` (list) | 신용매매동향 |  |
| `crd_trde_trend[].dt` | 일자 | 20 |
| `crd_trde_trend[].cur_prc` | 현재가 | 20 |
| `crd_trde_trend[].pred_pre_sig` | 전일대비기호 | 20 |
| `crd_trde_trend[].pred_pre` | 전일대비 | 20 |
| `crd_trde_trend[].trde_qty` | 거래량 | 20 |
| `crd_trde_trend[].new` | 신규 | 20 |
| `crd_trde_trend[].rpya` | 상환 | 20 |
| `crd_trde_trend[].remn` | 잔고 | 20 |
| `crd_trde_trend[].amt` | 금액 | 20 |
| `crd_trde_trend[].pre` | 대비 | 20 |
| `crd_trde_trend[].shr_rt` | 공여율 | 20 |
| `crd_trde_trend[].remn_rt` | 잔고율 | 20 |

<a id="ka10015"></a>

## `ka10015` · `daily_transaction_detail()` — 일별거래상세요청

일별거래상세요청 (Daily Transaction Detail) · `POST /api/dostk/stkinfo`

```python
api.stock_info.daily_transaction_detail(stk_cd=..., strt_dt=...)
```

**요청**

| 필드 | 한글명 | 필수 | 길이 |
|---|---|:---:|---:|
| `stk_cd` | 종목코드 | Y | 20 |
| `strt_dt` | 시작일자 | Y | 8 |

**응답**

| 필드 | 한글명 | 길이 |
|---|---|---:|
| `daly_trde_dtl` (list) | 일별거래상세 |  |
| `daly_trde_dtl[].dt` | 일자 | 20 |
| `daly_trde_dtl[].close_pric` | 종가 | 20 |
| `daly_trde_dtl[].pred_pre_sig` | 전일대비기호 | 20 |
| `daly_trde_dtl[].pred_pre` | 전일대비 | 20 |
| `daly_trde_dtl[].flu_rt` | 등락율 | 20 |
| `daly_trde_dtl[].trde_qty` | 거래량 | 20 |
| `daly_trde_dtl[].trde_prica` | 거래대금 | 20 |
| `daly_trde_dtl[].bf_mkrt_trde_qty` | 장전거래량 | 20 |
| `daly_trde_dtl[].bf_mkrt_trde_wght` | 장전거래비중 | 20 |
| `daly_trde_dtl[].opmr_trde_qty` | 장중거래량 | 20 |
| `daly_trde_dtl[].opmr_trde_wght` | 장중거래비중 | 20 |
| `daly_trde_dtl[].af_mkrt_trde_qty` | 장후거래량 | 20 |
| `daly_trde_dtl[].af_mkrt_trde_wght` | 장후거래비중 | 20 |
| `daly_trde_dtl[].tot_3` | 합계3 | 20 |
| `daly_trde_dtl[].prid_trde_qty` | 기간중거래량 | 20 |
| `daly_trde_dtl[].cntr_str` | 체결강도 | 20 |
| `daly_trde_dtl[].for_poss` | 외인보유 | 20 |
| `daly_trde_dtl[].for_wght` | 외인비중 | 20 |
| `daly_trde_dtl[].for_netprps` | 외인순매수 | 20 |
| `daly_trde_dtl[].orgn_netprps` | 기관순매수 | 20 |
| `daly_trde_dtl[].ind_netprps` | 개인순매수 | 20 |
| `daly_trde_dtl[].frgn` | 외국계 | 20 |
| `daly_trde_dtl[].crd_remn_rt` | 신용잔고율 | 20 |
| `daly_trde_dtl[].prm` | 프로그램 | 20 |
| `daly_trde_dtl[].bf_mkrt_trde_prica` | 장전거래대금 | 20 |
| `daly_trde_dtl[].bf_mkrt_trde_prica_wght` | 장전거래대금비중 | 20 |
| `daly_trde_dtl[].opmr_trde_prica` | 장중거래대금 | 20 |
| `daly_trde_dtl[].opmr_trde_prica_wght` | 장중거래대금비중 | 20 |
| `daly_trde_dtl[].af_mkrt_trde_prica` | 장후거래대금 | 20 |
| `daly_trde_dtl[].af_mkrt_trde_prica_wght` | 장후거래대금비중 | 20 |

<a id="ka10016"></a>

## `ka10016` · `new_high_low()` — 신고저가요청

신고저가요청 (New High/Low) · `POST /api/dostk/stkinfo`

```python
api.stock_info.new_high_low(mrkt_tp=..., ntl_tp=..., high_low_close_tp=..., stk_cnd=..., trde_qty_tp=..., crd_cnd=..., updown_incls=..., dt=..., stex_tp=...)
```

**요청**

| 필드 | 한글명 | 필수 | 길이 |
|---|---|:---:|---:|
| `mrkt_tp` | 시장구분 | Y | 3 |
| `ntl_tp` | 신고저구분 | Y | 1 |
| `high_low_close_tp` | 고저종구분 | Y | 1 |
| `stk_cnd` | 종목조건 | Y | 1 |
| `trde_qty_tp` | 거래량구분 | Y | 5 |
| `crd_cnd` | 신용조건 | Y | 1 |
| `updown_incls` | 상하한포함 | Y | 1 |
| `dt` | 기간 | Y | 3 |
| `stex_tp` | 거래소구분 | Y | 1 |

**응답**

| 필드 | 한글명 | 길이 |
|---|---|---:|
| `ntl_pric` (list) | 신고저가 |  |
| `ntl_pric[].stk_cd` | 종목코드 | 20 |
| `ntl_pric[].stk_nm` | 종목명 | 40 |
| `ntl_pric[].cur_prc` | 현재가 | 20 |
| `ntl_pric[].pred_pre_sig` | 전일대비기호 | 20 |
| `ntl_pric[].pred_pre` | 전일대비 | 20 |
| `ntl_pric[].flu_rt` | 등락률 | 20 |
| `ntl_pric[].trde_qty` | 거래량 | 20 |
| `ntl_pric[].pred_trde_qty_pre_rt` | 전일거래량대비율 | 20 |
| `ntl_pric[].sel_bid` | 매도호가 | 20 |
| `ntl_pric[].buy_bid` | 매수호가 | 20 |
| `ntl_pric[].high_pric` | 고가 | 20 |
| `ntl_pric[].low_pric` | 저가 | 20 |

<a id="ka10017"></a>

## `ka10017` · `upper_lower_limit()` — 상하한가요청

상하한가요청 (Upper/Lower Limit Price) · `POST /api/dostk/stkinfo`

```python
api.stock_info.upper_lower_limit(mrkt_tp=..., updown_tp=..., sort_tp=..., stk_cnd=..., trde_qty_tp=..., crd_cnd=..., trde_gold_tp=..., stex_tp=...)
```

**요청**

| 필드 | 한글명 | 필수 | 길이 |
|---|---|:---:|---:|
| `mrkt_tp` | 시장구분 | Y | 3 |
| `updown_tp` | 상하한구분 | Y | 1 |
| `sort_tp` | 정렬구분 | Y | 1 |
| `stk_cnd` | 종목조건 | Y | 1 |
| `trde_qty_tp` | 거래량구분 | Y | 5 |
| `crd_cnd` | 신용조건 | Y | 1 |
| `trde_gold_tp` | 매매금구분 | Y | 1 |
| `stex_tp` | 거래소구분 | Y | 1 |

**응답**

| 필드 | 한글명 | 길이 |
|---|---|---:|
| `updown_pric` (list) | 상하한가 |  |
| `updown_pric[].stk_cd` | 종목코드 | 20 |
| `updown_pric[].stk_infr` | 종목정보 | 20 |
| `updown_pric[].stk_nm` | 종목명 | 40 |
| `updown_pric[].cur_prc` | 현재가 | 20 |
| `updown_pric[].pred_pre_sig` | 전일대비기호 | 20 |
| `updown_pric[].pred_pre` | 전일대비 | 20 |
| `updown_pric[].flu_rt` | 등락률 | 20 |
| `updown_pric[].trde_qty` | 거래량 | 20 |
| `updown_pric[].pred_trde_qty` | 전일거래량 | 20 |
| `updown_pric[].sel_req` | 매도잔량 | 20 |
| `updown_pric[].sel_bid` | 매도호가 | 20 |
| `updown_pric[].buy_bid` | 매수호가 | 20 |
| `updown_pric[].buy_req` | 매수잔량 | 20 |
| `updown_pric[].cnt` | 횟수 | 20 |

<a id="ka10018"></a>

## `ka10018` · `near_high_low()` — 고저가근접요청

고저근접요청 (Near High/Low) · `POST /api/dostk/stkinfo`

```python
api.stock_info.near_high_low(high_low_tp=..., alacc_rt=..., mrkt_tp=..., trde_qty_tp=..., stk_cnd=..., crd_cnd=..., stex_tp=...)
```

**요청**

| 필드 | 한글명 | 필수 | 길이 |
|---|---|:---:|---:|
| `high_low_tp` | 고저구분 | Y | 1 |
| `alacc_rt` | 근접율 | Y | 2 |
| `mrkt_tp` | 시장구분 | Y | 3 |
| `trde_qty_tp` | 거래량구분 | Y | 5 |
| `stk_cnd` | 종목조건 | Y | 1 |
| `crd_cnd` | 신용조건 | Y | 1 |
| `stex_tp` | 거래소구분 | Y | 1 |

**응답**

| 필드 | 한글명 | 길이 |
|---|---|---:|
| `high_low_pric_alacc` (list) | 고저가근접 |  |
| `high_low_pric_alacc[].stk_cd` | 종목코드 | 20 |
| `high_low_pric_alacc[].stk_nm` | 종목명 | 40 |
| `high_low_pric_alacc[].cur_prc` | 현재가 | 20 |
| `high_low_pric_alacc[].pred_pre_sig` | 전일대비기호 | 20 |
| `high_low_pric_alacc[].pred_pre` | 전일대비 | 20 |
| `high_low_pric_alacc[].flu_rt` | 등락률 | 20 |
| `high_low_pric_alacc[].trde_qty` | 거래량 | 20 |
| `high_low_pric_alacc[].sel_bid` | 매도호가 | 20 |
| `high_low_pric_alacc[].buy_bid` | 매수호가 | 20 |
| `high_low_pric_alacc[].tdy_high_pric` | 당일고가 | 20 |
| `high_low_pric_alacc[].tdy_low_pric` | 당일저가 | 20 |

<a id="ka10019"></a>

## `ka10019` · `rapid_price_change()` — 가격급등락요청

급등락요청 (Rapid Price Change) · `POST /api/dostk/stkinfo`

```python
api.stock_info.rapid_price_change(mrkt_tp=..., flu_tp=..., tm_tp=..., tm=..., trde_qty_tp=..., stk_cnd=..., crd_cnd=..., pric_cnd=..., updown_incls=..., stex_tp=...)
```

**요청**

| 필드 | 한글명 | 필수 | 길이 |
|---|---|:---:|---:|
| `mrkt_tp` | 시장구분 | Y | 3 |
| `flu_tp` | 등락구분 | Y | 1 |
| `tm_tp` | 시간구분 | Y | 1 |
| `tm` | 시간 | Y | 2 |
| `trde_qty_tp` | 거래량구분 | Y | 4 |
| `stk_cnd` | 종목조건 | Y | 1 |
| `crd_cnd` | 신용조건 | Y | 1 |
| `pric_cnd` | 가격조건 | Y | 1 |
| `updown_incls` | 상하한포함 | Y | 1 |
| `stex_tp` | 거래소구분 | Y | 1 |

**응답**

| 필드 | 한글명 | 길이 |
|---|---|---:|
| `pric_jmpflu` (list) | 가격급등락 |  |
| `pric_jmpflu[].stk_cd` | 종목코드 | 20 |
| `pric_jmpflu[].stk_cls` | 종목분류 | 20 |
| `pric_jmpflu[].stk_nm` | 종목명 | 40 |
| `pric_jmpflu[].pred_pre_sig` | 전일대비기호 | 20 |
| `pric_jmpflu[].pred_pre` | 전일대비 | 20 |
| `pric_jmpflu[].flu_rt` | 등락률 | 20 |
| `pric_jmpflu[].base_pric` | 기준가 | 20 |
| `pric_jmpflu[].cur_prc` | 현재가 | 20 |
| `pric_jmpflu[].base_pre` | 기준대비 | 20 |
| `pric_jmpflu[].trde_qty` | 거래량 | 20 |
| `pric_jmpflu[].jmp_rt` | 급등률 | 20 |

<a id="ka10024"></a>

## `ka10024` · `trading_volume_update()` — 거래량갱신요청

거래량갱신요청 (Trading Volume Update) · `POST /api/dostk/stkinfo`

```python
api.stock_info.trading_volume_update(mrkt_tp=..., cycle_tp=..., trde_qty_tp=..., stex_tp=...)
```

**요청**

| 필드 | 한글명 | 필수 | 길이 |
|---|---|:---:|---:|
| `mrkt_tp` | 시장구분 | Y | 3 |
| `cycle_tp` | 주기구분 | Y | 1 |
| `trde_qty_tp` | 거래량구분 | Y | 1 |
| `stex_tp` | 거래소구분 | Y | 1 |

**응답**

| 필드 | 한글명 | 길이 |
|---|---|---:|
| `trde_qty_updt` (list) | 거래량갱신 |  |
| `trde_qty_updt[].stk_cd` | 종목코드 | 20 |
| `trde_qty_updt[].stk_nm` | 종목명 | 40 |
| `trde_qty_updt[].cur_prc` | 현재가 | 20 |
| `trde_qty_updt[].pred_pre_sig` | 전일대비기호 | 20 |
| `trde_qty_updt[].pred_pre` | 전일대비 | 20 |
| `trde_qty_updt[].flu_rt` | 등락률 | 20 |
| `trde_qty_updt[].prev_trde_qty` | 이전거래량 | 20 |
| `trde_qty_updt[].now_trde_qty` | 현재거래량 | 20 |
| `trde_qty_updt[].sel_bid` | 매도호가 | 20 |
| `trde_qty_updt[].buy_bid` | 매수호가 | 20 |

<a id="ka10025"></a>

## `ka10025` · `volume_concentration()` — 매물대집중요청

매물대집중요청 (Volume Concentration) · `POST /api/dostk/stkinfo`

```python
api.stock_info.volume_concentration(mrkt_tp=..., prps_cnctr_rt=..., cur_prc_entry=..., prpscnt=..., cycle_tp=..., stex_tp=...)
```

**요청**

| 필드 | 한글명 | 필수 | 길이 |
|---|---|:---:|---:|
| `mrkt_tp` | 시장구분 | Y | 3 |
| `prps_cnctr_rt` | 매물집중비율 | Y | 3 |
| `cur_prc_entry` | 현재가진입 | Y | 1 |
| `prpscnt` | 매물대수 | Y | 2 |
| `cycle_tp` | 주기구분 | Y | 2 |
| `stex_tp` | 거래소구분 | Y | 1 |

**응답**

| 필드 | 한글명 | 길이 |
|---|---|---:|
| `prps_cnctr` (list) | 매물대집중 |  |
| `prps_cnctr[].stk_cd` | 종목코드 | 20 |
| `prps_cnctr[].stk_nm` | 종목명 | 40 |
| `prps_cnctr[].cur_prc` | 현재가 | 20 |
| `prps_cnctr[].pred_pre_sig` | 전일대비기호 | 20 |
| `prps_cnctr[].pred_pre` | 전일대비 | 20 |
| `prps_cnctr[].flu_rt` | 등락률 | 20 |
| `prps_cnctr[].now_trde_qty` | 현재거래량 | 20 |
| `prps_cnctr[].pric_strt` | 가격대시작 | 20 |
| `prps_cnctr[].pric_end` | 가격대끝 | 20 |
| `prps_cnctr[].prps_qty` | 매물량 | 20 |
| `prps_cnctr[].prps_rt` | 매물비 | 20 |

<a id="ka10026"></a>

## `ka10026` · `high_low_per()` — 고저PER요청

고저PER요청 (High/Low PER) · `POST /api/dostk/stkinfo`

```python
api.stock_info.high_low_per(pertp=..., stex_tp=...)
```

**요청**

| 필드 | 한글명 | 필수 | 길이 |
|---|---|:---:|---:|
| `pertp` | PER구분 | Y | 1 |
| `stex_tp` | 거래소구분 | Y | 1 |

**응답**

| 필드 | 한글명 | 길이 |
|---|---|---:|
| `high_low_per` (list) | 고저PER |  |
| `high_low_per[].stk_cd` | 종목코드 | 20 |
| `high_low_per[].stk_nm` | 종목명 | 40 |
| `high_low_per[].per` | PER | 20 |
| `high_low_per[].cur_prc` | 현재가 | 20 |
| `high_low_per[].pred_pre_sig` | 전일대비기호 | 20 |
| `high_low_per[].pred_pre` | 전일대비 | 20 |
| `high_low_per[].flu_rt` | 등락률 | 20 |
| `high_low_per[].now_trde_qty` | 현재거래량 | 20 |
| `high_low_per[].sel_bid` | 매도호가 | 20 |

<a id="ka10028"></a>

## `ka10028` · `change_rate_vs_opening()` — 시가대비등락률요청

시가대비등락률요청 (Change Rate vs Opening Price) · `POST /api/dostk/stkinfo`

```python
api.stock_info.change_rate_vs_opening(sort_tp=..., trde_qty_cnd=..., mrkt_tp=..., updown_incls=..., stk_cnd=..., crd_cnd=..., trde_prica_cnd=..., flu_cnd=..., stex_tp=...)
```

**요청**

| 필드 | 한글명 | 필수 | 길이 |
|---|---|:---:|---:|
| `sort_tp` | 정렬구분 | Y | 1 |
| `trde_qty_cnd` | 거래량조건 | Y | 4 |
| `mrkt_tp` | 시장구분 | Y | 3 |
| `updown_incls` | 상하한포함 | Y | 1 |
| `stk_cnd` | 종목조건 | Y | 2 |
| `crd_cnd` | 신용조건 | Y | 1 |
| `trde_prica_cnd` | 거래대금조건 | Y | 4 |
| `flu_cnd` | 등락조건 | Y | 1 |
| `stex_tp` | 거래소구분 | Y | 1 |

**응답**

| 필드 | 한글명 | 길이 |
|---|---|---:|
| `open_pric_pre_flu_rt` (list) | 시가대비등락률 |  |
| `open_pric_pre_flu_rt[].stk_cd` | 종목코드 | 20 |
| `open_pric_pre_flu_rt[].stk_nm` | 종목명 | 40 |
| `open_pric_pre_flu_rt[].cur_prc` | 현재가 | 20 |
| `open_pric_pre_flu_rt[].pred_pre_sig` | 전일대비기호 | 20 |
| `open_pric_pre_flu_rt[].pred_pre` | 전일대비 | 20 |
| `open_pric_pre_flu_rt[].flu_rt` | 등락률 | 20 |
| `open_pric_pre_flu_rt[].open_pric` | 시가 | 20 |
| `open_pric_pre_flu_rt[].high_pric` | 고가 | 20 |
| `open_pric_pre_flu_rt[].low_pric` | 저가 | 20 |
| `open_pric_pre_flu_rt[].open_pric_pre` | 시가대비 | 20 |
| `open_pric_pre_flu_rt[].now_trde_qty` | 현재거래량 | 20 |
| `open_pric_pre_flu_rt[].cntr_str` | 체결강도 | 20 |

<a id="ka10043"></a>

## `ka10043` · `trading_agent_supply_demand()` — 거래원매물대분석요청

거래원매물대분석요청 (Trading Agent Supply/Demand Trend Analysis) · `POST /api/dostk/stkinfo`

```python
api.stock_info.trading_agent_supply_demand(stk_cd=..., strt_dt=..., end_dt=..., qry_dt_tp=..., pot_tp=..., dt=..., sort_base=..., mmcm_cd=..., stex_tp=...)
```

**요청**

| 필드 | 한글명 | 필수 | 길이 |
|---|---|:---:|---:|
| `stk_cd` | 종목코드 | Y | 20 |
| `strt_dt` | 시작일자 | Y | 8 |
| `end_dt` | 종료일자 | Y | 8 |
| `qry_dt_tp` | 조회기간구분 | Y | 1 |
| `pot_tp` | 시점구분 | Y | 1 |
| `dt` | 기간 | Y | 4 |
| `sort_base` | 정렬기준 | Y | 1 |
| `mmcm_cd` | 회원사코드 | Y | 3 |
| `stex_tp` | 거래소구분 | Y | 1 |

**응답**

| 필드 | 한글명 | 길이 |
|---|---|---:|
| `trde_ori_prps_anly` (list) | 거래원매물대분석 |  |
| `trde_ori_prps_anly[].dt` | 일자 | 20 |
| `trde_ori_prps_anly[].close_pric` | 종가 | 20 |
| `trde_ori_prps_anly[].pre_sig` | 대비기호 | 20 |
| `trde_ori_prps_anly[].pred_pre` | 전일대비 | 20 |
| `trde_ori_prps_anly[].sel_qty` | 매도량 | 20 |
| `trde_ori_prps_anly[].buy_qty` | 매수량 | 20 |
| `trde_ori_prps_anly[].netprps_qty` | 순매수수량 | 20 |
| `trde_ori_prps_anly[].trde_qty_sum` | 거래량합 | 20 |
| `trde_ori_prps_anly[].trde_wght` | 거래비중 | 20 |

<a id="ka10052"></a>

## `ka10052` · `trading_agent_instant_volume()` — 거래원순간거래량요청

거래원순간거래량요청 (Trading Agent Instant Volume) · `POST /api/dostk/stkinfo`

```python
api.stock_info.trading_agent_instant_volume(mmcm_cd=..., mrkt_tp=..., qty_tp=..., pric_tp=..., stex_tp=...)
```

**요청**

| 필드 | 한글명 | 필수 | 길이 |
|---|---|:---:|---:|
| `mmcm_cd` | 회원사코드 | Y | 3 |
| `stk_cd` | 종목코드 |  | 20 |
| `mrkt_tp` | 시장구분 | Y | 1 |
| `qty_tp` | 수량구분 | Y | 3 |
| `pric_tp` | 가격구분 | Y | 1 |
| `stex_tp` | 거래소구분 | Y | 1 |

**응답**

| 필드 | 한글명 | 길이 |
|---|---|---:|
| `trde_ori_mont_trde_qty` (list) | 거래원순간거래량 |  |
| `trde_ori_mont_trde_qty[].tm` | 시간 | 20 |
| `trde_ori_mont_trde_qty[].stk_cd` | 종목코드 | 20 |
| `trde_ori_mont_trde_qty[].stk_nm` | 종목명 | 20 |
| `trde_ori_mont_trde_qty[].trde_ori_nm` | 거래원명 | 20 |
| `trde_ori_mont_trde_qty[].tp` | 구분 | 20 |
| `trde_ori_mont_trde_qty[].mont_trde_qty` | 순간거래량 | 20 |
| `trde_ori_mont_trde_qty[].acc_netprps` | 누적순매수 | 20 |
| `trde_ori_mont_trde_qty[].cur_prc` | 현재가 | 20 |
| `trde_ori_mont_trde_qty[].pred_pre_sig` | 전일대비기호 | 20 |
| `trde_ori_mont_trde_qty[].pred_pre` | 전일대비 | 20 |
| `trde_ori_mont_trde_qty[].flu_rt` | 등락율 | 20 |

<a id="ka10054"></a>

## `ka10054` · `vi_triggered_stocks()` — 변동성완화장치발동종목요청

변동성완화장치발동종목요청 (VI Triggered Stocks) · `POST /api/dostk/stkinfo`

```python
api.stock_info.vi_triggered_stocks(mrkt_tp=..., bf_mkrt_tp=..., motn_tp=..., skip_stk=..., trde_qty_tp=..., min_trde_qty=..., max_trde_qty=..., trde_prica_tp=..., min_trde_prica=..., max_trde_prica=..., motn_drc=..., stex_tp=...)
```

**요청**

| 필드 | 한글명 | 필수 | 길이 |
|---|---|:---:|---:|
| `mrkt_tp` | 시장구분 | Y | 3 |
| `bf_mkrt_tp` | 장전구분 | Y | 1 |
| `stk_cd` | 종목코드 |  | 20 |
| `motn_tp` | 발동구분 | Y | 1 |
| `skip_stk` | 제외종목 | Y | 9 |
| `trde_qty_tp` | 거래량구분 | Y | 1 |
| `min_trde_qty` | 최소거래량 | Y | 12 |
| `max_trde_qty` | 최대거래량 | Y | 12 |
| `trde_prica_tp` | 거래대금구분 | Y | 1 |
| `min_trde_prica` | 최소거래대금 | Y | 10 |
| `max_trde_prica` | 최대거래대금 | Y | 10 |
| `motn_drc` | 발동방향 | Y | 1 |
| `stex_tp` | 거래소구분 | Y | 1 |

**응답**

| 필드 | 한글명 | 길이 |
|---|---|---:|
| `motn_stk` (list) | 발동종목 |  |
| `motn_stk[].stk_cd` | 종목코드 | 20 |
| `motn_stk[].stk_nm` | 종목명 | 40 |
| `motn_stk[].acc_trde_qty` | 누적거래량 | 20 |
| `motn_stk[].motn_pric` | 발동가격 | 20 |
| `motn_stk[].dynm_dispty_rt` | 동적괴리율 | 20 |
| `motn_stk[].trde_cntr_proc_time` | 매매체결처리시각 | 20 |
| `motn_stk[].virelis_time` | VI해제시각 | 20 |
| `motn_stk[].viaplc_tp` | VI적용구분 | 20 |
| `motn_stk[].dynm_stdpc` | 동적기준가격 | 20 |
| `motn_stk[].static_stdpc` | 정적기준가격 | 20 |
| `motn_stk[].static_dispty_rt` | 정적괴리율 | 20 |
| `motn_stk[].open_pric_pre_flu_rt` | 시가대비등락률 | 20 |
| `motn_stk[].vimotn_cnt` | VI발동횟수 | 20 |
| `motn_stk[].stex_tp` | 거래소구분 | 20 |

<a id="ka10055"></a>

## `ka10055` · `today_vs_yesterday_volume()` — 당일전일체결량요청

당일전일체결량요청 (Today vs Yesterday Execution Volume) · `POST /api/dostk/stkinfo`

```python
api.stock_info.today_vs_yesterday_volume(stk_cd=..., tdy_pred=...)
```

**요청**

| 필드 | 한글명 | 필수 | 길이 |
|---|---|:---:|---:|
| `stk_cd` | 종목코드 | Y | 20 |
| `tdy_pred` | 당일전일 | Y | 1 |

**응답**

| 필드 | 한글명 | 길이 |
|---|---|---:|
| `tdy_pred_cntr_qty` (list) | 당일전일체결량 |  |
| `tdy_pred_cntr_qty[].cntr_tm` | 체결시간 | 20 |
| `tdy_pred_cntr_qty[].cntr_pric` | 체결가 | 20 |
| `tdy_pred_cntr_qty[].pred_pre_sig` | 전일대비기호 | 20 |
| `tdy_pred_cntr_qty[].pred_pre` | 전일대비 | 20 |
| `tdy_pred_cntr_qty[].flu_rt` | 등락율 | 20 |
| `tdy_pred_cntr_qty[].cntr_qty` | 체결량 | 20 |
| `tdy_pred_cntr_qty[].acc_trde_qty` | 누적거래량 | 20 |
| `tdy_pred_cntr_qty[].acc_trde_prica` | 누적거래대금 | 20 |

<a id="ka10058"></a>

## `ka10058` · `daily_trading_by_investor()` — 투자자별일별매매종목요청

투자자별일별매매종목요청 (Daily Trading by Investor) · `POST /api/dostk/stkinfo`

```python
api.stock_info.daily_trading_by_investor(strt_dt=..., end_dt=..., trde_tp=..., mrkt_tp=..., invsr_tp=..., stex_tp=...)
```

**요청**

| 필드 | 한글명 | 필수 | 길이 |
|---|---|:---:|---:|
| `strt_dt` | 시작일자 | Y | 8 |
| `end_dt` | 종료일자 | Y | 8 |
| `trde_tp` | 매매구분 | Y | 1 |
| `mrkt_tp` | 시장구분 | Y | 3 |
| `invsr_tp` | 투자자구분 | Y | 4 |
| `stex_tp` | 거래소구분 | Y | 1 |

**응답**

| 필드 | 한글명 | 길이 |
|---|---|---:|
| `invsr_daly_trde_stk` (list) | 투자자별일별매매종목 |  |
| `invsr_daly_trde_stk[].stk_cd` | 종목코드 | 20 |
| `invsr_daly_trde_stk[].stk_nm` | 종목명 | 40 |
| `invsr_daly_trde_stk[].netslmt_qty` | 순매도수량 | 20 |
| `invsr_daly_trde_stk[].netslmt_amt` | 순매도금액 | 20 |
| `invsr_daly_trde_stk[].prsm_avg_pric` | 추정평균가 | 20 |
| `invsr_daly_trde_stk[].cur_prc` | 현재가 | 20 |
| `invsr_daly_trde_stk[].pre_sig` | 대비기호 | 20 |
| `invsr_daly_trde_stk[].pred_pre` | 전일대비 | 20 |
| `invsr_daly_trde_stk[].avg_pric_pre` | 평균가대비 | 20 |
| `invsr_daly_trde_stk[].pre_rt` | 대비율 | 20 |
| `invsr_daly_trde_stk[].dt_trde_qty` | 기간거래량 | 20 |

<a id="ka10059"></a>

## `ka10059` · `investor_institution_by_stock()` — 종목별투자자기관별요청

투자자기관별종목별요청 (Investor/Institution by Stock) · `POST /api/dostk/stkinfo`

```python
api.stock_info.investor_institution_by_stock(dt=..., stk_cd=..., amt_qty_tp=..., trde_tp=..., unit_tp=...)
```

**요청**

| 필드 | 한글명 | 필수 | 길이 |
|---|---|:---:|---:|
| `dt` | 일자 | Y | 8 |
| `stk_cd` | 종목코드 | Y | 20 |
| `amt_qty_tp` | 금액수량구분 | Y | 1 |
| `trde_tp` | 매매구분 | Y | 1 |
| `unit_tp` | 단위구분 | Y | 4 |

**응답**

| 필드 | 한글명 | 길이 |
|---|---|---:|
| `stk_invsr_orgn` (list) | 종목별투자자기관별 |  |
| `stk_invsr_orgn[].dt` | 일자 | 20 |
| `stk_invsr_orgn[].cur_prc` | 현재가 | 20 |
| `stk_invsr_orgn[].pre_sig` | 대비기호 | 20 |
| `stk_invsr_orgn[].pred_pre` | 전일대비 | 20 |
| `stk_invsr_orgn[].flu_rt` | 등락율 | 20 |
| `stk_invsr_orgn[].acc_trde_qty` | 누적거래량 | 20 |
| `stk_invsr_orgn[].acc_trde_prica` | 누적거래대금 | 20 |
| `stk_invsr_orgn[].ind_invsr` | 개인투자자 | 20 |
| `stk_invsr_orgn[].frgnr_invsr` | 외국인투자자 | 20 |
| `stk_invsr_orgn[].orgn` | 기관계 | 20 |
| `stk_invsr_orgn[].fnnc_invt` | 금융투자 | 20 |
| `stk_invsr_orgn[].insrnc` | 보험 | 20 |
| `stk_invsr_orgn[].invtrt` | 투신 | 20 |
| `stk_invsr_orgn[].etc_fnnc` | 기타금융 | 20 |
| `stk_invsr_orgn[].bank` | 은행 | 20 |
| `stk_invsr_orgn[].penfnd_etc` | 연기금등 | 20 |
| `stk_invsr_orgn[].samo_fund` | 사모펀드 | 20 |
| `stk_invsr_orgn[].natn` | 국가 | 20 |
| `stk_invsr_orgn[].etc_corp` | 기타법인 | 20 |
| `stk_invsr_orgn[].natfor` | 내외국인 | 20 |

<a id="ka10061"></a>

## `ka10061` · `investor_institution_aggregate()` — 종목별투자자기관별합계요청

종목별투자자기관별합계요청 (Investor/Institution by Stock Aggregate) · `POST /api/dostk/stkinfo`

```python
api.stock_info.investor_institution_aggregate(stk_cd=..., strt_dt=..., end_dt=..., amt_qty_tp=..., trde_tp=..., unit_tp=...)
```

**요청**

| 필드 | 한글명 | 필수 | 길이 |
|---|---|:---:|---:|
| `stk_cd` | 종목코드 | Y | 20 |
| `strt_dt` | 시작일자 | Y | 8 |
| `end_dt` | 종료일자 | Y | 8 |
| `amt_qty_tp` | 금액수량구분 | Y | 1 |
| `trde_tp` | 매매구분 | Y | 1 |
| `unit_tp` | 단위구분 | Y | 4 |

**응답**

| 필드 | 한글명 | 길이 |
|---|---|---:|
| `stk_invsr_orgn_tot` (list) | 종목별투자자기관별합계 |  |
| `stk_invsr_orgn_tot[].ind_invsr` | 개인투자자 | 20 |
| `stk_invsr_orgn_tot[].frgnr_invsr` | 외국인투자자 | 20 |
| `stk_invsr_orgn_tot[].orgn` | 기관계 | 20 |
| `stk_invsr_orgn_tot[].fnnc_invt` | 금융투자 | 20 |
| `stk_invsr_orgn_tot[].insrnc` | 보험 | 20 |
| `stk_invsr_orgn_tot[].invtrt` | 투신 | 20 |
| `stk_invsr_orgn_tot[].etc_fnnc` | 기타금융 | 20 |
| `stk_invsr_orgn_tot[].bank` | 은행 | 20 |
| `stk_invsr_orgn_tot[].penfnd_etc` | 연기금등 | 20 |
| `stk_invsr_orgn_tot[].samo_fund` | 사모펀드 | 20 |
| `stk_invsr_orgn_tot[].natn` | 국가 | 20 |
| `stk_invsr_orgn_tot[].etc_corp` | 기타법인 | 20 |
| `stk_invsr_orgn_tot[].natfor` | 내외국인 | 20 |

<a id="ka10084"></a>

## `ka10084` · `today_vs_yesterday_execution()` — 당일전일체결요청

당일전일체결요청 (Today vs Yesterday Execution) · `POST /api/dostk/stkinfo`

```python
api.stock_info.today_vs_yesterday_execution(stk_cd=..., tdy_pred=..., tic_min=...)
```

**요청**

| 필드 | 한글명 | 필수 | 길이 |
|---|---|:---:|---:|
| `stk_cd` | 종목코드 | Y | 20 |
| `tdy_pred` | 당일전일 | Y | 1 |
| `tic_min` | 틱분 | Y | 1 |
| `tm` | 시간 |  | 4 |

**응답**

| 필드 | 한글명 | 길이 |
|---|---|---:|
| `tdy_pred_cntr` (list) | 당일전일체결 |  |
| `tdy_pred_cntr[].tm` | 시간 | 20 |
| `tdy_pred_cntr[].cur_prc` | 현재가 | 20 |
| `tdy_pred_cntr[].pred_pre` | 전일대비 | 20 |
| `tdy_pred_cntr[].pre_rt` | 대비율 | 20 |
| `tdy_pred_cntr[].pri_sel_bid_unit` | 우선매도호가단위 | 20 |
| `tdy_pred_cntr[].pri_buy_bid_unit` | 우선매수호가단위 | 20 |
| `tdy_pred_cntr[].cntr_trde_qty` | 체결거래량 | 20 |
| `tdy_pred_cntr[].sign` | 전일대비기호 | 20 |
| `tdy_pred_cntr[].acc_trde_qty` | 누적거래량 | 20 |
| `tdy_pred_cntr[].acc_trde_prica` | 누적거래대금 | 20 |
| `tdy_pred_cntr[].cntr_str` | 체결강도 | 20 |
| `tdy_pred_cntr[].stex_tp` | 거래소구분 | 20 |

<a id="ka10095"></a>

## `ka10095` · `watchlist_stock_info()` — 지정종목 정보요청

관심종목정보요청 (Watchlist Stock Info) · `POST /api/dostk/stkinfo`

```python
api.stock_info.watchlist_stock_info(stk_cd=...)
```

**요청**

| 필드 | 한글명 | 필수 | 길이 |
|---|---|:---:|---:|
| `stk_cd` | 종목코드 | Y | 20 |

**응답**

| 필드 | 한글명 | 길이 |
|---|---|---:|
| `atn_stk_infr` (list) | 관심종목정보 |  |
| `atn_stk_infr[].stk_cd` | 종목코드 | 20 |
| `atn_stk_infr[].stk_nm` | 종목명 | 40 |
| `atn_stk_infr[].cur_prc` | 현재가 | 20 |
| `atn_stk_infr[].base_pric` | 기준가 | 20 |
| `atn_stk_infr[].pred_pre` | 전일대비 | 20 |
| `atn_stk_infr[].pred_pre_sig` | 전일대비기호 | 20 |
| `atn_stk_infr[].flu_rt` | 등락율 | 20 |
| `atn_stk_infr[].trde_qty` | 거래량 | 20 |
| `atn_stk_infr[].trde_prica` | 거래대금 | 20 |
| `atn_stk_infr[].cntr_qty` | 체결량 | 20 |
| `atn_stk_infr[].cntr_str` | 체결강도 | 20 |
| `atn_stk_infr[].pred_trde_qty_pre` | 전일거래량대비 | 20 |
| `atn_stk_infr[].sel_bid` | 매도호가 | 20 |
| `atn_stk_infr[].buy_bid` | 매수호가 | 20 |
| `atn_stk_infr[].sel_1th_bid` | 매도1차호가 | 20 |
| `atn_stk_infr[].sel_2th_bid` | 매도2차호가 | 20 |
| `atn_stk_infr[].sel_3th_bid` | 매도3차호가 | 20 |
| `atn_stk_infr[].sel_4th_bid` | 매도4차호가 | 20 |
| `atn_stk_infr[].sel_5th_bid` | 매도5차호가 | 20 |
| `atn_stk_infr[].buy_1th_bid` | 매수1차호가 | 20 |
| `atn_stk_infr[].buy_2th_bid` | 매수2차호가 | 20 |
| `atn_stk_infr[].buy_3th_bid` | 매수3차호가 | 20 |
| `atn_stk_infr[].buy_4th_bid` | 매수4차호가 | 20 |
| `atn_stk_infr[].buy_5th_bid` | 매수5차호가 | 20 |
| `atn_stk_infr[].upl_pric` | 상한가 | 20 |
| `atn_stk_infr[].lst_pric` | 하한가 | 20 |
| `atn_stk_infr[].open_pric` | 시가 | 20 |
| `atn_stk_infr[].high_pric` | 고가 | 20 |
| `atn_stk_infr[].low_pric` | 저가 | 20 |
| `atn_stk_infr[].close_pric` | 종가 | 20 |
| `atn_stk_infr[].cntr_tm` | 체결시간 | 20 |
| `atn_stk_infr[].exp_cntr_pric` | 예상체결가 | 20 |
| `atn_stk_infr[].exp_cntr_qty` | 예상체결량 | 20 |
| `atn_stk_infr[].cap` | 자본금 | 20 |
| `atn_stk_infr[].fav` | 액면가 | 20 |
| `atn_stk_infr[].mac` | 시가총액 | 20 |
| `atn_stk_infr[].stkcnt` | 주식수 | 20 |
| `atn_stk_infr[].bid_tm` | 호가시간 | 20 |
| `atn_stk_infr[].dt` | 일자 | 20 |
| `atn_stk_infr[].pri_sel_req` | 우선매도잔량 | 20 |
| `atn_stk_infr[].pri_buy_req` | 우선매수잔량 | 20 |
| `atn_stk_infr[].pri_sel_cnt` | 우선매도건수 | 20 |
| `atn_stk_infr[].pri_buy_cnt` | 우선매수건수 | 20 |
| `atn_stk_infr[].tot_sel_req` | 총매도잔량 | 20 |
| `atn_stk_infr[].tot_buy_req` | 총매수잔량 | 20 |
| `atn_stk_infr[].tot_sel_cnt` | 총매도건수 | 20 |
| `atn_stk_infr[].tot_buy_cnt` | 총매수건수 | 20 |
| `atn_stk_infr[].prty` | 패리티 | 20 |
| `atn_stk_infr[].gear` | 기어링 | 20 |
| `atn_stk_infr[].pl_qutr` | 손익분기 | 20 |
| `atn_stk_infr[].cap_support` | 자본지지 | 20 |
| `atn_stk_infr[].elwexec_pric` | ELW행사가 | 20 |
| `atn_stk_infr[].cnvt_rt` | 전환비율 | 20 |
| `atn_stk_infr[].elwexpr_dt` | ELW만기일 | 20 |
| `atn_stk_infr[].cntr_engg` | 미결제약정 | 20 |
| `atn_stk_infr[].cntr_pred_pre` | 미결제전일대비 | 20 |
| `atn_stk_infr[].theory_pric` | 이론가 | 20 |
| `atn_stk_infr[].innr_vltl` | 내재변동성 | 20 |
| `atn_stk_infr[].delta` | 델타 | 20 |
| `atn_stk_infr[].gam` | 감마 | 20 |
| `atn_stk_infr[].theta` | 쎄타 | 20 |
| `atn_stk_infr[].vega` | 베가 | 20 |
| `atn_stk_infr[].law` | 로 | 20 |

<a id="ka10099"></a>

## `ka10099` · `stock_info_list()` — 종목정보 리스트

종목정보 리스트 (Stock Info List) · `POST /api/dostk/stkinfo`

```python
api.stock_info.stock_info_list(mrkt_tp=...)
```

**요청**

| 필드 | 한글명 | 필수 | 길이 |
|---|---|:---:|---:|
| `mrkt_tp` | 시장구분 | Y | 2 |

**응답**

| 필드 | 한글명 | 길이 |
|---|---|---:|
| `list` (list) | 종목리스트 |  |
| `list[].code` | 종목코드 | 20 |
| `list[].name` | 종목명 | 40 |
| `list[].listCount` | 상장주식수 | 20 |
| `list[].auditInfo` | 감리구분 | 20 |
| `list[].regDay` | 상장일 | 20 |
| `list[].lastPrice` | 전일종가 | 20 |
| `list[].state` | 종목상태 | 20 |
| `list[].marketCode` | 시장구분코드 | 20 |
| `list[].marketName` | 시장명 | 20 |
| `list[].upName` | 업종명 | 20 |
| `list[].upSizeName` | 회사크기분류 | 20 |
| `list[].orderWarning` | 투자유의종목여부 | 20 |
| `list[].companyClassName` | 회사분류 | 20 |
| `list[].nxtEnable` | NXT가능여부 | 20 |

<a id="ka10100"></a>

## `ka10100` · `stock_info_inquiry()` — 종목정보 조회

종목정보 조회 (Stock Info Inquiry) · `POST /api/dostk/stkinfo`

```python
api.stock_info.stock_info_inquiry(stk_cd=...)
```

**요청**

| 필드 | 한글명 | 필수 | 길이 |
|---|---|:---:|---:|
| `stk_cd` | 종목코드 | Y | 6 |

**응답**

| 필드 | 한글명 | 길이 |
|---|---|---:|
| `code` | 종목코드 |  |
| `name` | 종목명 | 40 |
| `listCount` | 상장주식수 | 16 |
| `auditInfo` | 감리구분 |  |
| `regDay` | 상장일 | 8 |
| `lastPrice` | 전일종가 | 8 |
| `state` | 종목상태 |  |
| `marketCode` | 시장구분코드 |  |
| `marketName` | 시장명 |  |
| `upName` | 업종명 |  |
| `upSizeName` | 회사크기분류 |  |
| `companyClassName` | 회사분류 |  |
| `orderWarning` | 투자유의종목여부 |  |
| `nxtEnable` | NXT가능여부 |  |

<a id="ka10101"></a>

## `ka10101` · `industry_code_list()` — 업종코드 리스트

업종코드 리스트 (Industry Code List) · `POST /api/dostk/stkinfo`

```python
api.stock_info.industry_code_list(mrkt_tp=...)
```

**요청**

| 필드 | 한글명 | 필수 | 길이 |
|---|---|:---:|---:|
| `mrkt_tp` | 시장구분 | Y | 1 |

**응답**

| 필드 | 한글명 | 길이 |
|---|---|---:|
| `list` (list) | 업종코드리스트 |  |
| `list[].marketCode` | 시장구분코드 |  |
| `list[].code` | 코드 |  |
| `list[].name` | 업종명 |  |
| `list[].group` | 그룹 |  |

<a id="ka10102"></a>

## `ka10102` · `member_company_list()` — 회원사 리스트

회원사 리스트 (Member Company List) · `POST /api/dostk/stkinfo`

```python
api.stock_info.member_company_list()
```

**요청**

요청 필드 없음.

**응답**

| 필드 | 한글명 | 길이 |
|---|---|---:|
| `list` (list) | 회원사코드리스트 |  |
| `list[].code` | 코드 |  |
| `list[].name` | 업종명 |  |
| `list[].gb` | 구분 |  |

<a id="ka90003"></a>

## `ka90003` · `program_buy_top50()` — 프로그램순매수상위50요청

프로그램순매수상위50요청 (Program Buy Top 50) · `POST /api/dostk/stkinfo`

```python
api.stock_info.program_buy_top50(trde_upper_tp=..., amt_qty_tp=..., mrkt_tp=..., stex_tp=...)
```

**요청**

| 필드 | 한글명 | 필수 | 길이 |
|---|---|:---:|---:|
| `trde_upper_tp` | 매매상위구분 | Y | 1 |
| `amt_qty_tp` | 금액수량구분 | Y | 2 |
| `mrkt_tp` | 시장구분 | Y | 10 |
| `stex_tp` | 거래소구분 | Y | 1 |

**응답**

| 필드 | 한글명 | 길이 |
|---|---|---:|
| `prm_netprps_upper_50` (list) | 프로그램순매수상위50 |  |
| `prm_netprps_upper_50[].rank` | 순위 | 20 |
| `prm_netprps_upper_50[].stk_cd` | 종목코드 | 20 |
| `prm_netprps_upper_50[].stk_nm` | 종목명 | 40 |
| `prm_netprps_upper_50[].cur_prc` | 현재가 | 20 |
| `prm_netprps_upper_50[].flu_sig` | 등락기호 | 20 |
| `prm_netprps_upper_50[].pred_pre` | 전일대비 | 20 |
| `prm_netprps_upper_50[].flu_rt` | 등락율 | 20 |
| `prm_netprps_upper_50[].acc_trde_qty` | 누적거래량 | 20 |
| `prm_netprps_upper_50[].prm_sell_amt` | 프로그램매도금액 | 20 |
| `prm_netprps_upper_50[].prm_buy_amt` | 프로그램매수금액 | 20 |
| `prm_netprps_upper_50[].prm_netprps_amt` | 프로그램순매수금액 | 20 |

<a id="ka90004"></a>

## `ka90004` · `program_trading_by_stock()` — 종목별프로그램매매현황요청

종목별프로그램매매현황요청 (Program Trading by Stock) · `POST /api/dostk/stkinfo`

```python
api.stock_info.program_trading_by_stock(dt=..., mrkt_tp=..., stex_tp=...)
```

**요청**

| 필드 | 한글명 | 필수 | 길이 |
|---|---|:---:|---:|
| `dt` | 일자 | Y | 8 |
| `mrkt_tp` | 시장구분 | Y | 10 |
| `stex_tp` | 거래소구분 | Y | 1 |

**응답**

| 필드 | 한글명 | 길이 |
|---|---|---:|
| `tot_1` | 매수체결수량합계 | 20 |
| `tot_2` | 매수체결금액합계 | 20 |
| `tot_3` | 매도체결수량합계 | 20 |
| `tot_4` | 매도체결금액합계 | 20 |
| `tot_5` | 순매수대금합계 | 20 |
| `tot_6` | 합계6 | 20 |
| `stk_prm_trde_prst` (list) | 종목별프로그램매매현황 |  |
| `stk_prm_trde_prst[].stk_cd` | 종목코드 | 20 |
| `stk_prm_trde_prst[].stk_nm` | 종목명 | 40 |
| `stk_prm_trde_prst[].cur_prc` | 현재가 | 20 |
| `stk_prm_trde_prst[].flu_sig` | 등락기호 | 20 |
| `stk_prm_trde_prst[].pred_pre` | 전일대비 | 20 |
| `stk_prm_trde_prst[].buy_cntr_qty` | 매수체결수량 | 20 |
| `stk_prm_trde_prst[].buy_cntr_amt` | 매수체결금액 | 20 |
| `stk_prm_trde_prst[].sel_cntr_qty` | 매도체결수량 | 20 |
| `stk_prm_trde_prst[].sel_cntr_amt` | 매도체결금액 | 20 |
| `stk_prm_trde_prst[].netprps_prica` | 순매수대금 | 20 |
| `stk_prm_trde_prst[].all_trde_rt` | 전체거래비율 | 20 |

<a id="kt20016"></a>

## `kt20016` · `margin_loan_available_stocks()` — 신용융자 가능종목요청

신용융자 가능종목요청 (Margin Loan Available Stocks) · `POST /api/dostk/stkinfo`

```python
api.stock_info.margin_loan_available_stocks(mrkt_deal_tp=...)
```

**요청**

| 필드 | 한글명 | 필수 | 길이 |
|---|---|:---:|---:|
| `crd_stk_grde_tp` | 신용종목등급구분 |  | 1 |
| `mrkt_deal_tp` | 시장거래구분 | Y | 1 |
| `stk_cd` | 종목코드 |  | 12 |

**응답**

| 필드 | 한글명 | 길이 |
|---|---|---:|
| `crd_loan_able` | 신용융자가능여부 | 40 |
| `crd_loan_pos_stk` (list) | 신용융자가능종목 |  |
| `crd_loan_pos_stk[].stk_cd` | 종목코드 | 12 |
| `crd_loan_pos_stk[].stk_nm` | 종목명 | 40 |
| `crd_loan_pos_stk[].crd_assr_rt` | 신용보증금율 | 4 |
| `crd_loan_pos_stk[].repl_pric` | 대용가 | 12 |
| `crd_loan_pos_stk[].pred_close_pric` | 전일종가 | 12 |
| `crd_loan_pos_stk[].crd_limit_over_yn` | 신용한도초과여부 | 1 |
| `crd_loan_pos_stk[].crd_limit_over_txt` | 신용한도초과 | 40 |

<a id="kt20017"></a>

## `kt20017` · `margin_loan_inquiry()` — 신용융자 가능문의

신용융자 가능문의 (Margin Loan Inquiry) · `POST /api/dostk/stkinfo`

```python
api.stock_info.margin_loan_inquiry(stk_cd=...)
```

**요청**

| 필드 | 한글명 | 필수 | 길이 |
|---|---|:---:|---:|
| `stk_cd` | 종목코드 | Y | 12 |

**응답**

| 필드 | 한글명 | 길이 |
|---|---|---:|
| `crd_alow_yn` | 신용가능여부 | 40 |
