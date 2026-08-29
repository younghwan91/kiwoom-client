# 자주 묻는 질문 (FAQ)

[← README](../README.md)

### 키움 앱키(appkey)와 시크릿키는 어떻게 발급받나요?

[키움 REST API 포털](https://openapi.kiwoom.com)에 로그인한 뒤 **API 사용신청** 메뉴에서
신청하면 `appkey` 와 `secretkey` 가 발급됩니다. 발급받은 키는 `.env` 에 보관하고 코드에
직접 하드코딩하지 마세요 ([`.env.example`](../.env.example) 참고).

### 모의투자에서 실전투자로 어떻게 전환하나요?

`is_mock` 값만 바꾸면 됩니다. 서버 URL 은 라이브러리가 자동으로 전환합니다.

```python
api = KiwoomAPI(app_key="...", app_secret="...", is_mock=False)  # 실전투자
```

### 접근토큰(access token)이 만료되면 어떻게 하나요?

할 일이 없습니다. 토큰은 첫 호출에서 발급되고, 만료 60초 전에 선제 재발급되며, 그래도 인증
실패가 오면 재발급 후 한 번 더 시도합니다. 키움은 만료 토큰에 HTTP 401 이 아니라
`200 + return_code 3` 을 돌려주는데, 양쪽 다 인식합니다 (실서버 확인 완료).
갱신 시점은 `KiwoomAPI(..., expiry_margin=300)` 으로 조절합니다.

여러 프로세스가 토큰을 공유해야 한다면 `TokenProvider` 프로토콜
(`get_valid_token()` / `refresh_token()`)을 구현해 넘기면 Redis 등 외부 캐시를 쓸 수 있습니다.

### Rate limit 에러가 나면 어떻게 하나요?

내장 TR별 토큰 버킷이 호출 빈도를 자동 조절하고 `429` 발생 시 재시도까지 처리합니다
(실측 기준 TR당 1 req/s, 버스트 2). 그래도 걸린다면 여러 프로세스·스레드에서 **같은 TR 을
동시 호출** 중인지 확인하고, 연속조회는 `request_all()` 로 한 번에 처리하세요.
자세한 내용은 [요청 제한](guide.md#요청-제한-rate-limit).

### 조건검색(실시간)은 어떻게 사용하나요?

`api.condition_search` 가 요청 페이로드를 만들고, 전송·수신은 WebSocket 으로 합니다.
[지원 API 전체 목록](api-reference.md#조건검색-apicondition_search---4개-websocket) 참고.

### Windows 가 아닌 macOS/Linux 에서도 되나요?

네. REST/WebSocket 기반이라 OCX·COM 이 필요 없어 macOS·Linux·서버(헤드리스) 환경에서
모두 동작합니다.

### pandas DataFrame 으로 바로 받을 수 있나요?

`to_dataframe(result)` 한 줄이면 됩니다. 엔드포인트마다 다른 페이로드 키를 자동으로 찾고,
`"+70000"` 같은 문자열도 숫자로 바꿔줍니다.
[응답 변환](guide.md#응답을-숫자dataframe-으로)과
[`examples/pandas_usage.py`](../examples/pandas_usage.py) 참고.

### asyncio 를 지원하나요?

네. `AsyncKiwoomAPI` 가 `KiwoomAPI` 와 같은 엔드포인트를 제공합니다.
[asyncio](guide.md#asyncio) 참고.
