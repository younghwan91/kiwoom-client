# 자동 생성 — 고치지 말 것. scripts/build_stubs.py 가 spec/catalog.json 으로 만든다.
# 런타임은 .py 그대로(**kwargs). 스텁은 요청 필드를 IDE·mypy 에 알려 줄 뿐이다.
from typing import Any, Generic

from kiwoom_client.base import ClientProtocol, ResponseT

class Order(Generic[ResponseT]):
    """Wraps all Order (주문) endpoints under /api/dostk/ordr.

    Args:
        client: An authenticated BaseClient (sync) or AsyncBaseClient.
    """

    RESOURCE_URL: str

    def __init__(self, client: ClientProtocol[ResponseT]) -> None: ...

    def buy_order(
        self,
        cont_yn: str = "N",
        next_key: str = "",
        *,
        dmst_stex_tp: str = ...,
        stk_cd: str = ...,
        ord_qty: str = ...,
        ord_uv: str = ...,
        trde_tp: str = ...,
        cond_uv: str = ...,
        **kwargs: Any,
    ) -> ResponseT:
        """주식매수주문 (Stock Buy Order)

        api_id ``kt10000`` · 주식 매수주문 · ``POST /api/dostk/ordr``

        Args:
            dmst_stex_tp: 국내거래소구분 (필수) — KRX,NXT,SOR
            stk_cd: 종목코드 (필수)
            ord_qty: 주문수량 (필수) — 단위: 1주
            ord_uv: 주문단가 — 단위: 원
            trde_tp: 매매구분 (필수) — 0:보통 , 3:시장가 , 5:조건부지정가 , 81:장마감후시간외 ,
                61:장시작전시간외, 62:시간외단일가 , 6:최유리지정가 , 7:최우선지정가 , 10:보통(IOC)
                , 13:시장가(IOC) , 16:최유리(IOC) , 20:보통(FOK) , 23:시장가(FOK) , 26:최유리(FOK) ,
                28:스톱지정가,29:중간가,30:중간가(IOC),31:중간가(FOK)
            cond_uv: 조건단가 — 단위: 원
        """
        ...

    def cancel_order(
        self,
        cont_yn: str = "N",
        next_key: str = "",
        *,
        dmst_stex_tp: str = ...,
        orig_ord_no: str = ...,
        stk_cd: str = ...,
        cncl_qty: str = ...,
        **kwargs: Any,
    ) -> ResponseT:
        """주식취소주문 (Stock Cancel Order)

        api_id ``kt10003`` · 주식 취소주문 · ``POST /api/dostk/ordr``

        Args:
            dmst_stex_tp: 국내거래소구분 (필수) — KRX,NXT,SOR
            orig_ord_no: 원주문번호 (필수) — 매수/매도 주문 요청 응답 결과로 받은 7자리 주문번호
            stk_cd: 종목코드 (필수)
            cncl_qty: 취소수량 (필수) — 단위: 1주, '0' 입력시 잔량 전부 취소
        """
        ...

    def gold_spot_buy_order(
        self,
        cont_yn: str = "N",
        next_key: str = "",
        *,
        stk_cd: str = ...,
        ord_qty: str = ...,
        ord_uv: str = ...,
        trde_tp: str = ...,
        **kwargs: Any,
    ) -> ResponseT:
        """금현물 매수주문 (Gold Spot Buy Order)

        api_id ``kt50000`` · 금현물 매수주문 · ``POST /api/dostk/ordr``

        Args:
            stk_cd: 종목코드 (필수) — M04020000 금 99.99_1kg, M04020100 미니금 99.99_100g
            ord_qty: 주문수량 (필수) — 단위: 1주
            ord_uv: 주문단가 — 단위: 원
            trde_tp: 매매구분 (필수) — 00:보통, 10:보통(IOC), 20:보통(FOK)
        """
        ...

    def gold_spot_cancel_order(
        self,
        cont_yn: str = "N",
        next_key: str = "",
        *,
        orig_ord_no: str = ...,
        stk_cd: str = ...,
        cncl_qty: str = ...,
        **kwargs: Any,
    ) -> ResponseT:
        """금현물 취소주문 (Gold Spot Cancel Order)

        api_id ``kt50003`` · 금현물 취소주문 · ``POST /api/dostk/ordr``

        Args:
            orig_ord_no: 원주문번호 (필수) — 매수/매도 주문 요청 응답 결과로 받은 7자리 주문번호
            stk_cd: 종목코드 (필수) — M04020000 금 99.99_1kg, M04020100 미니금 99.99_100g
            cncl_qty: 취소수량 (필수) — 단위: 1주, '0' 입력시 잔량 전부 취소
        """
        ...

    def gold_spot_modify_order(
        self,
        cont_yn: str = "N",
        next_key: str = "",
        *,
        stk_cd: str = ...,
        orig_ord_no: str = ...,
        mdfy_qty: str = ...,
        mdfy_uv: str = ...,
        **kwargs: Any,
    ) -> ResponseT:
        """금현물 정정주문 (Gold Spot Modify Order)

        api_id ``kt50002`` · 금현물 정정주문 · ``POST /api/dostk/ordr``

        Args:
            stk_cd: 종목코드 (필수) — M04020000 금 99.99_1kg, M04020100 미니금 99.99_100g
            orig_ord_no: 원주문번호 (필수)
            mdfy_qty: 정정수량 (필수) — 단위: 1주, '0' 입력시 잔량 전부 정정
            mdfy_uv: 정정단가 (필수) — 단위: 원
        """
        ...

    def gold_spot_sell_order(
        self,
        cont_yn: str = "N",
        next_key: str = "",
        *,
        stk_cd: str = ...,
        ord_qty: str = ...,
        ord_uv: str = ...,
        trde_tp: str = ...,
        **kwargs: Any,
    ) -> ResponseT:
        """금현물 매도주문 (Gold Spot Sell Order)

        api_id ``kt50001`` · 금현물 매도주문 · ``POST /api/dostk/ordr``

        Args:
            stk_cd: 종목코드 (필수) — M04020000 금 99.99_1kg, M04020100 미니금 99.99_100g
            ord_qty: 주문수량 (필수) — 단위: 1주
            ord_uv: 주문단가 — 단위: 원
            trde_tp: 매매구분 (필수) — 00:보통, 10:보통(IOC), 20:보통(FOK)
        """
        ...

    def modify_order(
        self,
        cont_yn: str = "N",
        next_key: str = "",
        *,
        dmst_stex_tp: str = ...,
        orig_ord_no: str = ...,
        stk_cd: str = ...,
        mdfy_qty: str = ...,
        mdfy_uv: str = ...,
        mdfy_cond_uv: str = ...,
        **kwargs: Any,
    ) -> ResponseT:
        """주식정정주문 (Stock Modify Order)

        api_id ``kt10002`` · 주식 정정주문 · ``POST /api/dostk/ordr``

        Args:
            dmst_stex_tp: 국내거래소구분 (필수) — KRX,NXT,SOR
            orig_ord_no: 원주문번호 (필수) — 매수/매도 주문 요청 응답 결과로 받은 7자리 주문번호
            stk_cd: 종목코드 (필수)
            mdfy_qty: 정정수량 (필수) — 단위: 1주, '0' 입력 시 잔량 전부 정정
            mdfy_uv: 정정단가 (필수) — 단위: 원
            mdfy_cond_uv: 정정조건단가 — 단위: 원
        """
        ...

    def sell_order(
        self,
        cont_yn: str = "N",
        next_key: str = "",
        *,
        dmst_stex_tp: str = ...,
        stk_cd: str = ...,
        ord_qty: str = ...,
        ord_uv: str = ...,
        trde_tp: str = ...,
        cond_uv: str = ...,
        **kwargs: Any,
    ) -> ResponseT:
        """주식매도주문 (Stock Sell Order)

        api_id ``kt10001`` · 주식 매도주문 · ``POST /api/dostk/ordr``

        Args:
            dmst_stex_tp: 국내거래소구분 (필수) — KRX,NXT,SOR
            stk_cd: 종목코드 (필수)
            ord_qty: 주문수량 (필수) — 단위: 1주
            ord_uv: 주문단가 — 단위: 원
            trde_tp: 매매구분 (필수) — 0:보통 , 3:시장가 , 5:조건부지정가 , 81:장마감후시간외 ,
                61:장시작전시간외, 62:시간외단일가 , 6:최유리지정가 , 7:최우선지정가 , 10:보통(IOC)
                , 13:시장가(IOC) , 16:최유리(IOC) , 20:보통(FOK) , 23:시장가(FOK) , 26:최유리(FOK) ,
                28:스톱지정가,29:중간가,30:중간가(IOC),31:중간가(FOK)
            cond_uv: 조건단가 — 단위: 원
        """
        ...
