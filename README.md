# kiwoom-rest-api

키움증권 REST API를 Python으로 쉽게 사용할 수 있는 래퍼 라이브러리입니다.

국내주식 **207개 엔드포인트**와 **19종 실시간 WebSocket 데이터**를 지원합니다.

## 설치

```bash
pip install kiwoom-rest-api
```

소스에서 설치:
```bash
git clone https://github.com/younghwan91/kiwoom-rest-api.git
cd kiwoom-rest-api
pip install -e .
```

## 사전 준비

1. [키움 REST API 포털](https://openapi.kiwoom.com)에 가입합니다.
2. **API 사용신청**을 통해 `앱키(appkey)`와 `시크릿키(secretkey)`를 발급받습니다.
3. 처음에는 **모의투자**(`is_mock=True`)로 테스트한 뒤, 실전투자로 전환하세요.

## 빠른 시작

### 1단계: 로그인

```python
from kiwoom_rest_api import KiwoomAPI

# 모의투자 서버로 연결
api = KiwoomAPI(
    app_key="발급받은_앱키",
    app_secret="발급받은_시크릿키",
    is_mock=True,  # True=모의투자, False=실전투자
)

# 접근토큰 발급 (모든 API 호출 전에 반드시 필요)
api.login()
```

### 2단계: 종목 조회

```python
# 삼성전자(005930) 기본 정보 조회
info = api.stock_info.basic_stock_info(stk_cd="005930")
print(info)

# 삼성전자 일봉 차트 조회
chart = api.chart.stock_daily_chart(stk_cd="005930", base_dt="20260326")

# 당일 거래량 상위 종목 조회
ranking = api.ranking.top_volume_today()
```

### 3단계: 계좌 조회

```python
# 내 계좌 평가 현황
evaluation = api.account.account_evaluation()

# 예수금 상세 조회
deposit = api.account.deposit_detail()

# 체결 잔고 조회
position = api.account.filled_position()

# 미체결 주문 조회
unfilled = api.account.unfilled_orders()
```

### 4단계: 주문

```python
# 삼성전자 10주 지정가 매수
result = api.order.buy_order(
    dmst_stex_tp="01",   # 거래소 구분 (01: KRX)
    stk_cd="005930",     # 종목코드
    ord_qty=10,          # 주문 수량
    trde_tp="00",        # 주문 유형 (00: 지정가)
    ord_uv=70000,        # 주문 단가
)

# 매도 주문
api.order.sell_order(
    dmst_stex_tp="01",
    stk_cd="005930",
    ord_qty=10,
    trde_tp="00",
    ord_uv=75000,
)

# 주문 정정
api.order.modify_order(org_ord_no="원래주문번호", ord_qty=5, ord_uv=71000)

# 주문 취소
api.order.cancel_order(org_ord_no="원래주문번호", ord_qty=5)
```

### 5단계: 로그아웃

```python
api.logout()
```

## 실시간 WebSocket 데이터

실시간 체결가, 호가, 잔고 변동 등을 WebSocket으로 수신할 수 있습니다.

```python
import asyncio
from kiwoom_rest_api import KiwoomAPI

api = KiwoomAPI(app_key="앱키", app_secret="시크릿키")
api.login()

ws = api.create_websocket()

async def main():
    await ws.connect()

    # 실시간 체결 데이터 수신 콜백 등록
    ws.on("0B", lambda data: print(f"체결: {data}"))

    # 호가잔량 데이터 수신 콜백 등록
    ws.on("0D", lambda data: print(f"호가: {data}"))

    # 삼성전자 실시간 체결+호가 구독
    await ws.subscribe("0B", "005930")
    await ws.subscribe("0D", "005930")

    # 여러 종목 동시 구독도 가능
    await ws.subscribe("0B", ["005930", "000660", "035420"])

    # 메시지 수신 대기 (Ctrl+C로 종료)
    await ws.listen()

asyncio.run(main())
```

## 연속 조회 (페이지네이션)

데이터가 많은 API는 한 번에 모든 데이터를 반환하지 않습니다.
응답 헤더의 `cont_yn`이 `"Y"`이면 다음 페이지가 있다는 뜻입니다.

```python
# 방법 1: 수동 연속 조회
result = api.account.filled_orders()
# result에 cont_yn="Y"와 next_key가 있으면 다음 페이지 조회
next_result = api.account.filled_orders(cont_yn="Y", next_key=result["next_key"])

# 방법 2: 자동 전체 조회 (모든 페이지를 한번에)
from kiwoom_rest_api.base import BaseClient
all_data = api._client.request_all(
    "/api/dostk/acnt", "ka10076",
    data_key="filled_list",  # 응답에서 리스트 데이터의 키 이름
)
```

## 에러 처리

```python
from kiwoom_rest_api.base import KiwoomAPIError

try:
    result = api.order.buy_order(stk_cd="005930", ord_qty=10, ord_uv=70000)
except KiwoomAPIError as e:
    print(f"에러 코드: {e.code}")
    print(f"에러 메시지: {e.message}")
    print(f"전체 응답: {e.response}")
```

## 환경 설정

| 구분 | 실전투자 | 모의투자 |
|------|---------|---------|
| `is_mock` | `False` (기본값) | `True` |
| REST URL | `https://api.kiwoom.com` | `https://mockapi.kiwoom.com` |
| WebSocket URL | `wss://api.kiwoom.com:10000` | `wss://mockapi.kiwoom.com:10000` |

## 지원 API 목록

### 인증

```python
api.login()      # 접근토큰 발급 (au10001)
api.logout()     # 접근토큰 폐기 (au10002)
```

### 페이지네이션 (연속조회)

```python
# 단일 조회
result = api.stock_info.basic_stock_info(stk_cd="005930")

# 연속 조회 (다음 페이지)
result = api.account.filled_orders(cont_yn="Y", next_key="다음키값")
```

---

### 계좌 (`api.account`) - 33개

| 메서드 | API ID | 설명 |
|--------|--------|------|
| `realized_profit_by_date()` | ka10072 | 일자별종목별실현손익요청_일자 |
| `realized_profit_by_period()` | ka10073 | 일자별종목별실현손익요청_기간 |
| `daily_realized_profit()` | ka10074 | 일자별실현손익요청 |
| `unfilled_orders()` | ka10075 | 미체결요청 |
| `filled_orders()` | ka10076 | 체결요청 |
| `today_realized_profit_detail()` | ka10077 | 당일실현손익상세요청 |
| `account_return_rate()` | ka10085 | 계좌수익률요청 |
| `unfilled_split_order_detail()` | ka10088 | 미체결 분할주문 상세 |
| `today_trading_journal()` | ka10170 | 당일매매일지요청 |
| `deposit_detail()` | kt00001 | 예수금상세현황요청 |
| `daily_estimated_deposit()` | kt00002 | 일별추정예탁자산현황요청 |
| `estimated_asset()` | kt00003 | 추정자산조회요청 |
| `account_evaluation()` | kt00004 | 계좌평가현황요청 |
| `filled_position()` | kt00005 | 체결잔고요청 |
| `order_execution_detail()` | kt00007 | 계좌별주문체결내역상세요청 |
| `next_day_settlement()` | kt00008 | 계좌별익일결제예정내역요청 |
| `order_execution_status()` | kt00009 | 계좌별주문체결현황요청 |
| `withdrawable_amount()` | kt00010 | 주문인출가능금액요청 |
| `orderable_qty_by_margin()` | kt00011 | 증거금율별주문가능수량조회요청 |
| `orderable_qty_by_credit()` | kt00012 | 신용보증금율별주문가능수량조회요청 |
| `margin_detail()` | kt00013 | 증거금세부내역조회요청 |
| `comprehensive_transaction_history()` | kt00015 | 위탁종합거래내역요청 |
| `daily_return_detail()` | kt00016 | 일별계좌수익률상세현황요청 |
| `today_account_status()` | kt00017 | 계좌별당일현황요청 |
| `evaluation_balance_detail()` | kt00018 | 계좌평가잔고내역요청 |
| `account_number_inquiry()` | ka00001 | 계좌번호조회 |
| `daily_balance_return_rate()` | ka01690 | 일별잔고수익률 |
| `gold_spot_balance()` | kt50020 | 금현물 잔고확인 |
| `gold_spot_deposit()` | kt50021 | 금현물 예수금 |
| `gold_spot_order_execution_all()` | kt50030 | 금현물 주문체결전체조회 |
| `gold_spot_order_execution()` | kt50031 | 금현물 주문체결조회 |
| `gold_spot_transaction_history()` | kt50032 | 금현물 거래내역조회 |
| `gold_spot_unfilled_orders()` | kt50075 | 금현물 미체결조회 |

### 종목정보 (`api.stock_info`) - 31개

| 메서드 | API ID | 설명 |
|--------|--------|------|
| `basic_stock_info()` | ka10001 | 주식기본정보요청 |
| `stock_trading_agent()` | ka10002 | 주식거래원요청 |
| `execution_info()` | ka10003 | 체결정보요청 |
| `credit_trading_trend()` | ka10013 | 신용매매동향요청 |
| `daily_transaction_detail()` | ka10015 | 일별거래상세요청 |
| `new_high_low()` | ka10016 | 신고저가요청 |
| `upper_lower_limit()` | ka10017 | 상하한가요청 |
| `near_high_low()` | ka10018 | 고저가근접요청 |
| `rapid_price_change()` | ka10019 | 가격급등락요청 |
| `trading_volume_update()` | ka10024 | 거래량갱신요청 |
| `volume_concentration()` | ka10025 | 매물대집중요청 |
| `high_low_per()` | ka10026 | 고저PER요청 |
| `change_rate_vs_opening()` | ka10028 | 시가대비등락률요청 |
| `trading_agent_supply_demand()` | ka10043 | 거래원매물대분석요청 |
| `trading_agent_instant_volume()` | ka10052 | 거래원순간거래량요청 |
| `vi_triggered_stocks()` | ka10054 | 변동성완화장치발동종목요청 |
| `today_vs_yesterday_volume()` | ka10055 | 당일전일체결량요청 |
| `daily_trading_by_investor()` | ka10058 | 투자자별일별매매종목요청 |
| `investor_institution_by_stock()` | ka10059 | 종목별투자자기관별요청 |
| `investor_institution_aggregate()` | ka10061 | 종목별투자자기관별합계요청 |
| `today_vs_yesterday_execution()` | ka10084 | 당일전일체결요청 |
| `watchlist_stock_info()` | ka10095 | 관심종목정보요청 |
| `stock_info_list()` | ka10099 | 종목정보 리스트 |
| `stock_info_inquiry()` | ka10100 | 종목정보 조회 |
| `industry_code_list()` | ka10101 | 업종코드 리스트 |
| `member_company_list()` | ka10102 | 회원사 리스트 |
| `program_buy_top50()` | ka90003 | 프로그램순매수상위50요청 |
| `program_trading_by_stock()` | ka90004 | 종목별프로그램매매현황요청 |
| `realtime_stock_inquiry_rank()` | ka00198 | 실시간종목조회순위 |
| `margin_loan_available_stocks()` | kt20016 | 신용융자 가능종목요청 |
| `margin_loan_inquiry()` | kt20017 | 신용융자 가능문의 |

### 시세 (`api.market`) - 25개

| 메서드 | API ID | 설명 |
|--------|--------|------|
| `stock_quote()` | ka10004 | 주식호가요청 |
| `stock_daily_weekly_monthly()` | ka10005 | 주식일주월시분요청 |
| `stock_minute_price()` | ka10006 | 주식시분요청 |
| `order_book_info()` | ka10007 | 시세표성정보요청 |
| `rights_issue_price()` | ka10011 | 신주인수권전체시세요청 |
| `daily_institutional_trading()` | ka10044 | 일별기관매매종목요청 |
| `institutional_trading_trend()` | ka10045 | 종목별기관매매추이요청 |
| `hourly_execution_strength()` | ka10046 | 체결강도추이시간별요청 |
| `daily_execution_strength()` | ka10047 | 체결강도추이일별요청 |
| `intraday_investor_trading()` | ka10063 | 장중투자자별매매요청 |
| `after_hours_investor_trading()` | ka10066 | 장마감후투자자별매매요청 |
| `broker_stock_trading_trend()` | ka10078 | 증권사별종목매매동향요청 |
| `daily_stock_price()` | ka10086 | 일별주가요청 |
| `after_hours_single_price()` | ka10087 | 시간외단일가요청 |
| `program_trading_by_time()` | ka90005 | 프로그램매매추이요청 시간대별 |
| `program_arbitrage_balance()` | ka90006 | 프로그램매매차익잔고추이요청 |
| `cumulative_program_trading()` | ka90007 | 프로그램매매누적추이요청 |
| `program_trading_by_stock_time()` | ka90008 | 종목시간별프로그램매매추이요청 |
| `program_trading_by_date()` | ka90010 | 프로그램매매추이요청 일자별 |
| `program_trading_by_stock_day()` | ka90013 | 종목일별프로그램매매추이요청 |
| `gold_spot_execution_trend()` | ka50010 | 금현물체결추이 |
| `gold_spot_daily_trend()` | ka50012 | 금현물일별추이 |
| `gold_spot_expected_execution()` | ka50087 | 금현물예상체결 |
| `gold_spot_price_info()` | ka50100 | 금현물 시세정보 |
| `gold_spot_order_book()` | ka50101 | 금현물 호가 |

### 주문 (`api.order`) - 8개

| 메서드 | API ID | 설명 |
|--------|--------|------|
| `buy_order()` | kt10000 | 주식 매수주문 |
| `sell_order()` | kt10001 | 주식 매도주문 |
| `modify_order()` | kt10002 | 주식 정정주문 |
| `cancel_order()` | kt10003 | 주식 취소주문 |
| `gold_spot_buy_order()` | kt50000 | 금현물 매수주문 |
| `gold_spot_sell_order()` | kt50001 | 금현물 매도주문 |
| `gold_spot_modify_order()` | kt50002 | 금현물 정정주문 |
| `gold_spot_cancel_order()` | kt50003 | 금현물 취소주문 |

### 신용주문 (`api.credit_order`) - 4개

| 메서드 | API ID | 설명 |
|--------|--------|------|
| `margin_buy_order()` | kt10006 | 신용 매수주문 |
| `margin_sell_order()` | kt10007 | 신용 매도주문 |
| `margin_modify_order()` | kt10008 | 신용 정정주문 |
| `margin_cancel_order()` | kt10009 | 신용 취소주문 |

### 차트 (`api.chart`) - 21개

| 메서드 | API ID | 설명 |
|--------|--------|------|
| `investor_institution_chart()` | ka10060 | 종목별투자자기관별차트요청 |
| `intraday_investor_chart()` | ka10064 | 장중투자자별매매차트요청 |
| `stock_tick_chart()` | ka10079 | 주식틱차트조회요청 |
| `stock_minute_chart()` | ka10080 | 주식분봉차트조회요청 |
| `stock_daily_chart()` | ka10081 | 주식일봉차트조회요청 |
| `stock_weekly_chart()` | ka10082 | 주식주봉차트조회요청 |
| `stock_monthly_chart()` | ka10083 | 주식월봉차트조회요청 |
| `stock_yearly_chart()` | ka10094 | 주식년봉차트조회요청 |
| `industry_tick_chart()` | ka20004 | 업종틱차트조회요청 |
| `industry_minute_chart()` | ka20005 | 업종분봉조회요청 |
| `industry_daily_chart()` | ka20006 | 업종일봉조회요청 |
| `industry_weekly_chart()` | ka20007 | 업종주봉조회요청 |
| `industry_monthly_chart()` | ka20008 | 업종월봉조회요청 |
| `industry_yearly_chart()` | ka20019 | 업종년봉조회요청 |
| `gold_spot_tick_chart()` | ka50079 | 금현물틱차트조회요청 |
| `gold_spot_minute_chart()` | ka50080 | 금현물분봉차트조회요청 |
| `gold_spot_daily_chart()` | ka50081 | 금현물일봉차트조회요청 |
| `gold_spot_weekly_chart()` | ka50082 | 금현물주봉차트조회요청 |
| `gold_spot_monthly_chart()` | ka50083 | 금현물월봉차트조회요청 |
| `gold_spot_intraday_tick_chart()` | ka50091 | 금현물당일틱차트조회요청 |
| `gold_spot_intraday_minute_chart()` | ka50092 | 금현물당일분봉차트조회요청 |

### 순위정보 (`api.ranking`) - 23개

| 메서드 | API ID | 설명 |
|--------|--------|------|
| `top_order_book_volume()` | ka10020 | 호가잔량상위요청 |
| `sudden_order_book_increase()` | ka10021 | 호가잔량급증요청 |
| `sudden_order_ratio_increase()` | ka10022 | 잔량율급증요청 |
| `sudden_volume_increase()` | ka10023 | 거래량급증요청 |
| `top_change_rate()` | ka10027 | 전일대비등락률상위요청 |
| `top_expected_change_rate()` | ka10029 | 예상체결등락률상위요청 |
| `top_volume_today()` | ka10030 | 당일거래량상위요청 |
| `top_volume_yesterday()` | ka10031 | 전일거래량상위요청 |
| `top_trading_value()` | ka10032 | 거래대금상위요청 |
| `top_credit_ratio()` | ka10033 | 신용비율상위요청 |
| `top_foreign_trades_by_period()` | ka10034 | 외인기간별매매상위요청 |
| `top_foreign_consecutive_buy()` | ka10035 | 외인연속순매매상위요청 |
| `top_foreign_limit_increase()` | ka10036 | 외인한도소진율증가상위 |
| `top_foreign_broker_trading()` | ka10037 | 외국계창구매매상위요청 |
| `broker_ranking_by_stock()` | ka10038 | 종목별증권사순위요청 |
| `top_broker_by_stock()` | ka10039 | 증권사별매매상위요청 |
| `main_brokers_today()` | ka10040 | 당일주요거래원요청 |
| `top_net_buying_brokers()` | ka10042 | 순매수거래원순위요청 |
| `departed_brokers_today()` | ka10053 | 당일상위이탈원요청 |
| `same_day_net_buying_rank()` | ka10062 | 동일순매매순위요청 |
| `top_intraday_investor_trading()` | ka10065 | 장중투자자별매매상위요청 |
| `after_hours_change_rate_rank()` | ka10098 | 시간외단일가등락율순위요청 |
| `top_foreign_institution_trades()` | ka90009 | 외국인기관매매상위요청 |

### 업종 (`api.sector`) - 6개

| 메서드 | API ID | 설명 |
|--------|--------|------|
| `industry_program_trading()` | ka10010 | 업종프로그램요청 |
| `industry_investor_net_buy()` | ka10051 | 업종별투자자순매수요청 |
| `industry_current_price()` | ka20001 | 업종현재가요청 |
| `industry_stock_price()` | ka20002 | 업종별주가요청 |
| `all_industry_index()` | ka20003 | 전업종지수요청 |
| `industry_daily_price()` | ka20009 | 업종현재가일별요청 |

### 기관/외국인 (`api.foreign_institution`) - 4개

| 메서드 | API ID | 설명 |
|--------|--------|------|
| `foreign_trading_trend()` | ka10008 | 주식외국인종목별매매동향 |
| `institutional_stock()` | ka10009 | 주식기관요청 |
| `consecutive_trading_status()` | ka10131 | 기관외국인연속매매현황요청 |
| `gold_spot_investor_status()` | ka52301 | 금현물투자자현황 |

### 공매도 (`api.short_selling`) - 1개

| 메서드 | API ID | 설명 |
|--------|--------|------|
| `short_selling_trend()` | ka10014 | 공매도추이요청 |

### 대차거래 (`api.slb`) - 4개

| 메서드 | API ID | 설명 |
|--------|--------|------|
| `lending_trend()` | ka10068 | 대차거래추이요청 |
| `top10_lending()` | ka10069 | 대차거래상위10종목요청 |
| `lending_trend_by_stock()` | ka20068 | 대차거래추이요청(종목별) |
| `lending_details()` | ka90012 | 대차거래내역요청 |

### 테마 (`api.theme`) - 2개

| 메서드 | API ID | 설명 |
|--------|--------|------|
| `theme_group_list()` | ka90001 | 테마그룹별요청 |
| `theme_component_stocks()` | ka90002 | 테마구성종목요청 |

### 조건검색 (`api.condition_search`) - 4개 (WebSocket)

| 메서드 | API ID | 설명 |
|--------|--------|------|
| `condition_list()` | ka10171 | 조건검색 목록조회 |
| `condition_search()` | ka10172 | 조건검색 요청 일반 |
| `condition_search_realtime()` | ka10173 | 조건검색 요청 실시간 |
| `condition_search_cancel()` | ka10174 | 조건검색 실시간 해제 |

### ELW (`api.elw`) - 11개

| 메서드 | API ID | 설명 |
|--------|--------|------|
| `daily_sensitivity_indicator()` | ka10048 | ELW일별민감도지표요청 |
| `sensitivity_indicator()` | ka10050 | ELW민감도지표요청 |
| `price_spike()` | ka30001 | ELW가격급등락요청 |
| `top_net_buying_by_broker()` | ka30002 | 거래원별ELW순매매상위요청 |
| `lp_daily_holding_trend()` | ka30003 | ELWLP보유일별추이요청 |
| `premium_rate()` | ka30004 | ELW괴리율요청 |
| `condition_search()` | ka30005 | ELW조건검색요청 |
| `change_rate_ranking()` | ka30009 | ELW등락율순위요청 |
| `order_volume_ranking()` | ka30010 | ELW잔량순위요청 |
| `proximity_rate()` | ka30011 | ELW근접율요청 |
| `detailed_stock_info()` | ka30012 | ELW종목상세정보요청 |

### ETF (`api.etf`) - 9개

| 메서드 | API ID | 설명 |
|--------|--------|------|
| `return_rate()` | ka40001 | ETF수익율요청 |
| `stock_info()` | ka40002 | ETF종목정보요청 |
| `daily_trend()` | ka40003 | ETF일별추이요청 |
| `overall_market_price()` | ka40004 | ETF전체시세요청 |
| `time_segment_trend()` | ka40006 | ETF시간대별추이요청 |
| `time_segment_execution()` | ka40007 | ETF시간대별체결요청 |
| `daily_execution()` | ka40008 | ETF일자별체결요청 |
| `time_nav()` | ka40009 | ETF시간대별체결요청 |
| `time_trend()` | ka40010 | ETF시간대별추이요청 |

### 실시간시세 (`api.create_websocket()`) - 19종

| 코드 | 설명 |
|------|------|
| 00 | 주문체결 |
| 04 | 잔고 |
| 0A | 주식기세 |
| 0B | 주식체결 |
| 0C | 주식우선호가 |
| 0D | 주식호가잔량 |
| 0E | 주식시간외호가 |
| 0F | 주식당일거래원 |
| 0G | ETF NAV |
| 0H | 주식예상체결 |
| 0I | 국제금환산가격 |
| 0J | 업종지수 |
| 0U | 업종등락 |
| 0g | 주식종목정보 |
| 0m | ELW 이론가 |
| 0s | 장시작시간 |
| 0u | ELW 지표 |
| 0w | 종목프로그램매매 |
| 1h | VI발동/해제 |

## 참고

- 공식 API 가이드: https://openapi.kiwoom.com/guide/apiguide
- 모의투자는 KRX만 지원됩니다.
- 모든 API 이름은 키움증권 공식 가이드 기준입니다.

## 라이선스

MIT
