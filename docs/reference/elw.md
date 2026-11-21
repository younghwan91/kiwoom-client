<!-- 자동 생성 파일 — 손으로 고치지 마세요. `python scripts/gen_docs.py` 가 TR 카탈로그(kiwoom_client.spec)로 다시 만듭니다. -->

# `api.elw` — ELW

요청·응답 필드는 키움 공식 REST API 명세에서 만든 TR 카탈로그([출처·라이선스](https://github.com/younghwan91/kiwoom-client/blob/main/src/kiwoom_client/spec/SOURCE.md))를 그대로 옮긴 것입니다. 뜻이 애매하면 [키움 REST API 포털](https://openapi.kiwoom.com)이 기준입니다. 값은 모두 문자열로 넘깁니다.

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

| 필드 | 한글명 | 필수 | 길이 | 설명 |
|---|---|:---:|---:|---|
| `stk_cd` | 종목코드 | Y | 6 |   |

**응답**

| 필드 | 한글명 | 길이 | 설명 |
|---|---|---:|---|
| `elwdaly_snst_ix` (list) | ELW일별민감도지표 |  |   |
| `elwdaly_snst_ix[].dt` | 일자 | 20 |   |
| `elwdaly_snst_ix[].iv` | IV | 20 | 소수점 제거 된 100배 값으로 제공 예) "2658"는 26.58를 의미합니다. |
| `elwdaly_snst_ix[].delta` | 델타 | 20 | 소수점 제거한 값으로 제공 예) "590470"값은 0.590470을 의미합니다. |
| `elwdaly_snst_ix[].gam` | 감마 | 20 | 소수점 제거한 값으로 제공 예) "167"값은 0.000167을 의미합니다. |
| `elwdaly_snst_ix[].theta` | 쎄타 | 20 | 소수점 제거한 값으로 제공 예) "-991554"값은 -0.991554를 의미합니다. |
| `elwdaly_snst_ix[].vega` | 베가 | 20 | 소수점 제거한 값으로 제공 예) "-991554"값은 -0.991554를 의미합니다. |
| `elwdaly_snst_ix[].law` | 로 | 20 | 소수점 제거한 값으로 제공 예) "76850"값은 0.076850을 의미합니다. |
| `elwdaly_snst_ix[].lp` | LP | 20 | 소수점 제거 된 100배 값으로 제공 예) "6197"값은 61.87을 의미합니다. |

<a id="ka10050"></a>

## `ka10050` · `sensitivity_indicator()` — ELW민감도지표요청

ELW민감도지표요청 (ELW Sensitivity Indicator) · `POST /api/dostk/elw`

```python
api.elw.sensitivity_indicator(stk_cd=...)
```

**요청**

| 필드 | 한글명 | 필수 | 길이 | 설명 |
|---|---|:---:|---:|---|
| `stk_cd` | 종목코드 | Y | 6 |   |

**응답**

| 필드 | 한글명 | 길이 | 설명 |
|---|---|---:|---|
| `elwsnst_ix_array` (list) | ELW민감도지표배열 |  |   |
| `elwsnst_ix_array[].cntr_tm` | 체결시간 | 20 | HHmmss |
| `elwsnst_ix_array[].cur_prc` | 현재가 | 20 | 단위: 원 |
| `elwsnst_ix_array[].elwtheory_pric` | ELW이론가 | 20 | 소수점 제거 된 100배 값으로 제공 예) "2658"값은 26.58을 의미합니다. |
| `elwsnst_ix_array[].iv` | IV | 20 | 소수점 제거 된 100배 값으로 제공 예) "2658"값은 26.58을 의미합니다. |
| `elwsnst_ix_array[].delta` | 델타 | 20 | 소수점 제거한 값으로 제공 예) "590470"값은 0.590470을 의미합니다. |
| `elwsnst_ix_array[].gam` | 감마 | 20 | 소수점 제거한 값으로 제공 예) "163"값은 0.000163을 의미합니다. |
| `elwsnst_ix_array[].theta` | 쎄타 | 20 | 소수점 제거한 값으로 제공 예) "-1057402"값은 -1.057402을 의미합니다. |
| `elwsnst_ix_array[].vega` | 베가 | 20 | 소수점 제거한 값으로 제공 예) "290965"값은 0.290965을 의미합니다. |
| `elwsnst_ix_array[].law` | 로 | 20 | 소수점 제거한 값으로 제공 예) "73629"값은 0.073629을 의미합니다. |
| `elwsnst_ix_array[].lp` | LP | 20 | 소수점 제거 된 100배 값으로 제공 예) "2658"값은 26.58을 의미합니다. |

<a id="ka30001"></a>

## `ka30001` · `price_spike()` — ELW가격급등락요청

ELW급등락요청 (ELW Price Spike) · `POST /api/dostk/elw`

```python
api.elw.price_spike(flu_tp=..., tm_tp=..., tm=..., trde_qty_tp=..., isscomp_cd=..., bsis_aset_cd=..., rght_tp=..., lpcd=..., trde_end_elwskip=...)
```

**요청**

| 필드 | 한글명 | 필수 | 길이 | 설명 |
|---|---|:---:|---:|---|
| `flu_tp` | 등락구분 | Y | 1 | 1:급등, 2:급락 |
| `tm_tp` | 시간구분 | Y | 1 | 1:분전, 2:일전 |
| `tm` | 시간 | Y | 2 | 분 혹은 일입력 (예 1, 3, 5) |
| `trde_qty_tp` | 거래량구분 | Y | 4 | 0:전체, 10:만주이상, 50:5만주이상, 100:10만주이상, 300:30만주이상, 500:50만주이상, 1000:백만주이상 |
| `isscomp_cd` | 발행사코드 | Y | 12 | 전체:000000000000, 한국투자증권:3, 미래대우:5, 신영:6, NK투자증권:12, KB증권:17 |
| `bsis_aset_cd` | 기초자산코드 | Y | 12 | 전체:000000000000, KOSPI200:201, KOSDAQ150:150, 삼성전자:005930, KT:030200.. |
| `rght_tp` | 권리구분 | Y | 3 | 000:전체, 001:콜, 002:풋, 003:DC, 004:DP, 005:EX, 006:조기종료콜, 007:조기종료풋 |
| `lpcd` | LP코드 | Y | 12 | 전체:000000000000, 한국투자증권:3, 미래대우:5, 신영:6, NK투자증권:12, KB증권:17 |
| `trde_end_elwskip` | 거래종료ELW제외 | Y | 1 | 0:포함, 1:제외 |

**응답**

| 필드 | 한글명 | 길이 | 설명 |
|---|---|---:|---|
| `base_pric_tm` | 기준가시간 | 20 |   |
| `elwpric_jmpflu` (list) | ELW가격급등락 |  |   |
| `elwpric_jmpflu[].stk_cd` | 종목코드 | 20 |   |
| `elwpric_jmpflu[].rank` | 순위 | 20 |   |
| `elwpric_jmpflu[].stk_nm` | 종목명 | 40 |   |
| `elwpric_jmpflu[].pre_sig` | 대비기호 | 20 | 1: 상한가, 2:상승, 3:보합, 4:하한가, 5:하락 |
| `elwpric_jmpflu[].pred_pre` | 전일대비 | 20 | 단위: 원, 부호가 포함된 숫자 |
| `elwpric_jmpflu[].trde_end_elwbase_pric` | 거래종료ELW기준가 | 20 | 단위: 원 |
| `elwpric_jmpflu[].cur_prc` | 현재가 | 20 | 단위: 원, 부호가 포함된 숫자 |
| `elwpric_jmpflu[].base_pre` | 기준대비 | 20 | 단위: 원 |
| `elwpric_jmpflu[].trde_qty` | 거래량 | 20 | 단위: 1주 |
| `elwpric_jmpflu[].jmp_rt` | 급등율 | 20 | 단위: %, 부호 포함 소수점 둘째 자리까지 포맷된 백분율 |

<a id="ka30002"></a>

## `ka30002` · `top_net_buying_by_broker()` — 거래원별ELW순매매상위요청

ELW회원사별순매수상위요청 (ELW Top Net Buying by Broker) · `POST /api/dostk/elw`

```python
api.elw.top_net_buying_by_broker(isscomp_cd=..., trde_qty_tp=..., trde_tp=..., dt=..., trde_end_elwskip=...)
```

**요청**

| 필드 | 한글명 | 필수 | 길이 | 설명 |
|---|---|:---:|---:|---|
| `isscomp_cd` | 발행사코드 | Y | 3 | 3자리, 영웅문4 0273화면참조 (교보:001, 신한금융투자:002, 한국투자증권:003, 대신:004, 미래대우:005, ,,,) |
| `trde_qty_tp` | 거래량구분 | Y | 4 | 0:전체, 5:5천주, 10:만주, 50:5만주, 100:10만주, 500:50만주, 1000:백만주 |
| `trde_tp` | 매매구분 | Y | 1 | 1:순매수, 2:순매도 |
| `dt` | 기간 | Y | 2 | 1:전일, 5:5일, 10:10일, 40:40일, 60:60일 |
| `trde_end_elwskip` | 거래종료ELW제외 | Y | 1 | 0:포함, 1:제외 |

**응답**

| 필드 | 한글명 | 길이 | 설명 |
|---|---|---:|---|
| `trde_ori_elwnettrde_upper` (list) | 거래원별ELW순매매상위 |  |   |
| `trde_ori_elwnettrde_upper[].stk_cd` | 종목코드 | 20 |   |
| `trde_ori_elwnettrde_upper[].stk_nm` | 종목명 | 40 |   |
| `trde_ori_elwnettrde_upper[].stkpc_flu` | 주가등락 | 20 | 부호가 포함된 숫자 |
| `trde_ori_elwnettrde_upper[].flu_rt` | 등락율 | 20 | 단위: %, 부호 포함 소수점 둘째 자리까지 포맷된 백분율 |
| `trde_ori_elwnettrde_upper[].trde_qty` | 거래량 | 20 | 단위: 1주 |
| `trde_ori_elwnettrde_upper[].netprps` | 순매수 | 20 | 단위: 1주, 부호가 포함된 숫자 |
| `trde_ori_elwnettrde_upper[].buy_trde_qty` | 매수거래량 | 20 | 단위: 1주 |
| `trde_ori_elwnettrde_upper[].sel_trde_qty` | 매도거래량 | 20 | 단위: 1주 |

<a id="ka30003"></a>

## `ka30003` · `lp_daily_holding_trend()` — ELWLP보유일별추이요청

ELW LP일별보유추이요청 (ELW LP Daily Holding Trend) · `POST /api/dostk/elw`

```python
api.elw.lp_daily_holding_trend(bsis_aset_cd=..., base_dt=...)
```

**요청**

| 필드 | 한글명 | 필수 | 길이 | 설명 |
|---|---|:---:|---:|---|
| `bsis_aset_cd` | 기초자산코드 | Y | 12 |   |
| `base_dt` | 기준일자 | Y | 8 | YYYYMMDD |

**응답**

| 필드 | 한글명 | 길이 | 설명 |
|---|---|---:|---|
| `elwlpposs_daly_trnsn` (list) | ELWLP보유일별추이 |  |   |
| `elwlpposs_daly_trnsn[].dt` | 일자 | 20 | YYYYMMDD |
| `elwlpposs_daly_trnsn[].cur_prc` | 현재가 | 20 | 단위: 원, 부호가 포함된 숫자 |
| `elwlpposs_daly_trnsn[].pre_tp` | 대비구분 | 20 |   |
| `elwlpposs_daly_trnsn[].pred_pre` | 전일대비 | 20 | 단위: 원, 부호가 포함된 숫자 |
| `elwlpposs_daly_trnsn[].flu_rt` | 등락율 | 20 | 단위: %, 부호 포함 소수점 둘째 자리까지 포맷된 백분율 |
| `elwlpposs_daly_trnsn[].trde_qty` | 거래량 | 20 | 단위: 1주 |
| `elwlpposs_daly_trnsn[].trde_prica` | 거래대금 | 20 | 단위: 백만원 |
| `elwlpposs_daly_trnsn[].chg_qty` | 변동수량 | 20 | 단위: 1주 |
| `elwlpposs_daly_trnsn[].lprmnd_qty` | LP보유수량 | 20 | 단위: 1주 |
| `elwlpposs_daly_trnsn[].wght` | 비중 | 20 | 단위: %, 부호 포함 소수점 둘째 자리까지 포맷된 백분율 |

<a id="ka30004"></a>

## `ka30004` · `premium_rate()` — ELW괴리율요청

ELW괴리율요청 (ELW Premium Rate) · `POST /api/dostk/elw`

```python
api.elw.premium_rate(isscomp_cd=..., bsis_aset_cd=..., rght_tp=..., lpcd=..., trde_end_elwskip=...)
```

**요청**

| 필드 | 한글명 | 필수 | 길이 | 설명 |
|---|---|:---:|---:|---|
| `isscomp_cd` | 발행사코드 | Y | 12 | 전체:000000000000, 한국투자증권:3, 미래대우:5, 신영:6, NK투자증권:12, KB증권:17 |
| `bsis_aset_cd` | 기초자산코드 | Y | 12 | 전체:000000000000, KOSPI200:201, KOSDAQ150:150, 삼성전자:005930, KT:030200.. |
| `rght_tp` | 권리구분 | Y | 3 | 000: 전체, 001: 콜, 002: 풋, 003: DC, 004: DP, 005: EX, 006: 조기종료콜, 007: 조기종료풋 |
| `lpcd` | LP코드 | Y | 12 | 전체:000000000000, 한국투자증권:3, 미래대우:5, 신영:6, NK투자증권:12, KB증권:17 |
| `trde_end_elwskip` | 거래종료ELW제외 | Y | 1 | 1:거래종료ELW제외, 0:거래종료ELW포함 |

**응답**

| 필드 | 한글명 | 길이 | 설명 |
|---|---|---:|---|
| `elwdispty_rt` (list) | ELW괴리율 |  |   |
| `elwdispty_rt[].stk_cd` | 종목코드 | 20 |   |
| `elwdispty_rt[].isscomp_nm` | 발행사명 | 20 |   |
| `elwdispty_rt[].sqnc` | 회차 | 20 |   |
| `elwdispty_rt[].base_aset_nm` | 기초자산명 | 20 |   |
| `elwdispty_rt[].rght_tp` | 권리구분 | 20 |   |
| `elwdispty_rt[].dispty_rt` | 괴리율 | 20 | 소수점 제거 된 100배 값으로 제공 예) "2658"값은 26.58을 의미합니다. |
| `elwdispty_rt[].basis` | 베이시스 | 20 | 단위: %, 부호 포함 소수점 둘째 자리까지 포맷된 백분율 |
| `elwdispty_rt[].srvive_dys` | 잔존일수 | 20 |   |
| `elwdispty_rt[].theory_pric` | 이론가 | 20 | 소수점 제거 된 100배 값으로 제공 예) "2658"값은 26.58을 의미합니다. |
| `elwdispty_rt[].cur_prc` | 현재가 | 20 | 단위: 원, 부호가 포함된 숫자 |
| `elwdispty_rt[].pre_tp` | 대비구분 | 20 | 1: 상한가, 2:상승, 3:보합, 4:하한가, 5:하락 |
| `elwdispty_rt[].pred_pre` | 전일대비 | 20 | 단위: 원, 부호가 포함된 숫자 |
| `elwdispty_rt[].flu_rt` | 등락율 | 20 | 단위: %, 부호 포함 소수점 둘째 자리까지 포맷된 백분율 |
| `elwdispty_rt[].trde_qty` | 거래량 | 20 | 단위: 1주 |
| `elwdispty_rt[].stk_nm` | 종목명 | 40 |   |

<a id="ka30005"></a>

## `ka30005` · `condition_search()` — ELW조건검색요청

ELW조건검색요청 (ELW Condition Search) · `POST /api/dostk/elw`

```python
api.elw.condition_search(isscomp_cd=..., bsis_aset_cd=..., rght_tp=..., lpcd=..., sort_tp=...)
```

**요청**

| 필드 | 한글명 | 필수 | 길이 | 설명 |
|---|---|:---:|---:|---|
| `isscomp_cd` | 발행사코드 | Y | 12 | 12자리입력(전체:000000000000, 한국투자증권:000,,,3, 미래대우:000,,,5, 신영:000,,,6, NK투자증권:000,,,12, KB증권:000,,,17) |
| `bsis_aset_cd` | 기초자산코드 | Y | 12 | 전체일때만 12자리입력(전체:000000000000, KOSPI200:201, KOSDAQ150:150, 삼정전자:005930, KT:030200,,) |
| `rght_tp` | 권리구분 | Y | 1 | 0:전체, 1:콜, 2:풋, 3:DC, 4:DP, 5:EX, 6:조기종료콜, 7:조기종료풋 |
| `lpcd` | LP코드 | Y | 12 | 전체일때만 12자리입력(전체:000000000000, 한국투자증권:003, 미래대우:005, 신영:006, NK투자증권:012, KB증권:017) |
| `sort_tp` | 정렬구분 | Y | 1 | 0:정렬없음, 1:상승율순, 2:상승폭순, 3:하락율순, 4:하락폭순, 5:거래량순, 6:거래대금순, 7:잔존일순 |

**응답**

| 필드 | 한글명 | 길이 | 설명 |
|---|---|---:|---|
| `elwcnd_qry` (list) | ELW조건검색 |  |   |
| `elwcnd_qry[].stk_cd` | 종목코드 | 20 |   |
| `elwcnd_qry[].isscomp_nm` | 발행사명 | 20 |   |
| `elwcnd_qry[].sqnc` | 회차 | 20 |   |
| `elwcnd_qry[].base_aset_nm` | 기초자산명 | 20 |   |
| `elwcnd_qry[].rght_tp` | 권리구분 | 20 |   |
| `elwcnd_qry[].expr_dt` | 만기일 | 20 | YYYYMMDD |
| `elwcnd_qry[].cur_prc` | 현재가 | 20 | 단위: 원, 부호가 포함된 숫자 |
| `elwcnd_qry[].pre_tp` | 대비구분 | 20 | 1: 상한가, 2:상승, 3:보합, 4:하한가, 5:하락 |
| `elwcnd_qry[].pred_pre` | 전일대비 | 20 | 단위: 원, 부호가 포함된 숫자 |
| `elwcnd_qry[].flu_rt` | 등락율 | 20 | 단위: %, 부호 포함 소수점 둘째 자리까지 포맷된 백분율 |
| `elwcnd_qry[].trde_qty` | 거래량 | 20 | 단위: 1주 |
| `elwcnd_qry[].trde_qty_pre` | 거래량대비 | 20 | 단위: 1주, 부호가 포함된 숫자 |
| `elwcnd_qry[].trde_prica` | 거래대금 | 20 | 단위: 백만원 |
| `elwcnd_qry[].pred_trde_qty` | 전일거래량 | 20 | 단위: 1주 |
| `elwcnd_qry[].sel_bid` | 매도호가 | 20 | 단위: 원, 부호가 포함된 숫자 |
| `elwcnd_qry[].buy_bid` | 매수호가 | 20 | 단위: 원, 부호가 포함된 숫자 |
| `elwcnd_qry[].prty` | 패리티 | 20 | 소수점 둘째 자리까지 포맷된 숫자 |
| `elwcnd_qry[].gear_rt` | 기어링비율 | 20 | 단위: %, 소수점 둘째 자리까지 포맷된 백분율 |
| `elwcnd_qry[].pl_qutr_rt` | 손익분기율 | 20 | 단위: %, 부호 포함 소수점 둘째 자리까지 포맷된 백분율 |
| `elwcnd_qry[].cfp` | 자본지지점 | 20 |   |
| `elwcnd_qry[].theory_pric` | 이론가 | 20 |   |
| `elwcnd_qry[].innr_vltl` | 내재변동성 | 20 |   |
| `elwcnd_qry[].delta` | 델타 | 20 |   |
| `elwcnd_qry[].lvrg` | 레버리지 | 20 |   |
| `elwcnd_qry[].exec_pric` | 행사가격 | 20 | 단위: 원 |
| `elwcnd_qry[].cnvt_rt` | 전환비율 | 20 | 소수점 넷째 자리까지 포맷된 숫자 |
| `elwcnd_qry[].lpposs_rt` | LP보유비율 | 20 | 단위: %, 부호 포함 소수점 둘째 자리까지 포맷된 백분율 |
| `elwcnd_qry[].pl_qutr_pt` | 손익분기점 | 20 |   |
| `elwcnd_qry[].fin_trde_dt` | 최종거래일 | 20 | YYYYMMDD |
| `elwcnd_qry[].flo_dt` | 상장일 | 20 | YYYYMMDD |
| `elwcnd_qry[].lpinitlast_suply_dt` | LP초종공급일 | 20 | YYYYMMDD |
| `elwcnd_qry[].stk_nm` | 종목명 | 40 |   |
| `elwcnd_qry[].srvive_dys` | 잔존일수 | 20 |   |
| `elwcnd_qry[].dispty_rt` | 괴리율 | 20 | 단위: %, 부호 포함 소수점 둘째 자리까지 포맷된 백분율 |
| `elwcnd_qry[].lpmmcm_nm` | LP회원사명 | 20 |   |
| `elwcnd_qry[].lpmmcm_nm_1` | LP회원사명1 | 20 |   |
| `elwcnd_qry[].lpmmcm_nm_2` | LP회원사명2 | 20 |   |
| `elwcnd_qry[].xraymont_cntr_qty_arng_trde_tp` | Xray순간체결량정리매매구분 | 20 |   |
| `elwcnd_qry[].xraymont_cntr_qty_profa_100tp` | Xray순간체결량증거금100구분 | 20 |   |

<a id="ka30009"></a>

## `ka30009` · `change_rate_ranking()` — ELW등락율순위요청

ELW등락율순위요청 (ELW Change Rate Ranking) · `POST /api/dostk/elw`

```python
api.elw.change_rate_ranking(sort_tp=..., rght_tp=..., trde_end_skip=...)
```

**요청**

| 필드 | 한글명 | 필수 | 길이 | 설명 |
|---|---|:---:|---:|---|
| `sort_tp` | 정렬구분 | Y | 1 | 1:상승률, 2:상승폭, 3:하락률, 4:하락폭 |
| `rght_tp` | 권리구분 | Y | 3 | 000:전체, 001:콜, 002:풋, 003:DC, 004:DP, 006:조기종료콜, 007:조기종료풋 |
| `trde_end_skip` | 거래종료제외 | Y | 1 | 1:거래종료제외, 0:거래종료포함 |

**응답**

| 필드 | 한글명 | 길이 | 설명 |
|---|---|---:|---|
| `elwflu_rt_rank` (list) | ELW등락율순위 |  |   |
| `elwflu_rt_rank[].rank` | 순위 | 20 |   |
| `elwflu_rt_rank[].stk_cd` | 종목코드 | 20 |   |
| `elwflu_rt_rank[].stk_nm` | 종목명 | 40 |   |
| `elwflu_rt_rank[].cur_prc` | 현재가 | 20 | 단위: 원, 부호가 포함된 숫자 |
| `elwflu_rt_rank[].pre_sig` | 대비기호 | 20 | 1: 상한가, 2:상승, 3:보합, 4:하한가, 5:하락 |
| `elwflu_rt_rank[].pred_pre` | 전일대비 | 20 | 단위: 원, 부호가 포함된 숫자 |
| `elwflu_rt_rank[].flu_rt` | 등락률 | 20 | 단위: %, 부호 포함 소수점 둘째 자리까지 포맷된 백분율 |
| `elwflu_rt_rank[].sel_req` | 매도잔량 | 20 | 단위: 1주 |
| `elwflu_rt_rank[].buy_req` | 매수잔량 | 20 | 단위: 1주 |
| `elwflu_rt_rank[].trde_qty` | 거래량 | 20 | 단위: 1주 |
| `elwflu_rt_rank[].trde_prica` | 거래대금 | 20 | 단위: 백만원 |

<a id="ka30010"></a>

## `ka30010` · `order_volume_ranking()` — ELW잔량순위요청

ELW호가잔량순위요청 (ELW Order Volume Ranking) · `POST /api/dostk/elw`

```python
api.elw.order_volume_ranking(sort_tp=..., rght_tp=..., trde_end_skip=...)
```

**요청**

| 필드 | 한글명 | 필수 | 길이 | 설명 |
|---|---|:---:|---:|---|
| `sort_tp` | 정렬구분 | Y | 1 | 1:순매수잔량상위, 2: 순매도 잔량상위 |
| `rght_tp` | 권리구분 | Y | 3 | 000: 전체, 001: 콜, 002: 풋, 003: DC, 004: DP, 006: 조기종료콜, 007: 조기종료풋 |
| `trde_end_skip` | 거래종료제외 | Y | 1 | 1:거래종료제외, 0:거래종료포함 |

**응답**

| 필드 | 한글명 | 길이 | 설명 |
|---|---|---:|---|
| `elwreq_rank` (list) | ELW잔량순위 |  |   |
| `elwreq_rank[].stk_cd` | 종목코드 | 20 |   |
| `elwreq_rank[].rank` | 순위 | 20 |   |
| `elwreq_rank[].stk_nm` | 종목명 | 40 |   |
| `elwreq_rank[].cur_prc` | 현재가 | 20 | 단위: 원, 부호가 포함된 숫자 |
| `elwreq_rank[].pre_sig` | 대비기호 | 20 | 1: 상한가, 2:상승, 3:보합, 4:하한가, 5:하락 |
| `elwreq_rank[].pred_pre` | 전일대비 | 20 | 단위: 원, 부호가 포함된 숫자 |
| `elwreq_rank[].flu_rt` | 등락률 | 20 | 단위: %, 부호 포함 소수점 둘째 자리까지 포맷된 백분율 |
| `elwreq_rank[].trde_qty` | 거래량 | 20 | 단위: 1주 |
| `elwreq_rank[].sel_req` | 매도잔량 | 20 | 단위: 1주 |
| `elwreq_rank[].buy_req` | 매수잔량 | 20 | 단위: 1주 |
| `elwreq_rank[].netprps_req` | 순매수잔량 | 20 | 단위: 1주 |
| `elwreq_rank[].trde_prica` | 거래대금 | 20 | 단위: 백만원 |

<a id="ka30011"></a>

## `ka30011` · `proximity_rate()` — ELW근접율요청

ELW근접율요청 (ELW Proximity Rate) · `POST /api/dostk/elw`

```python
api.elw.proximity_rate(stk_cd=...)
```

**요청**

| 필드 | 한글명 | 필수 | 길이 | 설명 |
|---|---|:---:|---:|---|
| `stk_cd` | 종목코드 | Y | 6 |   |

**응답**

| 필드 | 한글명 | 길이 | 설명 |
|---|---|---:|---|
| `elwalacc_rt` (list) | ELW근접율 |  |   |
| `elwalacc_rt[].stk_cd` | 종목코드 | 20 |   |
| `elwalacc_rt[].stk_nm` | 종목명 | 40 |   |
| `elwalacc_rt[].cur_prc` | 현재가 | 20 | 단위: 원, 부호가 포함된 숫자 |
| `elwalacc_rt[].pre_sig` | 대비기호 | 20 | 1: 상한가, 2:상승, 3:보합, 4:하한가, 5:하락 |
| `elwalacc_rt[].pred_pre` | 전일대비 | 20 | 단위: 원, 부호가 포함된 숫자 |
| `elwalacc_rt[].flu_rt` | 등락율 | 20 | 단위: %, 부호 포함 소수점 둘째 자리까지 포맷된 백분율 |
| `elwalacc_rt[].acc_trde_qty` | 누적거래량 | 20 | 단위: 1주 |
| `elwalacc_rt[].alacc_rt` | 근접율 | 20 | 단위: %, 소수점 둘째 자리까지 포맷된 백분율 |

<a id="ka30012"></a>

## `ka30012` · `detailed_stock_info()` — ELW종목상세정보요청

ELW종목상세정보요청 (ELW Detailed Stock Info) · `POST /api/dostk/elw`

```python
api.elw.detailed_stock_info(stk_cd=...)
```

**요청**

| 필드 | 한글명 | 필수 | 길이 | 설명 |
|---|---|:---:|---:|---|
| `stk_cd` | 종목코드 | Y | 6 |   |

**응답**

| 필드 | 한글명 | 길이 | 설명 |
|---|---|---:|---|
| `aset_cd` | 자산코드 | 20 |   |
| `cur_prc` | 현재가 | 20 | 단위: 원, 부호가 포함된 숫자 |
| `pred_pre_sig` | 전일대비기호 | 20 | 1: 상한가, 2:상승, 3:보합, 4:하한가, 5:하락 |
| `pred_pre` | 전일대비 | 20 | 단위: 원, 부호가 포함된 숫자 |
| `flu_rt` | 등락율 | 20 | 단위: %, 부호 포함 소수점 둘째 자리까지 포맷된 백분율 |
| `lpmmcm_nm` | LP회원사명 | 20 |   |
| `lpmmcm_nm_1` | LP회원사명1 | 20 |   |
| `lpmmcm_nm_2` | LP회원사명2 | 20 |   |
| `elwrght_cntn` | ELW권리내용 | 20 |   |
| `elwexpr_evlt_pric` | ELW만기평가가격 | 20 |   |
| `elwtheory_pric` | ELW이론가 | 20 | 소수점 제거 된 100배 값으로 제공 예) "4234322"값은 42,344.22를 의미합니다. |
| `dispty_rt` | 괴리율 | 20 | 단위: %, 부호 포함 소수점 둘째 자리까지 포맷된 백분율 |
| `elwinnr_vltl` | ELW내재변동성 | 20 |   |
| `exp_rght_pric` | 예상권리가 | 20 |   |
| `elwpl_qutr_rt` | ELW손익분기율 | 20 | 단위: %, 부호 포함 소수점 둘째 자리까지 포맷된 백분율 |
| `elwexec_pric` | ELW행사가 | 20 |   |
| `elwcnvt_rt` | ELW전환비율 | 20 | 소수점 넷째 자리까지 포맷된 숫자 |
| `elwcmpn_rt` | ELW보상율 | 20 | 단위: %, 소수점 둘째 자리까지 포맷된 백분율 |
| `elwpric_rising_part_rt` | ELW가격상승참여율 | 20 | 단위: %, 소수점 둘째 자리까지 포맷된 백분율 |
| `elwrght_type` | ELW권리유형 | 20 |   |
| `elwsrvive_dys` | ELW잔존일수 | 20 |   |
| `stkcnt` | 상장주식수 | 20 | 단위: 천원 |
| `elwlpord_pos` | ELWLP주문가능 | 20 |   |
| `lpposs_rt` | LP보유비율 | 20 | 단위: %, 소수점 둘째 자리까지 포맷된 백분율 |
| `lprmnd_qty` | LP보유수량 | 20 | 단위: 1주 |
| `elwspread` | ELW스프레드 | 20 | 소수점 둘째 자리까지 포맷된 숫자 |
| `elwprty` | ELW패리티 | 20 | 소수점 둘째 자리까지 포맷된 숫자 |
| `elwgear` | ELW기어링 | 20 | 소수점 둘째 자리까지 포맷된 숫자 |
| `elwflo_dt` | ELW상장일 | 20 | YYYYMMDD |
| `elwfin_trde_dt` | ELW최종거래일 | 20 | YYYYMMDD |
| `expr_dt` | 만기일 | 20 | YYYYMMDD |
| `exec_dt` | 행사일 | 20 | YYYYMMDD |
| `lpsuply_end_dt` | LP공급종료일 | 20 | YYYYMMDD |
| `elwpay_dt` | ELW지급일 | 20 | YYYYMMDD |
| `elwinvt_ix_comput` | ELW투자지표산출 |  |   |
| `elwpay_agnt` | ELW지급대리인 |  |   |
| `elwappr_way` | ELW결재방법 |  |   |
| `elwrght_exec_way` | ELW권리행사방식 |  |   |
| `elwpblicte_orgn` | ELW발행기관 |  |   |
| `dcsn_pay_amt` | 확정지급액 |  | 소수점 셋째 자리까지 포맷된 숫자 |
| `kobarr` | KO베리어 |  |   |
| `iv` | IV |  | 소수점 셋째 자리까지 포맷된 숫자 |
| `clsprd_end_elwocr` | 종기종료ELW발생 |  |   |
| `bsis_aset_1` | 기초자산1 |  |   |
| `bsis_aset_comp_rt_1` | 기초자산구성비율1 |  | 소수점 셋째 자리까지 포맷된 숫자 |
| `bsis_aset_2` | 기초자산2 |  |   |
| `bsis_aset_comp_rt_2` | 기초자산구성비율2 |  | 소수점 셋째 자리까지 포맷된 숫자 |
| `bsis_aset_3` | 기초자산3 |  |   |
| `bsis_aset_comp_rt_3` | 기초자산구성비율3 |  | 소수점 셋째 자리까지 포맷된 숫자 |
| `bsis_aset_4` | 기초자산4 |  |   |
| `bsis_aset_comp_rt_4` | 기초자산구성비율4 |  | 소수점 셋째 자리까지 포맷된 숫자 |
| `bsis_aset_5` | 기초자산5 |  |   |
| `bsis_aset_comp_rt_5` | 기초자산구성비율5 |  | 소수점 셋째 자리까지 포맷된 숫자 |
| `fr_dt` | 평가시작일자 |  |   |
| `to_dt` | 평가종료일자 |  |   |
| `fr_tm` | 평가시작시간 |  |   |
| `evlt_end_tm` | 평가종료시간 |  |   |
| `evlt_pric` | 평가가격 |  |   |
| `evlt_fnsh_yn` | 평가완료여부 |  |   |
| `all_hgst_pric` | 전체최고가 |  |   |
| `all_lwst_pric` | 전체최저가 |  |   |
| `imaf_hgst_pric` | 직후최고가 |  |   |
| `imaf_lwst_pric` | 직후최저가 |  |   |
| `sndhalf_mrkt_hgst_pric` | 후반장최고가 |  |   |
| `sndhalf_mrkt_lwst_pric` | 후반장최저가 |  |   |
