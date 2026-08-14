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

### 수정

- `kiwoom_rest_api.__version__` 이 `"0.1.0"` 으로 고정돼 있어 실제 버전과
  달랐습니다. 이제 패키지 메타데이터에서 읽습니다.

### 개발

- CI 에 ruff·mypy 검사 추가. ruff/mypy 설정을 `pyproject.toml` 에 고정했습니다.
- 테스트 43개 → 125개.

### 알려진 이슈

- WebSocket 실시간 시세 계층은 이번 릴리스에서 손대지 않았습니다. 키움 WebSocket
  프로토콜(LOGIN 핸드셰이크, PING/PONG, `trnm: "REAL"` 메시지 구조)과 현재 구현이
  어긋나 보이는 부분이 있어, 실계좌 검증 후 별도 릴리스로 수정할 예정입니다.

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
