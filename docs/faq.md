---
seo_title: "키움 REST API 파이썬 자주 묻는 질문 (FAQ)"
description: "키움증권 REST API 와 kiwoom-client 를 처음 쓸 때 자주 묻는 것 — 공식 여부, 앱키 발급, 모의투자, 맥·리눅스 지원, 주문 안전장치, MCP·AI 에이전트 연동."
---

# 자주 묻는 질문 (FAQ)

## 시작

**Q. 키움증권 공식 라이브러리인가요?**
아닙니다. 키움증권과 관계없는 오픈소스(MIT) 클라이언트입니다. 키움이 공개한 REST API 를 그대로 감쌌고,
필드·코드값은 키움 공식 문서·스펙을 따릅니다.

**Q. 앱키는 어디서 받나요?**
[키움 REST API 포털](https://openapi.kiwoom.com)에서 API 사용신청을 하면 앱키·시크릿키가 나옵니다.
**모의투자용과 실전투자용이 서로 다른 키**입니다.

**Q. 처음에 뭘 하면 되나요?**
모의투자 키로 시작하세요.

```python
from kiwoom_client import KiwoomAPI

api = KiwoomAPI.from_env(is_mock=True)  # KIWOOM_APP_KEY / KIWOOM_APP_SECRET
print(api.stock_info.basic_stock_info(stk_cd="005930")["stk_nm"])
```

`is_mock` 의 기본값은 `False`(실서버)입니다. 모의투자 키로 `is_mock` 을 빠뜨리면 8030/8031 오류가 납니다 —
[문제 해결](troubleshooting.md).

**Q. Windows 가 아니어도 되나요? 32bit 파이썬이 필요한가요?**
REST 라서 Windows · macOS · Linux 어디서나, 64bit 파이썬 3.10 이상이면 됩니다. OCX·로그인 창이 없어 서버·도커에서도 돕니다.
순서대로 따라 하려면 [맥·리눅스에서 쓰기](macos-linux.md).

**Q. OpenAPI+(KOA Studio)·pykiwoom 코드를 옮기려면?**
`opt10081` 같은 TR, `SendOrder`, `SetRealReg` 가 REST 에서 무엇인지 [OpenAPI+ 에서 옮겨 오기](migration-from-openapi-plus.md)에 정리했습니다.

## 쓰는 법

**Q. 원하는 TR(api_id)의 메서드를 어떻게 찾나요?**
[엔드포인트 전체 목록](endpoints.md)에서 api_id(`ka10081`)나 한글 TR 이름으로 찾으세요. 코드에서는:

```python
from kiwoom_client import spec

print([(t.api_id, t.name) for t in spec.search("일봉")])
print(spec.get("ka10081").required_fields)  # 필수 요청 필드
```

**Q. 요청 필드는 어떻게 넘기나요?**
키움 필드 이름 그대로 키워드 인자로, 값은 **문자열**로 넘깁니다(`stk_cd="005930"`, `ord_qty="10"`).
필드 목록은 [필드 레퍼런스](reference/index.md)나 `kiwoom_client.spec`. 자주 쓰는 코드값은 `kiwoom_client.codes`
(`OrderType.LIMIT`, `Exchange.KRX` …)에 이름이 있습니다.

**Q. 응답 값이 전부 문자열이에요.**
키움이 그렇게 줍니다(`"+70000"`, `"1,234"`). `to_dataframe()`·`normalize()`·`to_number()` 로 바꾸세요.
종목코드·날짜처럼 숫자처럼 보여도 숫자가 아닌 값은 문자열로 남깁니다.

**Q. sync(`KiwoomAPI`)와 async(`AsyncKiwoomAPI`) 중 뭘 쓰나요?**
간단한 스크립트는 sync. 서로 다른 TR 을 동시에 부르거나 WebSocket 과 같이 쓰면 async — [asyncio 레시피](cookbook/async-concurrency.md).

**Q. 연속조회(다음 페이지)는요?**
응답의 `"cont-yn"` 이 `"Y"` 면 `cont_yn="Y", next_key=resp["next-key"]` 로 다시 부르거나 `request_all()` — [연속조회 레시피](cookbook/pagination.md).

**Q. 토큰은 신경 써야 하나요?**
아니요. 첫 호출에서 발급하고, 만료 전에 갱신하고, 거부되면 다시 받아 한 번 더 보냅니다. 실서버 확인 결과 토큰 유효기간은
약 18시간이었고, 유효기간 안에 다시 발급하면 같은 토큰이 왔습니다(0.2.1 CHANGELOG).

**Q. `api.logout()` 을 불러야 하나요?**
필요 없습니다. `logout()` 은 토큰을 **폐기**해서, 같은 앱키를 쓰는 다른 프로그램의 세션까지 끊을 수 있습니다. 연결만 닫으려면 `api.close()` 나 `with` 문.

**Q. 호출 제한은?**
키움은 TR(api_id)마다 따로 제한합니다. 라이브러리가 TR당 초당 1건·버스트 2로 맞추고 429 면 재시도합니다 — [호출 제한 다루기](cookbook/rate-limits.md).

**Q. 넥스트레이드(NXT)·SOR 도 되나요?**
주문의 `dmst_stex_tp` 에 `KRX` · `NXT` · `SOR` 을 넣습니다. 시세·차트 TR 의 종목코드는 공식 스펙대로 `005930_NX` · `005930_AL` 꼴이고
`kiwoom_client.codes.exchange_stock_code("005930", "NXT")` 가 만들어 줍니다. 모의투자는 KRX 만 됩니다.

**Q. 해외주식은요?**
이 라이브러리는 국내주식 API(REST 182개 + 조건검색 + 실시간)만 감쌉니다. 금현물 시세·주문 TR 은 들어 있습니다.

## 주문과 안전

**Q. 주문 코드를 돌려도 안전한가요?**
`is_mock=True` 면 모의투자 서버라 실제 체결이 없습니다. `is_mock=False`(기본값)의 `api.order.*` · `api.credit_order.*` 는
**실계좌에 그대로 주문을 냅니다.** 파이썬 API 에는 이를 막는 장치가 없으니 실전에서는 수량·가격을 한 번 더 확인하는 코드를 두세요.

**Q. 지정가 주문이 거부돼요.**
가격이 호가단위의 배수가 아니면 거부되거나 다른 가격이 됩니다. `round_to_tick()` 으로 맞추세요 — [지정가 주문 레시피](cookbook/limit-order.md).

## AI 에이전트·MCP

**Q. Claude Code · Cursor 에서 쓸 수 있나요?**
두 가지입니다. ① MCP 서버(`pip install 'kiwoom-client[mcp]'`, `kiwoom-client-mcp`)로 엔드포인트를 도구로 직접 부르기.
② AI 가 이 라이브러리로 코드를 쓸 때 참고하는 규칙·스킬(`llms.txt`, `AGENTS.md`, Claude Code 스킬, Cursor·Copilot 규칙) — [AI 코딩 도구에서 쓰기](ai-tools.md).

**Q. MCP 에서 AI 가 마음대로 실주문을 낼 수 있나요?**
실전투자(`KIWOOM_IS_MOCK=false`)에서는 `KIWOOM_MCP_ALLOW_LIVE_ORDERS=true` 를 직접 켜기 전까지 주문 도구가 **등록조차 되지 않습니다.**
모의투자에서는 항상 열려 있습니다.

## 기타

**Q. pandas 없이도 되나요?**
네. `to_dataframe()` 만 pandas 가 필요합니다(`pip install 'kiwoom-client[pandas]'`).

**Q. 버그·요청은 어디에?**
[GitHub Issues](https://github.com/younghwan91/kiwoom-client/issues). 사용법 질문은 [Discussions](https://github.com/younghwan91/kiwoom-client/discussions) 로.
앱키·계좌번호는 지우고 올려 주세요.
