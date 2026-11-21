# 기여 가이드 (Contributing)

kiwoom-client 에 관심 가져 주셔서 감사합니다. 이 라이브러리는 **실제 증권 계좌에 주문을 넣을 수 있고**,
여러 실매매 프로그램이 `kiwoom-client>=...` 로 새 릴리스를 그대로 받아 씁니다. 그래서 아래 규칙이
일반적인 오픈소스보다 조금 엄격합니다.

> English: issues and PRs in English are welcome. The rules below boil down to: never hit the live
> Kiwoom server or use real keys while developing, test HTTP with `pytest-httpx` mocks only, and
> keep existing public behaviour unchanged (add, don't change).

## 개발 환경

Python **3.10 이상**, [uv](https://docs.astral.sh/uv/) 를 권장합니다.

```bash
git clone https://github.com/younghwan91/kiwoom-client.git
cd kiwoom-client
uv run --extra dev --extra mcp pytest tests/ -q     # 첫 실행 때 .venv 를 만들고 의존성을 설치합니다
```

uv 없이 pip 로:

```bash
python -m venv .venv && . .venv/bin/activate
pip install -e ".[dev,mcp]"
pytest tests/ -q
```

`uv.lock` 은 커밋하지 않습니다(.gitignore). 라이브러리라 소비자가 각자 해상도를 정합니다.

## PR 전에 돌릴 것 (CI 와 같은 명령)

```bash
uv run --extra dev --extra mcp pytest tests/ -q                  # 단위 테스트, 수 초
uv run --extra dev --extra mcp ruff check src tests examples      # 린트
uv run --extra dev --extra mcp mypy                               # 타입 (src/kiwoom_client)
bash scripts/check_dist.sh                                        # (패키징을 건드렸다면) wheel 빌드·설치 스모크
```

- CI 는 `ruff` 최신판을 설치합니다. 로컬 ruff 가 오래됐으면 CI 에서 새 규칙이 먼저 걸릴 수 있습니다.
- `ruff format` 으로 **레포 전체를 재포매팅하지 마세요** — 고친 줄만 다듬어 주세요(리뷰·충돌이 커집니다).
- 커버리지는 `--cov` 를 붙이면 봅니다: `uv run --extra dev --extra mcp pytest tests/ -q --cov`

### pre-commit (선택)

커밋할 때 바뀐 파일에만 ruff 린트와 기본 검사(YAML/TOML/JSON 문법, 끝 공백, 개인키, 큰 파일,
`.env`·`uv.lock`·`.coverage` 커밋 금지)를 돌리고 싶다면:

```bash
uvx pre-commit install                    # 한 번만
uvx pre-commit run --files <바꾼 파일...>  # 수동 실행
```

CI 는 pre-commit 을 강제하지 않습니다. `pre-commit run --all-files` 는 레포 전체를 고칠 수 있으니
그 결과를 PR 에 섞지 마세요.

### 생성 파일

아래 파일은 코드에서 생성하고, 테스트가 커밋된 내용과 같은지 확인합니다. 엔드포인트를 더하거나
독스트링·이름을 바꿨다면 다시 생성해 **같이 커밋**하세요.

```bash
uv run python scripts/gen_docs.py        # docs/endpoints.md·reference/, llms*.txt, AGENTS.md, skills/, Cursor·Copilot 규칙
uv run python scripts/build_stubs.py     # src/kiwoom_client/domestic/*.pyi
```

## 안전 규칙 (꼭 지켜 주세요)

1. **실서버·실키로 개발하지 않습니다.** `KiwoomAPI(...)` 의 기본값은 `is_mock=False` = 실전투자 서버이고,
   `api.order.*`·`api.credit_order.*` 는 그대로 실주문을 냅니다. 파이썬 직접 호출에는 가드가 없습니다.
2. **테스트의 HTTP 는 전부 [pytest-httpx](https://colin-b.github.io/pytest_httpx/) 목**으로 씁니다.
   키움 서버(`api.kiwoom.com`, `mockapi.kiwoom.com`)에 실제 요청을 보내는 단위 테스트는 받지 않습니다.
   기존 테스트(`tests/test_modules.py` 등)를 본보기로 삼아 주세요.
3. `tests/integration_*_smoke.py` 는 **실서버 스크립트**라 pytest 가 모으지 않습니다(`test_` 접두 없음).
   메인테이너가 직접 돌립니다 — PR 에서 결과를 요구하지 않습니다.
4. `examples/*.py` 는 전부 `is_mock=True` 입니다(`tests/test_examples.py` 가 검사). 예제를 실키로 돌리거나
   `is_mock` 을 바꿔 돌리지 마세요. 예제 끝의 `api.logout()` 은 토큰을 폐기해, 같은 앱키를 쓰는 다른
   프로그램의 세션을 끊을 수 있습니다.
5. MCP 서버의 실주문 opt-in 가드(`KIWOOM_MCP_ALLOW_LIVE_ORDERS`, `src/kiwoom_client/mcp/guard.py`)를
   **약하게 하는 변경은 받지 않습니다.** 주문 경로에는 가드를 더하는 쪽이 기본입니다.
6. 커밋·이슈·PR·테스트 데이터에 **앱키·시크릿·토큰·계좌번호를 넣지 마세요.** 응답 예시는 `XXXX` 로 가립니다.

## 호환성 규칙 (추가는 쉽게, 변경은 어렵게)

소비자가 `>=` 로 새 릴리스를 받으므로, 아래는 **바꾸지 않습니다** — 필요하면 새 함수·새 옵션(기본값은
기존 동작)으로 더합니다.

- `request()`/`request_all()` 의 동작, 토큰 발급·자동 갱신, rate limiter
- `tick_size`/`round_to_tick` 등 기존 함수의 결과
- `is_mock=False` 기본값, 기존 메서드의 시그니처·반환값

## PR 절차

1. 이슈가 있으면 먼저 연결합니다(버그·기능 제안·엔드포인트 요청 템플릿이 있습니다).
2. `main` 에서 브랜치를 만듭니다 — 이름은 `feat/…`, `fix/…`, `docs/…`, `chore/…`, `ci/…` 처럼.
3. 커밋 메시지는 [Conventional Commits](https://www.conventionalcommits.org/ko/) 형식
   (`feat(order): …`, `fix(auth): …`). 한국어·영어 모두 좋습니다.
4. 새 동작에는 단위 테스트를 붙이고, 위 명령이 모두 통과하는지 확인합니다.
5. PR 템플릿의 체크리스트를 채웁니다. 작고 한 가지 일만 하는 PR 이 빨리 머지됩니다.
6. `CHANGELOG.md`([Keep a Changelog](https://keepachangelog.com/ko/1.1.0/))는 메인테이너가 릴리스 때 정리합니다.
   PR 본문에 "CHANGELOG 한 줄" 후보를 적어 주시면 고맙습니다. 버전(`pyproject.toml`)은 바꾸지 마세요.

## 이슈 · 보안

- 버그·기능·엔드포인트 요청: [Issues](https://github.com/younghwan91/kiwoom-client/issues/new/choose)
- 사용법 질문·아이디어: [Discussions](https://github.com/younghwan91/kiwoom-client/discussions)
- 보안 문제(실주문 가드 우회, 키 유출 등)는 공개 이슈 대신 [SECURITY.md](SECURITY.md) 의 비공개 경로로.
- 행동 강령: [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md)
