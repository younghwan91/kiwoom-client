---
seo_title: "키움 REST API 공매도 TR 요청·응답 필드 — api.short_selling"
description: "키움증권 REST API 공매도 TR 1개(ka10014)의 요청·응답 필드 ID·한글명·필수·길이와 kiwoom-client 파이썬 호출 예."
---

<!-- 자동 생성 파일 — 손으로 고치지 마세요. `python scripts/gen_docs.py` 가 TR 카탈로그(kiwoom_client.spec)로 다시 만듭니다. -->

# `api.short_selling` — 공매도 (Short Selling)

요청·응답 필드는 키움 공식 REST API 명세에서 만든 TR 카탈로그([출처·라이선스](https://github.com/younghwan91/kiwoom-client/blob/main/src/kiwoom_client/spec/SOURCE.md))에서 옮긴 필드 ID·한글명·필수·길이입니다. 필드 설명·코드값은 싣지 않으니 [키움 REST API 포털](https://openapi.kiwoom.com) 문서를 보세요(자주 쓰는 코드값은 `kiwoom_client.codes`). 값은 모두 문자열로 넘깁니다.

공통 헤더(`api-id`·`cont-yn`·`next-key`·`authorization`)는 라이브러리가 채웁니다 — 연속조회는 메서드의 `cont_yn`·`next_key` 인자나 `request_all()` 을 쓰세요.

| api_id | 메서드 | 이름 |
|---|---|---|
| [`ka10014`](#ka10014) | `short_selling_trend()` | 공매도추이요청 |

<a id="ka10014"></a>

## `ka10014` · `short_selling_trend()` — 공매도추이요청

공매도추이요청 (Short Selling Trend) · `POST /api/dostk/shsa`

```python
api.short_selling.short_selling_trend(stk_cd=..., strt_dt=..., end_dt=...)
```

**요청**

| 필드 | 한글명 | 필수 | 길이 |
|---|---|:---:|---:|
| `stk_cd` | 종목코드 | Y | 20 |
| `tm_tp` | 시간구분 |  | 1 |
| `strt_dt` | 시작일자 | Y | 8 |
| `end_dt` | 종료일자 | Y | 8 |

**응답**

| 필드 | 한글명 | 길이 |
|---|---|---:|
| `shrts_trnsn` (list) | 공매도추이 |  |
| `shrts_trnsn[].dt` | 일자 | 20 |
| `shrts_trnsn[].close_pric` | 종가 | 20 |
| `shrts_trnsn[].pred_pre_sig` | 전일대비기호 | 20 |
| `shrts_trnsn[].pred_pre` | 전일대비 | 20 |
| `shrts_trnsn[].flu_rt` | 등락율 | 20 |
| `shrts_trnsn[].trde_qty` | 거래량 | 20 |
| `shrts_trnsn[].shrts_qty` | 공매도량 | 20 |
| `shrts_trnsn[].ovr_shrts_qty` | 누적공매도량 | 20 |
| `shrts_trnsn[].trde_wght` | 매매비중 | 20 |
| `shrts_trnsn[].shrts_trde_prica` | 공매도거래대금 | 20 |
| `shrts_trnsn[].shrts_avg_pric` | 공매도평균가 | 20 |
