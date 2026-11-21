# 보안 정책 (Security Policy)

kiwoom-client 는 실제 증권 계좌에 주문을 넣을 수 있는 라이브러리입니다. 보안 문제는 공개 이슈가 아니라
아래의 **비공개 경로**로 알려 주세요.

## 지원 버전

| 버전 | 보안 수정 |
| --- | --- |
| 최신 릴리스 (`0.x` 의 가장 높은 minor) | 지원 |
| 그 이전 | 지원하지 않음 — 최신 버전으로 올려 주세요 |

## 제보 방법

1. 저장소의 **Security** 탭 → **Report a vulnerability** 로 비공개 제보를 남겨 주세요
   ([GitHub 문서: Privately reporting a security vulnerability](https://docs.github.com/en/code-security/security-advisories/guidance-on-reporting-and-writing-information-about-vulnerabilities/privately-reporting-a-security-vulnerability)).
2. 이 버튼이 보이지 않으면, 세부 내용 **없이** "보안 제보 연락 요청" 이라는 제목으로 이슈를 열어 주세요.
   메인테이너가 비공개 채널을 열어 드립니다.

제보에 담아 주시면 좋은 것:

- 영향받는 버전과 모듈(예: `mcp/guard.py`, `auth.py`)
- 재현 방법 — **모의투자 서버(`is_mock=True`) 또는 목(mock) 으로 재현**한 코드
- 예상 영향(예: 실주문이 의도치 않게 나감, 토큰이 로그에 남음)

**제보에도 앱키·시크릿·접근 토큰·계좌번호를 넣지 마세요.** 필요하면 `XXXX` 로 가려 주세요.

## 범위

이 저장소의 코드가 대상입니다. 특히 다음은 보안 문제로 다룹니다.

- MCP 서버의 실주문 opt-in 가드(`KIWOOM_MCP_ALLOW_LIVE_ORDERS`)를 우회해 실전 계좌에 주문 도구가 노출되는 경우
- 앱키·시크릿·토큰이 로그·예외 메시지·MCP 응답으로 새는 경우
- 사용자가 의도하지 않은 주문·정정·취소 요청이 나가는 경우
- 배포 패키지(PyPI)·CI 공급망 문제

범위 밖:

- 키움증권 서버·OpenAPI 자체의 취약점 → 키움증권에 직접 알려 주세요.
- 사용자가 직접 `is_mock=False` 로 주문 메서드를 호출한 결과(라이브러리의 문서화된 동작입니다).

## 처리 과정

- 접수 확인: 가능한 한 빨리(목표 7일 이내)
- 수정이 필요하면 비공개 advisory 에서 함께 고친 뒤 패치 릴리스와 함께 공개합니다.
- 원하시면 advisory 에 제보자로 기록합니다.

## 사용자에게: 키가 노출됐다면

이슈·로그·스크린샷 등에 앱키나 시크릿이 올라갔다면 즉시 키움 OpenAPI 포털에서 **앱키를 재발급**하세요.
글을 지우는 것만으로는 부족합니다(포크·캐시·알림 메일에 남습니다).
