"""배포 뒤 바뀐 문서 URL 을 IndexNow(Bing·Naver·Yandex 등)에 알린다 — docs-deploy.yml 의 마지막 잡.

    python scripts/indexnow.py --before <sha> --after <sha>     # push: 그 사이 바뀐 페이지만
    python scripts/indexnow.py --all                            # workflow_dispatch: sitemap 전부

키는 비밀이 아니다 — IndexNow 는 사이트 루트의 ``<키>.txt``(내용 = 키)로 소유를 확인한다
(``docs/<키>.txt`` 가 사이트에 실린다). 프로토콜: https://www.indexnow.org/documentation
실패해도 배포는 이미 끝났으므로 워크플로는 이 잡을 continue-on-error 로 둔다.
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path
from urllib.parse import urljoin, urlsplit

ROOT = Path(__file__).resolve().parent.parent
KEY = "e3ce83e7fbaa3bb375ab7015ff03bbd9"
SITE_URL = "https://younghwan91.github.io/kiwoom-client/"
ENDPOINT = "https://api.indexnow.org/indexnow"
#: 이 파일들이 바뀌면 모든 페이지의 <head> 가 바뀐다 → sitemap 전부를 보낸다.
SITE_WIDE = (
    "mkdocs.yml",
    "overrides/",
    "scripts/mkdocs_hooks.py",
    "docs/stylesheets/",
    "docs/.nav.yml",
)
#: 프로토콜 한도(요청 하나에 10,000개).
MAX_URLS = 10_000


def key_location() -> str:
    return urljoin(SITE_URL, f"{KEY}.txt")


def sitemap_urls(xml: str) -> list[str]:
    return re.findall(r"<loc>([^<]+)</loc>", xml)


def doc_url(path: str) -> str | None:
    """``docs/why.md`` → 사이트 URL, ``docs/why.en.md`` → ``/en/why/``. 문서가 아니면 None."""
    if not (path.startswith("docs/") and path.endswith(".md")):
        return None
    rel = path[len("docs/") : -len(".md")]
    prefix = ""
    if rel.endswith(".en"):
        rel, prefix = rel[: -len(".en")], "en/"
    if rel == "index":
        rel = ""
    elif rel.endswith("/index"):
        rel = rel[: -len("index")]
    else:
        rel += "/"
    return urljoin(SITE_URL, prefix + rel)


def select_urls(changed: list[str] | None, sitemap: list[str]) -> list[str]:
    """보낼 URL — sitemap 에 있는 것(정규 URL)만.

    ``changed`` 가 None 이거나 사이트 공통 파일이 바뀌었으면 sitemap 전부.
    """
    if changed is None or any(p.startswith(SITE_WIDE) for p in changed):
        return sitemap[:MAX_URLS]
    wanted = {u for u in map(doc_url, changed) if u}
    return [u for u in sitemap if u in wanted][:MAX_URLS]


def payload(urls: list[str]) -> dict[str, object]:
    return {
        "host": urlsplit(SITE_URL).hostname,
        "key": KEY,
        "keyLocation": key_location(),
        "urlList": urls,
    }


def changed_files(before: str, after: str) -> list[str] | None:
    """두 커밋 사이 바뀐 파일. 비교할 수 없으면(새 브랜치·강제 푸시) None = 전부."""
    if not before or set(before) == {"0"}:
        return None
    try:
        out = subprocess.run(
            ["git", "diff", "--name-only", before, after],
            cwd=ROOT,
            check=True,
            capture_output=True,
            text=True,
        ).stdout
    except subprocess.CalledProcessError:
        return None
    return [line for line in out.splitlines() if line]


def _get(url: str) -> str:
    with urllib.request.urlopen(url, timeout=30) as resp:
        return resp.read().decode("utf-8")


def _wait_for_key(tries: int = 12, delay: float = 10.0) -> bool:
    """방금 배포한 키 파일이 Pages 에 보일 때까지 기다린다(첫 배포·CDN 지연)."""
    for _ in range(tries):
        try:
            if _get(key_location()).strip() == KEY:
                return True
        except urllib.error.URLError:
            pass
        time.sleep(delay)
    return False


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--before", default="")
    ap.add_argument("--after", default="HEAD")
    ap.add_argument("--all", action="store_true")
    args = ap.parse_args(argv)

    changed = None if args.all else changed_files(args.before, args.after)
    urls = select_urls(changed, sitemap_urls(_get(urljoin(SITE_URL, "sitemap.xml"))))
    print(f"바뀐 파일 {'전부' if changed is None else len(changed)} → 보낼 URL {len(urls)}개")
    for u in urls:
        print(f"  {u}")
    if not urls:
        return 0
    if not _wait_for_key():
        print(f"키 파일이 아직 안 보인다: {key_location()}")
        return 1
    req = urllib.request.Request(
        ENDPOINT,
        data=json.dumps(payload(urls)).encode("utf-8"),
        headers={"Content-Type": "application/json; charset=utf-8"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            print(f"IndexNow 응답 {resp.status}")
            return 0
    except urllib.error.HTTPError as exc:
        # 200 OK · 202 Accepted(키 확인 대기) 이 정상. 400·403·422·429 는 원인을 남기고 실패.
        print(f"IndexNow 응답 {exc.code}: {exc.read().decode('utf-8', 'replace')[:300]}")
        return 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
