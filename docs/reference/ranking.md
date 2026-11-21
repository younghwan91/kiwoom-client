<!-- 자동 생성 파일 — 손으로 고치지 마세요. `python scripts/gen_docs.py` 가 TR 카탈로그(kiwoom_client.spec)로 다시 만듭니다. -->

# `api.ranking` — 순위정보 (Ranking)

요청·응답 필드는 키움 공식 REST API 명세에서 만든 TR 카탈로그([출처·라이선스](https://github.com/younghwan91/kiwoom-client/blob/main/src/kiwoom_client/spec/SOURCE.md))를 그대로 옮긴 것입니다. 뜻이 애매하면 [키움 REST API 포털](https://openapi.kiwoom.com)이 기준입니다. 값은 모두 문자열로 넘깁니다.

공통 헤더(`api-id`·`cont-yn`·`next-key`·`authorization`)는 라이브러리가 채웁니다 — 연속조회는 메서드의 `cont_yn`·`next_key` 인자나 `request_all()` 을 쓰세요.

| api_id | 메서드 | 이름 |
|---|---|---|
| [`ka10020`](#ka10020) | `top_order_book_volume()` | 호가잔량상위요청 |
| [`ka10021`](#ka10021) | `sudden_order_book_increase()` | 호가잔량급증요청 |
| [`ka10022`](#ka10022) | `sudden_order_ratio_increase()` | 잔량율급증요청 |
| [`ka10023`](#ka10023) | `sudden_volume_increase()` | 거래량급증요청 |
| [`ka10027`](#ka10027) | `top_change_rate()` | 전일대비등락률상위요청 |
| [`ka10029`](#ka10029) | `top_expected_change_rate()` | 예상체결등락률상위요청 |
| [`ka10030`](#ka10030) | `top_volume_today()` | 당일거래량상위요청 |
| [`ka10031`](#ka10031) | `top_volume_yesterday()` | 전일거래량상위요청 |
| [`ka10032`](#ka10032) | `top_trading_value()` | 거래대금상위요청 |
| [`ka10033`](#ka10033) | `top_credit_ratio()` | 신용비율상위요청 |
| [`ka10034`](#ka10034) | `top_foreign_trades_by_period()` | 외인기간별매매상위요청 |
| [`ka10035`](#ka10035) | `top_foreign_consecutive_buy()` | 외인연속순매매상위요청 |
| [`ka10036`](#ka10036) | `top_foreign_limit_increase()` | 외인한도소진율증가상위 |
| [`ka10037`](#ka10037) | `top_foreign_broker_trading()` | 외국계창구매매상위요청 |
| [`ka10038`](#ka10038) | `broker_ranking_by_stock()` | 종목별증권사순위요청 |
| [`ka10039`](#ka10039) | `top_broker_by_stock()` | 증권사별매매상위요청 |
| [`ka10040`](#ka10040) | `main_brokers_today()` | 당일주요거래원요청 |
| [`ka10042`](#ka10042) | `top_net_buying_brokers()` | 순매수거래원순위요청 |
| [`ka10053`](#ka10053) | `departed_brokers_today()` | 당일상위이탈원요청 |
| [`ka10062`](#ka10062) | `same_day_net_buying_rank()` | 동일순매매순위요청 |
| [`ka10065`](#ka10065) | `top_intraday_investor_trading()` | 장중투자자별매매상위요청 |
| [`ka10098`](#ka10098) | `after_hours_change_rate_rank()` | 시간외단일가등락율순위요청 |
| [`ka90009`](#ka90009) | `top_foreign_institution_trades()` | 외국인기관매매상위요청 |

<a id="ka10020"></a>

## `ka10020` · `top_order_book_volume()` — 호가잔량상위요청

호가잔량상위요청 (Top Order Book Volume) · `POST /api/dostk/rkinfo`

```python
api.ranking.top_order_book_volume(mrkt_tp=..., sort_tp=..., trde_qty_tp=..., stk_cnd=..., crd_cnd=..., stex_tp=...)
```

**요청**

| 필드 | 한글명 | 필수 | 길이 | 설명 |
|---|---|:---:|---:|---|
| `mrkt_tp` | 시장구분 | Y | 3 | 001:코스피, 101:코스닥 |
| `sort_tp` | 정렬구분 | Y | 1 | 1:순매수잔량순, 2:순매도잔량순, 3:매수비율순, 4:매도비율순 |
| `trde_qty_tp` | 거래량구분 | Y | 4 | 0000:장시작전(0주이상), 0010:만주이상, 0050:5만주이상, 00100:10만주이상 |
| `stk_cnd` | 종목조건 | Y | 1 | 0:전체조회, 1:관리종목제외, 5:증100제외, 6:증100만보기, 7:증40만보기, 8:증30만보기, 9:증20만보기 |
| `crd_cnd` | 신용조건 | Y | 1 | 0:전체조회, 1:신용융자A군, 2:신용융자B군, 3:신용융자C군, 4:신용융자D군, 7:신용융자E군, 9:신용융자전체 |
| `stex_tp` | 거래소구분 | Y | 1 | 1:KRX, 2:NXT 3.통합 |

**응답**

| 필드 | 한글명 | 길이 | 설명 |
|---|---|---:|---|
| `bid_req_upper` (list) | 호가잔량상위 |  |   |
| `bid_req_upper[].stk_cd` | 종목코드 | 20 |   |
| `bid_req_upper[].stk_nm` | 종목명 | 40 |   |
| `bid_req_upper[].cur_prc` | 현재가 | 20 | 단위: 원, 부호가 포함된 숫자 |
| `bid_req_upper[].pred_pre_sig` | 전일대비기호 | 20 | 1: 상한가, 2:상승, 3:보합, 4:하한가, 5:하락 |
| `bid_req_upper[].pred_pre` | 전일대비 | 20 | 단위: 원, 부호가 포함된 숫자 |
| `bid_req_upper[].trde_qty` | 거래량 | 20 | 단위: 1주 |
| `bid_req_upper[].tot_sel_req` | 총매도잔량 | 20 | 단위: 1주 |
| `bid_req_upper[].tot_buy_req` | 총매수잔량 | 20 | 단위: 1주 |
| `bid_req_upper[].netprps_req` | 순매수잔량 | 20 | 단위: 1주 |
| `bid_req_upper[].buy_rt` | 매수비율 | 20 | 단위: %, 소수점 둘째 자리까지 포맷된 백분율 |

<a id="ka10021"></a>

## `ka10021` · `sudden_order_book_increase()` — 호가잔량급증요청

호가잔량급증요청 (Sudden Order Book Increase) · `POST /api/dostk/rkinfo`

```python
api.ranking.sudden_order_book_increase(mrkt_tp=..., trde_tp=..., sort_tp=..., tm_tp=..., trde_qty_tp=..., stk_cnd=..., stex_tp=...)
```

**요청**

| 필드 | 한글명 | 필수 | 길이 | 설명 |
|---|---|:---:|---:|---|
| `mrkt_tp` | 시장구분 | Y | 3 | 001:코스피, 101:코스닥 |
| `trde_tp` | 매매구분 | Y | 1 | 1:매수잔량, 2:매도잔량 |
| `sort_tp` | 정렬구분 | Y | 1 | 1:급증량, 2:급증률 |
| `tm_tp` | 시간구분 | Y | 2 | 분 입력 |
| `trde_qty_tp` | 거래량구분 | Y | 4 | 1:천주이상, 5:5천주이상, 10:만주이상, 50:5만주이상, 100:10만주이상 |
| `stk_cnd` | 종목조건 | Y | 1 | 0:전체조회, 1:관리종목제외, 5:증100제외, 6:증100만보기, 7:증40만보기, 8:증30만보기, 9:증20만보기 |
| `stex_tp` | 거래소구분 | Y | 1 | 1:KRX, 2:NXT 3.통합 |

**응답**

| 필드 | 한글명 | 길이 | 설명 |
|---|---|---:|---|
| `bid_req_sdnin` (list) | 호가잔량급증 |  |   |
| `bid_req_sdnin[].stk_cd` | 종목코드 | 20 |   |
| `bid_req_sdnin[].stk_nm` | 종목명 | 40 |   |
| `bid_req_sdnin[].cur_prc` | 현재가 | 20 | 단위: 원, 부호가 포함된 숫자 |
| `bid_req_sdnin[].pred_pre_sig` | 전일대비기호 | 20 | 1: 상한가, 2:상승, 3:보합, 4:하한가, 5:하락 |
| `bid_req_sdnin[].pred_pre` | 전일대비 | 20 | 단위: 원, 부호가 포함된 숫자 |
| `bid_req_sdnin[].int` | 기준량 | 20 | 단위: 1주 |
| `bid_req_sdnin[].now` | 현재 | 20 | 단위: 1주 |
| `bid_req_sdnin[].sdnin_qty` | 급증수량 | 20 | 단위: 1주 |
| `bid_req_sdnin[].sdnin_rt` | 급증률 | 20 | 단위: %, 부호 포함 소수점 둘째 자리까지 포맷된 백분율 |
| `bid_req_sdnin[].tot_buy_qty` | 총매수량 | 20 | 단위: 1주 |

<a id="ka10022"></a>

## `ka10022` · `sudden_order_ratio_increase()` — 잔량율급증요청

잔량율급증요청 (Sudden Order Ratio Increase) · `POST /api/dostk/rkinfo`

```python
api.ranking.sudden_order_ratio_increase(mrkt_tp=..., rt_tp=..., tm_tp=..., trde_qty_tp=..., stk_cnd=..., stex_tp=...)
```

**요청**

| 필드 | 한글명 | 필수 | 길이 | 설명 |
|---|---|:---:|---:|---|
| `mrkt_tp` | 시장구분 | Y | 3 | 001:코스피, 101:코스닥 |
| `rt_tp` | 비율구분 | Y | 1 | 1:매수/매도비율, 2:매도/매수비율 |
| `tm_tp` | 시간구분 | Y | 2 | 분 입력 |
| `trde_qty_tp` | 거래량구분 | Y | 1 | 5:5천주이상, 10:만주이상, 50:5만주이상, 100:10만주이상 |
| `stk_cnd` | 종목조건 | Y | 1 | 0:전체조회, 1:관리종목제외, 5:증100제외, 6:증100만보기, 7:증40만보기, 8:증30만보기, 9:증20만보기 |
| `stex_tp` | 거래소구분 | Y | 1 | 1:KRX, 2:NXT 3.통합 |

**응답**

| 필드 | 한글명 | 길이 | 설명 |
|---|---|---:|---|
| `req_rt_sdnin` (list) | 잔량율급증 |  |   |
| `req_rt_sdnin[].stk_cd` | 종목코드 | 20 |   |
| `req_rt_sdnin[].stk_nm` | 종목명 | 40 |   |
| `req_rt_sdnin[].cur_prc` | 현재가 | 20 | 단위: 원, 부호가 포함된 숫자 |
| `req_rt_sdnin[].pred_pre_sig` | 전일대비기호 | 20 | 1: 상한가, 2:상승, 3:보합, 4:하한가, 5:하락 |
| `req_rt_sdnin[].pred_pre` | 전일대비 | 20 | 단위: 원, 부호가 포함된 숫자 |
| `req_rt_sdnin[].int` | 기준률 | 20 | 단위: %, 소수점 둘째 자리까지 포맷된 백분율 |
| `req_rt_sdnin[].now_rt` | 현재비율 | 20 | 단위: %, 소수점 둘째 자리까지 포맷된 백분율 |
| `req_rt_sdnin[].sdnin_rt` | 급증률 | 20 | 단위: %, 소수점 둘째 자리까지 포맷된 백분율 |
| `req_rt_sdnin[].tot_sel_req` | 총매도잔량 | 20 | 단위: 1주 |
| `req_rt_sdnin[].tot_buy_req` | 총매수잔량 | 20 | 단위: 1주 |

<a id="ka10023"></a>

## `ka10023` · `sudden_volume_increase()` — 거래량급증요청

거래량급증요청 (Sudden Volume Increase) · `POST /api/dostk/rkinfo`

```python
api.ranking.sudden_volume_increase(mrkt_tp=..., sort_tp=..., tm_tp=..., trde_qty_tp=..., stk_cnd=..., pric_tp=..., stex_tp=...)
```

**요청**

| 필드 | 한글명 | 필수 | 길이 | 설명 |
|---|---|:---:|---:|---|
| `mrkt_tp` | 시장구분 | Y | 3 | 000:전체, 001:코스피, 101:코스닥 |
| `sort_tp` | 정렬구분 | Y | 1 | 1:급증량, 2:급증률, 3:급감량, 4:급감률 |
| `tm_tp` | 시간구분 | Y | 1 | 1:분, 2:전일 |
| `trde_qty_tp` | 거래량구분 | Y | 1 | 5:5천주이상, 10:만주이상, 50:5만주이상, 100:10만주이상, 200:20만주이상, 300:30만주이상, 500:50만주이상, 1000:백만주이상 |
| `tm` | 시간 |  | 2 | 분 입력 |
| `stk_cnd` | 종목조건 | Y | 1 | 0:전체조회, 1:관리종목제외, 3:우선주제외, 11:정리매매종목제외, 4:관리종목,우선주제외, 5:증100제외, 6:증100만보기, 13:증60만보기, 12:증50만보기, 7:증40만보기, 8:증30만보기, 9:증20만보기, 17:ETN제외, 14:ETF제외, 18:ETF+ETN제외, 15:스팩제외, 20:ETF+ETN+스팩제외 |
| `pric_tp` | 가격구분 | Y | 1 | 0:전체조회, 2:5만원이상, 5:1만원이상, 6:5천원이상, 8:1천원이상, 9:10만원이상 |
| `stex_tp` | 거래소구분 | Y | 1 | 1:KRX, 2:NXT 3.통합 |

**응답**

| 필드 | 한글명 | 길이 | 설명 |
|---|---|---:|---|
| `trde_qty_sdnin` (list) | 거래량급증 |  |   |
| `trde_qty_sdnin[].stk_cd` | 종목코드 | 20 |   |
| `trde_qty_sdnin[].stk_nm` | 종목명 | 40 |   |
| `trde_qty_sdnin[].cur_prc` | 현재가 | 20 | 단위: 원, 부호가 포함된 숫자 |
| `trde_qty_sdnin[].pred_pre_sig` | 전일대비기호 | 20 | 1: 상한가, 2:상승, 3:보합, 4:하한가, 5:하락 |
| `trde_qty_sdnin[].pred_pre` | 전일대비 | 20 | 단위: 원, 부호가 포함된 숫자 |
| `trde_qty_sdnin[].flu_rt` | 등락률 | 20 | 단위: %, 부호 포함 소수점 둘째 자리까지 포맷된 백분율 |
| `trde_qty_sdnin[].prev_trde_qty` | 이전거래량 | 20 | 단위: 1주 |
| `trde_qty_sdnin[].now_trde_qty` | 현재거래량 | 20 | 단위: 1주 |
| `trde_qty_sdnin[].sdnin_qty` | 급증량 | 20 | 단위: 1주, 부호가 포함된 숫자 |
| `trde_qty_sdnin[].sdnin_rt` | 급증률 | 20 | 단위: %, 부호 포함 소수점 둘째 자리까지 포맷된 백분율 |

<a id="ka10027"></a>

## `ka10027` · `top_change_rate()` — 전일대비등락률상위요청

전일대비등락률상위요청 (Top Change Rate vs Previous Day) · `POST /api/dostk/rkinfo`

```python
api.ranking.top_change_rate(mrkt_tp=..., sort_tp=..., trde_qty_cnd=..., stk_cnd=..., crd_cnd=..., updown_incls=..., pric_cnd=..., trde_prica_cnd=..., stex_tp=...)
```

**요청**

| 필드 | 한글명 | 필수 | 길이 | 설명 |
|---|---|:---:|---:|---|
| `mrkt_tp` | 시장구분 | Y | 3 | 000:전체, 001:코스피, 101:코스닥 |
| `sort_tp` | 정렬구분 | Y | 1 | 1:상승률, 2:상승폭, 3:하락률, 4:하락폭, 5:보합 |
| `trde_qty_cnd` | 거래량조건 | Y | 5 | 0000:전체조회, 0010:만주이상, 0050:5만주이상, 0100:10만주이상, 0150:15만주이상, 0200:20만주이상, 0300:30만주이상, 0500:50만주이상, 1000:백만주이상 |
| `stk_cnd` | 종목조건 | Y | 2 | 0:전체조회, 1:관리종목제외, 4:우선주+관리주제외, 3:우선주제외, 5:증100제외, 6:증100만보기, 7:증40만보기, 8:증30만보기, 9:증20만보기, 11:정리매매종목제외, 12:증50만보기, 13:증60만보기, 14:ETF제외, 15:스펙제외, 16:ETF+ETN제외 |
| `crd_cnd` | 신용조건 | Y | 1 | 0:전체조회, 1:신용융자A군, 2:신용융자B군, 3:신용융자C군, 4:신용융자D군, 7:신용융자E군, 9:신용융자전체 |
| `updown_incls` | 상하한포함 | Y | 2 | 0:불 포함, 1:포함 |
| `pric_cnd` | 가격조건 | Y | 2 | 0:전체조회, 1:1천원미만, 2:1천원~2천원, 3:2천원~5천원, 4:5천원~1만원, 5:1만원이상, 8:1천원이상, 10: 1만원미만 |
| `trde_prica_cnd` | 거래대금조건 | Y | 4 | 0:전체조회, 3:3천만원이상, 5:5천만원이상, 10:1억원이상, 30:3억원이상, 50:5억원이상, 100:10억원이상, 300:30억원이상, 500:50억원이상, 1000:100억원이상, 3000:300억원이상, 5000:500억원이상 |
| `stex_tp` | 거래소구분 | Y | 1 | 1:KRX, 2:NXT 3.통합 |

**응답**

| 필드 | 한글명 | 길이 | 설명 |
|---|---|---:|---|
| `pred_pre_flu_rt_upper` (list) | 전일대비등락률상위 |  |   |
| `pred_pre_flu_rt_upper[].stk_cls` | 종목분류 | 20 |   |
| `pred_pre_flu_rt_upper[].stk_cd` | 종목코드 | 20 |   |
| `pred_pre_flu_rt_upper[].stk_nm` | 종목명 | 40 |   |
| `pred_pre_flu_rt_upper[].cur_prc` | 현재가 | 20 | 단위: 원, 부호가 포함된 숫자 |
| `pred_pre_flu_rt_upper[].pred_pre_sig` | 전일대비기호 | 20 | 1: 상한가, 2:상승, 3:보합, 4:하한가, 5:하락 |
| `pred_pre_flu_rt_upper[].pred_pre` | 전일대비 | 20 | 단위: 원, 부호가 포함된 숫자 |
| `pred_pre_flu_rt_upper[].flu_rt` | 등락률 | 20 | 단위: %, 부호 포함 소수점 둘째 자리까지 포맷된 백분율 |
| `pred_pre_flu_rt_upper[].sel_req` | 매도잔량 | 20 | 단위: 1주 |
| `pred_pre_flu_rt_upper[].buy_req` | 매수잔량 | 20 | 단위: 1주 |
| `pred_pre_flu_rt_upper[].now_trde_qty` | 현재거래량 | 20 | 단위: 1주 |
| `pred_pre_flu_rt_upper[].cntr_str` | 체결강도 | 20 | 단위: %, 소수점 둘째 자리까지 포맷된 백분율 |
| `pred_pre_flu_rt_upper[].cnt` | 횟수 | 20 |   |

<a id="ka10029"></a>

## `ka10029` · `top_expected_change_rate()` — 예상체결등락률상위요청

예상체결등락률상위요청 (Top Expected Execution Change Rate) · `POST /api/dostk/rkinfo`

```python
api.ranking.top_expected_change_rate(mrkt_tp=..., sort_tp=..., trde_qty_cnd=..., stk_cnd=..., crd_cnd=..., pric_cnd=..., stex_tp=...)
```

**요청**

| 필드 | 한글명 | 필수 | 길이 | 설명 |
|---|---|:---:|---:|---|
| `mrkt_tp` | 시장구분 | Y | 3 | 000:전체, 001:코스피, 101:코스닥 |
| `sort_tp` | 정렬구분 | Y | 1 | 1:상승률, 2:상승폭, 3:보합, 4:하락률, 5:하락폭, 6:체결량, 7:상한, 8:하한 |
| `trde_qty_cnd` | 거래량조건 | Y | 5 | 0:전체조회, 1;천주이상, 3:3천주, 5:5천주, 10:만주이상, 50:5만주이상, 100:10만주이상 |
| `stk_cnd` | 종목조건 | Y | 2 | 0:전체조회, 1:관리종목제외, 3:우선주제외, 4:관리종목,우선주제외, 5:증100제외, 6:증100만보기, 7:증40만보기, 8:증30만보기, 9:증20만보기, 11:정리매매종목제외, 12:증50만보기, 13:증60만보기, 14:ETF제외, 15:스팩제외, 16:ETF+ETN제외 |
| `crd_cnd` | 신용조건 | Y | 1 | 0:전체조회, 1:신용융자A군, 2:신용융자B군, 3:신용융자C군, 4:신용융자D군, 5:신용한도초과제외, 7:신용융자E군, 8:신용대주, 9:신용융자전체 |
| `pric_cnd` | 가격조건 | Y | 2 | 0:전체조회, 1:1천원미만, 2:1천원~2천원, 3:2천원~5천원, 4:5천원~1만원, 5:1만원이상, 8:1천원이상, 10:1만원미만 |
| `stex_tp` | 거래소구분 | Y | 1 | 1:KRX, 2:NXT 3.통합 |

**응답**

| 필드 | 한글명 | 길이 | 설명 |
|---|---|---:|---|
| `exp_cntr_flu_rt_upper` (list) | 예상체결등락률상위 |  |   |
| `exp_cntr_flu_rt_upper[].stk_cd` | 종목코드 | 20 |   |
| `exp_cntr_flu_rt_upper[].stk_nm` | 종목명 | 40 |   |
| `exp_cntr_flu_rt_upper[].exp_cntr_pric` | 예상체결가 | 20 | 단위: 원, 부호가 포함된 숫자 |
| `exp_cntr_flu_rt_upper[].base_pric` | 기준가 | 20 | 단위: 원, 부호가 포함된 숫자 |
| `exp_cntr_flu_rt_upper[].pred_pre_sig` | 전일대비기호 | 20 | 1: 상한가, 2:상승, 3:보합, 4:하한가, 5:하락 |
| `exp_cntr_flu_rt_upper[].pred_pre` | 전일대비 | 20 | 단위: 원, 부호가 포함된 숫자 |
| `exp_cntr_flu_rt_upper[].flu_rt` | 등락률 | 20 | 단위: %, 부호 포함 소수점 둘째 자리까지 포맷된 백분율 |
| `exp_cntr_flu_rt_upper[].exp_cntr_qty` | 예상체결량 | 20 | 단위: 1주 |
| `exp_cntr_flu_rt_upper[].sel_req` | 매도잔량 | 20 | 단위: 1주 |
| `exp_cntr_flu_rt_upper[].sel_bid` | 매도호가 | 20 | 단위: 원, 부호가 포함된 숫자 |
| `exp_cntr_flu_rt_upper[].buy_bid` | 매수호가 | 20 | 단위: 원, 부호가 포함된 숫자 |
| `exp_cntr_flu_rt_upper[].buy_req` | 매수잔량 | 20 | 단위: 1주 |

<a id="ka10030"></a>

## `ka10030` · `top_volume_today()` — 당일거래량상위요청

당일거래량상위요청 (Top Volume Today) · `POST /api/dostk/rkinfo`

```python
api.ranking.top_volume_today(mrkt_tp=..., sort_tp=..., mang_stk_incls=..., crd_tp=..., trde_qty_tp=..., pric_tp=..., trde_prica_tp=..., mrkt_open_tp=..., stex_tp=...)
```

**요청**

| 필드 | 한글명 | 필수 | 길이 | 설명 |
|---|---|:---:|---:|---|
| `mrkt_tp` | 시장구분 | Y | 3 | 000:전체, 001:코스피, 101:코스닥 |
| `sort_tp` | 정렬구분 | Y | 1 | 1:거래량, 2:거래회전율, 3:거래대금 |
| `mang_stk_incls` | 관리종목포함 | Y | 1 | 0:관리종목 포함, 1:관리종목 미포함, 3:우선주제외, 11:정리매매종목제외, 4:관리종목, 우선주제외, 5:증100제외, 6:증100마나보기, 13:증60만보기, 12:증50만보기, 7:증40만보기, 8:증30만보기, 9:증20만보기, 14:ETF제외, 15:스팩제외, 16:ETF+ETN제외 |
| `crd_tp` | 신용구분 | Y | 1 | 0:전체조회, 9:신용융자전체, 1:신용융자A군, 2:신용융자B군, 3:신용융자C군, 4:신용융자D군, 8:신용대주 |
| `trde_qty_tp` | 거래량구분 | Y | 1 | 0:전체조회, 5:5천주이상, 10:1만주이상, 50:5만주이상, 100:10만주이상, 200:20만주이상, 300:30만주이상, 500:500만주이상, 1000:백만주이상 |
| `pric_tp` | 가격구분 | Y | 1 | 0:전체조회, 1:1천원미만, 2:1천원이상, 3:1천원~2천원, 4:2천원~5천원, 5:5천원이상, 6:5천원~1만원, 10:1만원미만, 7:1만원이상, 8:5만원이상, 9:10만원이상 |
| `trde_prica_tp` | 거래대금구분 | Y | 1 | 0:전체조회, 1:1천만원이상, 3:3천만원이상, 4:5천만원이상, 10:1억원이상, 30:3억원이상, 50:5억원이상, 100:10억원이상, 300:30억원이상, 500:50억원이상, 1000:100억원이상, 3000:300억원이상, 5000:500억원이상 |
| `mrkt_open_tp` | 장운영구분 | Y | 1 | 0:전체조회, 1:장중, 2:장전시간외, 3:장후시간외 |
| `stex_tp` | 거래소구분 | Y | 1 | 1:KRX, 2:NXT 3.통합 |

**응답**

| 필드 | 한글명 | 길이 | 설명 |
|---|---|---:|---|
| `tdy_trde_qty_upper` (list) | 당일거래량상위 |  |   |
| `tdy_trde_qty_upper[].stk_cd` | 종목코드 | 20 |   |
| `tdy_trde_qty_upper[].stk_nm` | 종목명 | 40 |   |
| `tdy_trde_qty_upper[].cur_prc` | 현재가 | 20 | 단위: 원, 부호가 포함된 숫자 |
| `tdy_trde_qty_upper[].pred_pre_sig` | 전일대비기호 | 20 | 1: 상한가, 2:상승, 3:보합, 4:하한가, 5:하락 |
| `tdy_trde_qty_upper[].pred_pre` | 전일대비 | 20 | 단위: 원, 부호가 포함된 숫자 |
| `tdy_trde_qty_upper[].flu_rt` | 등락률 | 20 | 단위: %, 부호 포함 소수점 둘째 자리까지 포맷된 백분율 |
| `tdy_trde_qty_upper[].trde_qty` | 거래량 | 20 | 단위: 1주 |
| `tdy_trde_qty_upper[].pred_rt` | 전일비 | 20 | 단위: %, 부호 포함 소수점 둘째 자리까지 포맷된 백분율 |
| `tdy_trde_qty_upper[].trde_tern_rt` | 거래회전율 | 20 | 단위: %, 부호 포함 소수점 둘째 자리까지 포맷된 백분율 |
| `tdy_trde_qty_upper[].trde_amt` | 거래금액 | 20 | 단위: 백만원 |
| `tdy_trde_qty_upper[].opmr_trde_qty` | 장중거래량 | 20 |   |
| `tdy_trde_qty_upper[].opmr_pred_rt` | 장중전일비 | 20 |   |
| `tdy_trde_qty_upper[].opmr_trde_rt` | 장중거래회전율 | 20 |   |
| `tdy_trde_qty_upper[].opmr_trde_amt` | 장중거래금액 | 20 |   |
| `tdy_trde_qty_upper[].af_mkrt_trde_qty` | 장후거래량 | 20 |   |
| `tdy_trde_qty_upper[].af_mkrt_pred_rt` | 장후전일비 | 20 |   |
| `tdy_trde_qty_upper[].af_mkrt_trde_rt` | 장후거래회전율 | 20 |   |
| `tdy_trde_qty_upper[].af_mkrt_trde_amt` | 장후거래금액 | 20 |   |
| `tdy_trde_qty_upper[].bf_mkrt_trde_qty` | 장전거래량 | 20 |   |
| `tdy_trde_qty_upper[].bf_mkrt_pred_rt` | 장전전일비 | 20 |   |
| `tdy_trde_qty_upper[].bf_mkrt_trde_rt` | 장전거래회전율 | 20 |   |
| `tdy_trde_qty_upper[].bf_mkrt_trde_amt` | 장전거래금액 | 20 |   |

<a id="ka10031"></a>

## `ka10031` · `top_volume_yesterday()` — 전일거래량상위요청

전일거래량상위요청 (Top Volume Yesterday) · `POST /api/dostk/rkinfo`

```python
api.ranking.top_volume_yesterday(mrkt_tp=..., qry_tp=..., rank_strt=..., rank_end=..., stex_tp=...)
```

**요청**

| 필드 | 한글명 | 필수 | 길이 | 설명 |
|---|---|:---:|---:|---|
| `mrkt_tp` | 시장구분 | Y | 3 | 000:전체, 001:코스피, 101:코스닥 |
| `qry_tp` | 조회구분 | Y | 1 | 1:전일거래량 상위100종목, 2:전일거래대금 상위100종목 |
| `rank_strt` | 순위시작 | Y | 3 | 0 ~ 100 값 중에 조회를 원하는 순위 시작값 |
| `rank_end` | 순위끝 | Y | 3 | 0 ~ 100 값 중에 조회를 원하는 순위 끝값 |
| `stex_tp` | 거래소구분 | Y | 1 | 1:KRX, 2:NXT 3.통합 |

**응답**

| 필드 | 한글명 | 길이 | 설명 |
|---|---|---:|---|
| `pred_trde_qty_upper` (list) | 전일거래량상위 |  |   |
| `pred_trde_qty_upper[].stk_cd` | 종목코드 | 20 |   |
| `pred_trde_qty_upper[].stk_nm` | 종목명 | 40 |   |
| `pred_trde_qty_upper[].cur_prc` | 현재가 | 20 | 단위: 원, 부호가 포함된 숫자 |
| `pred_trde_qty_upper[].pred_pre_sig` | 전일대비기호 | 20 | 1: 상한가, 2:상승, 3:보합, 4:하한가, 5:하락 |
| `pred_trde_qty_upper[].pred_pre` | 전일대비 | 20 | 단위: 원, 부호가 포함된 숫자 |
| `pred_trde_qty_upper[].trde_qty` | 거래량 | 20 | 단위: 1주 |

<a id="ka10032"></a>

## `ka10032` · `top_trading_value()` — 거래대금상위요청

거래대금상위요청 (Top Trading Value) · `POST /api/dostk/rkinfo`

```python
api.ranking.top_trading_value(mrkt_tp=..., mang_stk_incls=..., stex_tp=...)
```

**요청**

| 필드 | 한글명 | 필수 | 길이 | 설명 |
|---|---|:---:|---:|---|
| `mrkt_tp` | 시장구분 | Y | 3 | 000:전체, 001:코스피, 101:코스닥 |
| `mang_stk_incls` | 관리종목포함 | Y | 1 | 0:관리종목 미포함, 1:관리종목 포함 |
| `stex_tp` | 거래소구분 | Y | 1 | 1:KRX, 2:NXT 3.통합 |

**응답**

| 필드 | 한글명 | 길이 | 설명 |
|---|---|---:|---|
| `trde_prica_upper` (list) | 거래대금상위 |  |   |
| `trde_prica_upper[].stk_cd` | 종목코드 | 20 |   |
| `trde_prica_upper[].now_rank` | 현재순위 | 20 |   |
| `trde_prica_upper[].pred_rank` | 전일순위 | 20 |   |
| `trde_prica_upper[].stk_nm` | 종목명 | 40 |   |
| `trde_prica_upper[].cur_prc` | 현재가 | 20 | 단위: 원, 부호가 포함된 숫자 |
| `trde_prica_upper[].pred_pre_sig` | 전일대비기호 | 20 | 1: 상한가, 2:상승, 3:보합, 4:하한가, 5:하락 |
| `trde_prica_upper[].pred_pre` | 전일대비 | 20 | 단위: 원, 부호가 포함된 숫자 |
| `trde_prica_upper[].flu_rt` | 등락률 | 20 | 단위: %, 부호 포함 소수점 둘째 자리까지 포맷된 백분율 |
| `trde_prica_upper[].sel_bid` | 매도호가 | 20 | 단위: 원, 부호가 포함된 숫자 |
| `trde_prica_upper[].buy_bid` | 매수호가 | 20 | 단위: 원, 부호가 포함된 숫자 |
| `trde_prica_upper[].now_trde_qty` | 현재거래량 | 20 | 단위: 1주 |
| `trde_prica_upper[].pred_trde_qty` | 전일거래량 | 20 | 단위: 1주 |
| `trde_prica_upper[].trde_prica` | 거래대금 | 20 | 단위: 백만원 |

<a id="ka10033"></a>

## `ka10033` · `top_credit_ratio()` — 신용비율상위요청

신용비율상위요청 (Top Credit Ratio) · `POST /api/dostk/rkinfo`

```python
api.ranking.top_credit_ratio(mrkt_tp=..., trde_qty_tp=..., stk_cnd=..., updown_incls=..., crd_cnd=..., stex_tp=...)
```

**요청**

| 필드 | 한글명 | 필수 | 길이 | 설명 |
|---|---|:---:|---:|---|
| `mrkt_tp` | 시장구분 | Y | 3 | 000:전체, 001:코스피, 101:코스닥 |
| `trde_qty_tp` | 거래량구분 | Y | 3 | 0:전체조회, 10:만주이상, 50:5만주이상, 100:10만주이상, 200:20만주이상, 300:30만주이상, 500:50만주이상, 1000:백만주이상 |
| `stk_cnd` | 종목조건 | Y | 1 | 0:전체조회, 1:관리종목제외, 5:증100제외, 6:증100만보기, 7:증40만보기, 8:증30만보기, 9:증20만보기 |
| `updown_incls` | 상하한포함 | Y | 1 | 0:상하한 미포함, 1:상하한포함 |
| `crd_cnd` | 신용조건 | Y | 1 | 0:전체조회, 1:신용융자A군, 2:신용융자B군, 3:신용융자C군, 4:신용융자D군, 7:신용융자E군, 9:신용융자전체 |
| `stex_tp` | 거래소구분 | Y | 1 | 1:KRX, 2:NXT 3.통합 |

**응답**

| 필드 | 한글명 | 길이 | 설명 |
|---|---|---:|---|
| `crd_rt_upper` (list) | 신용비율상위 |  |   |
| `crd_rt_upper[].stk_infr` | 종목정보 | 20 |   |
| `crd_rt_upper[].stk_cd` | 종목코드 | 20 |   |
| `crd_rt_upper[].stk_nm` | 종목명 | 40 |   |
| `crd_rt_upper[].cur_prc` | 현재가 | 20 | 단위: 원, 부호가 포함된 숫자 |
| `crd_rt_upper[].pred_pre_sig` | 전일대비기호 | 20 | 1: 상한가, 2:상승, 3:보합, 4:하한가, 5:하락 |
| `crd_rt_upper[].pred_pre` | 전일대비 | 20 | 단위: 원, 부호가 포함된 숫자 |
| `crd_rt_upper[].flu_rt` | 등락률 | 20 | 단위: %, 부호 포함 소수점 둘째 자리까지 포맷된 백분율 |
| `crd_rt_upper[].crd_rt` | 신용비율 | 20 | 단위: %, 부호 포함 소수점 둘째 자리까지 포맷된 백분율 |
| `crd_rt_upper[].sel_req` | 매도잔량 | 20 | 단위: 1주 |
| `crd_rt_upper[].buy_req` | 매수잔량 | 20 | 단위: 1주 |
| `crd_rt_upper[].now_trde_qty` | 현재거래량 | 20 | 단위: 1주 |

<a id="ka10034"></a>

## `ka10034` · `top_foreign_trades_by_period()` — 외인기간별매매상위요청

외인기간별매매상위요청 (Top Foreign Trades by Period) · `POST /api/dostk/rkinfo`

```python
api.ranking.top_foreign_trades_by_period(mrkt_tp=..., trde_tp=..., dt=..., stex_tp=...)
```

**요청**

| 필드 | 한글명 | 필수 | 길이 | 설명 |
|---|---|:---:|---:|---|
| `mrkt_tp` | 시장구분 | Y | 3 | 000:전체, 001:코스피, 101:코스닥 |
| `trde_tp` | 매매구분 | Y | 1 | 1:순매도, 2:순매수, 3:순매매 |
| `dt` | 기간 | Y | 2 | 0:당일, 1:전일, 5:5일, 10;10일, 20:20일, 60:60일 |
| `stex_tp` | 거래소구분 | Y | 1 | 1:KRX, 2:NXT, 3:통합 |

**응답**

| 필드 | 한글명 | 길이 | 설명 |
|---|---|---:|---|
| `for_dt_trde_upper` (list) | 외인기간별매매상위 |  |   |
| `for_dt_trde_upper[].rank` | 순위 | 20 |   |
| `for_dt_trde_upper[].stk_cd` | 종목코드 | 20 |   |
| `for_dt_trde_upper[].stk_nm` | 종목명 | 40 |   |
| `for_dt_trde_upper[].cur_prc` | 현재가 | 20 | 단위: 원, 부호가 포함된 숫자 |
| `for_dt_trde_upper[].pred_pre_sig` | 전일대비기호 | 20 | 1: 상한가, 2:상승, 3:보합, 4:하한가, 5:하락 |
| `for_dt_trde_upper[].pred_pre` | 전일대비 | 20 | 단위: 원, 부호가 포함된 숫자 |
| `for_dt_trde_upper[].sel_bid` | 매도호가 | 20 | 단위: 원, 부호가 포함된 숫자 |
| `for_dt_trde_upper[].buy_bid` | 매수호가 | 20 | 단위: 원, 부호가 포함된 숫자 |
| `for_dt_trde_upper[].trde_qty` | 거래량 | 20 | 단위: 1주 |
| `for_dt_trde_upper[].netprps_qty` | 순매수량 | 20 | 단위: 1주, 부호가 포함된 숫자 |
| `for_dt_trde_upper[].gain_pos_stkcnt` | 취득가능주식수 | 20 | 단위: 1주 |

<a id="ka10035"></a>

## `ka10035` · `top_foreign_consecutive_buy()` — 외인연속순매매상위요청

외인연속순매매상위요청 (Top Foreign Consecutive Net Buy) · `POST /api/dostk/rkinfo`

```python
api.ranking.top_foreign_consecutive_buy(mrkt_tp=..., trde_tp=..., base_dt_tp=..., stex_tp=...)
```

**요청**

| 필드 | 한글명 | 필수 | 길이 | 설명 |
|---|---|:---:|---:|---|
| `mrkt_tp` | 시장구분 | Y | 3 | 000:전체, 001:코스피, 101:코스닥 |
| `trde_tp` | 매매구분 | Y | 1 | 1:연속순매도, 2:연속순매수 |
| `base_dt_tp` | 기준일구분 | Y | 1 | 0:당일기준, 1:전일기준 |
| `stex_tp` | 거래소구분 | Y | 1 | 1:KRX, 2:NXT, 3:통합 |

**응답**

| 필드 | 한글명 | 길이 | 설명 |
|---|---|---:|---|
| `for_cont_nettrde_upper` (list) | 외인연속순매매상위 |  |   |
| `for_cont_nettrde_upper[].stk_cd` | 종목코드 | 20 |   |
| `for_cont_nettrde_upper[].stk_nm` | 종목명 | 40 |   |
| `for_cont_nettrde_upper[].cur_prc` | 현재가 | 20 | 단위: 원, 부호가 포함된 숫자 |
| `for_cont_nettrde_upper[].pred_pre_sig` | 전일대비기호 | 20 | 1: 상한가, 2:상승, 3:보합, 4:하한가, 5:하락 |
| `for_cont_nettrde_upper[].pred_pre` | 전일대비 | 20 | 단위: 원, 부호가 포함된 숫자 |
| `for_cont_nettrde_upper[].dm1` | D-1 | 20 | 단위: 1주, 부호가 포함된 숫자 |
| `for_cont_nettrde_upper[].dm2` | D-2 | 20 | 단위: 1주, 부호가 포함된 숫자 |
| `for_cont_nettrde_upper[].dm3` | D-3 | 20 | 단위: 1주, 부호가 포함된 숫자 |
| `for_cont_nettrde_upper[].tot` | 합계 | 20 | 단위: 1주, 부호가 포함된 숫자 |
| `for_cont_nettrde_upper[].limit_exh_rt` | 한도소진율 | 20 | 단위: %, 부호 포함 소수점 둘째 자리까지 포맷된 백분율 |
| `for_cont_nettrde_upper[].pred_pre_1` | 전일대비1 | 20 |   |
| `for_cont_nettrde_upper[].pred_pre_2` | 전일대비2 | 20 |   |
| `for_cont_nettrde_upper[].pred_pre_3` | 전일대비3 | 20 |   |

<a id="ka10036"></a>

## `ka10036` · `top_foreign_limit_increase()` — 외인한도소진율증가상위

외인한도소진율증가상위 (Top Foreign Limit Exhaustion Rate Increase) · `POST /api/dostk/rkinfo`

```python
api.ranking.top_foreign_limit_increase(mrkt_tp=..., dt=..., stex_tp=...)
```

**요청**

| 필드 | 한글명 | 필수 | 길이 | 설명 |
|---|---|:---:|---:|---|
| `mrkt_tp` | 시장구분 | Y | 3 | 000:전체, 001:코스피, 101:코스닥 |
| `dt` | 기간 | Y | 2 | 0:당일, 1:전일, 5:5일, 10;10일, 20:20일, 60:60일 |
| `stex_tp` | 거래소구분 | Y | 1 | 1:KRX, 2:NXT, 3:통합 |

**응답**

| 필드 | 한글명 | 길이 | 설명 |
|---|---|---:|---|
| `for_limit_exh_rt_incrs_upper` (list) | 외인한도소진율증가상위 |  |   |
| `for_limit_exh_rt_incrs_upper[].rank` | 순위 | 20 |   |
| `for_limit_exh_rt_incrs_upper[].stk_cd` | 종목코드 | 20 |   |
| `for_limit_exh_rt_incrs_upper[].stk_nm` | 종목명 | 40 |   |
| `for_limit_exh_rt_incrs_upper[].cur_prc` | 현재가 | 20 | 단위: 원, 부호가 포함된 숫자 |
| `for_limit_exh_rt_incrs_upper[].pred_pre_sig` | 전일대비기호 | 20 | 1: 상한가, 2:상승, 3:보합, 4:하한가, 5:하락 |
| `for_limit_exh_rt_incrs_upper[].pred_pre` | 전일대비 | 20 | 단위: 원, 부호가 포함된 숫자 |
| `for_limit_exh_rt_incrs_upper[].trde_qty` | 거래량 | 20 | 단위: 1주 |
| `for_limit_exh_rt_incrs_upper[].poss_stkcnt` | 보유주식수 | 20 | 단위: 1주 |
| `for_limit_exh_rt_incrs_upper[].gain_pos_stkcnt` | 취득가능주식수 | 20 | 단위: 1주 |
| `for_limit_exh_rt_incrs_upper[].base_limit_exh_rt` | 기준한도소진율 | 20 | 단위: %, 부호 포함 소수점 둘째 자리까지 포맷된 백분율 |
| `for_limit_exh_rt_incrs_upper[].limit_exh_rt` | 한도소진율 | 20 | 단위: %, 부호 포함 소수점 둘째 자리까지 포맷된 백분율 |
| `for_limit_exh_rt_incrs_upper[].exh_rt_incrs` | 소진율증가 | 20 | 단위: %, 부호 포함 소수점 둘째 자리까지 포맷된 백분율 |

<a id="ka10037"></a>

## `ka10037` · `top_foreign_broker_trading()` — 외국계창구매매상위요청

외국계창구매매상위요청 (Top Foreign Holding Broker Trading) · `POST /api/dostk/rkinfo`

```python
api.ranking.top_foreign_broker_trading(mrkt_tp=..., dt=..., trde_tp=..., sort_tp=..., stex_tp=...)
```

**요청**

| 필드 | 한글명 | 필수 | 길이 | 설명 |
|---|---|:---:|---:|---|
| `mrkt_tp` | 시장구분 | Y | 3 | 000:전체, 001:코스피, 101:코스닥 |
| `dt` | 기간 | Y | 2 | 0:당일, 1:전일, 5:5일, 10;10일, 20:20일, 60:60일 |
| `trde_tp` | 매매구분 | Y | 1 | 1:순매수, 2:순매도, 3:매수, 4:매도 |
| `sort_tp` | 정렬구분 | Y | 1 | 1:금액, 2:수량 |
| `stex_tp` | 거래소구분 | Y | 1 | 1:KRX, 2:NXT, 3:통합 |

**응답**

| 필드 | 한글명 | 길이 | 설명 |
|---|---|---:|---|
| `frgn_wicket_trde_upper` (list) | 외국계창구매매상위 |  |   |
| `frgn_wicket_trde_upper[].rank` | 순위 | 20 |   |
| `frgn_wicket_trde_upper[].stk_cd` | 종목코드 | 20 |   |
| `frgn_wicket_trde_upper[].stk_nm` | 종목명 | 40 |   |
| `frgn_wicket_trde_upper[].cur_prc` | 현재가 | 20 | 단위: 원, 부호가 포함된 숫자 |
| `frgn_wicket_trde_upper[].pred_pre_sig` | 전일대비기호 | 20 | 1: 상한가, 2:상승, 3:보합, 4:하한가, 5:하락 |
| `frgn_wicket_trde_upper[].pred_pre` | 전일대비 | 20 | 단위: 원, 부호가 포함된 숫자 |
| `frgn_wicket_trde_upper[].flu_rt` | 등락율 | 20 | 단위: %, 부호 포함 소수점 둘째 자리까지 포맷된 백분율 |
| `frgn_wicket_trde_upper[].sel_trde_qty` | 매도거래량 | 20 | 단위: 1주, 부호가 포함된 숫자 |
| `frgn_wicket_trde_upper[].buy_trde_qty` | 매수거래량 | 20 | 단위: 1주, 부호가 포함된 숫자 |
| `frgn_wicket_trde_upper[].netprps_trde_qty` | 순매수거래량 | 20 | 단위: 1주, 부호가 포함된 숫자 |
| `frgn_wicket_trde_upper[].netprps_prica` | 순매수대금 | 20 | 단위: 백만원 |
| `frgn_wicket_trde_upper[].trde_qty` | 거래량 | 20 | 단위: 1주 |
| `frgn_wicket_trde_upper[].trde_prica` | 거래대금 | 20 | 단위: 백만원 |

<a id="ka10038"></a>

## `ka10038` · `broker_ranking_by_stock()` — 종목별증권사순위요청

종목별증권사순위요청 (Broker Ranking by Stock) · `POST /api/dostk/rkinfo`

```python
api.ranking.broker_ranking_by_stock(stk_cd=..., qry_tp=...)
```

**요청**

| 필드 | 한글명 | 필수 | 길이 | 설명 |
|---|---|:---:|---:|---|
| `stk_cd` | 종목코드 | Y | 6 | 거래소별 종목코드 (KRX:039490,NXT:039490_NX,SOR:039490_AL) |
| `strt_dt` | 시작일자 |  | 8 | YYYYMMDD (연도4자리, 월 2자리, 일 2자리 형식) |
| `end_dt` | 종료일자 |  | 8 | YYYYMMDD (연도4자리, 월 2자리, 일 2자리 형식) |
| `qry_tp` | 조회구분 | Y | 1 | 1:순매도순위정렬, 2:순매수순위정렬 |
| `dt` | 기간 |  | 2 | 1:전일, 4:5일, 9:10일, 19:20일, 39:40일, 59:60일, 119:120일 ※ 시작일자와 종료일자로 조회를 원하는 경우 기간(dt)값은 빈값('')으로 설정 |

**응답**

| 필드 | 한글명 | 길이 | 설명 |
|---|---|---:|---|
| `rank_1` | 기간별 누적 매수량 | 20 | 단위: 1주, 부호가 포함된 숫자 |
| `rank_2` | 기간별 누적 매도량 | 20 | 단위: 1주, 부호가 포함된 숫자 |
| `rank_3` | 기간별 누적 순매수 | 20 | 단위: 1주, 부호가 포함된 숫자 |
| `prid_trde_qty` | 기간중거래량 | 20 | 단위: 1주 |
| `stk_sec_rank` (list) | 종목별증권사순위 |  |   |
| `stk_sec_rank[].rank` | 순위 | 20 |   |
| `stk_sec_rank[].mmcm_nm` | 회원사명 | 20 |   |
| `stk_sec_rank[].buy_qty` | 매수수량 | 20 | 단위: 1주, 부호가 포함된 숫자 |
| `stk_sec_rank[].sell_qty` | 매도수량 | 20 | 단위: 1주, 부호가 포함된 숫자 |
| `stk_sec_rank[].acc_netprps_qty` | 누적순매수수량 | 20 | 단위: 1주, 부호가 포함된 숫자 |

<a id="ka10039"></a>

## `ka10039` · `top_broker_by_stock()` — 증권사별매매상위요청

증권사별매매상위요청 (Top Broker by Stock) · `POST /api/dostk/rkinfo`

```python
api.ranking.top_broker_by_stock(mmcm_cd=..., trde_qty_tp=..., trde_tp=..., dt=..., stex_tp=...)
```

**요청**

| 필드 | 한글명 | 필수 | 길이 | 설명 |
|---|---|:---:|---:|---|
| `mmcm_cd` | 회원사코드 | Y | 3 | 회원사 코드는 ka10102 조회 |
| `trde_qty_tp` | 거래량구분 | Y | 4 | 0:전체, 5:5000주, 10:1만주, 50:5만주, 100:10만주, 500:50만주, 1000: 100만주 |
| `trde_tp` | 매매구분 | Y | 2 | 1:순매수, 2:순매도 |
| `dt` | 기간 | Y | 2 | 0:당일, 1:전일, 5:5일, 10:10일, 60:60일 |
| `stex_tp` | 거래소구분 | Y | 1 | 1:KRX, 2:NXT 3.통합 |

**응답**

| 필드 | 한글명 | 길이 | 설명 |
|---|---|---:|---|
| `sec_trde_upper` (list) | 증권사별매매상위 |  |   |
| `sec_trde_upper[].rank` | 순위 | 20 |   |
| `sec_trde_upper[].stk_cd` | 종목코드 | 20 |   |
| `sec_trde_upper[].stk_nm` | 종목명 | 40 |   |
| `sec_trde_upper[].prid_stkpc_flu` | 기간중주가등락 | 20 | 단위: 원, 부호가 포함된 숫자 |
| `sec_trde_upper[].flu_rt` | 등락율 | 20 | 단위: %, 부호 포함 소수점 둘째 자리까지 포맷된 백분율 |
| `sec_trde_upper[].prid_trde_qty` | 기간중거래량 | 20 | 단위: 1주 |
| `sec_trde_upper[].netprps` | 순매수 | 20 | 단위: 1주, 부호가 포함된 숫자 |
| `sec_trde_upper[].buy_trde_qty` | 매수거래량 | 20 | 단위: 1주, 부호가 포함된 숫자 |
| `sec_trde_upper[].sel_trde_qty` | 매도거래량 | 20 | 단위: 1주, 부호가 포함된 숫자 |
| `sec_trde_upper[].netprps_amt` | 순매수금액 | 20 | 단위: 천원, 부호가 포함된 숫자 |
| `sec_trde_upper[].buy_amt` | 매수금액 | 20 | 단위: 천원, 부호가 포함된 숫자 |
| `sec_trde_upper[].sell_amt` | 매도금액 | 20 | 단위: 천원, 부호가 포함된 숫자 |

<a id="ka10040"></a>

## `ka10040` · `main_brokers_today()` — 당일주요거래원요청

당일주요거래원요청 (Main Brokers Today) · `POST /api/dostk/rkinfo`

```python
api.ranking.main_brokers_today(stk_cd=...)
```

**요청**

| 필드 | 한글명 | 필수 | 길이 | 설명 |
|---|---|:---:|---:|---|
| `stk_cd` | 종목코드 | Y | 6 | 거래소별 종목코드 (KRX:039490,NXT:039490_NX,SOR:039490_AL) |

**응답**

| 필드 | 한글명 | 길이 | 설명 |
|---|---|---:|---|
| `sel_trde_ori_irds_1` | 매도거래원별증감1 |  | 단위: 1주, 부호가 포함된 숫자 |
| `sel_trde_ori_qty_1` | 매도거래원수량1 |  | 단위: 1주, 부호가 포함된 숫자 |
| `sel_trde_ori_1` | 매도거래원1 |  |   |
| `sel_trde_ori_cd_1` | 매도거래원코드1 |  |   |
| `buy_trde_ori_1` | 매수거래원1 |  |   |
| `buy_trde_ori_cd_1` | 매수거래원코드1 |  |   |
| `buy_trde_ori_qty_1` | 매수거래원수량1 |  | 단위: 1주, 부호가 포함된 숫자 |
| `buy_trde_ori_irds_1` | 매수거래원별증감1 |  | 단위: 1주, 부호가 포함된 숫자 |
| `sel_trde_ori_irds_2` | 매도거래원별증감2 |  | 단위: 1주, 부호가 포함된 숫자 |
| `sel_trde_ori_qty_2` | 매도거래원수량2 |  | 단위: 1주, 부호가 포함된 숫자 |
| `sel_trde_ori_2` | 매도거래원2 |  |   |
| `sel_trde_ori_cd_2` | 매도거래원코드2 |  |   |
| `buy_trde_ori_2` | 매수거래원2 |  |   |
| `buy_trde_ori_cd_2` | 매수거래원코드2 |  |   |
| `buy_trde_ori_qty_2` | 매수거래원수량2 |  | 단위: 1주, 부호가 포함된 숫자 |
| `buy_trde_ori_irds_2` | 매수거래원별증감2 |  | 단위: 1주, 부호가 포함된 숫자 |
| `sel_trde_ori_irds_3` | 매도거래원별증감3 |  | 단위: 1주, 부호가 포함된 숫자 |
| `sel_trde_ori_qty_3` | 매도거래원수량3 |  | 단위: 1주, 부호가 포함된 숫자 |
| `sel_trde_ori_3` | 매도거래원3 |  |   |
| `sel_trde_ori_cd_3` | 매도거래원코드3 |  |   |
| `buy_trde_ori_3` | 매수거래원3 |  |   |
| `buy_trde_ori_cd_3` | 매수거래원코드3 |  |   |
| `buy_trde_ori_qty_3` | 매수거래원수량3 |  | 단위: 1주, 부호가 포함된 숫자 |
| `buy_trde_ori_irds_3` | 매수거래원별증감3 |  | 단위: 1주, 부호가 포함된 숫자 |
| `sel_trde_ori_irds_4` | 매도거래원별증감4 |  | 단위: 1주, 부호가 포함된 숫자 |
| `sel_trde_ori_qty_4` | 매도거래원수량4 |  | 단위: 1주, 부호가 포함된 숫자 |
| `sel_trde_ori_4` | 매도거래원4 |  |   |
| `sel_trde_ori_cd_4` | 매도거래원코드4 |  |   |
| `buy_trde_ori_4` | 매수거래원4 |  |   |
| `buy_trde_ori_cd_4` | 매수거래원코드4 |  |   |
| `buy_trde_ori_qty_4` | 매수거래원수량4 |  | 단위: 1주, 부호가 포함된 숫자 |
| `buy_trde_ori_irds_4` | 매수거래원별증감4 |  | 단위: 1주, 부호가 포함된 숫자 |
| `sel_trde_ori_irds_5` | 매도거래원별증감5 |  | 단위: 1주, 부호가 포함된 숫자 |
| `sel_trde_ori_qty_5` | 매도거래원수량5 |  | 단위: 1주, 부호가 포함된 숫자 |
| `sel_trde_ori_5` | 매도거래원5 |  |   |
| `sel_trde_ori_cd_5` | 매도거래원코드5 |  |   |
| `buy_trde_ori_5` | 매수거래원5 |  |   |
| `buy_trde_ori_cd_5` | 매수거래원코드5 |  |   |
| `buy_trde_ori_qty_5` | 매수거래원수량5 |  | 단위: 1주, 부호가 포함된 숫자 |
| `buy_trde_ori_irds_5` | 매수거래원별증감5 |  | 단위: 1주, 부호가 포함된 숫자 |
| `frgn_sel_prsm_sum_chang` | 외국계매도추정합변동 |  | 단위: 1주, 부호가 포함된 숫자 |
| `frgn_sel_prsm_sum` | 외국계매도추정합 |  | 단위: 1주, 부호가 포함된 숫자 |
| `frgn_buy_prsm_sum` | 외국계매수추정합 |  | 단위: 1주, 부호가 포함된 숫자 |
| `frgn_buy_prsm_sum_chang` | 외국계매수추정합변동 |  | 단위: 1주, 부호가 포함된 숫자 |
| `tdy_main_trde_ori` (list) | 당일주요거래원 |  |   |
| `tdy_main_trde_ori[].sel_scesn_tm` | 매도이탈시간 | 20 |   |
| `tdy_main_trde_ori[].sell_qty` | 매도수량 | 20 |   |
| `tdy_main_trde_ori[].sel_upper_scesn_ori` | 매도상위이탈원 | 20 |   |
| `tdy_main_trde_ori[].buy_scesn_tm` | 매수이탈시간 | 20 |   |
| `tdy_main_trde_ori[].buy_qty` | 매수수량 | 20 |   |
| `tdy_main_trde_ori[].buy_upper_scesn_ori` | 매수상위이탈원 | 20 |   |
| `tdy_main_trde_ori[].qry_dt` | 조회일자 | 20 |   |
| `tdy_main_trde_ori[].qry_tm` | 조회시간 | 20 |   |

<a id="ka10042"></a>

## `ka10042` · `top_net_buying_brokers()` — 순매수거래원순위요청

순매수거래원순위요청 (Top Net Buying Brokers) · `POST /api/dostk/rkinfo`

```python
api.ranking.top_net_buying_brokers(stk_cd=..., qry_dt_tp=..., pot_tp=..., sort_base=...)
```

**요청**

| 필드 | 한글명 | 필수 | 길이 | 설명 |
|---|---|:---:|---:|---|
| `stk_cd` | 종목코드 | Y | 6 | 거래소별 종목코드 (KRX:039490,NXT:039490_NX,SOR:039490_AL) |
| `strt_dt` | 시작일자 |  | 8 | YYYYMMDD (연도4자리, 월 2자리, 일 2자리 형식) |
| `end_dt` | 종료일자 |  | 8 | YYYYMMDD (연도4자리, 월 2자리, 일 2자리 형식) |
| `qry_dt_tp` | 조회기간구분 | Y | 1 | 0:기간으로 조회, 1:시작일자, 종료일자로 조회 |
| `pot_tp` | 시점구분 | Y | 1 | 0:당일, 1:전일 |
| `dt` | 기간 |  | 4 | 5:5일, 10:10일, 20:20일, 40:40일, 60:60일, 120:120일 |
| `sort_base` | 정렬기준 | Y | 1 | 1:종가순, 2:날짜순 |

**응답**

| 필드 | 한글명 | 길이 | 설명 |
|---|---|---:|---|
| `netprps_trde_ori_rank` (list) | 순매수거래원순위 |  |   |
| `netprps_trde_ori_rank[].rank` | 순위 | 20 |   |
| `netprps_trde_ori_rank[].mmcm_cd` | 회원사코드 | 20 |   |
| `netprps_trde_ori_rank[].mmcm_nm` | 회원사명 | 20 |   |

<a id="ka10053"></a>

## `ka10053` · `departed_brokers_today()` — 당일상위이탈원요청

당일상위이탈원요청 (Departed Brokers Today) · `POST /api/dostk/rkinfo`

```python
api.ranking.departed_brokers_today(stk_cd=...)
```

**요청**

| 필드 | 한글명 | 필수 | 길이 | 설명 |
|---|---|:---:|---:|---|
| `stk_cd` | 종목코드 | Y | 6 | 거래소별 종목코드 (KRX:039490,NXT:039490_NX,SOR:039490_AL) |

**응답**

| 필드 | 한글명 | 길이 | 설명 |
|---|---|---:|---|
| `tdy_upper_scesn_ori` (list) | 당일상위이탈원 |  |   |
| `tdy_upper_scesn_ori[].sel_scesn_tm` | 매도이탈시간 | 20 | HHmmss |
| `tdy_upper_scesn_ori[].sell_qty` | 매도수량 | 20 | 단위: 1주 |
| `tdy_upper_scesn_ori[].sel_upper_scesn_ori` | 매도상위이탈원 | 20 |   |
| `tdy_upper_scesn_ori[].buy_scesn_tm` | 매수이탈시간 | 20 | HHmmss |
| `tdy_upper_scesn_ori[].buy_qty` | 매수수량 | 20 | 단위: 1주 |
| `tdy_upper_scesn_ori[].buy_upper_scesn_ori` | 매수상위이탈원 | 20 |   |
| `tdy_upper_scesn_ori[].qry_dt` | 조회일자 | 20 |   |
| `tdy_upper_scesn_ori[].qry_tm` | 조회시간 | 20 |   |

<a id="ka10062"></a>

## `ka10062` · `same_day_net_buying_rank()` — 동일순매매순위요청

동일순매매순위요청 (Same Day Net Buying Rank) · `POST /api/dostk/rkinfo`

```python
api.ranking.same_day_net_buying_rank(strt_dt=..., mrkt_tp=..., trde_tp=..., sort_cnd=..., unit_tp=..., stex_tp=...)
```

**요청**

| 필드 | 한글명 | 필수 | 길이 | 설명 |
|---|---|:---:|---:|---|
| `strt_dt` | 시작일자 | Y | 8 | YYYYMMDD (연도4자리, 월 2자리, 일 2자리 형식) |
| `end_dt` | 종료일자 |  | 8 | YYYYMMDD (연도4자리, 월 2자리, 일 2자리 형식) |
| `mrkt_tp` | 시장구분 | Y | 3 | 000:전체, 001: 코스피, 101:코스닥 |
| `trde_tp` | 매매구분 | Y | 1 | 1:순매수, 2:순매도 |
| `sort_cnd` | 정렬조건 | Y | 1 | 1:수량, 2:금액 |
| `unit_tp` | 단위구분 | Y | 1 | 1:단주, 1000:천주 |
| `stex_tp` | 거래소구분 | Y | 1 | 1:KRX, 2:NXT 3.통합 |

**응답**

| 필드 | 한글명 | 길이 | 설명 |
|---|---|---:|---|
| `eql_nettrde_rank` (list) | 동일순매매순위 |  |   |
| `eql_nettrde_rank[].stk_cd` | 종목코드 | 20 |   |
| `eql_nettrde_rank[].rank` | 순위 | 20 |   |
| `eql_nettrde_rank[].stk_nm` | 종목명 | 40 |   |
| `eql_nettrde_rank[].cur_prc` | 현재가 | 20 | 단위: 원, 부호가 포함된 숫자 |
| `eql_nettrde_rank[].pre_sig` | 대비기호 | 20 |   |
| `eql_nettrde_rank[].pred_pre` | 전일대비 | 20 | 단위: 원, 부호가 포함된 숫자 |
| `eql_nettrde_rank[].flu_rt` | 등락율 | 20 | 단위: %, 부호 포함 소수점 둘째 자리까지 포맷된 백분율 |
| `eql_nettrde_rank[].acc_trde_qty` | 누적거래량 | 20 | 단위: 1주 |
| `eql_nettrde_rank[].orgn_nettrde_qty` | 기관순매매수량 | 20 | 단위: 1주 혹은 1000주(unit_tp파라미터로 설정), 부호가 포함된 숫자 |
| `eql_nettrde_rank[].orgn_nettrde_amt` | 기관순매매금액 | 20 | 단위: 백만원, 부호가 포함된 숫자 |
| `eql_nettrde_rank[].orgn_nettrde_avg_pric` | 기관순매매평균가 | 20 | 단위: 백만원 |
| `eql_nettrde_rank[].for_nettrde_qty` | 외인순매매수량 | 20 | 단위: 1주 혹은 1000주(unit_tp파라미터로 설정), 부호가 포함된 숫자 |
| `eql_nettrde_rank[].for_nettrde_amt` | 외인순매매금액 | 20 | 단위: 백만원, 부호가 포함된 숫자 |
| `eql_nettrde_rank[].for_nettrde_avg_pric` | 외인순매매평균가 | 20 | 단위: 백만원 |
| `eql_nettrde_rank[].nettrde_qty` | 순매매수량 | 20 | 단위: 1주 혹은 1000주(unit_tp파라미터로 설정), 부호가 포함된 숫자 |
| `eql_nettrde_rank[].nettrde_amt` | 순매매금액 | 20 | 단위: 백만원, 부호가 포함된 숫자 |

<a id="ka10065"></a>

## `ka10065` · `top_intraday_investor_trading()` — 장중투자자별매매상위요청

장중투자자별매매상위요청 (Top Intraday Investor Trading by Time) · `POST /api/dostk/rkinfo`

```python
api.ranking.top_intraday_investor_trading(trde_tp=..., mrkt_tp=..., orgn_tp=...)
```

**요청**

| 필드 | 한글명 | 필수 | 길이 | 설명 |
|---|---|:---:|---:|---|
| `trde_tp` | 매매구분 | Y | 1 | 1:순매수, 2:순매도 |
| `mrkt_tp` | 시장구분 | Y | 3 | 000:전체, 001:코스피, 101:코스닥 |
| `orgn_tp` | 기관구분 | Y | 4 | 9000:외국인, 9100:외국계, 1000:금융투자, 3000:투신, 5000:기타금융, 4000:은행, 2000:보험, 6000:연기금, 7000:국가, 7100:기타법인, 9999:기관계 |
| `amt_qty_tp` | 금액수량구분 |  | 1 | 1:금액, 2:수량 |

**응답**

| 필드 | 한글명 | 길이 | 설명 |
|---|---|---:|---|
| `opmr_invsr_trde_upper` (list) | 장중투자자별매매상위 |  |   |
| `opmr_invsr_trde_upper[].stk_cd` | 종목코드 | 20 |   |
| `opmr_invsr_trde_upper[].stk_nm` | 종목명 | 40 |   |
| `opmr_invsr_trde_upper[].sel_qty` | 매도금액/매도량 | 20 | 단위: 1주 혹은 백만원(amt_qty_tp파라미터로 설정), 부호가 있는 숫자 |
| `opmr_invsr_trde_upper[].buy_qty` | 매수금액/매수량 | 20 | 단위: 1주 혹은 백만원(amt_qty_tp파라미터로 설정), 부호가 있는 숫자 |
| `opmr_invsr_trde_upper[].netslmt` | 순매수/순매도 | 20 | 단위: 1주 혹은 백만원(trde_tp파라미터로 설정), 부호가 있는 숫자 |

<a id="ka10098"></a>

## `ka10098` · `after_hours_change_rate_rank()` — 시간외단일가등락율순위요청

시간외단일가등락율순위요청 (After Hours Change Rate Rank) · `POST /api/dostk/rkinfo`

```python
api.ranking.after_hours_change_rate_rank(mrkt_tp=..., sort_base=..., stk_cnd=..., trde_qty_cnd=..., crd_cnd=..., trde_prica=...)
```

**요청**

| 필드 | 한글명 | 필수 | 길이 | 설명 |
|---|---|:---:|---:|---|
| `mrkt_tp` | 시장구분 | Y | 3 | 000:전체,001:코스피,101:코스닥 |
| `sort_base` | 정렬기준 | Y | 1 | 1:상승률, 2:상승폭, 3:하락률, 4:하락폭, 5:보합 |
| `stk_cnd` | 종목조건 | Y | 2 | 0:전체조회,1:관리종목제외,2:정리매매종목제외,3:우선주제외,4:관리종목우선주제외,5:증100제외,6:증100만보기,7:증40만보기,8:증30만보기,9:증20만보기,12:증50만보기,13:증60만보기,14:ETF제외,15:스팩제외,16:ETF+ETN제외,17:ETN제외 |
| `trde_qty_cnd` | 거래량조건 | Y | 5 | 0:전체조회, 10:백주이상,50:5백주이상,100;천주이상, 500:5천주이상, 1000:만주이상, 5000:5만주이상, 10000:10만주이상 |
| `crd_cnd` | 신용조건 | Y | 1 | 0:전체조회, 9:신용융자전체, 1:신용융자A군, 2:신용융자B군, 3:신용융자C군, 4:신용융자D군, 7:신용융자E군, 8:신용대주, 5:신용한도초과제외 |
| `trde_prica` | 거래대금 | Y | 5 | 0:전체조회, 5:5백만원이상,10:1천만원이상, 30:3천만원이상, 50:5천만원이상, 100:1억원이상, 300:3억원이상, 500:5억원이상, 1000:10억원이상, 3000:30억원이상, 5000:50억원이상, 10000:100억원이상 |

**응답**

| 필드 | 한글명 | 길이 | 설명 |
|---|---|---:|---|
| `ovt_sigpric_flu_rt_rank` (list) | 시간외단일가등락율순위 |  |   |
| `ovt_sigpric_flu_rt_rank[].rank` | 순위 | 20 |   |
| `ovt_sigpric_flu_rt_rank[].stk_cd` | 종목코드 | 20 |   |
| `ovt_sigpric_flu_rt_rank[].stk_nm` | 종목명 | 40 |   |
| `ovt_sigpric_flu_rt_rank[].cur_prc` | 현재가 | 20 | 단위: 원, 부호가 포함된 숫자 |
| `ovt_sigpric_flu_rt_rank[].pred_pre_sig` | 전일대비기호 | 20 | 1: 상한가, 2:상승, 3:보합, 4:하한가, 5:하락 |
| `ovt_sigpric_flu_rt_rank[].pred_pre` | 전일대비 | 20 | 단위: 원, 부호가 포함된 숫자 |
| `ovt_sigpric_flu_rt_rank[].flu_rt` | 등락률 | 20 | 단위: %, 부호 포함 소수점 둘째 자리까지 포맷된 백분율 |
| `ovt_sigpric_flu_rt_rank[].sel_tot_req` | 매도총잔량 | 20 | 단위: 1주 |
| `ovt_sigpric_flu_rt_rank[].buy_tot_req` | 매수총잔량 | 20 | 단위: 1주 |
| `ovt_sigpric_flu_rt_rank[].acc_trde_qty` | 누적거래량 | 20 | 단위: 1주 |
| `ovt_sigpric_flu_rt_rank[].acc_trde_prica` | 누적거래대금 | 20 | 단위: 백만원 |
| `ovt_sigpric_flu_rt_rank[].tdy_close_pric` | 당일종가 | 20 | 단위: 원 |
| `ovt_sigpric_flu_rt_rank[].tdy_close_pric_flu_rt` | 당일종가등락률 | 20 | 단위: %, 부호 포함 소수점 둘째 자리까지 포맷된 백분율 |

<a id="ka90009"></a>

## `ka90009` · `top_foreign_institution_trades()` — 외국인기관매매상위요청

외국인기관매매상위요청 (Top Foreign Institution Trades) · `POST /api/dostk/rkinfo`

```python
api.ranking.top_foreign_institution_trades(mrkt_tp=..., amt_qty_tp=..., qry_dt_tp=..., stex_tp=...)
```

**요청**

| 필드 | 한글명 | 필수 | 길이 | 설명 |
|---|---|:---:|---:|---|
| `mrkt_tp` | 시장구분 | Y | 3 | 000:전체, 001:코스피, 101:코스닥 |
| `amt_qty_tp` | 금액수량구분 | Y | 1 | 1:금액(천만), 2:수량(천) |
| `qry_dt_tp` | 조회일자구분 | Y | 1 | 0:조회일자 미포함, 1:조회일자 포함 |
| `date` | 날짜 |  | 8 | YYYYMMDD (연도4자리, 월 2자리, 일 2자리 형식) |
| `stex_tp` | 거래소구분 | Y | 1 | 1:KRX, 2:NXT, 3:통합 |

**응답**

| 필드 | 한글명 | 길이 | 설명 |
|---|---|---:|---|
| `frgnr_orgn_trde_upper` (list) | 외국인기관매매상위 |  |   |
| `frgnr_orgn_trde_upper[].for_netslmt_stk_cd` | 외인순매도종목코드 | 20 |   |
| `frgnr_orgn_trde_upper[].for_netslmt_stk_nm` | 외인순매도종목명 | 20 |   |
| `frgnr_orgn_trde_upper[].for_netslmt_amt` | 외인순매도금액 | 20 | 단위: 천만, 부호가 포함된 숫자 |
| `frgnr_orgn_trde_upper[].for_netslmt_qty` | 외인순매도수량 | 20 | 단위: 1000주(천주), 부호가 포함된 숫자 |
| `frgnr_orgn_trde_upper[].for_netprps_stk_cd` | 외인순매수종목코드 | 20 |   |
| `frgnr_orgn_trde_upper[].for_netprps_stk_nm` | 외인순매수종목명 | 20 |   |
| `frgnr_orgn_trde_upper[].for_netprps_amt` | 외인순매수금액 | 20 | 단위: 천만, 부호가 포함된 숫자 |
| `frgnr_orgn_trde_upper[].for_netprps_qty` | 외인순매수수량 | 20 | 단위: 1000주(천주), 부호가 포함된 숫자 |
| `frgnr_orgn_trde_upper[].orgn_netslmt_stk_cd` | 기관순매도종목코드 | 20 |   |
| `frgnr_orgn_trde_upper[].orgn_netslmt_stk_nm` | 기관순매도종목명 | 20 |   |
| `frgnr_orgn_trde_upper[].orgn_netslmt_amt` | 기관순매도금액 | 20 | 단위: 천만, 부호가 포함된 숫자 |
| `frgnr_orgn_trde_upper[].orgn_netslmt_qty` | 기관순매도수량 | 20 | 단위: 1000주(천주), 부호가 포함된 숫자 |
| `frgnr_orgn_trde_upper[].orgn_netprps_stk_cd` | 기관순매수종목코드 | 20 |   |
| `frgnr_orgn_trde_upper[].orgn_netprps_stk_nm` | 기관순매수종목명 | 20 |   |
| `frgnr_orgn_trde_upper[].orgn_netprps_amt` | 기관순매수금액 | 20 | 단위: 천만, 부호가 포함된 숫자 |
| `frgnr_orgn_trde_upper[].orgn_netprps_qty` | 기관순매수수량 | 20 | 단위: 1000주(천주), 부호가 포함된 숫자 |
