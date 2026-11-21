# Contributing

kiwoom-client에 기여해주셔서 감사합니다!

## 개발 환경 설정

```bash
git clone https://github.com/younghwan91/kiwoom-client.git
cd kiwoom-client
pip install -e ".[dev]"
# 또는
uv pip install -e ".[dev]"
```

Python **3.10 이상**이 필요합니다.

## 테스트 실행

```bash
pytest tests/ -v
```

## 문서 사이트

`docs/` 의 마크다운은 MkDocs Material 사이트로도 빌드됩니다. 새 페이지는 `docs/` 에 `.md` 를 넣기만 하면
내비게이션에 자동으로 들어갑니다(`docs/.nav.yml` 의 `"*"`). 영어판은 같은 이름에 `.en.md` 를 붙입니다.

```bash
uv run --extra docs mkdocs serve           # 미리보기 http://127.0.0.1:8000
uv run --extra docs mkdocs build --strict  # CI 와 같은 검사 — 경고가 하나라도 있으면 실패
```

`docs/` 밖의 파일(`README.md`, `src/...`)은 상대 경로 대신 `https://github.com/younghwan91/kiwoom-client/blob/main/...`
절대 URL 로 링크하세요. 상대 경로는 사이트에서 깨진 링크가 되어 `--strict` 가 실패합니다.

## PR 가이드라인

1. `main` 브랜치에서 새 브랜치를 생성합니다.
2. 변경 사항을 커밋합니다.
3. 모든 테스트가 통과하는지 확인합니다: `pytest tests/ -v`
4. PR을 생성합니다.

## 버그 리포트 & 기능 요청

[GitHub Issues](https://github.com/younghwan91/kiwoom-client/issues)에서 이슈를 생성해주세요.
