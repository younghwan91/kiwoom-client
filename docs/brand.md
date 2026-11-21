# 브랜드 가이드 (초안)

README·문서 사이트·이미지·홍보 문구를 같은 목소리로 쓰기 위한 기준입니다. 새 페이지나 그림을 만들 때 먼저 읽고,
여기와 어긋나는 결정을 하면 이 문서부터 고칩니다.

> kiwoom-client 는 키움증권과 **무관한 비공식 오픈소스 프로젝트**입니다. 키움증권의 로고·상표·색 조합을 쓰거나
> 흉내 내지 않고, 공식 제품처럼 보이는 표현을 쓰지 않습니다.

## 포지셔닝

| | 문장 |
|---|---|
| 한국어 | 키움증권 REST API 를 파이썬과 AI 에이전트에서 쓰는 가장 빠른 길 — 비공식 오픈소스 클라이언트. |
| English | The shortest path from Python and AI agents to the Kiwoom Securities REST API — an unofficial open-source client. |

누구를 위한 것인가: 키움 계좌로 자동매매·데이터 수집·리서치를 하려는 파이썬 개발자, 그리고 Claude Code·Cursor 같은
MCP 클라이언트로 시세·계좌를 다루려는 사람. OpenAPI+(OCX) 를 쓰던 사람이 Linux 서버나 맥으로 옮겨 올 때 처음 도착하는 곳이
되는 것이 목표입니다.

## 태그라인

| # | 한국어 | English | 쓰는 곳 |
|---|---|---|---|
| 1 | 키움 REST API, 파이썬과 AI 에이전트로. | The Kiwoom REST API, from Python and AI agents. | **추천** — README 제목 아래, 소셜 프리뷰, 사이트 히어로 |
| 2 | `pip install` 한 줄로 키움 엔드포인트 전부. | Every Kiwoom endpoint, one `pip install` away. | 설치·PyPI 맥락 |
| 3 | 시세는 에이전트에게, 실주문은 내 허락으로. | Agents get the market. Live orders need your say-so. | MCP 서버 소개 |

추천은 1번입니다. 무엇(키움 REST API)·누구(파이썬·AI 에이전트)를 한 줄에 담고, 숫자가 바뀌어도 낡지 않습니다.
2번은 엔드포인트 수 같은 숫자를 붙여 쓰기 쉽고, 3번은 MCP 가드를 설명할 때만 씁니다.

## 핵심 메시지

모든 첫 화면(README 상단, 사이트 랜딩, 소셜 프리뷰)은 이 세 가지를 이 순서로 말합니다. 각 메시지는 **코드나 테스트로
증명되는 사실**만 붙입니다.

1. **쉽다** — `pip install kiwoom-client` 하고 앱키 두 개만 넣으면 됩니다. 토큰 발급·만료 전 갱신·401 재발급,
   TR별 Rate Limit, 연속조회를 라이브러리가 맡습니다. COM/OCX 가 없어 Windows·macOS·Linux 어디서나 돕니다.
   - 근거: `auth.py`, `rate_limiter.py`, `request_all()`, 단위 테스트.
2. **AI 네이티브** — MCP 서버가 내장돼 있어 Claude Code·Cursor 가 REST 엔드포인트 전부와 조건검색을 도구로 부릅니다.
   응답은 `to_dataframe()` 으로 바로 계산 가능한 숫자가 됩니다.
   - 근거: `kiwoom-client-mcp` 엔트리포인트, `mcp/tools.py`.
3. **실주문은 안전하게** — 실전투자 서버에서는 `KIWOOM_MCP_ALLOW_LIVE_ORDERS=true` 를 켜기 전까지 주문 도구가
   **등록조차 되지 않습니다**. 에이전트는 그런 도구가 있는지도 모릅니다.
   - 근거: `mcp/guard.py`, 가드 테스트. 이 가드는 MCP 경로에만 있고 파이썬 직접 호출은 막지 않는다는 사실도 같이 말합니다.

## 톤 앤 매너

- **기술 중심, 담백하게.** 무엇을 하는지와 어떻게 증명되는지를 말합니다. "최고의", "완벽한", "혁신적인" 같은 말은 쓰지 않습니다.
- **숫자는 코드에서 센 것만.** 엔드포인트 수·실시간 타입 수는 `scripts/make_hero.py` 처럼 코드에서 세고, 손으로 적은
  숫자는 바뀔 때 같이 고칩니다. 측정값(Rate Limit 등)은 측정했다고 밝힙니다.
- **미확정은 미확정이라고.** 장중에만 확인되는 동작(WebSocket REAL 프레임 필드명 등)은 "검증 상태"로 따로 적습니다.
- **위험은 먼저 말합니다.** 실서버가 기본값(`is_mock=False`)이라는 것, 주문 메서드는 곧바로 실주문이라는 것을 숨기지 않습니다.
- **배지는 최소, 스타 요청은 없음.** 배지는 사실 정보(버전·CI·라이선스·파이썬 버전·다운로드)만. "스타 눌러 주세요", 스타 히스토리,
  이모지 장식은 넣지 않습니다.
- **한국어가 원본, 영어는 짝.** README 와 README_EN 은 같은 구조·같은 사실을 유지합니다. 키움 용어(TR, 실전투자/모의투자,
  호가단위)는 한국어 그대로 두고 영어판에서 한 번 풀어 줍니다(TR = transaction code, 실전투자 = live, 모의투자 = mock).
- **예시는 예시라고.** 실서버 호출 없이 만든 그림·대화 예시에는 "예시" 표시를 붙입니다.

## 비공식 고지

README 두 벌, 문서 사이트 푸터, PyPI 설명에 같은 뜻으로 들어갑니다.

- 한국어: 키움증권과 무관한 비공식 오픈소스 프로젝트입니다. "키움"·"Kiwoom" 은 키움증권(주)의 상표이며, 이 프로젝트는
  키움증권이 공개한 REST API 를 호출하는 클라이언트일 뿐입니다.
- English: An unofficial open-source project, not affiliated with or endorsed by Kiwoom Securities. "Kiwoom" is a
  trademark of Kiwoom Securities Co., Ltd.; this project is only a client for its public REST API.

## 색 토큰

`scripts/brand_tokens.py` 가 정본입니다(히어로 그림의 `hero_style.py` 도 여기서 가져갑니다). 그림과 로고와 사이트가 한 팔레트에서 나옵니다.
키움증권 CI 의 마젠타·보라 계열은 브랜드 색으로 쓰지 않습니다.

| 토큰 | 라이트 | 다크 | 쓰임 |
|---|---|---|---|
| `brand` | `#2563EB` | `#3B82F6` | 로고 마크, 링크, 사이트 primary |
| `ink` | `#0B0F19` | `#E6EDF3` | 본문 글자, 워드마크 |
| `ink2` | `#4B5563` | `#9DA7B3` | 보조 글자, 워드마크의 `-client` |
| `ink3` | `#9CA3AF` | `#6E7681` | 캡션·출처 |
| `surface` | `#FFFFFF` | `#0D1117` | 배경 |
| `surface2` | `#F6F8FA` | `#161B22` | 카드·코드 블록 배경 |
| `grid` | `#E5E7EB` | `#30363D` | 구분선 |
| `good` | `#059669` | `#059669` | "가드 켜짐", 성공 상태 |
| `warn` | `#B45309` | `#D97706` | 실서버·실주문 경고 |
| `bad` | `#DC2626` | `#F87171` | 오류 |

규칙: 상태색(`good`/`warn`/`bad`)은 상태에만 씁니다. 글자는 `ink` 계열로만 쓰고 데이터 색으로 쓰지 않습니다.
다크 배경은 GitHub 다크 테마(`#0D1117`)와 맞춰 README 의 `<picture>` 전환이 자연스럽게 보이게 합니다.

## 타이포그래피

| 용도 | 글꼴 | 비고 |
|---|---|---|
| 제목·본문 (한·영) | **Noto Sans KR** | 한글과 라틴을 한 글꼴로. 굵기 400 / 700 |
| 코드·식별자 | **JetBrains Mono** (없으면 DejaVu Sans Mono) | `api_id`, 환경변수, 터미널 그림 |
| 워드마크 | Noto Sans KR 700 + 400 | `kiwoom` 굵게 + `-client` 보통, 전부 소문자 |

그림 생성기는 시스템 글꼴을 쓰므로 Noto Sans KR 이 없으면 DejaVu Sans 로 떨어집니다. 사이트는 MkDocs Material 의
`theme.font` 로 같은 두 글꼴을 지정합니다.

## 로고 콘셉트

**캔들 K.** 소문자 `k` 의 세로획을 캔들스틱(몸통 + 위아래 꼬리)으로, 두 팔을 끝에 점이 달린 연결선으로 그립니다.
캔들은 시세를, 점 달린 선은 API·에이전트 연결을 뜻합니다.

- 모양: 둥근 사각형(라운드 22%) 안에 흰 마크, 또는 투명 배경 위 `brand` 색 마크. 16px 파비콘에서도 읽히게 선은 굵게.
- 색: `brand` 한 색. 라이트·다크 두 벌(다크는 `#3B82F6`). 그라데이션·그림자 없음.
- 워드마크: 마크 + `kiwoom-client`(소문자). 항상 `-client` 를 붙여 써서 "키움" 단독 표기처럼 보이지 않게 합니다.
- 하지 않는 것: 키움증권 로고 모양·마젠타·심볼 흉내, 증권사 공식 앱 아이콘처럼 보이는 구성, "키움증권" 한글 로고타입.
- 생성: 로고는 코드로 그립니다(SVG 원본 + PNG 렌더). 손으로 그린 파일은 두지 않습니다.

| 파일 (`docs/images/brand/`) | 쓰임 |
|---|---|
| `wordmark-light.svg` / `wordmark-dark.svg` | README 상단 `<picture>`, 문서 |
| `mark.svg` | 파비콘(SVG), 아바타 |
| `mark-white.svg` | 색 배경 위(문서 사이트 헤더) |
| `favicon-32.png` / `mark-512.png` | PNG 파비콘, 레지스트리·커뮤니티 아이콘 |

다시 만들기: `uv run --no-project --with fonttools --with cairosvg python scripts/make_logo.py`.
워드마크 글자는 글꼴 윤곽선을 path 로 박아 넣으므로 보는 쪽 글꼴과 상관없이 같게 보입니다.

## 시각물 원칙

- 그림은 전부 스크립트로 다시 만들 수 있어야 합니다(`scripts/`). 라이트·다크 두 벌을 만들고 README 에서 `<picture>` 로 바꿔 끼웁니다.
- 숫자가 든 그림은 코드에서 센 값으로 그리고, 생성 날짜를 스크립트에 남깁니다.
- 실서버를 부르지 않고 만든 터미널·대화 그림에는 "예시" 표시를 넣습니다.
- PyPI 에서도 보이게 README 의 이미지는 `raw.githubusercontent.com` 절대 URL 로 겁니다.

## 이름과 표기

- 패키지·레포 이름은 `kiwoom-client` 하나입니다(공개 PyPI 패키지라 바꾸지 않습니다). 임포트는 `kiwoom_client`,
  MCP 서버 명령은 `kiwoom-client-mcp`.
- 문장 안에서는 코드 글꼴 없이 kiwoom-client 로, 명령·임포트는 코드 글꼴로 씁니다.
- "키움증권 공식", "키움 API 공식 파이썬 SDK" 같은 표현은 쓰지 않습니다.
