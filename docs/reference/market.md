<!-- 자동 생성 파일 — 손으로 고치지 마세요. `python scripts/gen_docs.py` 가 TR 카탈로그(kiwoom_client.spec)로 다시 만듭니다. -->

# `api.market` — 시세 (Market Condition)

요청·응답 필드는 키움 공식 REST API 명세에서 만든 TR 카탈로그([출처·라이선스](https://github.com/younghwan91/kiwoom-client/blob/main/src/kiwoom_client/spec/SOURCE.md))에서 옮긴 필드 ID·한글명·필수·길이입니다. 필드 설명·코드값은 싣지 않으니 [키움 REST API 포털](https://openapi.kiwoom.com) 문서를 보세요(자주 쓰는 코드값은 `kiwoom_client.codes`). 값은 모두 문자열로 넘깁니다.

공통 헤더(`api-id`·`cont-yn`·`next-key`·`authorization`)는 라이브러리가 채웁니다 — 연속조회는 메서드의 `cont_yn`·`next_key` 인자나 `request_all()` 을 쓰세요.

| api_id | 메서드 | 이름 |
|---|---|---|
| [`ka10004`](#ka10004) | `stock_quote()` | 주식호가요청 |
| [`ka10005`](#ka10005) | `stock_daily_weekly_monthly()` | 주식일주월시분요청 |
| [`ka10006`](#ka10006) | `stock_minute_price()` | 주식시분요청 |
| [`ka10007`](#ka10007) | `order_book_info()` | 시세표성정보요청 |
| [`ka10011`](#ka10011) | `rights_issue_price()` | 신주인수권전체시세요청 |
| [`ka10044`](#ka10044) | `daily_institutional_trading()` | 일별기관매매종목요청 |
| [`ka10045`](#ka10045) | `institutional_trading_trend()` | 종목별기관매매추이요청 |
| [`ka10046`](#ka10046) | `hourly_execution_strength()` | 체결강도추이시간별요청 |
| [`ka10047`](#ka10047) | `daily_execution_strength()` | 체결강도추이일별요청 |
| [`ka10063`](#ka10063) | `intraday_investor_trading()` | 장중투자자별매매요청 |
| [`ka10066`](#ka10066) | `after_hours_investor_trading()` | 장마감후투자자별매매요청 |
| [`ka10078`](#ka10078) | `broker_stock_trading_trend()` | 증권사별종목매매동향요청 |
| [`ka10086`](#ka10086) | `daily_stock_price()` | 일별주가요청 |
| [`ka10087`](#ka10087) | `after_hours_single_price()` | 시간외단일가요청 |
| [`ka50010`](#ka50010) | `gold_spot_execution_trend()` | 금현물체결추이 |
| [`ka50012`](#ka50012) | `gold_spot_daily_trend()` | 금현물일별추이 |
| [`ka50087`](#ka50087) | `gold_spot_expected_execution()` | 금현물예상체결 |
| [`ka50100`](#ka50100) | `gold_spot_price_info()` | 금현물 시세정보 |
| [`ka50101`](#ka50101) | `gold_spot_order_book()` | 금현물 호가 |
| [`ka90005`](#ka90005) | `program_trading_by_time()` | 프로그램매매추이요청 시간대별 |
| [`ka90006`](#ka90006) | `program_arbitrage_balance()` | 프로그램매매차익잔고추이요청 |
| [`ka90007`](#ka90007) | `cumulative_program_trading()` | 프로그램매매누적추이요청 |
| [`ka90008`](#ka90008) | `program_trading_by_stock_time()` | 종목시간별프로그램매매추이요청 |
| [`ka90010`](#ka90010) | `program_trading_by_date()` | 프로그램매매추이요청 일자별 |
| [`ka90013`](#ka90013) | `program_trading_by_stock_day()` | 종목일별프로그램매매추이요청 |

<a id="ka10004"></a>

## `ka10004` · `stock_quote()` — 주식호가요청

주식호가요청 (Stock Quote) · `POST /api/dostk/mrkcond`

```python
api.market.stock_quote(stk_cd=...)
```

**요청**

| 필드 | 한글명 | 필수 | 길이 |
|---|---|:---:|---:|
| `stk_cd` | 종목코드 | Y | 20 |

**응답**

| 필드 | 한글명 | 길이 |
|---|---|---:|
| `bid_req_base_tm` | 호가잔량기준시간 | 20 |
| `sel_10th_pre_req_pre` | 매도10차선잔량대비 | 20 |
| `sel_10th_pre_req` | 매도10차선잔량 | 20 |
| `sel_10th_pre_bid` | 매도10차선호가 | 20 |
| `sel_9th_pre_req_pre` | 매도9차선잔량대비 | 20 |
| `sel_9th_pre_req` | 매도9차선잔량 | 20 |
| `sel_9th_pre_bid` | 매도9차선호가 | 20 |
| `sel_8th_pre_req_pre` | 매도8차선잔량대비 | 20 |
| `sel_8th_pre_req` | 매도8차선잔량 | 20 |
| `sel_8th_pre_bid` | 매도8차선호가 | 20 |
| `sel_7th_pre_req_pre` | 매도7차선잔량대비 | 20 |
| `sel_7th_pre_req` | 매도7차선잔량 | 20 |
| `sel_7th_pre_bid` | 매도7차선호가 | 20 |
| `sel_6th_pre_req_pre` | 매도6차선잔량대비 | 20 |
| `sel_6th_pre_req` | 매도6차선잔량 | 20 |
| `sel_6th_pre_bid` | 매도6차선호가 | 20 |
| `sel_5th_pre_req_pre` | 매도5차선잔량대비 | 20 |
| `sel_5th_pre_req` | 매도5차선잔량 | 20 |
| `sel_5th_pre_bid` | 매도5차선호가 | 20 |
| `sel_4th_pre_req_pre` | 매도4차선잔량대비 | 20 |
| `sel_4th_pre_req` | 매도4차선잔량 | 20 |
| `sel_4th_pre_bid` | 매도4차선호가 | 20 |
| `sel_3th_pre_req_pre` | 매도3차선잔량대비 | 20 |
| `sel_3th_pre_req` | 매도3차선잔량 | 20 |
| `sel_3th_pre_bid` | 매도3차선호가 | 20 |
| `sel_2th_pre_req_pre` | 매도2차선잔량대비 | 20 |
| `sel_2th_pre_req` | 매도2차선잔량 | 20 |
| `sel_2th_pre_bid` | 매도2차선호가 | 20 |
| `sel_1th_pre_req_pre` | 매도1차선잔량대비 | 20 |
| `sel_fpr_req` | 매도최우선잔량 | 20 |
| `sel_fpr_bid` | 매도최우선호가 | 20 |
| `buy_fpr_bid` | 매수최우선호가 | 20 |
| `buy_fpr_req` | 매수최우선잔량 | 20 |
| `buy_1th_pre_req_pre` | 매수1차선잔량대비 | 20 |
| `buy_2th_pre_bid` | 매수2차선호가 | 20 |
| `buy_2th_pre_req` | 매수2차선잔량 | 20 |
| `buy_2th_pre_req_pre` | 매수2차선잔량대비 | 20 |
| `buy_3th_pre_bid` | 매수3차선호가 | 20 |
| `buy_3th_pre_req` | 매수3차선잔량 | 20 |
| `buy_3th_pre_req_pre` | 매수3차선잔량대비 | 20 |
| `buy_4th_pre_bid` | 매수4차선호가 | 20 |
| `buy_4th_pre_req` | 매수4차선잔량 | 20 |
| `buy_4th_pre_req_pre` | 매수4차선잔량대비 | 20 |
| `buy_5th_pre_bid` | 매수5차선호가 | 20 |
| `buy_5th_pre_req` | 매수5차선잔량 | 20 |
| `buy_5th_pre_req_pre` | 매수5차선잔량대비 | 20 |
| `buy_6th_pre_bid` | 매수6차선호가 | 20 |
| `buy_6th_pre_req` | 매수6차선잔량 | 20 |
| `buy_6th_pre_req_pre` | 매수6차선잔량대비 | 20 |
| `buy_7th_pre_bid` | 매수7차선호가 | 20 |
| `buy_7th_pre_req` | 매수7차선잔량 | 20 |
| `buy_7th_pre_req_pre` | 매수7차선잔량대비 | 20 |
| `buy_8th_pre_bid` | 매수8차선호가 | 20 |
| `buy_8th_pre_req` | 매수8차선잔량 | 20 |
| `buy_8th_pre_req_pre` | 매수8차선잔량대비 | 20 |
| `buy_9th_pre_bid` | 매수9차선호가 | 20 |
| `buy_9th_pre_req` | 매수9차선잔량 | 20 |
| `buy_9th_pre_req_pre` | 매수9차선잔량대비 | 20 |
| `buy_10th_pre_bid` | 매수10차선호가 | 20 |
| `buy_10th_pre_req` | 매수10차선잔량 | 20 |
| `buy_10th_pre_req_pre` | 매수10차선잔량대비 | 20 |
| `tot_sel_req_jub_pre` | 총매도잔량직전대비 | 20 |
| `tot_sel_req` | 총매도잔량 | 20 |
| `tot_buy_req` | 총매수잔량 | 20 |
| `tot_buy_req_jub_pre` | 총매수잔량직전대비 | 20 |
| `ovt_sel_req_pre` | 시간외매도잔량대비 | 20 |
| `ovt_sel_req` | 시간외매도잔량 | 20 |
| `ovt_buy_req` | 시간외매수잔량 | 20 |
| `ovt_buy_req_pre` | 시간외매수잔량대비 | 20 |

<a id="ka10005"></a>

## `ka10005` · `stock_daily_weekly_monthly()` — 주식일주월시분요청

주식일주월시분요청 (Stock Daily/Weekly/Monthly by Time) · `POST /api/dostk/mrkcond`

```python
api.market.stock_daily_weekly_monthly(stk_cd=...)
```

**요청**

| 필드 | 한글명 | 필수 | 길이 |
|---|---|:---:|---:|
| `stk_cd` | 종목코드 | Y | 20 |

**응답**

| 필드 | 한글명 | 길이 |
|---|---|---:|
| `stk_ddwkmm` (list) | 주식일주월시분 |  |
| `stk_ddwkmm[].date` | 날짜 | 20 |
| `stk_ddwkmm[].open_pric` | 시가 | 20 |
| `stk_ddwkmm[].high_pric` | 고가 | 20 |
| `stk_ddwkmm[].low_pric` | 저가 | 20 |
| `stk_ddwkmm[].close_pric` | 종가 | 20 |
| `stk_ddwkmm[].pre` | 대비 | 20 |
| `stk_ddwkmm[].flu_rt` | 등락률 | 20 |
| `stk_ddwkmm[].trde_qty` | 거래량 | 20 |
| `stk_ddwkmm[].trde_prica` | 거래대금 | 20 |
| `stk_ddwkmm[].for_poss` | 외인보유 | 20 |
| `stk_ddwkmm[].for_wght` | 외인비중 | 20 |
| `stk_ddwkmm[].for_netprps` | 외인순매수 | 20 |
| `stk_ddwkmm[].orgn_netprps` | 기관순매수 | 20 |
| `stk_ddwkmm[].ind_netprps` | 개인순매수 | 20 |
| `stk_ddwkmm[].frgn` | 외국계 | 20 |
| `stk_ddwkmm[].crd_remn_rt` | 신용잔고율 | 20 |
| `stk_ddwkmm[].prm` | 프로그램 | 20 |

<a id="ka10006"></a>

## `ka10006` · `stock_minute_price()` — 주식시분요청

주식시분요청 (Stock Minute Price) · `POST /api/dostk/mrkcond`

```python
api.market.stock_minute_price(stk_cd=...)
```

**요청**

| 필드 | 한글명 | 필수 | 길이 |
|---|---|:---:|---:|
| `stk_cd` | 종목코드 | Y | 20 |

**응답**

| 필드 | 한글명 | 길이 |
|---|---|---:|
| `date` | 날짜 | 20 |
| `open_pric` | 시가 | 20 |
| `high_pric` | 고가 | 20 |
| `low_pric` | 저가 | 20 |
| `close_pric` | 종가 | 20 |
| `pre` | 대비 | 20 |
| `flu_rt` | 등락률 | 20 |
| `trde_qty` | 거래량 | 20 |
| `trde_prica` | 거래대금 | 20 |
| `cntr_str` | 체결강도 | 20 |

<a id="ka10007"></a>

## `ka10007` · `order_book_info()` — 시세표성정보요청

시세표성정보요청 (Order Book Info) · `POST /api/dostk/mrkcond`

```python
api.market.order_book_info(stk_cd=...)
```

**요청**

| 필드 | 한글명 | 필수 | 길이 |
|---|---|:---:|---:|
| `stk_cd` | 종목코드 | Y | 20 |

**응답**

| 필드 | 한글명 | 길이 |
|---|---|---:|
| `stk_nm` | 종목명 | 40 |
| `stk_cd` | 종목코드 | 6 |
| `date` | 날짜 | 20 |
| `tm` | 시간 | 20 |
| `pred_close_pric` | 전일종가 | 20 |
| `pred_trde_qty` | 전일거래량 | 20 |
| `upl_pric` | 상한가 | 20 |
| `lst_pric` | 하한가 | 20 |
| `pred_trde_prica` | 전일거래대금 | 20 |
| `flo_stkcnt` | 상장주식수 | 20 |
| `cur_prc` | 현재가 | 20 |
| `smbol` | 부호 | 20 |
| `flu_rt` | 등락률 | 20 |
| `pred_rt` | 전일비 | 20 |
| `open_pric` | 시가 | 20 |
| `high_pric` | 고가 | 20 |
| `low_pric` | 저가 | 20 |
| `cntr_qty` | 체결량 | 20 |
| `trde_qty` | 거래량 | 20 |
| `trde_prica` | 거래대금 | 20 |
| `exp_cntr_pric` | 예상체결가 | 20 |
| `exp_cntr_qty` | 예상체결량 | 20 |
| `exp_sel_pri_bid` | 예상매도우선호가 | 20 |
| `exp_buy_pri_bid` | 예상매수우선호가 | 20 |
| `trde_strt_dt` | 거래시작일 | 20 |
| `exec_pric` | 행사가격 | 20 |
| `hgst_pric` | 최고가 | 20 |
| `lwst_pric` | 최저가 | 20 |
| `hgst_pric_dt` | 최고가일 | 20 |
| `lwst_pric_dt` | 최저가일 | 20 |
| `sel_1bid` | 매도1호가 | 20 |
| `sel_2bid` | 매도2호가 | 20 |
| `sel_3bid` | 매도3호가 | 20 |
| `sel_4bid` | 매도4호가 | 20 |
| `sel_5bid` | 매도5호가 | 20 |
| `sel_6bid` | 매도6호가 | 20 |
| `sel_7bid` | 매도7호가 | 20 |
| `sel_8bid` | 매도8호가 | 20 |
| `sel_9bid` | 매도9호가 | 20 |
| `sel_10bid` | 매도10호가 | 20 |
| `buy_1bid` | 매수1호가 | 20 |
| `buy_2bid` | 매수2호가 | 20 |
| `buy_3bid` | 매수3호가 | 20 |
| `buy_4bid` | 매수4호가 | 20 |
| `buy_5bid` | 매수5호가 | 20 |
| `buy_6bid` | 매수6호가 | 20 |
| `buy_7bid` | 매수7호가 | 20 |
| `buy_8bid` | 매수8호가 | 20 |
| `buy_9bid` | 매수9호가 | 20 |
| `buy_10bid` | 매수10호가 | 20 |
| `sel_1bid_req` | 매도1호가잔량 | 20 |
| `sel_2bid_req` | 매도2호가잔량 | 20 |
| `sel_3bid_req` | 매도3호가잔량 | 20 |
| `sel_4bid_req` | 매도4호가잔량 | 20 |
| `sel_5bid_req` | 매도5호가잔량 | 20 |
| `sel_6bid_req` | 매도6호가잔량 | 20 |
| `sel_7bid_req` | 매도7호가잔량 | 20 |
| `sel_8bid_req` | 매도8호가잔량 | 20 |
| `sel_9bid_req` | 매도9호가잔량 | 20 |
| `sel_10bid_req` | 매도10호가잔량 | 20 |
| `buy_1bid_req` | 매수1호가잔량 | 20 |
| `buy_2bid_req` | 매수2호가잔량 | 20 |
| `buy_3bid_req` | 매수3호가잔량 | 20 |
| `buy_4bid_req` | 매수4호가잔량 | 20 |
| `buy_5bid_req` | 매수5호가잔량 | 20 |
| `buy_6bid_req` | 매수6호가잔량 | 20 |
| `buy_7bid_req` | 매수7호가잔량 | 20 |
| `buy_8bid_req` | 매수8호가잔량 | 20 |
| `buy_9bid_req` | 매수9호가잔량 | 20 |
| `buy_10bid_req` | 매수10호가잔량 | 20 |
| `sel_1bid_jub_pre` | 매도1호가직전대비 | 20 |
| `sel_2bid_jub_pre` | 매도2호가직전대비 | 20 |
| `sel_3bid_jub_pre` | 매도3호가직전대비 | 20 |
| `sel_4bid_jub_pre` | 매도4호가직전대비 | 20 |
| `sel_5bid_jub_pre` | 매도5호가직전대비 | 20 |
| `sel_6bid_jub_pre` | 매도6호가직전대비 | 20 |
| `sel_7bid_jub_pre` | 매도7호가직전대비 | 20 |
| `sel_8bid_jub_pre` | 매도8호가직전대비 | 20 |
| `sel_9bid_jub_pre` | 매도9호가직전대비 | 20 |
| `sel_10bid_jub_pre` | 매도10호가직전대비 | 20 |
| `buy_1bid_jub_pre` | 매수1호가직전대비 | 20 |
| `buy_2bid_jub_pre` | 매수2호가직전대비 | 20 |
| `buy_3bid_jub_pre` | 매수3호가직전대비 | 20 |
| `buy_4bid_jub_pre` | 매수4호가직전대비 | 20 |
| `buy_5bid_jub_pre` | 매수5호가직전대비 | 20 |
| `buy_6bid_jub_pre` | 매수6호가직전대비 | 20 |
| `buy_7bid_jub_pre` | 매수7호가직전대비 | 20 |
| `buy_8bid_jub_pre` | 매수8호가직전대비 | 20 |
| `buy_9bid_jub_pre` | 매수9호가직전대비 | 20 |
| `buy_10bid_jub_pre` | 매수10호가직전대비 | 20 |
| `sel_1bid_cnt` | 매도1호가건수 | 20 |
| `sel_2bid_cnt` | 매도2호가건수 | 20 |
| `sel_3bid_cnt` | 매도3호가건수 | 20 |
| `sel_4bid_cnt` | 매도4호가건수 | 20 |
| `sel_5bid_cnt` | 매도5호가건수 | 20 |
| `buy_1bid_cnt` | 매수1호가건수 | 20 |
| `buy_2bid_cnt` | 매수2호가건수 | 20 |
| `buy_3bid_cnt` | 매수3호가건수 | 20 |
| `buy_4bid_cnt` | 매수4호가건수 | 20 |
| `buy_5bid_cnt` | 매수5호가건수 | 20 |
| `lpsel_1bid_req` | LP매도1호가잔량 | 20 |
| `lpsel_2bid_req` | LP매도2호가잔량 | 20 |
| `lpsel_3bid_req` | LP매도3호가잔량 | 20 |
| `lpsel_4bid_req` | LP매도4호가잔량 | 20 |
| `lpsel_5bid_req` | LP매도5호가잔량 | 20 |
| `lpsel_6bid_req` | LP매도6호가잔량 | 20 |
| `lpsel_7bid_req` | LP매도7호가잔량 | 20 |
| `lpsel_8bid_req` | LP매도8호가잔량 | 20 |
| `lpsel_9bid_req` | LP매도9호가잔량 | 20 |
| `lpsel_10bid_req` | LP매도10호가잔량 | 20 |
| `lpbuy_1bid_req` | LP매수1호가잔량 | 20 |
| `lpbuy_2bid_req` | LP매수2호가잔량 | 20 |
| `lpbuy_3bid_req` | LP매수3호가잔량 | 20 |
| `lpbuy_4bid_req` | LP매수4호가잔량 | 20 |
| `lpbuy_5bid_req` | LP매수5호가잔량 | 20 |
| `lpbuy_6bid_req` | LP매수6호가잔량 | 20 |
| `lpbuy_7bid_req` | LP매수7호가잔량 | 20 |
| `lpbuy_8bid_req` | LP매수8호가잔량 | 20 |
| `lpbuy_9bid_req` | LP매수9호가잔량 | 20 |
| `lpbuy_10bid_req` | LP매수10호가잔량 | 20 |
| `tot_buy_req` | 총매수잔량 | 20 |
| `tot_sel_req` | 총매도잔량 | 20 |
| `tot_buy_cnt` | 총매수건수 | 20 |
| `tot_sel_cnt` | 총매도건수 | 20 |

<a id="ka10011"></a>

## `ka10011` · `rights_issue_price()` — 신주인수권전체시세요청

신주인수권전체시세요청 (Rights Issue Price) · `POST /api/dostk/mrkcond`

```python
api.market.rights_issue_price(newstk_recvrht_tp=...)
```

**요청**

| 필드 | 한글명 | 필수 | 길이 |
|---|---|:---:|---:|
| `newstk_recvrht_tp` | 신주인수권구분 | Y | 2 |

**응답**

| 필드 | 한글명 | 길이 |
|---|---|---:|
| `newstk_recvrht_mrpr` (list) | 신주인수권시세 |  |
| `newstk_recvrht_mrpr[].stk_cd` | 종목코드 | 20 |
| `newstk_recvrht_mrpr[].stk_nm` | 종목명 | 40 |
| `newstk_recvrht_mrpr[].cur_prc` | 현재가 | 20 |
| `newstk_recvrht_mrpr[].pred_pre_sig` | 전일대비기호 | 20 |
| `newstk_recvrht_mrpr[].pred_pre` | 전일대비 | 20 |
| `newstk_recvrht_mrpr[].flu_rt` | 등락율 | 20 |
| `newstk_recvrht_mrpr[].fpr_sel_bid` | 최우선매도호가 | 20 |
| `newstk_recvrht_mrpr[].fpr_buy_bid` | 최우선매수호가 | 20 |
| `newstk_recvrht_mrpr[].acc_trde_qty` | 누적거래량 | 20 |
| `newstk_recvrht_mrpr[].open_pric` | 시가 | 20 |
| `newstk_recvrht_mrpr[].high_pric` | 고가 | 20 |
| `newstk_recvrht_mrpr[].low_pric` | 저가 | 20 |

<a id="ka10044"></a>

## `ka10044` · `daily_institutional_trading()` — 일별기관매매종목요청

일별기관매매종목요청 (Daily Institutional Trading by Stock) · `POST /api/dostk/mrkcond`

```python
api.market.daily_institutional_trading(strt_dt=..., end_dt=..., trde_tp=..., mrkt_tp=..., stex_tp=...)
```

**요청**

| 필드 | 한글명 | 필수 | 길이 |
|---|---|:---:|---:|
| `strt_dt` | 시작일자 | Y | 8 |
| `end_dt` | 종료일자 | Y | 8 |
| `trde_tp` | 매매구분 | Y | 1 |
| `mrkt_tp` | 시장구분 | Y | 3 |
| `stex_tp` | 거래소구분 | Y | 1 |

**응답**

| 필드 | 한글명 | 길이 |
|---|---|---:|
| `daly_orgn_trde_stk` (list) | 일별기관매매종목 |  |
| `daly_orgn_trde_stk[].stk_cd` | 종목코드 | 20 |
| `daly_orgn_trde_stk[].stk_nm` | 종목명 | 40 |
| `daly_orgn_trde_stk[].netprps_qty` | 순매수수량 | 20 |
| `daly_orgn_trde_stk[].netprps_amt` | 순매수금액 | 20 |

<a id="ka10045"></a>

## `ka10045` · `institutional_trading_trend()` — 종목별기관매매추이요청

종목별기관매매추이요청 (Institutional Trading Trend by Stock) · `POST /api/dostk/mrkcond`

```python
api.market.institutional_trading_trend(stk_cd=..., strt_dt=..., end_dt=..., orgn_prsm_unp_tp=..., for_prsm_unp_tp=...)
```

**요청**

| 필드 | 한글명 | 필수 | 길이 |
|---|---|:---:|---:|
| `stk_cd` | 종목코드 | Y | 20 |
| `strt_dt` | 시작일자 | Y | 8 |
| `end_dt` | 종료일자 | Y | 8 |
| `orgn_prsm_unp_tp` | 기관추정단가구분 | Y | 1 |
| `for_prsm_unp_tp` | 외인추정단가구분 | Y | 1 |

**응답**

| 필드 | 한글명 | 길이 |
|---|---|---:|
| `orgn_prsm_avg_pric` | 기관추정평균가 |  |
| `for_prsm_avg_pric` | 외인추정평균가 |  |
| `stk_orgn_trde_trnsn` (list) | 종목별기관매매추이 |  |
| `stk_orgn_trde_trnsn[].dt` | 일자 | 20 |
| `stk_orgn_trde_trnsn[].close_pric` | 종가 | 20 |
| `stk_orgn_trde_trnsn[].pre_sig` | 대비기호 | 20 |
| `stk_orgn_trde_trnsn[].pred_pre` | 전일대비 | 20 |
| `stk_orgn_trde_trnsn[].flu_rt` | 등락율 | 20 |
| `stk_orgn_trde_trnsn[].trde_qty` | 거래량 | 20 |
| `stk_orgn_trde_trnsn[].orgn_dt_acc` | 기관기간누적 | 20 |
| `stk_orgn_trde_trnsn[].orgn_daly_nettrde_qty` | 기관일별순매매수량 | 20 |
| `stk_orgn_trde_trnsn[].for_dt_acc` | 외인기간누적 | 20 |
| `stk_orgn_trde_trnsn[].for_daly_nettrde_qty` | 외인일별순매매수량 | 20 |
| `stk_orgn_trde_trnsn[].limit_exh_rt` | 한도소진율 | 20 |

<a id="ka10046"></a>

## `ka10046` · `hourly_execution_strength()` — 체결강도추이시간별요청

체결강도추이시간별요청 (Hourly Execution Strength) · `POST /api/dostk/mrkcond`

```python
api.market.hourly_execution_strength(stk_cd=...)
```

**요청**

| 필드 | 한글명 | 필수 | 길이 |
|---|---|:---:|---:|
| `stk_cd` | 종목코드 | Y | 6 |

**응답**

| 필드 | 한글명 | 길이 |
|---|---|---:|
| `cntr_str_tm` (list) | 체결강도시간별 |  |
| `cntr_str_tm[].cntr_tm` | 체결시간 | 20 |
| `cntr_str_tm[].cur_prc` | 현재가 | 20 |
| `cntr_str_tm[].pred_pre` | 전일대비 | 20 |
| `cntr_str_tm[].pred_pre_sig` | 전일대비기호 | 20 |
| `cntr_str_tm[].flu_rt` | 등락율 | 20 |
| `cntr_str_tm[].trde_qty` | 거래량 | 20 |
| `cntr_str_tm[].acc_trde_prica` | 누적거래대금 | 20 |
| `cntr_str_tm[].acc_trde_qty` | 누적거래량 | 20 |
| `cntr_str_tm[].cntr_str` | 체결강도 | 20 |
| `cntr_str_tm[].cntr_str_5min` | 체결강도5분 | 20 |
| `cntr_str_tm[].cntr_str_20min` | 체결강도20분 | 20 |
| `cntr_str_tm[].cntr_str_60min` | 체결강도60분 | 20 |
| `cntr_str_tm[].stex_tp` | 거래소구분 | 20 |

<a id="ka10047"></a>

## `ka10047` · `daily_execution_strength()` — 체결강도추이일별요청

체결강도추이일별요청 (Daily Execution Strength) · `POST /api/dostk/mrkcond`

```python
api.market.daily_execution_strength(stk_cd=...)
```

**요청**

| 필드 | 한글명 | 필수 | 길이 |
|---|---|:---:|---:|
| `stk_cd` | 종목코드 | Y | 6 |

**응답**

| 필드 | 한글명 | 길이 |
|---|---|---:|
| `cntr_str_daly` (list) | 체결강도일별 |  |
| `cntr_str_daly[].dt` | 일자 | 20 |
| `cntr_str_daly[].cur_prc` | 현재가 | 20 |
| `cntr_str_daly[].pred_pre` | 전일대비 | 20 |
| `cntr_str_daly[].pred_pre_sig` | 전일대비기호 | 20 |
| `cntr_str_daly[].flu_rt` | 등락율 | 20 |
| `cntr_str_daly[].trde_qty` | 거래량 | 20 |
| `cntr_str_daly[].acc_trde_prica` | 누적거래대금 | 20 |
| `cntr_str_daly[].acc_trde_qty` | 누적거래량 | 20 |
| `cntr_str_daly[].cntr_str` | 체결강도 | 20 |
| `cntr_str_daly[].cntr_str_5min` | 체결강도5일 | 20 |
| `cntr_str_daly[].cntr_str_20min` | 체결강도20일 | 20 |
| `cntr_str_daly[].cntr_str_60min` | 체결강도60일 | 20 |

<a id="ka10063"></a>

## `ka10063` · `intraday_investor_trading()` — 장중투자자별매매요청

장중투자자별매매요청 (Intraday Investor Trading by Time Slot) · `POST /api/dostk/mrkcond`

```python
api.market.intraday_investor_trading(mrkt_tp=..., amt_qty_tp=..., invsr=..., frgn_all=..., smtm_netprps_tp=..., stex_tp=...)
```

**요청**

| 필드 | 한글명 | 필수 | 길이 |
|---|---|:---:|---:|
| `mrkt_tp` | 시장구분 | Y | 3 |
| `amt_qty_tp` | 금액수량구분 | Y | 1 |
| `invsr` | 투자자별 | Y | 1 |
| `frgn_all` | 외국계전체 | Y | 1 |
| `smtm_netprps_tp` | 동시순매수구분 | Y | 1 |
| `stex_tp` | 거래소구분 | Y | 1 |

**응답**

| 필드 | 한글명 | 길이 |
|---|---|---:|
| `opmr_invsr_trde` (list) | 장중투자자별매매 |  |
| `opmr_invsr_trde[].stk_cd` | 종목코드 | 20 |
| `opmr_invsr_trde[].stk_nm` | 종목명 | 40 |
| `opmr_invsr_trde[].cur_prc` | 현재가 | 20 |
| `opmr_invsr_trde[].pre_sig` | 대비기호 | 20 |
| `opmr_invsr_trde[].pred_pre` | 전일대비 | 20 |
| `opmr_invsr_trde[].flu_rt` | 등락율 | 20 |
| `opmr_invsr_trde[].acc_trde_qty` | 누적거래량 | 20 |
| `opmr_invsr_trde[].netprps_amt` | 순매수금액 | 20 |
| `opmr_invsr_trde[].prev_netprps_amt` | 이전순매수금액 | 20 |
| `opmr_invsr_trde[].buy_amt` | 매수금액 | 20 |
| `opmr_invsr_trde[].netprps_amt_irds` | 순매수금액증감 | 20 |
| `opmr_invsr_trde[].buy_amt_irds` | 매수금액증감 | 20 |
| `opmr_invsr_trde[].sell_amt` | 매도금액 | 20 |
| `opmr_invsr_trde[].sell_amt_irds` | 매도금액증감 | 20 |
| `opmr_invsr_trde[].netprps_qty` | 순매수수량 | 20 |
| `opmr_invsr_trde[].prev_pot_netprps_qty` | 이전시점순매수수량 | 20 |
| `opmr_invsr_trde[].netprps_irds` | 순매수증감 | 20 |
| `opmr_invsr_trde[].buy_qty` | 매수수량 | 20 |
| `opmr_invsr_trde[].buy_qty_irds` | 매수수량증감 | 20 |
| `opmr_invsr_trde[].sell_qty` | 매도수량 | 20 |
| `opmr_invsr_trde[].sell_qty_irds` | 매도수량증감 | 20 |

<a id="ka10066"></a>

## `ka10066` · `after_hours_investor_trading()` — 장마감후투자자별매매요청

장마감후투자자별매매요청 (After-Hours Investor Trading) · `POST /api/dostk/mrkcond`

```python
api.market.after_hours_investor_trading(mrkt_tp=..., amt_qty_tp=..., trde_tp=..., stex_tp=...)
```

**요청**

| 필드 | 한글명 | 필수 | 길이 |
|---|---|:---:|---:|
| `mrkt_tp` | 시장구분 | Y | 3 |
| `amt_qty_tp` | 금액수량구분 | Y | 1 |
| `trde_tp` | 매매구분 | Y | 1 |
| `stex_tp` | 거래소구분 | Y | 1 |

**응답**

| 필드 | 한글명 | 길이 |
|---|---|---:|
| `opaf_invsr_trde` (list) | 장중투자자별매매차트 |  |
| `opaf_invsr_trde[].stk_cd` | 종목코드 | 20 |
| `opaf_invsr_trde[].stk_nm` | 종목명 | 40 |
| `opaf_invsr_trde[].cur_prc` | 현재가 | 20 |
| `opaf_invsr_trde[].pre_sig` | 대비기호 | 20 |
| `opaf_invsr_trde[].pred_pre` | 전일대비 | 20 |
| `opaf_invsr_trde[].flu_rt` | 등락률 | 20 |
| `opaf_invsr_trde[].trde_qty` | 거래량 | 20 |
| `opaf_invsr_trde[].ind_invsr` | 개인투자자 | 20 |
| `opaf_invsr_trde[].frgnr_invsr` | 외국인투자자 | 20 |
| `opaf_invsr_trde[].orgn` | 기관계 | 20 |
| `opaf_invsr_trde[].fnnc_invt` | 금융투자 | 20 |
| `opaf_invsr_trde[].insrnc` | 보험 | 20 |
| `opaf_invsr_trde[].invtrt` | 투신 | 20 |
| `opaf_invsr_trde[].etc_fnnc` | 기타금융 | 20 |
| `opaf_invsr_trde[].bank` | 은행 | 20 |
| `opaf_invsr_trde[].penfnd_etc` | 연기금등 | 20 |
| `opaf_invsr_trde[].samo_fund` | 사모펀드 | 20 |
| `opaf_invsr_trde[].natn` | 국가 | 20 |
| `opaf_invsr_trde[].etc_corp` | 기타법인 | 20 |

<a id="ka10078"></a>

## `ka10078` · `broker_stock_trading_trend()` — 증권사별종목매매동향요청

증권사별종목매매동향요청 (Broker Stock Trading Trend) · `POST /api/dostk/mrkcond`

```python
api.market.broker_stock_trading_trend(mmcm_cd=..., stk_cd=..., strt_dt=..., end_dt=...)
```

**요청**

| 필드 | 한글명 | 필수 | 길이 |
|---|---|:---:|---:|
| `mmcm_cd` | 회원사코드 | Y | 3 |
| `stk_cd` | 종목코드 | Y | 20 |
| `strt_dt` | 시작일자 | Y | 8 |
| `end_dt` | 종료일자 | Y | 8 |

**응답**

| 필드 | 한글명 | 길이 |
|---|---|---:|
| `sec_stk_trde_trend` (list) | 증권사별종목매매동향 |  |
| `sec_stk_trde_trend[].dt` | 일자 | 20 |
| `sec_stk_trde_trend[].cur_prc` | 현재가 | 20 |
| `sec_stk_trde_trend[].pre_sig` | 대비기호 | 20 |
| `sec_stk_trde_trend[].pred_pre` | 전일대비 | 20 |
| `sec_stk_trde_trend[].flu_rt` | 등락율 | 20 |
| `sec_stk_trde_trend[].acc_trde_qty` | 누적거래량 | 20 |
| `sec_stk_trde_trend[].netprps_qty` | 순매수수량 | 20 |
| `sec_stk_trde_trend[].buy_qty` | 매수수량 | 20 |
| `sec_stk_trde_trend[].sell_qty` | 매도수량 | 20 |

<a id="ka10086"></a>

## `ka10086` · `daily_stock_price()` — 일별주가요청

일자별주가요청 (Daily Stock Price) · `POST /api/dostk/mrkcond`

```python
api.market.daily_stock_price(stk_cd=..., qry_dt=..., indc_tp=...)
```

**요청**

| 필드 | 한글명 | 필수 | 길이 |
|---|---|:---:|---:|
| `stk_cd` | 종목코드 | Y | 20 |
| `qry_dt` | 조회일자 | Y | 8 |
| `indc_tp` | 표시구분 | Y | 1 |

**응답**

| 필드 | 한글명 | 길이 |
|---|---|---:|
| `daly_stkpc` (list) | 일별주가 |  |
| `daly_stkpc[].date` | 날짜 | 20 |
| `daly_stkpc[].open_pric` | 시가 | 20 |
| `daly_stkpc[].high_pric` | 고가 | 20 |
| `daly_stkpc[].low_pric` | 저가 | 20 |
| `daly_stkpc[].close_pric` | 종가 | 20 |
| `daly_stkpc[].pred_rt` | 전일비 | 20 |
| `daly_stkpc[].flu_rt` | 등락률 | 20 |
| `daly_stkpc[].trde_qty` | 거래량 | 20 |
| `daly_stkpc[].amt_mn` | 금액(백만) | 20 |
| `daly_stkpc[].crd_rt` | 신용비 | 20 |
| `daly_stkpc[].ind` | 개인 | 20 |
| `daly_stkpc[].orgn` | 기관 | 20 |
| `daly_stkpc[].for_qty` | 외인수량 | 20 |
| `daly_stkpc[].frgn` | 외국계 | 20 |
| `daly_stkpc[].prm` | 프로그램 | 20 |
| `daly_stkpc[].for_rt` | 외인비 | 20 |
| `daly_stkpc[].for_poss` | 외인보유 | 20 |
| `daly_stkpc[].for_wght` | 외인비중 | 20 |
| `daly_stkpc[].for_netprps` | 외인순매수 | 20 |
| `daly_stkpc[].orgn_netprps` | 기관순매수 | 20 |
| `daly_stkpc[].ind_netprps` | 개인순매수 | 20 |
| `daly_stkpc[].crd_remn_rt` | 신용잔고율 | 20 |

<a id="ka10087"></a>

## `ka10087` · `after_hours_single_price()` — 시간외단일가요청

시간외단일가요청 (After-Hours Single Price) · `POST /api/dostk/mrkcond`

```python
api.market.after_hours_single_price(stk_cd=...)
```

**요청**

| 필드 | 한글명 | 필수 | 길이 |
|---|---|:---:|---:|
| `stk_cd` | 종목코드 | Y | 6 |

**응답**

| 필드 | 한글명 | 길이 |
|---|---|---:|
| `bid_req_base_tm` | 호가잔량기준시간 |  |
| `ovt_sigpric_sel_bid_jub_pre_5` | 시간외단일가_매도호가직전대비5 |  |
| `ovt_sigpric_sel_bid_jub_pre_4` | 시간외단일가_매도호가직전대비4 |  |
| `ovt_sigpric_sel_bid_jub_pre_3` | 시간외단일가_매도호가직전대비3 |  |
| `ovt_sigpric_sel_bid_jub_pre_2` | 시간외단일가_매도호가직전대비2 |  |
| `ovt_sigpric_sel_bid_jub_pre_1` | 시간외단일가_매도호가직전대비1 |  |
| `ovt_sigpric_sel_bid_qty_5` | 시간외단일가_매도호가수량5 |  |
| `ovt_sigpric_sel_bid_qty_4` | 시간외단일가_매도호가수량4 |  |
| `ovt_sigpric_sel_bid_qty_3` | 시간외단일가_매도호가수량3 |  |
| `ovt_sigpric_sel_bid_qty_2` | 시간외단일가_매도호가수량2 |  |
| `ovt_sigpric_sel_bid_qty_1` | 시간외단일가_매도호가수량1 |  |
| `ovt_sigpric_sel_bid_5` | 시간외단일가_매도호가5 |  |
| `ovt_sigpric_sel_bid_4` | 시간외단일가_매도호가4 |  |
| `ovt_sigpric_sel_bid_3` | 시간외단일가_매도호가3 |  |
| `ovt_sigpric_sel_bid_2` | 시간외단일가_매도호가2 |  |
| `ovt_sigpric_sel_bid_1` | 시간외단일가_매도호가1 |  |
| `ovt_sigpric_buy_bid_1` | 시간외단일가_매수호가1 |  |
| `ovt_sigpric_buy_bid_2` | 시간외단일가_매수호가2 |  |
| `ovt_sigpric_buy_bid_3` | 시간외단일가_매수호가3 |  |
| `ovt_sigpric_buy_bid_4` | 시간외단일가_매수호가4 |  |
| `ovt_sigpric_buy_bid_5` | 시간외단일가_매수호가5 |  |
| `ovt_sigpric_buy_bid_qty_1` | 시간외단일가_매수호가수량1 |  |
| `ovt_sigpric_buy_bid_qty_2` | 시간외단일가_매수호가수량2 |  |
| `ovt_sigpric_buy_bid_qty_3` | 시간외단일가_매수호가수량3 |  |
| `ovt_sigpric_buy_bid_qty_4` | 시간외단일가_매수호가수량4 |  |
| `ovt_sigpric_buy_bid_qty_5` | 시간외단일가_매수호가수량5 |  |
| `ovt_sigpric_buy_bid_jub_pre_1` | 시간외단일가_매수호가직전대비1 |  |
| `ovt_sigpric_buy_bid_jub_pre_2` | 시간외단일가_매수호가직전대비2 |  |
| `ovt_sigpric_buy_bid_jub_pre_3` | 시간외단일가_매수호가직전대비3 |  |
| `ovt_sigpric_buy_bid_jub_pre_4` | 시간외단일가_매수호가직전대비4 |  |
| `ovt_sigpric_buy_bid_jub_pre_5` | 시간외단일가_매수호가직전대비5 |  |
| `ovt_sigpric_sel_bid_tot_req` | 시간외단일가_매도호가총잔량 |  |
| `ovt_sigpric_buy_bid_tot_req` | 시간외단일가_매수호가총잔량 |  |
| `sel_bid_tot_req_jub_pre` | 매도호가총잔량직전대비 |  |
| `sel_bid_tot_req` | 매도호가총잔량 |  |
| `buy_bid_tot_req` | 매수호가총잔량 |  |
| `buy_bid_tot_req_jub_pre` | 매수호가총잔량직전대비 |  |
| `ovt_sel_bid_tot_req_jub_pre` | 시간외매도호가총잔량직전대비 |  |
| `ovt_sel_bid_tot_req` | 시간외매도호가총잔량 |  |
| `ovt_buy_bid_tot_req` | 시간외매수호가총잔량 |  |
| `ovt_buy_bid_tot_req_jub_pre` | 시간외매수호가총잔량직전대비 |  |
| `ovt_sigpric_cur_prc` | 시간외단일가_현재가 |  |
| `ovt_sigpric_pred_pre_sig` | 시간외단일가_전일대비기호 |  |
| `ovt_sigpric_pred_pre` | 시간외단일가_전일대비 |  |
| `ovt_sigpric_flu_rt` | 시간외단일가_등락률 |  |
| `ovt_sigpric_acc_trde_qty` | 시간외단일가_누적거래량 |  |

<a id="ka50010"></a>

## `ka50010` · `gold_spot_execution_trend()` — 금현물체결추이

금현물체결추이 (Gold Spot Execution Trend) · `POST /api/dostk/mrkcond`

```python
api.market.gold_spot_execution_trend(stk_cd=...)
```

**요청**

| 필드 | 한글명 | 필수 | 길이 |
|---|---|:---:|---:|
| `stk_cd` | 종목코드 | Y | 20 |

**응답**

| 필드 | 한글명 | 길이 |
|---|---|---:|
| `gold_cntr` (list) | 금현물체결추이 |  |
| `gold_cntr[].cntr_pric` | 체결가 | 20 |
| `gold_cntr[].pred_pre` | 전일 대비 | 20 |
| `gold_cntr[].flu_rt` | 등락율 | 20 |
| `gold_cntr[].trde_qty` | 누적 거래량 | 20 |
| `gold_cntr[].acc_trde_prica` | 누적 거래대금 | 20 |
| `gold_cntr[].cntr_trde_qty` | 거래량(체결량) | 20 |
| `gold_cntr[].tm` | 체결시간 | 20 |
| `gold_cntr[].pre_sig` | 전일대비기호 | 20 |
| `gold_cntr[].pri_sel_bid_unit` | 매도호가 | 20 |
| `gold_cntr[].pri_buy_bid_unit` | 매수호가 | 20 |
| `gold_cntr[].trde_pre` | 전일 거래량 대비 비율 | 20 |
| `gold_cntr[].trde_tern_rt` | 전일 거래량 대비 순간 거래량 비율 | 20 |
| `gold_cntr[].cntr_str` | 체결강도 | 20 |

<a id="ka50012"></a>

## `ka50012` · `gold_spot_daily_trend()` — 금현물일별추이

금현물일별추이 (Gold Spot Daily Trend) · `POST /api/dostk/mrkcond`

```python
api.market.gold_spot_daily_trend(stk_cd=..., base_dt=...)
```

**요청**

| 필드 | 한글명 | 필수 | 길이 |
|---|---|:---:|---:|
| `stk_cd` | 종목코드 | Y | 20 |
| `base_dt` | 기준일자 | Y | 8 |

**응답**

| 필드 | 한글명 | 길이 |
|---|---|---:|
| `gold_daly_trnsn` (list) | 금현물일별추이 |  |
| `gold_daly_trnsn[].cur_prc` | 종가 | 20 |
| `gold_daly_trnsn[].pred_pre` | 전일 대비 | 20 |
| `gold_daly_trnsn[].flu_rt` | 등락율 | 20 |
| `gold_daly_trnsn[].trde_qty` | 누적 거래량 | 20 |
| `gold_daly_trnsn[].acc_trde_prica` | 누적 거래대금(백만) | 20 |
| `gold_daly_trnsn[].open_pric` | 시가 | 20 |
| `gold_daly_trnsn[].high_pric` | 고가 | 20 |
| `gold_daly_trnsn[].low_pric` | 저가 | 20 |
| `gold_daly_trnsn[].dt` | 일자 | 20 |
| `gold_daly_trnsn[].pre_sig` | 전일대비기호 | 20 |
| `gold_daly_trnsn[].orgn_netprps` | 기관 순매수 수량 | 20 |
| `gold_daly_trnsn[].for_netprps` | 외국인 순매수 수량 | 20 |
| `gold_daly_trnsn[].ind_netprps` | 순매매량(개인) | 20 |

<a id="ka50087"></a>

## `ka50087` · `gold_spot_expected_execution()` — 금현물예상체결

금현물예상체결 (Gold Spot Expected Execution) · `POST /api/dostk/mrkcond`

```python
api.market.gold_spot_expected_execution(stk_cd=...)
```

**요청**

| 필드 | 한글명 | 필수 | 길이 |
|---|---|:---:|---:|
| `stk_cd` | 종목코드 | Y | 20 |

**응답**

| 필드 | 한글명 | 길이 |
|---|---|---:|
| `gold_expt_exec` (list) | 금현물예상체결 |  |
| `gold_expt_exec[].exp_cntr_pric` | 예상 체결가 | 20 |
| `gold_expt_exec[].exp_pred_pre` | 예상 체결가 전일대비 | 20 |
| `gold_expt_exec[].exp_flu_rt` | 예상 체결가 등락율 | 20 |
| `gold_expt_exec[].exp_acc_trde_qty` | 예상 체결 수량(누적) | 20 |
| `gold_expt_exec[].exp_cntr_trde_qty` | 예상 체결 수량 | 20 |
| `gold_expt_exec[].exp_tm` | 예상 체결 시간 | 20 |
| `gold_expt_exec[].exp_pre_sig` | 예상 체결가 전일대비기호 | 20 |
| `gold_expt_exec[].stex_tp` | 거래소 구분 |  |

<a id="ka50100"></a>

## `ka50100` · `gold_spot_price_info()` — 금현물 시세정보

금현물 시세정보 (Gold Spot Price Info) · `POST /api/dostk/mrkcond`

```python
api.market.gold_spot_price_info(stk_cd=...)
```

**요청**

| 필드 | 한글명 | 필수 | 길이 |
|---|---|:---:|---:|
| `stk_cd` | 종목코드 | Y | 20 |

**응답**

| 필드 | 한글명 | 길이 |
|---|---|---:|
| `pred_pre_sig` | 전일대비기호 | 20 |
| `pred_pre` | 전일대비 | 20 |
| `flu_rt` | 등락율 | 20 |
| `trde_qty` | 거래량 | 20 |
| `open_pric` | 시가 | 20 |
| `high_pric` | 고가 | 20 |
| `low_pric` | 저가 | 20 |
| `pred_rt` | 전일비 | 20 |
| `upl_pric` | 상한가 | 20 |
| `lst_pric` | 하한가 | 20 |
| `pred_close_pric` | 전일종가 | 20 |

<a id="ka50101"></a>

## `ka50101` · `gold_spot_order_book()` — 금현물 호가

금현물 호가 (Gold Spot Order Book) · `POST /api/dostk/mrkcond`

```python
api.market.gold_spot_order_book(stk_cd=..., tic_scope=...)
```

**요청**

| 필드 | 한글명 | 필수 | 길이 |
|---|---|:---:|---:|
| `stk_cd` | 종목코드 | Y | 20 |
| `tic_scope` | 틱범위 | Y | 2 |

**응답**

| 필드 | 한글명 | 길이 |
|---|---|---:|
| `gold_bid` (list) | 금현물호가 |  |
| `gold_bid[].cntr_pric` | 체결가 | 20 |
| `gold_bid[].pred_pre` | 전일 대비(원) | 20 |
| `gold_bid[].flu_rt` | 등락율 | 20 |
| `gold_bid[].trde_qty` | 누적 거래량 | 20 |
| `gold_bid[].acc_trde_prica` | 누적 거래대금 | 20 |
| `gold_bid[].cntr_trde_qty` | 거래량(체결량) | 20 |
| `gold_bid[].tm` | 체결시간 | 20 |
| `gold_bid[].pre_sig` | 전일대비기호 | 20 |
| `gold_bid[].pri_sel_bid_unit` | 매도호가 | 20 |
| `gold_bid[].pri_buy_bid_unit` | 매수호가 | 20 |
| `gold_bid[].trde_pre` | 전일 거래량 대비 비율 | 20 |
| `gold_bid[].trde_tern_rt` | 전일 거래량 대비 순간 거래량 비율 |  |
| `gold_bid[].cntr_str` | 체결강도 | 20 |
| `gold_bid[].lpmmcm_nm_1` | K.O 접근도 | 20 |
| `gold_bid[].stex_tp` | 거래소구분 | 20 |

<a id="ka90005"></a>

## `ka90005` · `program_trading_by_time()` — 프로그램매매추이요청 시간대별

프로그램매매추이요청 시간대별 (Program Trading by Time Slot) · `POST /api/dostk/mrkcond`

```python
api.market.program_trading_by_time(date=..., amt_qty_tp=..., mrkt_tp=..., min_tic_tp=..., stex_tp=...)
```

**요청**

| 필드 | 한글명 | 필수 | 길이 |
|---|---|:---:|---:|
| `date` | 날짜 | Y | 8 |
| `amt_qty_tp` | 금액수량구분 | Y | 1 |
| `mrkt_tp` | 시장구분 | Y | 10 |
| `min_tic_tp` | 분틱구분 | Y | 1 |
| `stex_tp` | 거래소구분 | Y | 1 |

**응답**

| 필드 | 한글명 | 길이 |
|---|---|---:|
| `prm_trde_trnsn` (list) | 프로그램매매추이 |  |
| `prm_trde_trnsn[].cntr_tm` | 체결시간 | 20 |
| `prm_trde_trnsn[].dfrt_trde_sel` | 차익거래매도 | 20 |
| `prm_trde_trnsn[].dfrt_trde_buy` | 차익거래매수 | 20 |
| `prm_trde_trnsn[].dfrt_trde_netprps` | 차익거래순매수 | 20 |
| `prm_trde_trnsn[].ndiffpro_trde_sel` | 비차익거래매도 | 20 |
| `prm_trde_trnsn[].ndiffpro_trde_buy` | 비차익거래매수 | 20 |
| `prm_trde_trnsn[].ndiffpro_trde_netprps` | 비차익거래순매수 | 20 |
| `prm_trde_trnsn[].dfrt_trde_sell_qty` | 차익거래매도수량 | 20 |
| `prm_trde_trnsn[].dfrt_trde_buy_qty` | 차익거래매수수량 | 20 |
| `prm_trde_trnsn[].dfrt_trde_netprps_qty` | 차익거래순매수수량 | 20 |
| `prm_trde_trnsn[].ndiffpro_trde_sell_qty` | 비차익거래매도수량 | 20 |
| `prm_trde_trnsn[].ndiffpro_trde_buy_qty` | 비차익거래매수수량 | 20 |
| `prm_trde_trnsn[].ndiffpro_trde_netprps_qty` | 비차익거래순매수수량 | 20 |
| `prm_trde_trnsn[].all_sel` | 전체매도 | 20 |
| `prm_trde_trnsn[].all_buy` | 전체매수 | 20 |
| `prm_trde_trnsn[].all_netprps` | 전체순매수 | 20 |
| `prm_trde_trnsn[].kospi200` | KOSPI200 | 20 |
| `prm_trde_trnsn[].basis` | BASIS | 20 |

<a id="ka90006"></a>

## `ka90006` · `program_arbitrage_balance()` — 프로그램매매차익잔고추이요청

프로그램매매차익잔고추이요청 (Program Arbitrage Balance Trend) · `POST /api/dostk/mrkcond`

```python
api.market.program_arbitrage_balance(date=..., stex_tp=...)
```

**요청**

| 필드 | 한글명 | 필수 | 길이 |
|---|---|:---:|---:|
| `date` | 날짜 | Y | 8 |
| `stex_tp` | 거래소구분 | Y | 1 |

**응답**

| 필드 | 한글명 | 길이 |
|---|---|---:|
| `prm_trde_dfrt_remn_trnsn` (list) | 프로그램매매차익잔고추이 |  |
| `prm_trde_dfrt_remn_trnsn[].dt` | 일자 | 20 |
| `prm_trde_dfrt_remn_trnsn[].buy_dfrt_trde_qty` | 매수차익거래수량 | 20 |
| `prm_trde_dfrt_remn_trnsn[].buy_dfrt_trde_amt` | 매수차익거래금액 | 20 |
| `prm_trde_dfrt_remn_trnsn[].buy_dfrt_trde_irds_amt` | 매수차익거래증감액 | 20 |
| `prm_trde_dfrt_remn_trnsn[].sel_dfrt_trde_qty` | 매도차익거래수량 | 20 |
| `prm_trde_dfrt_remn_trnsn[].sel_dfrt_trde_amt` | 매도차익거래금액 | 20 |
| `prm_trde_dfrt_remn_trnsn[].sel_dfrt_trde_irds_amt` | 매도차익거래증감액 | 20 |

<a id="ka90007"></a>

## `ka90007` · `cumulative_program_trading()` — 프로그램매매누적추이요청

프로그램매매누적추이요청 (Cumulative Program Trading Trend) · `POST /api/dostk/mrkcond`

```python
api.market.cumulative_program_trading(date=..., amt_qty_tp=..., mrkt_tp=..., stex_tp=...)
```

**요청**

| 필드 | 한글명 | 필수 | 길이 |
|---|---|:---:|---:|
| `date` | 날짜 | Y | 8 |
| `amt_qty_tp` | 금액수량구분 | Y | 1 |
| `mrkt_tp` | 시장구분 | Y | 5 |
| `stex_tp` | 거래소구분 | Y | 1 |

**응답**

| 필드 | 한글명 | 길이 |
|---|---|---:|
| `prm_trde_acc_trnsn` (list) | 프로그램매매누적추이 |  |
| `prm_trde_acc_trnsn[].dt` | 일자 | 20 |
| `prm_trde_acc_trnsn[].kospi200` | KOSPI200 | 20 |
| `prm_trde_acc_trnsn[].basis` | BASIS | 20 |
| `prm_trde_acc_trnsn[].dfrt_trde_tdy` | 차익거래당일 | 20 |
| `prm_trde_acc_trnsn[].dfrt_trde_acc` | 차익거래누적 | 20 |
| `prm_trde_acc_trnsn[].ndiffpro_trde_tdy` | 비차익거래당일 | 20 |
| `prm_trde_acc_trnsn[].ndiffpro_trde_acc` | 비차익거래누적 | 20 |
| `prm_trde_acc_trnsn[].all_tdy` | 전체당일 | 20 |
| `prm_trde_acc_trnsn[].all_acc` | 전체누적 | 20 |

<a id="ka90008"></a>

## `ka90008` · `program_trading_by_stock_time()` — 종목시간별프로그램매매추이요청

종목시간별프로그램매매추이요청 (Program Trading by Stock and Time Slot) · `POST /api/dostk/mrkcond`

```python
api.market.program_trading_by_stock_time(amt_qty_tp=..., stk_cd=..., date=...)
```

**요청**

| 필드 | 한글명 | 필수 | 길이 |
|---|---|:---:|---:|
| `amt_qty_tp` | 금액수량구분 | Y | 1 |
| `stk_cd` | 종목코드 | Y | 6 |
| `date` | 날짜 | Y | 8 |

**응답**

| 필드 | 한글명 | 길이 |
|---|---|---:|
| `stk_tm_prm_trde_trnsn` (list) | 종목시간별프로그램매매추이 |  |
| `stk_tm_prm_trde_trnsn[].tm` | 시간 | 20 |
| `stk_tm_prm_trde_trnsn[].cur_prc` | 현재가 | 20 |
| `stk_tm_prm_trde_trnsn[].pre_sig` | 대비기호 | 20 |
| `stk_tm_prm_trde_trnsn[].pred_pre` | 전일대비 | 20 |
| `stk_tm_prm_trde_trnsn[].flu_rt` | 등락율 | 20 |
| `stk_tm_prm_trde_trnsn[].trde_qty` | 거래량 | 20 |
| `stk_tm_prm_trde_trnsn[].prm_sell_amt` | 프로그램매도금액 | 20 |
| `stk_tm_prm_trde_trnsn[].prm_buy_amt` | 프로그램매수금액 | 20 |
| `stk_tm_prm_trde_trnsn[].prm_netprps_amt` | 프로그램순매수금액 | 20 |
| `stk_tm_prm_trde_trnsn[].prm_netprps_amt_irds` | 프로그램순매수금액증감 | 20 |
| `stk_tm_prm_trde_trnsn[].prm_sell_qty` | 프로그램매도수량 | 20 |
| `stk_tm_prm_trde_trnsn[].prm_buy_qty` | 프로그램매수수량 | 20 |
| `stk_tm_prm_trde_trnsn[].prm_netprps_qty` | 프로그램순매수수량 | 20 |
| `stk_tm_prm_trde_trnsn[].prm_netprps_qty_irds` | 프로그램순매수수량증감 | 20 |
| `stk_tm_prm_trde_trnsn[].base_pric_tm` | 기준가시간 | 20 |
| `stk_tm_prm_trde_trnsn[].dbrt_trde_rpy_sum` | 대차거래상환주수합 | 20 |
| `stk_tm_prm_trde_trnsn[].remn_rcvord_sum` | 잔고수주합 | 20 |
| `stk_tm_prm_trde_trnsn[].stex_tp` | 거래소구분 | 20 |

<a id="ka90010"></a>

## `ka90010` · `program_trading_by_date()` — 프로그램매매추이요청 일자별

프로그램매매추이요청 일자별 (Program Trading by Date) · `POST /api/dostk/mrkcond`

```python
api.market.program_trading_by_date(date=..., amt_qty_tp=..., mrkt_tp=..., min_tic_tp=..., stex_tp=...)
```

**요청**

| 필드 | 한글명 | 필수 | 길이 |
|---|---|:---:|---:|
| `date` | 날짜 | Y | 8 |
| `amt_qty_tp` | 금액수량구분 | Y | 1 |
| `mrkt_tp` | 시장구분 | Y | 10 |
| `min_tic_tp` | 분틱구분 | Y | 1 |
| `stex_tp` | 거래소구분 | Y | 1 |

**응답**

| 필드 | 한글명 | 길이 |
|---|---|---:|
| `prm_trde_trnsn` (list) | 프로그램매매추이 |  |
| `prm_trde_trnsn[].cntr_tm` | 체결시간 | 20 |
| `prm_trde_trnsn[].dfrt_trde_sel` | 차익거래매도 | 20 |
| `prm_trde_trnsn[].dfrt_trde_buy` | 차익거래매수 | 20 |
| `prm_trde_trnsn[].dfrt_trde_netprps` | 차익거래순매수 | 20 |
| `prm_trde_trnsn[].ndiffpro_trde_sel` | 비차익거래매도 | 20 |
| `prm_trde_trnsn[].ndiffpro_trde_buy` | 비차익거래매수 | 20 |
| `prm_trde_trnsn[].ndiffpro_trde_netprps` | 비차익거래순매수 | 20 |
| `prm_trde_trnsn[].dfrt_trde_sell_qty` | 차익거래매도수량 | 20 |
| `prm_trde_trnsn[].dfrt_trde_buy_qty` | 차익거래매수수량 | 20 |
| `prm_trde_trnsn[].dfrt_trde_netprps_qty` | 차익거래순매수수량 | 20 |
| `prm_trde_trnsn[].ndiffpro_trde_sell_qty` | 비차익거래매도수량 | 20 |
| `prm_trde_trnsn[].ndiffpro_trde_buy_qty` | 비차익거래매수수량 | 20 |
| `prm_trde_trnsn[].ndiffpro_trde_netprps_qty` | 비차익거래순매수수량 | 20 |
| `prm_trde_trnsn[].all_sel` | 전체매도 | 20 |
| `prm_trde_trnsn[].all_buy` | 전체매수 | 20 |
| `prm_trde_trnsn[].all_netprps` | 전체순매수 | 20 |
| `prm_trde_trnsn[].kospi200` | KOSPI200 | 20 |
| `prm_trde_trnsn[].basis` | BASIS | 20 |

<a id="ka90013"></a>

## `ka90013` · `program_trading_by_stock_day()` — 종목일별프로그램매매추이요청

종목일별프로그램매매추이요청 (Program Trading by Stock and Day) · `POST /api/dostk/mrkcond`

```python
api.market.program_trading_by_stock_day(stk_cd=...)
```

**요청**

| 필드 | 한글명 | 필수 | 길이 |
|---|---|:---:|---:|
| `amt_qty_tp` | 금액수량구분 |  | 1 |
| `stk_cd` | 종목코드 | Y | 20 |
| `date` | 날짜 |  | 8 |

**응답**

| 필드 | 한글명 | 길이 |
|---|---|---:|
| `stk_daly_prm_trde_trnsn` (list) | 종목일별프로그램매매추이 |  |
| `stk_daly_prm_trde_trnsn[].dt` | 일자 | 20 |
| `stk_daly_prm_trde_trnsn[].cur_prc` | 현재가 | 20 |
| `stk_daly_prm_trde_trnsn[].pre_sig` | 대비기호 | 20 |
| `stk_daly_prm_trde_trnsn[].pred_pre` | 전일대비 | 20 |
| `stk_daly_prm_trde_trnsn[].flu_rt` | 등락율 | 20 |
| `stk_daly_prm_trde_trnsn[].trde_qty` | 거래량 | 20 |
| `stk_daly_prm_trde_trnsn[].prm_sell_amt` | 프로그램매도금액 | 20 |
| `stk_daly_prm_trde_trnsn[].prm_buy_amt` | 프로그램매수금액 | 20 |
| `stk_daly_prm_trde_trnsn[].prm_netprps_amt` | 프로그램순매수금액 | 20 |
| `stk_daly_prm_trde_trnsn[].prm_netprps_amt_irds` | 프로그램순매수금액증감 | 20 |
| `stk_daly_prm_trde_trnsn[].prm_sell_qty` | 프로그램매도수량 | 20 |
| `stk_daly_prm_trde_trnsn[].prm_buy_qty` | 프로그램매수수량 | 20 |
| `stk_daly_prm_trde_trnsn[].prm_netprps_qty` | 프로그램순매수수량 | 20 |
| `stk_daly_prm_trde_trnsn[].prm_netprps_qty_irds` | 프로그램순매수수량증감 | 20 |
| `stk_daly_prm_trde_trnsn[].base_pric_tm` | 기준가시간 | 20 |
| `stk_daly_prm_trde_trnsn[].dbrt_trde_rpy_sum` | 대차거래상환주수합 | 20 |
| `stk_daly_prm_trde_trnsn[].remn_rcvord_sum` | 잔고수주합 | 20 |
| `stk_daly_prm_trde_trnsn[].stex_tp` | 거래소구분 | 20 |
