# 쿡북

자주 하는 일을 바로 돌려 볼 수 있는 코드로 모았습니다. 모든 예제는 **모의투자**(`is_mock=True`)이고, 키는 환경변수
`KIWOOM_APP_KEY` · `KIWOOM_APP_SECRET` 에서 읽습니다(`KiwoomAPI.from_env`).

```bash
pip install 'kiwoom-client[pandas]'
export KIWOOM_APP_KEY=...  KIWOOM_APP_SECRET=...   # 모의투자용 키
```

| 레시피 | 쓰는 것 |
|---|---|
| [일봉을 받아 DataFrame 으로](daily-chart.md) | `ka10081`, `to_dataframe()` |
| [연속조회를 끝까지](pagination.md) | `cont_yn`·`next_key`, `request_all()` |
| [잔고·평가 요약](account-summary.md) | `kt00018`, `kt00001` |
| [asyncio 로 동시에 조회하기](async-concurrency.md) | `AsyncKiwoomAPI`, `asyncio.gather` |
| [호가단위에 맞춘 지정가 주문 (모의투자)](limit-order.md) | `round_to_tick()`·`add_ticks()`, `kt10000`~`kt10003` |
| [WebSocket 으로 실시간 체결·호가](realtime-trades.md) | `0B`·`0D`, `ws.on()`·`ws.subscribe()` |
| [조건검색 결과를 실시간으로](condition-search-realtime.md) | `CNSRLST`·`CNSRREQ`·`CNSRCLR` |
| [호출 제한(429) 다루기](rate-limits.md) | `rate_limit`·`max_retries`, `KiwoomRateLimitError` |

필요한 TR 을 찾을 때는 [엔드포인트 전체 목록](../endpoints.md), 필드는 [필드 레퍼런스](../reference/index.md)를 보세요.
요청 필드 이름을 잘못 넣는 실수는 `KiwoomAPI.from_env(is_mock=True, validate_params="warn")` 로 보내기 전에 잡을 수 있습니다.

> 이 페이지들의 REST 예제는 테스트가 키움 공식 스펙으로 만든 가짜 응답에 대고 **실제로 실행**해 봅니다
> (`tests/test_cookbook_exec.py`). WebSocket 예제는 문법·이름만 검사합니다.
