---
hide:
  - navigation
  - toc
---

# kiwoom-client { .kc-sr-only }

<div class="kc-hero" markdown>

![kiwoom-client](images/brand/wordmark-light.svg#only-light)
![kiwoom-client](images/brand/wordmark-dark.svg#only-dark)

<p class="kc-tagline">키움 REST API, 파이썬과 AI 에이전트로.</p>
<p class="kc-sub">키움증권 REST API 182개 엔드포인트·조건검색·실시간 WebSocket 을 감싼 비공식 오픈소스 파이썬 클라이언트. MCP 서버 내장.</p>

[빠른 시작](#빠른-시작){ .md-button .md-button--primary }
[GitHub](https://github.com/younghwan91/kiwoom-client){ .md-button }
[PyPI](https://pypi.org/project/kiwoom-client/){ .md-button }

</div>

<div class="grid cards" markdown>

-   **쉽다**

    ---

    `pip install` 하고 앱키 두 개만 넣으면 됩니다. 토큰 발급·만료 전 갱신·401 재발급, TR별 Rate Limit,
    연속조회를 라이브러리가 맡습니다. COM/OCX 가 없어 Windows·macOS·Linux 어디서나 돕니다.

-   **AI 네이티브**

    ---

    `kiwoom-client-mcp` 하나로 Claude Code·Cursor 가 REST 엔드포인트 182개와 조건검색 4종을 MCP 도구로 부릅니다.
    응답은 `to_dataframe()` 으로 바로 계산 가능한 숫자가 됩니다.

-   **실주문은 허락받고**

    ---

    실전투자 서버에서는 `KIWOOM_MCP_ALLOW_LIVE_ORDERS=true` 를 켜기 전까지 주문 도구 12개가 **등록조차 되지 않습니다**.
    에이전트는 그런 도구가 있는지도 모릅니다.

</div>

## 빠른 시작

```bash
pip install kiwoom-client
```

```python
from kiwoom_client import KiwoomAPI

api = KiwoomAPI(app_key="발급받은_앱키", app_secret="발급받은_시크릿키", is_mock=True)  # True=모의투자

info = api.stock_info.basic_stock_info(stk_cd="005930")                   # 삼성전자 기본 정보
chart = api.chart.stock_daily_chart(stk_cd="005930", base_dt="20260326")  # 일봉
print(info["stk_nm"])
```

앱키·시크릿키는 [키움 REST API 포털](https://openapi.kiwoom.com)에서 발급받습니다. 처음에는 모의투자(`is_mock=True`)로 시작하세요.

!!! warning "기본값은 실서버입니다"
    `KiwoomAPI(...)` 의 기본값은 `is_mock=False`(실전투자)입니다. 실전 키로 `api.order.*`·`api.credit_order.*` 를
    부르면 그대로 실주문이 나갑니다. MCP 실주문 가드는 MCP 서버 경로에만 있고 파이썬 직접 호출은 막지 않습니다.

## 어디로 갈까

| 하고 싶은 것 | 갈 곳 |
|---|---|
| 설치·사용법 전체 (sync/async, WebSocket, 에러 처리) | [README](https://github.com/younghwan91/kiwoom-client#readme) |
| 182개 메서드의 api_id·TR 이름 찾기 | [엔드포인트 전체 목록](endpoints.md) |
| Claude Code·Cursor 에 붙이기 | [README — MCP 서버로 사용하기](https://github.com/younghwan91/kiwoom-client#mcp-서버로-사용하기) |
| OpenAPI+·pykiwoom·다른 REST 래퍼와 비교 | [왜 kiwoom-client 인가](why.md) |
| 이 라이브러리로 돌아가는 공개 프로젝트 | [쓰이는 곳](showcase.md) |
| 키움 공식 포털·MCP·공공 데이터 링크 | [자료 모음](resources.md) |
| 버그 제보·기능 요청 | [GitHub Issues](https://github.com/younghwan91/kiwoom-client/issues) |

---

<small>kiwoom-client 는 키움증권과 무관한 비공식 오픈소스 프로젝트입니다. "키움"·"Kiwoom" 은 키움증권(주)의 상표이며,
이 프로젝트는 키움증권이 공개한 REST API 를 호출하는 클라이언트일 뿐입니다.</small>
