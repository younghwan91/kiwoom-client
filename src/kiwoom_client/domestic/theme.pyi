# 자동 생성 — 고치지 말 것. scripts/build_stubs.py 가 spec/catalog.json 으로 만든다.
# 런타임은 .py 그대로(**kwargs). 스텁은 요청 필드를 IDE·mypy 에 알려 줄 뿐이다.
from typing import Any, Generic

from kiwoom_client.base import ClientProtocol, ResponseT

class Theme(Generic[ResponseT]):
    """Wraps all Theme (테마) endpoints under /api/dostk/thme.

    Args:
        client: An authenticated BaseClient (sync) or AsyncBaseClient.
    """

    RESOURCE_URL: str

    def __init__(self, client: ClientProtocol[ResponseT]) -> None: ...

    def theme_component_stocks(
        self,
        cont_yn: str = "N",
        next_key: str = "",
        *,
        date_tp: str = ...,
        thema_grp_cd: str = ...,
        stex_tp: str = ...,
        **kwargs: Any,
    ) -> ResponseT:
        """테마구성종목요청 (Theme Component Stocks)

        api_id ``ka90002`` · 테마구성종목요청 · ``POST /api/dostk/thme``

        Args:
            date_tp: 날짜구분 — 1일 ~ 99일 날짜입력
            thema_grp_cd: 테마그룹코드 (필수) — 테마그룹코드 번호
            stex_tp: 거래소구분 (필수) — 1:KRX, 2:NXT 3.통합
        """
        ...

    def theme_group_list(
        self,
        cont_yn: str = "N",
        next_key: str = "",
        *,
        qry_tp: str = ...,
        stk_cd: str = ...,
        date_tp: str = ...,
        thema_nm: str = ...,
        flu_pl_amt_tp: str = ...,
        stex_tp: str = ...,
        **kwargs: Any,
    ) -> ResponseT:
        """테마그룹별요청 (Theme Group List)

        api_id ``ka90001`` · 테마그룹별요청 · ``POST /api/dostk/thme``

        Args:
            qry_tp: 검색구분 (필수) — 0:전체검색, 1:테마검색, 2:종목검색
            stk_cd: 종목코드 — 검색하려는 종목코드
            date_tp: 날짜구분 (필수) — n일전 (1일 ~ 99일 날짜입력)
            thema_nm: 테마명 — 검색하려는 테마명
            flu_pl_amt_tp: 등락수익구분 (필수) — 1:상위기간수익률, 2:하위기간수익률, 3:상위등락률,
                4:하위등락률
            stex_tp: 거래소구분 (필수) — 1:KRX, 2:NXT 3.통합
        """
        ...
