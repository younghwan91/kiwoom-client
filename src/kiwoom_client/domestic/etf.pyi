# 자동 생성 — 고치지 말 것. scripts/build_stubs.py 가 spec/catalog.json 으로 만든다.
# 런타임은 .py 그대로(**kwargs). 스텁은 요청 필드를 IDE·mypy 에 알려 줄 뿐이다.
from typing import Any, Generic

from kiwoom_client.base import ClientProtocol, ResponseT

class ETF(Generic[ResponseT]):
    """Wraps all ETF endpoints under /api/dostk/etf.

    Args:
        client: An authenticated BaseClient (sync) or AsyncBaseClient.
    """

    RESOURCE_URL: str

    def __init__(self, client: ClientProtocol[ResponseT]) -> None: ...

    def daily_execution(
        self,
        cont_yn: str = "N",
        next_key: str = "",
        *,
        stk_cd: str = ...,
        **kwargs: Any,
    ) -> ResponseT:
        """ETF일자별체결요청 (ETF Daily Execution)

        api_id ``ka40008`` · ETF일자별체결요청 · ``POST /api/dostk/etf``

        Args:
            stk_cd: 종목코드 (필수)
        """
        ...

    def daily_trend(
        self,
        cont_yn: str = "N",
        next_key: str = "",
        *,
        stk_cd: str = ...,
        **kwargs: Any,
    ) -> ResponseT:
        """ETF일별추이요청 (ETF Daily Trend)

        api_id ``ka40003`` · ETF일별추이요청 · ``POST /api/dostk/etf``

        Args:
            stk_cd: 종목코드 (필수)
        """
        ...

    def overall_market_price(
        self,
        cont_yn: str = "N",
        next_key: str = "",
        *,
        txon_type: str = ...,
        navpre: str = ...,
        mngmcomp: str = ...,
        txon_yn: str = ...,
        trace_idex: str = ...,
        stex_tp: str = ...,
        **kwargs: Any,
    ) -> ResponseT:
        """ETF전체시세요청 (ETF Overall Market Price)

        api_id ``ka40004`` · ETF전체시세요청 · ``POST /api/dostk/etf``

        Args:
            txon_type: 과세유형 (필수) — 0:전체, 1:비과세, 2:보유기간과세, 3:회사형, 4:외국,
                5:비과세해외(보유기간관세)
            navpre: NAV대비 (필수) — 0:전체, 1:NAV > 전일종가, 2:NAV < 전일종가
            mngmcomp: 운용사 (필수) — 0000:전체, 3020:KODEX(삼성), 3027:KOSEF(키움),
                3191:TIGER(미래에셋), 3228:KINDEX(한국투자), 3023:KStar(KB), 3022:아리랑(한화),
                9999:기타운용사
            txon_yn: 과세여부 (필수) — 0:전체, 1:과세, 2:비과세
            trace_idex: 추적지수 (필수) — 0:전체
            stex_tp: 거래소구분 (필수) — 1:KRX, 2:NXT, 3:통합
        """
        ...

    def return_rate(
        self,
        cont_yn: str = "N",
        next_key: str = "",
        *,
        stk_cd: str = ...,
        etfobjt_idex_cd: str = ...,
        dt: str = ...,
        **kwargs: Any,
    ) -> ResponseT:
        """ETF수익률요청 (ETF Return Rate)

        api_id ``ka40001`` · ETF수익율요청 · ``POST /api/dostk/etf``

        Args:
            stk_cd: 종목코드 (필수)
            etfobjt_idex_cd: ETF대상지수코드 (필수)
            dt: 기간 (필수) — 0:1주, 1:1달, 2:6개월, 3:1년
        """
        ...

    def stock_info(
        self,
        cont_yn: str = "N",
        next_key: str = "",
        *,
        stk_cd: str = ...,
        **kwargs: Any,
    ) -> ResponseT:
        """ETF종목정보요청 (ETF Stock Info)

        api_id ``ka40002`` · ETF종목정보요청 · ``POST /api/dostk/etf``

        Args:
            stk_cd: 종목코드 (필수)
        """
        ...

    def time_nav(
        self,
        cont_yn: str = "N",
        next_key: str = "",
        *,
        stk_cd: str = ...,
        **kwargs: Any,
    ) -> ResponseT:
        """ETF시간대별NAV요청 (ETF Time NAV)

        api_id ``ka40009`` · ETF시간대별NAV현황 · ``POST /api/dostk/etf``

        Args:
            stk_cd: 종목코드 (필수)
        """
        ...

    def time_segment_execution(
        self,
        cont_yn: str = "N",
        next_key: str = "",
        *,
        stk_cd: str = ...,
        **kwargs: Any,
    ) -> ResponseT:
        """ETF시간대별체결요청 (ETF Time Segment Execution)

        api_id ``ka40007`` · ETF시간대별체결요청 · ``POST /api/dostk/etf``

        Args:
            stk_cd: 종목코드 (필수)
        """
        ...

    def time_segment_trend(
        self,
        cont_yn: str = "N",
        next_key: str = "",
        *,
        stk_cd: str = ...,
        **kwargs: Any,
    ) -> ResponseT:
        """ETF시간대별추이요청 (ETF Time Segment Trend)

        api_id ``ka40006`` · ETF시간대별추이요청 · ``POST /api/dostk/etf``

        Args:
            stk_cd: 종목코드 (필수)
        """
        ...

    def time_trend(
        self,
        cont_yn: str = "N",
        next_key: str = "",
        *,
        stk_cd: str = ...,
        **kwargs: Any,
    ) -> ResponseT:
        """ETF시간대별추이요청 (ETF Time Trend)

        api_id ``ka40010`` · ETF시간대별수급현황 · ``POST /api/dostk/etf``

        Args:
            stk_cd: 종목코드 (필수)
        """
        ...
