<!-- 자동 생성 파일 — 손으로 고치지 마세요. `python scripts/gen_docs.py` 가 TR 카탈로그(kiwoom_client.spec)로 다시 만듭니다. -->

# `api.theme` — 테마 (Theme)

요청·응답 필드는 키움 공식 REST API 명세에서 만든 TR 카탈로그([출처·라이선스](https://github.com/younghwan91/kiwoom-client/blob/main/src/kiwoom_client/spec/SOURCE.md))를 그대로 옮긴 것입니다. 뜻이 애매하면 [키움 REST API 포털](https://openapi.kiwoom.com)이 기준입니다. 값은 모두 문자열로 넘깁니다.

공통 헤더(`api-id`·`cont-yn`·`next-key`·`authorization`)는 라이브러리가 채웁니다 — 연속조회는 메서드의 `cont_yn`·`next_key` 인자나 `request_all()` 을 쓰세요.

| api_id | 메서드 | 이름 |
|---|---|---|
| [`ka90001`](#ka90001) | `theme_group_list()` | 테마그룹별요청 |
| [`ka90002`](#ka90002) | `theme_component_stocks()` | 테마구성종목요청 |

<a id="ka90001"></a>

## `ka90001` · `theme_group_list()` — 테마그룹별요청

테마그룹별요청 (Theme Group List) · `POST /api/dostk/thme`

```python
api.theme.theme_group_list(qry_tp=..., date_tp=..., flu_pl_amt_tp=..., stex_tp=...)
```

**요청**

| 필드 | 한글명 | 필수 | 길이 | 설명 |
|---|---|:---:|---:|---|
| `qry_tp` | 검색구분 | Y | 1 | 0:전체검색, 1:테마검색, 2:종목검색 |
| `stk_cd` | 종목코드 |  | 6 | 검색하려는 종목코드 |
| `date_tp` | 날짜구분 | Y | 2 | n일전 (1일 ~ 99일 날짜입력) |
| `thema_nm` | 테마명 |  | 50 | 검색하려는 테마명 |
| `flu_pl_amt_tp` | 등락수익구분 | Y | 1 | 1:상위기간수익률, 2:하위기간수익률, 3:상위등락률, 4:하위등락률 |
| `stex_tp` | 거래소구분 | Y | 1 | 1:KRX, 2:NXT 3.통합 |

**응답**

| 필드 | 한글명 | 길이 | 설명 |
|---|---|---:|---|
| `thema_grp` (list) | 테마그룹별 |  |   |
| `thema_grp[].thema_grp_cd` | 테마그룹코드 | 20 |   |
| `thema_grp[].thema_nm` | 테마명 | 20 |   |
| `thema_grp[].stk_num` | 종목수 | 20 |   |
| `thema_grp[].flu_sig` | 등락기호 | 20 | 1: 상한가, 2:상승, 3:보합, 4:하한가, 5:하락 |
| `thema_grp[].flu_rt` | 등락율 | 20 | 단위: %, 부호 포함 소수점 둘째 자리까지 포맷된 백분율 |
| `thema_grp[].rising_stk_num` | 상승종목수 | 20 |   |
| `thema_grp[].fall_stk_num` | 하락종목수 | 20 |   |
| `thema_grp[].dt_prft_rt` | 기간수익률 | 20 | 단위: %, 부호 포함 소수점 둘째 자리까지 포맷된 백분율 |
| `thema_grp[].main_stk` | 주요종목 | 20 |   |

<a id="ka90002"></a>

## `ka90002` · `theme_component_stocks()` — 테마구성종목요청

테마구성종목요청 (Theme Component Stocks) · `POST /api/dostk/thme`

```python
api.theme.theme_component_stocks(thema_grp_cd=..., stex_tp=...)
```

**요청**

| 필드 | 한글명 | 필수 | 길이 | 설명 |
|---|---|:---:|---:|---|
| `date_tp` | 날짜구분 |  | 1 | 1일 ~ 99일 날짜입력 |
| `thema_grp_cd` | 테마그룹코드 | Y | 6 | 테마그룹코드 번호 |
| `stex_tp` | 거래소구분 | Y | 1 | 1:KRX, 2:NXT 3.통합 |

**응답**

| 필드 | 한글명 | 길이 | 설명 |
|---|---|---:|---|
| `flu_rt` | 등락률 | 20 | 단위: %, 부호 포함 소수점 둘째 자리까지 포맷된 백분율 |
| `dt_prft_rt` | 기간수익률 | 20 | 단위: %, 부호 포함 소수점 둘째 자리까지 포맷된 백분율 |
| `thema_comp_stk` (list) | 테마구성종목 |  |   |
| `thema_comp_stk[].stk_cd` | 종목코드 | 20 |   |
| `thema_comp_stk[].stk_nm` | 종목명 | 40 |   |
| `thema_comp_stk[].cur_prc` | 현재가 | 20 | 단위: 원, 부호가 포함된 숫자 |
| `thema_comp_stk[].flu_sig` | 등락기호 | 20 | 1: 상한가, 2:상승, 3:보합, 4:하한가, 5:하락 |
| `thema_comp_stk[].pred_pre` | 전일대비 | 20 | 단위: 원, 부호가 포함된 숫자 |
| `thema_comp_stk[].flu_rt` | 등락율 | 20 | 단위: %, 부호 포함 소수점 둘째 자리까지 포맷된 백분율 |
| `thema_comp_stk[].acc_trde_qty` | 누적거래량 | 20 | 단위: 1주 |
| `thema_comp_stk[].sel_bid` | 매도호가 | 20 | 단위: 원, 부호가 포함된 숫자 |
| `thema_comp_stk[].sel_req` | 매도잔량 | 20 | 단위: 1주 |
| `thema_comp_stk[].buy_bid` | 매수호가 | 20 | 단위: 원, 부호가 포함된 숫자 |
| `thema_comp_stk[].buy_req` | 매수잔량 | 20 | 단위: 1주 |
| `thema_comp_stk[].dt_prft_rt_n` | 기간수익률n | 20 | 단위: %, 부호 포함 소수점 둘째 자리까지 포맷된 백분율 |
