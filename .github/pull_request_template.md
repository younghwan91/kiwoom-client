## 무엇을 · 왜

<!-- 한두 문단. 관련 이슈가 있으면 `Closes #번호` -->

## 검증

- [ ] `uv run --extra dev --extra mcp pytest tests/ -q`
- [ ] `uv run --extra dev --extra mcp ruff check src tests examples`
- [ ] `uv run --extra dev --extra mcp mypy`
- [ ] 새 동작에 단위 테스트를 붙였다 (HTTP 는 pytest-httpx 목 — 실서버 호출 없음)

## 안전 · 호환성 체크

- [ ] 실서버(`api.kiwoom.com`)·실키로 돌리지 않았다. `examples/`·`tests/integration_*_smoke.py` 를 실키로 실행하지 않았다.
- [ ] 기존 공개 동작(`request()`, 토큰 갱신, rate limiter, `tick_size`, `is_mock=False` 기본값, 기존 메서드 시그니처)을 바꾸지 않았다 — 바꿨다면 이유를 위에 적었다.
- [ ] MCP 실주문 가드(`KIWOOM_MCP_ALLOW_LIVE_ORDERS`)를 약하게 하지 않았다.
- [ ] 커밋·문서·테스트에 앱키·시크릿·토큰·계좌번호가 없다.
