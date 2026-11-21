---
seo_title: "kiwoom-client 가 쓰이는 곳 — 공개 프로젝트"
description: "kiwoom-client 로 매일 돌아가는 공개 프로젝트 — 데이터 수집 파이프라인, 퀀트 공통 코어, 자동매매 데몬에서 키움 REST API 를 어떻게 쓰는지 볼 수 있습니다."
---

# 쓰이는 곳

kiwoom-client 로 돌아가는 공개 프로젝트입니다. 실제로 매일 도는 코드라 라이브러리를 어떻게 쓰는지 보는 예제로도 좋습니다.

| 프로젝트 | 무엇을 하나 | kiwoom-client 를 쓰는 곳 |
|---|---|---|
| [quant-airflow](https://github.com/younghwan91/quant-airflow) | 한국 주식 데이터 수집 Airflow 파이프라인 — 시세·수급·실적을 TimescaleDB 에 적재 | 일일 수집 DAG 가 시세·수급·신용·공매도를 조회 |
| [krx-quant-core](https://github.com/younghwan91/krx-quant-core) | KRX 퀀트 공통 코어 — 호가·가격제한폭·거래비용 모델·주문 가드 | 호가단위 표(`tick_size`·`round_to_tick`)의 정본으로 가져다 쓰고, 백테스트 표가 어긋나면 실패하게 검사 |
| [daytrade-it](https://github.com/younghwan91/daytrade-it) | 데이트레이딩 연구 시스템 — 공시 리스크 게이트, 키움 브로커 어댑터, MCP 도구 | 키움 브로커 어댑터가 `KiwoomAPI` 로 시세·계좌·주문을 호출 |
| [scalp-it](https://github.com/younghwan91/scalp-it) | 단타 전략 검증 프레임워크 + 장중 실시간 틱·호가 수집 | 키움 어댑터가 `KiwoomAPI` 로 조회, 호가단위 계산에 `tick_size` |

<small>위 프로젝트는 모두 이 라이브러리 작성자의 공개 레포이고 연구·개인 운용 코드입니다(투자 권유 아님). 설명은 2026-11 기준 각 레포 소개 문구와 코드를 요약했습니다.</small>

## 내 프로젝트 올리기

kiwoom-client 를 쓰는 **공개** 프로젝트가 있다면 이 페이지에 PR 로 한 줄 추가해 주세요.

```markdown
| [프로젝트 이름](https://github.com/<계정>/<레포>) | 무엇을 하나 (한 줄) | kiwoom-client 를 쓰는 곳 (예: 실시간 체결 수집, 조건검색 알림 봇) |
```

- 공개 레포·공개 페이지만 받습니다. 계좌번호·키·수익 인증 같은 개인 정보는 넣지 마세요.
- 투자 권유나 수익률 홍보 문구는 빼 주세요. "무엇을 하는 코드인가" 만 적습니다.
