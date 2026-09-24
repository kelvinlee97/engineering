"""Build the wiki site (https://wiki.kelvin.ink/) with Quartz.

Copies wiki/ into a staging content directory, adds the few frontmatter keys
Quartz needs without touching the source files, then runs a pinned Quartz
release with the config in site/.

  python scripts/build_site.py stage --output .site-build/content
  python scripts/build_site.py build            # stage + clone Quartz + build
  python scripts/build_site.py check            # every page built, no broken links

Staging changes, per file:
  - reserved index.md / log.md: add a `title` (taken from the link text that
    points at the file from its parent index, since OKF index files carry no
    title of their own) and drop a leading H1 only when it repeats that title;
  - concept pages: add `modified` from `generated.at`, so Quartz shows the
    date the content last changed rather than the checkout time.
"""

from __future__ import annotations

import argparse
import re
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Any

import yaml

QUARTZ_REPO = "https://github.com/jackyzha0/quartz"
QUARTZ_TAG = "v4.5.2"
RESERVED = {"index.md", "log.md"}
ENTRY_RE = re.compile(r"^[*-] \[(?P<title>[^\]]+)\]\((?P<target>[^)\s]+)\)")
LEADING_H1_RE = re.compile(r"\A\s*# [^\n]*\n+")


def split(text: str) -> tuple[dict[str, Any], str]:
    if text.startswith("---\n"):
        end = text.index("\n---\n", 4)
        data = yaml.safe_load(text[4:end]) or {}
        return dict(data), text[end + 5 :]
    return {}, text


def join(data: dict[str, Any], body: str) -> str:
    if not data:
        return body
    return "---\n" + yaml.safe_dump(data, sort_keys=False, allow_unicode=True) + "---\n" + body


def _iso(value: Any) -> str:
    if hasattr(value, "strftime"):
        return str(value.strftime("%Y-%m-%dT%H:%M:%SZ"))
    return str(value)


def reserved_titles(wiki: Path) -> dict[Path, str]:
    """Map each reserved file to the link text its parent index uses for it."""
    titles: dict[Path, str] = {}
    for index in wiki.rglob("index.md"):
        for line in index.read_text(encoding="utf-8").splitlines():
            m = ENTRY_RE.match(line.strip())
            if not m or re.match(r"^[a-z][a-z0-9+.-]*:", m.group("target")):
                continue
            target = (index.parent / m.group("target")).resolve()
            if target.is_dir():
                target = target / "index.md"
            if target.name in RESERVED:
                titles[target] = m.group("title")
    return titles


def stage(wiki: Path, out: Path, site_title: str) -> int:
    if out.exists():
        shutil.rmtree(out)
    titles = reserved_titles(wiki)
    count = 0
    for src in sorted(wiki.rglob("*")):
        if src.is_dir():
            continue
        dest = out / src.relative_to(wiki)
        dest.parent.mkdir(parents=True, exist_ok=True)
        if src.suffix != ".md":
            shutil.copy2(src, dest)
            continue
        data, body = split(src.read_text(encoding="utf-8"))
        if src.name in RESERVED:
            fallback = site_title if src.parent == wiki else src.parent.name
            data["title"] = titles.get(src.resolve(), fallback)
            h1 = LEADING_H1_RE.match(body)
            if h1 and h1.group(0).strip()[2:].strip() == data["title"]:
                body = body[h1.end() :]
        else:
            generated = data.get("generated")
            if isinstance(generated, dict) and generated.get("at"):
                data["modified"] = _iso(generated["at"])
        dest.write_text(join(data, body), encoding="utf-8")
        count += 1
    return count


def build(repo: Path, work: Path, output: Path) -> None:
    content = work / "content"
    quartz = work / "quartz"
    pages = stage(repo / "wiki", content, "Engineering Wiki")
    print(f"staged {pages} pages in {content}")
    if not (quartz / "package.json").exists():
        subprocess.run(
            ["git", "clone", "--quiet", "--depth", "1", "--branch", QUARTZ_TAG, QUARTZ_REPO,
             str(quartz)],
            check=True,
        )
        subprocess.run(["npm", "ci", "--no-audit", "--no-fund"], cwd=quartz, check=True)
    for name in ("quartz.config.ts", "quartz.layout.ts"):
        shutil.copy2(repo / "site" / name, quartz / name)
    subprocess.run(
        ["npx", "quartz", "build", "-d", str(content.resolve()), "-o", str(output.resolve())],
        cwd=quartz,
        check=True,
    )


HREF_RE = re.compile(r'(?:href|src)="(?P<url>[^"#?]*)[^"]*"')


def _page_slug(rel: Path) -> str:
    return rel.with_suffix("").as_posix()


def check(wiki: Path, public: Path) -> list[str]:
    """Return problems: wiki pages with no HTML output, and internal links to nothing."""
    problems: list[str] = []
    for src in sorted(wiki.rglob("*.md")):
        slug = _page_slug(src.relative_to(wiki))
        if not (public / f"{slug}.html").exists():
            problems.append(f"{slug}: no page in the build output")
    for html in sorted(public.rglob("*.html")):
        text = html.read_text(encoding="utf-8")
        for m in HREF_RE.finditer(text):
            url = m.group("url")
            if not url or re.match(r"^(?:[a-z][a-z0-9+.-]*:|//)", url):
                continue
            target = (public / url.lstrip("/")) if url.startswith("/") else (html.parent / url)
            candidates = [target, Path(f"{target}.html"), target / "index.html"]
            if not any(c.exists() for c in candidates):
                problems.append(f"{html.relative_to(public)}: broken link {url}")
    return sorted(set(problems))


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    sub = parser.add_subparsers(dest="command", required=True)
    p_stage = sub.add_parser("stage", help="stage wiki/ as Quartz content")
    p_stage.add_argument("--output", type=Path, default=Path(".site-build/content"))
    p_build = sub.add_parser("build", help="stage, fetch Quartz, and build the site")
    p_build.add_argument("--work", type=Path, default=Path(".site-build"))
    p_build.add_argument("--output", type=Path, default=Path(".site-build/public"))
    p_check = sub.add_parser("check", help="check the build output")
    p_check.add_argument("--output", type=Path, default=Path(".site-build/public"))
    args = parser.parse_args(argv)
    if args.command == "stage":
        print(f"staged {stage(Path('wiki'), args.output, 'Engineering Wiki')} pages")
    elif args.command == "build":
        build(Path.cwd(), args.work, args.output)
    else:
        problems = check(Path("wiki"), args.output)
        for problem in problems:
            print(f"error: {problem}")
        pages = sum(1 for _ in args.output.rglob("*.html"))
        print(f"{pages} HTML files, {len(problems)} problems")
        return 1 if problems else 0
    return 0


if __name__ == "__main__":
    sys.exit(main())
