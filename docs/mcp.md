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
| `--discovery` | 메타 도구 3개만 노출(아래 "컨텍스트 줄이기") |
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
| `KIWOOM_MCP_MODE` | `--discovery` | `discovery` 면 메타 도구 3개만 | 전부 노출 |
| `KIWOOM_MCP_MAX_ROWS` | `--max-rows` | 리스트 응답 기본 행 수 제한 | 제한 없음 |
| `KIWOOM_MCP_ALLOW_LIVE_ORDERS` | (없음) | 실전 계좌에서 주문 도구 노출 | `false` |

CLI 옵션이 환경변수보다 우선합니다. 실주문 opt-in 에는 일부러 CLI 옵션을 두지 않았습니다.

toolset 이름은 엔드포인트 모듈 이름과 같습니다: `account`, `stock_info`, `market`, `chart`, `order`, `credit_order`, `ranking`, `sector`, `foreign_institution`, `short_selling`, `slb`, `theme`, `condition_search`, `elw`, `etf`.

## 실주문 가드

- `KIWOOM_IS_MOCK=false`(실전)이고 `KIWOOM_MCP_ALLOW_LIVE_ORDERS=true` 가 아니면 주문 도구(`order_*` 8개, `credit_order_*` 4개)를 서버가 **등록하지 않습니다**. 도구 목록, `call_tool`, `search_tools`, `kiwoom://tools` 어디에도 나오지 않습니다.
- toolset 필터·discovery 모드·편의 도구는 모두 가드가 남긴 도구만 봅니다. `--toolsets order` 로 골라도 opt-in 없이는 주문 도구가 생기지 않습니다. 이 동작은 회귀 테스트(`tests/test_mcp_live_order_regression.py`)로 고정돼 있습니다.
- 모의투자(`KIWOOM_IS_MOCK=true`)는 실제 체결이 없으므로 가드 없이 주문 도구가 보입니다.
- 가드는 MCP 서버 경로에만 있습니다. 파이썬에서 `KiwoomAPI`/`AsyncKiwoomAPI` 를 직접 쓰면 막지 않습니다.

주문 도구에는 `destructiveHint=true` annotation 이 붙습니다. 그래서 클라이언트는 실행 전에 확인을 받을 수 있습니다. 조회 도구는 `readOnlyHint=true` 입니다.

### 주문 미리보기 `order_preview`

주문을 보내지 않고(네트워크 호출 없음) 다음을 돌려줍니다.

- 호가단위 보정: 매수는 내림, 매도는 올림
- 필드 검증
- 예상 금액
- 경고
- 주문 도구에 그대로 넘길 `params`

`order_tools_enabled` 값으로 이 서버에 주문 도구가 있는지도 알려 줍니다. 에이전트는 미리보기를 사용자에게 보여 주고 확인을 받은 뒤에만 주문해야 합니다. 서버의 `instructions` 와 `order_checklist` 프롬프트가 이 순서를 안내합니다.

## 도구

| 종류 | 이름 | 비고 |
|---|---|---|
| 편의 도구 | `stock_search` | 종목명·코드로 종목 찾기(ka10099, 캐시) |
| | `stock_snapshot` | 현재가·등락률·시총·PER/PBR 등 한 번에(ka10001) |
| | `account_summary` | 계좌 총평가·손익·보유 종목(kt00018) |
| | `order_preview` | 주문 미리보기, 전송 안 함 |
| TR 도구 | `<모듈>_<메서드>` | 예: `stock_info_basic_stock_info`, `chart_stock_daily_chart`. [전체 목록](endpoints.md) |
| 조건검색 | `condition_search_*` 4개 | WebSocket. 실시간 등록은 첫 응답만 돌려줌 |

TR 도구는 `params` 에 키움 요청 필드를 문자열로 넣습니다. 각 도구의 입력 스키마에 TR 카탈로그의 필드 이름·필수 여부·설명이 들어 있습니다.

```json
{"params": {"stk_cd": "005930"}}
```

연속조회는 응답의 `cont-yn`/`next-key` 를 다음 호출의 `cont_yn="Y"`, `next_key` 로 넘깁니다.

## 컨텍스트 줄이기

도구 정의는 에이전트 컨텍스트에 통째로 올라갑니다. 설정별 `tools/list` 크기는 다음과 같습니다.

| 설정 | 도구 수 | `tools/list` 크기 (글자 수) |
|---|---|---|
| 전부 (실전, 가드) | 178 | 약 230 K |
| `--toolsets market,chart,account` | 80 | 약 100 K |
| `--discovery` | 3 | 약 1.5 K |

(0.4.x 기준. TR 도구의 입력 스키마에 필드 설명이 들어 있어 큽니다.)

- **toolset**: 쓰는 모듈만 켭니다.
- **discovery 모드**: `search_tools`(키워드·toolset 검색) → `describe_tool`(입력 스키마) → `call_tool`(실행) 세 도구로 전체 TR 을 씁니다.
- **`max_rows`**: 조회 도구 호출마다 `max_rows` 를 주면 응답의 각 리스트를 앞에서 N행만 남깁니다. 서버 기본값은 `--max-rows` 로 정합니다. 잘린 응답에는 `"_truncated": {"<키>": {"total": 300, "returned": 20}}` 가 붙습니다.

## resources 와 prompts

| URI | 내용 |
|---|---|
| `kiwoom://guide` | 에이전트용 사용 규칙 |
| `kiwoom://tools` | 지금 노출된 도구 목록(이름·toolset·조회 여부·api_id) |
| `kiwoom://codes/trade-types` | 매매구분 `trde_tp`·거래소구분 `dmst_stex_tp` |
| `kiwoom://codes/markets` | 시장구분 `mrkt_tp` (ka10099) |
| `kiwoom://tr/{api_id}` | TR 하나의 요청·응답 필드(예: `kiwoom://tr/ka10001`) |

프롬프트는 세 가지입니다.

- `analyze_stock(stock)`: 종목 분석, 조회만
- `review_account()`: 계좌 점검, 조회만
- `order_checklist(request)`: 미리보기를 만들고 사용자 확인 전에는 주문하지 않는 절차

## 문제 해결

| 증상 | 원인·해결 |
|---|---|
| `KIWOOM_APP_KEY and KIWOOM_APP_SECRET ... must be set` | 클라이언트 설정의 `env` 에 키를 넣었는지 확인 |
| `MCP 서버에는 mcp 패키지가 필요합니다` | `[mcp]` extra 없이 설치됨. `pip install 'kiwoom-client[mcp]'` 또는 `uvx --from 'kiwoom-client[mcp]' ...` |
| `ImportError: ServerRequestContext` | 오래된 `mcp` 1.x 가 깔려 있음. `pip install -U 'mcp>=2.0,<3'` |
| `KIWOOM_IS_MOCK=... 를 해석할 수 없습니다` | true/false (또는 1/0, yes/no) 로 지정 |
| 8030/8031 오류 | 모의/실전 키와 `KIWOOM_IS_MOCK` 이 서로 맞지 않음 |
| 주문 도구가 안 보임 | 의도된 동작(실전 + opt-in 없음). 모의투자로 시험하거나 위 "실주문 가드" 참고 |
