<!-- 자동 생성 파일 — 손으로 고치지 마세요. `python scripts/gen_docs.py` 가 TR 카탈로그(kiwoom_client.spec)로 다시 만듭니다. -->

# `api.stock_info` — 종목정보 (Stock Information)

요청·응답 필드는 키움 공식 REST API 명세에서 만든 TR 카탈로그([출처·라이선스](https://github.com/younghwan91/kiwoom-client/blob/main/src/kiwoom_client/spec/SOURCE.md))를 그대로 옮긴 것입니다. 뜻이 애매하면 [키움 REST API 포털](https://openapi.kiwoom.com)이 기준입니다. 값은 모두 문자열로 넘깁니다.

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

| 필드 | 한글명 | 필수 | 길이 | 설명 |
|---|---|:---:|---:|---|
| `qry_tp` | 구분 | Y | 1 | 1:1분, 2:10분, 3:1시간, 4:당일 누적, 5:30초 |

**응답**

| 필드 | 한글명 | 길이 | 설명 |
|---|---|---:|---|
| `item_inq_rank` (list) | 실시간종목조회순위 |  |   |
| `item_inq_rank[].stk_nm` | 종목명 | 40 |   |
| `item_inq_rank[].bigd_rank` | 빅데이터 순위 | 20 | 0: 순위 변동 없음 |
| `item_inq_rank[].rank_chg` | 순위 등락 | 20 | 순위 변동 없음(rank_chg=0)인 경우 빈값('') 출력 |
| `item_inq_rank[].rank_chg_sign` | 순위 등락 부호 | 20 | 순위상승: +, 순위하락: -, 순위변동없음: ' |
| `item_inq_rank[].past_curr_prc` | 과거 현재가 | 20 | 기준 시점 주가, 부호가 포함된 원화 값 |
| `item_inq_rank[].base_comp_sign` | 기준가 대비 부호 | 20 | 1: 상한가, 2:상승, 3:보합, 4:하한가, 5:하락 |
| `item_inq_rank[].base_comp_chgr` | 기준가 대비 등락율 | 20 | 단위: %, 부호 포함 소수점 둘째 자리까지 포맷된 백분율 |
| `item_inq_rank[].prev_base_sign` | 직전 기준 대비 부호 | 20 |   |
| `item_inq_rank[].prev_base_chgr` | 직전 기준 대비 등락율 | 20 | 단위: %, 부호 포함 소수점 둘째 자리까지 포맷된 백분율 |
| `item_inq_rank[].dt` | 일자 | 20 | 기준 일자, YYYYMMDD |
| `item_inq_rank[].tm` | 시간 | 20 | 기준 시간, HHmmss |
| `item_inq_rank[].stk_cd` | 종목코드 | 20 |   |

<a id="ka10001"></a>

## `ka10001` · `basic_stock_info()` — 주식기본정보요청

종목기본정보요청 (Basic Stock Info) · `POST /api/dostk/stkinfo`

```python
api.stock_info.basic_stock_info(stk_cd=...)
```

**요청**

| 필드 | 한글명 | 필수 | 길이 | 설명 |
|---|---|:---:|---:|---|
| `stk_cd` | 종목코드 | Y | 20 | 거래소별 종목코드 (KRX:039490,NXT:039490_NX,SOR:039490_AL) |

**응답**

| 필드 | 한글명 | 길이 | 설명 |
|---|---|---:|---|
| `stk_cd` | 종목코드 | 20 |   |
| `stk_nm` | 종목명 | 40 |   |
| `setl_mm` | 결산월 | 20 |   |
| `fav` | 액면가 | 20 | 단위: 원 |
| `cap` | 자본금 | 20 | 단위: 억원 |
| `flo_stk` | 상장주식 | 20 | 단위: 천원 |
| `crd_rt` | 신용비율 | 20 | 단위: %, 부호 포함 소수점 둘째 자리까지 포맷된 백분율 |
| `oyr_hgst` | 연중최고 | 20 | 단위: 원, 부호가 포함된 숫자 |
| `oyr_lwst` | 연중최저 | 20 | 단위: 원, 부호가 포함된 숫자 |
| `mac` | 시가총액 | 20 | 단위: 억원 |
| `mac_wght` | 시가총액비중 | 20 |   |
| `for_exh_rt` | 외인소진률 | 20 | 단위: %, 부호 포함 소수점 둘째 자리까지 포맷된 백분율 |
| `repl_pric` | 대용가 | 20 | 단위: 원 |
| `per` | PER | 20 | [ 주의 ] PER, ROE 값들은 외부벤더사에서 제공되는 데이터이며 일주일에 한번 또는 실적발표 시즌에 업데이트 됨 |
| `eps` | EPS | 20 |   |
| `roe` | ROE | 20 | [ 주의 ] PER, ROE 값들은 외부벤더사에서 제공되는 데이터이며 일주일에 한번 또는 실적발표 시즌에 업데이트 됨 |
| `pbr` | PBR | 20 |   |
| `ev` | EV | 20 |   |
| `bps` | BPS | 20 |   |
| `sale_amt` | 매출액 | 20 | 단위: 억원 |
| `bus_pro` | 영업이익 | 20 | 단위: 억원 |
| `cup_nga` | 당기순이익 | 20 | 단위: 억원 |
| `250hgst` | 250최고 | 20 | 단위: 원, 부호가 포함된 숫자 |
| `250lwst` | 250최저 | 20 | 단위: 원, 부호가 포함된 숫자 |
| `high_pric` | 고가 | 20 | 단위: 원, 부호가 포함된 숫자 |
| `open_pric` | 시가 | 20 | 단위: 원, 부호가 포함된 숫자 |
| `low_pric` | 저가 | 20 | 단위: 원, 부호가 포함된 숫자 |
| `upl_pric` | 상한가 | 20 | 단위: 원, 부호가 포함된 숫자 |
| `lst_pric` | 하한가 | 20 | 단위: 원, 부호가 포함된 숫자 |
| `base_pric` | 기준가 | 20 | 단위: 원 |
| `exp_cntr_pric` | 예상체결가 | 20 |   |
| `exp_cntr_qty` | 예상체결수량 | 20 |   |
| `250hgst_pric_dt` | 250최고가일 | 20 | YYYYMMDD |
| `250hgst_pric_pre_rt` | 250최고가대비율 | 20 | 단위: %, 부호 포함 소수점 둘째 자리까지 포맷된 백분율 |
| `250lwst_pric_dt` | 250최저가일 | 20 | YYYYMMDD |
| `250lwst_pric_pre_rt` | 250최저가대비율 | 20 | 단위: %, 부호 포함 소수점 둘째 자리까지 포맷된 백분율 |
| `cur_prc` | 현재가 | 20 | 단위: 원, 부호가 포함된 숫자 |
| `pre_sig` | 대비기호 | 20 | 1: 상한가, 2:상승, 3:보합, 4:하한가, 5:하락 |
| `pred_pre` | 전일대비 | 20 | 단위: 원, 부호가 포함된 숫자 |
| `flu_rt` | 등락율 | 20 | 단위: %, 부호 포함 소수점 둘째 자리까지 포맷된 백분율 |
| `trde_qty` | 거래량 | 20 | 단위: 1주 |
| `trde_pre` | 거래대비 | 20 | 단위: %, 부호 포함 소수점 둘째 자리까지 포맷된 백분율 |
| `fav_unit` | 액면가단위 | 20 |   |
| `dstr_stk` | 유통주식 | 20 | 단위: 1주 |
| `dstr_rt` | 유통비율 | 20 | 단위: %, 부호 포함 소수점 첫째 자리까지 포맷된 백분율 |

<a id="ka10002"></a>

## `ka10002` · `stock_trading_agent()` — 주식거래원요청

종목거래원요청 (Stock Trading Agent) · `POST /api/dostk/stkinfo`

```python
api.stock_info.stock_trading_agent(stk_cd=...)
```

**요청**

| 필드 | 한글명 | 필수 | 길이 | 설명 |
|---|---|:---:|---:|---|
| `stk_cd` | 종목코드 | Y | 20 | 거래소별 종목코드 (KRX:039490,NXT:039490_NX,SOR:039490_AL) |

**응답**

| 필드 | 한글명 | 길이 | 설명 |
|---|---|---:|---|
| `stk_cd` | 종목코드 | 20 |   |
| `stk_nm` | 종목명 | 40 |   |
| `cur_prc` | 현재가 | 20 | 단위: 원, 부호가 포함된 숫자 |
| `flu_smbol` | 등락부호 | 20 | 1: 상한가, 2:상승, 3:보합, 4:하한가, 5:하락 |
| `base_pric` | 기준가 | 20 | 단위: 원 |
| `pred_pre` | 전일대비 | 20 | 단위: 원, 부호가 포함된 숫자 |
| `flu_rt` | 등락율 | 20 | 단위: %, 부호 포함 소수점 둘째 자리까지 포맷된 백분율 |
| `sel_trde_ori_nm_1` | 매도거래원명1 | 20 |   |
| `sel_trde_ori_1` | 매도거래원1 | 20 |   |
| `sel_trde_qty_1` | 매도거래량1 | 20 | 단위: 1주, 부호가 포함된 숫자 |
| `buy_trde_ori_nm_1` | 매수거래원명1 | 20 |   |
| `buy_trde_ori_1` | 매수거래원1 | 20 |   |
| `buy_trde_qty_1` | 매수거래량1 | 20 | 단위: 1주, 부호가 포함된 숫자 |
| `sel_trde_ori_nm_2` | 매도거래원명2 | 20 |   |
| `sel_trde_ori_2` | 매도거래원2 | 20 |   |
| `sel_trde_qty_2` | 매도거래량2 | 20 | 단위: 1주, 부호가 포함된 숫자 |
| `buy_trde_ori_nm_2` | 매수거래원명2 | 20 |   |
| `buy_trde_ori_2` | 매수거래원2 | 20 |   |
| `buy_trde_qty_2` | 매수거래량2 | 20 | 단위: 1주, 부호가 포함된 숫자 |
| `sel_trde_ori_nm_3` | 매도거래원명3 | 20 |   |
| `sel_trde_ori_3` | 매도거래원3 | 20 |   |
| `sel_trde_qty_3` | 매도거래량3 | 20 | 단위: 1주, 부호가 포함된 숫자 |
| `buy_trde_ori_nm_3` | 매수거래원명3 | 20 |   |
| `buy_trde_ori_3` | 매수거래원3 | 20 |   |
| `buy_trde_qty_3` | 매수거래량3 | 20 | 단위: 1주, 부호가 포함된 숫자 |
| `sel_trde_ori_nm_4` | 매도거래원명4 | 20 |   |
| `sel_trde_ori_4` | 매도거래원4 | 20 |   |
| `sel_trde_qty_4` | 매도거래량4 | 20 | 단위: 1주, 부호가 포함된 숫자 |
| `buy_trde_ori_nm_4` | 매수거래원명4 | 20 |   |
| `buy_trde_ori_4` | 매수거래원4 | 20 |   |
| `buy_trde_qty_4` | 매수거래량4 | 20 | 단위: 1주, 부호가 포함된 숫자 |
| `sel_trde_ori_nm_5` | 매도거래원명5 | 20 |   |
| `sel_trde_ori_5` | 매도거래원5 | 20 |   |
| `sel_trde_qty_5` | 매도거래량5 | 20 | 단위: 1주, 부호가 포함된 숫자 |
| `buy_trde_ori_nm_5` | 매수거래원명5 | 20 |   |
| `buy_trde_ori_5` | 매수거래원5 | 20 |   |
| `buy_trde_qty_5` | 매수거래량5 | 20 | 단위: 1주, 부호가 포함된 숫자 |

<a id="ka10003"></a>

## `ka10003` · `execution_info()` — 체결정보요청

체결정보요청 (Execution Info) · `POST /api/dostk/stkinfo`

```python
api.stock_info.execution_info(stk_cd=...)
```

**요청**

| 필드 | 한글명 | 필수 | 길이 | 설명 |
|---|---|:---:|---:|---|
| `stk_cd` | 종목코드 | Y | 20 | 거래소별 종목코드 (KRX:039490,NXT:039490_NX,SOR:039490_AL) |

**응답**

| 필드 | 한글명 | 길이 | 설명 |
|---|---|---:|---|
| `cntr_infr` (list) | 체결정보 |  |   |
| `cntr_infr[].tm` | 시간 | 20 | HHmmss |
| `cntr_infr[].cur_prc` | 현재가 | 20 | 단위: 원, 부호가 포함된 숫자 |
| `cntr_infr[].pred_pre` | 전일대비 | 20 | 단위: 원, 부호가 포함된 숫자 |
| `cntr_infr[].pre_rt` | 대비율 | 20 | 단위: %, 부호 포함 소수점 둘째 자리까지 포맷된 백분율 |
| `cntr_infr[].pri_sel_bid_unit` | 우선매도호가단위 | 20 | 단위: 원, 부호가 포함된 숫자 |
| `cntr_infr[].pri_buy_bid_unit` | 우선매수호가단위 | 20 | 단위: 원, 부호가 포함된 숫자 |
| `cntr_infr[].cntr_trde_qty` | 체결거래량 | 20 | 단위: 1주, 부호가 포함된 숫자 |
| `cntr_infr[].sign` | sign | 20 | 1: 상한가, 2:상승, 3:보합, 4:하한가, 5:하락 |
| `cntr_infr[].acc_trde_qty` | 누적거래량 | 20 | 단위: 1주 |
| `cntr_infr[].acc_trde_prica` | 누적거래대금 | 20 | 단위: 원 |
| `cntr_infr[].cntr_str` | 체결강도 | 20 | 단위: %, 부호 포함 소수점 둘째 자리까지 포맷된 백분율 |
| `cntr_infr[].stex_tp` | 거래소구분 | 20 | KRX , NXT , 통합 |

<a id="ka10013"></a>

## `ka10013` · `credit_trading_trend()` — 신용매매동향요청

신용매매동향요청 (Credit Trading Trend) · `POST /api/dostk/stkinfo`

```python
api.stock_info.credit_trading_trend(stk_cd=..., dt=..., qry_tp=...)
```

**요청**

| 필드 | 한글명 | 필수 | 길이 | 설명 |
|---|---|:---:|---:|---|
| `stk_cd` | 종목코드 | Y | 20 | 거래소별 종목코드 (KRX:039490,NXT:039490_NX,SOR:039490_AL) |
| `dt` | 일자 | Y | 8 | YYYYMMDD |
| `qry_tp` | 조회구분 | Y | 1 | 1:융자, 2:대주 |

**응답**

| 필드 | 한글명 | 길이 | 설명 |
|---|---|---:|---|
| `crd_trde_trend` (list) | 신용매매동향 |  |   |
| `crd_trde_trend[].dt` | 일자 | 20 | YYYYMMDD |
| `crd_trde_trend[].cur_prc` | 현재가 | 20 | 단위: 원, 부호가 포함된 숫자 |
| `crd_trde_trend[].pred_pre_sig` | 전일대비기호 | 20 | 1: 상한가, 2:상승, 3:보합, 4:하한가, 5:하락 |
| `crd_trde_trend[].pred_pre` | 전일대비 | 20 | 단위: 원, 부호가 포함된 숫자 |
| `crd_trde_trend[].trde_qty` | 거래량 | 20 | 단위: 1주 |
| `crd_trde_trend[].new` | 신규 | 20 | 융자단위: 백만원, 대주단위: 백만주 |
| `crd_trde_trend[].rpya` | 상환 | 20 | 융자단위: 백만원, 대주단위: 백만주 |
| `crd_trde_trend[].remn` | 잔고 | 20 | 융자단위: 백만원, 대주단위: 백만주 |
| `crd_trde_trend[].amt` | 금액 | 20 | 융자단위: 백만원, 대주단위: 백만주 |
| `crd_trde_trend[].pre` | 대비 | 20 | 융자단위: 백만원, 대주단위: 백만주, 부호가 포함된 숫자 |
| `crd_trde_trend[].shr_rt` | 공여율 | 20 | 단위: %, 부호 포함 소수점 둘째 자리까지 포맷된 백분율 |
| `crd_trde_trend[].remn_rt` | 잔고율 | 20 | 단위: %, 부호 포함 소수점 둘째 자리까지 포맷된 백분율 |

<a id="ka10015"></a>

## `ka10015` · `daily_transaction_detail()` — 일별거래상세요청

일별거래상세요청 (Daily Transaction Detail) · `POST /api/dostk/stkinfo`

```python
api.stock_info.daily_transaction_detail(stk_cd=..., strt_dt=...)
```

**요청**

| 필드 | 한글명 | 필수 | 길이 | 설명 |
|---|---|:---:|---:|---|
| `stk_cd` | 종목코드 | Y | 20 | 거래소별 종목코드 (KRX:039490,NXT:039490_NX,SOR:039490_AL) |
| `strt_dt` | 시작일자 | Y | 8 | YYYMMDD, 시작일자 기준으로 이전 일별 거래 정보를 조회 |

**응답**

| 필드 | 한글명 | 길이 | 설명 |
|---|---|---:|---|
| `daly_trde_dtl` (list) | 일별거래상세 |  |   |
| `daly_trde_dtl[].dt` | 일자 | 20 | YYYYMMDD |
| `daly_trde_dtl[].close_pric` | 종가 | 20 | 단위: 원, 부호가 포함된 숫자 |
| `daly_trde_dtl[].pred_pre_sig` | 전일대비기호 | 20 | 1: 상한가, 2:상승, 3:보합, 4:하한가, 5:하락 |
| `daly_trde_dtl[].pred_pre` | 전일대비 | 20 | 단위: 원, 부호가 포함된 숫자 |
| `daly_trde_dtl[].flu_rt` | 등락율 | 20 | 단위: %, 부호 포함 소수점 둘째 자리까지 포맷된 백분율 |
| `daly_trde_dtl[].trde_qty` | 거래량 | 20 | 단위: 1주 |
| `daly_trde_dtl[].trde_prica` | 거래대금 | 20 | 단위: 백만원 |
| `daly_trde_dtl[].bf_mkrt_trde_qty` | 장전거래량 | 20 | 단위: 1주 |
| `daly_trde_dtl[].bf_mkrt_trde_wght` | 장전거래비중 | 20 | 단위: %, 소수점 둘째 자리까지 포맷된 백분율 |
| `daly_trde_dtl[].opmr_trde_qty` | 장중거래량 | 20 | 단위: 1주 |
| `daly_trde_dtl[].opmr_trde_wght` | 장중거래비중 | 20 | 단위: %, 부호 포함 소수점 둘째 자리까지 포맷된 백분율 |
| `daly_trde_dtl[].af_mkrt_trde_qty` | 장후거래량 | 20 | 단위: 1주 |
| `daly_trde_dtl[].af_mkrt_trde_wght` | 장후거래비중 | 20 | 단위: %, 부호 포함 소수점 둘째 자리까지 포맷된 백분율 |
| `daly_trde_dtl[].tot_3` | 합계3 | 20 |   |
| `daly_trde_dtl[].prid_trde_qty` | 기간중거래량 | 20 |   |
| `daly_trde_dtl[].cntr_str` | 체결강도 | 20 |   |
| `daly_trde_dtl[].for_poss` | 외인보유 | 20 |   |
| `daly_trde_dtl[].for_wght` | 외인비중 | 20 |   |
| `daly_trde_dtl[].for_netprps` | 외인순매수 | 20 |   |
| `daly_trde_dtl[].orgn_netprps` | 기관순매수 | 20 |   |
| `daly_trde_dtl[].ind_netprps` | 개인순매수 | 20 |   |
| `daly_trde_dtl[].frgn` | 외국계 | 20 |   |
| `daly_trde_dtl[].crd_remn_rt` | 신용잔고율 | 20 |   |
| `daly_trde_dtl[].prm` | 프로그램 | 20 |   |
| `daly_trde_dtl[].bf_mkrt_trde_prica` | 장전거래대금 | 20 | 단위: 백만원 |
| `daly_trde_dtl[].bf_mkrt_trde_prica_wght` | 장전거래대금비중 | 20 | 단위: %, 부호 포함 소수점 둘째 자리까지 포맷된 백분율 |
| `daly_trde_dtl[].opmr_trde_prica` | 장중거래대금 | 20 | 단위: 백만원 |
| `daly_trde_dtl[].opmr_trde_prica_wght` | 장중거래대금비중 | 20 | 단위: %, 부호 포함 소수점 둘째 자리까지 포맷된 백분율 |
| `daly_trde_dtl[].af_mkrt_trde_prica` | 장후거래대금 | 20 | 단위: 백만원 |
| `daly_trde_dtl[].af_mkrt_trde_prica_wght` | 장후거래대금비중 | 20 | 단위: %, 부호 포함 소수점 둘째 자리까지 포맷된 백분율 |

<a id="ka10016"></a>

## `ka10016` · `new_high_low()` — 신고저가요청

신고저가요청 (New High/Low) · `POST /api/dostk/stkinfo`

```python
api.stock_info.new_high_low(mrkt_tp=..., ntl_tp=..., high_low_close_tp=..., stk_cnd=..., trde_qty_tp=..., crd_cnd=..., updown_incls=..., dt=..., stex_tp=...)
```

**요청**

| 필드 | 한글명 | 필수 | 길이 | 설명 |
|---|---|:---:|---:|---|
| `mrkt_tp` | 시장구분 | Y | 3 | 000:전체, 001:코스피, 101:코스닥 |
| `ntl_tp` | 신고저구분 | Y | 1 | 1:신고가,2:신저가 |
| `high_low_close_tp` | 고저종구분 | Y | 1 | 1:고저기준, 2:종가기준 |
| `stk_cnd` | 종목조건 | Y | 1 | 0:전체조회,1:관리종목제외, 3:우선주제외, 5:증100제외, 6:증100만보기, 7:증40만보기, 8:증30만보기 |
| `trde_qty_tp` | 거래량구분 | Y | 5 | 00000:전체조회, 00010:만주이상, 00050:5만주이상, 00100:10만주이상, 00150:15만주이상, 00200:20만주이상, 00300:30만주이상, 00500:50만주이상, 01000:백만주이상 |
| `crd_cnd` | 신용조건 | Y | 1 | 0:전체조회, 1:신용융자A군, 2:신용융자B군, 3:신용융자C군, 4:신용융자D군, 7:신용융자E군, 9:신용융자전체 |
| `updown_incls` | 상하한포함 | Y | 1 | 0:미포함, 1:포함 |
| `dt` | 기간 | Y | 3 | 5:5일, 10:10일, 20:20일, 60:60일, 250:250일, 250일까지 입력가능 |
| `stex_tp` | 거래소구분 | Y | 1 | 1:KRX, 2:NXT 3.통합 |

**응답**

| 필드 | 한글명 | 길이 | 설명 |
|---|---|---:|---|
| `ntl_pric` (list) | 신고저가 |  |   |
| `ntl_pric[].stk_cd` | 종목코드 | 20 |   |
| `ntl_pric[].stk_nm` | 종목명 | 40 |   |
| `ntl_pric[].cur_prc` | 현재가 | 20 | 단위: 원, 부호가 포함된 숫자 |
| `ntl_pric[].pred_pre_sig` | 전일대비기호 | 20 | 1: 상한가, 2:상승, 3:보합, 4:하한가, 5:하락 |
| `ntl_pric[].pred_pre` | 전일대비 | 20 | 단위: 원, 부호가 포함된 숫자 |
| `ntl_pric[].flu_rt` | 등락률 | 20 | 단위: %, 부호 포함 소수점 둘째 자리까지 포맷된 백분율 |
| `ntl_pric[].trde_qty` | 거래량 | 20 | 단위: 1주 |
| `ntl_pric[].pred_trde_qty_pre_rt` | 전일거래량대비율 | 20 | 단위: %, 부호 포함 소수점 둘째 자리까지 포맷된 백분율 |
| `ntl_pric[].sel_bid` | 매도호가 | 20 | 단위: 원, 부호가 포함된 숫자 |
| `ntl_pric[].buy_bid` | 매수호가 | 20 | 단위: 원, 부호가 포함된 숫자 |
| `ntl_pric[].high_pric` | 고가 | 20 | 단위: 원 |
| `ntl_pric[].low_pric` | 저가 | 20 | 단위: 원 |

<a id="ka10017"></a>

## `ka10017` · `upper_lower_limit()` — 상하한가요청

상하한가요청 (Upper/Lower Limit Price) · `POST /api/dostk/stkinfo`

```python
api.stock_info.upper_lower_limit(mrkt_tp=..., updown_tp=..., sort_tp=..., stk_cnd=..., trde_qty_tp=..., crd_cnd=..., trde_gold_tp=..., stex_tp=...)
```

**요청**

| 필드 | 한글명 | 필수 | 길이 | 설명 |
|---|---|:---:|---:|---|
| `mrkt_tp` | 시장구분 | Y | 3 | 000:전체, 001:코스피, 101:코스닥 |
| `updown_tp` | 상하한구분 | Y | 1 | 1:상한, 2:상승, 3:보합, 4: 하한, 5:하락, 6:전일상한, 7:전일하한 |
| `sort_tp` | 정렬구분 | Y | 1 | 1:종목코드순, 2:연속횟수순(상위100개), 3:등락률순 |
| `stk_cnd` | 종목조건 | Y | 1 | 0:전체조회,1:관리종목제외, 3:우선주제외, 4:우선주+관리종목제외, 5:증100제외, 6:증100만 보기, 7:증40만 보기, 8:증30만 보기, 9:증20만 보기, 10:우선주+관리종목+환기종목제외 |
| `trde_qty_tp` | 거래량구분 | Y | 5 | 00000:전체조회, 00010:만주이상, 00050:5만주이상, 00100:10만주이상, 00150:15만주이상, 00200:20만주이상, 00300:30만주이상, 00500:50만주이상, 01000:백만주이상 |
| `crd_cnd` | 신용조건 | Y | 1 | 0:전체조회, 1:신용융자A군, 2:신용융자B군, 3:신용융자C군, 4:신용융자D군, 7:신용융자E군, 9:신용융자전체 |
| `trde_gold_tp` | 매매금구분 | Y | 1 | 0:전체조회, 1:1천원미만, 2:1천원~2천원, 3:2천원~3천원, 4:5천원~1만원, 5:1만원이상, 8:1천원이상 |
| `stex_tp` | 거래소구분 | Y | 1 | 1:KRX, 2:NXT 3.통합 |

**응답**

| 필드 | 한글명 | 길이 | 설명 |
|---|---|---:|---|
| `updown_pric` (list) | 상하한가 |  |   |
| `updown_pric[].stk_cd` | 종목코드 | 20 |   |
| `updown_pric[].stk_infr` | 종목정보 | 20 |   |
| `updown_pric[].stk_nm` | 종목명 | 40 |   |
| `updown_pric[].cur_prc` | 현재가 | 20 | 단위: 원, 부호가 포함된 숫자 |
| `updown_pric[].pred_pre_sig` | 전일대비기호 | 20 | 1: 상한가, 2:상승, 3:보합, 4:하한가, 5:하락 |
| `updown_pric[].pred_pre` | 전일대비 | 20 | 단위: 원, 부호가 포함된 숫자 |
| `updown_pric[].flu_rt` | 등락률 | 20 | 단위: %, 부호 포함 소수점 둘째 자리까지 포맷된 백분율 |
| `updown_pric[].trde_qty` | 거래량 | 20 | 단위: 1주 |
| `updown_pric[].pred_trde_qty` | 전일거래량 | 20 | 단위: 1주 |
| `updown_pric[].sel_req` | 매도잔량 | 20 | 단위: 1주 |
| `updown_pric[].sel_bid` | 매도호가 | 20 | 단위: 원, 부호가 포함된 숫자 |
| `updown_pric[].buy_bid` | 매수호가 | 20 | 단위: 원, 부호가 포함된 숫자 |
| `updown_pric[].buy_req` | 매수잔량 | 20 | 단위: 1주 |
| `updown_pric[].cnt` | 횟수 | 20 |   |

<a id="ka10018"></a>

## `ka10018` · `near_high_low()` — 고저가근접요청

고저근접요청 (Near High/Low) · `POST /api/dostk/stkinfo`

```python
api.stock_info.near_high_low(high_low_tp=..., alacc_rt=..., mrkt_tp=..., trde_qty_tp=..., stk_cnd=..., crd_cnd=..., stex_tp=...)
```

**요청**

| 필드 | 한글명 | 필수 | 길이 | 설명 |
|---|---|:---:|---:|---|
| `high_low_tp` | 고저구분 | Y | 1 | 1:고가, 2:저가 |
| `alacc_rt` | 근접율 | Y | 2 | 05:0.5 10:1.0, 15:1.5, 20:2.0. 25:2.5, 30:3.0 |
| `mrkt_tp` | 시장구분 | Y | 3 | 000:전체, 001:코스피, 101:코스닥 |
| `trde_qty_tp` | 거래량구분 | Y | 5 | 00000:전체조회, 00010:만주이상, 00050:5만주이상, 00100:10만주이상, 00150:15만주이상, 00200:20만주이상, 00300:30만주이상, 00500:50만주이상, 01000:백만주이상 |
| `stk_cnd` | 종목조건 | Y | 1 | 0:전체조회,1:관리종목제외, 3:우선주제외, 5:증100제외, 6:증100만보기, 7:증40만보기, 8:증30만보기 |
| `crd_cnd` | 신용조건 | Y | 1 | 0:전체조회, 1:신용융자A군, 2:신용융자B군, 3:신용융자C군, 4:신용융자D군, 7:신용융자E군, 9:신용융자전체 |
| `stex_tp` | 거래소구분 | Y | 1 | 1:KRX, 2:NXT 3.통합 |

**응답**

| 필드 | 한글명 | 길이 | 설명 |
|---|---|---:|---|
| `high_low_pric_alacc` (list) | 고저가근접 |  |   |
| `high_low_pric_alacc[].stk_cd` | 종목코드 | 20 |   |
| `high_low_pric_alacc[].stk_nm` | 종목명 | 40 |   |
| `high_low_pric_alacc[].cur_prc` | 현재가 | 20 | 단위: 원, 부호가 포함된 숫자 |
| `high_low_pric_alacc[].pred_pre_sig` | 전일대비기호 | 20 | 1: 상한가, 2:상승, 3:보합, 4:하한가, 5:하락 |
| `high_low_pric_alacc[].pred_pre` | 전일대비 | 20 | 단위: 원, 부호가 포함된 숫자 |
| `high_low_pric_alacc[].flu_rt` | 등락률 | 20 | 단위: %, 부호 포함 소수점 둘째 자리까지 포맷된 백분율 |
| `high_low_pric_alacc[].trde_qty` | 거래량 | 20 | 단위: 1주 |
| `high_low_pric_alacc[].sel_bid` | 매도호가 | 20 | 단위: 원, 부호가 포함된 숫자 |
| `high_low_pric_alacc[].buy_bid` | 매수호가 | 20 | 단위: 원, 부호가 포함된 숫자 |
| `high_low_pric_alacc[].tdy_high_pric` | 당일고가 | 20 | 단위: 원, 부호가 포함된 숫자 |
| `high_low_pric_alacc[].tdy_low_pric` | 당일저가 | 20 | 단위: 원, 부호가 포함된 숫자 |

<a id="ka10019"></a>

## `ka10019` · `rapid_price_change()` — 가격급등락요청

급등락요청 (Rapid Price Change) · `POST /api/dostk/stkinfo`

```python
api.stock_info.rapid_price_change(mrkt_tp=..., flu_tp=..., tm_tp=..., tm=..., trde_qty_tp=..., stk_cnd=..., crd_cnd=..., pric_cnd=..., updown_incls=..., stex_tp=...)
```

**요청**

| 필드 | 한글명 | 필수 | 길이 | 설명 |
|---|---|:---:|---:|---|
| `mrkt_tp` | 시장구분 | Y | 3 | 000:전체, 001:코스피, 101:코스닥, 201:코스피200 |
| `flu_tp` | 등락구분 | Y | 1 | 1:급등, 2:급락 |
| `tm_tp` | 시간구분 | Y | 1 | 1:분전, 2:일전 |
| `tm` | 시간 | Y | 2 | 분 혹은 일입력 |
| `trde_qty_tp` | 거래량구분 | Y | 4 | 00000:전체조회, 00010:만주이상, 00050:5만주이상, 00100:10만주이상, 00150:15만주이상, 00200:20만주이상, 00300:30만주이상, 00500:50만주이상, 01000:백만주이상 |
| `stk_cnd` | 종목조건 | Y | 1 | 0:전체조회,1:관리종목제외, 3:우선주제외, 5:증100제외, 6:증100만보기, 7:증40만보기, 8:증30만보기 |
| `crd_cnd` | 신용조건 | Y | 1 | 0:전체조회, 1:신용융자A군, 2:신용융자B군, 3:신용융자C군, 4:신용융자D군, 7:신용융자E군, 9:신용융자전체 |
| `pric_cnd` | 가격조건 | Y | 1 | 0:전체조회, 1:1천원미만, 2:1천원~2천원, 3:2천원~3천원, 4:5천원~1만원, 5:1만원이상, 8:1천원이상 |
| `updown_incls` | 상하한포함 | Y | 1 | 0:미포함, 1:포함 |
| `stex_tp` | 거래소구분 | Y | 1 | 1:KRX, 2:NXT 3.통합 |

**응답**

| 필드 | 한글명 | 길이 | 설명 |
|---|---|---:|---|
| `pric_jmpflu` (list) | 가격급등락 |  |   |
| `pric_jmpflu[].stk_cd` | 종목코드 | 20 |   |
| `pric_jmpflu[].stk_cls` | 종목분류 | 20 |   |
| `pric_jmpflu[].stk_nm` | 종목명 | 40 |   |
| `pric_jmpflu[].pred_pre_sig` | 전일대비기호 | 20 | 1: 상한가, 2:상승, 3:보합, 4:하한가, 5:하락 |
| `pric_jmpflu[].pred_pre` | 전일대비 | 20 | 단위: 원, 부호가 포함된 숫자 |
| `pric_jmpflu[].flu_rt` | 등락률 | 20 | 단위: %, 부호 포함 소수점 둘째 자리까지 포맷된 백분율 |
| `pric_jmpflu[].base_pric` | 기준가 | 20 | 단위: 원 |
| `pric_jmpflu[].cur_prc` | 현재가 | 20 | 단위: 원, 부호가 포함된 숫자 |
| `pric_jmpflu[].base_pre` | 기준대비 | 20 | 단위: 원 |
| `pric_jmpflu[].trde_qty` | 거래량 | 20 | 단위: 1주 |
| `pric_jmpflu[].jmp_rt` | 급등률 | 20 | 단위: %, 부호 포함 소수점 둘째 자리까지 포맷된 백분율 |

<a id="ka10024"></a>

## `ka10024` · `trading_volume_update()` — 거래량갱신요청

거래량갱신요청 (Trading Volume Update) · `POST /api/dostk/stkinfo`

```python
api.stock_info.trading_volume_update(mrkt_tp=..., cycle_tp=..., trde_qty_tp=..., stex_tp=...)
```

**요청**

| 필드 | 한글명 | 필수 | 길이 | 설명 |
|---|---|:---:|---:|---|
| `mrkt_tp` | 시장구분 | Y | 3 | 000:전체, 001:코스피, 101:코스닥 |
| `cycle_tp` | 주기구분 | Y | 1 | 5:5일, 10:10일, 20:20일, 60:60일, 250:250일 |
| `trde_qty_tp` | 거래량구분 | Y | 1 | 5:5천주이상, 10:만주이상, 50:5만주이상, 100:10만주이상, 200:20만주이상, 300:30만주이상, 500:50만주이상, 1000:백만주이상 |
| `stex_tp` | 거래소구분 | Y | 1 | 1:KRX, 2:NXT 3.통합 |

**응답**

| 필드 | 한글명 | 길이 | 설명 |
|---|---|---:|---|
| `trde_qty_updt` (list) | 거래량갱신 |  |   |
| `trde_qty_updt[].stk_cd` | 종목코드 | 20 |   |
| `trde_qty_updt[].stk_nm` | 종목명 | 40 |   |
| `trde_qty_updt[].cur_prc` | 현재가 | 20 | 단위: 원, 부호가 포함된 숫자 |
| `trde_qty_updt[].pred_pre_sig` | 전일대비기호 | 20 | 1: 상한가, 2:상승, 3:보합, 4:하한가, 5:하락 |
| `trde_qty_updt[].pred_pre` | 전일대비 | 20 | 단위: 원, 부호가 포함된 숫자 |
| `trde_qty_updt[].flu_rt` | 등락률 | 20 | 단위: %, 부호 포함 소수점 둘째 자리까지 포맷된 백분율 |
| `trde_qty_updt[].prev_trde_qty` | 이전거래량 | 20 | 단위: 1주 |
| `trde_qty_updt[].now_trde_qty` | 현재거래량 | 20 | 단위: 1주 |
| `trde_qty_updt[].sel_bid` | 매도호가 | 20 | 단위: 원, 부호가 포함된 숫자 |
| `trde_qty_updt[].buy_bid` | 매수호가 | 20 | 단위: 원, 부호가 포함된 숫자 |

<a id="ka10025"></a>

## `ka10025` · `volume_concentration()` — 매물대집중요청

매물대집중요청 (Volume Concentration) · `POST /api/dostk/stkinfo`

```python
api.stock_info.volume_concentration(mrkt_tp=..., prps_cnctr_rt=..., cur_prc_entry=..., prpscnt=..., cycle_tp=..., stex_tp=...)
```

**요청**

| 필드 | 한글명 | 필수 | 길이 | 설명 |
|---|---|:---:|---:|---|
| `mrkt_tp` | 시장구분 | Y | 3 | 000:전체, 001:코스피, 101:코스닥 |
| `prps_cnctr_rt` | 매물집중비율 | Y | 3 | 0~100 입력 |
| `cur_prc_entry` | 현재가진입 | Y | 1 | 0:현재가 매물대 진입 포함안함, 1:현재가 매물대 진입포함 |
| `prpscnt` | 매물대수 | Y | 2 | 숫자입력 |
| `cycle_tp` | 주기구분 | Y | 2 | 50:50일, 100:100일, 150:150일, 200:200일, 250:250일, 300:300일 |
| `stex_tp` | 거래소구분 | Y | 1 | 1:KRX, 2:NXT 3.통합 |

**응답**

| 필드 | 한글명 | 길이 | 설명 |
|---|---|---:|---|
| `prps_cnctr` (list) | 매물대집중 |  |   |
| `prps_cnctr[].stk_cd` | 종목코드 | 20 |   |
| `prps_cnctr[].stk_nm` | 종목명 | 40 |   |
| `prps_cnctr[].cur_prc` | 현재가 | 20 | 단위: 원, 부호가 포함된 숫자 |
| `prps_cnctr[].pred_pre_sig` | 전일대비기호 | 20 | 1: 상한가, 2:상승, 3:보합, 4:하한가, 5:하락 |
| `prps_cnctr[].pred_pre` | 전일대비 | 20 | 단위: 원, 부호가 포함된 숫자 |
| `prps_cnctr[].flu_rt` | 등락률 | 20 | 단위: %, 부호 포함 소수점 둘째 자리까지 포맷된 백분율 |
| `prps_cnctr[].now_trde_qty` | 현재거래량 | 20 | 단위: 1주 |
| `prps_cnctr[].pric_strt` | 가격대시작 | 20 | 단위: 원 |
| `prps_cnctr[].pric_end` | 가격대끝 | 20 | 단위: 원 |
| `prps_cnctr[].prps_qty` | 매물량 | 20 | 단위: 1주 |
| `prps_cnctr[].prps_rt` | 매물비 | 20 | 단위: %, 부호 포함 소수점 둘째 자리까지 포맷된 백분율 |

<a id="ka10026"></a>

## `ka10026` · `high_low_per()` — 고저PER요청

고저PER요청 (High/Low PER) · `POST /api/dostk/stkinfo`

```python
api.stock_info.high_low_per(pertp=..., stex_tp=...)
```

**요청**

| 필드 | 한글명 | 필수 | 길이 | 설명 |
|---|---|:---:|---:|---|
| `pertp` | PER구분 | Y | 1 | 1:저PBR, 2:고PBR, 3:저PER, 4:고PER, 5:저ROE, 6:고ROE |
| `stex_tp` | 거래소구분 | Y | 1 | 1:KRX, 2:NXT 3.통합 |

**응답**

| 필드 | 한글명 | 길이 | 설명 |
|---|---|---:|---|
| `high_low_per` (list) | 고저PER |  |   |
| `high_low_per[].stk_cd` | 종목코드 | 20 |   |
| `high_low_per[].stk_nm` | 종목명 | 40 |   |
| `high_low_per[].per` | PER | 20 |   |
| `high_low_per[].cur_prc` | 현재가 | 20 | 단위: 원, 부호가 포함된 숫자 |
| `high_low_per[].pred_pre_sig` | 전일대비기호 | 20 | 1: 상한가, 2:상승, 3:보합, 4:하한가, 5:하락 |
| `high_low_per[].pred_pre` | 전일대비 | 20 | 단위: 원, 부호가 포함된 숫자 |
| `high_low_per[].flu_rt` | 등락률 | 20 | 단위: %, 부호 포함 소수점 둘째 자리까지 포맷된 백분율 |
| `high_low_per[].now_trde_qty` | 현재거래량 | 20 | 단위: 1주 |
| `high_low_per[].sel_bid` | 매도호가 | 20 | 단위: 원, 부호가 포함된 숫자 |

<a id="ka10028"></a>

## `ka10028` · `change_rate_vs_opening()` — 시가대비등락률요청

시가대비등락률요청 (Change Rate vs Opening Price) · `POST /api/dostk/stkinfo`

```python
api.stock_info.change_rate_vs_opening(sort_tp=..., trde_qty_cnd=..., mrkt_tp=..., updown_incls=..., stk_cnd=..., crd_cnd=..., trde_prica_cnd=..., flu_cnd=..., stex_tp=...)
```

**요청**

| 필드 | 한글명 | 필수 | 길이 | 설명 |
|---|---|:---:|---:|---|
| `sort_tp` | 정렬구분 | Y | 1 | 1:시가, 2:고가, 3:저가, 4:기준가 |
| `trde_qty_cnd` | 거래량조건 | Y | 4 | 0000:전체조회, 0010:만주이상, 0050:5만주이상, 0100:10만주이상, 0500:50만주이상, 1000:백만주이상 |
| `mrkt_tp` | 시장구분 | Y | 3 | 000:전체, 001:코스피, 101:코스닥 |
| `updown_incls` | 상하한포함 | Y | 1 | 0:불 포함, 1:포함 |
| `stk_cnd` | 종목조건 | Y | 2 | 0:전체조회, 1:관리종목제외, 4:우선주+관리주제외, 3:우선주제외, 5:증100제외, 6:증100만보기, 7:증40만보기, 8:증30만보기, 9:증20만보기 |
| `crd_cnd` | 신용조건 | Y | 1 | 0:전체조회, 1:신용융자A군, 2:신용융자B군, 3:신용융자C군, 4:신용융자D군, 7:신용융자E군, 9:신용융자전체 |
| `trde_prica_cnd` | 거래대금조건 | Y | 4 | 0:전체조회, 3:3천만원이상, 5:5천만원이상, 10:1억원이상, 30:3억원이상, 50:5억원이상, 100:10억원이상, 300:30억원이상, 500:50억원이상, 1000:100억원이상, 3000:300억원이상, 5000:500억원이상 |
| `flu_cnd` | 등락조건 | Y | 1 | 1:상위, 2:하위 |
| `stex_tp` | 거래소구분 | Y | 1 | 1:KRX, 2:NXT 3.통합 |

**응답**

| 필드 | 한글명 | 길이 | 설명 |
|---|---|---:|---|
| `open_pric_pre_flu_rt` (list) | 시가대비등락률 |  |   |
| `open_pric_pre_flu_rt[].stk_cd` | 종목코드 | 20 |   |
| `open_pric_pre_flu_rt[].stk_nm` | 종목명 | 40 |   |
| `open_pric_pre_flu_rt[].cur_prc` | 현재가 | 20 | 단위: 원, 부호가 포함된 숫자 |
| `open_pric_pre_flu_rt[].pred_pre_sig` | 전일대비기호 | 20 | 1: 상한가, 2:상승, 3:보합, 4:하한가, 5:하락 |
| `open_pric_pre_flu_rt[].pred_pre` | 전일대비 | 20 | 단위: 원, 부호가 포함된 숫자 |
| `open_pric_pre_flu_rt[].flu_rt` | 등락률 | 20 | 단위: %, 부호 포함 소수점 둘째 자리까지 포맷된 백분율 |
| `open_pric_pre_flu_rt[].open_pric` | 시가 | 20 | 단위: 원, 부호가 포함된 숫자 |
| `open_pric_pre_flu_rt[].high_pric` | 고가 | 20 | 단위: 원, 부호가 포함된 숫자 |
| `open_pric_pre_flu_rt[].low_pric` | 저가 | 20 | 단위: 원, 부호가 포함된 숫자 |
| `open_pric_pre_flu_rt[].open_pric_pre` | 시가대비 | 20 | 단위: %, 부호 포함 소수점 둘째 자리까지 포맷된 백분율 |
| `open_pric_pre_flu_rt[].now_trde_qty` | 현재거래량 | 20 | 단위: 1주 |
| `open_pric_pre_flu_rt[].cntr_str` | 체결강도 | 20 | 단위: %, 소수점 둘째 자리까지 포맷된 백분율 |

<a id="ka10043"></a>

## `ka10043` · `trading_agent_supply_demand()` — 거래원매물대분석요청

거래원매물대분석요청 (Trading Agent Supply/Demand Trend Analysis) · `POST /api/dostk/stkinfo`

```python
api.stock_info.trading_agent_supply_demand(stk_cd=..., strt_dt=..., end_dt=..., qry_dt_tp=..., pot_tp=..., dt=..., sort_base=..., mmcm_cd=..., stex_tp=...)
```

**요청**

| 필드 | 한글명 | 필수 | 길이 | 설명 |
|---|---|:---:|---:|---|
| `stk_cd` | 종목코드 | Y | 20 | 거래소별 종목코드 (KRX:039490,NXT:039490_NX,SOR:039490_AL) |
| `strt_dt` | 시작일자 | Y | 8 | YYYYMMDD |
| `end_dt` | 종료일자 | Y | 8 | YYYYMMDD |
| `qry_dt_tp` | 조회기간구분 | Y | 1 | 0:기간으로 조회, 1:시작일자, 종료일자로 조회 |
| `pot_tp` | 시점구분 | Y | 1 | 0:당일, 1:전일 |
| `dt` | 기간 | Y | 4 | 5:5일, 10:10일, 20:20일, 40:40일, 60:60일, 120:120일 |
| `sort_base` | 정렬기준 | Y | 1 | 1:종가순, 2:날짜순 |
| `mmcm_cd` | 회원사코드 | Y | 3 | 회원사 코드는 ka10102 조회 |
| `stex_tp` | 거래소구분 | Y | 1 | 1:KRX, 2:NXT 3.통합 |

**응답**

| 필드 | 한글명 | 길이 | 설명 |
|---|---|---:|---|
| `trde_ori_prps_anly` (list) | 거래원매물대분석 |  |   |
| `trde_ori_prps_anly[].dt` | 일자 | 20 | YYYYMMDD |
| `trde_ori_prps_anly[].close_pric` | 종가 | 20 | 단위: 원 |
| `trde_ori_prps_anly[].pre_sig` | 대비기호 | 20 | 1: 상한가, 2:상승, 3:보합, 4:하한가, 5:하락 |
| `trde_ori_prps_anly[].pred_pre` | 전일대비 | 20 | 단위: 원, 부호가 포함된 숫자 |
| `trde_ori_prps_anly[].sel_qty` | 매도량 | 20 | 단위: 1주 |
| `trde_ori_prps_anly[].buy_qty` | 매수량 | 20 | 단위: 1주 |
| `trde_ori_prps_anly[].netprps_qty` | 순매수수량 | 20 | 단위: 1주 |
| `trde_ori_prps_anly[].trde_qty_sum` | 거래량합 | 20 | 단위: 1주 |
| `trde_ori_prps_anly[].trde_wght` | 거래비중 | 20 | 단위: %, 부호 포함 소수점 둘째 자리까지 포맷된 백분율 |

<a id="ka10052"></a>

## `ka10052` · `trading_agent_instant_volume()` — 거래원순간거래량요청

거래원순간거래량요청 (Trading Agent Instant Volume) · `POST /api/dostk/stkinfo`

```python
api.stock_info.trading_agent_instant_volume(mmcm_cd=..., mrkt_tp=..., qty_tp=..., pric_tp=..., stex_tp=...)
```

**요청**

| 필드 | 한글명 | 필수 | 길이 | 설명 |
|---|---|:---:|---:|---|
| `mmcm_cd` | 회원사코드 | Y | 3 | 회원사 코드는 ka10102 조회 |
| `stk_cd` | 종목코드 |  | 20 | 거래소별 종목코드 (KRX:039490,NXT:039490_NX,SOR:039490_AL) |
| `mrkt_tp` | 시장구분 | Y | 1 | 0:전체, 1:코스피, 2:코스닥, 3:종목 |
| `qty_tp` | 수량구분 | Y | 3 | 0:전체, 1:1000주, 2:2000주, 3:, 5:, 10:10000주, 30: 30000주, 50: 50000주, 100: 100000주 |
| `pric_tp` | 가격구분 | Y | 1 | 0:전체, 1:1천원 미만, 8:1천원 이상, 2:1천원 ~ 2천원, 3:2천원 ~ 5천원, 4:5천원 ~ 1만원, 5:1만원 이상 |
| `stex_tp` | 거래소구분 | Y | 1 | 1:KRX, 2:NXT 3.통합 |

**응답**

| 필드 | 한글명 | 길이 | 설명 |
|---|---|---:|---|
| `trde_ori_mont_trde_qty` (list) | 거래원순간거래량 |  |   |
| `trde_ori_mont_trde_qty[].tm` | 시간 | 20 | HHmmss |
| `trde_ori_mont_trde_qty[].stk_cd` | 종목코드 | 20 |   |
| `trde_ori_mont_trde_qty[].stk_nm` | 종목명 | 20 |   |
| `trde_ori_mont_trde_qty[].trde_ori_nm` | 거래원명 | 20 |   |
| `trde_ori_mont_trde_qty[].tp` | 구분 | 20 |   |
| `trde_ori_mont_trde_qty[].mont_trde_qty` | 순간거래량 | 20 | 단위: 1주 |
| `trde_ori_mont_trde_qty[].acc_netprps` | 누적순매수 | 20 | 단위: 1주 |
| `trde_ori_mont_trde_qty[].cur_prc` | 현재가 | 20 | 단위: 원, 부호가 포함된 숫자 |
| `trde_ori_mont_trde_qty[].pred_pre_sig` | 전일대비기호 | 20 | 1: 상한가, 2:상승, 3:보합, 4:하한가, 5:하락 |
| `trde_ori_mont_trde_qty[].pred_pre` | 전일대비 | 20 | 단위: 원 |
| `trde_ori_mont_trde_qty[].flu_rt` | 등락율 | 20 | 단위: %, 부호 포함 소수점 둘째 자리까지 포맷된 백분율 |

<a id="ka10054"></a>

## `ka10054` · `vi_triggered_stocks()` — 변동성완화장치발동종목요청

변동성완화장치발동종목요청 (VI Triggered Stocks) · `POST /api/dostk/stkinfo`

```python
api.stock_info.vi_triggered_stocks(mrkt_tp=..., bf_mkrt_tp=..., motn_tp=..., skip_stk=..., trde_qty_tp=..., min_trde_qty=..., max_trde_qty=..., trde_prica_tp=..., min_trde_prica=..., max_trde_prica=..., motn_drc=..., stex_tp=...)
```

**요청**

| 필드 | 한글명 | 필수 | 길이 | 설명 |
|---|---|:---:|---:|---|
| `mrkt_tp` | 시장구분 | Y | 3 | 000:전체, 001: 코스피, 101:코스닥 |
| `bf_mkrt_tp` | 장전구분 | Y | 1 | 0:전체, 1:정규시장,2:시간외단일가 |
| `stk_cd` | 종목코드 |  | 20 | 거래소별 종목코드 (KRX:039490,NXT:039490_NX,SOR:039490_AL) 공백입력시 시장구분으로 설정한 전체종목조회 |
| `motn_tp` | 발동구분 | Y | 1 | 0:전체, 1:정적VI, 2:동적VI, 3:동적VI + 정적VI |
| `skip_stk` | 제외종목 | Y | 9 | 전종목포함 조회시 9개 0으로 설정(000000000),전종목제외 조회시 9개 1으로 설정(111111111),9개 종목조회여부를 조회포함(0), 조회제외(1)로 설정하며 종목순서는 우선주,관리종목,투자경고/위험,투자주의,환기종목,단기과열종목,증거금100%,ETF,ETN가 됨.우선주만 조회시"011111111"", 관리종목만 조회시 ""101111111"" 설정" |
| `trde_qty_tp` | 거래량구분 | Y | 1 | 0:사용안함, 1:사용 |
| `min_trde_qty` | 최소거래량 | Y | 12 | 0 주 이상, 거래량구분이 1일때만 입력(공백허용) |
| `max_trde_qty` | 최대거래량 | Y | 12 | 100000000 주 이하, 거래량구분이 1일때만 입력(공백허용) |
| `trde_prica_tp` | 거래대금구분 | Y | 1 | 0:사용안함, 1:사용 |
| `min_trde_prica` | 최소거래대금 | Y | 10 | 0 백만원 이상, 거래대금구분 1일때만 입력(공백허용) |
| `max_trde_prica` | 최대거래대금 | Y | 10 | 100000000 백만원 이하, 거래대금구분 1일때만 입력(공백허용) |
| `motn_drc` | 발동방향 | Y | 1 | 0:전체, 1:상승, 2:하락 |
| `stex_tp` | 거래소구분 | Y | 1 | 1:KRX, 2:NXT 3.통합 |

**응답**

| 필드 | 한글명 | 길이 | 설명 |
|---|---|---:|---|
| `motn_stk` (list) | 발동종목 |  |   |
| `motn_stk[].stk_cd` | 종목코드 | 20 |   |
| `motn_stk[].stk_nm` | 종목명 | 40 |   |
| `motn_stk[].acc_trde_qty` | 누적거래량 | 20 | 단위: 1주 |
| `motn_stk[].motn_pric` | 발동가격 | 20 | 단위: 원 |
| `motn_stk[].dynm_dispty_rt` | 동적괴리율 | 20 | 단위: %, 부호 포함 소수점 둘째 자리까지 포맷된 백분율 |
| `motn_stk[].trde_cntr_proc_time` | 매매체결처리시각 | 20 | HHmmss |
| `motn_stk[].virelis_time` | VI해제시각 | 20 | HHmmss |
| `motn_stk[].viaplc_tp` | VI적용구분 | 20 |   |
| `motn_stk[].dynm_stdpc` | 동적기준가격 | 20 | 단위: 원 |
| `motn_stk[].static_stdpc` | 정적기준가격 | 20 | 단위: 원 |
| `motn_stk[].static_dispty_rt` | 정적괴리율 | 20 | 단위: %, 부호 포함 소수점 둘째 자리까지 포맷된 백분율 |
| `motn_stk[].open_pric_pre_flu_rt` | 시가대비등락률 | 20 | 단위: %, 부호 포함 소수점 둘째 자리까지 포맷된 백분율 |
| `motn_stk[].vimotn_cnt` | VI발동횟수 | 20 |   |
| `motn_stk[].stex_tp` | 거래소구분 | 20 |   |

<a id="ka10055"></a>

## `ka10055` · `today_vs_yesterday_volume()` — 당일전일체결량요청

당일전일체결량요청 (Today vs Yesterday Execution Volume) · `POST /api/dostk/stkinfo`

```python
api.stock_info.today_vs_yesterday_volume(stk_cd=..., tdy_pred=...)
```

**요청**

| 필드 | 한글명 | 필수 | 길이 | 설명 |
|---|---|:---:|---:|---|
| `stk_cd` | 종목코드 | Y | 20 | 거래소별 종목코드 (KRX:039490,NXT:039490_NX,SOR:039490_AL) |
| `tdy_pred` | 당일전일 | Y | 1 | 1:당일, 2:전일 |

**응답**

| 필드 | 한글명 | 길이 | 설명 |
|---|---|---:|---|
| `tdy_pred_cntr_qty` (list) | 당일전일체결량 |  |   |
| `tdy_pred_cntr_qty[].cntr_tm` | 체결시간 | 20 | HHmmss |
| `tdy_pred_cntr_qty[].cntr_pric` | 체결가 | 20 | 단위: 원, 부호가 포함된 숫자 |
| `tdy_pred_cntr_qty[].pred_pre_sig` | 전일대비기호 | 20 | 1: 상한가, 2:상승, 3:보합, 4:하한가, 5:하락 |
| `tdy_pred_cntr_qty[].pred_pre` | 전일대비 | 20 | 단위: 원, 부호가 포함된 숫자 |
| `tdy_pred_cntr_qty[].flu_rt` | 등락율 | 20 | 단위: %, 부호 포함 소수점 둘째 자리까지 포맷된 백분율 |
| `tdy_pred_cntr_qty[].cntr_qty` | 체결량 | 20 | 단위: 1주 |
| `tdy_pred_cntr_qty[].acc_trde_qty` | 누적거래량 | 20 | 단위: 1주 |
| `tdy_pred_cntr_qty[].acc_trde_prica` | 누적거래대금 | 20 | 단위: 백만원 |

<a id="ka10058"></a>

## `ka10058` · `daily_trading_by_investor()` — 투자자별일별매매종목요청

투자자별일별매매종목요청 (Daily Trading by Investor) · `POST /api/dostk/stkinfo`

```python
api.stock_info.daily_trading_by_investor(strt_dt=..., end_dt=..., trde_tp=..., mrkt_tp=..., invsr_tp=..., stex_tp=...)
```

**요청**

| 필드 | 한글명 | 필수 | 길이 | 설명 |
|---|---|:---:|---:|---|
| `strt_dt` | 시작일자 | Y | 8 | YYYYMMDD |
| `end_dt` | 종료일자 | Y | 8 | YYYYMMDD |
| `trde_tp` | 매매구분 | Y | 1 | 순매도:1, 순매수:2 |
| `mrkt_tp` | 시장구분 | Y | 3 | 001:코스피, 101:코스닥 |
| `invsr_tp` | 투자자구분 | Y | 4 | 8000:개인, 9000:외국인, 1000:금융투자, 3000:투신, 3100:사모펀드, 5000:기타금융, 4000:은행, 2000:보험, 6000:연기금, 7000:국가, 7100:기타법인, 9999:기관계 |
| `stex_tp` | 거래소구분 | Y | 1 | 1:KRX, 2:NXT 3.통합 |

**응답**

| 필드 | 한글명 | 길이 | 설명 |
|---|---|---:|---|
| `invsr_daly_trde_stk` (list) | 투자자별일별매매종목 |  |   |
| `invsr_daly_trde_stk[].stk_cd` | 종목코드 | 20 |   |
| `invsr_daly_trde_stk[].stk_nm` | 종목명 | 40 |   |
| `invsr_daly_trde_stk[].netslmt_qty` | 순매도수량 | 20 | 단위: 1주, 부호가 포함된 숫자 |
| `invsr_daly_trde_stk[].netslmt_amt` | 순매도금액 | 20 | 단위: 원, 부호가 포함된 숫자 |
| `invsr_daly_trde_stk[].prsm_avg_pric` | 추정평균가 | 20 | 단위: 원 |
| `invsr_daly_trde_stk[].cur_prc` | 현재가 | 20 | 단위: 원, 부호가 포함된 숫자 |
| `invsr_daly_trde_stk[].pre_sig` | 대비기호 | 20 | 1: 상한가, 2:상승, 3:보합, 4:하한가, 5:하락 |
| `invsr_daly_trde_stk[].pred_pre` | 전일대비 | 20 | 단위: 원, 부호가 포함된 숫자 |
| `invsr_daly_trde_stk[].avg_pric_pre` | 평균가대비 | 20 | 단위: 원, 부호가 포함된 숫자 |
| `invsr_daly_trde_stk[].pre_rt` | 대비율 | 20 | 단위: %, 부호 포함 소수점 둘째 자리까지 포맷된 백분율 |
| `invsr_daly_trde_stk[].dt_trde_qty` | 기간거래량 | 20 | 단위: 1주 |

<a id="ka10059"></a>

## `ka10059` · `investor_institution_by_stock()` — 종목별투자자기관별요청

투자자기관별종목별요청 (Investor/Institution by Stock) · `POST /api/dostk/stkinfo`

```python
api.stock_info.investor_institution_by_stock(dt=..., stk_cd=..., amt_qty_tp=..., trde_tp=..., unit_tp=...)
```

**요청**

| 필드 | 한글명 | 필수 | 길이 | 설명 |
|---|---|:---:|---:|---|
| `dt` | 일자 | Y | 8 | YYYYMMDD |
| `stk_cd` | 종목코드 | Y | 20 | 거래소별 종목코드 (KRX:039490,NXT:039490_NX,SOR:039490_AL) |
| `amt_qty_tp` | 금액수량구분 | Y | 1 | 1:금액, 2:수량 |
| `trde_tp` | 매매구분 | Y | 1 | 0:순매수, 1:매수, 2:매도 |
| `unit_tp` | 단위구분 | Y | 4 | 1000:천주, 1:단주 |

**응답**

| 필드 | 한글명 | 길이 | 설명 |
|---|---|---:|---|
| `stk_invsr_orgn` (list) | 종목별투자자기관별 |  |   |
| `stk_invsr_orgn[].dt` | 일자 | 20 | YYYYMMDD |
| `stk_invsr_orgn[].cur_prc` | 현재가 | 20 | 단위: 원, 부호가 포함된 숫자 |
| `stk_invsr_orgn[].pre_sig` | 대비기호 | 20 | 1: 상한가, 2:상승, 3:보합, 4:하한가, 5:하락 |
| `stk_invsr_orgn[].pred_pre` | 전일대비 | 20 | 단위: 원, 부호가 포함된 숫자 |
| `stk_invsr_orgn[].flu_rt` | 등락율 | 20 | 우측 2자리 소수점자리수 |
| `stk_invsr_orgn[].acc_trde_qty` | 누적거래량 | 20 | 단위: 1주 |
| `stk_invsr_orgn[].acc_trde_prica` | 누적거래대금 | 20 | 단위: 백만원 |
| `stk_invsr_orgn[].ind_invsr` | 개인투자자 | 20 | 금액 단위: 백만원, 수량 단위: 1000주 혹은 1주(unit_tp값으로 설정) |
| `stk_invsr_orgn[].frgnr_invsr` | 외국인투자자 | 20 | 금액 단위: 백만원, 수량 단위: 1000주 혹은 1주(unit_tp값으로 설정) |
| `stk_invsr_orgn[].orgn` | 기관계 | 20 | 금액 단위: 백만원, 수량 단위: 1000주 혹은 1주(unit_tp값으로 설정) |
| `stk_invsr_orgn[].fnnc_invt` | 금융투자 | 20 | 금액 단위: 백만원, 수량 단위: 1000주 혹은 1주(unit_tp값으로 설정) |
| `stk_invsr_orgn[].insrnc` | 보험 | 20 | 금액 단위: 백만원, 수량 단위: 1000주 혹은 1주(unit_tp값으로 설정) |
| `stk_invsr_orgn[].invtrt` | 투신 | 20 | 금액 단위: 백만원, 수량 단위: 1000주 혹은 1주(unit_tp값으로 설정) |
| `stk_invsr_orgn[].etc_fnnc` | 기타금융 | 20 | 금액 단위: 백만원, 수량 단위: 1000주 혹은 1주(unit_tp값으로 설정) |
| `stk_invsr_orgn[].bank` | 은행 | 20 | 금액 단위: 백만원, 수량 단위: 1000주 혹은 1주(unit_tp값으로 설정) |
| `stk_invsr_orgn[].penfnd_etc` | 연기금등 | 20 | 금액 단위: 백만원, 수량 단위: 1000주 혹은 1주(unit_tp값으로 설정) |
| `stk_invsr_orgn[].samo_fund` | 사모펀드 | 20 | 금액 단위: 백만원, 수량 단위: 1000주 혹은 1주(unit_tp값으로 설정) |
| `stk_invsr_orgn[].natn` | 국가 | 20 |   |
| `stk_invsr_orgn[].etc_corp` | 기타법인 | 20 | 금액 단위: 백만원, 수량 단위: 1000주 혹은 1주(unit_tp값으로 설정) |
| `stk_invsr_orgn[].natfor` | 내외국인 | 20 | 금액 단위: 백만원, 수량 단위: 1000주 혹은 1주(unit_tp값으로 설정) |

<a id="ka10061"></a>

## `ka10061` · `investor_institution_aggregate()` — 종목별투자자기관별합계요청

종목별투자자기관별합계요청 (Investor/Institution by Stock Aggregate) · `POST /api/dostk/stkinfo`

```python
api.stock_info.investor_institution_aggregate(stk_cd=..., strt_dt=..., end_dt=..., amt_qty_tp=..., trde_tp=..., unit_tp=...)
```

**요청**

| 필드 | 한글명 | 필수 | 길이 | 설명 |
|---|---|:---:|---:|---|
| `stk_cd` | 종목코드 | Y | 20 | 거래소별 종목코드 (KRX:039490,NXT:039490_NX,SOR:039490_AL) |
| `strt_dt` | 시작일자 | Y | 8 | YYYYMMDD |
| `end_dt` | 종료일자 | Y | 8 | YYYYMMDD |
| `amt_qty_tp` | 금액수량구분 | Y | 1 | 1:금액, 2:수량 |
| `trde_tp` | 매매구분 | Y | 1 | 0:순매수 |
| `unit_tp` | 단위구분 | Y | 4 | 1000:천주, 1:단주 |

**응답**

| 필드 | 한글명 | 길이 | 설명 |
|---|---|---:|---|
| `stk_invsr_orgn_tot` (list) | 종목별투자자기관별합계 |  |   |
| `stk_invsr_orgn_tot[].ind_invsr` | 개인투자자 | 20 | 금액 단위: 백만원, 수량 단위: 1000주 혹은 1주(unit_tp값으로 설정) |
| `stk_invsr_orgn_tot[].frgnr_invsr` | 외국인투자자 | 20 | 금액 단위: 백만원, 수량 단위: 1000주 혹은 1주(unit_tp값으로 설정) |
| `stk_invsr_orgn_tot[].orgn` | 기관계 | 20 | 금액 단위: 백만원, 수량 단위: 1000주 혹은 1주(unit_tp값으로 설정) |
| `stk_invsr_orgn_tot[].fnnc_invt` | 금융투자 | 20 | 금액 단위: 백만원, 수량 단위: 1000주 혹은 1주(unit_tp값으로 설정) |
| `stk_invsr_orgn_tot[].insrnc` | 보험 | 20 | 금액 단위: 백만원, 수량 단위: 1000주 혹은 1주(unit_tp값으로 설정) |
| `stk_invsr_orgn_tot[].invtrt` | 투신 | 20 | 금액 단위: 백만원, 수량 단위: 1000주 혹은 1주(unit_tp값으로 설정) |
| `stk_invsr_orgn_tot[].etc_fnnc` | 기타금융 | 20 | 금액 단위: 백만원, 수량 단위: 1000주 혹은 1주(unit_tp값으로 설정) |
| `stk_invsr_orgn_tot[].bank` | 은행 | 20 | 금액 단위: 백만원, 수량 단위: 1000주 혹은 1주(unit_tp값으로 설정) |
| `stk_invsr_orgn_tot[].penfnd_etc` | 연기금등 | 20 | 금액 단위: 백만원, 수량 단위: 1000주 혹은 1주(unit_tp값으로 설정) |
| `stk_invsr_orgn_tot[].samo_fund` | 사모펀드 | 20 | 금액 단위: 백만원, 수량 단위: 1000주 혹은 1주(unit_tp값으로 설정) |
| `stk_invsr_orgn_tot[].natn` | 국가 | 20 |   |
| `stk_invsr_orgn_tot[].etc_corp` | 기타법인 | 20 | 금액 단위: 백만원, 수량 단위: 1000주 혹은 1주(unit_tp값으로 설정) |
| `stk_invsr_orgn_tot[].natfor` | 내외국인 | 20 | 금액 단위: 백만원, 수량 단위: 1000주 혹은 1주(unit_tp값으로 설정) |

<a id="ka10084"></a>

## `ka10084` · `today_vs_yesterday_execution()` — 당일전일체결요청

당일전일체결요청 (Today vs Yesterday Execution) · `POST /api/dostk/stkinfo`

```python
api.stock_info.today_vs_yesterday_execution(stk_cd=..., tdy_pred=..., tic_min=...)
```

**요청**

| 필드 | 한글명 | 필수 | 길이 | 설명 |
|---|---|:---:|---:|---|
| `stk_cd` | 종목코드 | Y | 20 | 거래소별 종목코드 (KRX:039490,NXT:039490_NX,SOR:039490_AL) |
| `tdy_pred` | 당일전일 | Y | 1 | 당일 : 1, 전일 : 2 |
| `tic_min` | 틱분 | Y | 1 | 0:틱, 1:분 |
| `tm` | 시간 |  | 4 | 조회시간 4자리, 오전 9시일 경우 0900, 오후 2시 30분일 경우 1430, 빈값('') 입력 시 현재시간으로 자동 설정 |

**응답**

| 필드 | 한글명 | 길이 | 설명 |
|---|---|---:|---|
| `tdy_pred_cntr` (list) | 당일전일체결 |  |   |
| `tdy_pred_cntr[].tm` | 시간 | 20 | HHmmss |
| `tdy_pred_cntr[].cur_prc` | 현재가 | 20 | 단위: 원, 부호가 포함된 숫자 |
| `tdy_pred_cntr[].pred_pre` | 전일대비 | 20 | 단위: 원, 부호가 포함된 숫자 |
| `tdy_pred_cntr[].pre_rt` | 대비율 | 20 | 단위: %, 부호 포함 소수점 둘째 자리까지 포맷된 백분율 |
| `tdy_pred_cntr[].pri_sel_bid_unit` | 우선매도호가단위 | 20 | 단위: 원, 부호가 포함된 숫자 |
| `tdy_pred_cntr[].pri_buy_bid_unit` | 우선매수호가단위 | 20 | 단위: 원, 부호가 포함된 숫자 |
| `tdy_pred_cntr[].cntr_trde_qty` | 체결거래량 | 20 | 단위: 1주, 부호가 포함된 숫자 |
| `tdy_pred_cntr[].sign` | 전일대비기호 | 20 | 1: 상한가, 2:상승, 3:보합, 4:하한가, 5:하락 |
| `tdy_pred_cntr[].acc_trde_qty` | 누적거래량 | 20 | 단위: 1주 |
| `tdy_pred_cntr[].acc_trde_prica` | 누적거래대금 | 20 | 단위: 백만원 |
| `tdy_pred_cntr[].cntr_str` | 체결강도 | 20 | 단위: %, 부호 포함 소수점 둘째 자리까지 포맷된 백분율 |
| `tdy_pred_cntr[].stex_tp` | 거래소구분 | 20 | KRX , NXT , 통합 |

<a id="ka10095"></a>

## `ka10095` · `watchlist_stock_info()` — 지정종목 정보요청

관심종목정보요청 (Watchlist Stock Info) · `POST /api/dostk/stkinfo`

```python
api.stock_info.watchlist_stock_info(stk_cd=...)
```

**요청**

| 필드 | 한글명 | 필수 | 길이 | 설명 |
|---|---|:---:|---:|---|
| `stk_cd` | 종목코드 | Y | 20 | 거래소별 종목코드 (KRX:039490,NXT:039490_NX,SOR:039490_AL) 여러개의 종목코드 입력시 \| 로 구분 |

**응답**

| 필드 | 한글명 | 길이 | 설명 |
|---|---|---:|---|
| `atn_stk_infr` (list) | 관심종목정보 |  |   |
| `atn_stk_infr[].stk_cd` | 종목코드 | 20 |   |
| `atn_stk_infr[].stk_nm` | 종목명 | 40 |   |
| `atn_stk_infr[].cur_prc` | 현재가 | 20 | 단위: 원, 부호가 포함된 숫자 |
| `atn_stk_infr[].base_pric` | 기준가 | 20 | 단위: 원 |
| `atn_stk_infr[].pred_pre` | 전일대비 | 20 | 단위: 원, 부호가 포함된 숫자 |
| `atn_stk_infr[].pred_pre_sig` | 전일대비기호 | 20 | 1: 상한가, 2:상승, 3:보합, 4:하한가, 5:하락 |
| `atn_stk_infr[].flu_rt` | 등락율 | 20 | 단위: %, 부호 포함 소수점 둘째 자리까지 포맷된 백분율 |
| `atn_stk_infr[].trde_qty` | 거래량 | 20 | 단위: 1주 |
| `atn_stk_infr[].trde_prica` | 거래대금 | 20 | 단위: 백만원 |
| `atn_stk_infr[].cntr_qty` | 체결량 | 20 | 단위: 1주, 부호가 포함된 숫자 |
| `atn_stk_infr[].cntr_str` | 체결강도 | 20 | 단위: %, 부호 포함 소수점 둘째 자리까지 포맷된 백분율 |
| `atn_stk_infr[].pred_trde_qty_pre` | 전일거래량대비 | 20 |   |
| `atn_stk_infr[].sel_bid` | 매도호가 | 20 | 단위: 원, 부호가 포함된 숫자 |
| `atn_stk_infr[].buy_bid` | 매수호가 | 20 | 단위: 원, 부호가 포함된 숫자 |
| `atn_stk_infr[].sel_1th_bid` | 매도1차호가 | 20 | 단위: 원, 부호가 포함된 숫자 |
| `atn_stk_infr[].sel_2th_bid` | 매도2차호가 | 20 | 단위: 원, 부호가 포함된 숫자 |
| `atn_stk_infr[].sel_3th_bid` | 매도3차호가 | 20 | 단위: 원, 부호가 포함된 숫자 |
| `atn_stk_infr[].sel_4th_bid` | 매도4차호가 | 20 | 단위: 원, 부호가 포함된 숫자 |
| `atn_stk_infr[].sel_5th_bid` | 매도5차호가 | 20 | 단위: 원, 부호가 포함된 숫자 |
| `atn_stk_infr[].buy_1th_bid` | 매수1차호가 | 20 | 단위: 원, 부호가 포함된 숫자 |
| `atn_stk_infr[].buy_2th_bid` | 매수2차호가 | 20 | 단위: 원, 부호가 포함된 숫자 |
| `atn_stk_infr[].buy_3th_bid` | 매수3차호가 | 20 | 단위: 원, 부호가 포함된 숫자 |
| `atn_stk_infr[].buy_4th_bid` | 매수4차호가 | 20 | 단위: 원, 부호가 포함된 숫자 |
| `atn_stk_infr[].buy_5th_bid` | 매수5차호가 | 20 | 단위: 원, 부호가 포함된 숫자 |
| `atn_stk_infr[].upl_pric` | 상한가 | 20 | 단위: 원, 부호가 포함된 숫자 |
| `atn_stk_infr[].lst_pric` | 하한가 | 20 | 단위: 원, 부호가 포함된 숫자 |
| `atn_stk_infr[].open_pric` | 시가 | 20 | 단위: 원, 부호가 포함된 숫자 |
| `atn_stk_infr[].high_pric` | 고가 | 20 | 단위: 원, 부호가 포함된 숫자 |
| `atn_stk_infr[].low_pric` | 저가 | 20 | 단위: 원, 부호가 포함된 숫자 |
| `atn_stk_infr[].close_pric` | 종가 | 20 | 단위: 원, 부호가 포함된 숫자 |
| `atn_stk_infr[].cntr_tm` | 체결시간 | 20 | HHmmss |
| `atn_stk_infr[].exp_cntr_pric` | 예상체결가 | 20 | 단위: 원, 부호가 포함된 숫자 |
| `atn_stk_infr[].exp_cntr_qty` | 예상체결량 | 20 | 단위: 1주 |
| `atn_stk_infr[].cap` | 자본금 | 20 | 단위: 억원 |
| `atn_stk_infr[].fav` | 액면가 | 20 | 단위: 원 |
| `atn_stk_infr[].mac` | 시가총액 | 20 | 단위: 억원 |
| `atn_stk_infr[].stkcnt` | 주식수 | 20 | 단위: 1주 |
| `atn_stk_infr[].bid_tm` | 호가시간 | 20 | HHmmss |
| `atn_stk_infr[].dt` | 일자 | 20 | YYYYMMDD |
| `atn_stk_infr[].pri_sel_req` | 우선매도잔량 | 20 | 단위: 1주 |
| `atn_stk_infr[].pri_buy_req` | 우선매수잔량 | 20 | 단위: 1주 |
| `atn_stk_infr[].pri_sel_cnt` | 우선매도건수 | 20 |   |
| `atn_stk_infr[].pri_buy_cnt` | 우선매수건수 | 20 |   |
| `atn_stk_infr[].tot_sel_req` | 총매도잔량 | 20 | 단위: 1주 |
| `atn_stk_infr[].tot_buy_req` | 총매수잔량 | 20 | 단위: 1주 |
| `atn_stk_infr[].tot_sel_cnt` | 총매도건수 | 20 |   |
| `atn_stk_infr[].tot_buy_cnt` | 총매수건수 | 20 |   |
| `atn_stk_infr[].prty` | 패리티 | 20 | 단위: %, 부호 포함 소수점 둘째 자리까지 포맷된 백분율 |
| `atn_stk_infr[].gear` | 기어링 | 20 | 단위: %, 부호 포함 소수점 둘째 자리까지 포맷된 백분율 |
| `atn_stk_infr[].pl_qutr` | 손익분기 | 20 | 단위: %, 부호 포함 소수점 둘째 자리까지 포맷된 백분율 |
| `atn_stk_infr[].cap_support` | 자본지지 | 20 | 단위: %, 부호 포함 소수점 둘째 자리까지 포맷된 백분율 |
| `atn_stk_infr[].elwexec_pric` | ELW행사가 | 20 | 단위: 원 |
| `atn_stk_infr[].cnvt_rt` | 전환비율 | 20 | 단위: %, 부호 포함 소수점 넷째 자리까지 포맷된 백분율 |
| `atn_stk_infr[].elwexpr_dt` | ELW만기일 | 20 | YYYYMMDD |
| `atn_stk_infr[].cntr_engg` | 미결제약정 | 20 |   |
| `atn_stk_infr[].cntr_pred_pre` | 미결제전일대비 | 20 |   |
| `atn_stk_infr[].theory_pric` | 이론가 | 20 |   |
| `atn_stk_infr[].innr_vltl` | 내재변동성 | 20 |   |
| `atn_stk_infr[].delta` | 델타 | 20 |   |
| `atn_stk_infr[].gam` | 감마 | 20 |   |
| `atn_stk_infr[].theta` | 쎄타 | 20 |   |
| `atn_stk_infr[].vega` | 베가 | 20 |   |
| `atn_stk_infr[].law` | 로 | 20 |   |

<a id="ka10099"></a>

## `ka10099` · `stock_info_list()` — 종목정보 리스트

종목정보 리스트 (Stock Info List) · `POST /api/dostk/stkinfo`

```python
api.stock_info.stock_info_list(mrkt_tp=...)
```

**요청**

| 필드 | 한글명 | 필수 | 길이 | 설명 |
|---|---|:---:|---:|---|
| `mrkt_tp` | 시장구분 | Y | 2 | 0 : 코스피, 10 : 코스닥, 30 : K-OTC, 50 : 코넥스, 60 : ETN, 70 : 손실제한 ETN, 80 : 금현물, 90 : 변동성 ETN, 2 : 인프라투융자, 3 : ELW, 4 : 뮤추얼펀드, 5 : 신주인수권, 6 : 리츠종목, 7 : 신주인수권증서, 8 : ETF, 9 : 하이일드펀드 |

**응답**

| 필드 | 한글명 | 길이 | 설명 |
|---|---|---:|---|
| `list` (list) | 종목리스트 |  |   |
| `list[].code` | 종목코드 | 20 | 단축코드 |
| `list[].name` | 종목명 | 40 |   |
| `list[].listCount` | 상장주식수 | 20 | 단위: 1주, 좌측 0-padding 처리된 부호 포함 16자리 숫자 |
| `list[].auditInfo` | 감리구분 | 20 |   |
| `list[].regDay` | 상장일 | 20 | YYYYMMDD |
| `list[].lastPrice` | 전일종가 | 20 | 단위: 원, 좌측 0-padding 처리된 부호 포함 8자리 숫자 |
| `list[].state` | 종목상태 | 20 |   |
| `list[].marketCode` | 시장구분코드 | 20 |   |
| `list[].marketName` | 시장명 | 20 |   |
| `list[].upName` | 업종명 | 20 |   |
| `list[].upSizeName` | 회사크기분류 | 20 |   |
| `list[].orderWarning` | 투자유의종목여부 | 20 | 0: 해당없음, 2: 정리매매, 3: 단기과열, 4: 투자위험, 5: 투자경과, 1: ETF투자주의요망(ETF인 경우만 전달 |
| `list[].companyClassName` | 회사분류 | 20 | 코스닥만 존재함 |
| `list[].nxtEnable` | NXT가능여부 | 20 | Y: 가능 |

<a id="ka10100"></a>

## `ka10100` · `stock_info_inquiry()` — 종목정보 조회

종목정보 조회 (Stock Info Inquiry) · `POST /api/dostk/stkinfo`

```python
api.stock_info.stock_info_inquiry(stk_cd=...)
```

**요청**

| 필드 | 한글명 | 필수 | 길이 | 설명 |
|---|---|:---:|---:|---|
| `stk_cd` | 종목코드 | Y | 6 | 종목코드 6자리 |

**응답**

| 필드 | 한글명 | 길이 | 설명 |
|---|---|---:|---|
| `code` | 종목코드 |  | 단축코드 |
| `name` | 종목명 | 40 |   |
| `listCount` | 상장주식수 | 16 | 단위: 1주, 좌측 0-padding 처리된 부호 포함 16자리 숫자 |
| `auditInfo` | 감리구분 |  |   |
| `regDay` | 상장일 | 8 | YYYYMMDD |
| `lastPrice` | 전일종가 | 8 | 단위: 원, 좌측 0-padding 처리된 부호 포함 8자리 숫자 |
| `state` | 종목상태 |  |   |
| `marketCode` | 시장구분코드 |  |   |
| `marketName` | 시장명 |  |   |
| `upName` | 업종명 |  |   |
| `upSizeName` | 회사크기분류 |  |   |
| `companyClassName` | 회사분류 |  | 코스닥만 존재함 |
| `orderWarning` | 투자유의종목여부 |  | 0: 해당없음, 2: 정리매매, 3: 단기과열, 4: 투자위험, 5: 투자경과, 1: ETF투자주의요망(ETF인 경우만 전달 |
| `nxtEnable` | NXT가능여부 |  | Y: 가능 |

<a id="ka10101"></a>

## `ka10101` · `industry_code_list()` — 업종코드 리스트

업종코드 리스트 (Industry Code List) · `POST /api/dostk/stkinfo`

```python
api.stock_info.industry_code_list(mrkt_tp=...)
```

**요청**

| 필드 | 한글명 | 필수 | 길이 | 설명 |
|---|---|:---:|---:|---|
| `mrkt_tp` | 시장구분 | Y | 1 | 0:코스피(거래소),1:코스닥,2:KOSPI200,4:KOSPI100,7:KRX100(통합지수) |

**응답**

| 필드 | 한글명 | 길이 | 설명 |
|---|---|---:|---|
| `list` (list) | 업종코드리스트 |  |   |
| `list[].marketCode` | 시장구분코드 |  |   |
| `list[].code` | 코드 |  |   |
| `list[].name` | 업종명 |  |   |
| `list[].group` | 그룹 |  |   |

<a id="ka10102"></a>

## `ka10102` · `member_company_list()` — 회원사 리스트

회원사 리스트 (Member Company List) · `POST /api/dostk/stkinfo`

```python
api.stock_info.member_company_list()
```

**요청**

요청 필드 없음.

**응답**

| 필드 | 한글명 | 길이 | 설명 |
|---|---|---:|---|
| `list` (list) | 회원사코드리스트 |  |   |
| `list[].code` | 코드 |  |   |
| `list[].name` | 업종명 |  |   |
| `list[].gb` | 구분 |  |   |

<a id="ka90003"></a>

## `ka90003` · `program_buy_top50()` — 프로그램순매수상위50요청

프로그램순매수상위50요청 (Program Buy Top 50) · `POST /api/dostk/stkinfo`

```python
api.stock_info.program_buy_top50(trde_upper_tp=..., amt_qty_tp=..., mrkt_tp=..., stex_tp=...)
```

**요청**

| 필드 | 한글명 | 필수 | 길이 | 설명 |
|---|---|:---:|---:|---|
| `trde_upper_tp` | 매매상위구분 | Y | 1 | 1:순매도상위, 2:순매수상위 |
| `amt_qty_tp` | 금액수량구분 | Y | 2 | 1:금액, 2:수량 |
| `mrkt_tp` | 시장구분 | Y | 10 | P00101:코스피, P10102:코스닥 |
| `stex_tp` | 거래소구분 | Y | 1 | 1:KRX, 2:NXT 3.통합 |

**응답**

| 필드 | 한글명 | 길이 | 설명 |
|---|---|---:|---|
| `prm_netprps_upper_50` (list) | 프로그램순매수상위50 |  |   |
| `prm_netprps_upper_50[].rank` | 순위 | 20 |   |
| `prm_netprps_upper_50[].stk_cd` | 종목코드 | 20 |   |
| `prm_netprps_upper_50[].stk_nm` | 종목명 | 40 |   |
| `prm_netprps_upper_50[].cur_prc` | 현재가 | 20 | 단위: 원, 부호가 포함된 숫자 |
| `prm_netprps_upper_50[].flu_sig` | 등락기호 | 20 | 1: 상한가, 2:상승, 3:보합, 4:하한가, 5:하락 |
| `prm_netprps_upper_50[].pred_pre` | 전일대비 | 20 | 단위: 원, 부호가 포함된 숫자 |
| `prm_netprps_upper_50[].flu_rt` | 등락율 | 20 | 단위: %, 부호 포함 소수점 둘째 자리까지 포맷된 백분율 |
| `prm_netprps_upper_50[].acc_trde_qty` | 누적거래량 | 20 | 단위: 1주 |
| `prm_netprps_upper_50[].prm_sell_amt` | 프로그램매도금액 | 20 | 단위: 백만원 |
| `prm_netprps_upper_50[].prm_buy_amt` | 프로그램매수금액 | 20 | 단위: 백만원 |
| `prm_netprps_upper_50[].prm_netprps_amt` | 프로그램순매수금액 | 20 | 단위: 백만원 |

<a id="ka90004"></a>

## `ka90004` · `program_trading_by_stock()` — 종목별프로그램매매현황요청

종목별프로그램매매현황요청 (Program Trading by Stock) · `POST /api/dostk/stkinfo`

```python
api.stock_info.program_trading_by_stock(dt=..., mrkt_tp=..., stex_tp=...)
```

**요청**

| 필드 | 한글명 | 필수 | 길이 | 설명 |
|---|---|:---:|---:|---|
| `dt` | 일자 | Y | 8 | YYYYMMDD |
| `mrkt_tp` | 시장구분 | Y | 10 | P00101:코스피, P10102:코스닥 |
| `stex_tp` | 거래소구분 | Y | 1 | 1:KRX, 2:NXT 3.통합 |

**응답**

| 필드 | 한글명 | 길이 | 설명 |
|---|---|---:|---|
| `tot_1` | 매수체결수량합계 | 20 | 단위: 1000주, 매수체결수량합계 |
| `tot_2` | 매수체결금액합계 | 20 | 단위: 백만원, 매수체결금액합계 |
| `tot_3` | 매도체결수량합계 | 20 | 단위: 1000주, 매도체결수량합계 |
| `tot_4` | 매도체결금액합계 | 20 | 단위: 백만원, 매도체결금액합계 |
| `tot_5` | 순매수대금합계 | 20 | 단위: 백만원, 순매수대금합계 |
| `tot_6` | 합계6 | 20 |   |
| `stk_prm_trde_prst` (list) | 종목별프로그램매매현황 |  |   |
| `stk_prm_trde_prst[].stk_cd` | 종목코드 | 20 |   |
| `stk_prm_trde_prst[].stk_nm` | 종목명 | 40 |   |
| `stk_prm_trde_prst[].cur_prc` | 현재가 | 20 | 단위: 원, 부호가 포함된 숫자 |
| `stk_prm_trde_prst[].flu_sig` | 등락기호 | 20 | 1: 상한가, 2:상승, 3:보합, 4:하한가, 5:하락 |
| `stk_prm_trde_prst[].pred_pre` | 전일대비 | 20 | 단위: 원, 부호가 포함된 숫자 |
| `stk_prm_trde_prst[].buy_cntr_qty` | 매수체결수량 | 20 | 단위: 1000주 |
| `stk_prm_trde_prst[].buy_cntr_amt` | 매수체결금액 | 20 | 단위: 백만원 |
| `stk_prm_trde_prst[].sel_cntr_qty` | 매도체결수량 | 20 | 단위: 1000주 |
| `stk_prm_trde_prst[].sel_cntr_amt` | 매도체결금액 | 20 | 단위: 백만원 |
| `stk_prm_trde_prst[].netprps_prica` | 순매수대금 | 20 | 단위: 백만원 |
| `stk_prm_trde_prst[].all_trde_rt` | 전체거래비율 | 20 | 단위: %, 부호 포함 소수점 둘째 자리까지 포맷된 백분율 |

<a id="kt20016"></a>

## `kt20016` · `margin_loan_available_stocks()` — 신용융자 가능종목요청

신용융자 가능종목요청 (Margin Loan Available Stocks) · `POST /api/dostk/stkinfo`

```python
api.stock_info.margin_loan_available_stocks(mrkt_deal_tp=...)
```

**요청**

| 필드 | 한글명 | 필수 | 길이 | 설명 |
|---|---|:---:|---:|---|
| `crd_stk_grde_tp` | 신용종목등급구분 |  | 1 | %:전체, A:A군, B:B군, C:C군, D:D군, E:E군 |
| `mrkt_deal_tp` | 시장거래구분 | Y | 1 | %:전체, 1:코스피, 0:코스닥 |
| `stk_cd` | 종목코드 |  | 12 | 종목 코드 입력 |

**응답**

| 필드 | 한글명 | 길이 | 설명 |
|---|---|---:|---|
| `crd_loan_able` | 신용융자가능여부 | 40 |   |
| `crd_loan_pos_stk` (list) | 신용융자가능종목 |  |   |
| `crd_loan_pos_stk[].stk_cd` | 종목코드 | 12 |   |
| `crd_loan_pos_stk[].stk_nm` | 종목명 | 40 |   |
| `crd_loan_pos_stk[].crd_assr_rt` | 신용보증금율 | 4 | %가 포함된 백분율 |
| `crd_loan_pos_stk[].repl_pric` | 대용가 | 12 | 단위: 원, 좌측 0-padding 처리된 부호 포함 12자리 숫자 |
| `crd_loan_pos_stk[].pred_close_pric` | 전일종가 | 12 | 단위: 원, 좌측 0-padding 처리된 부호 포함 12자리 숫자 |
| `crd_loan_pos_stk[].crd_limit_over_yn` | 신용한도초과여부 | 1 | Y, N |
| `crd_loan_pos_stk[].crd_limit_over_txt` | 신용한도초과 | 40 | N:공란,Y:회사한도 초과 |

<a id="kt20017"></a>

## `kt20017` · `margin_loan_inquiry()` — 신용융자 가능문의

신용융자 가능문의 (Margin Loan Inquiry) · `POST /api/dostk/stkinfo`

```python
api.stock_info.margin_loan_inquiry(stk_cd=...)
```

**요청**

| 필드 | 한글명 | 필수 | 길이 | 설명 |
|---|---|:---:|---:|---|
| `stk_cd` | 종목코드 | Y | 12 | 종목 코드 입력 |

**응답**

| 필드 | 한글명 | 길이 | 설명 |
|---|---|---:|---|
| `crd_alow_yn` | 신용가능여부 | 40 |   |
