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
            sort_tp: 정렬구분 (필수) — 1:상승률, 2:상승폭, 3:하락률, 4:하락폭
            rght_tp: 권리구분 (필수) — 000:전체, 001:콜, 002:풋, 003:DC, 004:DP, 006:조기종료콜,
                007:조기종료풋
            trde_end_skip: 거래종료제외 (필수) — 1:거래종료제외, 0:거래종료포함
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
            isscomp_cd: 발행사코드 (필수) — 12자리입력(전체:000000000000, 한국투자증권:000,,,3,
                미래대우:000,,,5, 신영:000,,,6, NK투자증권:000,,,12, KB증권:000,,,17)
            bsis_aset_cd: 기초자산코드 (필수) — 전체일때만 12자리입력(전체:000000000000,
                KOSPI200:201, KOSDAQ150:150, 삼정전자:005930, KT:030200,,)
            rght_tp: 권리구분 (필수) — 0:전체, 1:콜, 2:풋, 3:DC, 4:DP, 5:EX, 6:조기종료콜,
                7:조기종료풋
            lpcd: LP코드 (필수) — 전체일때만 12자리입력(전체:000000000000, 한국투자증권:003,
                미래대우:005, 신영:006, NK투자증권:012, KB증권:017)
            sort_tp: 정렬구분 (필수) — 0:정렬없음, 1:상승율순, 2:상승폭순, 3:하락율순, 4:하락폭순,
                5:거래량순, 6:거래대금순, 7:잔존일순
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
            base_dt: 기준일자 (필수) — YYYYMMDD
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
            sort_tp: 정렬구분 (필수) — 1:순매수잔량상위, 2: 순매도 잔량상위
            rght_tp: 권리구분 (필수) — 000: 전체, 001: 콜, 002: 풋, 003: DC, 004: DP, 006:
                조기종료콜, 007: 조기종료풋
            trde_end_skip: 거래종료제외 (필수) — 1:거래종료제외, 0:거래종료포함
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
            isscomp_cd: 발행사코드 (필수) — 전체:000000000000, 한국투자증권:3, 미래대우:5, 신영:6,
                NK투자증권:12, KB증권:17
            bsis_aset_cd: 기초자산코드 (필수) — 전체:000000000000, KOSPI200:201, KOSDAQ150:150,
                삼성전자:005930, KT:030200..
            rght_tp: 권리구분 (필수) — 000: 전체, 001: 콜, 002: 풋, 003: DC, 004: DP, 005: EX, 006:
                조기종료콜, 007: 조기종료풋
            lpcd: LP코드 (필수) — 전체:000000000000, 한국투자증권:3, 미래대우:5, 신영:6,
                NK투자증권:12, KB증권:17
            trde_end_elwskip: 거래종료ELW제외 (필수) — 1:거래종료ELW제외, 0:거래종료ELW포함
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
            flu_tp: 등락구분 (필수) — 1:급등, 2:급락
            tm_tp: 시간구분 (필수) — 1:분전, 2:일전
            tm: 시간 (필수) — 분 혹은 일입력 (예 1, 3, 5)
            trde_qty_tp: 거래량구분 (필수) — 0:전체, 10:만주이상, 50:5만주이상, 100:10만주이상,
                300:30만주이상, 500:50만주이상, 1000:백만주이상
            isscomp_cd: 발행사코드 (필수) — 전체:000000000000, 한국투자증권:3, 미래대우:5, 신영:6,
                NK투자증권:12, KB증권:17
            bsis_aset_cd: 기초자산코드 (필수) — 전체:000000000000, KOSPI200:201, KOSDAQ150:150,
                삼성전자:005930, KT:030200..
            rght_tp: 권리구분 (필수) — 000:전체, 001:콜, 002:풋, 003:DC, 004:DP, 005:EX,
                006:조기종료콜, 007:조기종료풋
            lpcd: LP코드 (필수) — 전체:000000000000, 한국투자증권:3, 미래대우:5, 신영:6,
                NK투자증권:12, KB증권:17
            trde_end_elwskip: 거래종료ELW제외 (필수) — 0:포함, 1:제외
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
            isscomp_cd: 발행사코드 (필수) — 3자리, 영웅문4 0273화면참조 (교보:001, 신한금융투자:002,
                한국투자증권:003, 대신:004, 미래대우:005, ,,,)
            trde_qty_tp: 거래량구분 (필수) — 0:전체, 5:5천주, 10:만주, 50:5만주, 100:10만주,
                500:50만주, 1000:백만주
            trde_tp: 매매구분 (필수) — 1:순매수, 2:순매도
            dt: 기간 (필수) — 1:전일, 5:5일, 10:10일, 40:40일, 60:60일
            trde_end_elwskip: 거래종료ELW제외 (필수) — 0:포함, 1:제외
        """
        ...
