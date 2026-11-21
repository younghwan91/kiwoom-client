"""빌드된 문서 사이트(``site/``)의 검색엔진·SNS 메타를 검사한다.

``mkdocs build --strict`` 는 링크·앵커만 본다. 이 스크립트는 그 뒤에 돌아 각 페이지 ``<head>`` 에
검색 결과·링크 미리보기에 쓰이는 태그가 제대로 나갔는지 확인한다(ci.yml docs 잡, docs-deploy.yml).

    python scripts/check_site_seo.py site

hreflang(절대 URL·ko/en/x-default)과 sitemap(겹침·canonical 일치)도 본다 —
scripts/mkdocs_hooks.py 가 맞춰 둔 것.

문제가 있으면 페이지별로 출력하고 종료 코드 1.
"""

from __future__ import annotations

import json
import re
import sys
from html.parser import HTMLParser
from pathlib import Path

#: 검사하지 않는 HTML(검색 결과 틀·리다이렉트 등).
SKIP = {"404.html", "search.html"}
#: JSON-LD 를 실어야 하는 홈 페이지(사이트 루트 기준).
HOME_PAGES = ("index.html", "en/index.html")


class _Head(HTMLParser):
    """``<head>`` 안의 meta·link·JSON-LD 를 모은다."""

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.meta: dict[str, str] = {}
        self.links: list[dict[str, str]] = []
        self.jsonld: list[str] = []
        self._in_head = False
        self._in_jsonld = False
        self._buf: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        a = {k: (v or "") for k, v in attrs}
        if tag == "head":
            self._in_head = True
        if not self._in_head:
            return
        if tag == "meta":
            key = a.get("property") or a.get("name")
            if key:
                self.meta.setdefault(key, a.get("content", ""))
        elif tag == "link":
            self.links.append(a)
        elif tag == "script" and a.get("type") == "application/ld+json":
            self._in_jsonld = True
            self._buf = []

    def handle_endtag(self, tag: str) -> None:
        if tag == "head":
            self._in_head = False
        elif tag == "script" and self._in_jsonld:
            self._in_jsonld = False
            self.jsonld.append("".join(self._buf))

    def handle_data(self, data: str) -> None:
        if self._in_jsonld:
            self._buf.append(data)


def parse_head(html: str) -> _Head:
    head = _Head()
    head.feed(html)
    return head


def check_page(rel: str, html: str) -> list[str]:
    """페이지 하나의 문제 목록(없으면 빈 리스트)."""
    head = parse_head(html)
    problems: list[str] = []
    m = head.meta

    canonical = next((lk.get("href", "") for lk in head.links if lk.get("rel") == "canonical"), "")
    if not canonical.startswith("https://"):
        problems.append(f"canonical 이 절대 URL 이 아님: {canonical!r}")
    if not m.get("description"):
        problems.append("meta description 없음")
    for key in ("og:title", "og:description", "og:url", "og:image", "og:locale", "twitter:card"):
        if not m.get(key):
            problems.append(f"{key} 없음")
    if m.get("og:url") and m.get("og:url") != canonical:
        problems.append(f"og:url({m.get('og:url')}) 이 canonical({canonical}) 과 다름")
    if m.get("og:image") and not m["og:image"].startswith("https://"):
        problems.append(f"og:image 가 절대 URL 이 아님: {m['og:image']!r}")
    if m.get("og:locale") and not re.fullmatch(r"[a-z]{2}_[A-Z]{2}", m["og:locale"]):
        problems.append(f"og:locale 형식이 틀림: {m['og:locale']!r}")
    if m.get("twitter:card") and m["twitter:card"] != "summary_large_image":
        problems.append(f"twitter:card 가 summary_large_image 가 아님: {m['twitter:card']!r}")

    hreflang = {
        lk.get("hreflang", ""): lk.get("href", "")
        for lk in head.links
        if lk.get("rel") == "alternate"
    }
    hreflang.pop("", None)
    if hreflang:
        if set(hreflang) != {"ko", "en", "x-default"}:
            problems.append(f"hreflang 은 ko·en·x-default 세트여야 함: {sorted(hreflang)}")
        problems += [
            f"hreflang {k} 가 절대 URL 이 아님: {v!r}"
            for k, v in hreflang.items()
            if not v.startswith("https://")
        ]
        if canonical not in hreflang.values():
            problems.append("hreflang 에 자기 자신(canonical)이 없음")

    if rel in HOME_PAGES:
        problems += _check_jsonld(head.jsonld)
    elif head.jsonld:
        problems.append("홈이 아닌 페이지에 JSON-LD 가 있음")
    return problems


def _check_jsonld(blocks: list[str]) -> list[str]:
    if len(blocks) != 1:
        return [f"JSON-LD 블록이 {len(blocks)}개(1개여야 함)"]
    try:
        data = json.loads(blocks[0])
    except json.JSONDecodeError as exc:
        return [f"JSON-LD 가 JSON 이 아님: {exc}"]
    nodes = {n.get("@type"): n for n in data.get("@graph", [])}
    problems = []
    app = nodes.get("SoftwareApplication")
    code = nodes.get("SoftwareSourceCode")
    if not app or not code:
        return ["JSON-LD 에 SoftwareApplication·SoftwareSourceCode 가 다 있어야 함"]
    for node, keys in (
        (app, ("name", "description", "applicationCategory", "offers", "license")),
        (code, ("name", "description", "codeRepository", "programmingLanguage", "license")),
    ):
        problems += [f"JSON-LD {node['@type']}.{k} 없음" for k in keys if not node.get(k)]
    return problems


def check_site(site: Path) -> dict[str, list[str]]:
    """사이트 전체를 검사해 ``{상대경로: 문제 목록}`` (문제 있는 페이지만)."""
    if not (site / "index.html").is_file():
        return {"index.html": ["사이트 루트에 index.html 이 없음 — 빌드를 먼저"]}
    out: dict[str, list[str]] = {}
    canonicals: dict[str, str] = {}
    for path in sorted(site.rglob("*.html")):
        rel = path.relative_to(site).as_posix()
        if rel in SKIP or rel.startswith("assets/"):
            continue
        html = path.read_text(encoding="utf-8")
        canonicals[rel] = next(
            (lk.get("href", "") for lk in parse_head(html).links if lk.get("rel") == "canonical"),
            "",
        )
        problems = check_page(rel, html)
        if problems:
            out[rel] = problems
    sitemap = site / "sitemap.xml"
    if sitemap.is_file():
        problems = check_sitemap(
            sitemap.read_text(encoding="utf-8"), canonicals["index.html"], canonicals
        )
        if problems:
            out["sitemap.xml"] = problems
    return out


def check_sitemap(xml: str, root: str, canonicals: dict[str, str]) -> list[str]:
    """sitemap 의 URL 은 겹치지 않고, 각각 실제 페이지이며 그 canonical 이 자기 자신이어야 한다.

    (영어판이 없어 한국어 본문으로 대체된 ``/en/`` 사본은 canonical 이 한국어판이라
    sitemap 에 있으면 안 된다.)
    """
    locs = re.findall(r"<loc>([^<]*)</loc>", xml)
    problems = [
        f"sitemap 에 같은 URL 이 두 번: {u}" for u in sorted({u for u in locs if locs.count(u) > 1})
    ]
    for loc in locs:
        if not loc.startswith(root):
            problems.append(f"sitemap URL 이 사이트 밖: {loc}")
            continue
        rel = loc[len(root) :] + "index.html"
        if rel not in canonicals:
            problems.append(f"sitemap URL 에 해당하는 페이지가 없음: {loc}")
        elif canonicals[rel] != loc:
            problems.append(f"sitemap URL 의 canonical 이 다른 곳: {loc} → {canonicals[rel]}")
    return problems


def main(argv: list[str]) -> int:
    site = Path(argv[1] if len(argv) > 1 else "site")
    bad = check_site(site)
    for rel, problems in bad.items():
        for p in problems:
            print(f"{rel}: {p}")
    pages = sum(1 for _ in site.rglob("*.html"))
    print(f"검사한 HTML {pages}개, 문제 있는 페이지 {len(bad)}개")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
