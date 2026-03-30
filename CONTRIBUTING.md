# Contributing

kiwoom-rest-api에 기여해주셔서 감사합니다!

## 개발 환경 설정

```bash
git clone https://github.com/younghwan91/kiwoom-rest-api.git
cd kiwoom-rest-api
pip install -e ".[dev]"
# 또는
uv pip install -e ".[dev]"
```

Python **3.10 이상**이 필요합니다.

## 테스트 실행

```bash
pytest tests/ -v
```

## PR 가이드라인

1. `main` 브랜치에서 새 브랜치를 생성합니다.
2. 변경 사항을 커밋합니다.
3. 모든 테스트가 통과하는지 확인합니다: `pytest tests/ -v`
4. PR을 생성합니다.

## 버그 리포트 & 기능 요청

[GitHub Issues](https://github.com/younghwan91/kiwoom-rest-api/issues)에서 이슈를 생성해주세요.
