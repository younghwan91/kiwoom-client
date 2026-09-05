# 변경 이력

이 프로젝트는 [Keep a Changelog](https://keepachangelog.com/ko/1.1.0/) 형식을 따르며,
[유의적 버전](https://semver.org/lang/ko/)을 사용합니다.

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

- 수급 앱 코드를 [kiwoom-quant](https://github.com/younghwan91/kiwoom-quant)
  레포로 분리해 라이브러리를 가볍게 유지합니다.

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
