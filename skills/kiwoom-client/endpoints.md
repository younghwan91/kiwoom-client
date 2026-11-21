# kiwoom-client endpoints

<!-- 자동 생성 파일 — 손으로 고치지 마세요. `python scripts/gen_docs.py` 로 다시 만듭니다. -->

Search this file for an api_id (`ka10081`), a Korean TR name (`일봉`) or a method name. Request fields: `kiwoom_client.spec.get(api_id)` or [Kiwoom's REST API guide](https://openapi.kiwoom.com/guide/apiguide).

## REST endpoints (182)

Format: `api_id` `api.<module>.<method>()` — 한글 TR 이름 (English) [POST url]. ⚠️ = places a real order when `is_mock=False`.

### api.account — 계좌 (Account)

- `ka00001` `api.account.account_number_inquiry()` — 계좌번호조회 (Account Number Inquiry) [POST /api/dostk/acnt]
- `ka01690` `api.account.daily_balance_return_rate()` — 일별잔고수익률 (Daily Balance Return Rate) [POST /api/dostk/acnt]
- `ka10072` `api.account.realized_profit_by_date()` — 일자별종목별실현손익요청_일자 (Realized Profit by Date per Stock) [POST /api/dostk/acnt]
- `ka10073` `api.account.realized_profit_by_period()` — 일자별종목별실현손익요청_기간 (Realized Profit by Period per Stock) [POST /api/dostk/acnt]
- `ka10074` `api.account.daily_realized_profit()` — 일별실현손익요청 (Daily Realized Profit) [POST /api/dostk/acnt]
- `ka10075` `api.account.unfilled_orders()` — 미체결요청 (Unfilled Orders) [POST /api/dostk/acnt]
- `ka10076` `api.account.filled_orders()` — 체결요청 (Filled Orders History) [POST /api/dostk/acnt]
- `ka10077` `api.account.today_realized_profit_detail()` — 당일실현손익상세요청 (Today Realized Profit Detail) [POST /api/dostk/acnt]
- `ka10085` `api.account.account_return_rate()` — 계좌수익률요청 (Account Return Rate) [POST /api/dostk/acnt]
- `ka10088` `api.account.unfilled_split_order_detail()` — 미체결 분할주문 상세 (Unfilled Split Order Detail) [POST /api/dostk/acnt]
- `ka10170` `api.account.today_trading_journal()` — 당일매매일지요청 (Today Trading Journal) [POST /api/dostk/acnt]
- `kt00001` `api.account.deposit_detail()` — 예수금상세현황요청 (Deposit Detail Status) [POST /api/dostk/acnt]
- `kt00002` `api.account.daily_estimated_deposit()` — 일별추정예탁자산현황요청 (Daily Estimated Deposit Asset Status) [POST /api/dostk/acnt]
- `kt00003` `api.account.estimated_asset()` — 추정자산조회요청 (Estimated Asset Inquiry) [POST /api/dostk/acnt]
- `kt00004` `api.account.account_evaluation()` — 계좌평가현황요청 (Account Evaluation Status) [POST /api/dostk/acnt]
- `kt00005` `api.account.filled_position()` — 체결잔고요청 (Filled Position Balance) [POST /api/dostk/acnt]
- `kt00007` `api.account.order_execution_detail()` — 계좌별주문체결내역상세요청 (Account Order Execution Detail) [POST /api/dostk/acnt]
- `kt00008` `api.account.next_day_settlement()` — 계좌별익일결제예정내역요청 (Next Day Settlement Schedule) [POST /api/dostk/acnt]
- `kt00009` `api.account.order_execution_status()` — 계좌별주문체결현황요청 (Account Order Execution Status) [POST /api/dostk/acnt]
- `kt00010` `api.account.withdrawable_amount()` — 주문인출가능금액요청 (Withdrawable Order Amount) [POST /api/dostk/acnt]
- `kt00011` `api.account.orderable_qty_by_margin()` — 증거금율별주문가능수량조회요청 (Orderable Quantity by Margin Rate) [POST /api/dostk/acnt]
- `kt00012` `api.account.orderable_qty_by_credit()` — 신용보증금율별주문가능수량조회요청 (Orderable Quantity by Credit Margin Rate) [POST /api/dostk/acnt]
- `kt00013` `api.account.margin_detail()` — 증거금세부내역조회요청 (Margin Detail Inquiry) [POST /api/dostk/acnt]
- `kt00015` `api.account.comprehensive_transaction_history()` — 위탁종합거래내역요청 (Comprehensive Transaction History) [POST /api/dostk/acnt]
- `kt00016` `api.account.daily_return_detail()` — 일별계좌수익률상세현황요청 (Daily Account Return Rate Detail) [POST /api/dostk/acnt]
- `kt00017` `api.account.today_account_status()` — 계좌별당일현황요청 (Today Account Status by Account) [POST /api/dostk/acnt]
- `kt00018` `api.account.evaluation_balance_detail()` — 계좌평가잔고내역요청 (Account Evaluation Balance Detail) [POST /api/dostk/acnt]
- `kt50020` `api.account.gold_spot_balance()` — 금현물 잔고확인 (Gold Spot Balance) [POST /api/dostk/acnt]
- `kt50021` `api.account.gold_spot_deposit()` — 금현물 예수금 (Gold Spot Deposit) [POST /api/dostk/acnt]
- `kt50030` `api.account.gold_spot_order_execution_all()` — 금현물 주문체결전체조회 (Gold Spot All Order Execution) [POST /api/dostk/acnt]
- `kt50031` `api.account.gold_spot_order_execution()` — 금현물 주문체결조회 (Gold Spot Order Execution) [POST /api/dostk/acnt]
- `kt50032` `api.account.gold_spot_transaction_history()` — 금현물 거래내역조회 (Gold Spot Transaction History) [POST /api/dostk/acnt]
- `kt50075` `api.account.gold_spot_unfilled_orders()` — 금현물 미체결조회 (Gold Spot Unfilled Orders) [POST /api/dostk/acnt]

### api.stock_info — 종목정보 (Stock info)

- `ka00198` `api.stock_info.realtime_stock_inquiry_rank()` — 실시간종목조회순위 (Real-time Stock Inquiry Ranking) [POST /api/dostk/stkinfo]
- `ka10001` `api.stock_info.basic_stock_info()` — 종목기본정보요청 (Basic Stock Info) [POST /api/dostk/stkinfo]
- `ka10002` `api.stock_info.stock_trading_agent()` — 종목거래원요청 (Stock Trading Agent) [POST /api/dostk/stkinfo]
- `ka10003` `api.stock_info.execution_info()` — 체결정보요청 (Execution Info) [POST /api/dostk/stkinfo]
- `ka10013` `api.stock_info.credit_trading_trend()` — 신용매매동향요청 (Credit Trading Trend) [POST /api/dostk/stkinfo]
- `ka10015` `api.stock_info.daily_transaction_detail()` — 일별거래상세요청 (Daily Transaction Detail) [POST /api/dostk/stkinfo]
- `ka10016` `api.stock_info.new_high_low()` — 신고저가요청 (New High/Low) [POST /api/dostk/stkinfo]
- `ka10017` `api.stock_info.upper_lower_limit()` — 상하한가요청 (Upper/Lower Limit Price) [POST /api/dostk/stkinfo]
- `ka10018` `api.stock_info.near_high_low()` — 고저근접요청 (Near High/Low) [POST /api/dostk/stkinfo]
- `ka10019` `api.stock_info.rapid_price_change()` — 급등락요청 (Rapid Price Change) [POST /api/dostk/stkinfo]
- `ka10024` `api.stock_info.trading_volume_update()` — 거래량갱신요청 (Trading Volume Update) [POST /api/dostk/stkinfo]
- `ka10025` `api.stock_info.volume_concentration()` — 매물대집중요청 (Volume Concentration) [POST /api/dostk/stkinfo]
- `ka10026` `api.stock_info.high_low_per()` — 고저PER요청 (High/Low PER) [POST /api/dostk/stkinfo]
- `ka10028` `api.stock_info.change_rate_vs_opening()` — 시가대비등락률요청 (Change Rate vs Opening Price) [POST /api/dostk/stkinfo]
- `ka10043` `api.stock_info.trading_agent_supply_demand()` — 거래원매물대분석요청 (Trading Agent Supply/Demand Trend Analysis) [POST /api/dostk/stkinfo]
- `ka10052` `api.stock_info.trading_agent_instant_volume()` — 거래원순간거래량요청 (Trading Agent Instant Volume) [POST /api/dostk/stkinfo]
- `ka10054` `api.stock_info.vi_triggered_stocks()` — 변동성완화장치발동종목요청 (VI Triggered Stocks) [POST /api/dostk/stkinfo]
- `ka10055` `api.stock_info.today_vs_yesterday_volume()` — 당일전일체결량요청 (Today vs Yesterday Execution Volume) [POST /api/dostk/stkinfo]
- `ka10058` `api.stock_info.daily_trading_by_investor()` — 투자자별일별매매종목요청 (Daily Trading by Investor) [POST /api/dostk/stkinfo]
- `ka10059` `api.stock_info.investor_institution_by_stock()` — 투자자기관별종목별요청 (Investor/Institution by Stock) [POST /api/dostk/stkinfo]
- `ka10061` `api.stock_info.investor_institution_aggregate()` — 종목별투자자기관별합계요청 (Investor/Institution by Stock Aggregate) [POST /api/dostk/stkinfo]
- `ka10084` `api.stock_info.today_vs_yesterday_execution()` — 당일전일체결요청 (Today vs Yesterday Execution) [POST /api/dostk/stkinfo]
- `ka10095` `api.stock_info.watchlist_stock_info()` — 관심종목정보요청 (Watchlist Stock Info) [POST /api/dostk/stkinfo]
- `ka10099` `api.stock_info.stock_info_list()` — 종목정보 리스트 (Stock Info List) [POST /api/dostk/stkinfo]
- `ka10100` `api.stock_info.stock_info_inquiry()` — 종목정보 조회 (Stock Info Inquiry) [POST /api/dostk/stkinfo]
- `ka10101` `api.stock_info.industry_code_list()` — 업종코드 리스트 (Industry Code List) [POST /api/dostk/stkinfo]
- `ka10102` `api.stock_info.member_company_list()` — 회원사 리스트 (Member Company List) [POST /api/dostk/stkinfo]
- `ka90003` `api.stock_info.program_buy_top50()` — 프로그램순매수상위50요청 (Program Buy Top 50) [POST /api/dostk/stkinfo]
- `ka90004` `api.stock_info.program_trading_by_stock()` — 종목별프로그램매매현황요청 (Program Trading by Stock) [POST /api/dostk/stkinfo]
- `kt20016` `api.stock_info.margin_loan_available_stocks()` — 신용융자 가능종목요청 (Margin Loan Available Stocks) [POST /api/dostk/stkinfo]
- `kt20017` `api.stock_info.margin_loan_inquiry()` — 신용융자 가능문의 (Margin Loan Inquiry) [POST /api/dostk/stkinfo]

### api.market — 시세 (Market)

- `ka10004` `api.market.stock_quote()` — 주식호가요청 (Stock Quote) [POST /api/dostk/mrkcond]
- `ka10005` `api.market.stock_daily_weekly_monthly()` — 주식일주월시분요청 (Stock Daily/Weekly/Monthly by Time) [POST /api/dostk/mrkcond]
- `ka10006` `api.market.stock_minute_price()` — 주식시분요청 (Stock Minute Price) [POST /api/dostk/mrkcond]
- `ka10007` `api.market.order_book_info()` — 시세표성정보요청 (Order Book Info) [POST /api/dostk/mrkcond]
- `ka10011` `api.market.rights_issue_price()` — 신주인수권전체시세요청 (Rights Issue Price) [POST /api/dostk/mrkcond]
- `ka10044` `api.market.daily_institutional_trading()` — 일별기관매매종목요청 (Daily Institutional Trading by Stock) [POST /api/dostk/mrkcond]
- `ka10045` `api.market.institutional_trading_trend()` — 종목별기관매매추이요청 (Institutional Trading Trend by Stock) [POST /api/dostk/mrkcond]
- `ka10046` `api.market.hourly_execution_strength()` — 체결강도추이시간별요청 (Hourly Execution Strength) [POST /api/dostk/mrkcond]
- `ka10047` `api.market.daily_execution_strength()` — 체결강도추이일별요청 (Daily Execution Strength) [POST /api/dostk/mrkcond]
- `ka10063` `api.market.intraday_investor_trading()` — 장중투자자별매매요청 (Intraday Investor Trading by Time Slot) [POST /api/dostk/mrkcond]
- `ka10066` `api.market.after_hours_investor_trading()` — 장마감후투자자별매매요청 (After-Hours Investor Trading) [POST /api/dostk/mrkcond]
- `ka10078` `api.market.broker_stock_trading_trend()` — 증권사별종목매매동향요청 (Broker Stock Trading Trend) [POST /api/dostk/mrkcond]
- `ka10086` `api.market.daily_stock_price()` — 일자별주가요청 (Daily Stock Price) [POST /api/dostk/mrkcond]
- `ka10087` `api.market.after_hours_single_price()` — 시간외단일가요청 (After-Hours Single Price) [POST /api/dostk/mrkcond]
- `ka50010` `api.market.gold_spot_execution_trend()` — 금현물체결추이 (Gold Spot Execution Trend) [POST /api/dostk/mrkcond]
- `ka50012` `api.market.gold_spot_daily_trend()` — 금현물일별추이 (Gold Spot Daily Trend) [POST /api/dostk/mrkcond]
- `ka50087` `api.market.gold_spot_expected_execution()` — 금현물예상체결 (Gold Spot Expected Execution) [POST /api/dostk/mrkcond]
- `ka50100` `api.market.gold_spot_price_info()` — 금현물 시세정보 (Gold Spot Price Info) [POST /api/dostk/mrkcond]
- `ka50101` `api.market.gold_spot_order_book()` — 금현물 호가 (Gold Spot Order Book) [POST /api/dostk/mrkcond]
- `ka90005` `api.market.program_trading_by_time()` — 프로그램매매추이요청 시간대별 (Program Trading by Time Slot) [POST /api/dostk/mrkcond]
- `ka90006` `api.market.program_arbitrage_balance()` — 프로그램매매차익잔고추이요청 (Program Arbitrage Balance Trend) [POST /api/dostk/mrkcond]
- `ka90007` `api.market.cumulative_program_trading()` — 프로그램매매누적추이요청 (Cumulative Program Trading Trend) [POST /api/dostk/mrkcond]
- `ka90008` `api.market.program_trading_by_stock_time()` — 종목시간별프로그램매매추이요청 (Program Trading by Stock and Time Slot) [POST /api/dostk/mrkcond]
- `ka90010` `api.market.program_trading_by_date()` — 프로그램매매추이요청 일자별 (Program Trading by Date) [POST /api/dostk/mrkcond]
- `ka90013` `api.market.program_trading_by_stock_day()` — 종목일별프로그램매매추이요청 (Program Trading by Stock and Day) [POST /api/dostk/mrkcond]

### api.chart — 차트 (Chart)

- `ka10060` `api.chart.investor_institution_chart()` — 종목별투자자기관별차트요청 (Investor/Institution Chart by Stock) [POST /api/dostk/chart]
- `ka10064` `api.chart.intraday_investor_chart()` — 시간대별투자자매매차트요청 (Intraday Investor Trading Chart by Time Slot) [POST /api/dostk/chart]
- `ka10079` `api.chart.stock_tick_chart()` — 주식틱차트요청 (Stock Tick Chart) [POST /api/dostk/chart]
- `ka10080` `api.chart.stock_minute_chart()` — 주식분봉차트요청 (Stock Minute Chart) [POST /api/dostk/chart]
- `ka10081` `api.chart.stock_daily_chart()` — 주식일봉차트요청 (Stock Daily Chart) [POST /api/dostk/chart]
- `ka10082` `api.chart.stock_weekly_chart()` — 주식주봉차트요청 (Stock Weekly Chart) [POST /api/dostk/chart]
- `ka10083` `api.chart.stock_monthly_chart()` — 주식월봉차트요청 (Stock Monthly Chart) [POST /api/dostk/chart]
- `ka10094` `api.chart.stock_yearly_chart()` — 주식년봉차트요청 (Stock Yearly Chart) [POST /api/dostk/chart]
- `ka20004` `api.chart.industry_tick_chart()` — 업종틱차트요청 (Industry Tick Chart) [POST /api/dostk/chart]
- `ka20005` `api.chart.industry_minute_chart()` — 업종분봉차트요청 (Industry Minute Chart) [POST /api/dostk/chart]
- `ka20006` `api.chart.industry_daily_chart()` — 업종일봉차트요청 (Industry Daily Chart) [POST /api/dostk/chart]
- `ka20007` `api.chart.industry_weekly_chart()` — 업종주봉차트요청 (Industry Weekly Chart) [POST /api/dostk/chart]
- `ka20008` `api.chart.industry_monthly_chart()` — 업종월봉차트요청 (Industry Monthly Chart) [POST /api/dostk/chart]
- `ka20019` `api.chart.industry_yearly_chart()` — 업종년봉차트요청 (Industry Yearly Chart) [POST /api/dostk/chart]
- `ka50079` `api.chart.gold_spot_tick_chart()` — 금현물틱차트조회요청 (Gold Spot Tick Chart) [POST /api/dostk/chart]
- `ka50080` `api.chart.gold_spot_minute_chart()` — 금현물분봉차트조회요청 (Gold Spot Minute Chart) [POST /api/dostk/chart]
- `ka50081` `api.chart.gold_spot_daily_chart()` — 금현물일봉차트조회요청 (Gold Spot Daily Chart) [POST /api/dostk/chart]
- `ka50082` `api.chart.gold_spot_weekly_chart()` — 금현물주봉차트조회요청 (Gold Spot Weekly Chart) [POST /api/dostk/chart]
- `ka50083` `api.chart.gold_spot_monthly_chart()` — 금현물월봉차트조회요청 (Gold Spot Monthly Chart) [POST /api/dostk/chart]
- `ka50091` `api.chart.gold_spot_intraday_tick_chart()` — 금현물당일틱차트조회요청 (Gold Spot Intraday Tick Chart) [POST /api/dostk/chart]
- `ka50092` `api.chart.gold_spot_intraday_minute_chart()` — 금현물당일분봉차트조회요청 (Gold Spot Intraday Minute Chart) [POST /api/dostk/chart]

### api.order — 주문 (Order)

- ⚠️ `kt10000` `api.order.buy_order()` — 주식매수주문 (Stock Buy Order) [POST /api/dostk/ordr]
- ⚠️ `kt10001` `api.order.sell_order()` — 주식매도주문 (Stock Sell Order) [POST /api/dostk/ordr]
- ⚠️ `kt10002` `api.order.modify_order()` — 주식정정주문 (Stock Modify Order) [POST /api/dostk/ordr]
- ⚠️ `kt10003` `api.order.cancel_order()` — 주식취소주문 (Stock Cancel Order) [POST /api/dostk/ordr]
- ⚠️ `kt50000` `api.order.gold_spot_buy_order()` — 금현물 매수주문 (Gold Spot Buy Order) [POST /api/dostk/ordr]
- ⚠️ `kt50001` `api.order.gold_spot_sell_order()` — 금현물 매도주문 (Gold Spot Sell Order) [POST /api/dostk/ordr]
- ⚠️ `kt50002` `api.order.gold_spot_modify_order()` — 금현물 정정주문 (Gold Spot Modify Order) [POST /api/dostk/ordr]
- ⚠️ `kt50003` `api.order.gold_spot_cancel_order()` — 금현물 취소주문 (Gold Spot Cancel Order) [POST /api/dostk/ordr]

### api.credit_order — 신용주문 (Credit order)

- ⚠️ `kt10006` `api.credit_order.margin_buy_order()` — 신용매수주문 (Credit Margin Buy Order) [POST /api/dostk/crdordr]
- ⚠️ `kt10007` `api.credit_order.margin_sell_order()` — 신용매도주문 (Credit Margin Sell Order) [POST /api/dostk/crdordr]
- ⚠️ `kt10008` `api.credit_order.margin_modify_order()` — 신용정정주문 (Credit Margin Modify Order) [POST /api/dostk/crdordr]
- ⚠️ `kt10009` `api.credit_order.margin_cancel_order()` — 신용취소주문 (Credit Margin Cancel Order) [POST /api/dostk/crdordr]

### api.ranking — 순위정보 (Ranking)

- `ka10020` `api.ranking.top_order_book_volume()` — 호가잔량상위요청 (Top Order Book Volume) [POST /api/dostk/rkinfo]
- `ka10021` `api.ranking.sudden_order_book_increase()` — 호가잔량급증요청 (Sudden Order Book Increase) [POST /api/dostk/rkinfo]
- `ka10022` `api.ranking.sudden_order_ratio_increase()` — 잔량율급증요청 (Sudden Order Ratio Increase) [POST /api/dostk/rkinfo]
- `ka10023` `api.ranking.sudden_volume_increase()` — 거래량급증요청 (Sudden Volume Increase) [POST /api/dostk/rkinfo]
- `ka10027` `api.ranking.top_change_rate()` — 전일대비등락률상위요청 (Top Change Rate vs Previous Day) [POST /api/dostk/rkinfo]
- `ka10029` `api.ranking.top_expected_change_rate()` — 예상체결등락률상위요청 (Top Expected Execution Change Rate) [POST /api/dostk/rkinfo]
- `ka10030` `api.ranking.top_volume_today()` — 당일거래량상위요청 (Top Volume Today) [POST /api/dostk/rkinfo]
- `ka10031` `api.ranking.top_volume_yesterday()` — 전일거래량상위요청 (Top Volume Yesterday) [POST /api/dostk/rkinfo]
- `ka10032` `api.ranking.top_trading_value()` — 거래대금상위요청 (Top Trading Value) [POST /api/dostk/rkinfo]
- `ka10033` `api.ranking.top_credit_ratio()` — 신용비율상위요청 (Top Credit Ratio) [POST /api/dostk/rkinfo]
- `ka10034` `api.ranking.top_foreign_trades_by_period()` — 외인기간별매매상위요청 (Top Foreign Trades by Period) [POST /api/dostk/rkinfo]
- `ka10035` `api.ranking.top_foreign_consecutive_buy()` — 외인연속순매매상위요청 (Top Foreign Consecutive Net Buy) [POST /api/dostk/rkinfo]
- `ka10036` `api.ranking.top_foreign_limit_increase()` — 외인한도소진율증가상위 (Top Foreign Limit Exhaustion Rate Increase) [POST /api/dostk/rkinfo]
- `ka10037` `api.ranking.top_foreign_broker_trading()` — 외국계창구매매상위요청 (Top Foreign Holding Broker Trading) [POST /api/dostk/rkinfo]
- `ka10038` `api.ranking.broker_ranking_by_stock()` — 종목별증권사순위요청 (Broker Ranking by Stock) [POST /api/dostk/rkinfo]
- `ka10039` `api.ranking.top_broker_by_stock()` — 증권사별매매상위요청 (Top Broker by Stock) [POST /api/dostk/rkinfo]
- `ka10040` `api.ranking.main_brokers_today()` — 당일주요거래원요청 (Main Brokers Today) [POST /api/dostk/rkinfo]
- `ka10042` `api.ranking.top_net_buying_brokers()` — 순매수거래원순위요청 (Top Net Buying Brokers) [POST /api/dostk/rkinfo]
- `ka10053` `api.ranking.departed_brokers_today()` — 당일상위이탈원요청 (Departed Brokers Today) [POST /api/dostk/rkinfo]
- `ka10062` `api.ranking.same_day_net_buying_rank()` — 동일순매매순위요청 (Same Day Net Buying Rank) [POST /api/dostk/rkinfo]
- `ka10065` `api.ranking.top_intraday_investor_trading()` — 장중투자자별매매상위요청 (Top Intraday Investor Trading by Time) [POST /api/dostk/rkinfo]
- `ka10098` `api.ranking.after_hours_change_rate_rank()` — 시간외단일가등락율순위요청 (After Hours Change Rate Rank) [POST /api/dostk/rkinfo]
- `ka90009` `api.ranking.top_foreign_institution_trades()` — 외국인기관매매상위요청 (Top Foreign Institution Trades) [POST /api/dostk/rkinfo]

### api.sector — 업종 (Sector)

- `ka10010` `api.sector.industry_program_trading()` — 업종프로그램매매요청 (Industry Program Trading) [POST /api/dostk/sect]
- `ka10051` `api.sector.industry_investor_net_buy()` — 업종별투자자순매수요청 (Industry Investor Net Buy) [POST /api/dostk/sect]
- `ka20001` `api.sector.industry_current_price()` — 업종현재가요청 (Industry Current Price) [POST /api/dostk/sect]
- `ka20002` `api.sector.industry_stock_price()` — 업종별주가요청 (Industry Stock Price) [POST /api/dostk/sect]
- `ka20003` `api.sector.all_industry_index()` — 전업종지수요청 (All Industry Index) [POST /api/dostk/sect]
- `ka20009` `api.sector.industry_daily_price()` — 업종현재가일별요청 (Industry Daily Price) [POST /api/dostk/sect]

### api.foreign_institution — 기관/외국인 (Foreign / institution)

- `ka10008` `api.foreign_institution.foreign_trading_trend()` — 주식외국인종목별매매동향 (Foreign Trading Trend by Stock) [POST /api/dostk/frgnistt]
- `ka10009` `api.foreign_institution.institutional_stock()` — 주식기관요청 (Institutional Stock) [POST /api/dostk/frgnistt]
- `ka10131` `api.foreign_institution.consecutive_trading_status()` — 기관외국인연속매매현황요청 (Institution and Foreign Consecutive Trading Status) [POST /api/dostk/frgnistt]
- `ka52301` `api.foreign_institution.gold_spot_investor_status()` — 금현물투자자현황 (Gold Spot Investor Status) [POST /api/dostk/frgnistt]

### api.short_selling — 공매도 (Short selling)

- `ka10014` `api.short_selling.short_selling_trend()` — 공매도추이요청 (Short Selling Trend) [POST /api/dostk/shsa]

### api.slb — 대차거래 (Stock lending & borrowing)

- `ka10068` `api.slb.lending_trend()` — 대차거래추이요청 (Lending Trend) [POST /api/dostk/slb]
- `ka10069` `api.slb.top10_lending()` — 대차거래상위10종목요청 (Top 10 Lending Stocks) [POST /api/dostk/slb]
- `ka20068` `api.slb.lending_trend_by_stock()` — 대차거래추이요청종목별 (Lending Trend by Stock) [POST /api/dostk/slb]
- `ka90012` `api.slb.lending_details()` — 대차거래내역요청 (Lending Details) [POST /api/dostk/slb]

### api.theme — 테마 (Theme)

- `ka90001` `api.theme.theme_group_list()` — 테마그룹별요청 (Theme Group List) [POST /api/dostk/thme]
- `ka90002` `api.theme.theme_component_stocks()` — 테마구성종목요청 (Theme Component Stocks) [POST /api/dostk/thme]

### api.elw — ELW

- `ka10048` `api.elw.daily_sensitivity_indicator()` — ELW일별민감도지표요청 (ELW Daily Sensitivity Indicator) [POST /api/dostk/elw]
- `ka10050` `api.elw.sensitivity_indicator()` — ELW민감도지표요청 (ELW Sensitivity Indicator) [POST /api/dostk/elw]
- `ka30001` `api.elw.price_spike()` — ELW급등락요청 (ELW Price Spike) [POST /api/dostk/elw]
- `ka30002` `api.elw.top_net_buying_by_broker()` — ELW회원사별순매수상위요청 (ELW Top Net Buying by Broker) [POST /api/dostk/elw]
- `ka30003` `api.elw.lp_daily_holding_trend()` — ELW LP일별보유추이요청 (ELW LP Daily Holding Trend) [POST /api/dostk/elw]
- `ka30004` `api.elw.premium_rate()` — ELW괴리율요청 (ELW Premium Rate) [POST /api/dostk/elw]
- `ka30005` `api.elw.condition_search()` — ELW조건검색요청 (ELW Condition Search) [POST /api/dostk/elw]
- `ka30009` `api.elw.change_rate_ranking()` — ELW등락율순위요청 (ELW Change Rate Ranking) [POST /api/dostk/elw]
- `ka30010` `api.elw.order_volume_ranking()` — ELW호가잔량순위요청 (ELW Order Volume Ranking) [POST /api/dostk/elw]
- `ka30011` `api.elw.proximity_rate()` — ELW근접율요청 (ELW Proximity Rate) [POST /api/dostk/elw]
- `ka30012` `api.elw.detailed_stock_info()` — ELW종목상세정보요청 (ELW Detailed Stock Info) [POST /api/dostk/elw]

### api.etf — ETF

- `ka40001` `api.etf.return_rate()` — ETF수익률요청 (ETF Return Rate) [POST /api/dostk/etf]
- `ka40002` `api.etf.stock_info()` — ETF종목정보요청 (ETF Stock Info) [POST /api/dostk/etf]
- `ka40003` `api.etf.daily_trend()` — ETF일별추이요청 (ETF Daily Trend) [POST /api/dostk/etf]
- `ka40004` `api.etf.overall_market_price()` — ETF전체시세요청 (ETF Overall Market Price) [POST /api/dostk/etf]
- `ka40006` `api.etf.time_segment_trend()` — ETF시간대별추이요청 (ETF Time Segment Trend) [POST /api/dostk/etf]
- `ka40007` `api.etf.time_segment_execution()` — ETF시간대별체결요청 (ETF Time Segment Execution) [POST /api/dostk/etf]
- `ka40008` `api.etf.daily_execution()` — ETF일자별체결요청 (ETF Daily Execution) [POST /api/dostk/etf]
- `ka40009` `api.etf.time_nav()` — ETF시간대별NAV요청 (ETF Time NAV) [POST /api/dostk/etf]
- `ka40010` `api.etf.time_trend()` — ETF시간대별추이요청 (ETF Time Trend) [POST /api/dostk/etf]

## Condition search (WebSocket payload builders)

- `CNSRLST` `api.condition_search.condition_list()` — 조건검색 목록조회 (Condition List)
- `CNSRREQ` `api.condition_search.condition_search()` — 조건검색 요청 일반 (Condition Search)
- `CNSRREQ` `api.condition_search.condition_search_realtime()` — 조건검색 요청 실시간 (Condition Search + Realtime)
- `CNSRCLR` `api.condition_search.condition_search_cancel()` — 조건검색 실시간 해제 (Cancel Realtime Condition Search)

## Real-time types (`await ws.subscribe(type, item)`)

- `00` 주문체결
- `04` 잔고
- `0A` 주식기세
- `0B` 주식체결
- `0C` 주식우선호가
- `0D` 주식호가잔량
- `0E` 주식시간외호가
- `0F` 주식당일거래원
- `0G` ETF NAV
- `0H` 주식예상체결
- `0I` 국제금환산가격
- `0J` 업종지수
- `0U` 업종등락
- `0g` 주식종목정보
- `0m` ELW 이론가
- `0s` 장시작시간
- `0u` ELW 지표
- `0w` 종목프로그램매매
- `1h` VI발동/해제
