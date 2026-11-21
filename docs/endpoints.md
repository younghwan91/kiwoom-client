<!-- 자동 생성 파일 — 손으로 고치지 마세요. `python scripts/gen_docs.py` 로 다시 만듭니다. -->

# 엔드포인트 전체 목록 (Endpoint reference)

kiwoom-client 가 감싼 키움 REST API **182개**, 조건검색 **4종**, 실시간 시세 **19종**을 코드에서 그대로 뽑은 표입니다.

- **api_id** 는 키움 공식 가이드의 TR 코드(`ka10001` 등)와 같습니다. 이 페이지에서 `Ctrl+F` 로 api_id·한글 TR 이름·메서드 이름 어느 것으로든 찾을 수 있습니다.
- 모든 REST 메서드는 시그니처가 같습니다: `(cont_yn="N", next_key="", **요청필드)`. 요청 필드는 키워드 인자로 그대로 넘기면 본문(JSON)이 됩니다 — 필드 목록은 [키움 REST API 가이드](https://openapi.kiwoom.com/guide/apiguide)에서 api_id 로 찾으세요.
- **MCP 도구 이름**은 `<모듈>_<메서드>` 입니다 (예: `stock_info_basic_stock_info`).
- ⚠️ 표시는 **실주문**입니다. `is_mock=False`(기본값) 로 부르면 실계좌에서 체결됩니다.

```python
from kiwoom_client import KiwoomAPI

api = KiwoomAPI(app_key="...", app_secret="...", is_mock=True)
info = api.stock_info.basic_stock_info(stk_cd="005930")  # ka10001
```

## 모듈 요약

| 모듈 | 이름 | 개수 | URL |
|---|---|---:|---|
| [`api.account`](#account) | 계좌 (Account) | 33 | `/api/dostk/acnt` |
| [`api.stock_info`](#stock_info) | 종목정보 (Stock info) | 31 | `/api/dostk/stkinfo` |
| [`api.market`](#market) | 시세 (Market) | 25 | `/api/dostk/mrkcond` |
| [`api.chart`](#chart) | 차트 (Chart) | 21 | `/api/dostk/chart` |
| [`api.order`](#order) | 주문 (Order) | 8 | `/api/dostk/ordr` |
| [`api.credit_order`](#credit_order) | 신용주문 (Credit order) | 4 | `/api/dostk/crdordr` |
| [`api.ranking`](#ranking) | 순위정보 (Ranking) | 23 | `/api/dostk/rkinfo` |
| [`api.sector`](#sector) | 업종 (Sector) | 6 | `/api/dostk/sect` |
| [`api.foreign_institution`](#foreign_institution) | 기관/외국인 (Foreign / institution) | 4 | `/api/dostk/frgnistt` |
| [`api.short_selling`](#short_selling) | 공매도 (Short selling) | 1 | `/api/dostk/shsa` |
| [`api.slb`](#slb) | 대차거래 (Stock lending & borrowing) | 4 | `/api/dostk/slb` |
| [`api.theme`](#theme) | 테마 (Theme) | 2 | `/api/dostk/thme` |
| [`api.condition_search`](#condition_search) | 조건검색 (Condition search) | 4 | WebSocket (`trnm`) |
| [`api.elw`](#elw) | ELW | 11 | `/api/dostk/elw` |
| [`api.etf`](#etf) | ETF | 9 | `/api/dostk/etf` |
| [`api.create_websocket()`](#realtime) | 실시간 시세 (Real-time) | 19 | WebSocket (`REG`) |

<a id="account"></a>

## `api.account` — 계좌 (Account)

URL: `POST /api/dostk/acnt`

| api_id | 메서드 | 이름 | English |
|---|---|---|---|
| `ka00001` | `api.account.account_number_inquiry()` | 계좌번호조회 | Account Number Inquiry |
| `ka01690` | `api.account.daily_balance_return_rate()` | 일별잔고수익률 | Daily Balance Return Rate |
| `ka10072` | `api.account.realized_profit_by_date()` | 일자별종목별실현손익요청_일자 | Realized Profit by Date per Stock |
| `ka10073` | `api.account.realized_profit_by_period()` | 일자별종목별실현손익요청_기간 | Realized Profit by Period per Stock |
| `ka10074` | `api.account.daily_realized_profit()` | 일별실현손익요청 | Daily Realized Profit |
| `ka10075` | `api.account.unfilled_orders()` | 미체결요청 | Unfilled Orders |
| `ka10076` | `api.account.filled_orders()` | 체결요청 | Filled Orders History |
| `ka10077` | `api.account.today_realized_profit_detail()` | 당일실현손익상세요청 | Today Realized Profit Detail |
| `ka10085` | `api.account.account_return_rate()` | 계좌수익률요청 | Account Return Rate |
| `ka10088` | `api.account.unfilled_split_order_detail()` | 미체결 분할주문 상세 | Unfilled Split Order Detail |
| `ka10170` | `api.account.today_trading_journal()` | 당일매매일지요청 | Today Trading Journal |
| `kt00001` | `api.account.deposit_detail()` | 예수금상세현황요청 | Deposit Detail Status |
| `kt00002` | `api.account.daily_estimated_deposit()` | 일별추정예탁자산현황요청 | Daily Estimated Deposit Asset Status |
| `kt00003` | `api.account.estimated_asset()` | 추정자산조회요청 | Estimated Asset Inquiry |
| `kt00004` | `api.account.account_evaluation()` | 계좌평가현황요청 | Account Evaluation Status |
| `kt00005` | `api.account.filled_position()` | 체결잔고요청 | Filled Position Balance |
| `kt00007` | `api.account.order_execution_detail()` | 계좌별주문체결내역상세요청 | Account Order Execution Detail |
| `kt00008` | `api.account.next_day_settlement()` | 계좌별익일결제예정내역요청 | Next Day Settlement Schedule |
| `kt00009` | `api.account.order_execution_status()` | 계좌별주문체결현황요청 | Account Order Execution Status |
| `kt00010` | `api.account.withdrawable_amount()` | 주문인출가능금액요청 | Withdrawable Order Amount |
| `kt00011` | `api.account.orderable_qty_by_margin()` | 증거금율별주문가능수량조회요청 | Orderable Quantity by Margin Rate |
| `kt00012` | `api.account.orderable_qty_by_credit()` | 신용보증금율별주문가능수량조회요청 | Orderable Quantity by Credit Margin Rate |
| `kt00013` | `api.account.margin_detail()` | 증거금세부내역조회요청 | Margin Detail Inquiry |
| `kt00015` | `api.account.comprehensive_transaction_history()` | 위탁종합거래내역요청 | Comprehensive Transaction History |
| `kt00016` | `api.account.daily_return_detail()` | 일별계좌수익률상세현황요청 | Daily Account Return Rate Detail |
| `kt00017` | `api.account.today_account_status()` | 계좌별당일현황요청 | Today Account Status by Account |
| `kt00018` | `api.account.evaluation_balance_detail()` | 계좌평가잔고내역요청 | Account Evaluation Balance Detail |
| `kt50020` | `api.account.gold_spot_balance()` | 금현물 잔고확인 | Gold Spot Balance |
| `kt50021` | `api.account.gold_spot_deposit()` | 금현물 예수금 | Gold Spot Deposit |
| `kt50030` | `api.account.gold_spot_order_execution_all()` | 금현물 주문체결전체조회 | Gold Spot All Order Execution |
| `kt50031` | `api.account.gold_spot_order_execution()` | 금현물 주문체결조회 | Gold Spot Order Execution |
| `kt50032` | `api.account.gold_spot_transaction_history()` | 금현물 거래내역조회 | Gold Spot Transaction History |
| `kt50075` | `api.account.gold_spot_unfilled_orders()` | 금현물 미체결조회 | Gold Spot Unfilled Orders |

<a id="stock_info"></a>

## `api.stock_info` — 종목정보 (Stock info)

URL: `POST /api/dostk/stkinfo`

| api_id | 메서드 | 이름 | English |
|---|---|---|---|
| `ka00198` | `api.stock_info.realtime_stock_inquiry_rank()` | 실시간종목조회순위 | Real-time Stock Inquiry Ranking |
| `ka10001` | `api.stock_info.basic_stock_info()` | 종목기본정보요청 | Basic Stock Info |
| `ka10002` | `api.stock_info.stock_trading_agent()` | 종목거래원요청 | Stock Trading Agent |
| `ka10003` | `api.stock_info.execution_info()` | 체결정보요청 | Execution Info |
| `ka10013` | `api.stock_info.credit_trading_trend()` | 신용매매동향요청 | Credit Trading Trend |
| `ka10015` | `api.stock_info.daily_transaction_detail()` | 일별거래상세요청 | Daily Transaction Detail |
| `ka10016` | `api.stock_info.new_high_low()` | 신고저가요청 | New High/Low |
| `ka10017` | `api.stock_info.upper_lower_limit()` | 상하한가요청 | Upper/Lower Limit Price |
| `ka10018` | `api.stock_info.near_high_low()` | 고저근접요청 | Near High/Low |
| `ka10019` | `api.stock_info.rapid_price_change()` | 급등락요청 | Rapid Price Change |
| `ka10024` | `api.stock_info.trading_volume_update()` | 거래량갱신요청 | Trading Volume Update |
| `ka10025` | `api.stock_info.volume_concentration()` | 매물대집중요청 | Volume Concentration |
| `ka10026` | `api.stock_info.high_low_per()` | 고저PER요청 | High/Low PER |
| `ka10028` | `api.stock_info.change_rate_vs_opening()` | 시가대비등락률요청 | Change Rate vs Opening Price |
| `ka10043` | `api.stock_info.trading_agent_supply_demand()` | 거래원매물대분석요청 | Trading Agent Supply/Demand Trend Analysis |
| `ka10052` | `api.stock_info.trading_agent_instant_volume()` | 거래원순간거래량요청 | Trading Agent Instant Volume |
| `ka10054` | `api.stock_info.vi_triggered_stocks()` | 변동성완화장치발동종목요청 | VI Triggered Stocks |
| `ka10055` | `api.stock_info.today_vs_yesterday_volume()` | 당일전일체결량요청 | Today vs Yesterday Execution Volume |
| `ka10058` | `api.stock_info.daily_trading_by_investor()` | 투자자별일별매매종목요청 | Daily Trading by Investor |
| `ka10059` | `api.stock_info.investor_institution_by_stock()` | 투자자기관별종목별요청 | Investor/Institution by Stock |
| `ka10061` | `api.stock_info.investor_institution_aggregate()` | 종목별투자자기관별합계요청 | Investor/Institution by Stock Aggregate |
| `ka10084` | `api.stock_info.today_vs_yesterday_execution()` | 당일전일체결요청 | Today vs Yesterday Execution |
| `ka10095` | `api.stock_info.watchlist_stock_info()` | 관심종목정보요청 | Watchlist Stock Info |
| `ka10099` | `api.stock_info.stock_info_list()` | 종목정보 리스트 | Stock Info List |
| `ka10100` | `api.stock_info.stock_info_inquiry()` | 종목정보 조회 | Stock Info Inquiry |
| `ka10101` | `api.stock_info.industry_code_list()` | 업종코드 리스트 | Industry Code List |
| `ka10102` | `api.stock_info.member_company_list()` | 회원사 리스트 | Member Company List |
| `ka90003` | `api.stock_info.program_buy_top50()` | 프로그램순매수상위50요청 | Program Buy Top 50 |
| `ka90004` | `api.stock_info.program_trading_by_stock()` | 종목별프로그램매매현황요청 | Program Trading by Stock |
| `kt20016` | `api.stock_info.margin_loan_available_stocks()` | 신용융자 가능종목요청 | Margin Loan Available Stocks |
| `kt20017` | `api.stock_info.margin_loan_inquiry()` | 신용융자 가능문의 | Margin Loan Inquiry |

<a id="market"></a>

## `api.market` — 시세 (Market)

URL: `POST /api/dostk/mrkcond`

| api_id | 메서드 | 이름 | English |
|---|---|---|---|
| `ka10004` | `api.market.stock_quote()` | 주식호가요청 | Stock Quote |
| `ka10005` | `api.market.stock_daily_weekly_monthly()` | 주식일주월시분요청 | Stock Daily/Weekly/Monthly by Time |
| `ka10006` | `api.market.stock_minute_price()` | 주식시분요청 | Stock Minute Price |
| `ka10007` | `api.market.order_book_info()` | 시세표성정보요청 | Order Book Info |
| `ka10011` | `api.market.rights_issue_price()` | 신주인수권전체시세요청 | Rights Issue Price |
| `ka10044` | `api.market.daily_institutional_trading()` | 일별기관매매종목요청 | Daily Institutional Trading by Stock |
| `ka10045` | `api.market.institutional_trading_trend()` | 종목별기관매매추이요청 | Institutional Trading Trend by Stock |
| `ka10046` | `api.market.hourly_execution_strength()` | 체결강도추이시간별요청 | Hourly Execution Strength |
| `ka10047` | `api.market.daily_execution_strength()` | 체결강도추이일별요청 | Daily Execution Strength |
| `ka10063` | `api.market.intraday_investor_trading()` | 장중투자자별매매요청 | Intraday Investor Trading by Time Slot |
| `ka10066` | `api.market.after_hours_investor_trading()` | 장마감후투자자별매매요청 | After-Hours Investor Trading |
| `ka10078` | `api.market.broker_stock_trading_trend()` | 증권사별종목매매동향요청 | Broker Stock Trading Trend |
| `ka10086` | `api.market.daily_stock_price()` | 일자별주가요청 | Daily Stock Price |
| `ka10087` | `api.market.after_hours_single_price()` | 시간외단일가요청 | After-Hours Single Price |
| `ka50010` | `api.market.gold_spot_execution_trend()` | 금현물체결추이 | Gold Spot Execution Trend |
| `ka50012` | `api.market.gold_spot_daily_trend()` | 금현물일별추이 | Gold Spot Daily Trend |
| `ka50087` | `api.market.gold_spot_expected_execution()` | 금현물예상체결 | Gold Spot Expected Execution |
| `ka50100` | `api.market.gold_spot_price_info()` | 금현물 시세정보 | Gold Spot Price Info |
| `ka50101` | `api.market.gold_spot_order_book()` | 금현물 호가 | Gold Spot Order Book |
| `ka90005` | `api.market.program_trading_by_time()` | 프로그램매매추이요청 시간대별 | Program Trading by Time Slot |
| `ka90006` | `api.market.program_arbitrage_balance()` | 프로그램매매차익잔고추이요청 | Program Arbitrage Balance Trend |
| `ka90007` | `api.market.cumulative_program_trading()` | 프로그램매매누적추이요청 | Cumulative Program Trading Trend |
| `ka90008` | `api.market.program_trading_by_stock_time()` | 종목시간별프로그램매매추이요청 | Program Trading by Stock and Time Slot |
| `ka90010` | `api.market.program_trading_by_date()` | 프로그램매매추이요청 일자별 | Program Trading by Date |
| `ka90013` | `api.market.program_trading_by_stock_day()` | 종목일별프로그램매매추이요청 | Program Trading by Stock and Day |

<a id="chart"></a>

## `api.chart` — 차트 (Chart)

URL: `POST /api/dostk/chart`

| api_id | 메서드 | 이름 | English |
|---|---|---|---|
| `ka10060` | `api.chart.investor_institution_chart()` | 종목별투자자기관별차트요청 | Investor/Institution Chart by Stock |
| `ka10064` | `api.chart.intraday_investor_chart()` | 시간대별투자자매매차트요청 | Intraday Investor Trading Chart by Time Slot |
| `ka10079` | `api.chart.stock_tick_chart()` | 주식틱차트요청 | Stock Tick Chart |
| `ka10080` | `api.chart.stock_minute_chart()` | 주식분봉차트요청 | Stock Minute Chart |
| `ka10081` | `api.chart.stock_daily_chart()` | 주식일봉차트요청 | Stock Daily Chart |
| `ka10082` | `api.chart.stock_weekly_chart()` | 주식주봉차트요청 | Stock Weekly Chart |
| `ka10083` | `api.chart.stock_monthly_chart()` | 주식월봉차트요청 | Stock Monthly Chart |
| `ka10094` | `api.chart.stock_yearly_chart()` | 주식년봉차트요청 | Stock Yearly Chart |
| `ka20004` | `api.chart.industry_tick_chart()` | 업종틱차트요청 | Industry Tick Chart |
| `ka20005` | `api.chart.industry_minute_chart()` | 업종분봉차트요청 | Industry Minute Chart |
| `ka20006` | `api.chart.industry_daily_chart()` | 업종일봉차트요청 | Industry Daily Chart |
| `ka20007` | `api.chart.industry_weekly_chart()` | 업종주봉차트요청 | Industry Weekly Chart |
| `ka20008` | `api.chart.industry_monthly_chart()` | 업종월봉차트요청 | Industry Monthly Chart |
| `ka20019` | `api.chart.industry_yearly_chart()` | 업종년봉차트요청 | Industry Yearly Chart |
| `ka50079` | `api.chart.gold_spot_tick_chart()` | 금현물틱차트조회요청 | Gold Spot Tick Chart |
| `ka50080` | `api.chart.gold_spot_minute_chart()` | 금현물분봉차트조회요청 | Gold Spot Minute Chart |
| `ka50081` | `api.chart.gold_spot_daily_chart()` | 금현물일봉차트조회요청 | Gold Spot Daily Chart |
| `ka50082` | `api.chart.gold_spot_weekly_chart()` | 금현물주봉차트조회요청 | Gold Spot Weekly Chart |
| `ka50083` | `api.chart.gold_spot_monthly_chart()` | 금현물월봉차트조회요청 | Gold Spot Monthly Chart |
| `ka50091` | `api.chart.gold_spot_intraday_tick_chart()` | 금현물당일틱차트조회요청 | Gold Spot Intraday Tick Chart |
| `ka50092` | `api.chart.gold_spot_intraday_minute_chart()` | 금현물당일분봉차트조회요청 | Gold Spot Intraday Minute Chart |

<a id="order"></a>

## `api.order` — 주문 (Order)

URL: `POST /api/dostk/ordr`

> ⚠️ **실주문 모듈입니다.** `is_mock=False`(기본값)면 실계좌에 주문이 나갑니다. MCP 서버는 실전 계좌에서 `KIWOOM_MCP_ALLOW_LIVE_ORDERS=true` 가 아니면 이 도구들을 등록하지 않지만, 파이썬에서 직접 부르는 호출은 막지 않습니다.

| api_id | 메서드 | 이름 | English |
|---|---|---|---|
| `kt10000` | ⚠️ `api.order.buy_order()` | 주식매수주문 | Stock Buy Order |
| `kt10001` | ⚠️ `api.order.sell_order()` | 주식매도주문 | Stock Sell Order |
| `kt10002` | ⚠️ `api.order.modify_order()` | 주식정정주문 | Stock Modify Order |
| `kt10003` | ⚠️ `api.order.cancel_order()` | 주식취소주문 | Stock Cancel Order |
| `kt50000` | ⚠️ `api.order.gold_spot_buy_order()` | 금현물 매수주문 | Gold Spot Buy Order |
| `kt50001` | ⚠️ `api.order.gold_spot_sell_order()` | 금현물 매도주문 | Gold Spot Sell Order |
| `kt50002` | ⚠️ `api.order.gold_spot_modify_order()` | 금현물 정정주문 | Gold Spot Modify Order |
| `kt50003` | ⚠️ `api.order.gold_spot_cancel_order()` | 금현물 취소주문 | Gold Spot Cancel Order |

<a id="credit_order"></a>

## `api.credit_order` — 신용주문 (Credit order)

URL: `POST /api/dostk/crdordr`

> ⚠️ **실주문 모듈입니다.** `is_mock=False`(기본값)면 실계좌에 주문이 나갑니다. MCP 서버는 실전 계좌에서 `KIWOOM_MCP_ALLOW_LIVE_ORDERS=true` 가 아니면 이 도구들을 등록하지 않지만, 파이썬에서 직접 부르는 호출은 막지 않습니다.

| api_id | 메서드 | 이름 | English |
|---|---|---|---|
| `kt10006` | ⚠️ `api.credit_order.margin_buy_order()` | 신용매수주문 | Credit Margin Buy Order |
| `kt10007` | ⚠️ `api.credit_order.margin_sell_order()` | 신용매도주문 | Credit Margin Sell Order |
| `kt10008` | ⚠️ `api.credit_order.margin_modify_order()` | 신용정정주문 | Credit Margin Modify Order |
| `kt10009` | ⚠️ `api.credit_order.margin_cancel_order()` | 신용취소주문 | Credit Margin Cancel Order |

<a id="ranking"></a>

## `api.ranking` — 순위정보 (Ranking)

URL: `POST /api/dostk/rkinfo`

| api_id | 메서드 | 이름 | English |
|---|---|---|---|
| `ka10020` | `api.ranking.top_order_book_volume()` | 호가잔량상위요청 | Top Order Book Volume |
| `ka10021` | `api.ranking.sudden_order_book_increase()` | 호가잔량급증요청 | Sudden Order Book Increase |
| `ka10022` | `api.ranking.sudden_order_ratio_increase()` | 잔량율급증요청 | Sudden Order Ratio Increase |
| `ka10023` | `api.ranking.sudden_volume_increase()` | 거래량급증요청 | Sudden Volume Increase |
| `ka10027` | `api.ranking.top_change_rate()` | 전일대비등락률상위요청 | Top Change Rate vs Previous Day |
| `ka10029` | `api.ranking.top_expected_change_rate()` | 예상체결등락률상위요청 | Top Expected Execution Change Rate |
| `ka10030` | `api.ranking.top_volume_today()` | 당일거래량상위요청 | Top Volume Today |
| `ka10031` | `api.ranking.top_volume_yesterday()` | 전일거래량상위요청 | Top Volume Yesterday |
| `ka10032` | `api.ranking.top_trading_value()` | 거래대금상위요청 | Top Trading Value |
| `ka10033` | `api.ranking.top_credit_ratio()` | 신용비율상위요청 | Top Credit Ratio |
| `ka10034` | `api.ranking.top_foreign_trades_by_period()` | 외인기간별매매상위요청 | Top Foreign Trades by Period |
| `ka10035` | `api.ranking.top_foreign_consecutive_buy()` | 외인연속순매매상위요청 | Top Foreign Consecutive Net Buy |
| `ka10036` | `api.ranking.top_foreign_limit_increase()` | 외인한도소진율증가상위 | Top Foreign Limit Exhaustion Rate Increase |
| `ka10037` | `api.ranking.top_foreign_broker_trading()` | 외국계창구매매상위요청 | Top Foreign Holding Broker Trading |
| `ka10038` | `api.ranking.broker_ranking_by_stock()` | 종목별증권사순위요청 | Broker Ranking by Stock |
| `ka10039` | `api.ranking.top_broker_by_stock()` | 증권사별매매상위요청 | Top Broker by Stock |
| `ka10040` | `api.ranking.main_brokers_today()` | 당일주요거래원요청 | Main Brokers Today |
| `ka10042` | `api.ranking.top_net_buying_brokers()` | 순매수거래원순위요청 | Top Net Buying Brokers |
| `ka10053` | `api.ranking.departed_brokers_today()` | 당일상위이탈원요청 | Departed Brokers Today |
| `ka10062` | `api.ranking.same_day_net_buying_rank()` | 동일순매매순위요청 | Same Day Net Buying Rank |
| `ka10065` | `api.ranking.top_intraday_investor_trading()` | 장중투자자별매매상위요청 | Top Intraday Investor Trading by Time |
| `ka10098` | `api.ranking.after_hours_change_rate_rank()` | 시간외단일가등락율순위요청 | After Hours Change Rate Rank |
| `ka90009` | `api.ranking.top_foreign_institution_trades()` | 외국인기관매매상위요청 | Top Foreign Institution Trades |

<a id="sector"></a>

## `api.sector` — 업종 (Sector)

URL: `POST /api/dostk/sect`

| api_id | 메서드 | 이름 | English |
|---|---|---|---|
| `ka10010` | `api.sector.industry_program_trading()` | 업종프로그램매매요청 | Industry Program Trading |
| `ka10051` | `api.sector.industry_investor_net_buy()` | 업종별투자자순매수요청 | Industry Investor Net Buy |
| `ka20001` | `api.sector.industry_current_price()` | 업종현재가요청 | Industry Current Price |
| `ka20002` | `api.sector.industry_stock_price()` | 업종별주가요청 | Industry Stock Price |
| `ka20003` | `api.sector.all_industry_index()` | 전업종지수요청 | All Industry Index |
| `ka20009` | `api.sector.industry_daily_price()` | 업종현재가일별요청 | Industry Daily Price |

<a id="foreign_institution"></a>

## `api.foreign_institution` — 기관/외국인 (Foreign / institution)

URL: `POST /api/dostk/frgnistt`

| api_id | 메서드 | 이름 | English |
|---|---|---|---|
| `ka10008` | `api.foreign_institution.foreign_trading_trend()` | 주식외국인종목별매매동향 | Foreign Trading Trend by Stock |
| `ka10009` | `api.foreign_institution.institutional_stock()` | 주식기관요청 | Institutional Stock |
| `ka10131` | `api.foreign_institution.consecutive_trading_status()` | 기관외국인연속매매현황요청 | Institution and Foreign Consecutive Trading Status |
| `ka52301` | `api.foreign_institution.gold_spot_investor_status()` | 금현물투자자현황 | Gold Spot Investor Status |

<a id="short_selling"></a>

## `api.short_selling` — 공매도 (Short selling)

URL: `POST /api/dostk/shsa`

| api_id | 메서드 | 이름 | English |
|---|---|---|---|
| `ka10014` | `api.short_selling.short_selling_trend()` | 공매도추이요청 | Short Selling Trend |

<a id="slb"></a>

## `api.slb` — 대차거래 (Stock lending & borrowing)

URL: `POST /api/dostk/slb`

| api_id | 메서드 | 이름 | English |
|---|---|---|---|
| `ka10068` | `api.slb.lending_trend()` | 대차거래추이요청 | Lending Trend |
| `ka10069` | `api.slb.top10_lending()` | 대차거래상위10종목요청 | Top 10 Lending Stocks |
| `ka20068` | `api.slb.lending_trend_by_stock()` | 대차거래추이요청종목별 | Lending Trend by Stock |
| `ka90012` | `api.slb.lending_details()` | 대차거래내역요청 | Lending Details |

<a id="theme"></a>

## `api.theme` — 테마 (Theme)

URL: `POST /api/dostk/thme`

| api_id | 메서드 | 이름 | English |
|---|---|---|---|
| `ka90001` | `api.theme.theme_group_list()` | 테마그룹별요청 | Theme Group List |
| `ka90002` | `api.theme.theme_component_stocks()` | 테마구성종목요청 | Theme Component Stocks |

<a id="condition_search"></a>

## `api.condition_search` — 조건검색 (Condition search)

REST 가 아니라 WebSocket 으로 보냅니다. 메서드는 요청 페이로드(dict)만 만들고, `ws.send()` 로 보낸 뒤 `ws.on_trnm()` 으로 응답을 받습니다.

| 메서드 | trnm | 이름 | English |
|---|---|---|---|
| `api.condition_search.condition_list()` | `CNSRLST` | 조건검색 목록조회 | Condition List |
| `api.condition_search.condition_search()` | `CNSRREQ` | 조건검색 요청 일반 | Condition Search |
| `api.condition_search.condition_search_realtime()` | `CNSRREQ` | 조건검색 요청 실시간 | Condition Search + Realtime |
| `api.condition_search.condition_search_cancel()` | `CNSRCLR` | 조건검색 실시간 해제 | Cancel Realtime Condition Search |

<a id="elw"></a>

## `api.elw` — ELW

URL: `POST /api/dostk/elw`

| api_id | 메서드 | 이름 | English |
|---|---|---|---|
| `ka10048` | `api.elw.daily_sensitivity_indicator()` | ELW일별민감도지표요청 | ELW Daily Sensitivity Indicator |
| `ka10050` | `api.elw.sensitivity_indicator()` | ELW민감도지표요청 | ELW Sensitivity Indicator |
| `ka30001` | `api.elw.price_spike()` | ELW급등락요청 | ELW Price Spike |
| `ka30002` | `api.elw.top_net_buying_by_broker()` | ELW회원사별순매수상위요청 | ELW Top Net Buying by Broker |
| `ka30003` | `api.elw.lp_daily_holding_trend()` | ELW LP일별보유추이요청 | ELW LP Daily Holding Trend |
| `ka30004` | `api.elw.premium_rate()` | ELW괴리율요청 | ELW Premium Rate |
| `ka30005` | `api.elw.condition_search()` | ELW조건검색요청 | ELW Condition Search |
| `ka30009` | `api.elw.change_rate_ranking()` | ELW등락율순위요청 | ELW Change Rate Ranking |
| `ka30010` | `api.elw.order_volume_ranking()` | ELW호가잔량순위요청 | ELW Order Volume Ranking |
| `ka30011` | `api.elw.proximity_rate()` | ELW근접율요청 | ELW Proximity Rate |
| `ka30012` | `api.elw.detailed_stock_info()` | ELW종목상세정보요청 | ELW Detailed Stock Info |

<a id="etf"></a>

## `api.etf` — ETF

URL: `POST /api/dostk/etf`

| api_id | 메서드 | 이름 | English |
|---|---|---|---|
| `ka40001` | `api.etf.return_rate()` | ETF수익률요청 | ETF Return Rate |
| `ka40002` | `api.etf.stock_info()` | ETF종목정보요청 | ETF Stock Info |
| `ka40003` | `api.etf.daily_trend()` | ETF일별추이요청 | ETF Daily Trend |
| `ka40004` | `api.etf.overall_market_price()` | ETF전체시세요청 | ETF Overall Market Price |
| `ka40006` | `api.etf.time_segment_trend()` | ETF시간대별추이요청 | ETF Time Segment Trend |
| `ka40007` | `api.etf.time_segment_execution()` | ETF시간대별체결요청 | ETF Time Segment Execution |
| `ka40008` | `api.etf.daily_execution()` | ETF일자별체결요청 | ETF Daily Execution |
| `ka40009` | `api.etf.time_nav()` | ETF시간대별NAV요청 | ETF Time NAV |
| `ka40010` | `api.etf.time_trend()` | ETF시간대별추이요청 | ETF Time Trend |

<a id="realtime"></a>

## 실시간 시세 — `api.create_websocket()`

`ws.subscribe(<타입>, <종목코드>)` 로 등록하고 `ws.on(<타입>, 콜백)` 으로 받습니다. 콜백이 받는 `values` 의 키는 키움 FID 번호입니다.

| 타입 | 이름 |
|---|---|
| `00` | 주문체결 |
| `04` | 잔고 |
| `0A` | 주식기세 |
| `0B` | 주식체결 |
| `0C` | 주식우선호가 |
| `0D` | 주식호가잔량 |
| `0E` | 주식시간외호가 |
| `0F` | 주식당일거래원 |
| `0G` | ETF NAV |
| `0H` | 주식예상체결 |
| `0I` | 국제금환산가격 |
| `0J` | 업종지수 |
| `0U` | 업종등락 |
| `0g` | 주식종목정보 |
| `0m` | ELW 이론가 |
| `0s` | 장시작시간 |
| `0u` | ELW 지표 |
| `0w` | 종목프로그램매매 |
| `1h` | VI발동/해제 |

## api_id 색인

api_id 순으로 정렬한 같은 목록입니다.

| api_id | 메서드 | 이름 |
|---|---|---|
| `ka00001` | `api.account.account_number_inquiry()` | 계좌번호조회 |
| `ka00198` | `api.stock_info.realtime_stock_inquiry_rank()` | 실시간종목조회순위 |
| `ka01690` | `api.account.daily_balance_return_rate()` | 일별잔고수익률 |
| `ka10001` | `api.stock_info.basic_stock_info()` | 종목기본정보요청 |
| `ka10002` | `api.stock_info.stock_trading_agent()` | 종목거래원요청 |
| `ka10003` | `api.stock_info.execution_info()` | 체결정보요청 |
| `ka10004` | `api.market.stock_quote()` | 주식호가요청 |
| `ka10005` | `api.market.stock_daily_weekly_monthly()` | 주식일주월시분요청 |
| `ka10006` | `api.market.stock_minute_price()` | 주식시분요청 |
| `ka10007` | `api.market.order_book_info()` | 시세표성정보요청 |
| `ka10008` | `api.foreign_institution.foreign_trading_trend()` | 주식외국인종목별매매동향 |
| `ka10009` | `api.foreign_institution.institutional_stock()` | 주식기관요청 |
| `ka10010` | `api.sector.industry_program_trading()` | 업종프로그램매매요청 |
| `ka10011` | `api.market.rights_issue_price()` | 신주인수권전체시세요청 |
| `ka10013` | `api.stock_info.credit_trading_trend()` | 신용매매동향요청 |
| `ka10014` | `api.short_selling.short_selling_trend()` | 공매도추이요청 |
| `ka10015` | `api.stock_info.daily_transaction_detail()` | 일별거래상세요청 |
| `ka10016` | `api.stock_info.new_high_low()` | 신고저가요청 |
| `ka10017` | `api.stock_info.upper_lower_limit()` | 상하한가요청 |
| `ka10018` | `api.stock_info.near_high_low()` | 고저근접요청 |
| `ka10019` | `api.stock_info.rapid_price_change()` | 급등락요청 |
| `ka10020` | `api.ranking.top_order_book_volume()` | 호가잔량상위요청 |
| `ka10021` | `api.ranking.sudden_order_book_increase()` | 호가잔량급증요청 |
| `ka10022` | `api.ranking.sudden_order_ratio_increase()` | 잔량율급증요청 |
| `ka10023` | `api.ranking.sudden_volume_increase()` | 거래량급증요청 |
| `ka10024` | `api.stock_info.trading_volume_update()` | 거래량갱신요청 |
| `ka10025` | `api.stock_info.volume_concentration()` | 매물대집중요청 |
| `ka10026` | `api.stock_info.high_low_per()` | 고저PER요청 |
| `ka10027` | `api.ranking.top_change_rate()` | 전일대비등락률상위요청 |
| `ka10028` | `api.stock_info.change_rate_vs_opening()` | 시가대비등락률요청 |
| `ka10029` | `api.ranking.top_expected_change_rate()` | 예상체결등락률상위요청 |
| `ka10030` | `api.ranking.top_volume_today()` | 당일거래량상위요청 |
| `ka10031` | `api.ranking.top_volume_yesterday()` | 전일거래량상위요청 |
| `ka10032` | `api.ranking.top_trading_value()` | 거래대금상위요청 |
| `ka10033` | `api.ranking.top_credit_ratio()` | 신용비율상위요청 |
| `ka10034` | `api.ranking.top_foreign_trades_by_period()` | 외인기간별매매상위요청 |
| `ka10035` | `api.ranking.top_foreign_consecutive_buy()` | 외인연속순매매상위요청 |
| `ka10036` | `api.ranking.top_foreign_limit_increase()` | 외인한도소진율증가상위 |
| `ka10037` | `api.ranking.top_foreign_broker_trading()` | 외국계창구매매상위요청 |
| `ka10038` | `api.ranking.broker_ranking_by_stock()` | 종목별증권사순위요청 |
| `ka10039` | `api.ranking.top_broker_by_stock()` | 증권사별매매상위요청 |
| `ka10040` | `api.ranking.main_brokers_today()` | 당일주요거래원요청 |
| `ka10042` | `api.ranking.top_net_buying_brokers()` | 순매수거래원순위요청 |
| `ka10043` | `api.stock_info.trading_agent_supply_demand()` | 거래원매물대분석요청 |
| `ka10044` | `api.market.daily_institutional_trading()` | 일별기관매매종목요청 |
| `ka10045` | `api.market.institutional_trading_trend()` | 종목별기관매매추이요청 |
| `ka10046` | `api.market.hourly_execution_strength()` | 체결강도추이시간별요청 |
| `ka10047` | `api.market.daily_execution_strength()` | 체결강도추이일별요청 |
| `ka10048` | `api.elw.daily_sensitivity_indicator()` | ELW일별민감도지표요청 |
| `ka10050` | `api.elw.sensitivity_indicator()` | ELW민감도지표요청 |
| `ka10051` | `api.sector.industry_investor_net_buy()` | 업종별투자자순매수요청 |
| `ka10052` | `api.stock_info.trading_agent_instant_volume()` | 거래원순간거래량요청 |
| `ka10053` | `api.ranking.departed_brokers_today()` | 당일상위이탈원요청 |
| `ka10054` | `api.stock_info.vi_triggered_stocks()` | 변동성완화장치발동종목요청 |
| `ka10055` | `api.stock_info.today_vs_yesterday_volume()` | 당일전일체결량요청 |
| `ka10058` | `api.stock_info.daily_trading_by_investor()` | 투자자별일별매매종목요청 |
| `ka10059` | `api.stock_info.investor_institution_by_stock()` | 투자자기관별종목별요청 |
| `ka10060` | `api.chart.investor_institution_chart()` | 종목별투자자기관별차트요청 |
| `ka10061` | `api.stock_info.investor_institution_aggregate()` | 종목별투자자기관별합계요청 |
| `ka10062` | `api.ranking.same_day_net_buying_rank()` | 동일순매매순위요청 |
| `ka10063` | `api.market.intraday_investor_trading()` | 장중투자자별매매요청 |
| `ka10064` | `api.chart.intraday_investor_chart()` | 시간대별투자자매매차트요청 |
| `ka10065` | `api.ranking.top_intraday_investor_trading()` | 장중투자자별매매상위요청 |
| `ka10066` | `api.market.after_hours_investor_trading()` | 장마감후투자자별매매요청 |
| `ka10068` | `api.slb.lending_trend()` | 대차거래추이요청 |
| `ka10069` | `api.slb.top10_lending()` | 대차거래상위10종목요청 |
| `ka10072` | `api.account.realized_profit_by_date()` | 일자별종목별실현손익요청_일자 |
| `ka10073` | `api.account.realized_profit_by_period()` | 일자별종목별실현손익요청_기간 |
| `ka10074` | `api.account.daily_realized_profit()` | 일별실현손익요청 |
| `ka10075` | `api.account.unfilled_orders()` | 미체결요청 |
| `ka10076` | `api.account.filled_orders()` | 체결요청 |
| `ka10077` | `api.account.today_realized_profit_detail()` | 당일실현손익상세요청 |
| `ka10078` | `api.market.broker_stock_trading_trend()` | 증권사별종목매매동향요청 |
| `ka10079` | `api.chart.stock_tick_chart()` | 주식틱차트요청 |
| `ka10080` | `api.chart.stock_minute_chart()` | 주식분봉차트요청 |
| `ka10081` | `api.chart.stock_daily_chart()` | 주식일봉차트요청 |
| `ka10082` | `api.chart.stock_weekly_chart()` | 주식주봉차트요청 |
| `ka10083` | `api.chart.stock_monthly_chart()` | 주식월봉차트요청 |
| `ka10084` | `api.stock_info.today_vs_yesterday_execution()` | 당일전일체결요청 |
| `ka10085` | `api.account.account_return_rate()` | 계좌수익률요청 |
| `ka10086` | `api.market.daily_stock_price()` | 일자별주가요청 |
| `ka10087` | `api.market.after_hours_single_price()` | 시간외단일가요청 |
| `ka10088` | `api.account.unfilled_split_order_detail()` | 미체결 분할주문 상세 |
| `ka10094` | `api.chart.stock_yearly_chart()` | 주식년봉차트요청 |
| `ka10095` | `api.stock_info.watchlist_stock_info()` | 관심종목정보요청 |
| `ka10098` | `api.ranking.after_hours_change_rate_rank()` | 시간외단일가등락율순위요청 |
| `ka10099` | `api.stock_info.stock_info_list()` | 종목정보 리스트 |
| `ka10100` | `api.stock_info.stock_info_inquiry()` | 종목정보 조회 |
| `ka10101` | `api.stock_info.industry_code_list()` | 업종코드 리스트 |
| `ka10102` | `api.stock_info.member_company_list()` | 회원사 리스트 |
| `ka10131` | `api.foreign_institution.consecutive_trading_status()` | 기관외국인연속매매현황요청 |
| `ka10170` | `api.account.today_trading_journal()` | 당일매매일지요청 |
| `ka20001` | `api.sector.industry_current_price()` | 업종현재가요청 |
| `ka20002` | `api.sector.industry_stock_price()` | 업종별주가요청 |
| `ka20003` | `api.sector.all_industry_index()` | 전업종지수요청 |
| `ka20004` | `api.chart.industry_tick_chart()` | 업종틱차트요청 |
| `ka20005` | `api.chart.industry_minute_chart()` | 업종분봉차트요청 |
| `ka20006` | `api.chart.industry_daily_chart()` | 업종일봉차트요청 |
| `ka20007` | `api.chart.industry_weekly_chart()` | 업종주봉차트요청 |
| `ka20008` | `api.chart.industry_monthly_chart()` | 업종월봉차트요청 |
| `ka20009` | `api.sector.industry_daily_price()` | 업종현재가일별요청 |
| `ka20019` | `api.chart.industry_yearly_chart()` | 업종년봉차트요청 |
| `ka20068` | `api.slb.lending_trend_by_stock()` | 대차거래추이요청종목별 |
| `ka30001` | `api.elw.price_spike()` | ELW급등락요청 |
| `ka30002` | `api.elw.top_net_buying_by_broker()` | ELW회원사별순매수상위요청 |
| `ka30003` | `api.elw.lp_daily_holding_trend()` | ELW LP일별보유추이요청 |
| `ka30004` | `api.elw.premium_rate()` | ELW괴리율요청 |
| `ka30005` | `api.elw.condition_search()` | ELW조건검색요청 |
| `ka30009` | `api.elw.change_rate_ranking()` | ELW등락율순위요청 |
| `ka30010` | `api.elw.order_volume_ranking()` | ELW호가잔량순위요청 |
| `ka30011` | `api.elw.proximity_rate()` | ELW근접율요청 |
| `ka30012` | `api.elw.detailed_stock_info()` | ELW종목상세정보요청 |
| `ka40001` | `api.etf.return_rate()` | ETF수익률요청 |
| `ka40002` | `api.etf.stock_info()` | ETF종목정보요청 |
| `ka40003` | `api.etf.daily_trend()` | ETF일별추이요청 |
| `ka40004` | `api.etf.overall_market_price()` | ETF전체시세요청 |
| `ka40006` | `api.etf.time_segment_trend()` | ETF시간대별추이요청 |
| `ka40007` | `api.etf.time_segment_execution()` | ETF시간대별체결요청 |
| `ka40008` | `api.etf.daily_execution()` | ETF일자별체결요청 |
| `ka40009` | `api.etf.time_nav()` | ETF시간대별NAV요청 |
| `ka40010` | `api.etf.time_trend()` | ETF시간대별추이요청 |
| `ka50010` | `api.market.gold_spot_execution_trend()` | 금현물체결추이 |
| `ka50012` | `api.market.gold_spot_daily_trend()` | 금현물일별추이 |
| `ka50079` | `api.chart.gold_spot_tick_chart()` | 금현물틱차트조회요청 |
| `ka50080` | `api.chart.gold_spot_minute_chart()` | 금현물분봉차트조회요청 |
| `ka50081` | `api.chart.gold_spot_daily_chart()` | 금현물일봉차트조회요청 |
| `ka50082` | `api.chart.gold_spot_weekly_chart()` | 금현물주봉차트조회요청 |
| `ka50083` | `api.chart.gold_spot_monthly_chart()` | 금현물월봉차트조회요청 |
| `ka50087` | `api.market.gold_spot_expected_execution()` | 금현물예상체결 |
| `ka50091` | `api.chart.gold_spot_intraday_tick_chart()` | 금현물당일틱차트조회요청 |
| `ka50092` | `api.chart.gold_spot_intraday_minute_chart()` | 금현물당일분봉차트조회요청 |
| `ka50100` | `api.market.gold_spot_price_info()` | 금현물 시세정보 |
| `ka50101` | `api.market.gold_spot_order_book()` | 금현물 호가 |
| `ka52301` | `api.foreign_institution.gold_spot_investor_status()` | 금현물투자자현황 |
| `ka90001` | `api.theme.theme_group_list()` | 테마그룹별요청 |
| `ka90002` | `api.theme.theme_component_stocks()` | 테마구성종목요청 |
| `ka90003` | `api.stock_info.program_buy_top50()` | 프로그램순매수상위50요청 |
| `ka90004` | `api.stock_info.program_trading_by_stock()` | 종목별프로그램매매현황요청 |
| `ka90005` | `api.market.program_trading_by_time()` | 프로그램매매추이요청 시간대별 |
| `ka90006` | `api.market.program_arbitrage_balance()` | 프로그램매매차익잔고추이요청 |
| `ka90007` | `api.market.cumulative_program_trading()` | 프로그램매매누적추이요청 |
| `ka90008` | `api.market.program_trading_by_stock_time()` | 종목시간별프로그램매매추이요청 |
| `ka90009` | `api.ranking.top_foreign_institution_trades()` | 외국인기관매매상위요청 |
| `ka90010` | `api.market.program_trading_by_date()` | 프로그램매매추이요청 일자별 |
| `ka90012` | `api.slb.lending_details()` | 대차거래내역요청 |
| `ka90013` | `api.market.program_trading_by_stock_day()` | 종목일별프로그램매매추이요청 |
| `kt00001` | `api.account.deposit_detail()` | 예수금상세현황요청 |
| `kt00002` | `api.account.daily_estimated_deposit()` | 일별추정예탁자산현황요청 |
| `kt00003` | `api.account.estimated_asset()` | 추정자산조회요청 |
| `kt00004` | `api.account.account_evaluation()` | 계좌평가현황요청 |
| `kt00005` | `api.account.filled_position()` | 체결잔고요청 |
| `kt00007` | `api.account.order_execution_detail()` | 계좌별주문체결내역상세요청 |
| `kt00008` | `api.account.next_day_settlement()` | 계좌별익일결제예정내역요청 |
| `kt00009` | `api.account.order_execution_status()` | 계좌별주문체결현황요청 |
| `kt00010` | `api.account.withdrawable_amount()` | 주문인출가능금액요청 |
| `kt00011` | `api.account.orderable_qty_by_margin()` | 증거금율별주문가능수량조회요청 |
| `kt00012` | `api.account.orderable_qty_by_credit()` | 신용보증금율별주문가능수량조회요청 |
| `kt00013` | `api.account.margin_detail()` | 증거금세부내역조회요청 |
| `kt00015` | `api.account.comprehensive_transaction_history()` | 위탁종합거래내역요청 |
| `kt00016` | `api.account.daily_return_detail()` | 일별계좌수익률상세현황요청 |
| `kt00017` | `api.account.today_account_status()` | 계좌별당일현황요청 |
| `kt00018` | `api.account.evaluation_balance_detail()` | 계좌평가잔고내역요청 |
| `kt10000` | ⚠️ `api.order.buy_order()` | 주식매수주문 |
| `kt10001` | ⚠️ `api.order.sell_order()` | 주식매도주문 |
| `kt10002` | ⚠️ `api.order.modify_order()` | 주식정정주문 |
| `kt10003` | ⚠️ `api.order.cancel_order()` | 주식취소주문 |
| `kt10006` | ⚠️ `api.credit_order.margin_buy_order()` | 신용매수주문 |
| `kt10007` | ⚠️ `api.credit_order.margin_sell_order()` | 신용매도주문 |
| `kt10008` | ⚠️ `api.credit_order.margin_modify_order()` | 신용정정주문 |
| `kt10009` | ⚠️ `api.credit_order.margin_cancel_order()` | 신용취소주문 |
| `kt20016` | `api.stock_info.margin_loan_available_stocks()` | 신용융자 가능종목요청 |
| `kt20017` | `api.stock_info.margin_loan_inquiry()` | 신용융자 가능문의 |
| `kt50000` | ⚠️ `api.order.gold_spot_buy_order()` | 금현물 매수주문 |
| `kt50001` | ⚠️ `api.order.gold_spot_sell_order()` | 금현물 매도주문 |
| `kt50002` | ⚠️ `api.order.gold_spot_modify_order()` | 금현물 정정주문 |
| `kt50003` | ⚠️ `api.order.gold_spot_cancel_order()` | 금현물 취소주문 |
| `kt50020` | `api.account.gold_spot_balance()` | 금현물 잔고확인 |
| `kt50021` | `api.account.gold_spot_deposit()` | 금현물 예수금 |
| `kt50030` | `api.account.gold_spot_order_execution_all()` | 금현물 주문체결전체조회 |
| `kt50031` | `api.account.gold_spot_order_execution()` | 금현물 주문체결조회 |
| `kt50032` | `api.account.gold_spot_transaction_history()` | 금현물 거래내역조회 |
| `kt50075` | `api.account.gold_spot_unfilled_orders()` | 금현물 미체결조회 |
