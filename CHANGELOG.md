# 변경 이력

이 프로젝트는 [Keep a Changelog](https://keepachangelog.com/ko/1.1.0/) 형식을 따르며,
[유의적 버전](https://semver.org/lang/ko/)을 사용합니다.

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
  실제 동작이 다르면 [이슈](https://github.com/younghwan91/kiwoom-rest-api/issues)로
  알려주세요.

## [0.1.14] - 2026-08

### 변경

- 수급 앱 코드를 [kiwoom-quant](https://github.com/younghwan91/kiwoom-quant)
  레포로 분리해 라이브러리를 가볍게 유지합니다.

## [0.1.13]

### 추가

- TR(api_id)별 Rate Limiter 와 429 자동 재시도. 실측 한도(초당 1건, 버스트 2)에
  맞춰 기본값을 잡았습니다.

### 수정

- 토큰 발급/폐기 요청의 필드명을 `appsecretkey` → `secretkey` 로 수정.

[0.2.0]: https://github.com/younghwan91/kiwoom-rest-api/releases/tag/v0.2.0
[0.1.14]: https://github.com/younghwan91/kiwoom-rest-api/releases/tag/v0.1.14
[0.1.13]: https://github.com/younghwan91/kiwoom-rest-api/releases/tag/v0.1.13
