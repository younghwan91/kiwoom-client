<!-- 자동 생성 파일 — 손으로 고치지 마세요. `python scripts/gen_docs.py` 가 TR 카탈로그(kiwoom_client.spec)로 다시 만듭니다. -->

# `api.sector` — 업종 (Sector)

요청·응답 필드는 키움 공식 REST API 명세에서 만든 TR 카탈로그([출처·라이선스](https://github.com/younghwan91/kiwoom-client/blob/main/src/kiwoom_client/spec/SOURCE.md))에서 옮긴 필드 ID·한글명·필수·길이입니다. 필드 설명·코드값은 싣지 않으니 [키움 REST API 포털](https://openapi.kiwoom.com) 문서를 보세요(자주 쓰는 코드값은 `kiwoom_client.codes`). 값은 모두 문자열로 넘깁니다.

공통 헤더(`api-id`·`cont-yn`·`next-key`·`authorization`)는 라이브러리가 채웁니다 — 연속조회는 메서드의 `cont_yn`·`next_key` 인자나 `request_all()` 을 쓰세요.

| api_id | 메서드 | 이름 |
|---|---|---|
| [`ka10010`](#ka10010) | `industry_program_trading()` | 업종프로그램요청 |
| [`ka10051`](#ka10051) | `industry_investor_net_buy()` | 업종별투자자순매수요청 |
| [`ka20001`](#ka20001) | `industry_current_price()` | 업종현재가요청 |
| [`ka20002`](#ka20002) | `industry_stock_price()` | 업종별주가요청 |
| [`ka20003`](#ka20003) | `all_industry_index()` | 전업종지수요청 |
| [`ka20009`](#ka20009) | `industry_daily_price()` | 업종현재가일별요청 |

<a id="ka10010"></a>

## `ka10010` · `industry_program_trading()` — 업종프로그램요청

업종프로그램매매요청 (Industry Program Trading) · `POST /api/dostk/sect`

```python
api.sector.industry_program_trading(stk_cd=...)
```

**요청**

| 필드 | 한글명 | 필수 | 길이 |
|---|---|:---:|---:|
| `stk_cd` | 종목코드 | Y | 20 |

**응답**

| 필드 | 한글명 | 길이 |
|---|---|---:|
| `dfrt_trst_sell_qty` | 차익위탁매도수량 | 20 |
| `dfrt_trst_sell_amt` | 차익위탁매도금액 | 20 |
| `dfrt_trst_buy_qty` | 차익위탁매수수량 | 20 |
| `dfrt_trst_buy_amt` | 차익위탁매수금액 | 20 |
| `dfrt_trst_netprps_qty` | 차익위탁순매수수량 | 20 |
| `dfrt_trst_netprps_amt` | 차익위탁순매수금액 | 20 |
| `ndiffpro_trst_sell_qty` | 비차익위탁매도수량 | 20 |
| `ndiffpro_trst_sell_amt` | 비차익위탁매도금액 | 20 |
| `ndiffpro_trst_buy_qty` | 비차익위탁매수수량 | 20 |
| `ndiffpro_trst_buy_amt` | 비차익위탁매수금액 | 20 |
| `ndiffpro_trst_netprps_qty` | 비차익위탁순매수수량 | 20 |
| `ndiffpro_trst_netprps_amt` | 비차익위탁순매수금액 | 20 |
| `all_dfrt_trst_sell_qty` | 전체차익위탁매도수량 | 20 |
| `all_dfrt_trst_sell_amt` | 전체차익위탁매도금액 | 20 |
| `all_dfrt_trst_buy_qty` | 전체차익위탁매수수량 | 20 |
| `all_dfrt_trst_buy_amt` | 전체차익위탁매수금액 | 20 |
| `all_dfrt_trst_netprps_qty` | 전체차익위탁순매수수량 | 20 |
| `all_dfrt_trst_netprps_amt` | 전체차익위탁순매수금액 | 20 |

<a id="ka10051"></a>

## `ka10051` · `industry_investor_net_buy()` — 업종별투자자순매수요청

업종별투자자순매수요청 (Industry Investor Net Buy) · `POST /api/dostk/sect`

```python
api.sector.industry_investor_net_buy(mrkt_tp=..., amt_qty_tp=..., stex_tp=...)
```

**요청**

| 필드 | 한글명 | 필수 | 길이 |
|---|---|:---:|---:|
| `mrkt_tp` | 시장구분 | Y | 1 |
| `amt_qty_tp` | 금액수량구분 | Y | 1 |
| `base_dt` | 기준일자 |  | 8 |
| `stex_tp` | 거래소구분 | Y | 1 |

**응답**

| 필드 | 한글명 | 길이 |
|---|---|---:|
| `inds_netprps` (list) | 업종별순매수 |  |
| `inds_netprps[].inds_cd` | 업종코드 | 20 |
| `inds_netprps[].inds_nm` | 업종명 | 20 |
| `inds_netprps[].cur_prc` | 현재가 | 20 |
| `inds_netprps[].pre_smbol` | 대비부호 | 20 |
| `inds_netprps[].pred_pre` | 전일대비 | 20 |
| `inds_netprps[].flu_rt` | 등락율 | 20 |
| `inds_netprps[].trde_qty` | 거래량 | 20 |
| `inds_netprps[].sc_netprps` | 증권순매수 | 20 |
| `inds_netprps[].insrnc_netprps` | 보험순매수 | 20 |
| `inds_netprps[].invtrt_netprps` | 투신순매수 | 20 |
| `inds_netprps[].bank_netprps` | 은행순매수 | 20 |
| `inds_netprps[].jnsinkm_netprps` | 종신금순매수 | 20 |
| `inds_netprps[].endw_netprps` | 기금순매수 | 20 |
| `inds_netprps[].etc_corp_netprps` | 기타법인순매수 | 20 |
| `inds_netprps[].ind_netprps` | 개인순매수 | 20 |
| `inds_netprps[].frgnr_netprps` | 외국인순매수 | 20 |
| `inds_netprps[].native_trmt_frgnr_netprps` | 내국인대우외국인순매수 | 20 |
| `inds_netprps[].natn_netprps` | 국가순매수 | 20 |
| `inds_netprps[].samo_fund_netprps` | 사모펀드순매수 | 20 |
| `inds_netprps[].orgn_netprps` | 기관계순매수 | 20 |

<a id="ka20001"></a>

## `ka20001` · `industry_current_price()` — 업종현재가요청

업종현재가요청 (Industry Current Price) · `POST /api/dostk/sect`

```python
api.sector.industry_current_price(mrkt_tp=..., inds_cd=...)
```

**요청**

| 필드 | 한글명 | 필수 | 길이 |
|---|---|:---:|---:|
| `mrkt_tp` | 시장구분 | Y | 1 |
| `inds_cd` | 업종코드 | Y | 3 |

**응답**

| 필드 | 한글명 | 길이 |
|---|---|---:|
| `cur_prc` | 현재가 | 20 |
| `pred_pre_sig` | 전일대비기호 | 20 |
| `pred_pre` | 전일대비 | 20 |
| `flu_rt` | 등락률 | 20 |
| `trde_qty` | 거래량 | 20 |
| `trde_prica` | 거래대금 | 20 |
| `trde_frmatn_stk_num` | 거래형성종목수 | 20 |
| `trde_frmatn_rt` | 거래형성비율 | 20 |
| `open_pric` | 시가 | 20 |
| `high_pric` | 고가 | 20 |
| `low_pric` | 저가 | 20 |
| `upl` | 상한 | 20 |
| `rising` | 상승 | 20 |
| `stdns` | 보합 | 20 |
| `fall` | 하락 | 20 |
| `lst` | 하한 | 20 |
| `52wk_hgst_pric` | 52주최고가 | 20 |
| `52wk_hgst_pric_dt` | 52주최고가일 | 20 |
| `52wk_hgst_pric_pre_rt` | 52주최고가대비율 | 20 |
| `52wk_lwst_pric` | 52주최저가 | 20 |
| `52wk_lwst_pric_dt` | 52주최저가일 | 20 |
| `52wk_lwst_pric_pre_rt` | 52주최저가대비율 | 20 |
| `inds_cur_prc_tm` (list) | 업종현재가_시간별 |  |
| `inds_cur_prc_tm[].tm_n` | 시간n | 20 |
| `inds_cur_prc_tm[].cur_prc_n` | 현재가n | 20 |
| `inds_cur_prc_tm[].pred_pre_sig_n` | 전일대비기호n | 20 |
| `inds_cur_prc_tm[].pred_pre_n` | 전일대비n | 20 |
| `inds_cur_prc_tm[].flu_rt_n` | 등락률n | 20 |
| `inds_cur_prc_tm[].trde_qty_n` | 거래량n | 20 |
| `inds_cur_prc_tm[].acc_trde_qty_n` | 누적거래량n | 20 |

<a id="ka20002"></a>

## `ka20002` · `industry_stock_price()` — 업종별주가요청

업종별주가요청 (Industry Stock Price) · `POST /api/dostk/sect`

```python
api.sector.industry_stock_price(mrkt_tp=..., inds_cd=..., stex_tp=...)
```

**요청**

| 필드 | 한글명 | 필수 | 길이 |
|---|---|:---:|---:|
| `mrkt_tp` | 시장구분 | Y | 1 |
| `inds_cd` | 업종코드 | Y | 3 |
| `stex_tp` | 거래소구분 | Y | 1 |

**응답**

| 필드 | 한글명 | 길이 |
|---|---|---:|
| `inds_stkpc` (list) | 업종별주가 |  |
| `inds_stkpc[].stk_cd` | 종목코드 | 20 |
| `inds_stkpc[].stk_nm` | 종목명 | 40 |
| `inds_stkpc[].cur_prc` | 현재가 | 20 |
| `inds_stkpc[].pred_pre_sig` | 전일대비기호 | 20 |
| `inds_stkpc[].pred_pre` | 전일대비 | 20 |
| `inds_stkpc[].flu_rt` | 등락률 | 20 |
| `inds_stkpc[].now_trde_qty` | 현재거래량 | 20 |
| `inds_stkpc[].sel_bid` | 매도호가 | 20 |
| `inds_stkpc[].buy_bid` | 매수호가 | 20 |
| `inds_stkpc[].open_pric` | 시가 | 20 |
| `inds_stkpc[].high_pric` | 고가 | 20 |
| `inds_stkpc[].low_pric` | 저가 | 20 |

<a id="ka20003"></a>

## `ka20003` · `all_industry_index()` — 전업종지수요청

전업종지수요청 (All Industry Index) · `POST /api/dostk/sect`

```python
api.sector.all_industry_index(inds_cd=...)
```

**요청**

| 필드 | 한글명 | 필수 | 길이 |
|---|---|:---:|---:|
| `inds_cd` | 업종코드 | Y | 3 |

**응답**

| 필드 | 한글명 | 길이 |
|---|---|---:|
| `all_inds_idex` (list) | 전업종지수 |  |
| `all_inds_idex[].stk_cd` | 종목코드 | 20 |
| `all_inds_idex[].stk_nm` | 종목명 | 40 |
| `all_inds_idex[].cur_prc` | 현재가 | 20 |
| `all_inds_idex[].pre_sig` | 대비기호 | 20 |
| `all_inds_idex[].pred_pre` | 전일대비 | 20 |
| `all_inds_idex[].flu_rt` | 등락률 | 20 |
| `all_inds_idex[].trde_qty` | 거래량 | 20 |
| `all_inds_idex[].wght` | 비중 | 20 |
| `all_inds_idex[].trde_prica` | 거래대금 | 20 |
| `all_inds_idex[].upl` | 상한 | 20 |
| `all_inds_idex[].rising` | 상승 | 20 |
| `all_inds_idex[].stdns` | 보합 | 20 |
| `all_inds_idex[].fall` | 하락 | 20 |
| `all_inds_idex[].lst` | 하한 | 20 |
| `all_inds_idex[].flo_stk_num` | 상장종목수 | 20 |

<a id="ka20009"></a>

## `ka20009` · `industry_daily_price()` — 업종현재가일별요청

업종현재가일별요청 (Industry Daily Price) · `POST /api/dostk/sect`

```python
api.sector.industry_daily_price(mrkt_tp=..., inds_cd=...)
```

**요청**

| 필드 | 한글명 | 필수 | 길이 |
|---|---|:---:|---:|
| `mrkt_tp` | 시장구분 | Y | 1 |
| `inds_cd` | 업종코드 | Y | 3 |

**응답**

| 필드 | 한글명 | 길이 |
|---|---|---:|
| `cur_prc` | 현재가 | 20 |
| `pred_pre_sig` | 전일대비기호 | 20 |
| `pred_pre` | 전일대비 | 20 |
| `flu_rt` | 등락률 | 20 |
| `trde_qty` | 거래량 | 20 |
| `trde_prica` | 거래대금 | 20 |
| `trde_frmatn_stk_num` | 거래형성종목수 | 20 |
| `trde_frmatn_rt` | 거래형성비율 | 20 |
| `open_pric` | 시가 | 20 |
| `high_pric` | 고가 | 20 |
| `low_pric` | 저가 | 20 |
| `upl` | 상한 | 20 |
| `rising` | 상승 | 20 |
| `stdns` | 보합 | 20 |
| `fall` | 하락 | 20 |
| `lst` | 하한 | 20 |
| `52wk_hgst_pric` | 52주최고가 | 20 |
| `52wk_hgst_pric_dt` | 52주최고가일 | 20 |
| `52wk_hgst_pric_pre_rt` | 52주최고가대비율 | 20 |
| `52wk_lwst_pric` | 52주최저가 | 20 |
| `52wk_lwst_pric_dt` | 52주최저가일 | 20 |
| `52wk_lwst_pric_pre_rt` | 52주최저가대비율 | 20 |
| `inds_cur_prc_daly_rept` (list) | 업종현재가_일별반복 |  |
| `inds_cur_prc_daly_rept[].dt_n` | 일자n | 20 |
| `inds_cur_prc_daly_rept[].cur_prc_n` | 현재가n | 20 |
| `inds_cur_prc_daly_rept[].pred_pre_sig_n` | 전일대비기호n | 20 |
| `inds_cur_prc_daly_rept[].pred_pre_n` | 전일대비n | 20 |
| `inds_cur_prc_daly_rept[].flu_rt_n` | 등락률n | 20 |
| `inds_cur_prc_daly_rept[].acc_trde_qty_n` | 누적거래량n | 20 |
