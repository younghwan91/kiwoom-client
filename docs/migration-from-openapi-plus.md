# OpenAPI+(OCX) · pykiwoom 에서 옮겨 오기

키움 **OpenAPI+**(OCX/COM, KOA Studio)나 이를 감싼 `pykiwoom` 으로 짜 둔 코드를 키움 **REST API** 와
kiwoom-client 로 옮길 때 보는 대응표입니다. TR 번호는 대부분 숫자가 그대로 이어지지만(`opt10001` → `ka10001`),
**전부 그런 것은 아닙니다** — 아래 표에는 이름까지 같은 것만 올렸고, 번호만 같고 이름이 다른 TR 은 따로 모았습니다.

> **이 표의 근거**
>
> - OpenAPI+ TR 이름: KOA Studio 메타데이터([KOAPY](https://github.com/elbakramer/koapy) 가 패키징한 `trinfo_by_code.json`)
> - OpenAPI+ 함수·이벤트: 키움 [OpenAPI+ 개발가이드 1.7](https://download.kiwoom.com/web/openapi/kiwoom_openapi_plus_devguide_ver_1.7.pdf)
> - REST TR 이름·필드: 키움 공식 [REST API 스펙](https://github.com/Kiwoom-Securities/Kiwoom-REST-API)(`kiwoom/_data/kiwoom_api_spec.json`)과 [REST API 가이드](https://openapi.kiwoom.com/guide/apiguide)
> - 키움이 "opt10001 = ka10001" 이라고 공식으로 밝힌 문서는 찾지 못했습니다. 아래 대응은 **번호와 TR 이름이 둘 다 같은 것**만입니다.

## 무엇이 달라지나

| | OpenAPI+ (OCX) | kiwoom-client (REST) |
|---|---|---|
| 실행 환경 | Windows, 32bit 파이썬, 로그인 창(GUI) | Windows · macOS · Linux, 64bit, 헤드리스 서버 |
| 인증 | `CommConnect()` → 로그인 창 → `OnEventConnect` | 앱키·시크릿키로 토큰 자동 발급·갱신 |
| 조회 | `SetInputValue` × N → `CommRqData` → `OnReceiveTrData` 이벤트에서 `GetCommData` | 메서드 한 번 호출, 응답 dict 를 바로 반환 |
| 이벤트 루프 | PyQt `QEventLoop` 등으로 이벤트를 기다림 | 없음 (동기) 또는 `asyncio` (`AsyncKiwoomAPI`) |
| 화면번호 `sScreenNo` | 필요 | 없음 |
| 실시간 | `SetRealReg(화면, 종목, FID, 타입)` → `OnReceiveRealData` | `ws.subscribe(타입, 종목)` → `ws.on(타입, 콜백)` |
| 조회 제한 | 초당 5건·분당 100건·시간당 1,000건 ([키움 안내](https://www.kiwoom.com/h/customer/download/VOpenApiInfoView)) | TR(api_id)마다 따로 — 이 라이브러리가 기본으로 TR당 1 req/s·버스트 2 로 맞춤 |

## 함수·이벤트 대응

| OpenAPI+ | kiwoom-client | 메모 |
|---|---|---|
| `CommConnect()` / `OnEventConnect` | `KiwoomAPI(app_key, app_secret, is_mock=True)` | 토큰은 첫 호출에서 자동 발급. 미리 확인하려면 `api.login()` |
| `GetLoginInfo("ACCNO")` | `api.account.account_number_inquiry()` | `ka00001` 계좌번호조회, 응답 키 `acctNo` |
| `SetInputValue(이름, 값)` | 메서드의 키워드 인자 | 이름은 REST 필드명(영문 약어)으로 바뀜 — `"종목코드"` → `stk_cd="005930"` |
| `CommRqData(rq, "opt10001", 0, 화면)` | `api.stock_info.basic_stock_info(stk_cd="005930")` | TR 코드 → 메서드는 [엔드포인트 표](endpoints.md) |
| `OnReceiveTrData` + `GetCommData` / `GetRepeatCnt` | 반환값 dict, 반복 데이터는 그 안의 리스트 | `to_dataframe(resp)` 가 리스트를 찾아 DataFrame 으로 |
| `nPrevNext=2` (연속조회) | `cont_yn="Y", next_key=resp["next-key"]` | 응답의 `"cont-yn"` 이 `"Y"` 면 다음 페이지가 있음 |
| `SetRealReg(화면, 종목들, FID들, "0"/"1")` | `await ws.subscribe(타입들, 종목들, grp_no="1", refresh="1")` | FID 가 아니라 **실시간 타입**(`"0B"` 등)으로 등록. `refresh="1"` 기존 유지, `"0"` 기존 해지 — OpenAPI+ 의 `"1"`/`"0"` 과 같은 뜻 |
| `SetRealRemove(화면, 종목)` | `await ws.unsubscribe(타입들, 종목들)` | |
| `OnReceiveRealData` + `GetCommRealData(종목, FID)` | `ws.on("0B", 콜백)` → `d["item"]`, `d["values"]["10"]` | **FID 번호는 그대로** (10=현재가, 13=누적거래량 …) |
| `OnReceiveChejanData` (`sGubun` 0 주문체결 / 1 잔고) | 실시간 타입 `"00"` 주문체결 / `"04"` 잔고 | |
| `GetConditionLoad()` + `GetConditionNameList()` | `api.condition_search.condition_list()` → `CNSRLST` | 조건식 번호(`seq`)를 여기서 얻음 |
| `SendCondition(화면, 이름, 인덱스, 0)` | `api.condition_search.condition_search(seq)` → `CNSRREQ` | 공식 문서의 `ka10172` |
| `SendCondition(화면, 이름, 인덱스, 1)` | `api.condition_search.condition_search_realtime(seq)` | 공식 문서의 `ka10173` |
| `SendConditionStop(화면, 이름, 인덱스)` | `api.condition_search.condition_search_cancel(seq)` → `CNSRCLR` | 공식 문서의 `ka10174` |
| `GetCodeListByMarket(시장)` | `api.stock_info.stock_info_list(mrkt_tp=...)` | `ka10099`. REST `mrkt_tp`: 0 코스피, 10 코스닥, 8 ETF … (공식 스펙) |
| `GetMasterCodeName(종목코드)` | `api.stock_info.stock_info_inquiry(stk_cd=...)` | `ka10100`, 응답 키 `name` |

조건검색은 REST 가 아니라 실시간과 같은 WebSocket 으로 보냅니다:

```python
import asyncio

from kiwoom_client import KiwoomAPI


async def main():
    api = KiwoomAPI.from_env(is_mock=True)
    ws = api.create_websocket()
    await ws.connect()
    ws.on_trnm("CNSRLST", lambda d: print("조건식:", d.get("data")))
    ws.on_trnm("CNSRREQ", lambda d: print("검색 결과:", d.get("data")))
    await ws.send(api.condition_search.condition_list())
    await ws.send(api.condition_search.condition_search(seq="0"))  # seq 는 목록에서 받은 값
    await ws.listen()


asyncio.run(main())
```

## 주문 (`SendOrder`)

```text
SendOrder(sRQName, sScreenNo, sAccNo, nOrderType, sCode, nQty, nPrice, sHogaGb, sOrgOrderNo)
```

| `nOrderType` | kiwoom-client | api_id |
|---|---|---|
| 1 신규매수 | `api.order.buy_order(...)` | `kt10000` |
| 2 신규매도 | `api.order.sell_order(...)` | `kt10001` |
| 5 매수정정 · 6 매도정정 | `api.order.modify_order(...)` | `kt10002` |
| 3 매수취소 · 4 매도취소 | `api.order.cancel_order(...)` | `kt10003` |

| OpenAPI+ 인자 | REST 필드 | 메모 |
|---|---|---|
| `sAccNo` | (없음) | 공식 스펙의 주문 요청 본문에 계좌번호 필드가 없음 |
| `sCode` | `stk_cd` | |
| `nQty` | `ord_qty` | 문자열 (`"10"`) |
| `nPrice` | `ord_uv` | 문자열, 공식 스펙상 필수 아님 — OpenAPI+ 에서도 시장가·최유리 등엔 가격을 넣지 않았음 |
| `sHogaGb` | `trde_tp` | 아래 표 |
| `sOrgOrderNo` | `orig_ord_no` | 정정·취소에서. 수량은 `mdfy_qty` / `cncl_qty` (`"0"` 이면 잔량 전부) |
| (없음) | `dmst_stex_tp` | **필수** — `KRX` · `NXT` · `SOR`. 모의투자는 `KRX` 만 |

`sHogaGb`(OpenAPI+, 개발가이드) 와 `trde_tp`(REST, 공식 스펙) 는 숫자가 같고 앞의 0 만 빠집니다.
`kiwoom_client.codes.OrderType` 에 이름이 붙어 있습니다.

| `sHogaGb` | 뜻 (OpenAPI+) | `trde_tp` | 뜻 (REST) | `OrderType` |
|---|---|---|---|---|
| `00` | 지정가 | `0` | 보통 | `LIMIT` |
| `03` | 시장가 | `3` | 시장가 | `MARKET` |
| `05` | 조건부지정가 | `5` | 조건부지정가 | `CONDITIONAL_LIMIT` |
| `06` | 최유리지정가 | `6` | 최유리지정가 | `BEST_LIMIT` |
| `07` | 최우선지정가 | `7` | 최우선지정가 | `FIRST_LIMIT` |
| `10` | 지정가IOC | `10` | 보통(IOC) | `LIMIT_IOC` |
| `13` | 시장가IOC | `13` | 시장가(IOC) | `MARKET_IOC` |
| `16` | 최유리IOC | `16` | 최유리(IOC) | `BEST_IOC` |
| `20` | 지정가FOK | `20` | 보통(FOK) | `LIMIT_FOK` |
| `23` | 시장가FOK | `23` | 시장가(FOK) | `MARKET_FOK` |
| `26` | 최유리FOK | `26` | 최유리(FOK) | `BEST_FOK` |
| `61` | 장전시간외종가 | `61` | 장시작전시간외 | `PRE_MARKET` |
| `62` | 시간외단일가 | `62` | 시간외단일가 | `AFTER_HOURS_SINGLE` |
| `81` | 장후시간외종가 | `81` | 장마감후시간외 | `POST_MARKET` |
| — | | `28` | 스톱지정가 | `STOP_LIMIT` |
| — | | `29` / `30` / `31` | 중간가 / 중간가(IOC) / 중간가(FOK) | `MID_PRICE` / `MID_PRICE_IOC` / `MID_PRICE_FOK` |

```python
from kiwoom_client import KiwoomAPI, round_to_tick
from kiwoom_client.codes import Exchange, OrderType

api = KiwoomAPI.from_env(is_mock=True)  # 모의투자 — 실전이면 실제로 체결됩니다

# OpenAPI+: SendOrder("매수", "0101", 계좌, 1, "005930", 10, 70000, "00", "")
result = api.order.buy_order(
    dmst_stex_tp=Exchange.KRX,
    stk_cd="005930",
    ord_qty="10",
    ord_uv=str(round_to_tick(70000)),
    trde_tp=OrderType.LIMIT,
)
print(result["ord_no"])
```

> ⚠️ **실주문** — `is_mock=False`(기본값)로 만든 클라이언트의 `api.order.*` · `api.credit_order.*` 는 실계좌에 그대로 주문을 냅니다.
> 파이썬 API 에는 이를 막는 장치가 없습니다(MCP 서버에만 opt-in 가드가 있습니다).

## 실시간 타입

OpenAPI+ 의 실시간 타입 이름(`OnReceiveRealData` 의 `sRealType`)과 REST WebSocket 의 타입 코드입니다.
FID 번호는 같은 번호를 그대로 씁니다(공식 REST 스펙 기준 — 예: 주식체결 `0B` 의 43개 FID 중 42개가 OpenAPI+ 와 같고,
`9081` 거래소구분이 새로 생겼습니다).

| REST 타입 | REST 이름 | OpenAPI+ 이름 |
|---|---|---|
| `00` | 주문체결 | (`OnReceiveChejanData` `sGubun=0`) |
| `04` | 잔고 | 현물잔고 (`OnReceiveChejanData` `sGubun=1`) |
| `0A` | 주식기세 | 주식시세 |
| `0B` | 주식체결 | 주식체결 |
| `0C` | 주식우선호가 | 주식우선호가 |
| `0D` | 주식호가잔량 | 주식호가잔량 |
| `0E` | 주식시간외호가 | 주식시간외호가 |
| `0F` | 주식당일거래원 | 주식당일거래원 |
| `0G` | ETF NAV | ETF NAV |
| `0H` | 주식예상체결 | 주식예상체결 |
| `0J` | 업종지수 | 업종지수 |
| `0U` | 업종등락 | 업종등락 |
| `0g` | 주식종목정보 | 주식종목정보 |
| `0m` | ELW 이론가 | ELW 이론가 |
| `0s` | 장시작시간 | 장시작시간 |
| `0u` | ELW 지표 | ELW 지표 |
| `0w` | 종목프로그램매매 | 종목별프로그램매매 |
| `1h` | VI발동/해제 | VI발동/해제 |

자주 쓰는 FID(개발가이드 8장, 공식 REST 스펙에서도 같은 번호): `10` 현재가, `11` 전일대비, `12` 등락율, `13` 누적거래량,
`14` 누적거래대금, `15` 거래량(체결량), `16` 시가, `17` 고가, `18` 저가, `20` 체결시간, `27` (최우선)매도호가,
`28` (최우선)매수호가, `228` 체결강도, `41`~`50` 매도호가1~10, `51`~`60` 매수호가1~10.

## TR 대응표 — 번호와 이름이 같은 것

OpenAPI+ TR 과 **번호·이름이 둘 다 같은** REST TR 입니다. 요청·응답 필드명은 REST 에서 영문 약어로 바뀌었으니
필드는 [키움 REST API 가이드](https://openapi.kiwoom.com/guide/apiguide)나 `kiwoom_client.spec.get("ka10001")` 로 확인하세요.

| OpenAPI+ | 이름 | REST api_id | kiwoom-client |
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

## 번호는 같지만 이름이 다른 TR

아래는 번호만 같고 TR 이름이 다릅니다. **같은 TR 이라고 가정하지 말고** 공식 가이드에서 필드를 비교한 뒤 쓰세요.
`opt50010`(선물옵션) ↔ `ka50010`(금현물)처럼 아예 다른 것도 있습니다.

| OpenAPI+ | OpenAPI+ 이름 | REST api_id | REST 이름 (공식 스펙) | kiwoom-client |
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

## 더 보기

- [엔드포인트 전체 목록](endpoints.md) — api_id · 한글 TR 이름 · 메서드로 찾기
- [키움 REST API 가이드](https://openapi.kiwoom.com/guide/apiguide) — TR 별 요청·응답 필드
