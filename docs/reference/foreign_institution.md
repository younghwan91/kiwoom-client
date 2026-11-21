<!-- 자동 생성 파일 — 손으로 고치지 마세요. `python scripts/gen_docs.py` 가 TR 카탈로그(kiwoom_client.spec)로 다시 만듭니다. -->

# `api.foreign_institution` — 기관/외국인 (Foreign/Institution)

요청·응답 필드는 키움 공식 REST API 명세에서 만든 TR 카탈로그([출처·라이선스](https://github.com/younghwan91/kiwoom-client/blob/main/src/kiwoom_client/spec/SOURCE.md))에서 옮긴 필드 ID·한글명·필수·길이입니다. 필드 설명·코드값은 싣지 않으니 [키움 REST API 포털](https://openapi.kiwoom.com) 문서를 보세요(자주 쓰는 코드값은 `kiwoom_client.codes`). 값은 모두 문자열로 넘깁니다.

공통 헤더(`api-id`·`cont-yn`·`next-key`·`authorization`)는 라이브러리가 채웁니다 — 연속조회는 메서드의 `cont_yn`·`next_key` 인자나 `request_all()` 을 쓰세요.

| api_id | 메서드 | 이름 |
|---|---|---|
| [`ka10008`](#ka10008) | `foreign_trading_trend()` | 주식외국인종목별매매동향 |
| [`ka10009`](#ka10009) | `institutional_stock()` | 주식기관요청 |
| [`ka10131`](#ka10131) | `consecutive_trading_status()` | 기관외국인연속매매현황요청 |
| [`ka52301`](#ka52301) | `gold_spot_investor_status()` | 금현물투자자현황 |

<a id="ka10008"></a>

## `ka10008` · `foreign_trading_trend()` — 주식외국인종목별매매동향

주식외국인종목별매매동향 (Foreign Trading Trend by Stock) · `POST /api/dostk/frgnistt`

```python
api.foreign_institution.foreign_trading_trend(stk_cd=...)
```

**요청**

| 필드 | 한글명 | 필수 | 길이 |
|---|---|:---:|---:|
| `stk_cd` | 종목코드 | Y | 20 |

**응답**

| 필드 | 한글명 | 길이 |
|---|---|---:|
| `stk_frgnr` (list) | 주식외국인 |  |
| `stk_frgnr[].dt` | 일자 | 20 |
| `stk_frgnr[].close_pric` | 종가 | 20 |
| `stk_frgnr[].pred_pre` | 전일대비 | 20 |
| `stk_frgnr[].trde_qty` | 거래량 | 20 |
| `stk_frgnr[].chg_qty` | 변동수량 | 20 |
| `stk_frgnr[].poss_stkcnt` | 보유주식수 | 20 |
| `stk_frgnr[].wght` | 비중 | 20 |
| `stk_frgnr[].gain_pos_stkcnt` | 취득가능주식수 | 20 |
| `stk_frgnr[].frgnr_limit` | 외국인한도 | 20 |
| `stk_frgnr[].frgnr_limit_irds` | 외국인한도증감 | 20 |
| `stk_frgnr[].limit_exh_rt` | 한도소진률 | 20 |

<a id="ka10009"></a>

## `ka10009` · `institutional_stock()` — 주식기관요청

주식기관요청 (Institutional Stock) · `POST /api/dostk/frgnistt`

```python
api.foreign_institution.institutional_stock(stk_cd=...)
```

> 출처 `repo`: 현재 공식 명세(SOURCE_COMMIT)에 없다. 요청 필드는 tests/integration_api_smoke.py 표 기준이고 응답 필드는 미확인.

**요청**

| 필드 | 한글명 | 필수 | 길이 |
|---|---|:---:|---:|
| `stk_cd` | 종목코드 | Y | 20 |

**응답**

응답 필드 미확인.

<a id="ka10131"></a>

## `ka10131` · `consecutive_trading_status()` — 기관외국인연속매매현황요청

기관외국인연속매매현황요청 (Institution and Foreign Consecutive Trading Status) · `POST /api/dostk/frgnistt`

```python
api.foreign_institution.consecutive_trading_status(dt=..., mrkt_tp=..., netslmt_tp=..., stk_inds_tp=..., amt_qty_tp=..., stex_tp=...)
```

**요청**

| 필드 | 한글명 | 필수 | 길이 |
|---|---|:---:|---:|
| `dt` | 기간 | Y | 3 |
| `strt_dt` | 시작일자 |  | 8 |
| `end_dt` | 종료일자 |  | 8 |
| `mrkt_tp` | 장구분 | Y | 3 |
| `netslmt_tp` | 순매도수구분 | Y | 1 |
| `stk_inds_tp` | 종목업종구분 | Y | 1 |
| `amt_qty_tp` | 금액수량구분 | Y | 1 |
| `stex_tp` | 거래소구분 | Y | 1 |

**응답**

| 필드 | 한글명 | 길이 |
|---|---|---:|
| `orgn_frgnr_cont_trde_prst` (list) | 기관외국인연속매매현황 |  |
| `orgn_frgnr_cont_trde_prst[].rank` | 순위 |  |
| `orgn_frgnr_cont_trde_prst[].stk_cd` | 종목코드 | 6 |
| `orgn_frgnr_cont_trde_prst[].stk_nm` | 종목명 | 40 |
| `orgn_frgnr_cont_trde_prst[].prid_stkpc_flu_rt` | 기간중주가등락률 |  |
| `orgn_frgnr_cont_trde_prst[].orgn_nettrde_amt` | 기관순매매금액 |  |
| `orgn_frgnr_cont_trde_prst[].orgn_nettrde_qty` | 기관순매매량 |  |
| `orgn_frgnr_cont_trde_prst[].orgn_cont_netprps_dys` | 기관계연속순매수일수 |  |
| `orgn_frgnr_cont_trde_prst[].orgn_cont_netprps_qty` | 기관계연속순매수량 |  |
| `orgn_frgnr_cont_trde_prst[].orgn_cont_netprps_amt` | 기관계연속순매수금액 |  |
| `orgn_frgnr_cont_trde_prst[].frgnr_nettrde_qty` | 외국인순매매량 |  |
| `orgn_frgnr_cont_trde_prst[].frgnr_nettrde_amt` | 외국인순매매액 |  |
| `orgn_frgnr_cont_trde_prst[].frgnr_cont_netprps_dys` | 외국인연속순매수일수 |  |
| `orgn_frgnr_cont_trde_prst[].frgnr_cont_netprps_qty` | 외국인연속순매수량 |  |
| `orgn_frgnr_cont_trde_prst[].frgnr_cont_netprps_amt` | 외국인연속순매수금액 |  |
| `orgn_frgnr_cont_trde_prst[].nettrde_qty` | 순매매량 |  |
| `orgn_frgnr_cont_trde_prst[].nettrde_amt` | 순매매액 |  |
| `orgn_frgnr_cont_trde_prst[].tot_cont_netprps_dys` | 합계연속순매수일수 |  |
| `orgn_frgnr_cont_trde_prst[].tot_cont_nettrde_qty` | 합계연속순매매수량 |  |
| `orgn_frgnr_cont_trde_prst[].tot_cont_netprps_amt` | 합계연속순매수금액 |  |

<a id="ka52301"></a>

## `ka52301` · `gold_spot_investor_status()` — 금현물투자자현황

금현물투자자현황 (Gold Spot Investor Status) · `POST /api/dostk/frgnistt`

```python
api.foreign_institution.gold_spot_investor_status()
```

**요청**

요청 필드 없음.

**응답**

| 필드 | 한글명 | 길이 |
|---|---|---:|
| `inve_trad_stat` (list) | 금현물투자자현황 |  |
| `inve_trad_stat[].all_dfrt_trst_sell_qty` | 투자자별 매도 수량(천) | 20 |
| `inve_trad_stat[].sell_qty_irds` | 투자자별 매도 수량 증감(천) | 20 |
| `inve_trad_stat[].all_dfrt_trst_sell_amt` | 투자자별 매도 금액(억) | 20 |
| `inve_trad_stat[].sell_amt_irds` | 투자자별 매도 금액 증감(억) | 20 |
| `inve_trad_stat[].all_dfrt_trst_buy_qty` | 투자자별 매수 수량(천) | 20 |
| `inve_trad_stat[].buy_qty_irds` | 투자자별 매수 수량 증감(천) | 20 |
| `inve_trad_stat[].all_dfrt_trst_buy_amt` | 투자자별 매수 금액(억) | 20 |
| `inve_trad_stat[].buy_amt_irds` | 투자자별 매수 금액 증감(억) | 20 |
| `inve_trad_stat[].all_dfrt_trst_netprps_qty` | 투자자별 순매수 수량(천) | 20 |
| `inve_trad_stat[].netprps_qty_irds` | 투자자별 순매수 수량 증감(천) | 20 |
| `inve_trad_stat[].all_dfrt_trst_netprps_amt` | 투자자별 순매수 금액(억) | 20 |
| `inve_trad_stat[].netprps_amt_irds` | 투자자별 순매수 금액 증감(억) | 20 |
| `inve_trad_stat[].sell_uv` | 투자자별 매도 단가 | 20 |
| `inve_trad_stat[].buy_uv` | 투자자별 매수 단가 | 20 |
| `inve_trad_stat[].stk_nm` | 투자자 구분명 | 20 |
| `inve_trad_stat[].acc_netprps_amt` | 누적 순매수 금액(억) | 20 |
| `inve_trad_stat[].acc_netprps_qty` | 누적 순매수 수량(천) | 20 |
| `inve_trad_stat[].stk_cd` | 투자자 코드 | 20 |
