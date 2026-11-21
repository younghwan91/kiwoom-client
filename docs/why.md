---
seo_title: "키움증권 파이썬 API 비교 — OpenAPI+(OCX)·pykiwoom vs REST API"
description: "키움 OpenAPI+(OCX/COM)와 REST API, pykiwoom 등 파이썬 라이브러리를 운영체제·64bit·서버 배포·인증 방식으로 사실대로 비교합니다. 다른 것을 고를 때도 함께 적었습니다."
---

# 왜 kiwoom-client 인가

키움증권으로 파이썬 자동매매·데이터 수집을 하는 방법은 크게 둘입니다. 오래된 **OpenAPI+(OCX/COM)** 를 감싼 라이브러리,
그리고 새로 공개된 **키움 REST API** 를 감싼 라이브러리. 이 페이지는 둘을, 그리고 REST 쪽 대안들을 사실대로 비교합니다.
어느 것이 맞는지는 하려는 일에 달려 있습니다 — 아래 "다른 것을 고를 때" 도 같이 보세요.

## OpenAPI+(OCX) 와 REST API

| 항목 | OpenAPI+ (OCX/COM) | 키움 REST API |
|---|---|---|
| 연동 방식 | Windows COM 컨트롤 + 이벤트 콜백 | HTTPS(JSON) + WebSocket |
| 운영체제 | Windows 전용 | Windows · macOS · Linux |
| 파이썬 | 오랫동안 32bit 파이썬 전용이었고, Qt 이벤트 루프에 묶임 | 64bit, 일반 `asyncio`/스레드 |
| 서버·도커·클라우드 배포 | GUI 세션이 필요해 어렵다 | 헤드리스로 가능 |
| 로그인 | OpenAPI 로그인 창(사람 입력 또는 자동로그인 설정) | 앱키·시크릿키로 토큰 발급 |
| 인증 단위 | 사용자 PC 설치 | 앱 등록(포털에서 API 사용신청) |

REST API 로 옮기면 Linux 서버나 맥에서, 사람이 로그인 창을 누르지 않고 돌릴 수 있습니다. 대신 OpenAPI+ 에만 있던 기능이
REST 에 아직 없을 수 있으니, 꼭 필요한 TR 은 [키움 REST API 가이드](https://openapi.kiwoom.com/guide/apiguide)에서
먼저 찾아보세요. kiwoom-client 가 감싼 목록은 [엔드포인트 전체 목록](endpoints.md)에, OpenAPI+ TR·함수와의 대응은
[OpenAPI+(OCX) · pykiwoom 에서 옮겨 오기](migration-from-openapi-plus.md)에 있습니다.

## 파이썬 라이브러리 한눈에

2026-11-21 PyPI 메타데이터와 각 프로젝트 README 에 적힌 내용 기준입니다. 버전과 기능은 바뀌므로 고르기 전에 각 프로젝트 페이지를 확인하세요.

### 키움증권 공식

| 저장소 / 패키지 | 최신 (올린 날) | 파이썬 | 라이선스 | README 에 적힌 내용 |
|---|---|---|---|---|
| [Kiwoom-Securities/Kiwoom-REST-API](https://github.com/Kiwoom-Securities/Kiwoom-REST-API) · PyPI `kwcli` | `kwcli` 1.0.3 (2026-09) | ≥ 3.13 | 키움증권 자체 라이선스(키움 OpenAPI 이용 목적으로 사용 허락) | API 337종 스펙(국내주식·**미국주식**), 함수별 예제 362개, Postman 컬렉션, CLI `kiwoomcli`, MCP 서버 2종(스펙 검색용·실행용 — 주문은 명시 허용 시에만) |

키움증권이 직접 내는 저장소라 API 스펙의 정본에 가장 가깝고, 미국주식까지 다룹니다. 아래 비교는 이 공식 도구와 겹치는 부분이 있다는 것을 전제로 읽어 주세요.

### OpenAPI+(OCX) 래퍼

| 패키지 | 최신 버전 (올린 날) | 파이썬 | 비고 |
|---|---|---|---|
| [pykiwoom](https://github.com/sharebook-kr/pykiwoom) | 0.1.6 (2024-01) | 명시 없음 | pywin32·PyQt5 의존. 한국어 자료가 가장 많다 |
| [KOAPY](https://github.com/elbakramer/koapy) | 0.9.0 (2022-09) | 3.8–3.10 | gRPC 서버로 OCX 를 원격 호출 |
| [kiwoom](https://github.com/breadum/kiwoom) | 1.5.0 (2025-08) | 3.8–3.11 | PyQt5 기반의 얇은 래퍼 |

### REST API 래퍼

| 패키지 | 최신 버전 (올린 날) | 파이썬 | 라이선스 | README 에 적힌 특징 |
|---|---|---|---|---|
| **kiwoom-client** (이 프로젝트) | PyPI 참고 | ≥ 3.10 | MIT | sync·async 같은 표면, 토큰 자동 갱신, TR별 Rate Limiter, 실시간 WebSocket, MCP 서버(실주문 opt-in) |
| [pykiwoom-rest](https://github.com/unohee/pykiwoom-rest) | 2.2.0 (2026-07) | ≥ 3.8 (MCP 는 ≥ 3.10) | MIT | 라이브러리 + `kiwoom` CLI + MCP 서버, pandas 출력 |
| [kiwoom-cli](https://github.com/gejyn14/kiwoom-cli) / [kiwoom-mcp](https://github.com/gejyn14/kiwoom-plugin) | 2.14.0 / 0.1.2 (2026-07) | ≥ 3.10 | 자체 라이선스 / Apache-2.0 | CLI 중심. MCP 는 `--allow-orders` 일 때만 주문 도구 등록, 주문 사전점검·dry-run |
| [kiwoompy](https://github.com/meonji-gogo/kiwoompy) | 0.1.6 (2026-03) | ≥ 3.12 | MIT | 응답을 속성으로 읽는 모델(`balance.tot_evlt_amt`), 문서 사이트 |
| [kiwoom-rest-api](https://pypi.org/project/kiwoom-rest-api/) | 0.1.12 (2025-06) | ≥ 3.9 | 명시 없음 | 모듈별 클래스 + CLI |

## kiwoom-client 가 다른 점

모두 코드와 테스트로 확인할 수 있는 것만 적습니다.

- **엔드포인트를 코드에서 센다.** REST 182개·조건검색 4종·실시간 19종을 15개 모듈로 감쌌고, 그 목록은 소스에서 생성됩니다
  ([엔드포인트 전체 목록](endpoints.md)). 메서드 이름 옆에 키움 공식 api_id(`ka10001` 등)가 그대로 붙어 있어 공식 가이드와 바로 대조됩니다.
- **sync 와 async 가 같은 표면.** `KiwoomAPI` 와 `AsyncKiwoomAPI` 는 같은 모듈·같은 메서드를 갖습니다. 스크립트로 시작해
  `asyncio.gather` 로 넘어갈 때 코드를 다시 짜지 않아도 됩니다.
- **오래 도는 봇을 위한 기본값.** 토큰은 만료 전에 갱신되고 401 이면 재발급 후 재시도합니다. Rate Limit 은 실측한 TR별 한도
  (약 1 req/s, 버스트 2)에 맞춘 토큰 버킷이고, 429 가 나면 백오프 후 다시 보냅니다.
- **에이전트가 실주문을 모르게.** 내장 MCP 서버는 실전투자 서버에서 `KIWOOM_MCP_ALLOW_LIVE_ORDERS=true` 를 켜기 전까지
  주문 도구 12개를 **등록하지 않습니다**. 모의투자에서는 항상 쓸 수 있습니다.
  키움 공식 MCP·플러그인을 쓰면서 주문 **내용**(금액·수량 상한, 시장가 매수, 반복 전송, 하루 횟수)까지 막고 싶다면
  같은 저자의 Claude Code 훅 [kiwoom-order-guard](https://github.com/younghwan91/kiwoom-order-guard)를 함께 쓰세요.
- **계산 가능한 응답.** `to_dataframe()`·`to_number()` 가 `"+70000"`, `"1,234,567"` 같은 문자열을 숫자로 바꾸고,
  종목코드처럼 앞자리 0 이 의미 있는 값은 문자열로 남깁니다. `round_to_tick()` 은 지정가를 KRX 호가단위에 맞춥니다.
- **타입 정보 포함.** `py.typed` 를 배포하고 CI 에서 mypy 를 돌립니다.

## 다른 것을 고를 때

- **터미널에서 바로 조회·주문하는 CLI** 가 주목적이면 kiwoom-cli 나 pykiwoom-rest 의 CLI 가 더 맞습니다. kiwoom-client 는 라이브러리와 MCP 서버만 제공합니다.
- **응답을 속성 접근 모델로** 받고 싶다면 kiwoompy 를 보세요. kiwoom-client 는 키움 응답 JSON(dict) 을 그대로 돌려주고, 필요하면 `to_dataframe()` 으로 바꿉니다.
- **키움증권이 직접 관리하는 도구**, 또는 **미국주식 API** 가 필요하다면 [키움 공식 저장소](https://github.com/Kiwoom-Securities/Kiwoom-REST-API)와 `kwcli` 를 쓰세요. kiwoom-client 는 국내주식 REST 만 감쌉니다.
- **OpenAPI+ 에만 있는 기능**에 의존한다면 아직은 pykiwoom 같은 OCX 래퍼가 필요할 수 있습니다.
- **파이썬 3.8·3.9** 를 써야 한다면 kiwoom-client(≥ 3.10)는 맞지 않습니다.

반대로 MIT 라이선스의 `pip install` 라이브러리로 국내주식 REST 를 sync·async 양쪽에서 쓰고, 같은 패키지로 MCP 서버까지 띄우고 싶다면 kiwoom-client 가 맞습니다.

비교에 틀린 내용이 있거나 빠진 프로젝트가 있으면 [이슈](https://github.com/younghwan91/kiwoom-client/issues)로 알려 주세요. 바로 고치겠습니다.

<small>kiwoom-client 는 키움증권과 무관한 비공식 오픈소스 프로젝트입니다.</small>
