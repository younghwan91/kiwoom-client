"""Every exception kiwoom-client raises, in one place.

::

    KiwoomError
    ├── KiwoomAuthError              토큰 발급·폐기 실패 (/oauth2/*)
    ├── KiwoomWebSocketError         WebSocket 로그인·프로토콜 실패
    └── KiwoomAPIError               return_code != 0
        ├── KiwoomTokenError         토큰 거부 (return_code 3; 8003/8005/8010/8103)
        │   └── KiwoomServerMismatchError  모의/실전 키·토큰 불일치 (8030/8031)
        ├── KiwoomRateLimitError     호출 한도 초과 (return_code 5; 1700-1702)
        ├── KiwoomRequestError       잘못된 요청 파라미터·헤더 (15xx, 1687)
        │   └── KiwoomStockNotFoundError  종목코드 없음 (1901-1903)
        └── KiwoomUnsupportedError   모의투자·법인 미지원 API (8104/8200)

The subclasses only *narrow* what was already raised: every one of them is a
``KiwoomAPIError`` with the same ``code``/``message``/``response`` as before,
so existing ``except KiwoomAPIError`` blocks catch them unchanged. The extra
``error_code`` attribute holds the 4-digit code Kiwoom embeds in
``return_msg`` (``"...[8005:Token이 유효하지 않습니다]"``).

HTTP failures that survive the built-in retries (429, 401 after a refresh)
still surface as ``httpx.HTTPStatusError``, as before.

Error codes: 키움 REST API 가이드 "오류코드" (https://openapi.kiwoom.com/guide/apiguide).
"""

from __future__ import annotations

from kiwoom_client._errors import KiwoomError, parse_error_code
from kiwoom_client.auth import KiwoomAuthError
from kiwoom_client.base import (
    KiwoomAPIError,
    KiwoomRateLimitError,
    KiwoomRequestError,
    KiwoomServerMismatchError,
    KiwoomStockNotFoundError,
    KiwoomTokenError,
    KiwoomUnsupportedError,
    api_error_class,
)
from kiwoom_client.websocket import KiwoomWebSocketError

__all__ = [
    "KiwoomAPIError",
    "KiwoomAuthError",
    "KiwoomError",
    "KiwoomRateLimitError",
    "KiwoomRequestError",
    "KiwoomServerMismatchError",
    "KiwoomStockNotFoundError",
    "KiwoomTokenError",
    "KiwoomUnsupportedError",
    "KiwoomWebSocketError",
    "api_error_class",
    "parse_error_code",
]
