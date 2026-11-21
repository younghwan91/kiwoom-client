---
seo_title: "키움 REST API ETF TR 요청·응답 필드 — api.etf"
description: "키움증권 REST API ETF TR 9개(ka40001·ka40002·ka40003 등)의 요청·응답 필드 ID·한글명·필수·길이와 kiwoom-client 파이썬 호출 예."
---

<!-- 자동 생성 파일 — 손으로 고치지 마세요. `python scripts/gen_docs.py` 가 TR 카탈로그(kiwoom_client.spec)로 다시 만듭니다. -->

# `api.etf` — ETF

요청·응답 필드는 키움 공식 REST API 명세에서 만든 TR 카탈로그([출처·라이선스](https://github.com/younghwan91/kiwoom-client/blob/main/src/kiwoom_client/spec/SOURCE.md))에서 옮긴 필드 ID·한글명·필수·길이입니다. 필드 설명·코드값은 싣지 않으니 [키움 REST API 포털](https://openapi.kiwoom.com) 문서를 보세요(자주 쓰는 코드값은 `kiwoom_client.codes`). 값은 모두 문자열로 넘깁니다.

공통 헤더(`api-id`·`cont-yn`·`next-key`·`authorization`)는 라이브러리가 채웁니다 — 연속조회는 메서드의 `cont_yn`·`next_key` 인자나 `request_all()` 을 쓰세요.

| api_id | 메서드 | 이름 |
|---|---|---|
| [`ka40001`](#ka40001) | `return_rate()` | ETF수익율요청 |
| [`ka40002`](#ka40002) | `stock_info()` | ETF종목정보요청 |
| [`ka40003`](#ka40003) | `daily_trend()` | ETF일별추이요청 |
| [`ka40004`](#ka40004) | `overall_market_price()` | ETF전체시세요청 |
| [`ka40006`](#ka40006) | `time_segment_trend()` | ETF시간대별추이요청 |
| [`ka40007`](#ka40007) | `time_segment_execution()` | ETF시간대별체결요청 |
| [`ka40008`](#ka40008) | `daily_execution()` | ETF일자별체결요청 |
| [`ka40009`](#ka40009) | `time_nav()` | ETF시간대별NAV현황 |
| [`ka40010`](#ka40010) | `time_trend()` | ETF시간대별수급현황 |

<a id="ka40001"></a>

## `ka40001` · `return_rate()` — ETF수익율요청

ETF수익률요청 (ETF Return Rate) · `POST /api/dostk/etf`

```python
api.etf.return_rate(stk_cd=..., etfobjt_idex_cd=..., dt=...)
```

**요청**

| 필드 | 한글명 | 필수 | 길이 |
|---|---|:---:|---:|
| `stk_cd` | 종목코드 | Y | 6 |
| `etfobjt_idex_cd` | ETF대상지수코드 | Y | 3 |
| `dt` | 기간 | Y | 1 |

**응답**

| 필드 | 한글명 | 길이 |
|---|---|---:|
| `etfprft_rt_lst` (list) | ETF수익율 |  |
| `etfprft_rt_lst[].etfprft_rt` | ETF수익률 | 20 |
| `etfprft_rt_lst[].cntr_prft_rt` | 체결수익률 | 20 |
| `etfprft_rt_lst[].for_netprps_qty` | 외인순매수수량 | 20 |
| `etfprft_rt_lst[].orgn_netprps_qty` | 기관순매수수량 | 20 |

<a id="ka40002"></a>

## `ka40002` · `stock_info()` — ETF종목정보요청

ETF종목정보요청 (ETF Stock Info) · `POST /api/dostk/etf`

```python
api.etf.stock_info(stk_cd=...)
```

**요청**

| 필드 | 한글명 | 필수 | 길이 |
|---|---|:---:|---:|
| `stk_cd` | 종목코드 | Y | 6 |

**응답**

| 필드 | 한글명 | 길이 |
|---|---|---:|
| `stk_nm` | 종목명 | 40 |
| `etfobjt_idex_nm` | ETF대상지수명 | 20 |
| `wonju_pric` | 원주가격 | 20 |
| `etftxon_type` | ETF과세유형 | 20 |
| `etntxon_type` | ETN과세유형 | 20 |

<a id="ka40003"></a>

## `ka40003` · `daily_trend()` — ETF일별추이요청

ETF일별추이요청 (ETF Daily Trend) · `POST /api/dostk/etf`

```python
api.etf.daily_trend(stk_cd=...)
```

**요청**

| 필드 | 한글명 | 필수 | 길이 |
|---|---|:---:|---:|
| `stk_cd` | 종목코드 | Y | 6 |

**응답**

| 필드 | 한글명 | 길이 |
|---|---|---:|
| `etfdaly_trnsn` (list) | ETF일별추이 |  |
| `etfdaly_trnsn[].cntr_dt` | 체결일자 | 20 |
| `etfdaly_trnsn[].cur_prc` | 현재가 | 20 |
| `etfdaly_trnsn[].pre_sig` | 대비기호 | 20 |
| `etfdaly_trnsn[].pred_pre` | 전일대비 | 20 |
| `etfdaly_trnsn[].pre_rt` | 대비율 | 20 |
| `etfdaly_trnsn[].trde_qty` | 거래량 | 20 |
| `etfdaly_trnsn[].nav` | NAV | 20 |
| `etfdaly_trnsn[].acc_trde_prica` | 누적거래대금 | 20 |
| `etfdaly_trnsn[].navidex_dispty_rt` | NAV/지수괴리율 | 20 |
| `etfdaly_trnsn[].navetfdispty_rt` | NAV/ETF괴리율 | 20 |
| `etfdaly_trnsn[].trace_eor_rt` | 추적오차율 | 20 |
| `etfdaly_trnsn[].trace_cur_prc` | 추적현재가 | 20 |
| `etfdaly_trnsn[].trace_pred_pre` | 추적전일대비 | 20 |
| `etfdaly_trnsn[].trace_pre_sig` | 추적대비기호 | 20 |

<a id="ka40004"></a>

## `ka40004` · `overall_market_price()` — ETF전체시세요청

ETF전체시세요청 (ETF Overall Market Price) · `POST /api/dostk/etf`

```python
api.etf.overall_market_price(txon_type=..., navpre=..., mngmcomp=..., txon_yn=..., trace_idex=..., stex_tp=...)
```

**요청**

| 필드 | 한글명 | 필수 | 길이 |
|---|---|:---:|---:|
| `txon_type` | 과세유형 | Y | 1 |
| `navpre` | NAV대비 | Y | 1 |
| `mngmcomp` | 운용사 | Y | 4 |
| `txon_yn` | 과세여부 | Y | 1 |
| `trace_idex` | 추적지수 | Y | 1 |
| `stex_tp` | 거래소구분 | Y | 1 |

**응답**

| 필드 | 한글명 | 길이 |
|---|---|---:|
| `etfall_mrpr` (list) | ETF전체시세 |  |
| `etfall_mrpr[].stk_cd` | 종목코드 | 20 |
| `etfall_mrpr[].stk_cls` | 종목분류 | 20 |
| `etfall_mrpr[].stk_nm` | 종목명 | 40 |
| `etfall_mrpr[].close_pric` | 종가 | 20 |
| `etfall_mrpr[].pre_sig` | 대비기호 | 20 |
| `etfall_mrpr[].pred_pre` | 전일대비 | 20 |
| `etfall_mrpr[].pre_rt` | 대비율 | 20 |
| `etfall_mrpr[].trde_qty` | 거래량 | 20 |
| `etfall_mrpr[].nav` | NAV | 20 |
| `etfall_mrpr[].trace_eor_rt` | 추적오차율 | 20 |
| `etfall_mrpr[].txbs` | 과표기준 | 20 |
| `etfall_mrpr[].dvid_bf_base` | 배당전기준 | 20 |
| `etfall_mrpr[].pred_dvida` | 전일배당금 | 20 |
| `etfall_mrpr[].trace_idex_nm` | 추적지수명 | 20 |
| `etfall_mrpr[].drng` | 배수 | 20 |
| `etfall_mrpr[].trace_idex_cd` | 추적지수코드 | 20 |
| `etfall_mrpr[].trace_idex` | 추적지수 | 20 |
| `etfall_mrpr[].trace_flu_rt` | 추적등락율 | 20 |

<a id="ka40006"></a>

## `ka40006` · `time_segment_trend()` — ETF시간대별추이요청

ETF시간대별추이요청 (ETF Time Segment Trend) · `POST /api/dostk/etf`

```python
api.etf.time_segment_trend(stk_cd=...)
```

**요청**

| 필드 | 한글명 | 필수 | 길이 |
|---|---|:---:|---:|
| `stk_cd` | 종목코드 | Y | 6 |

**응답**

| 필드 | 한글명 | 길이 |
|---|---|---:|
| `stk_nm` | 종목명 | 40 |
| `etfobjt_idex_nm` | ETF대상지수명 | 20 |
| `wonju_pric` | 원주가격 | 20 |
| `etftxon_type` | ETF과세유형 | 20 |
| `etntxon_type` | ETN과세유형 | 20 |
| `etftisl_trnsn` (list) | ETF시간대별추이 |  |
| `etftisl_trnsn[].tm` | 시간 | 20 |
| `etftisl_trnsn[].close_pric` | 종가 | 20 |
| `etftisl_trnsn[].pre_sig` | 대비기호 | 20 |
| `etftisl_trnsn[].pred_pre` | 전일대비 | 20 |
| `etftisl_trnsn[].flu_rt` | 등락율 | 20 |
| `etftisl_trnsn[].trde_qty` | 거래량 | 20 |
| `etftisl_trnsn[].nav` | NAV | 20 |
| `etftisl_trnsn[].trde_prica` | 거래대금 | 20 |
| `etftisl_trnsn[].navidex` | NAV지수 | 20 |
| `etftisl_trnsn[].navetf` | 괴리율 | 20 |
| `etftisl_trnsn[].trace` | 추적오차율 | 20 |
| `etftisl_trnsn[].trace_idex` | 추적지수 | 20 |
| `etftisl_trnsn[].trace_idex_pred_pre` | 추적지수전일대비 | 20 |
| `etftisl_trnsn[].trace_idex_pred_pre_sig` | 추적지수전일대비기호 | 20 |

<a id="ka40007"></a>

## `ka40007` · `time_segment_execution()` — ETF시간대별체결요청

ETF시간대별체결요청 (ETF Time Segment Execution) · `POST /api/dostk/etf`

```python
api.etf.time_segment_execution(stk_cd=...)
```

**요청**

| 필드 | 한글명 | 필수 | 길이 |
|---|---|:---:|---:|
| `stk_cd` | 종목코드 | Y | 6 |

**응답**

| 필드 | 한글명 | 길이 |
|---|---|---:|
| `stk_cls` | 종목분류 | 20 |
| `stk_nm` | 종목명 | 40 |
| `etfobjt_idex_nm` | ETF대상지수명 | 20 |
| `etfobjt_idex_cd` | ETF대상지수코드 | 20 |
| `objt_idex_pre_rt` | 대상지수대비율 | 20 |
| `wonju_pric` | 원주가격 | 20 |
| `etftisl_cntr_array` (list) | ETF시간대별체결배열 |  |
| `etftisl_cntr_array[].cntr_tm` | 체결시간 | 20 |
| `etftisl_cntr_array[].cur_prc` | 현재가 | 20 |
| `etftisl_cntr_array[].pre_sig` | 대비기호 | 20 |
| `etftisl_cntr_array[].pred_pre` | 전일대비 | 20 |
| `etftisl_cntr_array[].trde_qty` | 거래량 | 20 |
| `etftisl_cntr_array[].stex_tp` | 거래소구분 | 20 |

<a id="ka40008"></a>

## `ka40008` · `daily_execution()` — ETF일자별체결요청

ETF일자별체결요청 (ETF Daily Execution) · `POST /api/dostk/etf`

```python
api.etf.daily_execution(stk_cd=...)
```

**요청**

| 필드 | 한글명 | 필수 | 길이 |
|---|---|:---:|---:|
| `stk_cd` | 종목코드 | Y | 6 |

**응답**

| 필드 | 한글명 | 길이 |
|---|---|---:|
| `cntr_tm` | 체결시간 | 20 |
| `cur_prc` | 현재가 | 20 |
| `pre_sig` | 대비기호 | 20 |
| `pred_pre` | 전일대비 | 20 |
| `trde_qty` | 거래량 | 20 |
| `etfnetprps_qty_array` (list) | ETF순매수수량배열 |  |
| `etfnetprps_qty_array[].dt` | 일자 | 20 |
| `etfnetprps_qty_array[].cur_prc_n` | 현재가n | 20 |
| `etfnetprps_qty_array[].pre_sig_n` | 대비기호n | 20 |
| `etfnetprps_qty_array[].pred_pre_n` | 전일대비n | 20 |
| `etfnetprps_qty_array[].acc_trde_qty` | 누적거래량 | 20 |
| `etfnetprps_qty_array[].for_netprps_qty` | 외인순매수수량 | 20 |
| `etfnetprps_qty_array[].orgn_netprps_qty` | 기관순매수수량 | 20 |

<a id="ka40009"></a>

## `ka40009` · `time_nav()` — ETF시간대별NAV현황

ETF시간대별NAV요청 (ETF Time NAV) · `POST /api/dostk/etf`

```python
api.etf.time_nav(stk_cd=...)
```

**요청**

| 필드 | 한글명 | 필수 | 길이 |
|---|---|:---:|---:|
| `stk_cd` | 종목코드 | Y | 6 |

**응답**

| 필드 | 한글명 | 길이 |
|---|---|---:|
| `etfnavarray` (list) | ETFNAV배열 |  |
| `etfnavarray[].nav` | NAV | 20 |
| `etfnavarray[].navpred_pre` | NAV전일대비 | 20 |
| `etfnavarray[].navflu_rt` | NAV등락율 | 20 |
| `etfnavarray[].trace_eor_rt` | 추적오차율 | 20 |
| `etfnavarray[].dispty_rt` | 괴리율 | 20 |
| `etfnavarray[].stkcnt` | 주식수 | 20 |
| `etfnavarray[].base_pric` | 기준가 | 20 |
| `etfnavarray[].for_rmnd_qty` | 외인보유수량 | 20 |
| `etfnavarray[].repl_pric` | 대용가 | 20 |
| `etfnavarray[].conv_pric` | 환산가격 | 20 |
| `etfnavarray[].drstk` | DR/주 | 20 |
| `etfnavarray[].wonju_pric` | 원주가격 | 20 |

<a id="ka40010"></a>

## `ka40010` · `time_trend()` — ETF시간대별수급현황

ETF시간대별추이요청 (ETF Time Trend) · `POST /api/dostk/etf`

```python
api.etf.time_trend(stk_cd=...)
```

**요청**

| 필드 | 한글명 | 필수 | 길이 |
|---|---|:---:|---:|
| `stk_cd` | 종목코드 | Y | 6 |

**응답**

| 필드 | 한글명 | 길이 |
|---|---|---:|
| `etftisl_trnsn` (list) | ETF시간대별추이 |  |
| `etftisl_trnsn[].cur_prc` | 현재가 | 20 |
| `etftisl_trnsn[].pre_sig` | 대비기호 | 20 |
| `etftisl_trnsn[].pred_pre` | 전일대비 | 20 |
| `etftisl_trnsn[].trde_qty` | 거래량 | 20 |
| `etftisl_trnsn[].for_netprps` | 외인순매수 | 20 |
