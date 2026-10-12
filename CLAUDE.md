# kiwoom-client

키움증권 REST/WebSocket API 파이썬 래퍼(공개 PyPI 패키지). 사용법·엔드포인트·MCP 서버는 `README.md`, 변경 이력은 `CHANGELOG.md`.

## 실계좌 위험

- 이 PC 에 있는 키움 키는 `~/git/quant-airflow/.env` 의 **실전투자용** 키뿐이다(이 레포엔 `.env.example` 만 있다).
  같은 앱키로 scalp-it·daytrade-it 데몬과 Airflow 수집이 돈다. 모의투자 서버(`mockapi`)는 이 키로 인증이 안 된다(8030, 2026-08 확인).
- `KiwoomAPI(...)`/`AsyncKiwoomAPI(...)` 의 기본값은 `is_mock=False` = **실서버**다. 키를 불러 `api.order.*`·
  `api.credit_order.*`(kt10000~kt10009)를 부르면 그대로 실주문이 나간다. 라이브러리 쪽 가드
  (`KIWOOM_MCP_ALLOW_LIVE_ORDERS`)는 **MCP 서버 경로에만** 있고 파이썬 직접 호출은 막지 않는다.
- `api.logout()`/`revoke_token` 은 공유 앱키의 토큰을 폐기해 돌고 있는 데몬을 죽일 수 있다. `examples/*.py` 는 전부
  `is_mock=True` 에 끝에 `api.logout()` 을 부른다 — 실키로 예제를 돌리지 않고, `is_mock` 을 바꿔 돌리지도 않는다.
- 결정론 장치: `.claude/hooks/live_order_guard.py`(PreToolUse) 가 키를 불러오면서 주문·토큰 폐기를 실행하는 Bash 명령과
  `KIWOOM_MCP_ALLOW_LIVE_ORDERS=true` 를 막는다. 막히면 우회하지 말고 명령을 사용자에게 보여 `! <명령>` 으로 직접 돌리게 한다.
- 실서버 조회 스모크(`tests/integration_api_smoke.py --prod` — 키는 환경변수나 레포 루트 `.env` 에서만 읽고 `--env-file` 이 없다,
  `tests/integration_ws_smoke.py --prod --env-file ~/git/quant-airflow/.env`)는
  주문을 빼고 조회만 하지만 실키로 토큰을 받는다 — 사용자가 시킬 때만, 장중 데몬이 도는 시간엔 특히 조심한다.
- 실주문 경로에 가드를 더하는 쪽이 기본이다. 사용자는 "가드 없이 전부 노출" 지시 뒤에도 MCP opt-in 가드(5807b03)가 맞았다고 확인했다.
  가드를 없애거나 약하게 하는 변경은 하지 않는다.

## 명령

```bash
uv run --extra dev --extra mcp pytest tests/ -q        # 단위 테스트 ~200개, 수 초. HTTP 는 전부 pytest-httpx 목
uv run --extra dev --extra mcp ruff check src tests examples
uv run --extra dev --extra mcp mypy                      # files = src/kiwoom_client
```

`uv.lock` 은 커밋하지 않는다(.gitignore). CI 는 `ruff>=0.6` 최신판을 깔아서 로컬보다 새 규칙이 먼저 걸린 적이 있다(b17d3c7, RUF022).
`tests/integration_*_smoke.py` 는 `test_` 접두가 없어 pytest 가 모으지 않는다 — 실서버 스크립트라 일부러 그렇다.

## 소비자와 릴리스

- 소비자: krx-quant-core(`kiwoom-client>=0.4.0`, **호가단위 표 `tick_size` 의 정본이 여기**), scalp-it, daytrade-it,
  quant-airflow Docker 이미지. 전부 하한만 걸어(`>=`) 다음 `uv lock`·이미지 재빌드 때 새 릴리스를 그대로 받는다 —
  `tick_size`·`request()`·토큰 갱신 동작을 바꾸면 코어 골든 테스트와 실매매 데몬이 같이 바뀐다.
- 버전은 `pyproject.toml` 한 곳(`__version__` 은 설치 메타데이터에서 읽는다) + `CHANGELOG.md`(Keep a Changelog) — 예: c1a53cd.
  태그 `v*` 푸시 → `publish.yml` 이 PyPI 에 올린다. 되돌릴 수 없으니 사용자가 배포를 지시했을 때만.
- 공개 레포·공개 패키지다. 커밋·CHANGELOG·README 에 계좌번호·키·사내 정보를 넣지 않는다.

## 아직 미확정 (README 에 명시돼 있음)

- WebSocket REAL 프레임 항목 필드명(`item`/`values`) — 장중 실서버로만 판정된다(README "검증 상태").

## 문서

- `docs/superpowers/specs/2026-09-07-mcp-server-design.md` — MCP 서버·실주문 가드 설계. `mcp/` 를 바꿀 때 먼저 읽는다.
