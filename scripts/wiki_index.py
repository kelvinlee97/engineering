"""Regenerate the wiki's index.md files from page frontmatter.

  python scripts/wiki_index.py          # rewrite the indexes in place
  python scripts/wiki_index.py --check  # exit 1 if any index is out of date

Rules:
  - The root index keeps everything above its first type section (the title,
    intro, and navigation list) and regenerates the type sections below it,
    listing every page in the wiki.
  - Each directory that directly holds pages gets an index listing those pages,
    grouped by `type` in the vocabulary order.
  - A directory that only holds subdirectories (such as wiki/engineering/) is
    written by hand, because its entries describe domains; this script only
    fails if a subdirectory has no entry there.
Entry format and descriptions follow OKF v0.2 and CLAUDE.md:
`* [title](relative/path.md) - description`.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path
from typing import Any

from scripts.wiki_check import RESERVED, split_frontmatter

TYPE_ORDER = [
    "Concept",
    "Pattern",
    "Playbook",
    "Tool",
    "Service",
    "Configuration",
    "Command",
    "Comparison",
    "Synthesis",
    "Source Summary",
]


def load_pages(wiki: Path) -> dict[Path, dict[str, Any]]:
    pages: dict[Path, dict[str, Any]] = {}
    for path in sorted(wiki.rglob("*.md")):
        if path.name in RESERVED:
            continue
        data, _, err = split_frontmatter(path.read_text(encoding="utf-8"))
        if err or data is None:
            raise SystemExit(f"{path}: unreadable frontmatter; run wiki_check.py first")
        pages[path] = data
    return pages


def grouped(pages: list[tuple[Path, dict[str, Any]]], base: Path) -> str:
    types = TYPE_ORDER + sorted({str(d["type"]) for _, d in pages} - set(TYPE_ORDER))
    sections = []
    for type_ in types:
        entries = [
            f"* [{d['title']}]({p.relative_to(base).as_posix()}) - {d['description']}"
            for p, d in sorted(pages, key=lambda item: str(item[1]["title"]).lower())
            if d["type"] == type_
        ]
        if entries:
            sections.append(f"# {type_}\n\n" + "\n".join(entries) + "\n")
    return "\n".join(sections)


def root_head(text: str) -> str:
    """Everything above the first `# <Type>` section of the root index."""
    pattern = r"(?m)^# (?:" + "|".join(re.escape(t) for t in TYPE_ORDER) + r")\s*$"
    match = re.search(pattern, text)
    return (text[: match.start()] if match else text).rstrip() + "\n\n"


def render(wiki: Path) -> tuple[dict[Path, str], list[str]]:
    pages = load_pages(wiki)
    items = list(pages.items())
    out: dict[Path, str] = {}
    problems: list[str] = []
    root = wiki / "index.md"
    out[root] = root_head(root.read_text(encoding="utf-8")) + grouped(items, wiki)
    for directory in sorted({p.parent for p in pages} - {wiki}):
        local = [(p, d) for p, d in items if p.parent == directory]
        out[directory / "index.md"] = grouped(local, directory)
    for directory in sorted(d for d in wiki.rglob("*") if d.is_dir()):
        if any(p.parent == directory for p in pages) or directory == wiki:
            continue
        index = directory / "index.md"
        listed = index.read_text(encoding="utf-8") if index.exists() else ""
        for sub in sorted(s for s in directory.iterdir() if s.is_dir()):
            if f"]({sub.name}/)" not in listed:
                problems.append(f"{index.relative_to(wiki)}: add an entry for {sub.name}/")
    return out, problems


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--wiki", type=Path, default=Path("wiki"))
    parser.add_argument("--check", action="store_true", help="report stale indexes only")
    args = parser.parse_args(argv)
    out, problems = render(args.wiki)
    stale = [
        p for p, text in out.items() if not p.exists() or p.read_text(encoding="utf-8") != text
    ]
    if not args.check:
        for path in stale:
            path.write_text(out[path], encoding="utf-8")
    for problem in problems:
        print(f"error: {problem}")
    verb = "stale" if args.check else "rewrote"
    for path in stale:
        print(f"{verb}: {path.relative_to(args.wiki)}")
    print(f"{len(out)} indexes, {len(stale)} {verb}, {len(problems)} problems")
    return 1 if problems or (args.check and stale) else 0


if __name__ == "__main__":
    sys.exit(main())
