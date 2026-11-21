---
seo_title: "키움 REST API 순위정보 TR 요청·응답 필드 — api.ranking"
description: "키움증권 REST API 순위정보 TR 23개(ka10020·ka10021·ka10022 등)의 요청·응답 필드 ID·한글명·필수·길이와 kiwoom-client 파이썬 호출 예."
---

<!-- 자동 생성 파일 — 손으로 고치지 마세요. `python scripts/gen_docs.py` 가 TR 카탈로그(kiwoom_client.spec)로 다시 만듭니다. -->

# `api.ranking` — 순위정보 (Ranking)

요청·응답 필드는 키움 공식 REST API 명세에서 만든 TR 카탈로그([출처·라이선스](https://github.com/younghwan91/kiwoom-client/blob/main/src/kiwoom_client/spec/SOURCE.md))에서 옮긴 필드 ID·한글명·필수·길이입니다. 필드 설명·코드값은 싣지 않으니 [키움 REST API 포털](https://openapi.kiwoom.com) 문서를 보세요(자주 쓰는 코드값은 `kiwoom_client.codes`). 값은 모두 문자열로 넘깁니다.

공통 헤더(`api-id`·`cont-yn`·`next-key`·`authorization`)는 라이브러리가 채웁니다 — 연속조회는 메서드의 `cont_yn`·`next_key` 인자나 `request_all()` 을 쓰세요.

| api_id | 메서드 | 이름 |
|---|---|---|
| [`ka10020`](#ka10020) | `top_order_book_volume()` | 호가잔량상위요청 |
| [`ka10021`](#ka10021) | `sudden_order_book_increase()` | 호가잔량급증요청 |
| [`ka10022`](#ka10022) | `sudden_order_ratio_increase()` | 잔량율급증요청 |
| [`ka10023`](#ka10023) | `sudden_volume_increase()` | 거래량급증요청 |
| [`ka10027`](#ka10027) | `top_change_rate()` | 전일대비등락률상위요청 |
| [`ka10029`](#ka10029) | `top_expected_change_rate()` | 예상체결등락률상위요청 |
| [`ka10030`](#ka10030) | `top_volume_today()` | 당일거래량상위요청 |
| [`ka10031`](#ka10031) | `top_volume_yesterday()` | 전일거래량상위요청 |
| [`ka10032`](#ka10032) | `top_trading_value()` | 거래대금상위요청 |
| [`ka10033`](#ka10033) | `top_credit_ratio()` | 신용비율상위요청 |
| [`ka10034`](#ka10034) | `top_foreign_trades_by_period()` | 외인기간별매매상위요청 |
| [`ka10035`](#ka10035) | `top_foreign_consecutive_buy()` | 외인연속순매매상위요청 |
| [`ka10036`](#ka10036) | `top_foreign_limit_increase()` | 외인한도소진율증가상위 |
| [`ka10037`](#ka10037) | `top_foreign_broker_trading()` | 외국계창구매매상위요청 |
| [`ka10038`](#ka10038) | `broker_ranking_by_stock()` | 종목별증권사순위요청 |
| [`ka10039`](#ka10039) | `top_broker_by_stock()` | 증권사별매매상위요청 |
| [`ka10040`](#ka10040) | `main_brokers_today()` | 당일주요거래원요청 |
| [`ka10042`](#ka10042) | `top_net_buying_brokers()` | 순매수거래원순위요청 |
| [`ka10053`](#ka10053) | `departed_brokers_today()` | 당일상위이탈원요청 |
| [`ka10062`](#ka10062) | `same_day_net_buying_rank()` | 동일순매매순위요청 |
| [`ka10065`](#ka10065) | `top_intraday_investor_trading()` | 장중투자자별매매상위요청 |
| [`ka10098`](#ka10098) | `after_hours_change_rate_rank()` | 시간외단일가등락율순위요청 |
| [`ka90009`](#ka90009) | `top_foreign_institution_trades()` | 외국인기관매매상위요청 |

<a id="ka10020"></a>

## `ka10020` · `top_order_book_volume()` — 호가잔량상위요청

호가잔량상위요청 (Top Order Book Volume) · `POST /api/dostk/rkinfo`

```python
api.ranking.top_order_book_volume(mrkt_tp=..., sort_tp=..., trde_qty_tp=..., stk_cnd=..., crd_cnd=..., stex_tp=...)
```

**요청**

| 필드 | 한글명 | 필수 | 길이 |
|---|---|:---:|---:|
| `mrkt_tp` | 시장구분 | Y | 3 |
| `sort_tp` | 정렬구분 | Y | 1 |
| `trde_qty_tp` | 거래량구분 | Y | 4 |
| `stk_cnd` | 종목조건 | Y | 1 |
| `crd_cnd` | 신용조건 | Y | 1 |
| `stex_tp` | 거래소구분 | Y | 1 |

**응답**

| 필드 | 한글명 | 길이 |
|---|---|---:|
| `bid_req_upper` (list) | 호가잔량상위 |  |
| `bid_req_upper[].stk_cd` | 종목코드 | 20 |
| `bid_req_upper[].stk_nm` | 종목명 | 40 |
| `bid_req_upper[].cur_prc` | 현재가 | 20 |
| `bid_req_upper[].pred_pre_sig` | 전일대비기호 | 20 |
| `bid_req_upper[].pred_pre` | 전일대비 | 20 |
| `bid_req_upper[].trde_qty` | 거래량 | 20 |
| `bid_req_upper[].tot_sel_req` | 총매도잔량 | 20 |
| `bid_req_upper[].tot_buy_req` | 총매수잔량 | 20 |
| `bid_req_upper[].netprps_req` | 순매수잔량 | 20 |
| `bid_req_upper[].buy_rt` | 매수비율 | 20 |

<a id="ka10021"></a>

## `ka10021` · `sudden_order_book_increase()` — 호가잔량급증요청

호가잔량급증요청 (Sudden Order Book Increase) · `POST /api/dostk/rkinfo`

```python
api.ranking.sudden_order_book_increase(mrkt_tp=..., trde_tp=..., sort_tp=..., tm_tp=..., trde_qty_tp=..., stk_cnd=..., stex_tp=...)
```

**요청**

| 필드 | 한글명 | 필수 | 길이 |
|---|---|:---:|---:|
| `mrkt_tp` | 시장구분 | Y | 3 |
| `trde_tp` | 매매구분 | Y | 1 |
| `sort_tp` | 정렬구분 | Y | 1 |
| `tm_tp` | 시간구분 | Y | 2 |
| `trde_qty_tp` | 거래량구분 | Y | 4 |
| `stk_cnd` | 종목조건 | Y | 1 |
| `stex_tp` | 거래소구분 | Y | 1 |

**응답**

| 필드 | 한글명 | 길이 |
|---|---|---:|
| `bid_req_sdnin` (list) | 호가잔량급증 |  |
| `bid_req_sdnin[].stk_cd` | 종목코드 | 20 |
| `bid_req_sdnin[].stk_nm` | 종목명 | 40 |
| `bid_req_sdnin[].cur_prc` | 현재가 | 20 |
| `bid_req_sdnin[].pred_pre_sig` | 전일대비기호 | 20 |
| `bid_req_sdnin[].pred_pre` | 전일대비 | 20 |
| `bid_req_sdnin[].int` | 기준량 | 20 |
| `bid_req_sdnin[].now` | 현재 | 20 |
| `bid_req_sdnin[].sdnin_qty` | 급증수량 | 20 |
| `bid_req_sdnin[].sdnin_rt` | 급증률 | 20 |
| `bid_req_sdnin[].tot_buy_qty` | 총매수량 | 20 |

<a id="ka10022"></a>

## `ka10022` · `sudden_order_ratio_increase()` — 잔량율급증요청

잔량율급증요청 (Sudden Order Ratio Increase) · `POST /api/dostk/rkinfo`

```python
api.ranking.sudden_order_ratio_increase(mrkt_tp=..., rt_tp=..., tm_tp=..., trde_qty_tp=..., stk_cnd=..., stex_tp=...)
```

**요청**

| 필드 | 한글명 | 필수 | 길이 |
|---|---|:---:|---:|
| `mrkt_tp` | 시장구분 | Y | 3 |
| `rt_tp` | 비율구분 | Y | 1 |
| `tm_tp` | 시간구분 | Y | 2 |
| `trde_qty_tp` | 거래량구분 | Y | 1 |
| `stk_cnd` | 종목조건 | Y | 1 |
| `stex_tp` | 거래소구분 | Y | 1 |

**응답**

| 필드 | 한글명 | 길이 |
|---|---|---:|
| `req_rt_sdnin` (list) | 잔량율급증 |  |
| `req_rt_sdnin[].stk_cd` | 종목코드 | 20 |
| `req_rt_sdnin[].stk_nm` | 종목명 | 40 |
| `req_rt_sdnin[].cur_prc` | 현재가 | 20 |
| `req_rt_sdnin[].pred_pre_sig` | 전일대비기호 | 20 |
| `req_rt_sdnin[].pred_pre` | 전일대비 | 20 |
| `req_rt_sdnin[].int` | 기준률 | 20 |
| `req_rt_sdnin[].now_rt` | 현재비율 | 20 |
| `req_rt_sdnin[].sdnin_rt` | 급증률 | 20 |
| `req_rt_sdnin[].tot_sel_req` | 총매도잔량 | 20 |
| `req_rt_sdnin[].tot_buy_req` | 총매수잔량 | 20 |

<a id="ka10023"></a>

## `ka10023` · `sudden_volume_increase()` — 거래량급증요청

거래량급증요청 (Sudden Volume Increase) · `POST /api/dostk/rkinfo`

```python
api.ranking.sudden_volume_increase(mrkt_tp=..., sort_tp=..., tm_tp=..., trde_qty_tp=..., stk_cnd=..., pric_tp=..., stex_tp=...)
```

**요청**

| 필드 | 한글명 | 필수 | 길이 |
|---|---|:---:|---:|
| `mrkt_tp` | 시장구분 | Y | 3 |
| `sort_tp` | 정렬구분 | Y | 1 |
| `tm_tp` | 시간구분 | Y | 1 |
| `trde_qty_tp` | 거래량구분 | Y | 1 |
| `tm` | 시간 |  | 2 |
| `stk_cnd` | 종목조건 | Y | 1 |
| `pric_tp` | 가격구분 | Y | 1 |
| `stex_tp` | 거래소구분 | Y | 1 |

**응답**

| 필드 | 한글명 | 길이 |
|---|---|---:|
| `trde_qty_sdnin` (list) | 거래량급증 |  |
| `trde_qty_sdnin[].stk_cd` | 종목코드 | 20 |
| `trde_qty_sdnin[].stk_nm` | 종목명 | 40 |
| `trde_qty_sdnin[].cur_prc` | 현재가 | 20 |
| `trde_qty_sdnin[].pred_pre_sig` | 전일대비기호 | 20 |
| `trde_qty_sdnin[].pred_pre` | 전일대비 | 20 |
| `trde_qty_sdnin[].flu_rt` | 등락률 | 20 |
| `trde_qty_sdnin[].prev_trde_qty` | 이전거래량 | 20 |
| `trde_qty_sdnin[].now_trde_qty` | 현재거래량 | 20 |
| `trde_qty_sdnin[].sdnin_qty` | 급증량 | 20 |
| `trde_qty_sdnin[].sdnin_rt` | 급증률 | 20 |

<a id="ka10027"></a>

## `ka10027` · `top_change_rate()` — 전일대비등락률상위요청

전일대비등락률상위요청 (Top Change Rate vs Previous Day) · `POST /api/dostk/rkinfo`

```python
api.ranking.top_change_rate(mrkt_tp=..., sort_tp=..., trde_qty_cnd=..., stk_cnd=..., crd_cnd=..., updown_incls=..., pric_cnd=..., trde_prica_cnd=..., stex_tp=...)
```

**요청**

| 필드 | 한글명 | 필수 | 길이 |
|---|---|:---:|---:|
| `mrkt_tp` | 시장구분 | Y | 3 |
| `sort_tp` | 정렬구분 | Y | 1 |
| `trde_qty_cnd` | 거래량조건 | Y | 5 |
| `stk_cnd` | 종목조건 | Y | 2 |
| `crd_cnd` | 신용조건 | Y | 1 |
| `updown_incls` | 상하한포함 | Y | 2 |
| `pric_cnd` | 가격조건 | Y | 2 |
| `trde_prica_cnd` | 거래대금조건 | Y | 4 |
| `stex_tp` | 거래소구분 | Y | 1 |

**응답**

| 필드 | 한글명 | 길이 |
|---|---|---:|
| `pred_pre_flu_rt_upper` (list) | 전일대비등락률상위 |  |
| `pred_pre_flu_rt_upper[].stk_cls` | 종목분류 | 20 |
| `pred_pre_flu_rt_upper[].stk_cd` | 종목코드 | 20 |
| `pred_pre_flu_rt_upper[].stk_nm` | 종목명 | 40 |
| `pred_pre_flu_rt_upper[].cur_prc` | 현재가 | 20 |
| `pred_pre_flu_rt_upper[].pred_pre_sig` | 전일대비기호 | 20 |
| `pred_pre_flu_rt_upper[].pred_pre` | 전일대비 | 20 |
| `pred_pre_flu_rt_upper[].flu_rt` | 등락률 | 20 |
| `pred_pre_flu_rt_upper[].sel_req` | 매도잔량 | 20 |
| `pred_pre_flu_rt_upper[].buy_req` | 매수잔량 | 20 |
| `pred_pre_flu_rt_upper[].now_trde_qty` | 현재거래량 | 20 |
| `pred_pre_flu_rt_upper[].cntr_str` | 체결강도 | 20 |
| `pred_pre_flu_rt_upper[].cnt` | 횟수 | 20 |

<a id="ka10029"></a>

## `ka10029` · `top_expected_change_rate()` — 예상체결등락률상위요청

예상체결등락률상위요청 (Top Expected Execution Change Rate) · `POST /api/dostk/rkinfo`

```python
api.ranking.top_expected_change_rate(mrkt_tp=..., sort_tp=..., trde_qty_cnd=..., stk_cnd=..., crd_cnd=..., pric_cnd=..., stex_tp=...)
```

**요청**

| 필드 | 한글명 | 필수 | 길이 |
|---|---|:---:|---:|
| `mrkt_tp` | 시장구분 | Y | 3 |
| `sort_tp` | 정렬구분 | Y | 1 |
| `trde_qty_cnd` | 거래량조건 | Y | 5 |
| `stk_cnd` | 종목조건 | Y | 2 |
| `crd_cnd` | 신용조건 | Y | 1 |
| `pric_cnd` | 가격조건 | Y | 2 |
| `stex_tp` | 거래소구분 | Y | 1 |

**응답**

| 필드 | 한글명 | 길이 |
|---|---|---:|
| `exp_cntr_flu_rt_upper` (list) | 예상체결등락률상위 |  |
| `exp_cntr_flu_rt_upper[].stk_cd` | 종목코드 | 20 |
| `exp_cntr_flu_rt_upper[].stk_nm` | 종목명 | 40 |
| `exp_cntr_flu_rt_upper[].exp_cntr_pric` | 예상체결가 | 20 |
| `exp_cntr_flu_rt_upper[].base_pric` | 기준가 | 20 |
| `exp_cntr_flu_rt_upper[].pred_pre_sig` | 전일대비기호 | 20 |
| `exp_cntr_flu_rt_upper[].pred_pre` | 전일대비 | 20 |
| `exp_cntr_flu_rt_upper[].flu_rt` | 등락률 | 20 |
| `exp_cntr_flu_rt_upper[].exp_cntr_qty` | 예상체결량 | 20 |
| `exp_cntr_flu_rt_upper[].sel_req` | 매도잔량 | 20 |
| `exp_cntr_flu_rt_upper[].sel_bid` | 매도호가 | 20 |
| `exp_cntr_flu_rt_upper[].buy_bid` | 매수호가 | 20 |
| `exp_cntr_flu_rt_upper[].buy_req` | 매수잔량 | 20 |

<a id="ka10030"></a>

## `ka10030` · `top_volume_today()` — 당일거래량상위요청

당일거래량상위요청 (Top Volume Today) · `POST /api/dostk/rkinfo`

```python
api.ranking.top_volume_today(mrkt_tp=..., sort_tp=..., mang_stk_incls=..., crd_tp=..., trde_qty_tp=..., pric_tp=..., trde_prica_tp=..., mrkt_open_tp=..., stex_tp=...)
```

**요청**

| 필드 | 한글명 | 필수 | 길이 |
|---|---|:---:|---:|
| `mrkt_tp` | 시장구분 | Y | 3 |
| `sort_tp` | 정렬구분 | Y | 1 |
| `mang_stk_incls` | 관리종목포함 | Y | 1 |
| `crd_tp` | 신용구분 | Y | 1 |
| `trde_qty_tp` | 거래량구분 | Y | 1 |
| `pric_tp` | 가격구분 | Y | 1 |
| `trde_prica_tp` | 거래대금구분 | Y | 1 |
| `mrkt_open_tp` | 장운영구분 | Y | 1 |
| `stex_tp` | 거래소구분 | Y | 1 |

**응답**

| 필드 | 한글명 | 길이 |
|---|---|---:|
| `tdy_trde_qty_upper` (list) | 당일거래량상위 |  |
| `tdy_trde_qty_upper[].stk_cd` | 종목코드 | 20 |
| `tdy_trde_qty_upper[].stk_nm` | 종목명 | 40 |
| `tdy_trde_qty_upper[].cur_prc` | 현재가 | 20 |
| `tdy_trde_qty_upper[].pred_pre_sig` | 전일대비기호 | 20 |
| `tdy_trde_qty_upper[].pred_pre` | 전일대비 | 20 |
| `tdy_trde_qty_upper[].flu_rt` | 등락률 | 20 |
| `tdy_trde_qty_upper[].trde_qty` | 거래량 | 20 |
| `tdy_trde_qty_upper[].pred_rt` | 전일비 | 20 |
| `tdy_trde_qty_upper[].trde_tern_rt` | 거래회전율 | 20 |
| `tdy_trde_qty_upper[].trde_amt` | 거래금액 | 20 |
| `tdy_trde_qty_upper[].opmr_trde_qty` | 장중거래량 | 20 |
| `tdy_trde_qty_upper[].opmr_pred_rt` | 장중전일비 | 20 |
| `tdy_trde_qty_upper[].opmr_trde_rt` | 장중거래회전율 | 20 |
| `tdy_trde_qty_upper[].opmr_trde_amt` | 장중거래금액 | 20 |
| `tdy_trde_qty_upper[].af_mkrt_trde_qty` | 장후거래량 | 20 |
| `tdy_trde_qty_upper[].af_mkrt_pred_rt` | 장후전일비 | 20 |
| `tdy_trde_qty_upper[].af_mkrt_trde_rt` | 장후거래회전율 | 20 |
| `tdy_trde_qty_upper[].af_mkrt_trde_amt` | 장후거래금액 | 20 |
| `tdy_trde_qty_upper[].bf_mkrt_trde_qty` | 장전거래량 | 20 |
| `tdy_trde_qty_upper[].bf_mkrt_pred_rt` | 장전전일비 | 20 |
| `tdy_trde_qty_upper[].bf_mkrt_trde_rt` | 장전거래회전율 | 20 |
| `tdy_trde_qty_upper[].bf_mkrt_trde_amt` | 장전거래금액 | 20 |

<a id="ka10031"></a>

## `ka10031` · `top_volume_yesterday()` — 전일거래량상위요청

전일거래량상위요청 (Top Volume Yesterday) · `POST /api/dostk/rkinfo`

```python
api.ranking.top_volume_yesterday(mrkt_tp=..., qry_tp=..., rank_strt=..., rank_end=..., stex_tp=...)
```

**요청**

| 필드 | 한글명 | 필수 | 길이 |
|---|---|:---:|---:|
| `mrkt_tp` | 시장구분 | Y | 3 |
| `qry_tp` | 조회구분 | Y | 1 |
| `rank_strt` | 순위시작 | Y | 3 |
| `rank_end` | 순위끝 | Y | 3 |
| `stex_tp` | 거래소구분 | Y | 1 |

**응답**

| 필드 | 한글명 | 길이 |
|---|---|---:|
| `pred_trde_qty_upper` (list) | 전일거래량상위 |  |
| `pred_trde_qty_upper[].stk_cd` | 종목코드 | 20 |
| `pred_trde_qty_upper[].stk_nm` | 종목명 | 40 |
| `pred_trde_qty_upper[].cur_prc` | 현재가 | 20 |
| `pred_trde_qty_upper[].pred_pre_sig` | 전일대비기호 | 20 |
| `pred_trde_qty_upper[].pred_pre` | 전일대비 | 20 |
| `pred_trde_qty_upper[].trde_qty` | 거래량 | 20 |

<a id="ka10032"></a>

## `ka10032` · `top_trading_value()` — 거래대금상위요청

거래대금상위요청 (Top Trading Value) · `POST /api/dostk/rkinfo`

```python
api.ranking.top_trading_value(mrkt_tp=..., mang_stk_incls=..., stex_tp=...)
```

**요청**

| 필드 | 한글명 | 필수 | 길이 |
|---|---|:---:|---:|
| `mrkt_tp` | 시장구분 | Y | 3 |
| `mang_stk_incls` | 관리종목포함 | Y | 1 |
| `stex_tp` | 거래소구분 | Y | 1 |

**응답**

| 필드 | 한글명 | 길이 |
|---|---|---:|
| `trde_prica_upper` (list) | 거래대금상위 |  |
| `trde_prica_upper[].stk_cd` | 종목코드 | 20 |
| `trde_prica_upper[].now_rank` | 현재순위 | 20 |
| `trde_prica_upper[].pred_rank` | 전일순위 | 20 |
| `trde_prica_upper[].stk_nm` | 종목명 | 40 |
| `trde_prica_upper[].cur_prc` | 현재가 | 20 |
| `trde_prica_upper[].pred_pre_sig` | 전일대비기호 | 20 |
| `trde_prica_upper[].pred_pre` | 전일대비 | 20 |
| `trde_prica_upper[].flu_rt` | 등락률 | 20 |
| `trde_prica_upper[].sel_bid` | 매도호가 | 20 |
| `trde_prica_upper[].buy_bid` | 매수호가 | 20 |
| `trde_prica_upper[].now_trde_qty` | 현재거래량 | 20 |
| `trde_prica_upper[].pred_trde_qty` | 전일거래량 | 20 |
| `trde_prica_upper[].trde_prica` | 거래대금 | 20 |

<a id="ka10033"></a>

## `ka10033` · `top_credit_ratio()` — 신용비율상위요청

신용비율상위요청 (Top Credit Ratio) · `POST /api/dostk/rkinfo`

```python
api.ranking.top_credit_ratio(mrkt_tp=..., trde_qty_tp=..., stk_cnd=..., updown_incls=..., crd_cnd=..., stex_tp=...)
```

**요청**

| 필드 | 한글명 | 필수 | 길이 |
|---|---|:---:|---:|
| `mrkt_tp` | 시장구분 | Y | 3 |
| `trde_qty_tp` | 거래량구분 | Y | 3 |
| `stk_cnd` | 종목조건 | Y | 1 |
| `updown_incls` | 상하한포함 | Y | 1 |
| `crd_cnd` | 신용조건 | Y | 1 |
| `stex_tp` | 거래소구분 | Y | 1 |

**응답**

| 필드 | 한글명 | 길이 |
|---|---|---:|
| `crd_rt_upper` (list) | 신용비율상위 |  |
| `crd_rt_upper[].stk_infr` | 종목정보 | 20 |
| `crd_rt_upper[].stk_cd` | 종목코드 | 20 |
| `crd_rt_upper[].stk_nm` | 종목명 | 40 |
| `crd_rt_upper[].cur_prc` | 현재가 | 20 |
| `crd_rt_upper[].pred_pre_sig` | 전일대비기호 | 20 |
| `crd_rt_upper[].pred_pre` | 전일대비 | 20 |
| `crd_rt_upper[].flu_rt` | 등락률 | 20 |
| `crd_rt_upper[].crd_rt` | 신용비율 | 20 |
| `crd_rt_upper[].sel_req` | 매도잔량 | 20 |
| `crd_rt_upper[].buy_req` | 매수잔량 | 20 |
| `crd_rt_upper[].now_trde_qty` | 현재거래량 | 20 |

<a id="ka10034"></a>

## `ka10034` · `top_foreign_trades_by_period()` — 외인기간별매매상위요청

외인기간별매매상위요청 (Top Foreign Trades by Period) · `POST /api/dostk/rkinfo`

```python
api.ranking.top_foreign_trades_by_period(mrkt_tp=..., trde_tp=..., dt=..., stex_tp=...)
```

**요청**

| 필드 | 한글명 | 필수 | 길이 |
|---|---|:---:|---:|
| `mrkt_tp` | 시장구분 | Y | 3 |
| `trde_tp` | 매매구분 | Y | 1 |
| `dt` | 기간 | Y | 2 |
| `stex_tp` | 거래소구분 | Y | 1 |

**응답**

| 필드 | 한글명 | 길이 |
|---|---|---:|
| `for_dt_trde_upper` (list) | 외인기간별매매상위 |  |
| `for_dt_trde_upper[].rank` | 순위 | 20 |
| `for_dt_trde_upper[].stk_cd` | 종목코드 | 20 |
| `for_dt_trde_upper[].stk_nm` | 종목명 | 40 |
| `for_dt_trde_upper[].cur_prc` | 현재가 | 20 |
| `for_dt_trde_upper[].pred_pre_sig` | 전일대비기호 | 20 |
| `for_dt_trde_upper[].pred_pre` | 전일대비 | 20 |
| `for_dt_trde_upper[].sel_bid` | 매도호가 | 20 |
| `for_dt_trde_upper[].buy_bid` | 매수호가 | 20 |
| `for_dt_trde_upper[].trde_qty` | 거래량 | 20 |
| `for_dt_trde_upper[].netprps_qty` | 순매수량 | 20 |
| `for_dt_trde_upper[].gain_pos_stkcnt` | 취득가능주식수 | 20 |

<a id="ka10035"></a>

## `ka10035` · `top_foreign_consecutive_buy()` — 외인연속순매매상위요청

외인연속순매매상위요청 (Top Foreign Consecutive Net Buy) · `POST /api/dostk/rkinfo`

```python
api.ranking.top_foreign_consecutive_buy(mrkt_tp=..., trde_tp=..., base_dt_tp=..., stex_tp=...)
```

**요청**

| 필드 | 한글명 | 필수 | 길이 |
|---|---|:---:|---:|
| `mrkt_tp` | 시장구분 | Y | 3 |
| `trde_tp` | 매매구분 | Y | 1 |
| `base_dt_tp` | 기준일구분 | Y | 1 |
| `stex_tp` | 거래소구분 | Y | 1 |

**응답**

| 필드 | 한글명 | 길이 |
|---|---|---:|
| `for_cont_nettrde_upper` (list) | 외인연속순매매상위 |  |
| `for_cont_nettrde_upper[].stk_cd` | 종목코드 | 20 |
| `for_cont_nettrde_upper[].stk_nm` | 종목명 | 40 |
| `for_cont_nettrde_upper[].cur_prc` | 현재가 | 20 |
| `for_cont_nettrde_upper[].pred_pre_sig` | 전일대비기호 | 20 |
| `for_cont_nettrde_upper[].pred_pre` | 전일대비 | 20 |
| `for_cont_nettrde_upper[].dm1` | D-1 | 20 |
| `for_cont_nettrde_upper[].dm2` | D-2 | 20 |
| `for_cont_nettrde_upper[].dm3` | D-3 | 20 |
| `for_cont_nettrde_upper[].tot` | 합계 | 20 |
| `for_cont_nettrde_upper[].limit_exh_rt` | 한도소진율 | 20 |
| `for_cont_nettrde_upper[].pred_pre_1` | 전일대비1 | 20 |
| `for_cont_nettrde_upper[].pred_pre_2` | 전일대비2 | 20 |
| `for_cont_nettrde_upper[].pred_pre_3` | 전일대비3 | 20 |

<a id="ka10036"></a>

## `ka10036` · `top_foreign_limit_increase()` — 외인한도소진율증가상위

외인한도소진율증가상위 (Top Foreign Limit Exhaustion Rate Increase) · `POST /api/dostk/rkinfo`

```python
api.ranking.top_foreign_limit_increase(mrkt_tp=..., dt=..., stex_tp=...)
```

**요청**

| 필드 | 한글명 | 필수 | 길이 |
|---|---|:---:|---:|
| `mrkt_tp` | 시장구분 | Y | 3 |
| `dt` | 기간 | Y | 2 |
| `stex_tp` | 거래소구분 | Y | 1 |

**응답**

| 필드 | 한글명 | 길이 |
|---|---|---:|
| `for_limit_exh_rt_incrs_upper` (list) | 외인한도소진율증가상위 |  |
| `for_limit_exh_rt_incrs_upper[].rank` | 순위 | 20 |
| `for_limit_exh_rt_incrs_upper[].stk_cd` | 종목코드 | 20 |
| `for_limit_exh_rt_incrs_upper[].stk_nm` | 종목명 | 40 |
| `for_limit_exh_rt_incrs_upper[].cur_prc` | 현재가 | 20 |
| `for_limit_exh_rt_incrs_upper[].pred_pre_sig` | 전일대비기호 | 20 |
| `for_limit_exh_rt_incrs_upper[].pred_pre` | 전일대비 | 20 |
| `for_limit_exh_rt_incrs_upper[].trde_qty` | 거래량 | 20 |
| `for_limit_exh_rt_incrs_upper[].poss_stkcnt` | 보유주식수 | 20 |
| `for_limit_exh_rt_incrs_upper[].gain_pos_stkcnt` | 취득가능주식수 | 20 |
| `for_limit_exh_rt_incrs_upper[].base_limit_exh_rt` | 기준한도소진율 | 20 |
| `for_limit_exh_rt_incrs_upper[].limit_exh_rt` | 한도소진율 | 20 |
| `for_limit_exh_rt_incrs_upper[].exh_rt_incrs` | 소진율증가 | 20 |

<a id="ka10037"></a>

## `ka10037` · `top_foreign_broker_trading()` — 외국계창구매매상위요청

외국계창구매매상위요청 (Top Foreign Holding Broker Trading) · `POST /api/dostk/rkinfo`

```python
api.ranking.top_foreign_broker_trading(mrkt_tp=..., dt=..., trde_tp=..., sort_tp=..., stex_tp=...)
```

**요청**

| 필드 | 한글명 | 필수 | 길이 |
|---|---|:---:|---:|
| `mrkt_tp` | 시장구분 | Y | 3 |
| `dt` | 기간 | Y | 2 |
| `trde_tp` | 매매구분 | Y | 1 |
| `sort_tp` | 정렬구분 | Y | 1 |
| `stex_tp` | 거래소구분 | Y | 1 |

**응답**

| 필드 | 한글명 | 길이 |
|---|---|---:|
| `frgn_wicket_trde_upper` (list) | 외국계창구매매상위 |  |
| `frgn_wicket_trde_upper[].rank` | 순위 | 20 |
| `frgn_wicket_trde_upper[].stk_cd` | 종목코드 | 20 |
| `frgn_wicket_trde_upper[].stk_nm` | 종목명 | 40 |
| `frgn_wicket_trde_upper[].cur_prc` | 현재가 | 20 |
| `frgn_wicket_trde_upper[].pred_pre_sig` | 전일대비기호 | 20 |
| `frgn_wicket_trde_upper[].pred_pre` | 전일대비 | 20 |
| `frgn_wicket_trde_upper[].flu_rt` | 등락율 | 20 |
| `frgn_wicket_trde_upper[].sel_trde_qty` | 매도거래량 | 20 |
| `frgn_wicket_trde_upper[].buy_trde_qty` | 매수거래량 | 20 |
| `frgn_wicket_trde_upper[].netprps_trde_qty` | 순매수거래량 | 20 |
| `frgn_wicket_trde_upper[].netprps_prica` | 순매수대금 | 20 |
| `frgn_wicket_trde_upper[].trde_qty` | 거래량 | 20 |
| `frgn_wicket_trde_upper[].trde_prica` | 거래대금 | 20 |

<a id="ka10038"></a>

## `ka10038` · `broker_ranking_by_stock()` — 종목별증권사순위요청

종목별증권사순위요청 (Broker Ranking by Stock) · `POST /api/dostk/rkinfo`

```python
api.ranking.broker_ranking_by_stock(stk_cd=..., qry_tp=...)
```

**요청**

| 필드 | 한글명 | 필수 | 길이 |
|---|---|:---:|---:|
| `stk_cd` | 종목코드 | Y | 6 |
| `strt_dt` | 시작일자 |  | 8 |
| `end_dt` | 종료일자 |  | 8 |
| `qry_tp` | 조회구분 | Y | 1 |
| `dt` | 기간 |  | 2 |

**응답**

| 필드 | 한글명 | 길이 |
|---|---|---:|
| `rank_1` | 기간별 누적 매수량 | 20 |
| `rank_2` | 기간별 누적 매도량 | 20 |
| `rank_3` | 기간별 누적 순매수 | 20 |
| `prid_trde_qty` | 기간중거래량 | 20 |
| `stk_sec_rank` (list) | 종목별증권사순위 |  |
| `stk_sec_rank[].rank` | 순위 | 20 |
| `stk_sec_rank[].mmcm_nm` | 회원사명 | 20 |
| `stk_sec_rank[].buy_qty` | 매수수량 | 20 |
| `stk_sec_rank[].sell_qty` | 매도수량 | 20 |
| `stk_sec_rank[].acc_netprps_qty` | 누적순매수수량 | 20 |

<a id="ka10039"></a>

## `ka10039` · `top_broker_by_stock()` — 증권사별매매상위요청

증권사별매매상위요청 (Top Broker by Stock) · `POST /api/dostk/rkinfo`

```python
api.ranking.top_broker_by_stock(mmcm_cd=..., trde_qty_tp=..., trde_tp=..., dt=..., stex_tp=...)
```

**요청**

| 필드 | 한글명 | 필수 | 길이 |
|---|---|:---:|---:|
| `mmcm_cd` | 회원사코드 | Y | 3 |
| `trde_qty_tp` | 거래량구분 | Y | 4 |
| `trde_tp` | 매매구분 | Y | 2 |
| `dt` | 기간 | Y | 2 |
| `stex_tp` | 거래소구분 | Y | 1 |

**응답**

| 필드 | 한글명 | 길이 |
|---|---|---:|
| `sec_trde_upper` (list) | 증권사별매매상위 |  |
| `sec_trde_upper[].rank` | 순위 | 20 |
| `sec_trde_upper[].stk_cd` | 종목코드 | 20 |
| `sec_trde_upper[].stk_nm` | 종목명 | 40 |
| `sec_trde_upper[].prid_stkpc_flu` | 기간중주가등락 | 20 |
| `sec_trde_upper[].flu_rt` | 등락율 | 20 |
| `sec_trde_upper[].prid_trde_qty` | 기간중거래량 | 20 |
| `sec_trde_upper[].netprps` | 순매수 | 20 |
| `sec_trde_upper[].buy_trde_qty` | 매수거래량 | 20 |
| `sec_trde_upper[].sel_trde_qty` | 매도거래량 | 20 |
| `sec_trde_upper[].netprps_amt` | 순매수금액 | 20 |
| `sec_trde_upper[].buy_amt` | 매수금액 | 20 |
| `sec_trde_upper[].sell_amt` | 매도금액 | 20 |

<a id="ka10040"></a>

## `ka10040` · `main_brokers_today()` — 당일주요거래원요청

당일주요거래원요청 (Main Brokers Today) · `POST /api/dostk/rkinfo`

```python
api.ranking.main_brokers_today(stk_cd=...)
```

**요청**

| 필드 | 한글명 | 필수 | 길이 |
|---|---|:---:|---:|
| `stk_cd` | 종목코드 | Y | 6 |

**응답**

| 필드 | 한글명 | 길이 |
|---|---|---:|
| `sel_trde_ori_irds_1` | 매도거래원별증감1 |  |
| `sel_trde_ori_qty_1` | 매도거래원수량1 |  |
| `sel_trde_ori_1` | 매도거래원1 |  |
| `sel_trde_ori_cd_1` | 매도거래원코드1 |  |
| `buy_trde_ori_1` | 매수거래원1 |  |
| `buy_trde_ori_cd_1` | 매수거래원코드1 |  |
| `buy_trde_ori_qty_1` | 매수거래원수량1 |  |
| `buy_trde_ori_irds_1` | 매수거래원별증감1 |  |
| `sel_trde_ori_irds_2` | 매도거래원별증감2 |  |
| `sel_trde_ori_qty_2` | 매도거래원수량2 |  |
| `sel_trde_ori_2` | 매도거래원2 |  |
| `sel_trde_ori_cd_2` | 매도거래원코드2 |  |
| `buy_trde_ori_2` | 매수거래원2 |  |
| `buy_trde_ori_cd_2` | 매수거래원코드2 |  |
| `buy_trde_ori_qty_2` | 매수거래원수량2 |  |
| `buy_trde_ori_irds_2` | 매수거래원별증감2 |  |
| `sel_trde_ori_irds_3` | 매도거래원별증감3 |  |
| `sel_trde_ori_qty_3` | 매도거래원수량3 |  |
| `sel_trde_ori_3` | 매도거래원3 |  |
| `sel_trde_ori_cd_3` | 매도거래원코드3 |  |
| `buy_trde_ori_3` | 매수거래원3 |  |
| `buy_trde_ori_cd_3` | 매수거래원코드3 |  |
| `buy_trde_ori_qty_3` | 매수거래원수량3 |  |
| `buy_trde_ori_irds_3` | 매수거래원별증감3 |  |
| `sel_trde_ori_irds_4` | 매도거래원별증감4 |  |
| `sel_trde_ori_qty_4` | 매도거래원수량4 |  |
| `sel_trde_ori_4` | 매도거래원4 |  |
| `sel_trde_ori_cd_4` | 매도거래원코드4 |  |
| `buy_trde_ori_4` | 매수거래원4 |  |
| `buy_trde_ori_cd_4` | 매수거래원코드4 |  |
| `buy_trde_ori_qty_4` | 매수거래원수량4 |  |
| `buy_trde_ori_irds_4` | 매수거래원별증감4 |  |
| `sel_trde_ori_irds_5` | 매도거래원별증감5 |  |
| `sel_trde_ori_qty_5` | 매도거래원수량5 |  |
| `sel_trde_ori_5` | 매도거래원5 |  |
| `sel_trde_ori_cd_5` | 매도거래원코드5 |  |
| `buy_trde_ori_5` | 매수거래원5 |  |
| `buy_trde_ori_cd_5` | 매수거래원코드5 |  |
| `buy_trde_ori_qty_5` | 매수거래원수량5 |  |
| `buy_trde_ori_irds_5` | 매수거래원별증감5 |  |
| `frgn_sel_prsm_sum_chang` | 외국계매도추정합변동 |  |
| `frgn_sel_prsm_sum` | 외국계매도추정합 |  |
| `frgn_buy_prsm_sum` | 외국계매수추정합 |  |
| `frgn_buy_prsm_sum_chang` | 외국계매수추정합변동 |  |
| `tdy_main_trde_ori` (list) | 당일주요거래원 |  |
| `tdy_main_trde_ori[].sel_scesn_tm` | 매도이탈시간 | 20 |
| `tdy_main_trde_ori[].sell_qty` | 매도수량 | 20 |
| `tdy_main_trde_ori[].sel_upper_scesn_ori` | 매도상위이탈원 | 20 |
| `tdy_main_trde_ori[].buy_scesn_tm` | 매수이탈시간 | 20 |
| `tdy_main_trde_ori[].buy_qty` | 매수수량 | 20 |
| `tdy_main_trde_ori[].buy_upper_scesn_ori` | 매수상위이탈원 | 20 |
| `tdy_main_trde_ori[].qry_dt` | 조회일자 | 20 |
| `tdy_main_trde_ori[].qry_tm` | 조회시간 | 20 |

<a id="ka10042"></a>

## `ka10042` · `top_net_buying_brokers()` — 순매수거래원순위요청

순매수거래원순위요청 (Top Net Buying Brokers) · `POST /api/dostk/rkinfo`

```python
api.ranking.top_net_buying_brokers(stk_cd=..., qry_dt_tp=..., pot_tp=..., sort_base=...)
```

**요청**

| 필드 | 한글명 | 필수 | 길이 |
|---|---|:---:|---:|
| `stk_cd` | 종목코드 | Y | 6 |
| `strt_dt` | 시작일자 |  | 8 |
| `end_dt` | 종료일자 |  | 8 |
| `qry_dt_tp` | 조회기간구분 | Y | 1 |
| `pot_tp` | 시점구분 | Y | 1 |
| `dt` | 기간 |  | 4 |
| `sort_base` | 정렬기준 | Y | 1 |

**응답**

| 필드 | 한글명 | 길이 |
|---|---|---:|
| `netprps_trde_ori_rank` (list) | 순매수거래원순위 |  |
| `netprps_trde_ori_rank[].rank` | 순위 | 20 |
| `netprps_trde_ori_rank[].mmcm_cd` | 회원사코드 | 20 |
| `netprps_trde_ori_rank[].mmcm_nm` | 회원사명 | 20 |

<a id="ka10053"></a>

## `ka10053` · `departed_brokers_today()` — 당일상위이탈원요청

당일상위이탈원요청 (Departed Brokers Today) · `POST /api/dostk/rkinfo`

```python
api.ranking.departed_brokers_today(stk_cd=...)
```

**요청**

| 필드 | 한글명 | 필수 | 길이 |
|---|---|:---:|---:|
| `stk_cd` | 종목코드 | Y | 6 |

**응답**

| 필드 | 한글명 | 길이 |
|---|---|---:|
| `tdy_upper_scesn_ori` (list) | 당일상위이탈원 |  |
| `tdy_upper_scesn_ori[].sel_scesn_tm` | 매도이탈시간 | 20 |
| `tdy_upper_scesn_ori[].sell_qty` | 매도수량 | 20 |
| `tdy_upper_scesn_ori[].sel_upper_scesn_ori` | 매도상위이탈원 | 20 |
| `tdy_upper_scesn_ori[].buy_scesn_tm` | 매수이탈시간 | 20 |
| `tdy_upper_scesn_ori[].buy_qty` | 매수수량 | 20 |
| `tdy_upper_scesn_ori[].buy_upper_scesn_ori` | 매수상위이탈원 | 20 |
| `tdy_upper_scesn_ori[].qry_dt` | 조회일자 | 20 |
| `tdy_upper_scesn_ori[].qry_tm` | 조회시간 | 20 |

<a id="ka10062"></a>

## `ka10062` · `same_day_net_buying_rank()` — 동일순매매순위요청

동일순매매순위요청 (Same Day Net Buying Rank) · `POST /api/dostk/rkinfo`

```python
api.ranking.same_day_net_buying_rank(strt_dt=..., mrkt_tp=..., trde_tp=..., sort_cnd=..., unit_tp=..., stex_tp=...)
```

**요청**

| 필드 | 한글명 | 필수 | 길이 |
|---|---|:---:|---:|
| `strt_dt` | 시작일자 | Y | 8 |
| `end_dt` | 종료일자 |  | 8 |
| `mrkt_tp` | 시장구분 | Y | 3 |
| `trde_tp` | 매매구분 | Y | 1 |
| `sort_cnd` | 정렬조건 | Y | 1 |
| `unit_tp` | 단위구분 | Y | 1 |
| `stex_tp` | 거래소구분 | Y | 1 |

**응답**

| 필드 | 한글명 | 길이 |
|---|---|---:|
| `eql_nettrde_rank` (list) | 동일순매매순위 |  |
| `eql_nettrde_rank[].stk_cd` | 종목코드 | 20 |
| `eql_nettrde_rank[].rank` | 순위 | 20 |
| `eql_nettrde_rank[].stk_nm` | 종목명 | 40 |
| `eql_nettrde_rank[].cur_prc` | 현재가 | 20 |
| `eql_nettrde_rank[].pre_sig` | 대비기호 | 20 |
| `eql_nettrde_rank[].pred_pre` | 전일대비 | 20 |
| `eql_nettrde_rank[].flu_rt` | 등락율 | 20 |
| `eql_nettrde_rank[].acc_trde_qty` | 누적거래량 | 20 |
| `eql_nettrde_rank[].orgn_nettrde_qty` | 기관순매매수량 | 20 |
| `eql_nettrde_rank[].orgn_nettrde_amt` | 기관순매매금액 | 20 |
| `eql_nettrde_rank[].orgn_nettrde_avg_pric` | 기관순매매평균가 | 20 |
| `eql_nettrde_rank[].for_nettrde_qty` | 외인순매매수량 | 20 |
| `eql_nettrde_rank[].for_nettrde_amt` | 외인순매매금액 | 20 |
| `eql_nettrde_rank[].for_nettrde_avg_pric` | 외인순매매평균가 | 20 |
| `eql_nettrde_rank[].nettrde_qty` | 순매매수량 | 20 |
| `eql_nettrde_rank[].nettrde_amt` | 순매매금액 | 20 |

<a id="ka10065"></a>

## `ka10065` · `top_intraday_investor_trading()` — 장중투자자별매매상위요청

장중투자자별매매상위요청 (Top Intraday Investor Trading by Time) · `POST /api/dostk/rkinfo`

```python
api.ranking.top_intraday_investor_trading(trde_tp=..., mrkt_tp=..., orgn_tp=...)
```

**요청**

| 필드 | 한글명 | 필수 | 길이 |
|---|---|:---:|---:|
| `trde_tp` | 매매구분 | Y | 1 |
| `mrkt_tp` | 시장구분 | Y | 3 |
| `orgn_tp` | 기관구분 | Y | 4 |
| `amt_qty_tp` | 금액수량구분 |  | 1 |

**응답**

| 필드 | 한글명 | 길이 |
|---|---|---:|
| `opmr_invsr_trde_upper` (list) | 장중투자자별매매상위 |  |
| `opmr_invsr_trde_upper[].stk_cd` | 종목코드 | 20 |
| `opmr_invsr_trde_upper[].stk_nm` | 종목명 | 40 |
| `opmr_invsr_trde_upper[].sel_qty` | 매도금액/매도량 | 20 |
| `opmr_invsr_trde_upper[].buy_qty` | 매수금액/매수량 | 20 |
| `opmr_invsr_trde_upper[].netslmt` | 순매수/순매도 | 20 |

<a id="ka10098"></a>

## `ka10098` · `after_hours_change_rate_rank()` — 시간외단일가등락율순위요청

시간외단일가등락율순위요청 (After Hours Change Rate Rank) · `POST /api/dostk/rkinfo`

```python
api.ranking.after_hours_change_rate_rank(mrkt_tp=..., sort_base=..., stk_cnd=..., trde_qty_cnd=..., crd_cnd=..., trde_prica=...)
```

**요청**

| 필드 | 한글명 | 필수 | 길이 |
|---|---|:---:|---:|
| `mrkt_tp` | 시장구분 | Y | 3 |
| `sort_base` | 정렬기준 | Y | 1 |
| `stk_cnd` | 종목조건 | Y | 2 |
| `trde_qty_cnd` | 거래량조건 | Y | 5 |
| `crd_cnd` | 신용조건 | Y | 1 |
| `trde_prica` | 거래대금 | Y | 5 |

**응답**

| 필드 | 한글명 | 길이 |
|---|---|---:|
| `ovt_sigpric_flu_rt_rank` (list) | 시간외단일가등락율순위 |  |
| `ovt_sigpric_flu_rt_rank[].rank` | 순위 | 20 |
| `ovt_sigpric_flu_rt_rank[].stk_cd` | 종목코드 | 20 |
| `ovt_sigpric_flu_rt_rank[].stk_nm` | 종목명 | 40 |
| `ovt_sigpric_flu_rt_rank[].cur_prc` | 현재가 | 20 |
| `ovt_sigpric_flu_rt_rank[].pred_pre_sig` | 전일대비기호 | 20 |
| `ovt_sigpric_flu_rt_rank[].pred_pre` | 전일대비 | 20 |
| `ovt_sigpric_flu_rt_rank[].flu_rt` | 등락률 | 20 |
| `ovt_sigpric_flu_rt_rank[].sel_tot_req` | 매도총잔량 | 20 |
| `ovt_sigpric_flu_rt_rank[].buy_tot_req` | 매수총잔량 | 20 |
| `ovt_sigpric_flu_rt_rank[].acc_trde_qty` | 누적거래량 | 20 |
| `ovt_sigpric_flu_rt_rank[].acc_trde_prica` | 누적거래대금 | 20 |
| `ovt_sigpric_flu_rt_rank[].tdy_close_pric` | 당일종가 | 20 |
| `ovt_sigpric_flu_rt_rank[].tdy_close_pric_flu_rt` | 당일종가등락률 | 20 |

<a id="ka90009"></a>

## `ka90009` · `top_foreign_institution_trades()` — 외국인기관매매상위요청

외국인기관매매상위요청 (Top Foreign Institution Trades) · `POST /api/dostk/rkinfo`

```python
api.ranking.top_foreign_institution_trades(mrkt_tp=..., amt_qty_tp=..., qry_dt_tp=..., stex_tp=...)
```

**요청**

| 필드 | 한글명 | 필수 | 길이 |
|---|---|:---:|---:|
| `mrkt_tp` | 시장구분 | Y | 3 |
| `amt_qty_tp` | 금액수량구분 | Y | 1 |
| `qry_dt_tp` | 조회일자구분 | Y | 1 |
| `date` | 날짜 |  | 8 |
| `stex_tp` | 거래소구분 | Y | 1 |

**응답**

| 필드 | 한글명 | 길이 |
|---|---|---:|
| `frgnr_orgn_trde_upper` (list) | 외국인기관매매상위 |  |
| `frgnr_orgn_trde_upper[].for_netslmt_stk_cd` | 외인순매도종목코드 | 20 |
| `frgnr_orgn_trde_upper[].for_netslmt_stk_nm` | 외인순매도종목명 | 20 |
| `frgnr_orgn_trde_upper[].for_netslmt_amt` | 외인순매도금액 | 20 |
| `frgnr_orgn_trde_upper[].for_netslmt_qty` | 외인순매도수량 | 20 |
| `frgnr_orgn_trde_upper[].for_netprps_stk_cd` | 외인순매수종목코드 | 20 |
| `frgnr_orgn_trde_upper[].for_netprps_stk_nm` | 외인순매수종목명 | 20 |
| `frgnr_orgn_trde_upper[].for_netprps_amt` | 외인순매수금액 | 20 |
| `frgnr_orgn_trde_upper[].for_netprps_qty` | 외인순매수수량 | 20 |
| `frgnr_orgn_trde_upper[].orgn_netslmt_stk_cd` | 기관순매도종목코드 | 20 |
| `frgnr_orgn_trde_upper[].orgn_netslmt_stk_nm` | 기관순매도종목명 | 20 |
| `frgnr_orgn_trde_upper[].orgn_netslmt_amt` | 기관순매도금액 | 20 |
| `frgnr_orgn_trde_upper[].orgn_netslmt_qty` | 기관순매도수량 | 20 |
| `frgnr_orgn_trde_upper[].orgn_netprps_stk_cd` | 기관순매수종목코드 | 20 |
| `frgnr_orgn_trde_upper[].orgn_netprps_stk_nm` | 기관순매수종목명 | 20 |
| `frgnr_orgn_trde_upper[].orgn_netprps_amt` | 기관순매수금액 | 20 |
| `frgnr_orgn_trde_upper[].orgn_netprps_qty` | 기관순매수수량 | 20 |
