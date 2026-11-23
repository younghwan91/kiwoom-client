"""Build the Claude Desktop bundle (``.mcpb``) of the MCP server.

::

    python scripts/build_mcpb.py                 # 검사 + 검증 + dist/kiwoom-client-<버전>.mcpb
    python scripts/build_mcpb.py --check-only    # 레포 안 검사만 (node·네트워크 불필요)

The bundle is the ``mcpb/`` directory plus the brand icon. It is a ``uv``
server (MCPB manifest 0.4): it ships no server code, the host installs
``kiwoom-client[mcp]==<버전>`` from PyPI on first run. Packing and validation
use the official CLI (``npx @anthropic-ai/mcpb``), so they need Node.js.

Never touches Kiwoom servers or API keys.
"""

from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BUNDLE_DIR = ROOT / "mcpb"
ICON = ROOT / "docs" / "images" / "brand" / "mark-512.png"

#: Official MCPB CLI, pinned so CI does not change under us.
MCPB_CLI = "@anthropic-ai/mcpb@2.1.2"

#: Env vars the bundle must never set: the live-order opt-in stays a manual edit.
FORBIDDEN_ENV = ("KIWOOM_MCP_ALLOW_LIVE_ORDERS",)


def package_version(root: Path = ROOT) -> str:
    text = (root / "pyproject.toml").read_text(encoding="utf-8")
    match = re.search(r'^version\s*=\s*"([^"]+)"', text, re.MULTILINE)
    if match is None:
        raise ValueError("pyproject.toml 에서 version 을 찾지 못했습니다")
    return match.group(1)


def bundle_version(bundle: Path = BUNDLE_DIR) -> tuple[str, str]:
    """(project version, pinned kiwoom-client version) of the bundle's pyproject.toml."""
    text = (bundle / "pyproject.toml").read_text(encoding="utf-8")
    version = re.search(r'^version\s*=\s*"([^"]+)"', text, re.MULTILINE)
    pin = re.search(r'"kiwoom-client\[mcp\]==([^"]+)"', text)
    if version is None or pin is None:
        raise ValueError(
            "mcpb/pyproject.toml 에 version 과 kiwoom-client[mcp]==<버전> 이 있어야 합니다"
        )
    return version.group(1), pin.group(1)


def load_manifest(bundle: Path = BUNDLE_DIR) -> dict:
    return json.loads((bundle / "manifest.json").read_text(encoding="utf-8"))


def check_sources(root: Path = ROOT, bundle: Path = BUNDLE_DIR) -> list[str]:
    """Problems in the bundle sources (empty list = fine). No network."""
    problems: list[str] = []
    version = package_version(root)
    manifest = load_manifest(bundle)
    project_version, pin = bundle_version(bundle)
    for label, value in (
        ("manifest.json version", manifest.get("version")),
        ("mcpb/pyproject.toml version", project_version),
        ("mcpb/pyproject.toml kiwoom-client[mcp]==", pin),
    ):
        if value != version:
            problems.append(f"{label} 가 {value!r} — 패키지 버전 {version!r} 과 같아야 합니다")

    server = manifest.get("server", {})
    entry = server.get("entry_point", "")
    if not (bundle / entry).is_file():
        problems.append(f"entry_point {entry!r} 파일이 없습니다")
    env = server.get("mcp_config", {}).get("env", {})
    user_config = manifest.get("user_config", {})
    for name, value in env.items():
        if name in FORBIDDEN_ENV:
            problems.append(f"번들이 {name} 를 설정하면 안 됩니다(실주문 opt-in 은 수동으로만)")
        for key in re.findall(r"\$\{user_config\.([A-Za-z0-9_]+)\}", value):
            if key not in user_config:
                problems.append(f"env {name} 가 없는 user_config.{key} 를 씁니다")
    for path in bundle.rglob("*"):
        if path.is_file() and path.suffix in {".json", ".toml", ".py"}:
            text = path.read_text(encoding="utf-8")
            for name in FORBIDDEN_ENV:
                if name in text:
                    problems.append(f"{path.relative_to(bundle)} 에 {name} 가 있습니다")
    return problems


def stage(dest: Path, bundle: Path = BUNDLE_DIR) -> Path:
    """Copy the bundle sources and the icon into ``dest`` (created)."""
    ignore = shutil.ignore_patterns(".venv", "__pycache__", "*.pyc", "uv.lock")
    shutil.copytree(bundle, dest, ignore=ignore)
    shutil.copyfile(ICON, dest / "icon.png")
    return dest


def _mcpb(*args: str) -> None:
    npx = shutil.which("npx")
    if npx is None:
        raise SystemExit("npx 가 없습니다 — Node.js 를 설치하거나 --check-only 로 돌리세요")
    subprocess.run([npx, "--yes", MCPB_CLI, *args], check=True)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument(
        "--out", type=Path, default=ROOT / "dist", help="출력 디렉터리 (기본 dist/)"
    )
    parser.add_argument("--check-only", action="store_true", help="레포 안 검사만 (node 불필요)")
    args = parser.parse_args(argv)

    problems = check_sources()
    for problem in problems:
        print(f"error: {problem}", file=sys.stderr)
    if problems:
        return 1
    if args.check_only:
        print("mcpb sources OK")
        return 0

    version = package_version()
    args.out.mkdir(parents=True, exist_ok=True)
    output = args.out.resolve() / f"kiwoom-client-{version}.mcpb"
    with tempfile.TemporaryDirectory() as tmp:
        staged = stage(Path(tmp) / "kiwoom-client")
        _mcpb("validate", str(staged / "manifest.json"))
        _mcpb("pack", str(staged), str(output))
    _mcpb("info", str(output))
    print(output)
    return 0


if __name__ == "__main__":
    sys.exit(main())
