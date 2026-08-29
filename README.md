[한국어](README.md) | [English](README_EN.md)

# kiwoom-rest-api — 키움증권 REST API Python 라이브러리

[![PyPI version](https://img.shields.io/pypi/v/kiwoom-client)](https://pypi.org/project/kiwoom-client/)
[![Downloads](https://img.shields.io/pypi/dm/kiwoom-client)](https://pypi.org/project/kiwoom-client/)
[![CI](https://github.com/younghwan91/kiwoom-rest-api/actions/workflows/ci.yml/badge.svg)](https://github.com/younghwan91/kiwoom-rest-api/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/github/license/younghwan91/kiwoom-rest-api)](https://github.com/younghwan91/kiwoom-rest-api/blob/main/LICENSE)
[![Python](https://img.shields.io/pypi/pyversions/kiwoom-client)](https://pypi.org/project/kiwoom-client/)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-younghwan--chae-0A66C2?logo=linkedin&logoColor=white)](https://www.linkedin.com/in/younghwan-chae/)

> **키움 OpenAPI+(OCX/COM)를 대체하는 Python REST 래퍼.** COM/OCX 없이 Windows · macOS · Linux
> 어디서나 **국내주식 자동매매 · 시세조회 · 실시간 WebSocket** 을 씁니다. 토큰은 알아서 갱신되고,
> sync / async 양쪽을 지원합니다. **182개 REST 엔드포인트 · 조건검색 4종 · 19종 실시간 데이터.**

```bash
pip install kiwoom-client
```

> ⚠️ 패키지 이름은 **`kiwoom-client`** 입니다. 저장소 이름(`kiwoom-rest-api`)으로 설치하면
> PyPI 에 먼저 등록된 **다른 사람의 패키지**가 깔립니다.

```python
from kiwoom_rest_api import KiwoomAPI, to_dataframe

api = KiwoomAPI(app_key="앱키", app_secret="시크릿키", is_mock=True)  # 로그인 단계 없음

info = api.stock_info.basic_stock_info(stk_cd="005930")            # 삼성전자 기본정보
df   = to_dataframe(api.chart.stock_daily_chart(stk_cd="005930"))  # 일봉 → DataFrame

api.order.buy_order(dmst_stex_tp="01", stk_cd="005930",            # 10주 지정가 매수
                    ord_qty=10, trde_tp="00", ord_uv=70000)
```

키움은 모든 값을 문자열로 돌려줍니다 — 가격은 `"+70000"`, 거래량은 `"1,234,567"`.
`to_dataframe()` 이 페이로드 키를 찾아 숫자로 바꾸되, 종목코드처럼 앞자리 0 이 의미를
갖는 필드는 문자열로 남깁니다.

![to_dataframe() 실행 결과 — 문자열 응답이 계산 가능한 DataFrame 이 된다](docs/images/to_dataframe.png)

## 기존 키움 OpenAPI+ / pykiwoom 과 무엇이 다른가

| 항목 | 키움 OpenAPI+ (OCX) | pykiwoom | **kiwoom-client** |
|------|---------------------|----------|---------------------|
| 연동 방식 | COM/OCX | OCX 래퍼 | **REST + WebSocket** |
| 운영체제 | Windows 전용 | Windows 전용 | **Windows · macOS · Linux** |
| Python 비트수 | 32bit 전용 | 32bit 전용 | **64bit 지원** |
| 서버/헤드리스 배포 | 어려움 (GUI 필요) | 어려움 | **가능** |
| 실시간 데이터 | 이벤트 콜백 | 이벤트 콜백 | **async WebSocket** |
| 설치 | 별도 모듈 설치 | OCX + 모듈 | **`pip install` 한 줄** |

여기에 더해 **토큰 자동 갱신**(만료 전 선제 재발급 + 인증 실패 시 재시도), **TR별 토큰 버킷
Rate Limiter**(429 자동 백오프), **`request_all()` 자동 페이지네이션**, 그리고 `KiwoomAPI` 와
동일한 인터페이스의 **`AsyncKiwoomAPI`** 가 기본 탑재입니다.

## 실시간 WebSocket

```python
import asyncio
from kiwoom_rest_api import KiwoomAPI

ws = KiwoomAPI(app_key="앱키", app_secret="시크릿키").create_websocket()

async def main():
    await ws.connect()                    # LOGIN 핸드셰이크까지 끝낸다
    ws.on("0B", lambda d: print(f"체결 {d['item']}: {d['values'].get('10')}"))
    await ws.subscribe(["0B", "0D"], ["005930", "000660"])
    await ws.listen()                     # PING 응답·재연결·구독 복원은 알아서

asyncio.run(main())
```

`values` 의 키는 키움 FID 번호입니다 (10=현재가, 13=누적거래량, 41=매도최우선호가).
조건검색도 같은 소켓을 타며, `api.condition_search` 가 만든 페이로드를 `ws.send()` 로 보냅니다.

> **검증 상태**: LOGIN 핸드셰이크 · PING · REG 응답까지 실서버(api.kiwoom.com)에서 확인했습니다.
> REAL 프레임의 항목 필드명(`item`/`values`)은 아직 장중 검증 전입니다.
> 이상 동작을 만나면 [이슈](https://github.com/younghwan91/kiwoom-rest-api/issues)로 알려주세요.

## 지원 범위

REST **182개** + 조건검색 **4종**(WebSocket) + 실시간 **19종**.

계좌 33 · 종목정보 31 · 시세 25 · 순위 23 · 차트 21 · ELW 11 · ETF 9 · 주문 8 · 업종 6 ·
신용주문 4 · 기관외국인 4 · 대차 4 · 조건검색 4 · 테마 2 · 공매도 1

메서드 이름과 API ID 전수 목록은 **[지원 API 전체 목록](docs/api-reference.md)** 에 있습니다.

## 더 보기

- **[사용 가이드](docs/guide.md)** — 사전 준비, 모의/실전 전환, 계좌·주문, asyncio, 연속조회, Rate Limit
- **[FAQ](docs/faq.md)** — 앱키 발급, 토큰 만료, 429 대응
- **[예제 코드](examples/)** — 기본·시세·주문·async·pandas·WebSocket 6종
- [CHANGELOG](CHANGELOG.md) · [CONTRIBUTING](CONTRIBUTING.md) · [키움 공식 가이드](https://openapi.kiwoom.com/guide/apiguide)

**실제로 돌아가는 곳** — [quant-airflow](https://github.com/younghwan91/quant-airflow) 의 일일 수집
DAG 가 이 라이브러리로 시세·수급·신용·공매도를 매일 TimescaleDB 에 적재합니다.

## 라이선스

MIT

---

## ⭐ 도움이 되셨다면

우측 상단 **[⭐ Star](https://github.com/younghwan91/kiwoom-rest-api)** 를 눌러주세요.
버그·질문은 [Issues](https://github.com/younghwan91/kiwoom-rest-api/issues), 개선 PR 환영합니다.

## 관련 프로젝트 — 오픈소스 퀀트 스택

한국·미국 주식과 암호화폐를 아우르는 오픈소스 스택입니다. 각 저장소는 독립적으로 쓸 수 있습니다.

| 축 | 프로젝트 | 설명 |
|---|---|---|
| 🇰🇷 한국 주식 | **[krx-fundamentals-api](https://github.com/younghwan91/krx-fundamentals-api)** | 국내 기업 펀더멘탈 REST API — 재무제표·투자지표·배당·종목 스크리닝 (DART + KRX + 네이버) |
| 🇰🇷 한국 주식 | **[krx-news-rest-api](https://github.com/younghwan91/krx-news-rest-api)** | 한국 주식 뉴스·공시 수집 REST API (FastAPI + Redis) |
| 🇰🇷 한국 주식 | **[quant-airflow](https://github.com/younghwan91/quant-airflow)** | 시세·수급·실적을 TimescaleDB 로 수집하는 Airflow 파이프라인 — 상장폐지 종목까지 담아 생존편향을 막는다 |
| 🇰🇷 한국 주식 | **[kr-quant](https://github.com/younghwan91/kr-quant)** | 코스피·코스닥 알파 리서치 — walk-forward·랜덤 음성대조·purged CV·Deflated Sharpe 를 CI 가드레일로 강제 |
| 🇺🇸 미국 주식 | **[portfolio-research](https://github.com/younghwan91/portfolio-research)** | 미국주식 팩터 엔진 — point-in-time·생존편향 보정 데이터 위에서 walk-forward 를 Deflated Sharpe·PBO 로 게이팅 (+ ETF 전술배분 TAA — 9개 사전등록, 채택 0) |
| 🇺🇸 미국 주식 | **[automated-stock-trading-systems](https://github.com/younghwan91/automated-stock-trading-systems)** | Bensdorp 의 7개 비상관 트레이딩 시스템 백테스터 (교육용 재구현) |
| ₿ 암호화폐 | **[quantbox-engine](https://github.com/younghwan91/quantbox-engine)** | 암호화폐 선물 백테스트·실행 엔진 — 룩어헤드 0, 백테스트↔실거래 일체화 |

## 만든 사람

**채영환 (Younghwan Chae)** · [GitHub @younghwan91](https://github.com/younghwan91) · [LinkedIn](https://www.linkedin.com/in/younghwan-chae/)

전체 오픈소스 퀀트 스택은 [프로필](https://github.com/younghwan91)에서 한눈에 볼 수 있습니다.
