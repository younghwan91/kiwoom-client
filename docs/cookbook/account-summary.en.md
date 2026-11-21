# Account balance and valuation summary

An account's "total valuation · profit and loss · holdings by stock" on one screen. The TRs used:

| TR | Method | Values used |
|---|---|---|
| `kt00018` account evaluation balance detail (계좌평가잔고내역요청) | `api.account.evaluation_balance_detail()` | Totals (`tot_pur_amt` · `tot_evlt_amt` · `tot_evlt_pl` · `tot_prft_rt`) + the per-stock list `acnt_evlt_remn_indv_tot` |
| `kt00001` deposit detail (예수금상세현황요청) | `api.account.deposit_detail()` | `entr` deposit (예수금), `d2_entra` estimated D+2 deposit, `ord_alow_amt` orderable amount |

Field names and meanings follow the official spec — [account reference](../reference/account.md#kt00018).

```python
from kiwoom_client import KiwoomAPI, to_dataframe
from kiwoom_client.codes import Exchange


def num(value) -> float | int:
    """'+1,234' · '-000001234' · '12.34' to a number. Zero-padded strings are read as amounts too."""
    text = str(value).replace(",", "").strip()
    return float(text) if "." in text else int(text or 0)


api = KiwoomAPI.from_env(is_mock=True)

bal = api.account.evaluation_balance_detail(
    qry_tp="1",                 # 1: combined, 2: individual
    dmst_stex_tp=Exchange.KRX,  # KRX / NXT
)
dep = api.account.deposit_detail(qry_tp="3")  # 3: estimated, 2: normal

print(f"Purchased  {num(bal['tot_pur_amt']):>15,} KRW")
print(f"Valuation  {num(bal['tot_evlt_amt']):>15,} KRW")
print(f"P&L        {num(bal['tot_evlt_pl']):>15,} KRW ({num(bal['tot_prft_rt'])}%)")
print(f"Deposit    {num(dep['entr']):>15,} KRW · D+2 {num(dep['d2_entra']):,} KRW · "
      f"orderable {num(dep['ord_alow_amt']):,} KRW")

holdings = to_dataframe(bal, key="acnt_evlt_remn_indv_tot", numeric=False)
if not holdings.empty:
    amounts = ["rmnd_qty", "pur_pric", "cur_prc", "evlt_amt", "evltv_prft", "prft_rt"]
    holdings[amounts] = holdings[amounts].apply(lambda col: col.map(num))
    print(holdings[["stk_cd", "stk_nm", *amounts]]
          .sort_values("evlt_amt", ascending=False).to_string(index=False))
```

- `to_number()` · `normalize()` · `to_dataframe()` treat zero-padded strings (`"005930"`) as **codes and leave them as
  strings.** So that amount fields still compute when they arrive zero-padded, this example converts them itself with
  `num()`.
- With many holdings a continuation query kicks in — put `evaluation_balance_detail` into the loop from
  [pagination](pagination.md).
- TRs the mock-trading server does not support come back as `KiwoomUnsupportedError` (Kiwoom error 8104).
- Query TRs do not place orders, but when looking at a live account pass the keys only through environment variables
  and keep account numbers out of your output and logs.

## Best and worst holdings by return

```python
ranked = holdings.sort_values("prft_rt")
print("bottom 3:", ranked.head(3)[["stk_nm", "prft_rt"]].to_dict("records"))
print("top 3:", ranked.tail(3)[["stk_nm", "prft_rt"]].to_dict("records"))
```
