"""Root of the library's exception hierarchy (no imports, so anyone can use it).

The public view of the whole hierarchy is :mod:`kiwoom_client.errors`.
"""

from __future__ import annotations

import re

__all__ = ["KiwoomError", "describe_server", "error_hint", "parse_error_code"]


class KiwoomError(Exception):
    """Base class of every error kiwoom-client raises on purpose.

    ``except KiwoomError`` catches API errors, token errors and WebSocket
    errors alike. Subclassing it changes nothing for code that already
    catches ``KiwoomAPIError``, ``KiwoomAuthError`` or ``Exception``.
    """


# Kiwoom puts its 4-digit error code inside return_msg, e.g.
#   "인증에 실패했습니다[8005:Token이 유효하지 않습니다]"
_ERROR_CODE = re.compile(r"\[\s*(\d{4})\s*:")


def parse_error_code(message: object) -> int | None:
    """Pull Kiwoom's 4-digit error code (``[8005:...]``) out of a message."""
    if not isinstance(message, str):
        return None
    match = _ERROR_CODE.search(message)
    return int(match.group(1)) if match else None


_PROD_HOST = "api.kiwoom.com"
_MOCK_HOST = "mockapi.kiwoom.com"


def describe_server(base_url: str | None) -> str | None:
    """Human description of the server a client talks to, or None if unknown."""
    if not base_url:
        return None
    if _MOCK_HOST in base_url:
        return f"모의투자 서버({_MOCK_HOST}, is_mock=True)"
    if _PROD_HOST in base_url:
        return f"실전투자 서버({_PROD_HOST}, is_mock=False)"
    return base_url


def _mismatch_hint(base_url: str | None) -> str:
    server = describe_server(base_url)
    if server is None:
        return "모의투자 키와 실전투자 키는 서로 다릅니다 — is_mock 을 키 종류에 맞추세요."
    if _MOCK_HOST in server:
        other = "실전투자 키라면 is_mock=False"
    elif _PROD_HOST in server:
        other = "모의투자 키라면 is_mock=True"
    else:
        other = "키 종류에 맞는 서버를 쓰세요"
    return f"지금 {server}에 연결돼 있습니다. {other} (KIWOOM_IS_MOCK) 로 바꾸세요."


def error_hint(
    error_code: int | None,
    return_code: object = None,
    base_url: str | None = None,
) -> str | None:
    """A one-line next step for a Kiwoom error, or None when there is nothing to add.

    Hints only add advice — they never change which exception is raised.
    """
    if error_code in (8030, 8031):
        return _mismatch_hint(base_url)
    if error_code in (8001, 8002):
        server = describe_server(base_url)
        where = f" 지금 {server}에 연결돼 있습니다." if server else ""
        return (
            "앱키·시크릿키가 맞는지, 키 종류(모의/실전)와 is_mock 이 짝인지 확인하세요." + where
        )
    if error_code == 8010:
        return (
            "토큰을 발급받은 IP 와 요청한 IP 가 다릅니다 — "
            "프록시·NAT·여러 서버 공유 여부를 확인하세요."
        )
    if error_code == 8104:
        return (
            "모의투자 서버에서 지원하지 않는 API 입니다 — "
            "실전투자 서버에서만 호출할 수 있습니다."
        )
    if error_code in (1700, 1701, 1702) or return_code == 5:
        return (
            "호출 한도를 넘었습니다 — rate_limit 을 낮추거나, 같은 앱키로 여러 프로세스가 "
            "같은 TR 을 동시에 부르지 않는지 확인하세요."
        )
    if error_code in (1901, 1902, 1903):
        return (
            "종목코드를 확인하세요. NXT/SOR 은 005930_NX / 005930_AL 형식입니다 "
            "(kiwoom_client.codes.exchange_stock_code)."
        )
    if error_code in (8005, 8003, 8103) or return_code == 3:
        return (
            "토큰이 거부됐습니다(자동 재발급 후에도 실패). is_mock 과 키 종류가 짝인지, "
            "다른 곳에서 토큰을 폐기하지 않았는지 확인하세요."
        )
    return None
