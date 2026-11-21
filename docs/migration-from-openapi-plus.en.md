---
seo_title: "Kiwoom OpenAPI+ / pykiwoom to the REST API — TR mapping table"
description: "Port Kiwoom OpenAPI+ (OCX/KOA Studio) or pykiwoom code to the Kiwoom REST API: TR and function mapping (opt10001 → ka10001) plus the TRs whose name changed."
---

# Migrating from OpenAPI+ (OCX) / pykiwoom

A mapping table for moving code written against Kiwoom **OpenAPI+** (OCX/COM, KOA Studio), or `pykiwoom` which wraps it,
to the Kiwoom **REST API** and kiwoom-client. Most TR numbers carry straight over (`opt10001` → `ka10001`), but
**not all of them** — the main table below lists only TRs whose number and name both match; TRs with the same number
but a different name are collected separately.

> **Sources for these tables**
>
> - OpenAPI+ TR names: KOA Studio metadata (`trinfo_by_code.json`, packaged by [KOAPY](https://github.com/elbakramer/koapy))
> - OpenAPI+ functions and events: Kiwoom's [OpenAPI+ developer guide 1.7](https://download.kiwoom.com/web/openapi/kiwoom_openapi_plus_devguide_ver_1.7.pdf) (Korean)
> - REST TR names and fields: Kiwoom's official [REST API spec](https://github.com/Kiwoom-Securities/Kiwoom-REST-API) (`kiwoom/_data/kiwoom_api_spec.json`) and the [REST API guide](https://openapi.kiwoom.com/guide/apiguide)
> - We found no document in which Kiwoom officially states "opt10001 = ka10001". The mappings below cover **only TRs whose number and TR name are both identical**.

## What changes

| | OpenAPI+ (OCX) | kiwoom-client (REST) |
|---|---|---|
| Runs on | Windows, 32-bit Python, a login window (GUI) | Windows · macOS · Linux, 64-bit, headless servers |
| Authentication | `CommConnect()` → login window → `OnEventConnect` | App key and secret; tokens are issued and refreshed for you |
| Queries | `SetInputValue` × N → `CommRqData` → `GetCommData` inside the `OnReceiveTrData` event | One method call that returns the response dict directly |
| Event loop | Wait for events with a PyQt `QEventLoop` or similar | None (sync) or `asyncio` (`AsyncKiwoomAPI`) |
| Screen number `sScreenNo` | Required | None |
| Real-time | `SetRealReg(screen, codes, FIDs, type)` → `OnReceiveRealData` | `ws.subscribe(type, codes)` → `ws.on(type, callback)` |
| Rate limits | 5 per second · 100 per minute · 1,000 per hour ([Kiwoom notice](https://www.kiwoom.com/h/customer/download/VOpenApiInfoView), Korean) | Separate per TR (api_id) — by default this library paces each TR at 1 req/s with a burst of 2 |

## Functions and events

| OpenAPI+ | kiwoom-client | Notes |
|---|---|---|
| `CommConnect()` / `OnEventConnect` | `KiwoomAPI(app_key, app_secret, is_mock=True)` | The token is issued on the first call. To check up front, `api.login()` |
| `GetLoginInfo("ACCNO")` | `api.account.account_number_inquiry()` | `ka00001` account number inquiry (계좌번호조회), response key `acctNo` |
| `SetInputValue(name, value)` | Keyword arguments of the method | Names become REST field names (English abbreviations) — `"종목코드"` (stock code) → `stk_cd="005930"` |
| `CommRqData(rq, "opt10001", 0, screen)` | `api.stock_info.basic_stock_info(stk_cd="005930")` | TR code → method: see the [endpoint reference](endpoints.md) |
| `OnReceiveTrData` + `GetCommData` / `GetRepeatCnt` | The returned dict; repeated rows are a list inside it | `to_dataframe(resp)` finds the list and makes a DataFrame |
| `nPrevNext=2` (continuation query, 연속조회) | `cont_yn="Y", next_key=resp["next-key"]` | If the response's `"cont-yn"` is `"Y"`, there is another page |
| `SetRealReg(screen, codes, FIDs, "0"/"1")` | `await ws.subscribe(types, codes, grp_no="1", refresh="1")` | Register by **real-time type** (`"0B"` etc.), not by FID. `refresh="1"` keeps existing registrations, `"0"` drops them — the same meaning as OpenAPI+'s `"1"`/`"0"` |
| `SetRealRemove(screen, code)` | `await ws.unsubscribe(types, codes)` | |
| `OnReceiveRealData` + `GetCommRealData(code, FID)` | `ws.on("0B", callback)` → `d["item"]`, `d["values"]["10"]` | **FID numbers are unchanged** (10 = current price, 13 = cumulative volume …) |
| `OnReceiveChejanData` (`sGubun` 0 order execution / 1 balance) | Real-time type `"00"` order execution / `"04"` balance | |
| `GetConditionLoad()` + `GetConditionNameList()` | `api.condition_search.condition_list()` → `CNSRLST` | This is where you get the condition number (`seq`) |
| `SendCondition(screen, name, index, 0)` | `api.condition_search.condition_search(seq)` → `CNSRREQ` | `ka10172` in the official docs |
| `SendCondition(screen, name, index, 1)` | `api.condition_search.condition_search_realtime(seq)` | `ka10173` in the official docs |
| `SendConditionStop(screen, name, index)` | `api.condition_search.condition_search_cancel(seq)` → `CNSRCLR` | `ka10174` in the official docs |
| `GetCodeListByMarket(market)` | `api.stock_info.stock_info_list(mrkt_tp=...)` | `ka10099`. REST `mrkt_tp`: 0 KOSPI, 10 KOSDAQ, 8 ETF … (official spec) |
| `GetMasterCodeName(code)` | `api.stock_info.stock_info_inquiry(stk_cd=...)` | `ka10100`, response key `name` |

Condition search (조건검색) is not sent over REST but over the same WebSocket as real-time data:

```python
import asyncio

from kiwoom_client import KiwoomAPI


async def main():
    api = KiwoomAPI.from_env(is_mock=True)
    ws = api.create_websocket()
    await ws.connect()
    ws.on_trnm("CNSRLST", lambda d: print("conditions:", d.get("data")))
    ws.on_trnm("CNSRREQ", lambda d: print("results:", d.get("data")))
    await ws.send(api.condition_search.condition_list())
    await ws.send(api.condition_search.condition_search(seq="0"))  # seq comes from the list
    await ws.listen()


asyncio.run(main())
```

## Orders (`SendOrder`)

```text
SendOrder(sRQName, sScreenNo, sAccNo, nOrderType, sCode, nQty, nPrice, sHogaGb, sOrgOrderNo)
```

| `nOrderType` | kiwoom-client | api_id |
|---|---|---|
| 1 new buy | `api.order.buy_order(...)` | `kt10000` |
| 2 new sell | `api.order.sell_order(...)` | `kt10001` |
| 5 modify buy · 6 modify sell | `api.order.modify_order(...)` | `kt10002` |
| 3 cancel buy · 4 cancel sell | `api.order.cancel_order(...)` | `kt10003` |

| OpenAPI+ argument | REST field | Notes |
|---|---|---|
| `sAccNo` | (none) | The official spec's order request body has no account-number field |
| `sCode` | `stk_cd` | |
| `nQty` | `ord_qty` | A string (`"10"`) |
| `nPrice` | `ord_uv` | A string, not required by the official spec — OpenAPI+ also left the price empty for market, best-price and similar orders |
| `sHogaGb` | `trde_tp` | Table below |
| `sOrgOrderNo` | `orig_ord_no` | For modify and cancel. The quantity is `mdfy_qty` / `cncl_qty` (`"0"` means the whole remaining quantity) |
| (none) | `dmst_stex_tp` | **Required** — `KRX` · `NXT` · `SOR`. Mock trading supports `KRX` only |

`sHogaGb` (OpenAPI+, developer guide) and `trde_tp` (REST, official spec) use the same numbers, just without the leading 0.
`kiwoom_client.codes.OrderType` gives them names.

| `sHogaGb` | Meaning (OpenAPI+) | `trde_tp` | Meaning (REST) | `OrderType` |
|---|---|---|---|---|
| `00` | Limit (지정가) | `0` | Normal (보통) | `LIMIT` |
| `03` | Market | `3` | Market | `MARKET` |
| `05` | Conditional limit | `5` | Conditional limit | `CONDITIONAL_LIMIT` |
| `06` | Best limit (최유리지정가) | `6` | Best limit | `BEST_LIMIT` |
| `07` | First limit (최우선지정가) | `7` | First limit | `FIRST_LIMIT` |
| `10` | Limit IOC | `10` | Normal (IOC) | `LIMIT_IOC` |
| `13` | Market IOC | `13` | Market (IOC) | `MARKET_IOC` |
| `16` | Best IOC | `16` | Best (IOC) | `BEST_IOC` |
| `20` | Limit FOK | `20` | Normal (FOK) | `LIMIT_FOK` |
| `23` | Market FOK | `23` | Market (FOK) | `MARKET_FOK` |
| `26` | Best FOK | `26` | Best (FOK) | `BEST_FOK` |
| `61` | Pre-market off-hours closing price (장전시간외종가) | `61` | Pre-open off-hours (장시작전시간외) | `PRE_MARKET` |
| `62` | Off-hours single price (시간외단일가) | `62` | Off-hours single price | `AFTER_HOURS_SINGLE` |
| `81` | Post-market off-hours closing price (장후시간외종가) | `81` | After-close off-hours (장마감후시간외) | `POST_MARKET` |
| — | | `28` | Stop limit (스톱지정가) | `STOP_LIMIT` |
| — | | `29` / `30` / `31` | Mid price / mid price (IOC) / mid price (FOK) (중간가) | `MID_PRICE` / `MID_PRICE_IOC` / `MID_PRICE_FOK` |

```python
from kiwoom_client import KiwoomAPI, round_to_tick
from kiwoom_client.codes import Exchange, OrderType

api = KiwoomAPI.from_env(is_mock=True)  # mock trading — on the live server this really fills

# OpenAPI+: SendOrder("buy", "0101", account, 1, "005930", 10, 70000, "00", "")
result = api.order.buy_order(
    dmst_stex_tp=Exchange.KRX,
    stk_cd="005930",
    ord_qty="10",
    ord_uv=str(round_to_tick(70000)),
    trde_tp=OrderType.LIMIT,
)
print(result["ord_no"])
```

> ⚠️ **Real orders** — with a client created with `is_mock=False` (the default), `api.order.*` · `api.credit_order.*` send orders straight to your real account.
> The Python API has nothing that blocks them (only the MCP server has an opt-in guard).

## Real-time types

The OpenAPI+ real-time type names (`sRealType` in `OnReceiveRealData`) and the REST WebSocket type codes.
FID numbers are reused as they are (per the official REST spec — for example, 42 of the 43 FIDs of the stock trade
type `0B` are the same as in OpenAPI+, and `9081` exchange type is new).

| REST type | REST name | OpenAPI+ name | Meaning |
|---|---|---|---|
| `00` | 주문체결 | (`OnReceiveChejanData` `sGubun=0`) | Order execution |
| `04` | 잔고 | 현물잔고 (`OnReceiveChejanData` `sGubun=1`) | Balance |
| `0A` | 주식기세 | 주식시세 | Stock quote |
| `0B` | 주식체결 | 주식체결 | Stock trade |
| `0C` | 주식우선호가 | 주식우선호가 | Best bid/ask |
| `0D` | 주식호가잔량 | 주식호가잔량 | Order book (bid/ask volumes) |
| `0E` | 주식시간외호가 | 주식시간외호가 | Off-hours order book |
| `0F` | 주식당일거래원 | 주식당일거래원 | Today's brokers |
| `0G` | ETF NAV | ETF NAV | ETF NAV |
| `0H` | 주식예상체결 | 주식예상체결 | Expected execution |
| `0J` | 업종지수 | 업종지수 | Sector index |
| `0U` | 업종등락 | 업종등락 | Sector advance/decline |
| `0g` | 주식종목정보 | 주식종목정보 | Stock information |
| `0m` | ELW 이론가 | ELW 이론가 | ELW theoretical price |
| `0s` | 장시작시간 | 장시작시간 | Market session time |
| `0u` | ELW 지표 | ELW 지표 | ELW indicators |
| `0w` | 종목프로그램매매 | 종목별프로그램매매 | Program trading by stock |
| `1h` | VI발동/해제 | VI발동/해제 | VI triggered / released |

Common FIDs (developer guide chapter 8; the official REST spec uses the same numbers): `10` current price, `11` change
from previous close, `12` change rate, `13` cumulative volume, `14` cumulative trading value, `15` volume (trade
size), `16` open, `17` high, `18` low, `20` trade time, `27` (best) ask, `28` (best) bid, `228` execution strength
(체결강도), `41`–`50` ask 1–10, `51`–`60` bid 1–10.

## TR mapping — same number and name

REST TRs whose **number and name both match** an OpenAPI+ TR. The names below are Kiwoom's Korean TR names, as shown
in KOA Studio and the REST guide. Request and response field names changed to English abbreviations in REST, so check
the fields in the [Kiwoom REST API guide](https://openapi.kiwoom.com/guide/apiguide) or with
`kiwoom_client.spec.get("ka10001")`.

| OpenAPI+ | Name (Korean) | REST api_id | kiwoom-client |
|---|---|---|---|
| `opt10001` | 주식기본정보요청 | `ka10001` | `api.stock_info.basic_stock_info()` |
| `opt10002` | 주식거래원요청 | `ka10002` | `api.stock_info.stock_trading_agent()` |
| `opt10003` | 체결정보요청 | `ka10003` | `api.stock_info.execution_info()` |
| `opt10004` | 주식호가요청 | `ka10004` | `api.market.stock_quote()` |
| `opt10005` | 주식일주월시분요청 | `ka10005` | `api.market.stock_daily_weekly_monthly()` |
| `opt10006` | 주식시분요청 | `ka10006` | `api.market.stock_minute_price()` |
| `opt10007` | 시세표성정보요청 | `ka10007` | `api.market.order_book_info()` |
| `opt10010` | 업종프로그램요청 | `ka10010` | `api.sector.industry_program_trading()` |
| `opt10011` | 신주인수권전체시세요청 | `ka10011` | `api.market.rights_issue_price()` |
| `opt10013` | 신용매매동향요청 | `ka10013` | `api.stock_info.credit_trading_trend()` |
| `opt10014` | 공매도추이요청 | `ka10014` | `api.short_selling.short_selling_trend()` |
| `opt10015` | 일별거래상세요청 | `ka10015` | `api.stock_info.daily_transaction_detail()` |
| `opt10016` | 신고저가요청 | `ka10016` | `api.stock_info.new_high_low()` |
| `opt10017` | 상하한가요청 | `ka10017` | `api.stock_info.upper_lower_limit()` |
| `opt10018` | 고저가근접요청 | `ka10018` | `api.stock_info.near_high_low()` |
| `opt10019` | 가격급등락요청 | `ka10019` | `api.stock_info.rapid_price_change()` |
| `opt10020` | 호가잔량상위요청 | `ka10020` | `api.ranking.top_order_book_volume()` |
| `opt10021` | 호가잔량급증요청 | `ka10021` | `api.ranking.sudden_order_book_increase()` |
| `opt10022` | 잔량율급증요청 | `ka10022` | `api.ranking.sudden_order_ratio_increase()` |
| `opt10023` | 거래량급증요청 | `ka10023` | `api.ranking.sudden_volume_increase()` |
| `opt10024` | 거래량갱신요청 | `ka10024` | `api.stock_info.trading_volume_update()` |
| `opt10025` | 매물대집중요청 | `ka10025` | `api.stock_info.volume_concentration()` |
| `opt10026` | 고저PER요청 | `ka10026` | `api.stock_info.high_low_per()` |
| `opt10027` | 전일대비등락률상위요청 | `ka10027` | `api.ranking.top_change_rate()` |
| `opt10028` | 시가대비등락률요청 | `ka10028` | `api.stock_info.change_rate_vs_opening()` |
| `opt10029` | 예상체결등락률상위요청 | `ka10029` | `api.ranking.top_expected_change_rate()` |
| `opt10030` | 당일거래량상위요청 | `ka10030` | `api.ranking.top_volume_today()` |
| `opt10031` | 전일거래량상위요청 | `ka10031` | `api.ranking.top_volume_yesterday()` |
| `opt10032` | 거래대금상위요청 | `ka10032` | `api.ranking.top_trading_value()` |
| `opt10033` | 신용비율상위요청 | `ka10033` | `api.ranking.top_credit_ratio()` |
| `opt10034` | 외인기간별매매상위요청 | `ka10034` | `api.ranking.top_foreign_trades_by_period()` |
| `opt10035` | 외인연속순매매상위요청 | `ka10035` | `api.ranking.top_foreign_consecutive_buy()` |
| `opt10036` | 외인한도소진율증가상위 | `ka10036` | `api.ranking.top_foreign_limit_increase()` |
| `opt10037` | 외국계창구매매상위요청 | `ka10037` | `api.ranking.top_foreign_broker_trading()` |
| `opt10038` | 종목별증권사순위요청 | `ka10038` | `api.ranking.broker_ranking_by_stock()` |
| `opt10039` | 증권사별매매상위요청 | `ka10039` | `api.ranking.top_broker_by_stock()` |
| `opt10040` | 당일주요거래원요청 | `ka10040` | `api.ranking.main_brokers_today()` |
| `opt10042` | 순매수거래원순위요청 | `ka10042` | `api.ranking.top_net_buying_brokers()` |
| `opt10043` | 거래원매물대분석요청 | `ka10043` | `api.stock_info.trading_agent_supply_demand()` |
| `opt10044` | 일별기관매매종목요청 | `ka10044` | `api.market.daily_institutional_trading()` |
| `opt10045` | 종목별기관매매추이요청 | `ka10045` | `api.market.institutional_trading_trend()` |
| `opt10046` | 체결강도추이시간별요청 | `ka10046` | `api.market.hourly_execution_strength()` |
| `opt10047` | 체결강도추이일별요청 | `ka10047` | `api.market.daily_execution_strength()` |
| `opt10048` | ELW일별민감도지표요청 | `ka10048` | `api.elw.daily_sensitivity_indicator()` |
| `opt10050` | ELW민감도지표요청 | `ka10050` | `api.elw.sensitivity_indicator()` |
| `opt10051` | 업종별투자자순매수요청 | `ka10051` | `api.sector.industry_investor_net_buy()` |
| `opt10052` | 거래원순간거래량요청 | `ka10052` | `api.stock_info.trading_agent_instant_volume()` |
| `opt10053` | 당일상위이탈원요청 | `ka10053` | `api.ranking.departed_brokers_today()` |
| `opt10054` | 변동성완화장치발동종목요청 | `ka10054` | `api.stock_info.vi_triggered_stocks()` |
| `opt10058` | 투자자별일별매매종목요청 | `ka10058` | `api.stock_info.daily_trading_by_investor()` |
| `opt10059` | 종목별투자자기관별요청 | `ka10059` | `api.stock_info.investor_institution_by_stock()` |
| `opt10060` | 종목별투자자기관별차트요청 | `ka10060` | `api.chart.investor_institution_chart()` |
| `opt10061` | 종목별투자자기관별합계요청 | `ka10061` | `api.stock_info.investor_institution_aggregate()` |
| `opt10062` | 동일순매매순위요청 | `ka10062` | `api.ranking.same_day_net_buying_rank()` |
| `opt10063` | 장중투자자별매매요청 | `ka10063` | `api.market.intraday_investor_trading()` |
| `opt10064` | 장중투자자별매매차트요청 | `ka10064` | `api.chart.intraday_investor_chart()` |
| `opt10065` | 장중투자자별매매상위요청 | `ka10065` | `api.ranking.top_intraday_investor_trading()` |
| `opt10068` | 대차거래추이요청 | `ka10068` | `api.slb.lending_trend()` |
| `opt10069` | 대차거래상위10종목요청 | `ka10069` | `api.slb.top10_lending()` |
| `opt10074` | 일자별실현손익요청 | `ka10074` | `api.account.daily_realized_profit()` |
| `opt10075` | 미체결요청 | `ka10075` | `api.account.unfilled_orders()` |
| `opt10076` | 체결요청 | `ka10076` | `api.account.filled_orders()` |
| `opt10077` | 당일실현손익상세요청 | `ka10077` | `api.account.today_realized_profit_detail()` |
| `opt10078` | 증권사별종목매매동향요청 | `ka10078` | `api.market.broker_stock_trading_trend()` |
| `opt10079` | 주식틱차트조회요청 | `ka10079` | `api.chart.stock_tick_chart()` |
| `opt10080` | 주식분봉차트조회요청 | `ka10080` | `api.chart.stock_minute_chart()` |
| `opt10081` | 주식일봉차트조회요청 | `ka10081` | `api.chart.stock_daily_chart()` |
| `opt10082` | 주식주봉차트조회요청 | `ka10082` | `api.chart.stock_weekly_chart()` |
| `opt10083` | 주식월봉차트조회요청 | `ka10083` | `api.chart.stock_monthly_chart()` |
| `opt10084` | 당일전일체결요청 | `ka10084` | `api.stock_info.today_vs_yesterday_execution()` |
| `opt10085` | 계좌수익률요청 | `ka10085` | `api.account.account_return_rate()` |
| `opt10086` | 일별주가요청 | `ka10086` | `api.market.daily_stock_price()` |
| `opt10087` | 시간외단일가요청 | `ka10087` | `api.market.after_hours_single_price()` |
| `opt10094` | 주식년봉차트조회요청 | `ka10094` | `api.chart.stock_yearly_chart()` |
| `opt10098` | 시간외단일가등락율순위요청 | `ka10098` | `api.ranking.after_hours_change_rate_rank()` |
| `opt10131` | 기관외국인연속매매현황요청 | `ka10131` | `api.foreign_institution.consecutive_trading_status()` |
| `opt10170` | 당일매매일지요청 | `ka10170` | `api.account.today_trading_journal()` |
| `opt20001` | 업종현재가요청 | `ka20001` | `api.sector.industry_current_price()` |
| `opt20002` | 업종별주가요청 | `ka20002` | `api.sector.industry_stock_price()` |
| `opt20003` | 전업종지수요청 | `ka20003` | `api.sector.all_industry_index()` |
| `opt20004` | 업종틱차트조회요청 | `ka20004` | `api.chart.industry_tick_chart()` |
| `opt20005` | 업종분봉조회요청 | `ka20005` | `api.chart.industry_minute_chart()` |
| `opt20006` | 업종일봉조회요청 | `ka20006` | `api.chart.industry_daily_chart()` |
| `opt20007` | 업종주봉조회요청 | `ka20007` | `api.chart.industry_weekly_chart()` |
| `opt20008` | 업종월봉조회요청 | `ka20008` | `api.chart.industry_monthly_chart()` |
| `opt20009` | 업종현재가일별요청 | `ka20009` | `api.sector.industry_daily_price()` |
| `opt20019` | 업종년봉조회요청 | `ka20019` | `api.chart.industry_yearly_chart()` |
| `opt20068` | 대차거래추이요청(종목별) | `ka20068` | `api.slb.lending_trend_by_stock()` |
| `opt30001` | ELW가격급등락요청 | `ka30001` | `api.elw.price_spike()` |
| `opt30002` | 거래원별ELW순매매상위요청 | `ka30002` | `api.elw.top_net_buying_by_broker()` |
| `opt30003` | ELWLP보유일별추이요청 | `ka30003` | `api.elw.lp_daily_holding_trend()` |
| `opt30004` | ELW괴리율요청 | `ka30004` | `api.elw.premium_rate()` |
| `opt30005` | ELW조건검색요청 | `ka30005` | `api.elw.condition_search()` |
| `opt30009` | ELW등락율순위요청 | `ka30009` | `api.elw.change_rate_ranking()` |
| `opt30010` | ELW잔량순위요청 | `ka30010` | `api.elw.order_volume_ranking()` |
| `opt30011` | ELW근접율요청 | `ka30011` | `api.elw.proximity_rate()` |
| `opt30012` | ELW종목상세정보요청 | `ka30012` | `api.elw.detailed_stock_info()` |
| `opt40001` | ETF수익율요청 | `ka40001` | `api.etf.return_rate()` |
| `opt40002` | ETF종목정보요청 | `ka40002` | `api.etf.stock_info()` |
| `opt40003` | ETF일별추이요청 | `ka40003` | `api.etf.daily_trend()` |
| `opt40004` | ETF전체시세요청 | `ka40004` | `api.etf.overall_market_price()` |
| `opt40006` | ETF시간대별추이요청 | `ka40006` | `api.etf.time_segment_trend()` |
| `opt40007` | ETF시간대별체결요청 | `ka40007` | `api.etf.time_segment_execution()` |
| `opt40008` | ETF일자별체결요청 | `ka40008` | `api.etf.daily_execution()` |
| `opt90001` | 테마그룹별요청 | `ka90001` | `api.theme.theme_group_list()` |
| `opt90002` | 테마구성종목요청 | `ka90002` | `api.theme.theme_component_stocks()` |
| `opt90003` | 프로그램순매수상위50요청 | `ka90003` | `api.stock_info.program_buy_top50()` |
| `opt90004` | 종목별프로그램매매현황요청 | `ka90004` | `api.stock_info.program_trading_by_stock()` |
| `opt90006` | 프로그램매매차익잔고추이요청 | `ka90006` | `api.market.program_arbitrage_balance()` |
| `opt90007` | 프로그램매매누적추이요청 | `ka90007` | `api.market.cumulative_program_trading()` |
| `opt90008` | 종목시간별프로그램매매추이요청 | `ka90008` | `api.market.program_trading_by_stock_time()` |
| `opt90009` | 외국인기관매매상위요청 | `ka90009` | `api.ranking.top_foreign_institution_trades()` |
| `opt90012` | 대차거래내역요청 | `ka90012` | `api.slb.lending_details()` |
| `opt90013` | 종목일별프로그램매매추이요청 | `ka90013` | `api.market.program_trading_by_stock_day()` |
| `opw00001` | 예수금상세현황요청 | `kt00001` | `api.account.deposit_detail()` |
| `opw00002` | 일별추정예탁자산현황요청 | `kt00002` | `api.account.daily_estimated_deposit()` |
| `opw00003` | 추정자산조회요청 | `kt00003` | `api.account.estimated_asset()` |
| `opw00004` | 계좌평가현황요청 | `kt00004` | `api.account.account_evaluation()` |
| `opw00005` | 체결잔고요청 | `kt00005` | `api.account.filled_position()` |
| `opw00007` | 계좌별주문체결내역상세요청 | `kt00007` | `api.account.order_execution_detail()` |
| `opw00008` | 계좌별익일결제예정내역요청 | `kt00008` | `api.account.next_day_settlement()` |
| `opw00009` | 계좌별주문체결현황요청 | `kt00009` | `api.account.order_execution_status()` |
| `opw00010` | 주문인출가능금액요청 | `kt00010` | `api.account.withdrawable_amount()` |
| `opw00011` | 증거금율별주문가능수량조회요청 | `kt00011` | `api.account.orderable_qty_by_margin()` |
| `opw00012` | 신용보증금율별주문가능수량조회요청 | `kt00012` | `api.account.orderable_qty_by_credit()` |
| `opw00013` | 증거금세부내역조회요청 | `kt00013` | `api.account.margin_detail()` |
| `opw00015` | 위탁종합거래내역요청 | `kt00015` | `api.account.comprehensive_transaction_history()` |
| `opw00016` | 일별계좌수익률상세현황요청 | `kt00016` | `api.account.daily_return_detail()` |
| `opw00017` | 계좌별당일현황요청 | `kt00017` | `api.account.today_account_status()` |
| `opw00018` | 계좌평가잔고내역요청 | `kt00018` | `api.account.evaluation_balance_detail()` |
| `opw20016` | 신용융자 가능종목요청 | `kt20016` | `api.stock_info.margin_loan_available_stocks()` |
| `opw20017` | 신용융자 가능문의 | `kt20017` | `api.stock_info.margin_loan_inquiry()` |

## Same number, different name

These TRs share only the number; the TR name differs. **Do not assume they are the same TR** — compare the fields in
the official guide before using them. Some are entirely different, such as `opt50010` (futures/options) ↔ `ka50010`
(gold spot).

| OpenAPI+ | OpenAPI+ name | REST api_id | REST name (official spec) | kiwoom-client |
|---|---|---|---|---|
| `opt10008` | 주식외국인요청 | `ka10008` | 주식외국인종목별매매동향 | `api.foreign_institution.foreign_trading_trend()` |
| `opt10055` | 당일전일체결대량요청 | `ka10055` | 당일전일체결량요청 | `api.stock_info.today_vs_yesterday_volume()` |
| `opt10066` | 장중투자자별매매차트요청 | `ka10066` | 장마감후투자자별매매요청 | `api.market.after_hours_investor_trading()` |
| `opt10072` | 일자별종목별실현손익요청 | `ka10072` | 일자별종목별실현손익요청_일자 | `api.account.realized_profit_by_date()` |
| `opt10073` | 일자별종목별실현손익요청 | `ka10073` | 일자별종목별실현손익요청_기간 | `api.account.realized_profit_by_period()` |
| `opt40009` | ETF시간대별체결요청 | `ka40009` | ETF시간대별NAV현황 | `api.etf.time_nav()` |
| `opt40010` | ETF시간대별추이요청 | `ka40010` | ETF시간대별수급현황 | `api.etf.time_trend()` |
| `opt50010` | 선옵호가잔량추이요청 | `ka50010` | 금현물체결추이 | `api.market.gold_spot_execution_trend()` |
| `opt50012` | 선옵타임스프레드차트요청 | `ka50012` | 금현물일별추이 | `api.market.gold_spot_daily_trend()` |
| `opt90005` | 프로그램매매추이요청 | `ka90005` | 프로그램매매추이요청 시간대별 | `api.market.program_trading_by_time()` |
| `opt90010` | 차익잔고현황요청 | `ka90010` | 프로그램매매추이요청 일자별 | `api.market.program_trading_by_date()` |

## See also

- [Endpoint reference](endpoints.md) — find a TR by api_id, Korean TR name or method
- [Kiwoom REST API guide](https://openapi.kiwoom.com/guide/apiguide) — request and response fields per TR
