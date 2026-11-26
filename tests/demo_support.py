"""Helpers for the demo-mode tests (not collected: no ``test_`` prefix)."""

from __future__ import annotations

import ipaddress
import socket

import pytest


class NetworkBlocked(AssertionError):
    """Something in demo mode tried to reach the network."""


def _loopback(address: object) -> bool:
    host = address[0] if isinstance(address, tuple) else address
    try:
        return ipaddress.ip_address(str(host)).is_loopback
    except ValueError:
        return False


@pytest.fixture
def no_network(monkeypatch):
    """Fail any DNS lookup or outbound connection.

    Loopback connects stay allowed only because asyncio's self-pipe on
    Windows is a socketpair built with ``connect('127.0.0.1')``; nothing in
    demo mode listens there, so a demo connection attempt would still fail.
    """
    real_connect = socket.socket.connect
    real_connect_ex = socket.socket.connect_ex

    def blocked(*args, **kwargs):
        raise NetworkBlocked(f"network access in demo mode: {args!r}")

    def connect(self, address):
        if not _loopback(address):
            blocked(address)
        return real_connect(self, address)

    def connect_ex(self, address):
        if not _loopback(address):
            blocked(address)
        return real_connect_ex(self, address)

    monkeypatch.setattr(socket, "create_connection", blocked)
    monkeypatch.setattr(socket, "getaddrinfo", blocked)
    monkeypatch.setattr(socket.socket, "connect", connect)
    monkeypatch.setattr(socket.socket, "connect_ex", connect_ex)
    yield
