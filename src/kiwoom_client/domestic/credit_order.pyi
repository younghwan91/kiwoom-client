# 자동 생성 — 고치지 말 것. scripts/build_stubs.py 가 spec/catalog.json 으로 만든다.
# 런타임은 .py 그대로(**kwargs). 스텁은 요청 필드를 IDE·mypy 에 알려 줄 뿐이다.
from typing import Any, Generic

from kiwoom_client.base import ClientProtocol, ResponseT

class CreditOrder(Generic[ResponseT]):
    """Wraps all Credit Order (신용주문) endpoints under /api/dostk/crdordr.

    Args:
        client: An authenticated BaseClient (sync) or AsyncBaseClient.
    """

    RESOURCE_URL: str

    def __init__(self, client: ClientProtocol[ResponseT]) -> None: ...

    def margin_buy_order(
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
        """신용매수주문 (Credit Margin Buy Order)

        api_id ``kt10006`` · 신용 매수주문 · ``POST /api/dostk/crdordr``

        Args:
            dmst_stex_tp: 국내거래소구분 (필수)
            stk_cd: 종목코드 (필수)
            ord_qty: 주문수량 (필수)
            ord_uv: 주문단가
            trde_tp: 매매구분 (필수)
            cond_uv: 조건단가
        """
        ...

    def margin_cancel_order(
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
        """신용취소주문 (Credit Margin Cancel Order)

        api_id ``kt10009`` · 신용 취소주문 · ``POST /api/dostk/crdordr``

        Args:
            dmst_stex_tp: 국내거래소구분 (필수)
            orig_ord_no: 원주문번호 (필수)
            stk_cd: 종목코드 (필수)
            cncl_qty: 취소수량 (필수)
        """
        ...

    def margin_modify_order(
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
        """신용정정주문 (Credit Margin Modify Order)

        api_id ``kt10008`` · 신용 정정주문 · ``POST /api/dostk/crdordr``

        Args:
            dmst_stex_tp: 국내거래소구분 (필수)
            orig_ord_no: 원주문번호 (필수)
            stk_cd: 종목코드 (필수)
            mdfy_qty: 정정수량 (필수)
            mdfy_uv: 정정단가 (필수)
            mdfy_cond_uv: 정정조건단가
        """
        ...

    def margin_sell_order(
        self,
        cont_yn: str = "N",
        next_key: str = "",
        *,
        dmst_stex_tp: str = ...,
        stk_cd: str = ...,
        ord_qty: str = ...,
        ord_uv: str = ...,
        trde_tp: str = ...,
        crd_deal_tp: str = ...,
        crd_loan_dt: str = ...,
        cond_uv: str = ...,
        **kwargs: Any,
    ) -> ResponseT:
        """신용매도주문 (Credit Margin Sell Order)

        api_id ``kt10007`` · 신용 매도주문 · ``POST /api/dostk/crdordr``

        Args:
            dmst_stex_tp: 국내거래소구분 (필수)
            stk_cd: 종목코드 (필수)
            ord_qty: 주문수량 (필수)
            ord_uv: 주문단가
            trde_tp: 매매구분 (필수)
            crd_deal_tp: 신용거래구분 (필수)
            crd_loan_dt: 대출일
            cond_uv: 조건단가
        """
        ...
