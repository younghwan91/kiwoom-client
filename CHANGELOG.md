# 변경 이력

이 프로젝트는 [Keep a Changelog](https://keepachangelog.com/ko/1.1.0/) 형식을 따르며,
[유의적 버전](https://semver.org/lang/ko/)을 사용합니다.

## [Unreleased]

### Added

- 문서: README(한·영) 빠른 시작에 "키 없이 체험"(`kiwoom-client-mcp --demo`, Claude Code 등록 한 줄)과 `KiwoomAPI.demo()` 안내를, MCP 문서에 데모 모드 절(가상 데이터 경고, 되는 것·안 되는 것, `KIWOOM_MCP_DEMO`·`config --demo`·번들 `데모 모드` 항목)을, 편의 기능 문서에 `kiwoom --demo` 를 더했습니다
- `kiwoom-client-mcp config <client> --demo` — 키 자리표시자 없이 `--demo` 로 띄우는 설정을 출력합니다. `KIWOOM_MCP_DEMO=auto` 는 앱키·시크릿이 없을 때만 데모로 뜹니다. Claude Desktop 번들(.mcpb)은 키 입력을 선택으로 바꾸고 `데모 모드`(기본 `auto`) 항목을 더해, 키 없이 설치하면 바로 데모로 동작하고 키를 넣으면 실제 서버에 연결합니다. `kiwoom-client-mcp --demo doctor` 도 데모를 인식해 키를 요구하지 않고 인증 확인(네트워크)을 건너뜁니다
- 문서: 튜토리얼 [10분 만에 조건검색 알림 봇](docs/tutorials/condition-alert-bot.md)(·영문) — `KiwoomAPI.demo()` 로 키 없이 바로 돌아가는 조건검색 + 실시간 가격 알림 봇입니다. 주문은 하지 않고, 실제 계좌는 클라이언트 한 줄만 바꿉니다. 코드 블록은 테스트가 데모 백엔드로 실제 실행합니다
- MCP 데모 모드 — `kiwoom-client-mcp --demo`(또는 `KIWOOM_MCP_DEMO=true`)는 키 없이 데모 백엔드로 뜹니다. smart 모드의 의도 도구 전부와 `order_preview`→확인 토큰→`place_order` 흐름이 종이 거래로 동작하고, 서버 instructions 가 가상 데이터임을 밝히라고 지시하며 모든 도구 응답 첫 키가 `_demo` 입니다(오류는 `[데모]` 접두). 실제 키가 있어도 경고하고 쓰지 않으며, 데모 주문은 기본적으로 감사 로그에 남기지 않습니다
- CLI `kiwoom --demo` — 키 없이 `quote`·`chart`·`balance`·`find` 를 가상 데이터로 실행합니다. 출력 첫 줄에 `[데모] 가상 데이터` 배너가 붙고(`--json` 이면 stderr), 환경의 실제 앱키는 경고와 함께 무시합니다
- `KiwoomAPI.demo()` / `AsyncKiwoomAPI.demo()` — 키·계좌·네트워크 없이 데모 백엔드에 붙은 클라이언트를 만듭니다(`seed=` 로 합성 데이터 고정). 주문은 메모리 안의 종이 거래가 되고 `create_websocket()` 은 데모 WebSocket 을 돌려줍니다. `api.is_demo`·`api.demo_backend` 로 확인합니다
- 데모 WebSocket `kiwoom_client.demo.DemoWebSocket` — 소켓 없이 LOGIN·실시간 등록(REG/REMOVE)·0B 체결 푸시(합성 가격 주변의 가상 체결)·조건검색(CNSRLST/CNSRREQ, 가상 조건식 4개)을 흉내 냅니다. `KiwoomWebSocket` 의 `subscribe`·`listen`·콜백과 MCP 세션이 그대로 동작합니다
- 데모 종이 거래 — 데모 백엔드가 주식 매수·매도·정정·취소(kt10000~kt10003)를 메모리 안에서 체결·미체결로 시뮬레이션하고, 미체결(ka10075)·체결(ka10076)·주문내역(kt00007)·잔고·예수금에 반영합니다. 키움으로는 아무것도 전송하지 않으며, 신용·금현물 주문은 거부합니다
- 데모 백엔드 `kiwoom_client.demo.DemoBackend` — 키움 계좌·앱키·네트워크 없이 도는 프로세스 안 가짜 키움 서버(`httpx.MockTransport`)입니다. 실제 종목명·코드 20개에 시드 고정 합성 시세(오늘 기준 과거 영업일)를 주고, 응답 키는 TR 카탈로그를 따르며 모든 응답에 `"_demo"` 표시가 붙습니다. 가격은 실제 시세가 아닙니다
- 토큰 파일 캐시 — `KiwoomAPI(..., token_cache="경로")`(async 도 같음, `from_env()` 는 `KIWOOM_TOKEN_CACHE`)를 주면
  받은 토큰을 0600 JSON 파일에 두고, 같은 앱키·서버의 다음 프로세스(크론·스크립트·`kiwoom` CLI)가 만료 전까지
  다시 쓴다. 앱키·시크릿은 저장하지 않고, 갱신·폐기 때 파일도 고치며, 파일 오류는 경고만 남긴다. 기본은 메모리만(동작 변화 없음)
- 실시간: `ws.on("0B", cb, named=True)` — 콜백이 받는 `values` 키를 FID 번호(`"10"`) 대신 키움 스펙의 한글
  필드명(`"현재가"`)으로 바꾼 사본을 준다. 스펙에 없는 FID·타입은 그대로, 같은 타입의 다른 콜백은 FID 키를 받는다
- CI: 단위 테스트를 Windows·macOS 에서도 돌린다
- 문서: [프롬프트 모음](docs/prompts.md)(·영문) — Claude·Cursor 에 그대로 붙여 넣는 질문 19개와 쓰이는 도구·결과를 정리했습니다. 주문은 미리보기까지만 만들고, 테스트가 도구 이름 실존을 확인합니다

### Changed

- README 데모 GIF(`scripts/demo_mock_session.py`)가 자체 가짜 서버 대신 `kiwoom-client-mcp --demo` 와 같은 데모 백엔드로 돌아가도록 바꾸고 GIF 를 다시 만들었습니다. 화면에 `[DEMO]` 배너와 `_demo` 표시가 보입니다

### Fixed

- Windows: 출력이 파이프·파일로 가면 쓰이는 레거시 코드 페이지(cp949·cp1252)에서 `kiwoom --help`·
  `kiwoom-client-mcp --help` 등이 `UnicodeEncodeError` 로 죽던 것. 인코딩할 수 없는 글자(cp949 의 `—` 등)는 `?` 로 찍는다
- 개발용 Claude Code 훅 `live_order_guard.py` 가 cp1252·cp949 콘솔에서 차단 메시지를 못 찍어 명령을 그대로
  통과시키던 것(fail-open). 응답을 ASCII JSON 으로 쓰고 stdin 은 UTF-8 로 읽는다. Windows 경로(`C:\...\x.py`)로 가리킨 스크립트도 읽는다

- MCP: 2단계 주문 — `order_preview` 가 그 주문에만 쓸 수 있는 1회용 `confirm_token`(HMAC, 120초)을 돌려주고,
  종목명·수량·단가로 주문하는 `place_order`·`modify_order`·`cancel_order` 는 토큰이 없거나 파라미터가 다르거나
  만료·재사용이면 전송하지 않고 거부한다(실주문 opt-in 가드 뒤에만 등록). `order_preview` 는 정정·취소(`action`)와
  신용·금현물 TR(`tool`+`params`) 미리보기도 만든다
- MCP: `order_preview` 가 서버 연결이 있으면 상·하한가(ka10001)·매수 주문가능수량(kt00011)·매도가능수량(kt00018)을
  조회해 위반은 `errors`(토큰 발급 안 함), 근접·조회 실패는 `warnings` 로 돌려준다
- MCP: 주문 한도·허용 종목 — `KIWOOM_MCP_MAX_ORDER_AMOUNT`(원, 시장가는 상한가로 계산)·`KIWOOM_MCP_MAX_ORDER_QTY`·
  `KIWOOM_MCP_ALLOWED_STOCKS`(쉼표)·`KIWOOM_MCP_DAILY_ORDER_LIMIT`(프로세스·KST 하루). `order_preview` 와 전송 직전
  둘 다에서 강제하고, 설정하지 않으면 제한 없음
- MCP: 중복 주문 방지 — TR 도구·요청 필드가 똑같은 주문이 `KIWOOM_MCP_DUPLICATE_WINDOW`(기본 10초, `0` = 끔) 안에
  다시 오면 새 토큰이어도 전송하지 않고 거부한다
- MCP: 주문 감사 로그 — 미리보기·거부·전송·실패를 JSONL 로 `KIWOOM_MCP_AUDIT_LOG`(기본
  `~/.kiwoom-client/mcp-audit.jsonl`, `off` = 끔)에 남긴다. 키·토큰은 쓰지 않고 계좌번호는 마스킹, 파일 `0600`
- MCP: 읽기 전용 모드 `KIWOOM_MCP_READ_ONLY=true` — 모의투자·opt-in 과 상관없이 주문 도구를 하나도 등록하지 않는다
  (`doctor` 도 보고)
- MCP: `place_order`·`modify_order`·`cancel_order` 가 스키마 밖 인자(`trde_tp` 등)를 받으면 전송하지 않고 거부한다.
  주문 안전장치 회귀 테스트 묶음 — 모든 경로 × 차단 조건에서 주문 요청 0건, 문서에 안전장치 표
- 문서 사이트: 모든 페이지에 Open Graph·Twitter Card 메타, 홈에 JSON-LD(SoftwareApplication·SoftwareSourceCode).
  CI 가 빌드한 사이트를 `scripts/check_site_seo.py` 로 검사한다
- 문서 사이트: 한/영 `hreflang` 을 절대 URL + `x-default` 로. 영어판이 없어 한국어 본문으로 대체된 `/en/` 사본은
  canonical 을 한국어판으로 돌리고 hreflang·sitemap 에서 뺀다(중복 문서 정리)
- 문서 사이트: 주요 페이지(홈·why·migration·MCP·FAQ·문제 해결·쿡북 등, 한/영)에 검색 결과용 제목(`seo_title`)과
  설명(`description`) — 내비게이션 이름은 그대로
- 문서 사이트: 생성 페이지(엔드포인트 목록·필드 레퍼런스 15쪽)도 `scripts/gen_docs.py` 가 검색 제목·설명을 함께 만든다
- 문서 배포 뒤 바뀐 페이지 URL 을 IndexNow(Bing·Naver 등)에 알린다 — `scripts/indexnow.py`, 키 파일 `docs/<키>.txt`.
  실패해도 배포는 성공으로 둔다
- 문서 사이트: 쓸모 있는 링크를 단 404 페이지(noindex), 바닥글 GitHub·PyPI 링크, `site_author`
- 문서: "맥·리눅스에서 키움증권 API 쓰기"(한/영) — OCX 없이 설치부터 첫 조회·일봉 DataFrame·실시간 체결·서버 실행까지
- README(한/영) 첫 문단에 OpenAPI+(OCX) 대체·자동매매 용도를 밝힌다
- PyPI 요약·키워드에 "OCX 없이 macOS·Linux" (`openapi-plus`·`macos`·`linux`)
- 문서(영어): "Migrating from OpenAPI+ (OCX) / pykiwoom" — TR·함수·주문 코드·실시간 타입 대응표 영어판.
  영어판 링크의 "(Korean)" 표시가 번역이 생긴 페이지에 남지 않게 검사(`tests/test_docs_en.py`)
- 문서(영어): 쿡북 첫 페이지·일봉 DataFrame·연속조회(pagination) 영어판 — 예제는 한국어판처럼 테스트가 가짜 응답에 대고 실행한다
- 문서(영어): 쿡북 "호가단위에 맞춘 지정가 주문(모의투자)"·"잔고·평가 요약" 영어판
- 문서(영어): 쿡북 "WebSocket 실시간 체결·호가"·"조건검색 실시간" 영어판
- 문서(영어): 쿡북 "asyncio 동시 조회"·"호출 제한(429) 다루기" 영어판 — 쿡북 전 페이지 영어판 완료
- 문서(영어): "편의 기능"(from_env·종목코드 찾기·코드값 상수·to_ohlcv·호가 계산·예외·CLI) 영어판
- MCP: 의도 도구 골격 `kiwoom_client.mcp.intents` — 등록 레지스트리, 숫자·퍼센트·날짜 정규화, 종목 인자(이름 또는 코드)
  해석(모호하면 후보 목록 에러), 기본 행 수 제한. `stock_snapshot` 은 `stock`(종목명)도 받고 가격의 등락 부호를 떼어 낸다
- MCP 프롬프트 `market_today`(오늘 시장)·`rebalance`(리밸런싱 계획 — 미리보기와 사용자 확인 전에는 주문 안 함).
  서버 `instructions`·`kiwoom://guide` 는 "편의 도구 먼저 → 없으면 `search_tools` → 주문은 미리보기·확인 뒤
  `confirm_token`" 순서로 다시 썼다
- MCP: `get_chart` 의도 도구 — 일·주·월·분봉 OHLCV(오름차순)와 요약(기간 수익률·고저·평균 거래량·5/20 이동평균)을
  한 번에, 연속조회로 `count` 개까지. pandas 없이 쓰는 `ohlcv_rows()`(`to_ohlcv` 와 같은 필드 규칙) 추가
- Claude Desktop 원클릭 번들 `kiwoom-client-<버전>.mcpb`(MCPB manifest 0.4, `uv` 서버 — 코드는 PyPI 에서 받는다).
  설치 화면에서 앱키·시크릿(가림), 모의투자 여부(기본 켬), 모드, toolset 을 받고 실주문 opt-in 은 넣지 않는다.
  `scripts/build_mcpb.py` 가 공식 `@anthropic-ai/mcpb` 로 검증·팩하고, CI 가 매 PR 에 돌린다.
  릴리스 태그 때 PyPI 배포가 끝나면 GitHub Release 에 붙는다(`mcpb-release.yml`)
- `kiwoom-client-mcp doctor` — 서버를 띄우지 않고 설정 점검: 파이썬·`mcp` 버전, 환경변수 유무(값은 출력 안 함),
  모의/실전·모드·toolset·실주문 가드 상태, 노출될 도구 수와 `tools/list` 크기. 기본은 네트워크 호출 없음,
  `--check-auth` 일 때만 토큰을 한 번 발급한다(폐기 안 함)
- MCP: `get_quotes` 의도 도구 — 최대 20종목의 현재가·등락률·거래량·거래대금·시가총액을 ka10095 요청 한 번에. 종목별 부분 실패는 그 종목만 error
- `kiwoom-client-mcp config vscode`(GitHub Copilot 의 `.mcp.json`·`~/.copilot/mcp-config.json`, `type: "stdio"`)·
  `config gemini-cli`(`~/.gemini/settings.json`). `config claude-desktop` 안내에 `.mcpb` 원클릭 설치를 먼저 적는다
- 문서: MCP 페이지(한/영)를 "무엇을 물어보면 되나" 표(질문 → 쓰이는 도구 → 호출 수)로 시작한다. why 페이지에 공식 MCP 와의
  구조 차이를 사실만 두 줄
- MCP: `market_movers` 의도 도구 — 거래량·상승률·하락률·거래대금·거래량 급증 상위를 시장별로, 순위 TR 요청 코드를 채워 정규화된 행으로
- MCP: `investor_flow` 의도 도구 — 종목의 일별 투자자별(개인·외국인·기관 등) 순매수와 기간 합계·순매수일 수(ka10059)
- MCP: `get_orders`(미체결·체결 주문, 다른 날 포함 — 미체결 행에 취소 미리보기 인자)·`get_buying_power`(종목별 주문가능수량·
  금액, 계좌 예수금·D+2·주문가능금액) 의도 도구
- MCP: `get_portfolio` 의도 도구 — 보유 종목별 비중(총자산·주식 대비)·평가손익·수익률, 현금(D+2)·주문가능금액·총자산, 계좌번호 마스킹
- MCP: `rebalance_plan` 의도 도구 — 목표 비중까지 매수/매도 수량(정수 주식·호가단위 단가, 매도 먼저, 현금 안에서만 매수)을
  계산만 하고 주문은 보내지 않는다. 행마다 `order_preview` 에 넘길 인자
- MCP: `watch` 의도 도구 — WebSocket 실시간 체결(0B)을 최대 60초 모아 종목별 요약(마지막가·고저·매수/매도 체결량·틱 수),
  `until` 가격 조건에 걸리면 즉시 반환. 서버의 WebSocket 하나를 조건검색과 함께 쓴다
- MCP: `condition_search_run` 의도 도구 — 조건검색식을 이름(일부)이나 번호로 바로 실행해 종목명·현재가·등락률을 숫자로(목록조회·seq 불필요)

### Changed

- README·문서 첫 화면의 데모 GIF 흐름을 바꿨습니다 — 포트폴리오 요약 → 리밸런싱 계산 → 주문 미리보기(전송 없음) 흐름이고, 화면마다 "가상 데이터" 표시가 보입니다
- MCP 프롬프트(`analyze_stock`·`review_account`·`market_today`·`rebalance`), `kiwoom://guide`, 서버 instructions 가
  TR 도구 대신 의도 도구(`get_chart`·`investor_flow`·`get_portfolio`·`get_orders`·`market_movers`·`rebalance_plan`)를
  안내합니다. smart 모드에서 `search_tools` 왕복이 줄어듭니다. 프롬프트가 다시 TR 도구를 가리키면 테스트가 실패합니다.
- MCP 서버의 기본 모드가 `smart` 로 바뀝니다: `tools/list` 에 편의 도구(`stock_search`·`stock_snapshot`·
  `account_summary`·`order_preview` 등)와 메타 도구 3개(`search_tools`·`describe_tool`·`call_tool`)만 올리고,
  나머지 TR 도구는 메타 도구로 찾아 부릅니다. TR 도구 181개를 전부 올리면 도구 정의만 약 222 K 글자라
  에이전트 컨텍스트를 대화 전에 다 써 버리기 때문입니다(smart 는 약 7.5 K). 전처럼 전부 올리려면
  `KIWOOM_MCP_MODE=full` 또는 `kiwoom-client-mcp --full`. 실주문 가드·toolset 필터는 모든 모드에서 먼저 적용됩니다.
  파이썬에서 직접 부르는 `build_server()` 의 기본은 그대로 전체 목록입니다
- MCP: 실전 서버에서 opt-in 으로 노출한 TR 주문 도구(`order_*`·`credit_order_*`)가 `order_preview` 의 `confirm_token` 을
  요구한다 — `KIWOOM_MCP_REQUIRE_CONFIRM`(실전 기본 `true`, 모의 기본 `false`). 토큰은 요청 필드로 전송되지 않는다
- MCP: TR 주문 도구(`order_*`·`credit_order_*`)가 TR 카탈로그의 요청 필드만 받는다 — 모르는 키가 섞이면 전송하지 않고
  거부한다(입력 스키마 `params` 도 `additionalProperties: false`). 조회 도구는 그대로
- MCP: 도구 응답의 계좌번호 필드(`acnt_no`·`acctNo`·`acnt_print` 등, TR 카탈로그 기준)를 끝 4자리만 남기고 가린다.
  그대로 받으려면 `KIWOOM_MCP_MASK_ACCOUNTS=false`

## [0.5.0] - 2026-11-21

기존 코드는 그대로 돕니다 — `request()`·토큰 갱신·Rate Limiter·`tick_size`/`round_to_tick` 결과·
`is_mock=False` 기본값은 바뀌지 않았습니다. MCP 서버를 쓴다면 아래 **Changed** 의 두 항목을 확인하세요.

### Added

**시작·조회 편의**

- `KiwoomAPI.from_env()` / `AsyncKiwoomAPI.from_env()` — `KIWOOM_APP_KEY`·`KIWOOM_APP_SECRET`·`KIWOOM_IS_MOCK`
  환경변수나 `.env` 파일로 클라이언트를 만든다. `is_mock` 이 어디에도 없으면 실전 + 경고 (#14)
- `api.find_stock()`·`api.stock_code("삼성전자")`·`api.stock_list()` — 종목명↔종목코드 (ka10099 캐시) (#48)
- `to_ohlcv()` — 차트 응답을 시간 인덱스 `open/high/low/close/volume` DataFrame 으로 (#41)
- 호가 산술 `add_ticks()`·`ticks_between()`·`round_up_to_tick()`·`is_on_tick()` (#30)
- `kiwoom_client.codes` — `OrderType`·`Exchange`·`Market` 등 공식 코드값 `str` Enum, `exchange_stock_code()` (#18)
- `timeout=` 옵션(기본 30초 그대로)과 DEBUG 요청 추적 로그 — 헤더·본문은 남기지 않는다 (#57)
- 조회 전용 CLI `kiwoom` — `quote`·`chart`·`balance`·`find`·`endpoints` (주문 기능 없음) (#64)

**TR 명세·검증**

- `kiwoom_client.spec` — 키움 공식 명세에서 만든 TR 요청·응답 필드 카탈로그 (#21)
- `api.describe("ka10001")` — 호출 예·필수 필드·응답 필드를 네트워크 없이 (#65)
- `spec.label()` / `spec.field_names()` — 응답 필드·실시간 FID 를 한글명으로 (#66)
- `kiwoom_client.spec.responses` — 자주 쓰는 TR 10개의 응답 TypedDict (#71)
- `validate_params="warn"|"error"` — 보내기 전에 필드 오타·빠진 필수 필드를 알린다 (기본 꺼짐) (#45)
- 엔드포인트 메서드 `.pyi` 스텁 — 요청 필드가 IDE 자동완성·mypy 에 키워드 인자로 보인다 (#27)

**오류·디버깅**

- 예외 계층 `KiwoomError` 와 `KiwoomTokenError`·`KiwoomServerMismatchError`·`KiwoomRateLimitError`·
  `KiwoomRequestError`·`KiwoomStockNotFoundError`·`KiwoomUnsupportedError` — 모두 `KiwoomAPIError` 하위라
  기존 `except` 는 그대로 잡는다. `KiwoomAPIError.error_code` (#24)
- `exc.hint` — 다음 할 일 한 줄 (예: 모의/실전 불일치면 맞는 `is_mock`) (#37)
- 클라이언트·인증·WebSocket 객체의 `repr()` 이 시크릿·토큰을 가린다 (#51)

**MCP 서버**

- `order_preview` — 주문을 보내지 않고 호가단위 보정·필드 검증·예상 금액 (#25)
- 편의 도구 `stock_search`·`stock_snapshot`·`account_summary` (조회 전용) (#53)
- discovery 모드(`KIWOOM_MCP_MODE=discovery` / `--discovery`) — 메타 도구 3개로 도구 정의 컨텍스트를 크게 줄인다 (#32)
- `KIWOOM_MCP_TOOLSETS` / `--toolsets` 로 노출할 모듈 선택, `max_rows` 로 큰 리스트 응답 자르기 (#11, #43)
- resources(가이드·도구 목록·코드표·`kiwoom://tr/{api_id}`)와 prompts(`analyze_stock`·`review_account`·`order_checklist`) (#61)
- 도구 `title`·annotations(조회 `readOnlyHint`, 주문 `destructiveHint`), `serverInfo` 의 version·instructions (#9, #67)
- `kiwoom-client-mcp --help`·`--version`·`--mock`, `config claude-code|claude-desktop|cursor|codex` 설정 스니펫 (#19)
- MCP 레지스트리용 `server.json` (#67)

**AI 코딩 도구**

- `llms.txt`·`llms-full.txt`, `AGENTS.md`, Cursor 규칙·Copilot 지침 — 같은 규칙에서 생성 (#29, #56, #69)
- Claude Code 스킬과 플러그인 마켓플레이스 — `/plugin marketplace add younghwan91/kiwoom-client` (#63)

**문서**

- 문서 사이트(MkDocs, 한·영) — 엔드포인트 전체 표, TR별 필드 레퍼런스, MCP 서버, 편의 기능, 쿡북(모의투자 레시피 8개),
  문제 해결(오류코드별), FAQ, OpenAPI+·pykiwoom 옮겨 오기, 비교, 자료 모음, 쓰이는 곳
  (#13, #23, #33, #49, #50, #58, #60, #62, #68, #75, #76, #77, #78)
- 문서 사이트를 GitHub Pages(https://younghwan91.github.io/kiwoom-client/)에 main 머지마다 자동 배포,
  사이트 루트에 `llms.txt`·`llms-full.txt`. 패키지 `Documentation` URL·README 링크가 사이트를 가리킨다 (#86, #88)
- `SECURITY.md`·`CODE_OF_CONDUCT.md`, 이슈 폼·PR 템플릿, CONTRIBUTING 보강 (#20, #22, #38)
- 사용법 질문은 GitHub Discussions 로 — 이슈 선택 화면·CONTRIBUTING·FAQ 에 안내 (#87)

### Changed

- **MCP 서버가 `KIWOOM_IS_MOCK=1`/`yes`/`on` 을 이제 모의투자로 읽는다** — 전에는 `true` 만 모의로 보고 나머지는
  실전으로 붙었다. `from_env()` 와 같은 규칙이며, 모르는 값(`ture` 등)은 서버를 띄우지 않고 시작 오류로 끝난다.
  미설정은 지금처럼 실전. `KIWOOM_MCP_ALLOW_LIVE_ORDERS` 는 여전히 `true` 만 인정한다 (#73)
- **`[mcp]` extra 가 `mcp>=2.0,<3`** — 서버는 mcp 2.x API 를 쓰는데 `mcp>=1.0` 을 허용해, 1.x 가 깔린 환경에서는
  import 부터 실패했다. CI 가 하한(mcp 2.0.0)에서도 테스트한다 (#67, #83)
- 힌트가 있는 오류는 `str(exc)` 둘째 줄에 `힌트: …` 가 붙는다. 첫 줄·`code`·`message`·예외 타입은 그대로 (#37)
- 토큰 발급이 HTTP 오류로 끝나면 메시지에 응답의 `return_msg` 를 덧붙인다 (#37)
- MCP REST 도구의 입력 스키마·설명에 공식 TR 이름·api_id·필드 한글명·필수 여부가 실린다.
  `params={...}` 호출은 그대로이고, 필드를 평평하게 넘겨도 받는다 (#42, #55)
- TR 카탈로그(`kiwoom_client.spec`)에서 키움 명세 원문의 필드 설명(`desc`)·코드값 목록(`codes`)을 뺐다 —
  필드 ID·한글명·타입·길이·필수만 남는다. `Field.desc`/`Field.codes` 는 하위 호환으로 남아 늘 비어 있고,
  `describe()`·MCP 스키마·필드 레퍼런스에서도 빠졌다. 자주 쓰는 코드값은 `kiwoom_client.codes`, 나머지는
  키움 REST API 포털 문서를 본다 (#85)
- README 첫 화면과 빠른 시작을 `from_env()`·MCP 30초 시작 위주로 다시 썼다 (#46, #68)

### Fixed

- 문서·예제의 TR 요청이 공식 명세와 달랐다 — 순위 예제의 없는 필드명, 일봉의 `upd_stkpc_tp`(수정주가구분)와
  계좌 조회·거래량 상위의 빠진 필수 필드. 문서 테스트가 이제 없는 필드와 빠진 필수 필드를 모두 잡는다 (#72, #79)
- `KiwoomAPIError`(와 하위 예외)·`KiwoomParamError` 를 pickle 할 수 있다 — multiprocessing 워커에서 던진 예외가
  부모 프로세스로 넘어온다 (#80)
- PyPI 프로젝트 페이지에서 README 그림·링크가 깨지던 문제 (#40)
- MCP `initialize` 응답의 `serverInfo.version` 이 빈 문자열이던 문제 (#67)

## [0.4.0] - 2026-09-13

### Added

- **MCP 서버.** `pip install 'kiwoom-client[mcp]'` 후 `kiwoom-client-mcp`로
  실행하면 Claude Code/Cursor 등에서 182개 REST 엔드포인트 + condition_search
  4종을 도구로 직접 호출할 수 있습니다. 주문/신용주문 도구는 실전투자 계좌에서
  `KIWOOM_MCP_ALLOW_LIVE_ORDERS=true`를 명시해야 노출됩니다.
- **`tick_size`/`round_to_tick`/`ticks_in`.** KRX 호가단위(2023-01-25 통합
  기준) 유틸. scalp-it·krx-signal-engine이 각자 구현해둔 같은 표를 여기로
  모았다 — 주문가를 실제로 계산하는 이 레포가 정본이 되는 게 맞다.

### Fixed

- **`request_all()`가 실제 페이지네이션이 필요한 엔드포인트에서 1페이지 만에
  조용히 멈췄습니다.** Kiwoom은 연속조회 여부(`cont-yn`/`next-key`)를 응답
  **헤더**로 주는데, `_accumulate()`는 JSON 바디에서만 그 키를 찾고 있었습니다
  — 실제로는 바디에 없으니 매번 즉시 종료, 에러도 없이 데이터만 덜 옵니다.
  `request()`가 이제 응답 헤더를 바디에 옮겨 넣어 채워줍니다. (scalp-it을
  이 클라이언트로 옮기려다 발견 — 테마·차트처럼 페이지가 여러 장 나오는
  엔드포인트를 실제로 쓰는 코드가 아직 없어서 안 걸렸던 것으로 보입니다.)

## [0.3.0] - 2026-09-05

### ⚠️ Breaking

- **임포트 경로가 바뀌었습니다.** 저장소·PyPI 배포명(`kiwoom-client`)과
  실제 파이썬 모듈명이 서로 달라 혼란을 준다는 지적에 따라, 모듈명을
  `kiwoom_rest_api` 에서 `kiwoom_client` 로 통일했습니다.

  ```python
  # 이전 (0.2.x)
  from kiwoom_rest_api import KiwoomAPI

  # 이후 (0.3.0+)
  from kiwoom_client import KiwoomAPI
  ```

  `sed -i 's/kiwoom_rest_api/kiwoom_client/g'` 로 기존 코드베이스를 일괄
  치환할 수 있습니다. GitHub 저장소 이름도 `kiwoom-rest-api` 에서
  `kiwoom-client` 로 함께 바꿨습니다 (GitHub 이 이전 URL을 자동 리다이렉트).

## [0.2.2] - 2026-08-30

문서·배포 파이프라인만 손봅니다. **라이브러리 코드는 0.2.1 과 한 줄도 다르지
않으므로, 0.2.1 사용자가 굳이 올릴 이유는 없습니다.**

### 문서

- README 를 축약 이전의 전체 문서로 되돌렸습니다. PyPI 프로젝트 페이지 본문이
  README 라, 이 릴리즈로 페이지가 함께 갱신됩니다.
- 사실 오류를 고쳤습니다 — "186개 엔드포인트"는 REST **182개 + 조건검색 4종**
  입니다(코드의 고유 `api_id` 는 182개이고 조건검색 4개는 `api_id` 가 없습니다).
  조건검색 표의 `ka10171`~`ka10174` 는 코드에 없는 ID 라 `trnm`
  (`CNSRLST`/`CNSRREQ`/`CNSRCLR`) 기준으로 다시 썼고, `api.login()` 주석의
  `au10001`/`au10002` 도 걷어냈습니다. 무인자로 부르던
  `top_volume_today()` 예제에 필수 파라미터 6개를 채웠습니다.

### CI

- 배포 워크플로가 `actions/checkout` 에서 죽던 문제를 고쳤습니다. `permissions`
  블록에 `id-token: write` 만 적혀 있어 `contents` 가 `none` 으로 깎였고,
  `GITHUB_TOKEN` 에 읽기 권한이 없어 GitHub 이 404 를 돌려주고 있었습니다
  (`remote: Repository not found`). `contents: read` 를 추가했습니다.

## [0.2.1] - 2026-08-15

실서버 프로토콜 검증에서 드러난 문제를 고칩니다. **0.2.0 사용자는 업그레이드를
권합니다** — 토큰 자동 갱신의 안전망이 실제로는 작동하지 않았습니다.

### 수정

- **만료 토큰 자동 재발급이 트리거되지 않던 문제.** 키움은 무효·만료 토큰에
  HTTP 401 이 아니라 **HTTP 200 + `return_code: 3`**
  (`"인증에 실패했습니다[8005:Token이 유효하지 않습니다]"`)을 돌려줍니다.
  0.2.0 은 401 만 보고 있어서 재발급이 걸리지 않고 `KiwoomAPIError` 가
  그대로 터졌습니다. 이제 `return_code` 도 함께 봅니다
  (`BaseClient.TOKEN_ERROR_RETURN_CODES`).
  선제 갱신 경로는 0.2.0 에서도 정상이었으므로, 그쪽으로 막히던 경우가
  대부분이고 이번 수정은 안전망을 되살리는 것입니다.
- WebSocket 핸드셰이크 중 서버가 연결을 끊으면 raw `ConnectionClosedOK` 가
  올라와 원인을 알 수 없었습니다. 이제 `KiwoomWebSocketError` 로 상황을
  설명합니다. LOGIN 응답이 JSON 이 아닌 경우도 마찬가지입니다.

### 추가

- `tests/integration_ws_smoke.py` — 실서버 프로토콜 검증 하네스. 라이브러리의
  가정(만료 필드명·인증 실패 신호·WebSocket 프레임 구조)이 실제 서버와 맞는지
  확인하고, 자동 재발급이 실제로 도는지까지 실증합니다. 비밀값은 출력하지
  않습니다.

  ```bash
  python tests/integration_ws_smoke.py --prod --env-file /path/to/.env
  ```

### 실서버 확인 결과 (2026-08-15, api.kiwoom.com)

| 항목 | 실제 |
|---|---|
| 토큰 만료 필드 | `expires_dt` (`yyyyMMddHHmmss`, 약 18시간) |
| 토큰 키 | `token` |
| 무효 토큰 | HTTP 200 + `return_code: 3` |
| 토큰 재발급 | 유효기간 내에는 **같은 토큰**을 반환하고 기존 토큰도 유효 |
| WS LOGIN 응답 | `{"trnm":"LOGIN","return_code":0,"return_msg":"","sor_yn":"Y"}` |
| WS PING | `{"trnm":"PING"}` — 필드 없는 프레임 |
| WS REG 응답 | `{"trnm":"REG","return_code":0,"return_msg":""}` |
| WS 동시 세션 | 같은 토큰으로 2세션 동시 접속 가능 |

REAL 프레임의 항목 필드명(`item`/`values`)은 장 마감 중이라 아직 미확정입니다.

## [0.2.0] - 2026-08-15

0.1.x 를 쓰고 계셨다면 코드 수정 없이 그대로 업그레이드됩니다. 동작이 바뀌는 부분은
아래 "변경"에 정리했습니다.

### 추가

- **액세스 토큰 자동 갱신.** 토큰 만료 60초 전에 선제 재발급하고, API 가 401 을
  돌려주면 재발급 후 한 번 재시도합니다. 장시간 도는 봇이 토큰 만료로 죽지 않습니다.
  - `KiwoomAuth` 가 토큰과 만료 시각을 캐싱합니다 (`token`, `expires_at`).
  - `expiry_margin` 으로 갱신 시점을 조절할 수 있습니다.
  - `TokenProvider` 프로토콜을 구현하면 Redis 등 외부 토큰 캐시로 교체할 수 있습니다.
- **asyncio 클라이언트 `AsyncKiwoomAPI`.** sync 와 동일한 엔드포인트 집합에
  `await` 만 붙이면 됩니다. 서로 다른 TR 호출이 동시에 나갑니다.
  ```python
  async with AsyncKiwoomAPI(app_key="...", app_secret="...") as api:
      info = await api.stock_info.basic_stock_info(stk_cd="005930")
  ```
- **응답 파싱 헬퍼.** 키움이 문자열로 주는 값을 숫자로 바꿔줍니다.
  - `to_number("+70000")` → `70000`
  - `normalize(response)` — 응답 전체를 재귀 변환
  - `extract_records(response)` — 엔드포인트마다 다른 페이로드 키를 자동 탐지
  - `to_dataframe(response)` — pandas DataFrame 으로 변환
    (`pip install 'kiwoom-client[pandas]'`)
  - 종목코드(`"005930"`)와 날짜(`base_dt`)는 문자열로 남습니다.
- `KiwoomAuthError` — 토큰 발급/폐기 실패 시 raw httpx 예외 대신 이 예외가 납니다.
- `pandas` optional extra 추가.
- **WebSocket 조건검색 연동.** `api.condition_search`가 만든 페이로드를
  `ws.send()`로 보내고 `ws.on_trnm()`으로 응답을 받습니다.
- WebSocket 콜백에 async 함수를 등록할 수 있습니다. `ws.on_message()`로 모든
  프레임을 볼 수 있습니다.

### 변경

- **`login()` 이 선택 사항이 되었습니다.** 첫 API 호출에서 토큰이 자동 발급됩니다.
  기존처럼 `login()` 을 호출해도 그대로 동작하며, 잘못된 키를 즉시 확인하고 싶을 때
  유용합니다.
- 토큰 발급 실패 시 `httpx.HTTPStatusError` 대신 `KiwoomAuthError` 가 발생합니다.
- `BaseClient` 가 재시도할 때마다 인증 헤더를 새로 만듭니다. 예전에는 요청 시작
  시점의 헤더를 재사용해서, 재시도 중 토큰이 갱신돼도 반영되지 않았습니다.
- 엔드포인트 모듈이 `Generic[ResponseT]` 가 되었습니다. sync 사용자에게는
  타입이 그대로(`dict[str, Any]`)이지만, 모듈을 직접 임포트해 타입을 명시하던
  코드라면 `Account` → `Account[dict[str, Any]]` 로 파라미터를 채워야 합니다.
- **WebSocket 콜백이 받는 데이터 모양이 바뀌었습니다.** 이제 REAL 프레임의 항목
  하나(`{"type", "item", "values"}`)를 받습니다. `values` 의 키는 FID 번호입니다.
  기존 콜백은 애초에 호출되지 않았으므로 실동작이 깨질 코드는 없습니다.
- `KiwoomWebSocket.send_condition_search()` 가 `send()` 로 바뀌었습니다.
- `create_websocket()` 이 `login()` 을 요구하지 않습니다.

### 수정

- `kiwoom_rest_api.__version__` 이 `"0.1.0"` 으로 고정돼 있어 실제 버전과
  달랐습니다. 이제 패키지 메타데이터에서 읽습니다.
- **WebSocket 프로토콜이 키움 스펙과 어긋나 있었습니다.** 아래 넷을 고쳤습니다.
  - `LOGIN` 핸드셰이크를 보내지 않고 토큰을 HTTP 헤더에만 실었습니다.
  - 서버 `PING` 에 응답하지 않아 연결이 끊겼습니다. 이제 프레임을 그대로 반향합니다.
  - 등록 메시지가 `{"trnm":"subscribe","stk_cd_lst":[...]}` 였습니다.
    실제 포맷은 `{"trnm":"REG","grp_no":"1","refresh":"1","data":[{"item":[...],"type":[...]}]}` 입니다.
  - 수신 메시지를 `grp_no`/`api_id` 로 찾아 **`ws.on("0B", ...)` 콜백이 한 번도
    호출되지 않았습니다.** 실제 구조는 `{"trnm":"REAL","data":[{"type":"0B",...}]}` 이며,
    이제 항목별 `type` 으로 디스패치합니다.
- 재연결 시 로그인과 구독을 복원하지 않아, 끊긴 뒤로는 데이터가 오지 않았습니다.
- 조건검색 모듈이 REST 형식(`{"api_id":"ka10171"}`)을 만들었습니다. 조건검색은
  WebSocket `trnm`(`CNSRLST`/`CNSRREQ`/`CNSRCLR`)으로 나갑니다.

### 개발

- CI 에 ruff·mypy 검사 추가. ruff/mypy 설정을 `pyproject.toml` 에 고정했습니다.
- 테스트 43개 → 144개. WebSocket 은 로컬 서버로 프로토콜을 검증합니다.

### 알려진 이슈

- WebSocket 수정은 키움 공식 프로토콜 문서를 근거로 구현하고 로컬 프로토콜
  테스트로 검증했지만, **실계좌 검증은 아직입니다.** 특히 REAL 프레임 항목의
  세부 필드명(`item`/`values`)은 등록 메시지 구조에서 유추한 부분이 있습니다.
  실제 동작이 다르면 [이슈](https://github.com/younghwan91/kiwoom-client/issues)로
  알려주세요.

## [0.1.14] - 2026-08

### 변경

- 수급 앱 코드를 별도 레포로 분리해 라이브러리를 가볍게 유지합니다.

## [0.1.13]

### 추가

- TR(api_id)별 Rate Limiter 와 429 자동 재시도. 실측 한도(초당 1건, 버스트 2)에
  맞춰 기본값을 잡았습니다.

### 수정

- 토큰 발급/폐기 요청의 필드명을 `appsecretkey` → `secretkey` 로 수정.

[0.2.1]: https://github.com/younghwan91/kiwoom-client/releases/tag/v0.2.1
[0.2.0]: https://github.com/younghwan91/kiwoom-client/releases/tag/v0.2.0
[0.1.14]: https://github.com/younghwan91/kiwoom-client/releases/tag/v0.1.14
[0.1.13]: https://github.com/younghwan91/kiwoom-client/releases/tag/v0.1.13
