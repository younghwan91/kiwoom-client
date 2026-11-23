"""Server-enforced order safety for the MCP server.

The live-order opt-in guard (:mod:`kiwoom_client.mcp.guard`) decides whether
order tools exist at all. Everything in this package sits *behind* it and only
adds checks on the tools that remain:

- :mod:`.policy`  — settings read from ``KIWOOM_MCP_*`` environment variables
  (no ``mcp`` import, so the CLI can validate them cheaply)
- :mod:`.confirm` — one-time, expiring confirmation tokens bound to the exact
  order parameters
- :mod:`.gate`    — the single checkpoint every order passes right before it
  is sent

Like the guard, none of this applies to ``KiwoomAPI``/``AsyncKiwoomAPI`` used
directly from Python.
"""
