<!-- 자동 생성 파일 — 손으로 고치지 마세요. `python scripts/gen_docs.py` 가 TR 카탈로그(kiwoom_client.spec)로 다시 만듭니다. -->

# `api.credit_order` — 신용주문 (Credit Order)

요청·응답 필드는 키움 공식 REST API 명세에서 만든 TR 카탈로그([출처·라이선스](https://github.com/younghwan91/kiwoom-client/blob/main/src/kiwoom_client/spec/SOURCE.md))를 그대로 옮긴 것입니다. 뜻이 애매하면 [키움 REST API 포털](https://openapi.kiwoom.com)이 기준입니다. 값은 모두 문자열로 넘깁니다.

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

| 필드 | 한글명 | 필수 | 길이 | 설명 |
|---|---|:---:|---:|---|
| `dmst_stex_tp` | 국내거래소구분 | Y | 3 | KRX,NXT,SOR |
| `stk_cd` | 종목코드 | Y | 12 |   |
| `ord_qty` | 주문수량 | Y | 12 | 단위: 1주 |
| `ord_uv` | 주문단가 |  | 12 | 단위: 원 |
| `trde_tp` | 매매구분 | Y | 2 | 0:보통 , 3:시장가 , 5:조건부지정가 , 81:장마감후시간외 , 61:장시작전시간외, 62:시간외단일가 , 6:최유리지정가 , 7:최우선지정가 , 10:보통(IOC) , 13:시장가(IOC) , 16:최유리(IOC) , 20:보통(FOK) , 23:시장가(FOK) , 26:최유리(FOK) , 28:스톱지정가,29:중간가,30:중간가(IOC),31:중간가(FOK) |
| `cond_uv` | 조건단가 |  | 12 | 단위: 원 |

**응답**

| 필드 | 한글명 | 길이 | 설명 |
|---|---|---:|---|
| `ord_no` | 주문번호 | 7 | 7자리 주문번호 |
| `dmst_stex_tp` | 국내거래소구분 | 6 | KRX, NXT, SOR |

<a id="kt10007"></a>

## `kt10007` · `margin_sell_order()` — 신용 매도주문

신용매도주문 (Credit Margin Sell Order) · `POST /api/dostk/crdordr`

```python
api.credit_order.margin_sell_order(dmst_stex_tp=..., stk_cd=..., ord_qty=..., trde_tp=..., crd_deal_tp=...)
```

**요청**

| 필드 | 한글명 | 필수 | 길이 | 설명 |
|---|---|:---:|---:|---|
| `dmst_stex_tp` | 국내거래소구분 | Y | 3 | KRX,NXT,SOR |
| `stk_cd` | 종목코드 | Y | 12 |   |
| `ord_qty` | 주문수량 | Y | 12 | 단위: 1주 |
| `ord_uv` | 주문단가 |  | 12 | 단위: 원 |
| `trde_tp` | 매매구분 | Y | 2 | 0:보통 , 3:시장가 , 5:조건부지정가 , 81:장마감후시간외 , 61:장시작전시간외, 62:시간외단일가 , 6:최유리지정가 , 7:최우선지정가 , 10:보통(IOC) , 13:시장가(IOC) , 16:최유리(IOC) , 20:보통(FOK) , 23:시장가(FOK) , 26:최유리(FOK) , 28:스톱지정가,29:중간가,30:중간가(IOC),31:중간가(FOK) |
| `crd_deal_tp` | 신용거래구분 | Y | 2 | 33:융자 , 99:융자합 |
| `crd_loan_dt` | 대출일 |  | 8 | YYYYMMDD(융자일경우필수) |
| `cond_uv` | 조건단가 |  | 12 | 단위: 원 |

**응답**

| 필드 | 한글명 | 길이 | 설명 |
|---|---|---:|---|
| `ord_no` | 주문번호 | 7 | 7자리 주문번호 |
| `dmst_stex_tp` | 국내거래소구분 | 6 | KRX, NXT, SOR |

<a id="kt10008"></a>

## `kt10008` · `margin_modify_order()` — 신용 정정주문

신용정정주문 (Credit Margin Modify Order) · `POST /api/dostk/crdordr`

```python
api.credit_order.margin_modify_order(dmst_stex_tp=..., orig_ord_no=..., stk_cd=..., mdfy_qty=..., mdfy_uv=...)
```

**요청**

| 필드 | 한글명 | 필수 | 길이 | 설명 |
|---|---|:---:|---:|---|
| `dmst_stex_tp` | 국내거래소구분 | Y | 3 | KRX,NXT,SOR |
| `orig_ord_no` | 원주문번호 | Y | 7 | 매수/매도 주문 요청 응답 결과로 받은 7자리 주문번호 |
| `stk_cd` | 종목코드 | Y | 12 |   |
| `mdfy_qty` | 정정수량 | Y | 12 | 단위: 1주, '0' 입력시 잔량 전부 정정 |
| `mdfy_uv` | 정정단가 | Y | 12 | 단위: 원 |
| `mdfy_cond_uv` | 정정조건단가 |  | 12 | 단위: 원 |

**응답**

| 필드 | 한글명 | 길이 | 설명 |
|---|---|---:|---|
| `ord_no` | 주문번호 | 7 | 새 주문번호 |
| `base_orig_ord_no` | 모주문번호 | 7 | 원 주문번호 |
| `mdfy_qty` | 정정수량 | 12 | 단위: 1주, 좌측 0-padding 처리된 부호 포함 12자리 숫자 |
| `dmst_stex_tp` | 국내거래소구분 | 6 | KRX, NXT, SOR |

<a id="kt10009"></a>

## `kt10009` · `margin_cancel_order()` — 신용 취소주문

신용취소주문 (Credit Margin Cancel Order) · `POST /api/dostk/crdordr`

```python
api.credit_order.margin_cancel_order(dmst_stex_tp=..., orig_ord_no=..., stk_cd=..., cncl_qty=...)
```

**요청**

| 필드 | 한글명 | 필수 | 길이 | 설명 |
|---|---|:---:|---:|---|
| `dmst_stex_tp` | 국내거래소구분 | Y | 3 | KRX,NXT,SOR |
| `orig_ord_no` | 원주문번호 | Y | 7 | 매수/매도 주문 요청 응답 결과로 받은 7자리 주문번호 |
| `stk_cd` | 종목코드 | Y | 12 |   |
| `cncl_qty` | 취소수량 | Y | 12 | 단위: 1주, '0' 입력시 잔량 전부 취소 |

**응답**

| 필드 | 한글명 | 길이 | 설명 |
|---|---|---:|---|
| `ord_no` | 주문번호 | 7 | 새 주문번호 |
| `base_orig_ord_no` | 모주문번호 | 7 | 원 주문번호 |
| `cncl_qty` | 취소수량 | 12 | 단위: 1주, 좌측 0-padding 처리된 부호 포함 12자리 숫자 |
