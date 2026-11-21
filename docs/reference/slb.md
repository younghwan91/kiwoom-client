<!-- 자동 생성 파일 — 손으로 고치지 마세요. `python scripts/gen_docs.py` 가 TR 카탈로그(kiwoom_client.spec)로 다시 만듭니다. -->

# `api.slb` — 대차거래 (Stock Lending & Borrowing)

요청·응답 필드는 키움 공식 REST API 명세에서 만든 TR 카탈로그([출처·라이선스](https://github.com/younghwan91/kiwoom-client/blob/main/src/kiwoom_client/spec/SOURCE.md))를 그대로 옮긴 것입니다. 뜻이 애매하면 [키움 REST API 포털](https://openapi.kiwoom.com)이 기준입니다. 값은 모두 문자열로 넘깁니다.

공통 헤더(`api-id`·`cont-yn`·`next-key`·`authorization`)는 라이브러리가 채웁니다 — 연속조회는 메서드의 `cont_yn`·`next_key` 인자나 `request_all()` 을 쓰세요.

| api_id | 메서드 | 이름 |
|---|---|---|
| [`ka10068`](#ka10068) | `lending_trend()` | 대차거래추이요청 |
| [`ka10069`](#ka10069) | `top10_lending()` | 대차거래상위10종목요청 |
| [`ka20068`](#ka20068) | `lending_trend_by_stock()` | 대차거래추이요청(종목별) |
| [`ka90012`](#ka90012) | `lending_details()` | 대차거래내역요청 |

<a id="ka10068"></a>

## `ka10068` · `lending_trend()` — 대차거래추이요청

대차거래추이요청 (Lending Trend) · `POST /api/dostk/slb`

```python
api.slb.lending_trend(all_tp=...)
```

**요청**

| 필드 | 한글명 | 필수 | 길이 | 설명 |
|---|---|:---:|---:|---|
| `strt_dt` | 시작일자 |  | 8 | YYYYMMDD |
| `end_dt` | 종료일자 |  | 8 | YYYYMMDD |
| `all_tp` | 전체구분 | Y | 6 | 1: 전체표시 |

**응답**

| 필드 | 한글명 | 길이 | 설명 |
|---|---|---:|---|
| `dbrt_trde_trnsn` (list) | 대차거래추이 |  |   |
| `dbrt_trde_trnsn[].dt` | 일자 | 8 | YYYYMMDD |
| `dbrt_trde_trnsn[].dbrt_trde_cntrcnt` | 대차거래체결주수 | 12 | 단위: 1주 |
| `dbrt_trde_trnsn[].dbrt_trde_rpy` | 대차거래상환주수 | 18 | 단위: 1주 |
| `dbrt_trde_trnsn[].dbrt_trde_irds` | 대차거래증감 | 60 | 단위: 1주 |
| `dbrt_trde_trnsn[].rmnd` | 잔고주수 | 18 | 단위: 1주 |
| `dbrt_trde_trnsn[].remn_amt` | 잔고금액 | 18 | 단위: 백만원 |

<a id="ka10069"></a>

## `ka10069` · `top10_lending()` — 대차거래상위10종목요청

대차거래상위10종목요청 (Top 10 Lending Stocks) · `POST /api/dostk/slb`

```python
api.slb.top10_lending(strt_dt=..., mrkt_tp=...)
```

**요청**

| 필드 | 한글명 | 필수 | 길이 | 설명 |
|---|---|:---:|---:|---|
| `strt_dt` | 시작일자 | Y | 8 | YYYYMMDD (연도4자리, 월 2자리, 일 2자리 형식) |
| `end_dt` | 종료일자 |  | 8 | YYYYMMDD (연도4자리, 월 2자리, 일 2자리 형식) |
| `mrkt_tp` | 시장구분 | Y | 3 | 001:코스피, 101:코스닥 |

**응답**

| 필드 | 한글명 | 길이 | 설명 |
|---|---|---:|---|
| `dbrt_trde_cntrcnt_sum` | 대차거래체결주수합 |  | 단위: 1주 |
| `dbrt_trde_rpy_sum` | 대차거래상환주수합 |  | 단위: 1주 |
| `rmnd_sum` | 잔고주수합 |  | 단위: 1주 |
| `remn_amt_sum` | 잔고금액합 |  | 단위: 백만원 |
| `dbrt_trde_cntrcnt_rt` | 대차거래체결주수비율 |  | 소수점 제거 된 100배 값으로 제공 예) "2658"는 26.58%를 의미합니다. |
| `dbrt_trde_rpy_rt` | 대차거래상환주수비율 |  | 소수점 제거 된 100배 값으로 제공 예) "2658"는 26.58%를 의미합니다. |
| `rmnd_rt` | 잔고주수비율 |  | 소수점 제거 된 100배 값으로 제공 예) "2658"는 26.58%를 의미합니다. |
| `remn_amt_rt` | 잔고금액비율 |  | 소수점 제거 된 100배 값으로 제공 예) "2658"는 26.58%를 의미합니다. |
| `dbrt_trde_upper_10stk` (list) | 대차거래상위10종목 |  |   |
| `dbrt_trde_upper_10stk[].stk_nm` | 종목명 | 40 |   |
| `dbrt_trde_upper_10stk[].stk_cd` | 종목코드 | 20 |   |
| `dbrt_trde_upper_10stk[].dbrt_trde_cntrcnt` | 대차거래체결주수 | 20 | 단위: 1주 |
| `dbrt_trde_upper_10stk[].dbrt_trde_rpy` | 대차거래상환주수 | 20 | 단위: 1주 |
| `dbrt_trde_upper_10stk[].rmnd` | 잔고주수 | 20 | 단위: 1주 |
| `dbrt_trde_upper_10stk[].remn_amt` | 잔고금액 | 20 | 단위: 백만원 |

<a id="ka20068"></a>

## `ka20068` · `lending_trend_by_stock()` — 대차거래추이요청(종목별)

대차거래추이요청종목별 (Lending Trend by Stock) · `POST /api/dostk/slb`

```python
api.slb.lending_trend_by_stock(stk_cd=...)
```

**요청**

| 필드 | 한글명 | 필수 | 길이 | 설명 |
|---|---|:---:|---:|---|
| `strt_dt` | 시작일자 |  | 8 | YYYYMMDD |
| `end_dt` | 종료일자 |  | 8 | YYYYMMDD |
| `all_tp` | 전체구분 |  | 1 | 0:종목코드 입력종목만 표시 |
| `stk_cd` | 종목코드 | Y | 6 |   |

**응답**

| 필드 | 한글명 | 길이 | 설명 |
|---|---|---:|---|
| `dbrt_trde_trnsn` (list) | 대차거래추이 |  |   |
| `dbrt_trde_trnsn[].dt` | 일자 | 20 | YYYYMMDD |
| `dbrt_trde_trnsn[].dbrt_trde_cntrcnt` | 대차거래체결주수 | 20 | 단위: 1주 |
| `dbrt_trde_trnsn[].dbrt_trde_rpy` | 대차거래상환주수 | 20 | 단위: 1주 |
| `dbrt_trde_trnsn[].dbrt_trde_irds` | 대차거래증감 | 20 | 단위: 1주 |
| `dbrt_trde_trnsn[].rmnd` | 잔고주수 | 20 | 단위: 1주 |
| `dbrt_trde_trnsn[].remn_amt` | 잔고금액 | 20 | 단위: 백만원 |

<a id="ka90012"></a>

## `ka90012` · `lending_details()` — 대차거래내역요청

대차거래내역요청 (Lending Details) · `POST /api/dostk/slb`

```python
api.slb.lending_details(dt=..., mrkt_tp=...)
```

**요청**

| 필드 | 한글명 | 필수 | 길이 | 설명 |
|---|---|:---:|---:|---|
| `dt` | 일자 | Y | 8 | YYYYMMDD |
| `mrkt_tp` | 시장구분 | Y | 3 | 001:코스피, 101:코스닥 |

**응답**

| 필드 | 한글명 | 길이 | 설명 |
|---|---|---:|---|
| `dbrt_trde_prps` (list) | 대차거래내역 |  |   |
| `dbrt_trde_prps[].stk_nm` | 종목명 | 40 |   |
| `dbrt_trde_prps[].stk_cd` | 종목코드 | 20 |   |
| `dbrt_trde_prps[].dbrt_trde_cntrcnt` | 대차거래체결주수 | 20 | 단위: 1주 |
| `dbrt_trde_prps[].dbrt_trde_rpy` | 대차거래상환주수 | 20 | 단위: 1주 |
| `dbrt_trde_prps[].rmnd` | 잔고주수 | 20 | 단위: 1주 |
| `dbrt_trde_prps[].remn_amt` | 잔고금액 | 20 | 단위: 백만원 |
