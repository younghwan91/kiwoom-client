---
seo_title: "키움증권 MCP 서버 — Claude·Cursor 에서 시세·계좌 조회"
description: "kiwoom-client-mcp 로 Claude Code·Claude Desktop·Cursor·Codex 가 키움 REST API 를 MCP 도구로 불러 시세·차트·순위·계좌를 조회합니다. 실계좌 주문 도구는 직접 켜기 전엔 등록되지 않습니다."
---

# MCP 서버

`kiwoom-client-mcp` 는 키움 REST API 를 MCP(Model Context Protocol) 도구로 노출합니다. Claude Code·Claude Desktop·Cursor·Codex 같은 에이전트가 시세·차트·순위·계좌를 직접 조회합니다. 실전 계좌의 주문 도구는 직접 켜기 전에는 **등록조차 되지 않습니다**.

## 무엇을 물어보면 되나

기본(smart) 모드에서 자주 묻는 일과 에이전트가 부르는 도구입니다. api_id·필드명은 몰라도 되고, 종목은 이름이나 코드로 말하면 됩니다.

| 이렇게 물으면 | 쓰이는 도구 | 호출 수 |
|---|---|---|
| "삼성전자 지금 얼마야? PER 은?" | `stock_snapshot` | 1 |
| "삼성전자·SK하이닉스·NAVER 시세 한 번에" | `get_quotes` (최대 20종목) | 1 |
| "내 잔고랑 수익률 보여 줘" | `account_summary` | 1 |
| "SK하이닉스 일봉으로 최근 추세 봐 줘" | `get_chart` (일·주·월·분봉, 이동평균·기간 수익률 포함) | 1 |
| "에코프로 종목코드가 뭐야?" | `stock_search` | 1 |
| "오늘 거래량 급등 종목" | `search_tools` → `describe_tool` → `call_tool`(`ranking_sudden_volume_increase`) | 3 |
| "삼성전자 외국인 매매 추이" | `search_tools` → `describe_tool` → `call_tool`(`foreign_institution_foreign_trading_trend`) | 3 |
| "삼성전자 10주 7만원에 사 줘" | `order_preview` → 사용자 확인 → `place_order`(`confirm_token`) | 2 |
| "미체결 주문 취소해 줘" | `call_tool`(`account_unfilled_orders`, 이름·입력을 찾는 데 2회 더) → `order_preview` → 사용자 확인 → `cancel_order` | 3–5 |

- 의도 도구(위의 호출 1회짜리)는 늘어나는 중입니다. 지금 목록은 [도구](#도구)에 있습니다.
- 주문 도구(`place_order` 등)는 모의투자에서, 또는 실전에서 `KIWOOM_MCP_ALLOW_LIVE_ORDERS=true` 를 켰을 때만 있습니다([실주문 가드](#실주문-가드)).
- 그대로 붙여 넣을 질문 19개와 결과 예시는 [프롬프트 모음](prompts.md)에 있습니다.
- 프롬프트 `review_account`·`analyze_stock`·`market_today`·`rebalance`·`order_checklist` 를 고르면 위 순서를 에이전트에게 한 번에 지시합니다([resources 와 prompts](#resources-와-prompts)).

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
kiwoom-client-mcp config vscode           # VS Code(GitHub Copilot) .mcp.json 또는 ~/.copilot/mcp-config.json
kiwoom-client-mcp config gemini-cli       # ~/.gemini/settings.json
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
| `KIWOOM_MCP_READ_ONLY` | (없음) | `true` 면 주문 도구를 하나도 등록하지 않음(모의투자 포함) | `false` |
| `KIWOOM_MCP_MASK_ACCOUNTS` | (없음) | `false` 면 응답의 계좌번호를 가리지 않음 | `true` (끝 4자리만) |
| `KIWOOM_MCP_REQUIRE_CONFIRM` | (없음) | TR 주문 도구(`order_*`·`credit_order_*`)에 `confirm_token` 요구 | 실전 `true`, 모의 `false` |
| `KIWOOM_MCP_MAX_ORDER_AMOUNT` | (없음) | 주문 1건(신규·정정) 금액 한도, 원 | 제한 없음 |
| `KIWOOM_MCP_MAX_ORDER_QTY` | (없음) | 주문 1건(신규·정정) 수량 한도, 주 | 제한 없음 |
| `KIWOOM_MCP_ALLOWED_STOCKS` | (없음) | 주문할 수 있는 종목코드, 쉼표 구분 | 제한 없음 |
| `KIWOOM_MCP_DAILY_ORDER_LIMIT` | (없음) | 이 서버 프로세스가 하루(KST)에 보낼 수 있는 주문 수 | 제한 없음 |
| `KIWOOM_MCP_DUPLICATE_WINDOW` | (없음) | 똑같은 주문을 이 초 안에 다시 보내면 거부. `0` = 끔 | `10` |
| `KIWOOM_MCP_AUDIT_LOG` | (없음) | 주문 감사 로그(JSONL) 경로. `off` = 끔 | `~/.kiwoom-client/mcp-audit.jsonl` |

CLI 옵션이 환경변수보다 우선합니다. 실주문 opt-in 에는 일부러 CLI 옵션을 두지 않았습니다.

toolset 이름은 엔드포인트 모듈 이름과 같습니다: `account`, `stock_info`, `market`, `chart`, `order`, `credit_order`, `ranking`, `sector`, `foreign_institution`, `short_selling`, `slb`, `theme`, `condition_search`, `elw`, `etf`.

## 실주문 가드

- `KIWOOM_IS_MOCK=false`(실전)이고 `KIWOOM_MCP_ALLOW_LIVE_ORDERS=true` 가 아니면 주문 도구(`order_*` 8개, `credit_order_*` 4개, `place_order`·`modify_order`·`cancel_order`)를 서버가 **등록하지 않습니다**. 도구 목록, `call_tool`, `search_tools`, `kiwoom://tools` 어디에도 나오지 않습니다.
- toolset 필터·모드(smart·full·discovery)·편의 도구는 모두 가드가 남긴 도구만 봅니다. `--toolsets order` 로 골라도 opt-in 없이는 주문 도구가 생기지 않습니다. 이 동작은 회귀 테스트(`tests/test_mcp_live_order_regression.py`)로 고정돼 있습니다.
- 모의투자(`KIWOOM_IS_MOCK=true`)는 실제 체결이 없으므로 가드 없이 주문 도구가 보입니다.
- `KIWOOM_MCP_READ_ONLY=true` 면 모의투자든 opt-in 이 있든 주문 도구(`order_*`·`credit_order_*`·`place_order` 등)를 하나도 등록하지 않습니다. 조회만 시키려는 에이전트에 씁니다. `order_preview` 는 남지만 토큰을 만들지 않습니다.
- 가드는 MCP 서버 경로에만 있습니다. 파이썬에서 `KiwoomAPI`/`AsyncKiwoomAPI` 를 직접 쓰면 막지 않습니다.

주문 도구에는 `destructiveHint=true` annotation 이 붙습니다. 그래서 클라이언트는 실행 전에 확인을 받을 수 있습니다. 조회 도구는 `readOnlyHint=true` 입니다.

### 서버가 강제하는 안전장치 한눈에

모두 MCP 서버 안에서 강제되고, 모델이 넣는 값으로 끄거나 우회할 수 없습니다. 위에서부터 차례로 적용되며, 하나라도 걸리면 주문 요청을 보내지 않습니다.

| 안전장치 | 막는 것 | 어디서 | 설정 |
|---|---|---|---|
| 실주문 opt-in 가드 | 실전 계좌에 주문 도구가 생기는 것 | 서버 시작 시 도구 등록 | `KIWOOM_MCP_ALLOW_LIVE_ORDERS` (기본 꺼짐) |
| 읽기 전용 모드 | 모의투자 포함 모든 주문 도구 | 서버 시작 시 도구 등록 | `KIWOOM_MCP_READ_ONLY` |
| 미리보기 검증 | 상·하한가 밖 단가, 주문가능·매도가능수량 초과 | `order_preview` (오류면 토큰 없음) | 항상 (서버 연결 시) |
| 주문 필드 화이트리스트 | 카탈로그에 없는 요청 필드, 고수준 도구의 스키마 밖 인자 | 미리보기 + 전송 직전 | 항상 |
| 한도·허용 종목·하루 주문 수 | 큰 주문, 허용하지 않은 종목, 폭주 | 미리보기 + 전송 직전 | `KIWOOM_MCP_MAX_ORDER_AMOUNT` 등 (기본 제한 없음) |
| 중복 방지 | 같은 주문의 연속 재전송 | 전송 직전 | `KIWOOM_MCP_DUPLICATE_WINDOW` (기본 10초) |
| 확인 토큰 | 미리보기·사용자 확인 없이 보내거나 확인 뒤 내용이 바뀐 주문 | 전송 직전 | `place_order` 등은 항상, TR 도구는 `KIWOOM_MCP_REQUIRE_CONFIRM` (실전 기본 켜짐) |
| 감사 로그 | (기록) 미리보기·거부·전송·실패 | 미리보기 + 전송 전후 | `KIWOOM_MCP_AUDIT_LOG` |
| 계좌번호 마스킹 | 응답에 계좌번호 노출 | 모든 도구 응답 | `KIWOOM_MCP_MASK_ACCOUNTS` (기본 켜짐) |

모든 조합(직접 호출·`call_tool`·smart·`place_order` × 토큰 없음·위조 토큰·한도 초과·허용 종목 밖·모르는 필드·중복·하루 한도·읽기 전용)에서 주문 엔드포인트로 요청이 0건인지 회귀 테스트(`tests/test_mcp_order_safety_regression.py`)가 확인합니다.

### 주문 미리보기 `order_preview`

주문을 보내지 않고 다음을 돌려줍니다. 종목명을 넣었을 때 종목 리스트(ka10099)를 조회하는 것 말고는 네트워크 호출이 없습니다.

- 호가단위 보정: 매수는 내림, 매도는 올림
- 필드 검증
- 예상 금액
- 경고
- 주문 도구에 그대로 넘길 `params`
- 주문 도구가 등록된 서버라면 그 주문에만 쓸 수 있는 `confirm_token`

신규 주문과 정정은 조회 TR 로 한 번 더 검사합니다. 결과는 `errors`(주문 불가)와 `warnings`(근접·확인 불가)로 나오고, 조회한 값은 `checks` 에 들어갑니다. `errors` 가 하나라도 있으면 토큰을 만들지 않습니다.

| 검사 | 조회 TR | error | warning |
|---|---|---|---|
| 상한가·하한가 | ka10001 `upl_pric`·`lst_pric` | 단가가 범위 밖 | 단가가 상·하한가의 2% 안 |
| 매수 주문가능수량 | kt00011, 적용증거금율(`aplc_rt`) 기준 수량 | 수량이 주문가능수량보다 많음 | 미수 없이 살 수 있는 수량(`min_ord_alowq`)보다 많음, 또는 주문가능수량의 90% 이상 |
| 매도가능수량 | kt00018 `trde_able_qty` | 수량이 매도가능수량보다 많음, 보유하지 않은 종목 | 잔고 첫 페이지에 없음 |

시장가 매수는 상한가로 주문가능수량을 조회합니다. 조회가 실패하면 검사를 통과한 것으로 보지 않고 "검사하지 못했습니다" 경고를 남깁니다. 취소는 조회하지 않습니다.

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

### 한도·허용 종목

위 환경변수 네 개를 설정하면 서버가 주문 한도를 강제합니다. `order_preview` 에서 위반이면 `errors` 에 넣고 토큰을 만들지 않으며, 전송 직전에 한 번 더 검사해 위반이면 보내지 않고 거부합니다. 미리보기 결과를 믿지 않고 전송할 때 다시 봅니다.

- 금액은 단가 × 수량입니다. 시장가 주문은 상한가(ka10001)로 계산하며, 상한가를 조회하지 못하면 금액 한도를 확인할 수 없어 거부합니다.
- 취소는 수량·금액 한도를 보지 않습니다. 허용 종목과 하루 주문 수는 취소에도 적용됩니다.
- 하루 주문 수는 이 프로세스가 키움에 보낸 주문(신규·정정·취소)을 셉니다. 거부된 시도는 세지 않고, 서버를 다시 시작하거나 날짜(KST)가 바뀌면 0부터 셉니다.
- 설정하지 않으면 제한이 없습니다(기존 동작).

### 주문 필드 화이트리스트

주문 도구(`order_*`·`credit_order_*`)는 `params`(와 최상위에 평평하게 넣은 필드)에 TR 카탈로그의 요청 필드만 받습니다. 모르는 키가 하나라도 있으면 값이 비어 있어도 보내지 않고 거부합니다. 프롬프트 인젝션 등으로 엉뚱한 필드가 주문에 섞이는 것을 막기 위해서입니다. 입력 스키마의 `params` 도 `additionalProperties: false` 입니다. 조회 도구는 전처럼 카탈로그에 없는 필드도 키움에 넘깁니다.

### 중복 방지

방금 보낸 주문과 TR 도구·요청 필드가 똑같은 주문이 `KIWOOM_MCP_DUPLICATE_WINDOW`(기본 10초) 안에 다시 오면 보내지 않고 거부합니다. 새 미리보기로 받은 새 토큰이어도 마찬가지입니다. 재시도 루프나 같은 지시를 두 번 처리해 같은 주문이 두 번 나가는 것을 막습니다. 미리보기는 이 경우 경고를 붙이고, 거부된 주문은 기억하지 않습니다.

### 응답의 계좌번호 마스킹

모든 도구 응답에서 계좌번호 필드(TR 카탈로그에서 이름이 계좌번호인 `acnt_no`·`acctNo`·`acnt_print` 등)는 끝 4자리만 남기고 `*` 로 가립니다. 대화 기록·에이전트 로그에 계좌번호가 남지 않게 하려는 것입니다. 그대로 받으려면 `KIWOOM_MCP_MASK_ACCOUNTS=false` 로 끕니다.

### 감사 로그

서버는 주문 시도를 한 줄에 하나씩 JSON 으로 `KIWOOM_MCP_AUDIT_LOG` 파일에 덧붙입니다. 기본 경로는 `~/.kiwoom-client/mcp-audit.jsonl` 이고, `off` 로 끌 수 있습니다.

| `event` | 언제 | 주요 필드 |
|---|---|---|
| `preview` | `order_preview` 가 주문을 만들었을 때 | `tool`, `params`, `errors`, `warnings`(개수), `token_issued` |
| `rejected` | 서버가 거부해 보내지 않았을 때 | `via`(부른 도구), `tool`, `params`, `reasons`, `token_given` |
| `sent` | 키움에 보냈을 때 | `via`, `tool`, `params`, `result`(`return_code`·`return_msg`·`ord_no`) |
| `failed` | 보냈는데 호출이 예외로 끝났을 때 | `via`, `tool`, `params`, `error` |

앱키·시크릿·접근 토큰·`confirm_token` 은 쓰지 않고, 계좌번호 필드는 끝 4자리만 남깁니다. 파일은 `0600`, 디렉터리는 `0700` 으로 만듭니다. 로그를 쓰지 못해도 주문은 막거나 바꾸지 않고 서버 로그에 경고만 남깁니다.

## 도구

| 종류 | 이름 | 비고 |
|---|---|---|
| 의도 도구 | `stock_search` | 종목명·코드로 종목 찾기(ka10099, 캐시) |
| | `stock_snapshot` | 현재가·등락률·시총·PER/PBR 등 한 번에(ka10001). 종목명으로도 받음 |
| | `account_summary` | 계좌 총평가·손익·보유 종목(kt00018) |
| | `get_chart` | 일·주·월·분봉 OHLCV(날짜 오름차순) + 기간 수익률·고저·평균 거래량·5/20 이동평균. 연속조회로 `count` 개까지(ka10081/82/83/80) |
| | `get_quotes` | 여러 종목(최대 20) 현재가·등락률·거래량·거래대금·시총을 요청 한 번에(ka10095). 못 찾은 종목만 error |
| | `market_movers` | 오늘 상위 종목: `kind` = volume 거래량·gainers 상승률·losers 하락률·value 거래대금·volume_spike 거래량 급증, `market` = all·kospi·kosdaq (ka10030/10027/10032/10023) |
| | `investor_flow` | 일별 투자자별 순매수(개인·외국인·기관계·연기금 등)와 기간 합계·순매수일 수. 금액(백만원) 또는 수량(ka10059) |
| | `get_orders` | 미체결(open)·체결(filled) 주문 목록. 오늘은 ka10075/ka10076, 다른 날은 kt00007. 미체결 행에 `order_preview` 취소 인자(`cancel_preview_args`) |
| | `get_buying_power` | 종목·단가로 살 수 있는 수량·금액(증거금률별, 현금만, kt00011). 종목을 빼면 예수금·D+2·주문가능·출금가능금액(kt00001) |
| | `get_portfolio` | 보유 종목별 수량·평균단가·평가금액·손익·수익률·비중(총자산·주식 대비)과 현금(D+2)·주문가능금액·총자산. 계좌번호 마스킹(kt00018+kt00001+ka00001) |
| | `rebalance_plan` | 목표 비중(`{"삼성전자": 0.5}`)까지 사고팔 정수 수량·호가단위 단가를 현재 잔고·현재가로 계산. 매도 먼저, 현금 안에서만 매수. **주문 안 함** — 행마다 `order_preview_args` |
| | `watch` | 실시간 체결(0B)을 최대 60초 모아 종목별 마지막가·고저·매수/매도 체결량·틱 수. `until`(예: `{"stock": "005930", "above": 72000}`)에 걸리면 즉시 반환. WebSocket |
| | `condition_search_run` | 영웅문4에 저장한 조건식을 이름(일부)·번호로 한 번 실행해 걸린 종목의 코드·이름·현재가·등락률·거래량(CNSRLST→CNSRREQ, WebSocket) |
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
| 기본 `smart` | 17 | 약 12.8 K |
| `--discovery` | 3 | 약 1.4 K |
| `--full` | 188 | 약 228 K |
| `--full --toolsets market,chart,account` | 86 | 약 102 K |

(TR 도구마다 입력 스키마에 요청 필드 ID·한글명이 들어 있어 큽니다. 모의투자는 주문 도구가 더해집니다. smart 의 도구 수는 편의 도구가 늘면 같이 늘어납니다. 표의 숫자는 테스트가 실제 목록과 대조합니다. 지금 내 설정의 값은 `kiwoom-client-mcp doctor` 로 봅니다.)

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
