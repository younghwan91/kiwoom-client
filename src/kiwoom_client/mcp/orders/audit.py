"""Append-only JSONL audit log of every order attempt through the MCP server.

One line per event:

- ``preview``  — ``order_preview`` built an order (with or without a token)
- ``rejected`` — the order gate refused an order; nothing was sent
- ``sent``     — the order went to Kiwoom (with Kiwoom's ``return_code``/
  ``return_msg``/``ord_no``)
- ``failed``   — the order went to Kiwoom and the call raised

Never written: app key/secret, access token, confirm token. Account numbers
are masked (:mod:`kiwoom_client.mcp.masking`). The file is created ``0600``
in a ``0700`` directory. A write failure is logged and never blocks or
changes an order.
"""

from __future__ import annotations

import json
import logging
import os
from collections.abc import Callable, Mapping
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any

from kiwoom_client.mcp.masking import mask_accounts

logger = logging.getLogger(__name__)

_KST = timezone(timedelta(hours=9))

#: Response fields kept in a ``sent`` line — Kiwoom's verdict, nothing more.
_RESULT_FIELDS = ("return_code", "return_msg", "ord_no", "base_orig_ord_no")


def summarize_response(response: Any) -> dict[str, Any]:
    if not isinstance(response, Mapping):
        return {}
    return {k: response[k] for k in _RESULT_FIELDS if k in response}


class AuditLog:
    def __init__(
        self, path: str | os.PathLike[str], *, now: Callable[[], datetime] | None = None
    ) -> None:
        self.path = Path(path).expanduser()
        self._now = now or (lambda: datetime.now(_KST))

    def record(self, event: str, **fields: Any) -> None:
        line = {"ts": self._now().isoformat(timespec="milliseconds"), "event": event}
        line.update(mask_accounts({k: v for k, v in fields.items() if v is not None}))
        try:
            self.path.parent.mkdir(mode=0o700, parents=True, exist_ok=True)
            fd = os.open(self.path, os.O_WRONLY | os.O_APPEND | os.O_CREAT, 0o600)
            with os.fdopen(fd, "a", encoding="utf-8") as handle:
                handle.write(json.dumps(line, ensure_ascii=False, default=str) + "\n")
        except OSError as exc:
            logger.warning("주문 감사 로그를 쓰지 못했습니다 (%s): %s", self.path, exc)
