#!/usr/bin/env bash
# 배포물(sdist·wheel) 스모크 — 레포 체크아웃이 아니라 빌드한 wheel 을 깨끗한 venv 에 설치해서 본다.
# 키·네트워크(키움 서버) 없이 끝난다. CI `build` 잡이 부르고, 로컬에서도 그대로 돌릴 수 있다:
#
#     bash scripts/check_dist.sh
#
# 필요: uv. 산출물은 임시 디렉터리에만 만든다(dist/ 를 건드리지 않는다).
set -euo pipefail

root="$(cd "$(dirname "$0")/.." && pwd)"
work="$(mktemp -d)"
trap 'rm -rf "$work"' EXIT

echo "== build (sdist + wheel)"
uv build --quiet --out-dir "$work/dist" "$root"
whl="$(ls "$work"/dist/*.whl)"

echo "== twine check --strict (PyPI README 렌더링 포함)"
uvx --quiet twine check --strict "$work"/dist/*

echo "== wheel 내용"
python3 -m zipfile -l "$whl" > "$work/files.txt"
for f in kiwoom_client/py.typed kiwoom_client/mcp/server.py; do
  grep -q "^$f " "$work/files.txt" || { echo "::error::wheel 에 $f 가 없다"; exit 1; }
done
if grep -qE '^(tests|examples|docs|scripts)/' "$work/files.txt"; then
  echo "::error::wheel 에 tests/·examples/·docs/·scripts/ 가 들어갔다"; exit 1
fi

# 레포 밖 디렉터리에서 import 해야 체크아웃이 아니라 설치본을 본다.
cd "$work"

echo "== 기본 의존성만으로 설치 후 import"
uv venv --quiet "$work/core"
uv pip install --quiet --python "$work/core/bin/python" "$whl"
"$work/core/bin/python" - <<'PY'
import kiwoom_client as k
from kiwoom_client import AsyncKiwoomAPI, KiwoomAPI  # noqa: F401

assert k.__file__ and "site-packages" in k.__file__, k.__file__
assert k.__version__ not in ("", "0.0.0"), k.__version__
print("kiwoom_client", k.__version__, "from", k.__file__)
PY

echo "== [mcp] extra 설치 후 kiwoom-client-mcp 엔트리포인트"
uv venv --quiet "$work/mcp"
uv pip install --quiet --python "$work/mcp/bin/python" "${whl}[mcp]"
"$work/mcp/bin/python" -c "import kiwoom_client.mcp.server"
# 키 환경변수가 없으면 서버를 띄우지 않고 종료 코드 1 + 안내로 끝나야 한다.
# env -i 로 환경을 비워 어떤 키도 넘어가지 않게 한다.
set +e
env -i PATH="/usr/bin:/bin" "$work/mcp/bin/kiwoom-client-mcp" </dev/null 2>"$work/err.txt"
code=$?
set -e
cat "$work/err.txt"
test "$code" -eq 1 || { echo "::error::kiwoom-client-mcp 종료 코드 $code (기대 1)"; exit 1; }
grep -q "environment variables must be set" "$work/err.txt"

echo "OK: dist 스모크 통과"
