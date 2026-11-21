# 잔고·평가 요약

계좌 하나의 "총 평가금액 · 손익 · 종목별 보유" 를 한 화면으로. 쓰는 TR:

| TR | 메서드 | 쓰는 값 |
|---|---|---|
| `kt00018` 계좌평가잔고내역요청 | `api.account.evaluation_balance_detail()` | 합계(`tot_pur_amt`·`tot_evlt_amt`·`tot_evlt_pl`·`tot_prft_rt`) + 종목별 리스트 `acnt_evlt_remn_indv_tot` |
| `kt00001` 예수금상세현황요청 | `api.account.deposit_detail()` | `entr` 예수금, `d2_entra` D+2 추정예수금, `ord_alow_amt` 주문가능금액 |

필드 이름·뜻은 공식 스펙 기준입니다 — [계좌 레퍼런스](../reference/account.md#kt00018).

```python
from kiwoom_client import KiwoomAPI, to_dataframe
from kiwoom_client.codes import Exchange


def num(value) -> float | int:
    """'+1,234' · '-000001234' · '12.34' 를 숫자로. 앞자리 0 채움도 금액으로 읽는다."""
    text = str(value).replace(",", "").strip()
    return float(text) if "." in text else int(text or 0)


api = KiwoomAPI.from_env(is_mock=True)

bal = api.account.evaluation_balance_detail(
    qry_tp="1",                 # 1: 합산, 2: 개별
    dmst_stex_tp=Exchange.KRX,  # KRX / NXT
)
dep = api.account.deposit_detail(qry_tp="3")  # 3: 추정조회, 2: 일반조회

print(f"총매입   {num(bal['tot_pur_amt']):>15,}원")
print(f"총평가   {num(bal['tot_evlt_amt']):>15,}원")
print(f"평가손익 {num(bal['tot_evlt_pl']):>15,}원 ({num(bal['tot_prft_rt'])}%)")
print(f"예수금   {num(dep['entr']):>15,}원 · D+2 {num(dep['d2_entra']):,}원 · "
      f"주문가능 {num(dep['ord_alow_amt']):,}원")

holdings = to_dataframe(bal, key="acnt_evlt_remn_indv_tot", numeric=False)
if not holdings.empty:
    amounts = ["rmnd_qty", "pur_pric", "cur_prc", "evlt_amt", "evltv_prft", "prft_rt"]
    holdings[amounts] = holdings[amounts].apply(lambda col: col.map(num))
    print(holdings[["stk_cd", "stk_nm", *amounts]]
          .sort_values("evlt_amt", ascending=False).to_string(index=False))
```

- `to_number()`·`normalize()`·`to_dataframe()` 는 앞자리가 0 으로 채워진 문자열(`"005930"`)을 **코드로 보고
  문자열로 남깁니다.** 금액 필드가 0 으로 채워져 와도 계산이 되게 여기서는 `num()` 으로 직접 바꿨습니다.
- 보유 종목이 많으면 연속조회가 붙습니다 — [연속조회](pagination.md)의 루프에 `evaluation_balance_detail` 을 넣으면 됩니다.
- 모의투자 서버가 지원하지 않는 TR 은 `KiwoomUnsupportedError`(키움 오류 8104)로 올라옵니다.
- 조회 TR 은 주문을 내지 않지만, 실전 계좌를 볼 때는 키를 환경변수로만 넘기고 출력·로그에 계좌번호가 섞이지 않게 하세요.

## 보유 종목 수익률 상위·하위

```python
ranked = holdings.sort_values("prft_rt")
print("하위 3:", ranked.head(3)[["stk_nm", "prft_rt"]].to_dict("records"))
print("상위 3:", ranked.tail(3)[["stk_nm", "prft_rt"]].to_dict("records"))
```
