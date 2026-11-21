<!-- 자동 생성 파일 — 손으로 고치지 마세요. `python scripts/gen_docs.py` 가 TR 카탈로그(kiwoom_client.spec)로 다시 만듭니다. -->

# 필드 레퍼런스 (Field reference)

REST 엔드포인트마다 요청·응답 필드(필드명·한글명·필수·길이·설명)를 모은 페이지입니다. 모듈별 표에서 api_id 를 누르면 그 TR 로 갑니다.

- 데이터: 키움 공식 명세 [`Kiwoom-Securities/Kiwoom-REST-API`](https://github.com/Kiwoom-Securities/Kiwoom-REST-API) 커밋 `c7a3d25` 을 변환한 TR 카탈로그 ([출처·라이선스](https://github.com/younghwan91/kiwoom-client/blob/main/src/kiwoom_client/spec/SOURCE.md))
- 코드에서: `kiwoom_client.spec.get("ka10001")`, IDE 에서는 메서드 키워드 인자 자동완성
- 보내기 전에 검사하려면 `KiwoomAPI(..., validate_params="warn")`

| 모듈 | 이름 | 개수 |
|---|---|---:|
| [`api.account`](account.md) | 계좌 (Account) | 33 |
| [`api.stock_info`](stock_info.md) | 종목정보 (Stock Information) | 31 |
| [`api.market`](market.md) | 시세 (Market Condition) | 25 |
| [`api.chart`](chart.md) | 차트 (Chart) | 21 |
| [`api.order`](order.md) | 주문 (Order) | 8 |
| [`api.credit_order`](credit_order.md) | 신용주문 (Credit Order) | 4 |
| [`api.ranking`](ranking.md) | 순위정보 (Ranking) | 23 |
| [`api.sector`](sector.md) | 업종 (Sector) | 6 |
| [`api.foreign_institution`](foreign_institution.md) | 기관/외국인 (Foreign/Institution) | 4 |
| [`api.short_selling`](short_selling.md) | 공매도 (Short Selling) | 1 |
| [`api.slb`](slb.md) | 대차거래 (Stock Lending & Borrowing) | 4 |
| [`api.theme`](theme.md) | 테마 (Theme) | 2 |
| [`api.elw`](elw.md) | ELW | 11 |
| [`api.etf`](etf.md) | ETF | 9 |
