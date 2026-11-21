# 자동 생성 — 고치지 말 것. scripts/build_stubs.py 가 spec/catalog.json 으로 만든다.
# 런타임은 .py 그대로(**kwargs). 스텁은 요청 필드를 IDE·mypy 에 알려 줄 뿐이다.
from typing import Any, Generic

from kiwoom_client.base import ClientProtocol, ResponseT

class ELW(Generic[ResponseT]):
    """Wraps all ELW endpoints under /api/dostk/elw.

    Args:
        client: An authenticated BaseClient (sync) or AsyncBaseClient.
    """

    RESOURCE_URL: str

    def __init__(self, client: ClientProtocol[ResponseT]) -> None: ...

    def change_rate_ranking(
        self,
        cont_yn: str = "N",
        next_key: str = "",
        *,
        sort_tp: str = ...,
        rght_tp: str = ...,
        trde_end_skip: str = ...,
        **kwargs: Any,
    ) -> ResponseT:
        """ELW등락율순위요청 (ELW Change Rate Ranking)

        api_id ``ka30009`` · ELW등락율순위요청 · ``POST /api/dostk/elw``

        Args:
            sort_tp: 정렬구분 (필수)
            rght_tp: 권리구분 (필수)
            trde_end_skip: 거래종료제외 (필수)
        """
        ...

    def condition_search(
        self,
        cont_yn: str = "N",
        next_key: str = "",
        *,
        isscomp_cd: str = ...,
        bsis_aset_cd: str = ...,
        rght_tp: str = ...,
        lpcd: str = ...,
        sort_tp: str = ...,
        **kwargs: Any,
    ) -> ResponseT:
        """ELW조건검색요청 (ELW Condition Search)

        api_id ``ka30005`` · ELW조건검색요청 · ``POST /api/dostk/elw``

        Args:
            isscomp_cd: 발행사코드 (필수)
            bsis_aset_cd: 기초자산코드 (필수)
            rght_tp: 권리구분 (필수)
            lpcd: LP코드 (필수)
            sort_tp: 정렬구분 (필수)
        """
        ...

    def daily_sensitivity_indicator(
        self,
        cont_yn: str = "N",
        next_key: str = "",
        *,
        stk_cd: str = ...,
        **kwargs: Any,
    ) -> ResponseT:
        """ELW일별민감도지표요청 (ELW Daily Sensitivity Indicator)

        api_id ``ka10048`` · ELW일별민감도지표요청 · ``POST /api/dostk/elw``

        Args:
            stk_cd: 종목코드 (필수)
        """
        ...

    def detailed_stock_info(
        self,
        cont_yn: str = "N",
        next_key: str = "",
        *,
        stk_cd: str = ...,
        **kwargs: Any,
    ) -> ResponseT:
        """ELW종목상세정보요청 (ELW Detailed Stock Info)

        api_id ``ka30012`` · ELW종목상세정보요청 · ``POST /api/dostk/elw``

        Args:
            stk_cd: 종목코드 (필수)
        """
        ...

    def lp_daily_holding_trend(
        self,
        cont_yn: str = "N",
        next_key: str = "",
        *,
        bsis_aset_cd: str = ...,
        base_dt: str = ...,
        **kwargs: Any,
    ) -> ResponseT:
        """ELW LP일별보유추이요청 (ELW LP Daily Holding Trend)

        api_id ``ka30003`` · ELWLP보유일별추이요청 · ``POST /api/dostk/elw``

        Args:
            bsis_aset_cd: 기초자산코드 (필수)
            base_dt: 기준일자 (필수)
        """
        ...

    def order_volume_ranking(
        self,
        cont_yn: str = "N",
        next_key: str = "",
        *,
        sort_tp: str = ...,
        rght_tp: str = ...,
        trde_end_skip: str = ...,
        **kwargs: Any,
    ) -> ResponseT:
        """ELW호가잔량순위요청 (ELW Order Volume Ranking)

        api_id ``ka30010`` · ELW잔량순위요청 · ``POST /api/dostk/elw``

        Args:
            sort_tp: 정렬구분 (필수)
            rght_tp: 권리구분 (필수)
            trde_end_skip: 거래종료제외 (필수)
        """
        ...

    def premium_rate(
        self,
        cont_yn: str = "N",
        next_key: str = "",
        *,
        isscomp_cd: str = ...,
        bsis_aset_cd: str = ...,
        rght_tp: str = ...,
        lpcd: str = ...,
        trde_end_elwskip: str = ...,
        **kwargs: Any,
    ) -> ResponseT:
        """ELW괴리율요청 (ELW Premium Rate)

        api_id ``ka30004`` · ELW괴리율요청 · ``POST /api/dostk/elw``

        Args:
            isscomp_cd: 발행사코드 (필수)
            bsis_aset_cd: 기초자산코드 (필수)
            rght_tp: 권리구분 (필수)
            lpcd: LP코드 (필수)
            trde_end_elwskip: 거래종료ELW제외 (필수)
        """
        ...

    def price_spike(
        self,
        cont_yn: str = "N",
        next_key: str = "",
        *,
        flu_tp: str = ...,
        tm_tp: str = ...,
        tm: str = ...,
        trde_qty_tp: str = ...,
        isscomp_cd: str = ...,
        bsis_aset_cd: str = ...,
        rght_tp: str = ...,
        lpcd: str = ...,
        trde_end_elwskip: str = ...,
        **kwargs: Any,
    ) -> ResponseT:
        """ELW급등락요청 (ELW Price Spike)

        api_id ``ka30001`` · ELW가격급등락요청 · ``POST /api/dostk/elw``

        Args:
            flu_tp: 등락구분 (필수)
            tm_tp: 시간구분 (필수)
            tm: 시간 (필수)
            trde_qty_tp: 거래량구분 (필수)
            isscomp_cd: 발행사코드 (필수)
            bsis_aset_cd: 기초자산코드 (필수)
            rght_tp: 권리구분 (필수)
            lpcd: LP코드 (필수)
            trde_end_elwskip: 거래종료ELW제외 (필수)
        """
        ...

    def proximity_rate(
        self,
        cont_yn: str = "N",
        next_key: str = "",
        *,
        stk_cd: str = ...,
        **kwargs: Any,
    ) -> ResponseT:
        """ELW근접율요청 (ELW Proximity Rate)

        api_id ``ka30011`` · ELW근접율요청 · ``POST /api/dostk/elw``

        Args:
            stk_cd: 종목코드 (필수)
        """
        ...

    def sensitivity_indicator(
        self,
        cont_yn: str = "N",
        next_key: str = "",
        *,
        stk_cd: str = ...,
        **kwargs: Any,
    ) -> ResponseT:
        """ELW민감도지표요청 (ELW Sensitivity Indicator)

        api_id ``ka10050`` · ELW민감도지표요청 · ``POST /api/dostk/elw``

        Args:
            stk_cd: 종목코드 (필수)
        """
        ...

    def top_net_buying_by_broker(
        self,
        cont_yn: str = "N",
        next_key: str = "",
        *,
        isscomp_cd: str = ...,
        trde_qty_tp: str = ...,
        trde_tp: str = ...,
        dt: str = ...,
        trde_end_elwskip: str = ...,
        **kwargs: Any,
    ) -> ResponseT:
        """ELW회원사별순매수상위요청 (ELW Top Net Buying by Broker)

        api_id ``ka30002`` · 거래원별ELW순매매상위요청 · ``POST /api/dostk/elw``

        Args:
            isscomp_cd: 발행사코드 (필수)
            trde_qty_tp: 거래량구분 (필수)
            trde_tp: 매매구분 (필수)
            dt: 기간 (필수)
            trde_end_elwskip: 거래종료ELW제외 (필수)
        """
        ...
