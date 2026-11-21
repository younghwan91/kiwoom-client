---
seo_title: "키움 REST API 주문 TR 요청·응답 필드 — api.order"
description: "키움증권 REST API 주문 TR 8개(kt10000·kt10001·kt10002 등)의 요청·응답 필드 ID·한글명·필수·길이와 kiwoom-client 파이썬 호출 예."
---

<!-- 자동 생성 파일 — 손으로 고치지 마세요. `python scripts/gen_docs.py` 가 TR 카탈로그(kiwoom_client.spec)로 다시 만듭니다. -->

# `api.order` — 주문 (Order)

요청·응답 필드는 키움 공식 REST API 명세에서 만든 TR 카탈로그([출처·라이선스](https://github.com/younghwan91/kiwoom-client/blob/main/src/kiwoom_client/spec/SOURCE.md))에서 옮긴 필드 ID·한글명·필수·길이입니다. 필드 설명·코드값은 싣지 않으니 [키움 REST API 포털](https://openapi.kiwoom.com) 문서를 보세요(자주 쓰는 코드값은 `kiwoom_client.codes`). 값은 모두 문자열로 넘깁니다.

공통 헤더(`api-id`·`cont-yn`·`next-key`·`authorization`)는 라이브러리가 채웁니다 — 연속조회는 메서드의 `cont_yn`·`next_key` 인자나 `request_all()` 을 쓰세요.

> ⚠️ **실주문 모듈입니다.** `is_mock=False`(기본값)면 실계좌에 주문이 나갑니다.

| api_id | 메서드 | 이름 |
|---|---|---|
| [`kt10000`](#kt10000) | `buy_order()` | 주식 매수주문 |
| [`kt10001`](#kt10001) | `sell_order()` | 주식 매도주문 |
| [`kt10002`](#kt10002) | `modify_order()` | 주식 정정주문 |
| [`kt10003`](#kt10003) | `cancel_order()` | 주식 취소주문 |
| [`kt50000`](#kt50000) | `gold_spot_buy_order()` | 금현물 매수주문 |
| [`kt50001`](#kt50001) | `gold_spot_sell_order()` | 금현물 매도주문 |
| [`kt50002`](#kt50002) | `gold_spot_modify_order()` | 금현물 정정주문 |
| [`kt50003`](#kt50003) | `gold_spot_cancel_order()` | 금현물 취소주문 |

<a id="kt10000"></a>

## `kt10000` · `buy_order()` — 주식 매수주문

주식매수주문 (Stock Buy Order) · `POST /api/dostk/ordr`

```python
api.order.buy_order(dmst_stex_tp=..., stk_cd=..., ord_qty=..., trde_tp=...)
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

<a id="kt10001"></a>

## `kt10001` · `sell_order()` — 주식 매도주문

주식매도주문 (Stock Sell Order) · `POST /api/dostk/ordr`

```python
api.order.sell_order(dmst_stex_tp=..., stk_cd=..., ord_qty=..., trde_tp=...)
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

<a id="kt10002"></a>

## `kt10002` · `modify_order()` — 주식 정정주문

주식정정주문 (Stock Modify Order) · `POST /api/dostk/ordr`

```python
api.order.modify_order(dmst_stex_tp=..., orig_ord_no=..., stk_cd=..., mdfy_qty=..., mdfy_uv=...)
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

<a id="kt10003"></a>

## `kt10003` · `cancel_order()` — 주식 취소주문

주식취소주문 (Stock Cancel Order) · `POST /api/dostk/ordr`

```python
api.order.cancel_order(dmst_stex_tp=..., orig_ord_no=..., stk_cd=..., cncl_qty=...)
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

<a id="kt50000"></a>

## `kt50000` · `gold_spot_buy_order()` — 금현물 매수주문

금현물 매수주문 (Gold Spot Buy Order) · `POST /api/dostk/ordr`

```python
api.order.gold_spot_buy_order(stk_cd=..., ord_qty=..., trde_tp=...)
```

**요청**

| 필드 | 한글명 | 필수 | 길이 |
|---|---|:---:|---:|
| `stk_cd` | 종목코드 | Y | 12 |
| `ord_qty` | 주문수량 | Y | 12 |
| `ord_uv` | 주문단가 |  | 12 |
| `trde_tp` | 매매구분 | Y | 2 |

**응답**

| 필드 | 한글명 | 길이 |
|---|---|---:|
| `ord_no` | 주문번호 | 7 |

<a id="kt50001"></a>

## `kt50001` · `gold_spot_sell_order()` — 금현물 매도주문

금현물 매도주문 (Gold Spot Sell Order) · `POST /api/dostk/ordr`

```python
api.order.gold_spot_sell_order(stk_cd=..., ord_qty=..., trde_tp=...)
```

**요청**

| 필드 | 한글명 | 필수 | 길이 |
|---|---|:---:|---:|
| `stk_cd` | 종목코드 | Y | 12 |
| `ord_qty` | 주문수량 | Y | 12 |
| `ord_uv` | 주문단가 |  | 12 |
| `trde_tp` | 매매구분 | Y | 2 |

**응답**

| 필드 | 한글명 | 길이 |
|---|---|---:|
| `ord_no` | 주문번호 | 7 |

<a id="kt50002"></a>

## `kt50002` · `gold_spot_modify_order()` — 금현물 정정주문

금현물 정정주문 (Gold Spot Modify Order) · `POST /api/dostk/ordr`

```python
api.order.gold_spot_modify_order(stk_cd=..., orig_ord_no=..., mdfy_qty=..., mdfy_uv=...)
```

**요청**

| 필드 | 한글명 | 필수 | 길이 |
|---|---|:---:|---:|
| `stk_cd` | 종목코드 | Y | 12 |
| `orig_ord_no` | 원주문번호 | Y | 7 |
| `mdfy_qty` | 정정수량 | Y | 12 |
| `mdfy_uv` | 정정단가 | Y | 12 |

**응답**

| 필드 | 한글명 | 길이 |
|---|---|---:|
| `ord_no` | 주문번호 | 7 |
| `base_orig_ord_no` | 모주문번호 | 7 |
| `mdfy_qty` | 정정수량 | 12 |

<a id="kt50003"></a>

## `kt50003` · `gold_spot_cancel_order()` — 금현물 취소주문

금현물 취소주문 (Gold Spot Cancel Order) · `POST /api/dostk/ordr`

```python
api.order.gold_spot_cancel_order(orig_ord_no=..., stk_cd=..., cncl_qty=...)
```

**요청**

| 필드 | 한글명 | 필수 | 길이 |
|---|---|:---:|---:|
| `orig_ord_no` | 원주문번호 | Y | 7 |
| `stk_cd` | 종목코드 | Y | 12 |
| `cncl_qty` | 취소수량 | Y | 12 |

**응답**

| 필드 | 한글명 | 길이 |
|---|---|---:|
| `ord_no` | 주문번호 | 7 |
| `base_orig_ord_no` | 모주문번호 | 7 |
| `cncl_qty` | 취소수량 | 12 |
