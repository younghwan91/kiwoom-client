---
seo_title: "키움증권 MCP 서버 — Claude·Cursor 에서 시세·계좌 조회"
description: "kiwoom-client-mcp 로 Claude Code·Claude Desktop·Cursor·Codex 가 키움 REST API 를 MCP 도구로 불러 시세·차트·순위·계좌를 조회합니다. 실계좌 주문 도구는 직접 켜기 전엔 등록되지 않습니다."
---

# MCP 서버

`kiwoom-client-mcp` 는 키움 REST API 를 MCP(Model Context Protocol) 도구로 노출합니다. Claude Code·Claude Desktop·Cursor·Codex 같은 에이전트가 시세·차트·순위·계좌를 직접 조회합니다. 실전 계좌의 주문 도구는 직접 켜기 전에는 **등록조차 되지 않습니다**.

## 설치

설치 없이 [uv](https://docs.astral.sh/uv/) 로 바로 띄우는 것이 가장 간단합니다.

```bash
uvx --from 'kiwoom-client[mcp]' kiwoom-client-mcp --help
```

pip 로 설치해도 됩니다. `[mcp]` extra 가 필요합니다(`mcp>=2.0`).

```bash
pip install 'kiwoom-client[mcp]'
kiwoom-client-mcp --version
```

앱키·시크릿키는 [키움 REST API 포털](https://openapi.kiwoom.com)에서 발급합니다. 처음에는 모의투자 키로 시작하세요(모의투자와 실전투자 키는 서로 다르고, 다른 서버에 쓰면 8030 오류가 납니다).

## 클라이언트에 붙이기

### Claude Desktop: 원클릭 번들 (.mcpb)

[GitHub Releases](https://github.com/younghwan91/kiwoom-client/releases) 의 `kiwoom-client-<버전>.mcpb` 를 받아 더블클릭하거나, Claude Desktop 의 설정 → 확장 프로그램 화면에 끌어다 놓습니다(번들은 0.5.0 다음 릴리스부터 붙습니다). 설치 화면에서 받는 값은 아래와 같습니다.

| 항목 | 기본값 | 설명 |
|---|---|---|
| 앱키·시크릿키 | — | 입력값을 가리고 안전한 저장소에 보관합니다 |
| 모의투자 서버 | 켜짐 | 끄면 실전 서버에 조회만 합니다. 이 번들로는 실전 주문 도구를 켤 수 없습니다 |
| 도구 목록 모드 | `smart` | `full`·`discovery` (아래 "컨텍스트 줄이기") |
| 노출할 모듈 | 비움(전부) | 예: `market,chart,account` |

번들에는 서버 코드가 들어 있지 않습니다. 처음 실행할 때 uv 가 PyPI 에서 번들과 같은 버전의 `kiwoom-client[mcp]` 를 받습니다. 직접 만들려면 `python scripts/build_mcpb.py` 를 실행합니다(Node.js 필요, 공식 `@anthropic-ai/mcpb` CLI 로 검증하고 팩).

### 설정 스니펫

`config` 명령이 클라이언트별로 붙여넣을 설정을 출력합니다. 키는 `YOUR_APP_KEY` 같은 자리표시자로 나오고, 기본값은 모의투자입니다. 키와 네트워크 없이 동작합니다.

```bash
kiwoom-client-mcp config claude-code      # 터미널에서 실행할 claude mcp add 명령
kiwoom-client-mcp config claude-desktop   # claude_desktop_config.json 에 병합할 JSON
kiwoom-client-mcp config cursor           # ~/.cursor/mcp.json 또는 .cursor/mcp.json
kiwoom-client-mcp config codex            # ~/.codex/config.toml
```

붙여넣을 본문은 stdout, 파일 위치 안내는 stderr 로 나옵니다. 그래서 `> mcp.json` 으로 저장해도 유효한 JSON 입니다. 쓸 수 있는 옵션은 아래와 같습니다.

| 옵션 | 효과 |
|---|---|
| `--live` | `KIWOOM_IS_MOCK=false`(실전 서버 조회). 주문 도구는 여전히 꺼져 있음 |
| `--toolsets market,chart` | 노출할 모듈만 넣음 |
| `--full` | TR 도구 전부를 목록에 올림(아래 "컨텍스트 줄이기") |
| `--discovery` | 메타 도구 3개만 노출 |
| `--launcher installed` | `uvx` 대신 PATH 의 `kiwoom-client-mcp` 를 씀 |

Claude Code 예시(출력 그대로):

```bash
claude mcp add kiwoom -e KIWOOM_APP_KEY=YOUR_APP_KEY -e KIWOOM_APP_SECRET=YOUR_APP_SECRET \
  -e KIWOOM_IS_MOCK=true -- uvx --from 'kiwoom-client[mcp]' kiwoom-client-mcp
```

## 환경변수와 옵션

| 환경변수 | CLI | 설명 | 기본값 |
|---|---|---|---|
| `KIWOOM_APP_KEY`, `KIWOOM_APP_SECRET` | — | 앱키·시크릿키 (서버 실행 시 필수) | — |
| `KIWOOM_IS_MOCK` | `--mock` | 모의투자 서버. true/false·1/0·yes/no 만 받고 그 밖의 값은 에러 | `false` (실전) |
| `KIWOOM_MCP_TOOLSETS` | `--toolsets` | 노출할 모듈, 쉼표 구분. `all` = 전부 | 전부 |
| `KIWOOM_MCP_MODE` | `--full`, `--discovery` | `smart`·`full`·`discovery` (아래 "컨텍스트 줄이기") | `smart` |
| `KIWOOM_MCP_MAX_ROWS` | `--max-rows` | 리스트 응답 기본 행 수 제한 | 제한 없음 |
| `KIWOOM_MCP_ALLOW_LIVE_ORDERS` | (없음) | 실전 계좌에서 주문 도구 노출 | `false` |
| `KIWOOM_MCP_REQUIRE_CONFIRM` | (없음) | TR 주문 도구(`order_*`·`credit_order_*`)에 `confirm_token` 요구 | 실전 `true`, 모의 `false` |

CLI 옵션이 환경변수보다 우선합니다. 실주문 opt-in 에는 일부러 CLI 옵션을 두지 않았습니다.

toolset 이름은 엔드포인트 모듈 이름과 같습니다: `account`, `stock_info`, `market`, `chart`, `order`, `credit_order`, `ranking`, `sector`, `foreign_institution`, `short_selling`, `slb`, `theme`, `condition_search`, `elw`, `etf`.

## 실주문 가드

- `KIWOOM_IS_MOCK=false`(실전)이고 `KIWOOM_MCP_ALLOW_LIVE_ORDERS=true` 가 아니면 주문 도구(`order_*` 8개, `credit_order_*` 4개, `place_order`·`modify_order`·`cancel_order`)를 서버가 **등록하지 않습니다**. 도구 목록, `call_tool`, `search_tools`, `kiwoom://tools` 어디에도 나오지 않습니다.
- toolset 필터·모드(smart·full·discovery)·편의 도구는 모두 가드가 남긴 도구만 봅니다. `--toolsets order` 로 골라도 opt-in 없이는 주문 도구가 생기지 않습니다. 이 동작은 회귀 테스트(`tests/test_mcp_live_order_regression.py`)로 고정돼 있습니다.
- 모의투자(`KIWOOM_IS_MOCK=true`)는 실제 체결이 없으므로 가드 없이 주문 도구가 보입니다.
- 가드는 MCP 서버 경로에만 있습니다. 파이썬에서 `KiwoomAPI`/`AsyncKiwoomAPI` 를 직접 쓰면 막지 않습니다.

주문 도구에는 `destructiveHint=true` annotation 이 붙습니다. 그래서 클라이언트는 실행 전에 확인을 받을 수 있습니다. 조회 도구는 `readOnlyHint=true` 입니다.

### 주문 미리보기 `order_preview`

주문을 보내지 않고 다음을 돌려줍니다. 종목명을 넣었을 때 종목 리스트(ka10099)를 조회하는 것 말고는 네트워크 호출이 없습니다.

- 호가단위 보정: 매수는 내림, 매도는 올림
- 필드 검증
- 예상 금액
- 경고
- 주문 도구에 그대로 넘길 `params`
- 주문 도구가 등록된 서버라면 그 주문에만 쓸 수 있는 `confirm_token`

종목은 `stock`(이름 또는 코드)이나 `stk_cd` 로, 수량·단가는 `qty`·`price`(`"market"` = 시장가)나 TR 필드명(`ord_qty`·`ord_uv`)으로 받습니다. `action="modify"`·`"cancel"` 과 `order_no` 를 주면 정정·취소 미리보기를, `tool`(예: `credit_order_margin_buy_order`)과 `params` 를 주면 그 TR 도구용 미리보기를 만듭니다.

`order_tools_enabled` 값으로 이 서버에 주문 도구가 있는지도 알려 줍니다. 에이전트는 미리보기를 사용자에게 보여 주고 확인을 받은 뒤에만 주문해야 합니다. 서버의 `instructions` 와 `order_checklist`·`rebalance` 프롬프트가 이 순서를 안내합니다.

### 확인 토큰 (2단계 주문)

`confirm_token` 은 서버가 만듭니다. 미리보기한 주문의 TR 도구 이름과 정규화한 요청 필드를, 프로세스를 시작할 때 만든 무작위 비밀키로 HMAC 서명합니다. 토큰 안에 주문 내용은 들어 있지 않습니다. 주문 도구는 다음 경우 주문을 **보내지 않고** 거부합니다.

- 토큰이 없을 때
- 미리보기와 종목·수량·단가·매매구분 등이 하나라도 다를 때
- 120초가 지났을 때
- 이미 쓴 토큰일 때
- 서버를 다시 시작하기 전에 받은 토큰일 때

`place_order`·`modify_order`·`cancel_order` 는 늘 토큰을 요구합니다. TR 주문 도구(`order_*`·`credit_order_*`)는 `KIWOOM_MCP_REQUIRE_CONFIRM` 을 따르며, 실전은 기본 `true`, 모의투자는 기본 `false` 입니다. 요구하지 않는 설정에서도 토큰을 넣으면 검사합니다. 이 검사는 실주문 opt-in 가드 **다음에** 적용됩니다. opt-in 없이 주문 도구가 등록되지 않는 동작은 그대로입니다.

## 도구

| 종류 | 이름 | 비고 |
|---|---|---|
| 의도 도구 | `stock_search` | 종목명·코드로 종목 찾기(ka10099, 캐시) |
| | `stock_snapshot` | 현재가·등락률·시총·PER/PBR 등 한 번에(ka10001). 종목명으로도 받음 |
| | `account_summary` | 계좌 총평가·손익·보유 종목(kt00018) |
| | `get_chart` | 일·주·월·분봉 OHLCV(날짜 오름차순) + 기간 수익률·고저·평균 거래량·5/20 이동평균. 연속조회로 `count` 개까지(ka10081/82/83/80) |
| | `order_preview` | 주문·정정·취소 미리보기, 전송 안 함. `confirm_token` 발급 |
| 주문 (opt-in) | `place_order`·`modify_order`·`cancel_order` | 종목명·수량·단가(또는 `"market"`)로 주문·정정·취소. `confirm_token` 필수 |
| TR 도구 | `<모듈>_<메서드>` | 예: `stock_info_basic_stock_info`, `chart_stock_daily_chart`. [전체 목록](endpoints.md) |
| 조건검색 | `condition_search_*` 4개 | WebSocket. 실시간 등록은 첫 응답만 돌려줌 |

의도 도구는 사용자가 묻는 일 하나를 호출 한 번에 답합니다. api_id·필드명을 몰라도 되고, 종목은 이름(`"삼성전자"`)이나 코드(`"005930"`)로 받습니다. 이름이 여러 종목에 맞으면 후보 목록을 담은 에러를 돌려줍니다. 응답의 숫자는 부호·쉼표·0 채움을 걷어낸 값이고, 리스트는 기본 행 수로 잘립니다. 모두 조회 전용(`readOnlyHint=true`)입니다.

TR 도구는 `params` 에 키움 요청 필드를 문자열로 넣습니다. 각 도구의 입력 스키마에 TR 카탈로그의 필드 이름·필수 여부·설명이 들어 있습니다.

```json
{"params": {"stk_cd": "005930"}}
```

연속조회는 응답의 `cont-yn`/`next-key` 를 다음 호출의 `cont_yn="Y"`, `next_key` 로 넘깁니다.

## 컨텍스트 줄이기

도구 정의는 에이전트 컨텍스트에 통째로 올라갑니다. 그래서 기본 모드(`smart`)는 편의 도구와 메타 도구 3개만 목록에 올리고, 나머지 TR 도구는 메타 도구로 찾아 씁니다. 설정별 `tools/list` 크기(실전 서버·가드 켜짐 기준 실측)는 다음과 같습니다.

| 설정 | 도구 수 | `tools/list` 크기 (글자 수) |
|---|---|---|
| 기본 `smart` | 7 | 약 3.9 K |
| `--discovery` | 3 | 약 1.4 K |
| `--full` | 178 | 약 219 K |
| `--full --toolsets market,chart,account` | 80 | 약 97 K |

(TR 도구마다 입력 스키마에 요청 필드 ID·한글명이 들어 있어 큽니다. 모의투자는 주문 도구가 더해집니다. smart 의 도구 수는 편의 도구가 늘면 같이 늘어납니다.)

- **smart 모드(기본)**: 편의 도구(`stock_search`·`stock_snapshot`·`account_summary`·`order_preview` 등)는 바로 부르고, 그 밖의 TR 은 `search_tools`(키워드·toolset 검색) → `describe_tool`(입력 스키마) → `call_tool`(실행)로 씁니다.
- **full 모드**: `--full` 또는 `KIWOOM_MCP_MODE=full`. 0.5.x 까지의 기본 동작으로, TR 도구 전부를 목록에 올립니다. 클라이언트가 메타 도구를 잘 못 쓰거나 TR 이름으로 바로 부르는 기존 설정이 있으면 이 모드로 되돌립니다.
- **discovery 모드**: 메타 도구 3개만 올립니다. 편의 도구도 `call_tool` 로 부릅니다.
- **toolset**: 쓰는 모듈만 켭니다. 모든 모드에 같이 적용됩니다.
- **`max_rows`**: 조회 도구 호출마다 `max_rows` 를 주면 응답의 각 리스트를 앞에서 N행만 남깁니다. 서버 기본값은 `--max-rows` 로 정합니다. 잘린 응답에는 `"_truncated": {"<키>": {"total": 300, "returned": 20}}` 가 붙습니다.

## resources 와 prompts

| URI | 내용 |
|---|---|
| `kiwoom://guide` | 에이전트용 사용 규칙 |
| `kiwoom://tools` | 지금 노출된 도구 목록(이름·toolset·조회 여부·api_id) |
| `kiwoom://codes/trade-types` | 매매구분 `trde_tp`·거래소구분 `dmst_stex_tp` |
| `kiwoom://codes/markets` | 시장구분 `mrkt_tp` (ka10099) |
| `kiwoom://tr/{api_id}` | TR 하나의 요청·응답 필드(예: `kiwoom://tr/ka10001`) |

서버의 `instructions` 는 "편의 도구 먼저 → 없으면 `search_tools` → 주문은 미리보기·사용자 확인 뒤" 순서를 안내합니다. 프롬프트는 다섯 가지입니다.

- `review_account()`: 잔고 점검(평가손익·미체결·예수금), 조회만
- `analyze_stock(stock)`: 종목 분석(시세·지표·일봉·수급), 조회만
- `market_today(focus?)`: 오늘 시장(업종 지수·거래대금/등락률 상위·외국인·기관), 조회만
- `rebalance(target)`: 목표 비중과 잔고를 비교해 주문 계획과 미리보기를 만들고, 확인 전에는 주문하지 않음
- `order_checklist(request)`: 미리보기를 만들고 사용자 확인 전에는 주문하지 않는 절차

## 문제 해결

먼저 `doctor` 로 설정을 점검합니다. 서버를 띄우지 않고, 키 없이도, 네트워크 호출 없이 돕니다. 환경변수는 있는지만 보여 주고 값은 출력하지 않습니다.

```bash
kiwoom-client-mcp doctor                  # 파이썬·mcp 버전, 환경변수 유무, 서버·모드·가드 상태, tools/list 크기
kiwoom-client-mcp --mock doctor           # 서버 옵션은 doctor 앞에 (실제로 띄울 때와 같은 해석)
kiwoom-client-mcp doctor --check-auth     # 토큰을 한 번 발급해 키를 확인 (키움 서버 요청 1회, 폐기는 안 함)
```

문제가 있으면 `[err]` 줄과 함께 종료 코드 1 로 끝납니다.

| 증상 | 원인·해결 |
|---|---|
| `KIWOOM_APP_KEY and KIWOOM_APP_SECRET ... must be set` | 클라이언트 설정의 `env` 에 키를 넣었는지 확인 |
| `MCP 서버에는 mcp 패키지가 필요합니다` | `[mcp]` extra 없이 설치됨. `pip install 'kiwoom-client[mcp]'` 또는 `uvx --from 'kiwoom-client[mcp]' ...` |
| `ImportError: ServerRequestContext` | 오래된 `mcp` 1.x 가 깔려 있음. `pip install -U 'mcp>=2.0,<3'` |
| `KIWOOM_IS_MOCK=... 를 해석할 수 없습니다` | true/false (또는 1/0, yes/no) 로 지정 |
| 8030/8031 오류 | 모의/실전 키와 `KIWOOM_IS_MOCK` 이 서로 맞지 않음 |
| 주문 도구가 안 보임 | 의도된 동작(실전 + opt-in 없음). 모의투자로 시험하거나 위 "실주문 가드" 참고 |
