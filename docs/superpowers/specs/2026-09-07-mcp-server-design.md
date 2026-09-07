# MCP 서버 — 설계 스펙

## 배경 및 목적

`kiwoom-client`는 기능적으로 밀리지 않는데도(REST 182개 엔드포인트 + WebSocket + sync/async) GitHub star가 1개뿐이다. 경쟁 비공식 래퍼 `tossinvest-cli`(star 493개)는 CLI+MCP 서버 형태로 `mcp`/`ai-agents`/`model-context-protocol` topic을 달아, Claude Code/Cursor 등 AI 코딩 도구용 검색 트래픽을 흡수하고 있다. 같은 효과를 노리고 이 레포 자체에 MCP 서버를 얹는다.

## 스코프

- 15개 도메인 모듈(account, stock_info, market, chart, ranking, order, credit_order, sector, foreign_institution, slb, condition_search, theme, short_selling, elw, etf) 전체를 MCP 도구로 노출한다.
- 주문(매수/매도/정정/취소)·신용주문·금현물 주문을 포함한 REST 엔드포인트 전체와, WebSocket 기반인 condition_search 4종을 포함한다.
- 주문 도구(매수/매도/정정/취소·신용주문·금현물)에는 **환경변수 opt-in 가드**를 둔다(아래 "안전장치" 절 참고) — 최초 요청 시 "가드 없음"으로 정했으나, 이후 사용자가 가드 추가를 요청해 반영했다.
- 실시간 시세 구독(REG/REAL, `create_websocket()`을 통한 지속 스트림)은 이번 스코프에서 제외한다 — MCP 도구는 요청-응답 모델이라 지속 푸시와 맞지 않고, 별도 설계가 필요하다.

## 접근 방식

### 도구 생성: 리플렉션 기반 자동 생성 (하드코딩 없음)

15개 모듈의 모든 public 메서드가 동일한 시그니처 패턴을 따른다:

```python
def method_name(self, cont_yn: str = "N", next_key: str = "", **kwargs: Any) -> ResponseT:
    """설명 (Description)"""
    return self._client.request(self.RESOURCE_URL, "<api_id>", kwargs, cont_yn, next_key)
```

즉 실질 요청 필드는 전부 `**kwargs`로 그대로 REST 바디에 실린다. 서버 기동 시 `ModuleRegistry.MODULE_NAMES`를 순회하며 `inspect.signature`로 각 모듈의 public 메서드를 스캔해 MCP 도구를 **동적으로 생성**한다. TR별 필드를 손으로 나열하지 않으므로 키움 스펙이 바뀌거나 라이브러리에 엔드포인트가 추가돼도 서버 코드 변경 없이 자동 반영된다.

- 도구 이름: `{module}_{method}` (예: `order_buy_order`, `stock_info_basic_stock_info`). 총 182개 생성 예상(신규 엔드포인트 추가 시 자동으로 늘어남 — 정확한 개수를 코드에 고정하지 않는다).
- 도구 설명: 메서드 docstring 그대로 사용.
- 입력 스키마: REST 15개 모듈은 전부 `{"cont_yn": str = "N", "next_key": str = "", "params": object}` — `params`가 `**kwargs`로 그대로 펼쳐져 요청 바디가 된다. 주문 계열 도구는 description에 opt-in 가드 필요 여부와 실계좌 경고 문구를 추가한다.
- 반환값: 키움 API가 준 dict를 JSON 텍스트로 그대로 반환한다(가공·필터링 없음).

### 안전장치: 실주문 opt-in 가드

이 가드는 **MCP 서버 경로에만** 적용된다 — 기존 `KiwoomAPI`/`AsyncKiwoomAPI`를 파이썬 코드에서 직접 쓰는 경로(`api.order.buy_order(...)` 등)는 이번 변경으로 전혀 건드리지 않으며 지금과 동일하게 동작한다.

- 대상 도구: `order.py`의 8개(`buy_order`, `sell_order`, `modify_order`, `cancel_order`, `gold_spot_*` 4종)와 `credit_order.py`의 신용주문 계열 전부.
- 환경변수 `KIWOOM_MCP_ALLOW_LIVE_ORDERS`(`"true"`/`"false"`, 기본 `false`)로 제어한다.
- `is_mock=True`(모의투자)인 경우 이 가드는 적용하지 않는다 — 항상 허용. 모의투자는 실제 체결이 아니므로 opt-in을 요구할 이유가 없다.
- `is_mock=False`(실전투자)이고 `KIWOOM_MCP_ALLOW_LIVE_ORDERS`가 `true`가 아니면, 위 대상 도구는 **서버 기동 시점에 등록하지 않는다**(도구 목록 자체에서 빠짐 — 호출 시점에 거부하는 방식이 아니라, LLM이 애초에 그 도구가 존재하는지 모르게 한다). 서버 시작 로그에 몇 개 도구가 이 가드로 제외됐는지 남긴다.
- 이렇게 도구 등록 단계에서 걸러내면, 사용자가 실계좌로 자동매매를 붙일 때 딱 한 번(서버 실행 시 환경변수 설정)만 의식적으로 허용하면 되고, 이후 개별 호출마다 확인할 필요는 없다.

### condition_search (WebSocket, 4개 도구)

`ConditionSearch`의 4개 메서드는 REST가 아니라 payload를 만들 뿐이며, 실제 전송은 `KiwoomWebSocket.send()`로 이뤄지고 응답은 콜백으로 비동기 도착한다. MCP 도구는 요청→(한 번의) 응답 모델이므로 다음과 같이 매핑한다:

- 서버 프로세스 전역에 `KiwoomWebSocket` 인스턴스 하나를 지연 연결(lazy connect)로 유지하고, 이후 모든 condition_search 도구 호출이 재사용한다.
- 각 도구 호출은 해당 payload를 보내고, `trnm`(과 `CNSRREQ`류는 `seq`)이 일치하는 다음 프레임을 one-shot future로 기다렸다가(타임아웃 15초) 그 프레임을 결과로 반환한다.
- `condition_search_realtime`(search_type="1")은 최초 응답 프레임 하나만 반환한다 — 이후 조건 편입/이탈에 따라 계속 도착하는 후속 REAL 프레임은 이 도구의 반환값에 포함되지 않는다(스코프 제외 사유와 동일: MCP 도구는 지속 스트림에 맞지 않음). 이 한계는 도구 description에 명시한다.
- `condition_search_cancel`은 후속 스트림 수신을 끊는 용도로, 별도 응답 프레임을 기다리지 않고 전송만 하고 반환한다(키움 프로토콜상 ack 프레임이 없음).

### 인증 및 클라이언트

- MCP 서버는 `AsyncKiwoomAPI` 하나를 프로세스 전역에서 재사용한다(토큰 자동 갱신, per-key rate limiter 그대로 활용).
- 인증 정보는 환경변수로 받는다: `KIWOOM_APP_KEY`, `KIWOOM_APP_SECRET`, `KIWOOM_IS_MOCK`(`"true"`/`"false"`, 기본 `false`) — 기존 `examples/README.md` 관례와 동일.
- 필수 환경변수 누락 시 서버는 기동 시점에 명확한 에러 메시지로 즉시 종료한다(도구 호출 시점이 아니라).

### 전송 방식

- MCP Python SDK(`mcp` 패키지)의 stdio 서버. Claude Code/Cursor 등 로컬 MCP 클라이언트의 표준 연결 방식과 일치.

### 패키지 구성

- 신규 서브패키지 `src/kiwoom_client/mcp/`:
  - `server.py` — 도구 생성·등록·stdio 진입점(`main()`).
  - `__init__.py`
- `pyproject.toml`:
  - `[project.optional-dependencies]`에 `mcp = ["mcp>=1.0"]` 추가(`pandas` extra와 같은 패턴).
  - `[project.scripts]`에 `kiwoom-client-mcp = "kiwoom_client.mcp.server:main"` 등록.
  - `keywords`에 `mcp`, `model-context-protocol`, `ai-agents`, `claude-code`, `cursor` 등 추가(경쟁 레포와 동일한 검색 트래픽 흡수 목적).
- GitHub repo topics(`mcp`, `model-context-protocol`, `ai-agents`)는 코드 변경 범위 밖 — 사용자가 직접 설정.

### 문서화

- README.md에 "MCP 서버로 사용하기" 섹션 추가: 설치(`pip install 'kiwoom-client[mcp]'`), Claude Code/Cursor MCP 설정 예시(JSON), 환경변수(`KIWOOM_MCP_ALLOW_LIVE_ORDERS` 포함), 실주문 가드 동작 방식 설명.
- README_EN.md에도 대응 섹션 추가.

## 에러 처리

- `KiwoomAPIError`(REST) 발생 시 MCP 도구는 예외를 삼키지 않고 MCP 에러 응답으로 그대로 전파한다(code, message 포함) — 클라이언트(LLM)가 실패를 인지해야 하므로 조용히 성공처럼 보이면 안 된다.
- WebSocket 타임아웃(condition_search 응답 15초 초과) 시 명확한 타임아웃 에러를 반환한다.

## 테스트

- 리플렉션 기반 도구 생성 로직: 15개 모듈이 스캔되고 각 모듈의 public 메서드 수만큼 도구가 생성되는지 유닛 테스트로 검증(정확한 182라는 숫자에 하드 의존하지 않고, "모듈별 메서드 수의 합과 일치"로 검증 — 라이브러리에 엔드포인트가 느는 걸 테스트가 막지 않도록).
- REST 도구 호출 → `AsyncKiwoomAPI`의 해당 모듈 메서드가 올바른 인자로 호출되는지 mock으로 검증(기존 `pytest-httpx` 패턴 재사용).
- condition_search 도구는 로컬 WebSocket 테스트 서버로 요청/응답 상관관계(trnm/seq 매칭)를 검증(기존 WebSocket 프로토콜 테스트 패턴 재사용).

## 스코프 밖 (명시)

- 실시간 시세 구독(REG/REAL 지속 스트림)을 MCP 도구로 노출하는 것.
- 개별 호출 단위의 확인 프롬프트(confirm 파라미터)나 금액 한도 — opt-in 환경변수 가드로 충분하다고 판단, 추가하지 않는다.
- HTTP/SSE 등 stdio 이외의 MCP 전송 방식.
