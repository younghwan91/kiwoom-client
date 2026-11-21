<!-- 자동 생성 파일 — 손으로 고치지 마세요. `python scripts/gen_docs.py` 가 TR 카탈로그(kiwoom_client.spec)로 다시 만듭니다. -->

# `api.elw` — ELW

요청·응답 필드는 키움 공식 REST API 명세에서 만든 TR 카탈로그([출처·라이선스](https://github.com/younghwan91/kiwoom-client/blob/main/src/kiwoom_client/spec/SOURCE.md))에서 옮긴 필드 ID·한글명·필수·길이입니다. 필드 설명·코드값은 싣지 않으니 [키움 REST API 포털](https://openapi.kiwoom.com) 문서를 보세요(자주 쓰는 코드값은 `kiwoom_client.codes`). 값은 모두 문자열로 넘깁니다.

공통 헤더(`api-id`·`cont-yn`·`next-key`·`authorization`)는 라이브러리가 채웁니다 — 연속조회는 메서드의 `cont_yn`·`next_key` 인자나 `request_all()` 을 쓰세요.

| api_id | 메서드 | 이름 |
|---|---|---|
| [`ka10048`](#ka10048) | `daily_sensitivity_indicator()` | ELW일별민감도지표요청 |
| [`ka10050`](#ka10050) | `sensitivity_indicator()` | ELW민감도지표요청 |
| [`ka30001`](#ka30001) | `price_spike()` | ELW가격급등락요청 |
| [`ka30002`](#ka30002) | `top_net_buying_by_broker()` | 거래원별ELW순매매상위요청 |
| [`ka30003`](#ka30003) | `lp_daily_holding_trend()` | ELWLP보유일별추이요청 |
| [`ka30004`](#ka30004) | `premium_rate()` | ELW괴리율요청 |
| [`ka30005`](#ka30005) | `condition_search()` | ELW조건검색요청 |
| [`ka30009`](#ka30009) | `change_rate_ranking()` | ELW등락율순위요청 |
| [`ka30010`](#ka30010) | `order_volume_ranking()` | ELW잔량순위요청 |
| [`ka30011`](#ka30011) | `proximity_rate()` | ELW근접율요청 |
| [`ka30012`](#ka30012) | `detailed_stock_info()` | ELW종목상세정보요청 |

<a id="ka10048"></a>

## `ka10048` · `daily_sensitivity_indicator()` — ELW일별민감도지표요청

ELW일별민감도지표요청 (ELW Daily Sensitivity Indicator) · `POST /api/dostk/elw`

```python
api.elw.daily_sensitivity_indicator(stk_cd=...)
```

**요청**

| 필드 | 한글명 | 필수 | 길이 |
|---|---|:---:|---:|
| `stk_cd` | 종목코드 | Y | 6 |

**응답**

| 필드 | 한글명 | 길이 |
|---|---|---:|
| `elwdaly_snst_ix` (list) | ELW일별민감도지표 |  |
| `elwdaly_snst_ix[].dt` | 일자 | 20 |
| `elwdaly_snst_ix[].iv` | IV | 20 |
| `elwdaly_snst_ix[].delta` | 델타 | 20 |
| `elwdaly_snst_ix[].gam` | 감마 | 20 |
| `elwdaly_snst_ix[].theta` | 쎄타 | 20 |
| `elwdaly_snst_ix[].vega` | 베가 | 20 |
| `elwdaly_snst_ix[].law` | 로 | 20 |
| `elwdaly_snst_ix[].lp` | LP | 20 |

<a id="ka10050"></a>

## `ka10050` · `sensitivity_indicator()` — ELW민감도지표요청

ELW민감도지표요청 (ELW Sensitivity Indicator) · `POST /api/dostk/elw`

```python
api.elw.sensitivity_indicator(stk_cd=...)
```

**요청**

| 필드 | 한글명 | 필수 | 길이 |
|---|---|:---:|---:|
| `stk_cd` | 종목코드 | Y | 6 |

**응답**

| 필드 | 한글명 | 길이 |
|---|---|---:|
| `elwsnst_ix_array` (list) | ELW민감도지표배열 |  |
| `elwsnst_ix_array[].cntr_tm` | 체결시간 | 20 |
| `elwsnst_ix_array[].cur_prc` | 현재가 | 20 |
| `elwsnst_ix_array[].elwtheory_pric` | ELW이론가 | 20 |
| `elwsnst_ix_array[].iv` | IV | 20 |
| `elwsnst_ix_array[].delta` | 델타 | 20 |
| `elwsnst_ix_array[].gam` | 감마 | 20 |
| `elwsnst_ix_array[].theta` | 쎄타 | 20 |
| `elwsnst_ix_array[].vega` | 베가 | 20 |
| `elwsnst_ix_array[].law` | 로 | 20 |
| `elwsnst_ix_array[].lp` | LP | 20 |

<a id="ka30001"></a>

## `ka30001` · `price_spike()` — ELW가격급등락요청

ELW급등락요청 (ELW Price Spike) · `POST /api/dostk/elw`

```python
api.elw.price_spike(flu_tp=..., tm_tp=..., tm=..., trde_qty_tp=..., isscomp_cd=..., bsis_aset_cd=..., rght_tp=..., lpcd=..., trde_end_elwskip=...)
```

**요청**

| 필드 | 한글명 | 필수 | 길이 |
|---|---|:---:|---:|
| `flu_tp` | 등락구분 | Y | 1 |
| `tm_tp` | 시간구분 | Y | 1 |
| `tm` | 시간 | Y | 2 |
| `trde_qty_tp` | 거래량구분 | Y | 4 |
| `isscomp_cd` | 발행사코드 | Y | 12 |
| `bsis_aset_cd` | 기초자산코드 | Y | 12 |
| `rght_tp` | 권리구분 | Y | 3 |
| `lpcd` | LP코드 | Y | 12 |
| `trde_end_elwskip` | 거래종료ELW제외 | Y | 1 |

**응답**

| 필드 | 한글명 | 길이 |
|---|---|---:|
| `base_pric_tm` | 기준가시간 | 20 |
| `elwpric_jmpflu` (list) | ELW가격급등락 |  |
| `elwpric_jmpflu[].stk_cd` | 종목코드 | 20 |
| `elwpric_jmpflu[].rank` | 순위 | 20 |
| `elwpric_jmpflu[].stk_nm` | 종목명 | 40 |
| `elwpric_jmpflu[].pre_sig` | 대비기호 | 20 |
| `elwpric_jmpflu[].pred_pre` | 전일대비 | 20 |
| `elwpric_jmpflu[].trde_end_elwbase_pric` | 거래종료ELW기준가 | 20 |
| `elwpric_jmpflu[].cur_prc` | 현재가 | 20 |
| `elwpric_jmpflu[].base_pre` | 기준대비 | 20 |
| `elwpric_jmpflu[].trde_qty` | 거래량 | 20 |
| `elwpric_jmpflu[].jmp_rt` | 급등율 | 20 |

<a id="ka30002"></a>

## `ka30002` · `top_net_buying_by_broker()` — 거래원별ELW순매매상위요청

ELW회원사별순매수상위요청 (ELW Top Net Buying by Broker) · `POST /api/dostk/elw`

```python
api.elw.top_net_buying_by_broker(isscomp_cd=..., trde_qty_tp=..., trde_tp=..., dt=..., trde_end_elwskip=...)
```

**요청**

| 필드 | 한글명 | 필수 | 길이 |
|---|---|:---:|---:|
| `isscomp_cd` | 발행사코드 | Y | 3 |
| `trde_qty_tp` | 거래량구분 | Y | 4 |
| `trde_tp` | 매매구분 | Y | 1 |
| `dt` | 기간 | Y | 2 |
| `trde_end_elwskip` | 거래종료ELW제외 | Y | 1 |

**응답**

| 필드 | 한글명 | 길이 |
|---|---|---:|
| `trde_ori_elwnettrde_upper` (list) | 거래원별ELW순매매상위 |  |
| `trde_ori_elwnettrde_upper[].stk_cd` | 종목코드 | 20 |
| `trde_ori_elwnettrde_upper[].stk_nm` | 종목명 | 40 |
| `trde_ori_elwnettrde_upper[].stkpc_flu` | 주가등락 | 20 |
| `trde_ori_elwnettrde_upper[].flu_rt` | 등락율 | 20 |
| `trde_ori_elwnettrde_upper[].trde_qty` | 거래량 | 20 |
| `trde_ori_elwnettrde_upper[].netprps` | 순매수 | 20 |
| `trde_ori_elwnettrde_upper[].buy_trde_qty` | 매수거래량 | 20 |
| `trde_ori_elwnettrde_upper[].sel_trde_qty` | 매도거래량 | 20 |

<a id="ka30003"></a>

## `ka30003` · `lp_daily_holding_trend()` — ELWLP보유일별추이요청

ELW LP일별보유추이요청 (ELW LP Daily Holding Trend) · `POST /api/dostk/elw`

```python
api.elw.lp_daily_holding_trend(bsis_aset_cd=..., base_dt=...)
```

**요청**

| 필드 | 한글명 | 필수 | 길이 |
|---|---|:---:|---:|
| `bsis_aset_cd` | 기초자산코드 | Y | 12 |
| `base_dt` | 기준일자 | Y | 8 |

**응답**

| 필드 | 한글명 | 길이 |
|---|---|---:|
| `elwlpposs_daly_trnsn` (list) | ELWLP보유일별추이 |  |
| `elwlpposs_daly_trnsn[].dt` | 일자 | 20 |
| `elwlpposs_daly_trnsn[].cur_prc` | 현재가 | 20 |
| `elwlpposs_daly_trnsn[].pre_tp` | 대비구분 | 20 |
| `elwlpposs_daly_trnsn[].pred_pre` | 전일대비 | 20 |
| `elwlpposs_daly_trnsn[].flu_rt` | 등락율 | 20 |
| `elwlpposs_daly_trnsn[].trde_qty` | 거래량 | 20 |
| `elwlpposs_daly_trnsn[].trde_prica` | 거래대금 | 20 |
| `elwlpposs_daly_trnsn[].chg_qty` | 변동수량 | 20 |
| `elwlpposs_daly_trnsn[].lprmnd_qty` | LP보유수량 | 20 |
| `elwlpposs_daly_trnsn[].wght` | 비중 | 20 |

<a id="ka30004"></a>

## `ka30004` · `premium_rate()` — ELW괴리율요청

ELW괴리율요청 (ELW Premium Rate) · `POST /api/dostk/elw`

```python
api.elw.premium_rate(isscomp_cd=..., bsis_aset_cd=..., rght_tp=..., lpcd=..., trde_end_elwskip=...)
```

**요청**

| 필드 | 한글명 | 필수 | 길이 |
|---|---|:---:|---:|
| `isscomp_cd` | 발행사코드 | Y | 12 |
| `bsis_aset_cd` | 기초자산코드 | Y | 12 |
| `rght_tp` | 권리구분 | Y | 3 |
| `lpcd` | LP코드 | Y | 12 |
| `trde_end_elwskip` | 거래종료ELW제외 | Y | 1 |

**응답**

| 필드 | 한글명 | 길이 |
|---|---|---:|
| `elwdispty_rt` (list) | ELW괴리율 |  |
| `elwdispty_rt[].stk_cd` | 종목코드 | 20 |
| `elwdispty_rt[].isscomp_nm` | 발행사명 | 20 |
| `elwdispty_rt[].sqnc` | 회차 | 20 |
| `elwdispty_rt[].base_aset_nm` | 기초자산명 | 20 |
| `elwdispty_rt[].rght_tp` | 권리구분 | 20 |
| `elwdispty_rt[].dispty_rt` | 괴리율 | 20 |
| `elwdispty_rt[].basis` | 베이시스 | 20 |
| `elwdispty_rt[].srvive_dys` | 잔존일수 | 20 |
| `elwdispty_rt[].theory_pric` | 이론가 | 20 |
| `elwdispty_rt[].cur_prc` | 현재가 | 20 |
| `elwdispty_rt[].pre_tp` | 대비구분 | 20 |
| `elwdispty_rt[].pred_pre` | 전일대비 | 20 |
| `elwdispty_rt[].flu_rt` | 등락율 | 20 |
| `elwdispty_rt[].trde_qty` | 거래량 | 20 |
| `elwdispty_rt[].stk_nm` | 종목명 | 40 |

<a id="ka30005"></a>

## `ka30005` · `condition_search()` — ELW조건검색요청

ELW조건검색요청 (ELW Condition Search) · `POST /api/dostk/elw`

```python
api.elw.condition_search(isscomp_cd=..., bsis_aset_cd=..., rght_tp=..., lpcd=..., sort_tp=...)
```

**요청**

| 필드 | 한글명 | 필수 | 길이 |
|---|---|:---:|---:|
| `isscomp_cd` | 발행사코드 | Y | 12 |
| `bsis_aset_cd` | 기초자산코드 | Y | 12 |
| `rght_tp` | 권리구분 | Y | 1 |
| `lpcd` | LP코드 | Y | 12 |
| `sort_tp` | 정렬구분 | Y | 1 |

**응답**

| 필드 | 한글명 | 길이 |
|---|---|---:|
| `elwcnd_qry` (list) | ELW조건검색 |  |
| `elwcnd_qry[].stk_cd` | 종목코드 | 20 |
| `elwcnd_qry[].isscomp_nm` | 발행사명 | 20 |
| `elwcnd_qry[].sqnc` | 회차 | 20 |
| `elwcnd_qry[].base_aset_nm` | 기초자산명 | 20 |
| `elwcnd_qry[].rght_tp` | 권리구분 | 20 |
| `elwcnd_qry[].expr_dt` | 만기일 | 20 |
| `elwcnd_qry[].cur_prc` | 현재가 | 20 |
| `elwcnd_qry[].pre_tp` | 대비구분 | 20 |
| `elwcnd_qry[].pred_pre` | 전일대비 | 20 |
| `elwcnd_qry[].flu_rt` | 등락율 | 20 |
| `elwcnd_qry[].trde_qty` | 거래량 | 20 |
| `elwcnd_qry[].trde_qty_pre` | 거래량대비 | 20 |
| `elwcnd_qry[].trde_prica` | 거래대금 | 20 |
| `elwcnd_qry[].pred_trde_qty` | 전일거래량 | 20 |
| `elwcnd_qry[].sel_bid` | 매도호가 | 20 |
| `elwcnd_qry[].buy_bid` | 매수호가 | 20 |
| `elwcnd_qry[].prty` | 패리티 | 20 |
| `elwcnd_qry[].gear_rt` | 기어링비율 | 20 |
| `elwcnd_qry[].pl_qutr_rt` | 손익분기율 | 20 |
| `elwcnd_qry[].cfp` | 자본지지점 | 20 |
| `elwcnd_qry[].theory_pric` | 이론가 | 20 |
| `elwcnd_qry[].innr_vltl` | 내재변동성 | 20 |
| `elwcnd_qry[].delta` | 델타 | 20 |
| `elwcnd_qry[].lvrg` | 레버리지 | 20 |
| `elwcnd_qry[].exec_pric` | 행사가격 | 20 |
| `elwcnd_qry[].cnvt_rt` | 전환비율 | 20 |
| `elwcnd_qry[].lpposs_rt` | LP보유비율 | 20 |
| `elwcnd_qry[].pl_qutr_pt` | 손익분기점 | 20 |
| `elwcnd_qry[].fin_trde_dt` | 최종거래일 | 20 |
| `elwcnd_qry[].flo_dt` | 상장일 | 20 |
| `elwcnd_qry[].lpinitlast_suply_dt` | LP초종공급일 | 20 |
| `elwcnd_qry[].stk_nm` | 종목명 | 40 |
| `elwcnd_qry[].srvive_dys` | 잔존일수 | 20 |
| `elwcnd_qry[].dispty_rt` | 괴리율 | 20 |
| `elwcnd_qry[].lpmmcm_nm` | LP회원사명 | 20 |
| `elwcnd_qry[].lpmmcm_nm_1` | LP회원사명1 | 20 |
| `elwcnd_qry[].lpmmcm_nm_2` | LP회원사명2 | 20 |
| `elwcnd_qry[].xraymont_cntr_qty_arng_trde_tp` | Xray순간체결량정리매매구분 | 20 |
| `elwcnd_qry[].xraymont_cntr_qty_profa_100tp` | Xray순간체결량증거금100구분 | 20 |

<a id="ka30009"></a>

## `ka30009` · `change_rate_ranking()` — ELW등락율순위요청

ELW등락율순위요청 (ELW Change Rate Ranking) · `POST /api/dostk/elw`

```python
api.elw.change_rate_ranking(sort_tp=..., rght_tp=..., trde_end_skip=...)
```

**요청**

| 필드 | 한글명 | 필수 | 길이 |
|---|---|:---:|---:|
| `sort_tp` | 정렬구분 | Y | 1 |
| `rght_tp` | 권리구분 | Y | 3 |
| `trde_end_skip` | 거래종료제외 | Y | 1 |

**응답**

| 필드 | 한글명 | 길이 |
|---|---|---:|
| `elwflu_rt_rank` (list) | ELW등락율순위 |  |
| `elwflu_rt_rank[].rank` | 순위 | 20 |
| `elwflu_rt_rank[].stk_cd` | 종목코드 | 20 |
| `elwflu_rt_rank[].stk_nm` | 종목명 | 40 |
| `elwflu_rt_rank[].cur_prc` | 현재가 | 20 |
| `elwflu_rt_rank[].pre_sig` | 대비기호 | 20 |
| `elwflu_rt_rank[].pred_pre` | 전일대비 | 20 |
| `elwflu_rt_rank[].flu_rt` | 등락률 | 20 |
| `elwflu_rt_rank[].sel_req` | 매도잔량 | 20 |
| `elwflu_rt_rank[].buy_req` | 매수잔량 | 20 |
| `elwflu_rt_rank[].trde_qty` | 거래량 | 20 |
| `elwflu_rt_rank[].trde_prica` | 거래대금 | 20 |

<a id="ka30010"></a>

## `ka30010` · `order_volume_ranking()` — ELW잔량순위요청

ELW호가잔량순위요청 (ELW Order Volume Ranking) · `POST /api/dostk/elw`

```python
api.elw.order_volume_ranking(sort_tp=..., rght_tp=..., trde_end_skip=...)
```

**요청**

| 필드 | 한글명 | 필수 | 길이 |
|---|---|:---:|---:|
| `sort_tp` | 정렬구분 | Y | 1 |
| `rght_tp` | 권리구분 | Y | 3 |
| `trde_end_skip` | 거래종료제외 | Y | 1 |

**응답**

| 필드 | 한글명 | 길이 |
|---|---|---:|
| `elwreq_rank` (list) | ELW잔량순위 |  |
| `elwreq_rank[].stk_cd` | 종목코드 | 20 |
| `elwreq_rank[].rank` | 순위 | 20 |
| `elwreq_rank[].stk_nm` | 종목명 | 40 |
| `elwreq_rank[].cur_prc` | 현재가 | 20 |
| `elwreq_rank[].pre_sig` | 대비기호 | 20 |
| `elwreq_rank[].pred_pre` | 전일대비 | 20 |
| `elwreq_rank[].flu_rt` | 등락률 | 20 |
| `elwreq_rank[].trde_qty` | 거래량 | 20 |
| `elwreq_rank[].sel_req` | 매도잔량 | 20 |
| `elwreq_rank[].buy_req` | 매수잔량 | 20 |
| `elwreq_rank[].netprps_req` | 순매수잔량 | 20 |
| `elwreq_rank[].trde_prica` | 거래대금 | 20 |

<a id="ka30011"></a>

## `ka30011` · `proximity_rate()` — ELW근접율요청

ELW근접율요청 (ELW Proximity Rate) · `POST /api/dostk/elw`

```python
api.elw.proximity_rate(stk_cd=...)
```

**요청**

| 필드 | 한글명 | 필수 | 길이 |
|---|---|:---:|---:|
| `stk_cd` | 종목코드 | Y | 6 |

**응답**

| 필드 | 한글명 | 길이 |
|---|---|---:|
| `elwalacc_rt` (list) | ELW근접율 |  |
| `elwalacc_rt[].stk_cd` | 종목코드 | 20 |
| `elwalacc_rt[].stk_nm` | 종목명 | 40 |
| `elwalacc_rt[].cur_prc` | 현재가 | 20 |
| `elwalacc_rt[].pre_sig` | 대비기호 | 20 |
| `elwalacc_rt[].pred_pre` | 전일대비 | 20 |
| `elwalacc_rt[].flu_rt` | 등락율 | 20 |
| `elwalacc_rt[].acc_trde_qty` | 누적거래량 | 20 |
| `elwalacc_rt[].alacc_rt` | 근접율 | 20 |

<a id="ka30012"></a>

## `ka30012` · `detailed_stock_info()` — ELW종목상세정보요청

ELW종목상세정보요청 (ELW Detailed Stock Info) · `POST /api/dostk/elw`

```python
api.elw.detailed_stock_info(stk_cd=...)
```

**요청**

| 필드 | 한글명 | 필수 | 길이 |
|---|---|:---:|---:|
| `stk_cd` | 종목코드 | Y | 6 |

**응답**

| 필드 | 한글명 | 길이 |
|---|---|---:|
| `aset_cd` | 자산코드 | 20 |
| `cur_prc` | 현재가 | 20 |
| `pred_pre_sig` | 전일대비기호 | 20 |
| `pred_pre` | 전일대비 | 20 |
| `flu_rt` | 등락율 | 20 |
| `lpmmcm_nm` | LP회원사명 | 20 |
| `lpmmcm_nm_1` | LP회원사명1 | 20 |
| `lpmmcm_nm_2` | LP회원사명2 | 20 |
| `elwrght_cntn` | ELW권리내용 | 20 |
| `elwexpr_evlt_pric` | ELW만기평가가격 | 20 |
| `elwtheory_pric` | ELW이론가 | 20 |
| `dispty_rt` | 괴리율 | 20 |
| `elwinnr_vltl` | ELW내재변동성 | 20 |
| `exp_rght_pric` | 예상권리가 | 20 |
| `elwpl_qutr_rt` | ELW손익분기율 | 20 |
| `elwexec_pric` | ELW행사가 | 20 |
| `elwcnvt_rt` | ELW전환비율 | 20 |
| `elwcmpn_rt` | ELW보상율 | 20 |
| `elwpric_rising_part_rt` | ELW가격상승참여율 | 20 |
| `elwrght_type` | ELW권리유형 | 20 |
| `elwsrvive_dys` | ELW잔존일수 | 20 |
| `stkcnt` | 상장주식수 | 20 |
| `elwlpord_pos` | ELWLP주문가능 | 20 |
| `lpposs_rt` | LP보유비율 | 20 |
| `lprmnd_qty` | LP보유수량 | 20 |
| `elwspread` | ELW스프레드 | 20 |
| `elwprty` | ELW패리티 | 20 |
| `elwgear` | ELW기어링 | 20 |
| `elwflo_dt` | ELW상장일 | 20 |
| `elwfin_trde_dt` | ELW최종거래일 | 20 |
| `expr_dt` | 만기일 | 20 |
| `exec_dt` | 행사일 | 20 |
| `lpsuply_end_dt` | LP공급종료일 | 20 |
| `elwpay_dt` | ELW지급일 | 20 |
| `elwinvt_ix_comput` | ELW투자지표산출 |  |
| `elwpay_agnt` | ELW지급대리인 |  |
| `elwappr_way` | ELW결재방법 |  |
| `elwrght_exec_way` | ELW권리행사방식 |  |
| `elwpblicte_orgn` | ELW발행기관 |  |
| `dcsn_pay_amt` | 확정지급액 |  |
| `kobarr` | KO베리어 |  |
| `iv` | IV |  |
| `clsprd_end_elwocr` | 종기종료ELW발생 |  |
| `bsis_aset_1` | 기초자산1 |  |
| `bsis_aset_comp_rt_1` | 기초자산구성비율1 |  |
| `bsis_aset_2` | 기초자산2 |  |
| `bsis_aset_comp_rt_2` | 기초자산구성비율2 |  |
| `bsis_aset_3` | 기초자산3 |  |
| `bsis_aset_comp_rt_3` | 기초자산구성비율3 |  |
| `bsis_aset_4` | 기초자산4 |  |
| `bsis_aset_comp_rt_4` | 기초자산구성비율4 |  |
| `bsis_aset_5` | 기초자산5 |  |
| `bsis_aset_comp_rt_5` | 기초자산구성비율5 |  |
| `fr_dt` | 평가시작일자 |  |
| `to_dt` | 평가종료일자 |  |
| `fr_tm` | 평가시작시간 |  |
| `evlt_end_tm` | 평가종료시간 |  |
| `evlt_pric` | 평가가격 |  |
| `evlt_fnsh_yn` | 평가완료여부 |  |
| `all_hgst_pric` | 전체최고가 |  |
| `all_lwst_pric` | 전체최저가 |  |
| `imaf_hgst_pric` | 직후최고가 |  |
| `imaf_lwst_pric` | 직후최저가 |  |
| `sndhalf_mrkt_hgst_pric` | 후반장최고가 |  |
| `sndhalf_mrkt_lwst_pric` | 후반장최저가 |  |
