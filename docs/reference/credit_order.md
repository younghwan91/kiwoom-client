---
seo_title: "키움 REST API 신용주문 TR 요청·응답 필드 — api.credit_order"
description: "키움증권 REST API 신용주문 TR 4개(kt10006·kt10007·kt10008 등)의 요청·응답 필드 ID·한글명·필수·길이와 kiwoom-client 파이썬 호출 예."
---

<!-- 자동 생성 파일 — 손으로 고치지 마세요. `python scripts/gen_docs.py` 가 TR 카탈로그(kiwoom_client.spec)로 다시 만듭니다. -->

# `api.credit_order` — 신용주문 (Credit Order)

요청·응답 필드는 키움 공식 REST API 명세에서 만든 TR 카탈로그([출처·라이선스](https://github.com/younghwan91/kiwoom-client/blob/main/src/kiwoom_client/spec/SOURCE.md))에서 옮긴 필드 ID·한글명·필수·길이입니다. 필드 설명·코드값은 싣지 않으니 [키움 REST API 포털](https://openapi.kiwoom.com) 문서를 보세요(자주 쓰는 코드값은 `kiwoom_client.codes`). 값은 모두 문자열로 넘깁니다.

공통 헤더(`api-id`·`cont-yn`·`next-key`·`authorization`)는 라이브러리가 채웁니다 — 연속조회는 메서드의 `cont_yn`·`next_key` 인자나 `request_all()` 을 쓰세요.

> ⚠️ **실주문 모듈입니다.** `is_mock=False`(기본값)면 실계좌에 주문이 나갑니다.

| api_id | 메서드 | 이름 |
|---|---|---|
| [`kt10006`](#kt10006) | `margin_buy_order()` | 신용 매수주문 |
| [`kt10007`](#kt10007) | `margin_sell_order()` | 신용 매도주문 |
| [`kt10008`](#kt10008) | `margin_modify_order()` | 신용 정정주문 |
| [`kt10009`](#kt10009) | `margin_cancel_order()` | 신용 취소주문 |

<a id="kt10006"></a>

## `kt10006` · `margin_buy_order()` — 신용 매수주문

신용매수주문 (Credit Margin Buy Order) · `POST /api/dostk/crdordr`

```python
api.credit_order.margin_buy_order(dmst_stex_tp=..., stk_cd=..., ord_qty=..., trde_tp=...)
```

**요청**

| 필드 | 한글명 | 필수 | 길이 |
|---|---|:---:|---:|
| `dmst_stex_tp` | 국내거래소구분 | Y | 3 |
| `stk_cd` | 종목코드 | Y | 12 |
| `ord_qty` | 주문수량 | Y | 12 |
| `ord_uv` | 주문단가 |  | 12 |
| `trde_tp` | 매매구분 | Y | 2 |
| `cond_uv` | 조건단가 |  | 12 |

**응답**

| 필드 | 한글명 | 길이 |
|---|---|---:|
| `ord_no` | 주문번호 | 7 |
| `dmst_stex_tp` | 국내거래소구분 | 6 |

<a id="kt10007"></a>

## `kt10007` · `margin_sell_order()` — 신용 매도주문

신용매도주문 (Credit Margin Sell Order) · `POST /api/dostk/crdordr`

```python
api.credit_order.margin_sell_order(dmst_stex_tp=..., stk_cd=..., ord_qty=..., trde_tp=..., crd_deal_tp=...)
```

**요청**

| 필드 | 한글명 | 필수 | 길이 |
|---|---|:---:|---:|
| `dmst_stex_tp` | 국내거래소구분 | Y | 3 |
| `stk_cd` | 종목코드 | Y | 12 |
| `ord_qty` | 주문수량 | Y | 12 |
| `ord_uv` | 주문단가 |  | 12 |
| `trde_tp` | 매매구분 | Y | 2 |
| `crd_deal_tp` | 신용거래구분 | Y | 2 |
| `crd_loan_dt` | 대출일 |  | 8 |
| `cond_uv` | 조건단가 |  | 12 |

**응답**

| 필드 | 한글명 | 길이 |
|---|---|---:|
| `ord_no` | 주문번호 | 7 |
| `dmst_stex_tp` | 국내거래소구분 | 6 |

<a id="kt10008"></a>

## `kt10008` · `margin_modify_order()` — 신용 정정주문

신용정정주문 (Credit Margin Modify Order) · `POST /api/dostk/crdordr`

```python
api.credit_order.margin_modify_order(dmst_stex_tp=..., orig_ord_no=..., stk_cd=..., mdfy_qty=..., mdfy_uv=...)
```

**요청**

| 필드 | 한글명 | 필수 | 길이 |
|---|---|:---:|---:|
| `dmst_stex_tp` | 국내거래소구분 | Y | 3 |
| `orig_ord_no` | 원주문번호 | Y | 7 |
| `stk_cd` | 종목코드 | Y | 12 |
| `mdfy_qty` | 정정수량 | Y | 12 |
| `mdfy_uv` | 정정단가 | Y | 12 |
| `mdfy_cond_uv` | 정정조건단가 |  | 12 |

**응답**

| 필드 | 한글명 | 길이 |
|---|---|---:|
| `ord_no` | 주문번호 | 7 |
| `base_orig_ord_no` | 모주문번호 | 7 |
| `mdfy_qty` | 정정수량 | 12 |
| `dmst_stex_tp` | 국내거래소구분 | 6 |

<a id="kt10009"></a>

## `kt10009` · `margin_cancel_order()` — 신용 취소주문

신용취소주문 (Credit Margin Cancel Order) · `POST /api/dostk/crdordr`

```python
api.credit_order.margin_cancel_order(dmst_stex_tp=..., orig_ord_no=..., stk_cd=..., cncl_qty=...)
```

**요청**

| 필드 | 한글명 | 필수 | 길이 |
|---|---|:---:|---:|
| `dmst_stex_tp` | 국내거래소구분 | Y | 3 |
| `orig_ord_no` | 원주문번호 | Y | 7 |
| `stk_cd` | 종목코드 | Y | 12 |
| `cncl_qty` | 취소수량 | Y | 12 |

**응답**

| 필드 | 한글명 | 길이 |
|---|---|---:|
| `ord_no` | 주문번호 | 7 |
| `base_orig_ord_no` | 모주문번호 | 7 |
| `cncl_qty` | 취소수량 | 12 |
