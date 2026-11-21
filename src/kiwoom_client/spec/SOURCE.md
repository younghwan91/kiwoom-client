# TR 카탈로그 출처 (`catalog.json`)

`catalog.json` 은 키움 REST API 의 TR(api_id)별 요청·응답 필드 표다. 사람이 손으로 적지 않고
`scripts/build_spec_catalog.py` 가 키움 공식 명세에서 만든다.

## 어디서 왔나

| 항목 | 값 |
|------|----|
| 원천 | 키움증권 공식 저장소 [`Kiwoom-Securities/Kiwoom-REST-API`](https://github.com/Kiwoom-Securities/Kiwoom-REST-API) 의 `kiwoom/_data/kiwoom_api_spec.json` |
| 고정 커밋 | `catalog.json` 의 `source.commit` (스크립트의 `SOURCE_COMMIT`) |
| 같은 내용의 다른 경로 | [키움 REST API 포털](https://openapi.kiwoom.com) 첫 화면의 "API 명세서 다운로드"(`kiwoom-rest-api-spec.json`), 공식 `kwcli`·`kiwoom-spec-mcp` 번들 |
| 범위 | 메뉴가 `국내주식`·`OAuth 인증` 인 TR. 미국주식은 이 라이브러리가 감싸지 않아 뺀다 |

포털의 문서 화면은 JS 로 그리고, 그 화면이 부르는 `POST /guide/getApiInfoListAjax` 는 봇 차단(eversafe)이 걸려
있다. 그래서 공식 저장소에 공개된 같은 명세 파일을 원천으로 쓴다. 문서 파일만 받으며 키움 API 서버
(`api.kiwoom.com`·`mockapi.kiwoom.com`)에는 요청하지 않는다.

## 무엇을 담고 무엇을 버리나

원본 명세 파일은 키움증권 주식회사에 저작권이 있다(원 저장소 `LICENSE.md`: 복제·배포는 사전 서면 동의 필요).
이 레포는 원본 파일을 싣지 않고, API 를 호출하는 데 필요한 **사실 정보만** 뽑아 다시 적는다.

- 담는 것: TR 의 api_id·이름·메뉴 위치·HTTP 메서드·URL, 필드별 ID·한글명·타입·길이·필수 여부
- 버리는 것: 필드 설명(`description`) 원문과 거기서 뽑던 코드값 목록, TR 개요 문장, 요청/응답 예제,
  공통 헤더(`api-id`·`cont-yn`·`next-key`·`authorization` — 라이브러리가 채운다), 오류 코드 표

필드 설명은 짧아도 원문 문장을 거의 그대로 옮기게 되고, 코드값 목록은 그 문장을 쪼갠 것이라 2026-11 에 둘 다
뺐다(이전 카탈로그의 `desc`·`codes`). 한글명은 필드 이름 수준의 사실이라 남긴다. 생성기는 보조 표
(`scripts/spec_supplement.json`)에 그 키가 섞여도 멈춘다(`DROPPED_FIELD_KEYS`), `tests/test_spec_catalog.py` 가
카탈로그에 없는지 본다. `Field.desc`·`Field.codes` 속성은 하위 호환으로 남아 늘 빈 값이다.

필드의 뜻·단위·코드값은 [키움 REST API 포털](https://openapi.kiwoom.com) 문서가 기준이다. 자주 쓰는 코드값
(매매구분·거래소·시장구분 등)은 이 레포가 따로 정리한 `kiwoom_client.codes` Enum 에 있다.

## 출처 수준 (`source`)

| 값 | 뜻 |
|----|----|
| `official` | 위 고정 커밋의 공식 명세에서 그대로 변환 |
| `repo` | 공식 명세에 없는 TR. `scripts/spec_supplement.json` 에 레포 코드·스모크 표에서 확인된 필드만 손으로 적었다. `note` 에 근거가 있다 |

## 스키마 (`schema_version` 1)

```jsonc
{
  "schema_version": 1,
  "source": {"repository": "...", "path": "...", "commit": "...", "portal": "..."},
  "trs": {
    "ka10001": {
      "api_id": "ka10001", "name": "주식기본정보요청", "menu": ["국내주식", "종목정보"],
      "method": "POST", "url": "/api/dostk/stkinfo", "transport": "rest",   // 또는 "websocket"
      "source": "official",
      "request":  [{"id": "stk_cd", "name": "종목코드", "type": "string", "length": 20,
                    "required": true}],
      "response": [{"id": "...", "type": "list"}, {"id": "...", "parent": "<list 필드 id>"}]
    }
  }
}
```

`type` 은 `string`·`list`·`object` 중 하나. `list` 필드의 자식은 `parent` 에 그 필드 id 를 갖는다.

## 다시 만들기

```bash
uv run python scripts/build_spec_catalog.py --download     # SOURCE_COMMIT 고정본을 GitHub 에서 받아 변환
git diff --stat src/kiwoom_client/spec/catalog.json
```

명세를 새 버전으로 올릴 때는 스크립트의 `SOURCE_COMMIT` 을 바꾸고 다시 돌린 뒤, `tests/test_spec_catalog.py` 가
라이브러리 api_id 와 어긋난 곳을 알려 준다.
