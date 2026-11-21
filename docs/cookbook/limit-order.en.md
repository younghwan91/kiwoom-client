# Tick-aligned limit orders (mock trading)

> ⚠️ The code on this page **places orders.** All of it uses `is_mock=True` (mock trading). Switch to `is_mock=False`
> and it fills on your real account as is — the Python API has nothing that blocks it.

A KRX limit price must be a **multiple of the tick size** (호가단위) for its price band (for example, 100 won in the
50,000–200,000 won band). A price off the tick is rejected or ends up at a price you did not intend. Align it with
`round_to_tick()` (round down) · `round_up_to_tick()` (round up) · `add_ticks()` (move n ticks).

```python
from kiwoom_client import add_ticks, round_to_tick, tick_size

tick_size(70123)        # Decimal('100')
round_to_tick(70123)    # Decimal('70100') — buy limits usually round down
add_ticks(70100, -2)    # Decimal('69900') — two ticks below
```

## Buy two ticks below the current price → modify → cancel

| Step | Method | api_id |
|---|---|---|
| Get the current price | `api.stock_info.basic_stock_info()` | `ka10001` |
| Buy | `api.order.buy_order()` | `kt10000` |
| Modify | `api.order.modify_order()` | `kt10002` |
| Cancel | `api.order.cancel_order()` | `kt10003` |
| Check open orders | `api.account.unfilled_orders()` | `ka10075` |

```python
from kiwoom_client import KiwoomAPI, add_ticks, round_to_tick, to_number
from kiwoom_client.codes import Exchange, OrderType

api = KiwoomAPI.from_env(is_mock=True)  # mock trading

code = "005930"
info = api.stock_info.basic_stock_info(stk_cd=code)
last = abs(to_number(info["cur_prc"]))  # the sign is the direction vs. the previous close, so drop it
price = add_ticks(round_to_tick(last), -2)

order = api.order.buy_order(
    dmst_stex_tp=Exchange.KRX,   # mock trading supports KRX only
    stk_cd=code,
    ord_qty="1",
    ord_uv=str(price),
    trde_tp=OrderType.LIMIT,     # "0" normal (limit)
)
ord_no = order["ord_no"]
print("order no.", ord_no, "price", price)

# Modify one tick up — a modify order gets a new order number
modified = api.order.modify_order(
    dmst_stex_tp=Exchange.KRX,
    orig_ord_no=ord_no,
    stk_cd=code,
    mdfy_qty="1",
    mdfy_uv=str(add_ticks(price, 1)),
)

# Cancel the whole remaining quantity (cncl_qty="0" = everything left)
api.order.cancel_order(
    dmst_stex_tp=Exchange.KRX,
    orig_ord_no=modified["ord_no"],
    stk_cd=code,
    cncl_qty="0",
)

open_orders = api.account.unfilled_orders(all_stk_tp="1", trde_tp="0", stk_cd=code, stex_tp="0")
print(open_orders.get("oso"))
```

- Fields follow the official spec: [order reference](../reference/order.md#kt10000). Every `trde_tp` value is in
  `kiwoom_client.codes.OrderType` (the table in the [OpenAPI+ migration guide](../migration-from-openapi-plus.md)).
- In modify and cancel responses, `ord_no` is the new order number and `base_orig_ord_no` the original order number.
- Order types and hours the mock-trading server does not accept come back as `KiwoomAPIError`. Kiwoom puts the reason
  in the message (`e.message`).
- Order TRs have per-TR rate limits too. When placing many orders quickly, see
  [handling rate limits](rate-limits.md) (Korean).
