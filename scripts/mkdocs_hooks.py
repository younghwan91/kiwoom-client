"""MkDocs 훅 — 레포 루트의 ``llms.txt``·``llms-full.txt`` 를 사이트 루트에도 싣는다.

정본은 레포 루트 파일(``scripts/gen_docs.py`` 가 만든다)이고, 사이트에는 빌드할 때 그대로 복사한다 —
``docs/`` 에 사본을 두지 않으므로 둘이 어긋날 일이 없다. ``mkdocs.yml`` 의 ``hooks:`` 가 부른다.
"""

from __future__ import annotations

import shutil
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent.parent
#: 사이트 루트(``/llms.txt``)에 올릴 레포 루트 파일.
SITE_ROOT_FILES = ("llms.txt", "llms-full.txt")


def on_post_build(config: Any, **kwargs: Any) -> None:
    site_dir = Path(config["site_dir"])
    for name in SITE_ROOT_FILES:
        shutil.copyfile(ROOT / name, site_dir / name)
