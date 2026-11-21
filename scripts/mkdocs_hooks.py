"""MkDocs 훅 — ``mkdocs.yml`` 의 ``hooks:`` 가 부른다.

1. 레포 루트의 ``llms.txt``·``llms-full.txt`` 를 사이트 루트에도 싣는다. 정본은 레포 루트 파일
   (``scripts/gen_docs.py`` 가 만든다)이고, 사이트에는 빌드할 때 그대로 복사한다 —
   ``docs/`` 에 사본을 두지 않으므로 둘이 어긋날 일이 없다.
2. 한/영 ``hreflang`` 을 검색엔진 규칙에 맞춘다. i18n 플러그인은 영어판(``*.en.md``)이 없는 페이지도
   ``/en/...`` 에 한국어 본문 그대로 만들고(fallback), ``<link rel="alternate" hreflang>`` 를
   상대 URL 로 낸다.
   - 번역이 있는 페이지: hreflang 을 절대 URL 로 바꾸고 ``x-default``(한국어판)를 더한다.
   - 번역이 없는 페이지: 같은 본문이 두 URL 에 있는 셈이라, ``/en/`` 사본의 canonical 을
     한국어판으로 돌리고 양쪽에서 hreflang 을 뺀다. sitemap 에서도 ``/en/`` 사본과
     그 alternate 를 뺀다.
   언어 전환 메뉴(``<a hreflang>``)는 그대로 둔다 — 영어 UI 로 한국어 본문을 보는 길은 남는다.
"""

from __future__ import annotations

import gzip
import re
import shutil
from pathlib import Path
from typing import Any
from urllib.parse import urljoin

try:  # 단위 테스트는 docs extra(mkdocs) 없이 이 파일을 불러온다
    from mkdocs.exceptions import PluginError
except ImportError:  # pragma: no cover
    PluginError = RuntimeError  # type: ignore[misc,assignment]

ROOT = Path(__file__).resolve().parent.parent
#: 사이트 루트(``/llms.txt``)에 올릴 레포 루트 파일.
SITE_ROOT_FILES = ("llms.txt", "llms-full.txt")
#: 기본(한국어) 언어와 번역 언어. mkdocs.yml 의 i18n 설정과 같아야 한다(tests/test_mkdocs_hooks.py).
DEFAULT_LANG = "ko"
OTHER_LANG = "en"
_SUFFIX = f".{OTHER_LANG}.md"

#: Material base.html 이 ``<head>`` 에 내는 줄 그대로.
_ALT_RE = re.compile(r'[ \t]*<link rel="alternate" href="([^"]*)" hreflang="([^"]*)">\n?')
_URL_RE = re.compile(r"[ \t]*<url>.*?</url>\n?", re.S)
_LOC_RE = re.compile(r"<loc>([^<]*)</loc>")
_XHTML_ALT_RE = re.compile(r'[ \t]*<xhtml:link rel="alternate" hreflang="[^"]*" href="[^"]*"/>\n?')


def src_to_url(src_uri: str) -> str:
    """``why.md`` → ``why/``, ``cookbook/index.md`` → ``cookbook/``, ``index.md`` → ``""``.

    mkdocs 의 ``use_directory_urls: true``(기본) 규칙.
    """
    stem = src_uri[: -len(".md")]
    if stem == "index":
        return ""
    if stem.endswith("/index"):
        return stem[: -len("index")]
    return stem + "/"


def has_translation(src_uri: str, docs_dir: Path) -> bool:
    """이 소스 파일(한국어 ``x.md`` 또는 영어 ``x.en.md``)에 다른 언어판이 있나."""
    if src_uri.endswith(_SUFFIX):
        return True
    return (docs_dir / (src_uri[: -len(".md")] + _SUFFIX)).is_file()


def untranslated_urls(docs_dir: Path) -> list[str]:
    """영어판이 없는 한국어 페이지의 URL(사이트 루트 기준, 예 ``cookbook/daily-chart/``)."""
    out = []
    for path in sorted(docs_dir.rglob("*.md")):
        src = path.relative_to(docs_dir).as_posix()
        if src.endswith(_SUFFIX) or has_translation(src, docs_dir):
            continue
        out.append(src_to_url(src))
    return out


def _page_lang(config: Any) -> str:
    return str(config["theme"]["language"])


def _is_fallback(page: Any, config: Any) -> bool:
    """영어 빌드에서 한국어 본문으로 대체된 페이지."""
    return _page_lang(config) == OTHER_LANG and not page.file.src_uri.endswith(_SUFFIX)


def on_page_context(context: Any, page: Any, config: Any, nav: Any) -> Any:
    if page.file and page.file.src_uri.endswith(".md") and _is_fallback(page, config):
        prefix = f"{OTHER_LANG}/"
        url = page.url[len(prefix) :] if page.url.startswith(prefix) else page.url
        page.canonical_url = urljoin(config["site_url"], url)
    return context


def rewrite_alternates(html: str, canonical: str, translated: bool) -> str:
    """``<head>`` 의 hreflang ``<link>`` 를 절대 URL + x-default 로, 번역이 없으면 지운다."""
    found: list[tuple[str, str]] = []

    def collect(m: re.Match[str]) -> str:
        found.append((m.group(2), urljoin(canonical, m.group(1))))
        return ""

    head, sep, body = html.partition("</head>")
    head = _ALT_RE.sub(collect, head)
    if not translated:
        return head + sep + body
    langs = dict(found)
    if set(langs) != {DEFAULT_LANG, OTHER_LANG}:
        raise PluginError(
            f"hreflang 링크를 찾지 못했다({canonical}, {sorted(langs)}) — "
            "Material 템플릿 형식이 바뀌었나?"
        )
    langs["x-default"] = langs[DEFAULT_LANG]
    links = "".join(f'<link rel="alternate" hreflang="{k}" href="{v}">\n' for k, v in langs.items())
    head = head.replace("</title>", "</title>\n" + links, 1) if "</title>" in head else head + links
    return head + sep + body


def on_post_page(output: str, page: Any, config: Any) -> str:
    if not (page.file and page.file.src_uri.endswith(".md") and page.canonical_url):
        return output
    translated = has_translation(page.file.src_uri, Path(config["docs_dir"])) and not _is_fallback(
        page, config
    )
    return rewrite_alternates(output, page.canonical_url, translated)


def rewrite_sitemap(xml: str, site_url: str, untranslated: list[str]) -> str:
    """번역 없는 페이지의 ``/en/`` 사본과 alternate 를 빼고, 번역 있는 쌍엔 x-default 를 더한다."""
    ko = {urljoin(site_url, u) for u in untranslated}
    en_copies = {urljoin(site_url, f"{OTHER_LANG}/{u}") for u in untranslated}

    def fix(m: re.Match[str]) -> str:
        block = m.group(0)
        loc_m = _LOC_RE.search(block)
        loc = loc_m.group(1) if loc_m else ""
        if loc in en_copies:
            return ""
        if loc in ko:
            return _XHTML_ALT_RE.sub("", block)
        default = re.search(rf'hreflang="{DEFAULT_LANG}" href="([^"]*)"', block)
        if default and 'hreflang="x-default"' not in block:
            href = default.group(1)
            x = f'        <xhtml:link rel="alternate" hreflang="x-default" href="{href}"/>\n'
            block = block.replace("    </url>", x + "    </url>", 1)
        return block

    return _URL_RE.sub(fix, xml)


def on_post_build(config: Any, **kwargs: Any) -> None:
    site_dir = Path(config["site_dir"])
    for name in SITE_ROOT_FILES:
        shutil.copyfile(ROOT / name, site_dir / name)
    # i18n 플러그인은 언어마다 같은 site_dir 로 다시 빌드해 sitemap.xml 을 덮어쓴다 —
    # 매 빌드 끝에 고친다(멱등).
    sitemap = site_dir / "sitemap.xml"
    if sitemap.is_file():
        xml = rewrite_sitemap(
            sitemap.read_text(encoding="utf-8"),
            config["site_url"],
            untranslated_urls(Path(config["docs_dir"])),
        )
        sitemap.write_text(xml, encoding="utf-8")
        with (
            open(site_dir / "sitemap.xml.gz", "wb") as raw,
            gzip.GzipFile(filename="sitemap.xml", fileobj=raw, mode="wb", mtime=0) as gz,
        ):
            gz.write(xml.encode("utf-8"))
