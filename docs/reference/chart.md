<!-- 자동 생성 파일 — 손으로 고치지 마세요. `python scripts/gen_docs.py` 가 TR 카탈로그(kiwoom_client.spec)로 다시 만듭니다. -->

# `api.chart` — 차트 (Chart)

요청·응답 필드는 키움 공식 REST API 명세에서 만든 TR 카탈로그([출처·라이선스](https://github.com/younghwan91/kiwoom-client/blob/main/src/kiwoom_client/spec/SOURCE.md))에서 옮긴 필드 ID·한글명·필수·길이입니다. 필드 설명·코드값은 싣지 않으니 [키움 REST API 포털](https://openapi.kiwoom.com) 문서를 보세요(자주 쓰는 코드값은 `kiwoom_client.codes`). 값은 모두 문자열로 넘깁니다.

공통 헤더(`api-id`·`cont-yn`·`next-key`·`authorization`)는 라이브러리가 채웁니다 — 연속조회는 메서드의 `cont_yn`·`next_key` 인자나 `request_all()` 을 쓰세요.

| api_id | 메서드 | 이름 |
|---|---|---|
| [`ka10060`](#ka10060) | `investor_institution_chart()` | 종목별투자자기관별차트요청 |
| [`ka10064`](#ka10064) | `intraday_investor_chart()` | 장중투자자별매매차트요청 |
| [`ka10079`](#ka10079) | `stock_tick_chart()` | 주식틱차트조회요청 |
| [`ka10080`](#ka10080) | `stock_minute_chart()` | 주식분봉차트조회요청 |
| [`ka10081`](#ka10081) | `stock_daily_chart()` | 주식일봉차트조회요청 |
| [`ka10082`](#ka10082) | `stock_weekly_chart()` | 주식주봉차트조회요청 |
| [`ka10083`](#ka10083) | `stock_monthly_chart()` | 주식월봉차트조회요청 |
| [`ka10094`](#ka10094) | `stock_yearly_chart()` | 주식년봉차트조회요청 |
| [`ka20004`](#ka20004) | `industry_tick_chart()` | 업종틱차트조회요청 |
| [`ka20005`](#ka20005) | `industry_minute_chart()` | 업종분봉조회요청 |
| [`ka20006`](#ka20006) | `industry_daily_chart()` | 업종일봉조회요청 |
| [`ka20007`](#ka20007) | `industry_weekly_chart()` | 업종주봉조회요청 |
| [`ka20008`](#ka20008) | `industry_monthly_chart()` | 업종월봉조회요청 |
| [`ka20019`](#ka20019) | `industry_yearly_chart()` | 업종년봉조회요청 |
| [`ka50079`](#ka50079) | `gold_spot_tick_chart()` | 금현물틱차트조회요청 |
| [`ka50080`](#ka50080) | `gold_spot_minute_chart()` | 금현물분봉차트조회요청 |
| [`ka50081`](#ka50081) | `gold_spot_daily_chart()` | 금현물일봉차트조회요청 |
| [`ka50082`](#ka50082) | `gold_spot_weekly_chart()` | 금현물주봉차트조회요청 |
| [`ka50083`](#ka50083) | `gold_spot_monthly_chart()` | 금현물월봉차트조회요청 |
| [`ka50091`](#ka50091) | `gold_spot_intraday_tick_chart()` | 금현물당일틱차트조회요청 |
| [`ka50092`](#ka50092) | `gold_spot_intraday_minute_chart()` | 금현물당일분봉차트조회요청 |

<a id="ka10060"></a>

## `ka10060` · `investor_institution_chart()` — 종목별투자자기관별차트요청

종목별투자자기관별차트요청 (Investor/Institution Chart by Stock) · `POST /api/dostk/chart`

```python
api.chart.investor_institution_chart(dt=..., stk_cd=..., amt_qty_tp=..., trde_tp=..., unit_tp=...)
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
| `stk_invsr_orgn_chart` (list) | 종목별투자자기관별차트 |  |
| `stk_invsr_orgn_chart[].dt` | 일자 | 20 |
| `stk_invsr_orgn_chart[].cur_prc` | 현재가 | 20 |
| `stk_invsr_orgn_chart[].pred_pre` | 전일대비 | 20 |
| `stk_invsr_orgn_chart[].acc_trde_prica` | 누적거래대금 | 20 |
| `stk_invsr_orgn_chart[].ind_invsr` | 개인투자자 | 20 |
| `stk_invsr_orgn_chart[].frgnr_invsr` | 외국인투자자 | 20 |
| `stk_invsr_orgn_chart[].orgn` | 기관계 | 20 |
| `stk_invsr_orgn_chart[].fnnc_invt` | 금융투자 | 20 |
| `stk_invsr_orgn_chart[].insrnc` | 보험 | 20 |
| `stk_invsr_orgn_chart[].invtrt` | 투신 | 20 |
| `stk_invsr_orgn_chart[].etc_fnnc` | 기타금융 | 20 |
| `stk_invsr_orgn_chart[].bank` | 은행 | 20 |
| `stk_invsr_orgn_chart[].penfnd_etc` | 연기금등 | 20 |
| `stk_invsr_orgn_chart[].samo_fund` | 사모펀드 | 20 |
| `stk_invsr_orgn_chart[].natn` | 국가 | 20 |
| `stk_invsr_orgn_chart[].etc_corp` | 기타법인 | 20 |
| `stk_invsr_orgn_chart[].natfor` | 내외국인 | 20 |

<a id="ka10064"></a>

## `ka10064` · `intraday_investor_chart()` — 장중투자자별매매차트요청

시간대별투자자매매차트요청 (Intraday Investor Trading Chart by Time Slot) · `POST /api/dostk/chart`

```python
api.chart.intraday_investor_chart(mrkt_tp=..., amt_qty_tp=..., trde_tp=..., stk_cd=...)
```

**요청**

| 필드 | 한글명 | 필수 | 길이 |
|---|---|:---:|---:|
| `mrkt_tp` | 시장구분 | Y | 3 |
| `amt_qty_tp` | 금액수량구분 | Y | 1 |
| `trde_tp` | 매매구분 | Y | 1 |
| `stk_cd` | 종목코드 | Y | 20 |

**응답**

| 필드 | 한글명 | 길이 |
|---|---|---:|
| `opmr_invsr_trde_chart` (list) | 장중투자자별매매차트 |  |
| `opmr_invsr_trde_chart[].tm` | 시간 | 20 |
| `opmr_invsr_trde_chart[].frgnr_invsr` | 외국인투자자 | 20 |
| `opmr_invsr_trde_chart[].orgn` | 기관계 | 20 |
| `opmr_invsr_trde_chart[].invtrt` | 투신 | 20 |
| `opmr_invsr_trde_chart[].insrnc` | 보험 | 20 |
| `opmr_invsr_trde_chart[].bank` | 은행 | 20 |
| `opmr_invsr_trde_chart[].penfnd_etc` | 연기금등 | 20 |
| `opmr_invsr_trde_chart[].etc_corp` | 기타법인 | 20 |
| `opmr_invsr_trde_chart[].natn` | 국가 | 20 |

<a id="ka10079"></a>

## `ka10079` · `stock_tick_chart()` — 주식틱차트조회요청

주식틱차트요청 (Stock Tick Chart) · `POST /api/dostk/chart`

```python
api.chart.stock_tick_chart(stk_cd=..., tic_scope=..., upd_stkpc_tp=...)
```

**요청**

| 필드 | 한글명 | 필수 | 길이 |
|---|---|:---:|---:|
| `stk_cd` | 종목코드 | Y | 20 |
| `tic_scope` | 틱범위 | Y | 2 |
| `upd_stkpc_tp` | 수정주가구분 | Y | 1 |

**응답**

| 필드 | 한글명 | 길이 |
|---|---|---:|
| `stk_cd` | 종목코드 | 6 |
| `last_tic_cnt` | 마지막틱갯수 |  |
| `stk_tic_chart_qry` (list) | 주식틱차트조회 |  |
| `stk_tic_chart_qry[].cur_prc` | 현재가 | 20 |
| `stk_tic_chart_qry[].trde_qty` | 거래량 | 20 |
| `stk_tic_chart_qry[].cntr_tm` | 체결시간 | 20 |
| `stk_tic_chart_qry[].open_pric` | 시가 | 20 |
| `stk_tic_chart_qry[].high_pric` | 고가 | 20 |
| `stk_tic_chart_qry[].low_pric` | 저가 | 20 |
| `stk_tic_chart_qry[].pred_pre` | 전일대비 | 20 |
| `stk_tic_chart_qry[].pred_pre_sig` | 전일대비 기호 | 20 |

<a id="ka10080"></a>

## `ka10080` · `stock_minute_chart()` — 주식분봉차트조회요청

주식분봉차트요청 (Stock Minute Chart) · `POST /api/dostk/chart`

```python
api.chart.stock_minute_chart(stk_cd=..., tic_scope=..., upd_stkpc_tp=...)
```

**요청**

| 필드 | 한글명 | 필수 | 길이 |
|---|---|:---:|---:|
| `stk_cd` | 종목코드 | Y | 20 |
| `tic_scope` | 틱범위 | Y | 2 |
| `upd_stkpc_tp` | 수정주가구분 | Y | 1 |
| `base_dt` | 기준일자 |  | 8 |

**응답**

| 필드 | 한글명 | 길이 |
|---|---|---:|
| `stk_cd` | 종목코드 | 6 |
| `stk_min_pole_chart_qry` (list) | 주식분봉차트조회 |  |
| `stk_min_pole_chart_qry[].cur_prc` | 현재가(종가) | 20 |
| `stk_min_pole_chart_qry[].trde_qty` | 거래량 | 20 |
| `stk_min_pole_chart_qry[].cntr_tm` | 체결시간 | 20 |
| `stk_min_pole_chart_qry[].open_pric` | 시가 | 20 |
| `stk_min_pole_chart_qry[].high_pric` | 고가 | 20 |
| `stk_min_pole_chart_qry[].low_pric` | 저가 | 20 |
| `stk_min_pole_chart_qry[].pred_pre` | 전일대비 | 20 |
| `stk_min_pole_chart_qry[].pred_pre_sig` | 전일대비 기호 | 20 |

<a id="ka10081"></a>

## `ka10081` · `stock_daily_chart()` — 주식일봉차트조회요청

주식일봉차트요청 (Stock Daily Chart) · `POST /api/dostk/chart`

```python
api.chart.stock_daily_chart(stk_cd=..., base_dt=..., upd_stkpc_tp=...)
```

**요청**

| 필드 | 한글명 | 필수 | 길이 |
|---|---|:---:|---:|
| `stk_cd` | 종목코드 | Y | 20 |
| `base_dt` | 기준일자 | Y | 8 |
| `upd_stkpc_tp` | 수정주가구분 | Y | 1 |

**응답**

| 필드 | 한글명 | 길이 |
|---|---|---:|
| `stk_cd` | 종목코드 | 6 |
| `stk_dt_pole_chart_qry` (list) | 주식일봉차트조회 |  |
| `stk_dt_pole_chart_qry[].cur_prc` | 현재가 | 20 |
| `stk_dt_pole_chart_qry[].trde_qty` | 거래량 | 20 |
| `stk_dt_pole_chart_qry[].trde_prica` | 거래대금 | 20 |
| `stk_dt_pole_chart_qry[].dt` | 일자 | 20 |
| `stk_dt_pole_chart_qry[].open_pric` | 시가 | 20 |
| `stk_dt_pole_chart_qry[].high_pric` | 고가 | 20 |
| `stk_dt_pole_chart_qry[].low_pric` | 저가 | 20 |
| `stk_dt_pole_chart_qry[].pred_pre` | 전일대비 | 20 |
| `stk_dt_pole_chart_qry[].pred_pre_sig` | 전일대비기호 | 20 |
| `stk_dt_pole_chart_qry[].trde_tern_rt` | 거래회전율 | 20 |

<a id="ka10082"></a>

## `ka10082` · `stock_weekly_chart()` — 주식주봉차트조회요청

주식주봉차트요청 (Stock Weekly Chart) · `POST /api/dostk/chart`

```python
api.chart.stock_weekly_chart(stk_cd=..., base_dt=..., upd_stkpc_tp=...)
```

**요청**

| 필드 | 한글명 | 필수 | 길이 |
|---|---|:---:|---:|
| `stk_cd` | 종목코드 | Y | 20 |
| `base_dt` | 기준일자 | Y | 8 |
| `upd_stkpc_tp` | 수정주가구분 | Y | 1 |

**응답**

| 필드 | 한글명 | 길이 |
|---|---|---:|
| `stk_cd` | 종목코드 | 6 |
| `stk_stk_pole_chart_qry` (list) | 주식주봉차트조회 |  |
| `stk_stk_pole_chart_qry[].cur_prc` | 현재가 | 20 |
| `stk_stk_pole_chart_qry[].trde_qty` | 거래량 | 20 |
| `stk_stk_pole_chart_qry[].trde_prica` | 거래대금 | 20 |
| `stk_stk_pole_chart_qry[].dt` | 일자 | 20 |
| `stk_stk_pole_chart_qry[].open_pric` | 시가 | 20 |
| `stk_stk_pole_chart_qry[].high_pric` | 고가 | 20 |
| `stk_stk_pole_chart_qry[].low_pric` | 저가 | 20 |
| `stk_stk_pole_chart_qry[].pred_pre` | 전일대비 | 20 |
| `stk_stk_pole_chart_qry[].pred_pre_sig` | 전일대비기호 | 20 |
| `stk_stk_pole_chart_qry[].trde_tern_rt` | 거래회전율 | 20 |

<a id="ka10083"></a>

## `ka10083` · `stock_monthly_chart()` — 주식월봉차트조회요청

주식월봉차트요청 (Stock Monthly Chart) · `POST /api/dostk/chart`

```python
api.chart.stock_monthly_chart(stk_cd=..., base_dt=..., upd_stkpc_tp=...)
```

**요청**

| 필드 | 한글명 | 필수 | 길이 |
|---|---|:---:|---:|
| `stk_cd` | 종목코드 | Y | 20 |
| `base_dt` | 기준일자 | Y | 8 |
| `upd_stkpc_tp` | 수정주가구분 | Y | 1 |

**응답**

| 필드 | 한글명 | 길이 |
|---|---|---:|
| `stk_cd` | 종목코드 | 6 |
| `stk_mth_pole_chart_qry` (list) | 주식월봉차트조회 |  |
| `stk_mth_pole_chart_qry[].cur_prc` | 현재가 | 20 |
| `stk_mth_pole_chart_qry[].trde_qty` | 거래량 | 20 |
| `stk_mth_pole_chart_qry[].trde_prica` | 거래대금 | 20 |
| `stk_mth_pole_chart_qry[].dt` | 일자 | 20 |
| `stk_mth_pole_chart_qry[].open_pric` | 시가 | 20 |
| `stk_mth_pole_chart_qry[].high_pric` | 고가 | 20 |
| `stk_mth_pole_chart_qry[].low_pric` | 저가 | 20 |
| `stk_mth_pole_chart_qry[].pred_pre` | 전일대비 | 20 |
| `stk_mth_pole_chart_qry[].pred_pre_sig` | 전일대비기호 | 20 |
| `stk_mth_pole_chart_qry[].trde_tern_rt` | 거래회전율 | 20 |

<a id="ka10094"></a>

## `ka10094` · `stock_yearly_chart()` — 주식년봉차트조회요청

주식년봉차트요청 (Stock Yearly Chart) · `POST /api/dostk/chart`

```python
api.chart.stock_yearly_chart(stk_cd=..., base_dt=..., upd_stkpc_tp=...)
```

**요청**

| 필드 | 한글명 | 필수 | 길이 |
|---|---|:---:|---:|
| `stk_cd` | 종목코드 | Y | 20 |
| `base_dt` | 기준일자 | Y | 8 |
| `upd_stkpc_tp` | 수정주가구분 | Y | 1 |

**응답**

| 필드 | 한글명 | 길이 |
|---|---|---:|
| `stk_cd` | 종목코드 | 6 |
| `stk_yr_pole_chart_qry` (list) | 주식년봉차트조회 |  |
| `stk_yr_pole_chart_qry[].cur_prc` | 현재가 | 20 |
| `stk_yr_pole_chart_qry[].trde_qty` | 거래량 | 20 |
| `stk_yr_pole_chart_qry[].trde_prica` | 거래대금 | 20 |
| `stk_yr_pole_chart_qry[].dt` | 일자 | 20 |
| `stk_yr_pole_chart_qry[].open_pric` | 시가 | 20 |
| `stk_yr_pole_chart_qry[].high_pric` | 고가 | 20 |
| `stk_yr_pole_chart_qry[].low_pric` | 저가 | 20 |

<a id="ka20004"></a>

## `ka20004` · `industry_tick_chart()` — 업종틱차트조회요청

업종틱차트요청 (Industry Tick Chart) · `POST /api/dostk/chart`

```python
api.chart.industry_tick_chart(inds_cd=..., tic_scope=...)
```

**요청**

| 필드 | 한글명 | 필수 | 길이 |
|---|---|:---:|---:|
| `inds_cd` | 업종코드 | Y | 3 |
| `tic_scope` | 틱범위 | Y | 2 |

**응답**

| 필드 | 한글명 | 길이 |
|---|---|---:|
| `inds_cd` | 업종코드 | 20 |
| `inds_tic_chart_qry` (list) | 업종틱차트조회 |  |
| `inds_tic_chart_qry[].cur_prc` | 현재가 | 20 |
| `inds_tic_chart_qry[].trde_qty` | 거래량 | 20 |
| `inds_tic_chart_qry[].cntr_tm` | 체결시간 | 20 |
| `inds_tic_chart_qry[].open_pric` | 시가 | 20 |
| `inds_tic_chart_qry[].high_pric` | 고가 | 20 |
| `inds_tic_chart_qry[].low_pric` | 저가 | 20 |
| `inds_tic_chart_qry[].pred_pre` | 전일대비 | 20 |
| `inds_tic_chart_qry[].pred_pre_sig` | 전일대비 기호 | 20 |

<a id="ka20005"></a>

## `ka20005` · `industry_minute_chart()` — 업종분봉조회요청

업종분봉차트요청 (Industry Minute Chart) · `POST /api/dostk/chart`

```python
api.chart.industry_minute_chart(inds_cd=..., tic_scope=...)
```

**요청**

| 필드 | 한글명 | 필수 | 길이 |
|---|---|:---:|---:|
| `inds_cd` | 업종코드 | Y | 3 |
| `tic_scope` | 틱범위 | Y | 2 |
| `base_dt` | 기준일자 |  | 8 |

**응답**

| 필드 | 한글명 | 길이 |
|---|---|---:|
| `inds_cd` | 업종코드 | 20 |
| `inds_min_pole_qry` (list) | 업종분봉조회 |  |
| `inds_min_pole_qry[].cur_prc` | 현재가 | 20 |
| `inds_min_pole_qry[].trde_qty` | 거래량 | 20 |
| `inds_min_pole_qry[].cntr_tm` | 체결시간 | 20 |
| `inds_min_pole_qry[].open_pric` | 시가 | 20 |
| `inds_min_pole_qry[].high_pric` | 고가 | 20 |
| `inds_min_pole_qry[].low_pric` | 저가 | 20 |
| `inds_min_pole_qry[].acc_trde_qty` | 누적거래량 | 20 |
| `inds_min_pole_qry[].pred_pre` | 전일대비 | 20 |
| `inds_min_pole_qry[].pred_pre_sig` | 전일대비 기호 | 20 |

<a id="ka20006"></a>

## `ka20006` · `industry_daily_chart()` — 업종일봉조회요청

업종일봉차트요청 (Industry Daily Chart) · `POST /api/dostk/chart`

```python
api.chart.industry_daily_chart(inds_cd=..., base_dt=...)
```

**요청**

| 필드 | 한글명 | 필수 | 길이 |
|---|---|:---:|---:|
| `inds_cd` | 업종코드 | Y | 3 |
| `base_dt` | 기준일자 | Y | 8 |

**응답**

| 필드 | 한글명 | 길이 |
|---|---|---:|
| `inds_cd` | 업종코드 | 20 |
| `inds_dt_pole_qry` (list) | 업종일봉조회 |  |
| `inds_dt_pole_qry[].cur_prc` | 현재가 | 20 |
| `inds_dt_pole_qry[].trde_qty` | 거래량 | 20 |
| `inds_dt_pole_qry[].dt` | 일자 | 20 |
| `inds_dt_pole_qry[].open_pric` | 시가 | 20 |
| `inds_dt_pole_qry[].high_pric` | 고가 | 20 |
| `inds_dt_pole_qry[].low_pric` | 저가 | 20 |
| `inds_dt_pole_qry[].trde_prica` | 거래대금 | 20 |

<a id="ka20007"></a>

## `ka20007` · `industry_weekly_chart()` — 업종주봉조회요청

업종주봉차트요청 (Industry Weekly Chart) · `POST /api/dostk/chart`

```python
api.chart.industry_weekly_chart(inds_cd=..., base_dt=...)
```

**요청**

| 필드 | 한글명 | 필수 | 길이 |
|---|---|:---:|---:|
| `inds_cd` | 업종코드 | Y | 8 |
| `base_dt` | 기준일자 | Y | 3 |

**응답**

| 필드 | 한글명 | 길이 |
|---|---|---:|
| `inds_cd` | 업종코드 | 20 |
| `inds_stk_pole_qry` (list) | 업종주봉조회 |  |
| `inds_stk_pole_qry[].cur_prc` | 현재가 | 20 |
| `inds_stk_pole_qry[].trde_qty` | 거래량 | 20 |
| `inds_stk_pole_qry[].dt` | 일자 | 20 |
| `inds_stk_pole_qry[].open_pric` | 시가 | 20 |
| `inds_stk_pole_qry[].high_pric` | 고가 | 20 |
| `inds_stk_pole_qry[].low_pric` | 저가 | 20 |
| `inds_stk_pole_qry[].trde_prica` | 거래대금 | 20 |

<a id="ka20008"></a>

## `ka20008` · `industry_monthly_chart()` — 업종월봉조회요청

업종월봉차트요청 (Industry Monthly Chart) · `POST /api/dostk/chart`

```python
api.chart.industry_monthly_chart(inds_cd=..., base_dt=...)
```

**요청**

| 필드 | 한글명 | 필수 | 길이 |
|---|---|:---:|---:|
| `inds_cd` | 업종코드 | Y | 3 |
| `base_dt` | 기준일자 | Y | 8 |

**응답**

| 필드 | 한글명 | 길이 |
|---|---|---:|
| `inds_cd` | 업종코드 | 20 |
| `inds_mth_pole_qry` (list) | 업종월봉조회 |  |
| `inds_mth_pole_qry[].cur_prc` | 현재가 | 20 |
| `inds_mth_pole_qry[].trde_qty` | 거래량 | 20 |
| `inds_mth_pole_qry[].dt` | 일자 | 20 |
| `inds_mth_pole_qry[].open_pric` | 시가 | 20 |
| `inds_mth_pole_qry[].high_pric` | 고가 | 20 |
| `inds_mth_pole_qry[].low_pric` | 저가 | 20 |
| `inds_mth_pole_qry[].trde_prica` | 거래대금 | 20 |

<a id="ka20019"></a>

## `ka20019` · `industry_yearly_chart()` — 업종년봉조회요청

업종년봉차트요청 (Industry Yearly Chart) · `POST /api/dostk/chart`

```python
api.chart.industry_yearly_chart(inds_cd=..., base_dt=...)
```

**요청**

| 필드 | 한글명 | 필수 | 길이 |
|---|---|:---:|---:|
| `inds_cd` | 업종코드 | Y | 3 |
| `base_dt` | 기준일자 | Y | 8 |

**응답**

| 필드 | 한글명 | 길이 |
|---|---|---:|
| `inds_cd` | 업종코드 | 20 |
| `inds_yr_pole_qry` (list) | 업종년봉조회 |  |
| `inds_yr_pole_qry[].cur_prc` | 현재가 | 20 |
| `inds_yr_pole_qry[].trde_qty` | 거래량 | 20 |
| `inds_yr_pole_qry[].dt` | 일자 | 20 |
| `inds_yr_pole_qry[].open_pric` | 시가 | 20 |
| `inds_yr_pole_qry[].high_pric` | 고가 | 20 |
| `inds_yr_pole_qry[].low_pric` | 저가 | 20 |
| `inds_yr_pole_qry[].trde_prica` | 거래대금 | 20 |

<a id="ka50079"></a>

## `ka50079` · `gold_spot_tick_chart()` — 금현물틱차트조회요청

금현물틱차트조회요청 (Gold Spot Tick Chart) · `POST /api/dostk/chart`

```python
api.chart.gold_spot_tick_chart(stk_cd=..., tic_scope=..., upd_stkpc_tp=...)
```

**요청**

| 필드 | 한글명 | 필수 | 길이 |
|---|---|:---:|---:|
| `stk_cd` | 종목코드 | Y | 20 |
| `tic_scope` | 틱범위 | Y | 2 |
| `upd_stkpc_tp` | 수정주가구분 | Y | 1 |

**응답**

| 필드 | 한글명 | 길이 |
|---|---|---:|
| `gds_tic_chart_qry` (list) | 금현물틱차트조회 |  |
| `gds_tic_chart_qry[].cur_prc` | 현재가 | 20 |
| `gds_tic_chart_qry[].pred_pre` | 전일대비 | 20 |
| `gds_tic_chart_qry[].trde_qty` | 거래량 | 20 |
| `gds_tic_chart_qry[].open_pric` | 시가 | 20 |
| `gds_tic_chart_qry[].high_pric` | 고가 | 20 |
| `gds_tic_chart_qry[].low_pric` | 저가 |  |
| `gds_tic_chart_qry[].cntr_tm` | 체결시간 | 20 |
| `gds_tic_chart_qry[].dt` | 일자 | 20 |
| `gds_tic_chart_qry[].pred_pre_sig` | 전일대비기호 | 20 |

<a id="ka50080"></a>

## `ka50080` · `gold_spot_minute_chart()` — 금현물분봉차트조회요청

금현물분봉차트조회요청 (Gold Spot Minute Chart) · `POST /api/dostk/chart`

```python
api.chart.gold_spot_minute_chart(stk_cd=..., tic_scope=...)
```

**요청**

| 필드 | 한글명 | 필수 | 길이 |
|---|---|:---:|---:|
| `stk_cd` | 종목코드 | Y | 20 |
| `tic_scope` | 틱범위 | Y | 3 |
| `upd_stkpc_tp` | 수정주가구분 |  | 1 |

**응답**

| 필드 | 한글명 | 길이 |
|---|---|---:|
| `gds_min_chart_qry` (list) | 금현물분봉차트조회 |  |
| `gds_min_chart_qry[].cur_prc` | 현재가 | 20 |
| `gds_min_chart_qry[].pred_pre` | 전일대비 | 20 |
| `gds_min_chart_qry[].acc_trde_qty` | 누적거래량 | 20 |
| `gds_min_chart_qry[].trde_qty` | 거래량 | 20 |
| `gds_min_chart_qry[].open_pric` | 시가 | 20 |
| `gds_min_chart_qry[].high_pric` | 고가 | 20 |
| `gds_min_chart_qry[].low_pric` | 저가 | 20 |
| `gds_min_chart_qry[].cntr_tm` | 체결시간 | 20 |
| `gds_min_chart_qry[].dt` | 일자 | 20 |
| `gds_min_chart_qry[].pred_pre_sig` | 전일대비기호 | 20 |

<a id="ka50081"></a>

## `ka50081` · `gold_spot_daily_chart()` — 금현물일봉차트조회요청

금현물일봉차트조회요청 (Gold Spot Daily Chart) · `POST /api/dostk/chart`

```python
api.chart.gold_spot_daily_chart(stk_cd=..., base_dt=..., upd_stkpc_tp=...)
```

**요청**

| 필드 | 한글명 | 필수 | 길이 |
|---|---|:---:|---:|
| `stk_cd` | 종목코드 | Y | 20 |
| `base_dt` | 기준일자 | Y | 8 |
| `upd_stkpc_tp` | 수정주가구분 | Y | 1 |

**응답**

| 필드 | 한글명 | 길이 |
|---|---|---:|
| `gds_day_chart_qry` (list) | 금현물일봉차트조회 |  |
| `gds_day_chart_qry[].cur_prc` | 현재가 | 20 |
| `gds_day_chart_qry[].acc_trde_qty` | 누적 거래량 | 20 |
| `gds_day_chart_qry[].acc_trde_prica` | 누적 거래대금 | 20 |
| `gds_day_chart_qry[].open_pric` | 시가 | 20 |
| `gds_day_chart_qry[].high_pric` | 고가 | 20 |
| `gds_day_chart_qry[].low_pric` | 저가 | 20 |
| `gds_day_chart_qry[].dt` | 일자 | 20 |
| `gds_day_chart_qry[].pred_pre_sig` | 전일대비기호 | 20 |

<a id="ka50082"></a>

## `ka50082` · `gold_spot_weekly_chart()` — 금현물주봉차트조회요청

금현물주봉차트조회요청 (Gold Spot Weekly Chart) · `POST /api/dostk/chart`

```python
api.chart.gold_spot_weekly_chart(stk_cd=..., base_dt=..., upd_stkpc_tp=...)
```

**요청**

| 필드 | 한글명 | 필수 | 길이 |
|---|---|:---:|---:|
| `stk_cd` | 종목코드 | Y | 20 |
| `base_dt` | 기준일자 | Y | 8 |
| `upd_stkpc_tp` | 수정주가구분 | Y | 1 |

**응답**

| 필드 | 한글명 | 길이 |
|---|---|---:|
| `gds_week_chart_qry` (list) | 금현물일봉차트조회 |  |
| `gds_week_chart_qry[].cur_prc` | 현재가 | 20 |
| `gds_week_chart_qry[].acc_trde_qty` | 누적 거래량 | 20 |
| `gds_week_chart_qry[].acc_trde_prica` | 누적 거래대금 | 20 |
| `gds_week_chart_qry[].open_pric` | 시가 | 20 |
| `gds_week_chart_qry[].high_pric` | 고가 | 20 |
| `gds_week_chart_qry[].low_pric` | 저가 | 20 |
| `gds_week_chart_qry[].dt` | 일자 | 20 |

<a id="ka50083"></a>

## `ka50083` · `gold_spot_monthly_chart()` — 금현물월봉차트조회요청

금현물월봉차트조회요청 (Gold Spot Monthly Chart) · `POST /api/dostk/chart`

```python
api.chart.gold_spot_monthly_chart(stk_cd=..., base_dt=..., upd_stkpc_tp=...)
```

**요청**

| 필드 | 한글명 | 필수 | 길이 |
|---|---|:---:|---:|
| `stk_cd` | 종목코드 | Y | 20 |
| `base_dt` | 기준일자 | Y | 8 |
| `upd_stkpc_tp` | 수정주가구분 | Y | 1 |

**응답**

| 필드 | 한글명 | 길이 |
|---|---|---:|
| `gds_month_chart_qry` (list) | 금현물일봉차트조회 |  |
| `gds_month_chart_qry[].cur_prc` | 현재가 | 20 |
| `gds_month_chart_qry[].acc_trde_qty` | 누적 거래량 | 20 |
| `gds_month_chart_qry[].acc_trde_prica` | 누적 거래대금 | 20 |
| `gds_month_chart_qry[].open_pric` | 시가 | 20 |
| `gds_month_chart_qry[].high_pric` | 고가 | 20 |
| `gds_month_chart_qry[].low_pric` | 저가 | 20 |
| `gds_month_chart_qry[].dt` | 일자 | 20 |

<a id="ka50091"></a>

## `ka50091` · `gold_spot_intraday_tick_chart()` — 금현물당일틱차트조회요청

금현물당일틱차트조회요청 (Gold Spot Intraday Tick Chart) · `POST /api/dostk/chart`

```python
api.chart.gold_spot_intraday_tick_chart(stk_cd=..., tic_scope=...)
```

**요청**

| 필드 | 한글명 | 필수 | 길이 |
|---|---|:---:|---:|
| `stk_cd` | 종목코드 | Y | 20 |
| `tic_scope` | 틱범위 | Y | 2 |

**응답**

| 필드 | 한글명 | 길이 |
|---|---|---:|
| `gds_tic_chart_qry` (list) | 금현물일봉차트조회 |  |
| `gds_tic_chart_qry[].cntr_pric` | 체결가 | 20 |
| `gds_tic_chart_qry[].pred_pre` | 전일 대비(원) | 20 |
| `gds_tic_chart_qry[].trde_qty` | 거래량(체결량) | 20 |
| `gds_tic_chart_qry[].open_pric` | 시가 | 20 |
| `gds_tic_chart_qry[].high_pric` | 고가 | 20 |
| `gds_tic_chart_qry[].low_pric` | 저가 | 20 |
| `gds_tic_chart_qry[].cntr_tm` | 체결시간 | 20 |
| `gds_tic_chart_qry[].dt` | 일자 | 20 |
| `gds_tic_chart_qry[].pred_pre_sig` | 전일대비기호 | 20 |

<a id="ka50092"></a>

## `ka50092` · `gold_spot_intraday_minute_chart()` — 금현물당일분봉차트조회요청

금현물당일분봉차트조회요청 (Gold Spot Intraday Minute Chart) · `POST /api/dostk/chart`

```python
api.chart.gold_spot_intraday_minute_chart(stk_cd=..., tic_scope=...)
```

**요청**

| 필드 | 한글명 | 필수 | 길이 |
|---|---|:---:|---:|
| `stk_cd` | 종목코드 | Y | 20 |
| `tic_scope` | 틱범위 | Y | 2 |

**응답**

| 필드 | 한글명 | 길이 |
|---|---|---:|
| `gds_min_chart_qry` (list) | 금현물일봉차트조회 |  |
| `gds_min_chart_qry[].cntr_pric` | 체결가 | 20 |
| `gds_min_chart_qry[].pred_pre` | 전일 대비(원) | 20 |
| `gds_min_chart_qry[].acc_trde_qty` | 누적 거래량 | 20 |
| `gds_min_chart_qry[].acc_trde_prica` | 누적 거래대금 | 20 |
| `gds_min_chart_qry[].trde_qty` | 거래량(체결량) | 20 |
| `gds_min_chart_qry[].open_pric` | 시가 | 20 |
| `gds_min_chart_qry[].high_pric` | 고가 | 20 |
| `gds_min_chart_qry[].low_pric` | 저가 | 20 |
| `gds_min_chart_qry[].cntr_tm` | 체결시간 | 20 |
| `gds_min_chart_qry[].dt` | 일자 | 20 |
| `gds_min_chart_qry[].pred_pre_sig` | 전일대비기호 | 20 |
