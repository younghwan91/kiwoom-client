# 호가단위에 맞춘 지정가 주문 (모의투자)

> ⚠️ 이 페이지의 코드는 **주문을 냅니다.** 전부 `is_mock=True`(모의투자)입니다. `is_mock=False` 로 바꾸면 실계좌에서
> 그대로 체결됩니다 — 파이썬 API 에는 이를 막는 장치가 없습니다.

KRX 지정가는 가격대별 **호가단위의 배수**여야 합니다(예: 5만~20만원 구간은 100원). 단위에 맞지 않으면 거부되거나
의도와 다른 가격이 됩니다. `round_to_tick()`(내림) · `round_up_to_tick()`(올림) · `add_ticks()`(n틱 이동)로 맞춥니다.

```python
from kiwoom_client import add_ticks, round_to_tick, tick_size

tick_size(70123)        # Decimal('100')
round_to_tick(70123)    # Decimal('70100') — 매수 지정가는 보통 내림
add_ticks(70100, -2)    # Decimal('69900') — 2틱 아래
```

## 현재가에서 2틱 아래로 매수 → 정정 → 취소

| 단계 | 메서드 | api_id |
|---|---|---|
| 현재가 조회 | `api.stock_info.basic_stock_info()` | `ka10001` |
| 매수 | `api.order.buy_order()` | `kt10000` |
| 정정 | `api.order.modify_order()` | `kt10002` |
| 취소 | `api.order.cancel_order()` | `kt10003` |
| 미체결 확인 | `api.account.unfilled_orders()` | `ka10075` |

```python
from kiwoom_client import KiwoomAPI, add_ticks, round_to_tick, to_number
from kiwoom_client.codes import Exchange, OrderType

api = KiwoomAPI.from_env(is_mock=True)  # 모의투자

code = "005930"
info = api.stock_info.basic_stock_info(stk_cd=code)
last = abs(to_number(info["cur_prc"]))  # 부호는 전일 대비 방향이라 뗀다
price = add_ticks(round_to_tick(last), -2)

order = api.order.buy_order(
    dmst_stex_tp=Exchange.KRX,   # 모의투자는 KRX 만
    stk_cd=code,
    ord_qty="1",
    ord_uv=str(price),
    trde_tp=OrderType.LIMIT,     # "0" 보통(지정가)
)
ord_no = order["ord_no"]
print("주문번호", ord_no, "가격", price)

# 한 틱 올려 정정 — 정정 주문은 새 주문번호를 받는다
modified = api.order.modify_order(
    dmst_stex_tp=Exchange.KRX,
    orig_ord_no=ord_no,
    stk_cd=code,
    mdfy_qty="1",
    mdfy_uv=str(add_ticks(price, 1)),
)

# 남은 수량 전부 취소 (cncl_qty="0" = 잔량 전부)
api.order.cancel_order(
    dmst_stex_tp=Exchange.KRX,
    orig_ord_no=modified["ord_no"],
    stk_cd=code,
    cncl_qty="0",
)

open_orders = api.account.unfilled_orders(all_stk_tp="1", trde_tp="0", stk_cd=code, stex_tp="0")
print(open_orders.get("oso"))
```

- 필드는 공식 스펙 기준입니다: [주문 레퍼런스](../reference/order.md#kt10000). `trde_tp` 전체 값은
  `kiwoom_client.codes.OrderType`([OpenAPI+ 이전 가이드](../migration-from-openapi-plus.md)의 표)에 있습니다.
- 정정·취소 응답의 `ord_no` 는 새 주문번호, `base_orig_ord_no` 는 모주문번호입니다.
- 모의투자 서버가 받지 않는 주문 유형·시간대는 `KiwoomAPIError` 로 올라옵니다. 메시지(`e.message`)에 키움이 이유를 적어 줍니다.
- 주문 TR 도 TR 마다 호출 제한이 있습니다. 빠르게 여러 건을 낼 때는 [호출 제한 다루기](rate-limits.md).
