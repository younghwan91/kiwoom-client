---
seo_title: "키움 REST API 자료 모음 — 공식 가이드·명세·커뮤니티"
description: "키움증권 REST API 를 파이썬·AI 에이전트로 쓸 때 자주 찾는 링크 — 키움 공식 가이드·명세, MCP 자료, 공공 시장 데이터, 커뮤니티를 출처와 함께 모았습니다."
---

# 자료 모음

키움 REST API 를 파이썬·AI 에이전트로 쓸 때 자주 찾게 되는 링크입니다. 공식 자료는 키움증권 것이고, 그 밖의 것은
출처를 밝혀 둡니다. 깨진 링크나 추가할 자료는 [이슈](https://github.com/younghwan91/kiwoom-client/issues)로 알려 주세요.

## 키움증권 공식

| 자료 | 무엇을 찾나 |
|---|---|
| [키움 REST API 포털](https://openapi.kiwoom.com) | API 사용신청, 앱키·시크릿키 발급, 공지 |
| [REST API 가이드](https://openapi.kiwoom.com/guide/apiguide) | api_id(`ka10001` 등)별 요청·응답 필드 정의. 이 라이브러리의 메서드 인자 이름은 여기와 같습니다 |
| [Kiwoom-REST-API (GitHub)](https://github.com/Kiwoom-Securities/Kiwoom-REST-API) | 키움증권 공식 저장소 — API 스펙, 예제 코드, Postman 컬렉션, MCP 서버. CLI 는 PyPI `kwcli` |

- 실전투자 키와 모의투자 키는 따로 발급되고 서로의 서버에서 인증되지 않습니다(`is_mock` 과 짝을 맞추세요).
- 모의투자 서버는 KRX 만 지원합니다.

## kiwoom-client 문서

| 자료 | 무엇을 찾나 |
|---|---|
| [README](https://github.com/younghwan91/kiwoom-client#readme) | 설치, 빠른 시작, 계좌·주문, asyncio, WebSocket, 연속조회, Rate Limit, MCP 서버 |
| [엔드포인트 전체 목록](endpoints.md) | 182개 메서드의 api_id·한글 TR 이름·URL, 조건검색, 실시간 타입 |
| [왜 kiwoom-client 인가](why.md) | OpenAPI+·pykiwoom·다른 REST 래퍼와 비교 |
| [examples/](https://github.com/younghwan91/kiwoom-client/tree/main/examples) | 모의투자 서버로 돌리는 예제 스크립트 |
| [llms.txt](https://raw.githubusercontent.com/younghwan91/kiwoom-client/main/llms.txt) · [llms-full.txt](https://raw.githubusercontent.com/younghwan91/kiwoom-client/main/llms-full.txt) | AI 코딩 도구에 붙여 넣는 요약·전체 API 문서 |
| [CHANGELOG](https://github.com/younghwan91/kiwoom-client/blob/main/CHANGELOG.md) | 릴리스별 변경 |

## MCP·AI 에이전트

| 자료 | 무엇을 찾나 |
|---|---|
| [Model Context Protocol](https://modelcontextprotocol.io) | MCP 사양과 개념 |
| [Claude Code — MCP](https://code.claude.com/docs/en/mcp) | `claude mcp add` 로 서버 등록 |
| [Cursor — MCP](https://docs.cursor.com/context/model-context-protocol) | Cursor 의 `mcp.json` 설정 |
| [MCP Registry](https://registry.modelcontextprotocol.io) | 공개 MCP 서버 목록 |

## 한국 시장 데이터 (공공)

| 자료 | 무엇을 찾나 |
|---|---|
| [KRX 정보데이터시스템](https://data.krx.co.kr) | 상장 종목·지수·투자자별 매매 통계 |
| [DART 오픈API](https://opendart.fss.or.kr) | 공시·재무제표 API (금융감독원) |

## 커뮤니티

- [GitHub `kiwoom` 토픽](https://github.com/topics/kiwoom) — 키움 관련 오픈소스 프로젝트
- 질문·버그 제보는 [kiwoom-client Issues](https://github.com/younghwan91/kiwoom-client/issues)

<small>kiwoom-client 는 키움증권과 무관한 비공식 오픈소스 프로젝트입니다. 위 키움증권 링크는 참고용이며 내용의 정본은 키움증권 공식 사이트입니다.</small>
