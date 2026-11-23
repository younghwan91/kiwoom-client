"""Entry point of the Claude Desktop bundle (.mcpb).

The bundle ships no server code: the host runs this file with ``uv run``,
which installs ``kiwoom-client[mcp]`` from PyPI (version pinned in the
bundle's pyproject.toml) and starts the same CLI as ``kiwoom-client-mcp``.
Configuration arrives as environment variables from the bundle's
``user_config`` (see manifest.json).
"""

from kiwoom_client.mcp.cli import main

if __name__ == "__main__":
    main()
