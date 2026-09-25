"""Check the LLM Wiki bundle in wiki/ against OKF v0.2 and the repo's schema.

Errors (exit code 1):
  - a non-reserved .md file without parseable frontmatter or a non-empty `type`
  - a wiki file named README.md or summary.md (the site build would publish it)
  - an index.md entry whose description differs from the page's frontmatter,
    or that points at a missing page; frontmatter on a non-root index.md
  - a concept missing from the root index.md or from its directory's index.md
  - a log.md date heading that is not YYYY-MM-DD or not newest first
  - a footnote label that is not a `sources[].id`, or a source without `resource`
  - a raw source or legacy article modified, deleted, or added relative to the
    base ref (raw/ only allows additions)

  - a page that breaks the house format set in CLAUDE.md: `type` outside the
    vocabulary; missing `title`, one-line `description`, `tags`, `sources`,
    `generated`, or a valid `status`; duplicate or uncited source ids; an H1 in
    the body; no `## Related` section; a footnote definition that does not link
    the source's summary page; a source cited more than once in one `##` or
    `###` section; or a Mermaid block without `accTitle` and `accDescr`
  - a number in a page that does not appear in any of the page's sources, when
    those sources are files in this repository (a guard against invented or
    mistyped figures)

Warnings: broken links between wiki pages (OKF allows them), and a missing base
ref, which skips the frozen-source check.
"""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any

import yaml

RESERVED = {"index.md", "log.md"}
FORBIDDEN = {"README.md", "summary.md"}
LEGACY_DIRS = {
    "AWS",
    "Bash",
    "Claude",
    "Ghostty",
    "Git",
    "Kubernetes",
    "Nginx",
    "Nodejs",
    "Python",
    "Ubuntu",
    "YouTube",
    "ZooKeeper",
    "apple",
}
ENTRY_RE = re.compile(r"^[*-] \[(?P<title>[^\]]+)\]\((?P<target>[^)\s]+)\) - (?P<desc>.+)$")
LINK_RE = re.compile(r"(?<!!)\[[^\]]*\]\((?P<target>[^)\s]+)\)")
FOOTNOTE_REF_RE = re.compile(r"\[\^(?P<label>[^\]]+)\](?!:)")
FOOTNOTE_DEF_RE = re.compile(r"(?m)^\[\^(?P<label>[^\]]+)\]:")
FOOTNOTE_DEF_LINE_RE = re.compile(r"(?m)^\[\^(?P<label>[^\]]+)\]:.*$")
SECTION_SPLIT_RE = re.compile(r"(?m)^(?=#{2,3} )")
MERMAID_RE = re.compile(r"(?ms)^```mermaid[^\n]*\n(?P<body>.*?)^```\s*$")
DATE_HEADING_RE = re.compile(r"^## (?P<date>.+?)\s*$")
ISO_DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
ISO_UTC_RE = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$")
TAG_RE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
TYPES = {
    "Concept",
    "Pattern",
    "Tool",
    "Configuration",
    "Command",
    "Service",
    "Playbook",
    "Source Summary",
    "Comparison",
    "Synthesis",
}
STATUSES = {"draft", "stable", "deprecated"}
SUMMARY_TYPE = "Source Summary"


@dataclass
class Report:
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)


def split_frontmatter(text: str) -> tuple[dict[str, Any] | None, str, str | None]:
    """Return (frontmatter, body, error). Frontmatter is None when absent."""
    lines = text.splitlines(keepends=True)
    if not lines or lines[0].strip() != "---":
        return None, text, None
    for i in range(1, len(lines)):
        if lines[i].strip() == "---":
            raw = "".join(lines[1:i])
            body = "".join(lines[i + 1 :])
            try:
                data = yaml.safe_load(raw)
            except yaml.YAMLError as exc:
                return None, body, f"frontmatter is not valid YAML: {exc}"
            if data is None:
                data = {}
            if not isinstance(data, dict):
                return None, body, "frontmatter is not a mapping"
            return data, body, None
    return None, text, "frontmatter has no closing ---"


def _strip_code(body: str) -> str:
    """Drop fenced and inline code so examples are not read as links or footnotes."""
    body = re.sub(r"(?ms)^(```|~~~).*?^\1[^\n]*$", "", body)
    return re.sub(r"`[^`\n]*`", "", body)


def check_concepts(wiki: Path, report: Report) -> dict[Path, dict[str, Any]]:
    concepts: dict[Path, dict[str, Any]] = {}
    for path in sorted(wiki.rglob("*.md")):
        rel = path.relative_to(wiki)
        if path.name in FORBIDDEN:
            report.errors.append(f"{rel}: file name {path.name} is not allowed in wiki/")
        if path.name in RESERVED:
            continue
        data, body, err = split_frontmatter(path.read_text(encoding="utf-8"))
        if err:
            report.errors.append(f"{rel}: {err}")
            continue
        if data is None:
            report.errors.append(f"{rel}: missing frontmatter")
            continue
        type_value = data.get("type")
        if not isinstance(type_value, str) or not type_value.strip():
            report.errors.append(f"{rel}: frontmatter `type` is missing or empty")
            continue
        concepts[path] = data
        check_style(wiki, path, data, body, report)
        check_footnotes(rel, data, body, report)
        check_links(wiki, path, body, report)
    return concepts


def _timestamp(value: Any) -> str:
    # PyYAML turns unquoted ISO timestamps into datetime objects; only a UTC
    # one may be rendered back with a Z suffix.
    if isinstance(value, datetime):
        offset = value.utcoffset()
        if offset is None or offset.total_seconds() != 0:
            return value.isoformat()
        return value.strftime("%Y-%m-%dT%H:%M:%SZ")
    return str(value)


def check_style(wiki: Path, page: Path, data: dict[str, Any], body: str, report: Report) -> None:
    rel = page.relative_to(wiki)
    err = report.errors.append
    if data["type"] not in TYPES:
        err(f"{rel}: type {data['type']!r} is not in the vocabulary {sorted(TYPES)}")
    for key in ("title", "description"):
        value = data.get(key)
        if not isinstance(value, str) or not value.strip() or "\n" in value.strip():
            err(f"{rel}: `{key}` must be a non-empty single line")
    tags = data.get("tags")
    if not isinstance(tags, list) or not tags or not all(
        isinstance(t, str) and TAG_RE.match(t) for t in tags
    ):
        err(f"{rel}: `tags` must be a non-empty list of lowercase-hyphenated tags")
    generated = data.get("generated")
    if not isinstance(generated, dict) or not generated.get("by"):
        err(f"{rel}: `generated.by` is required")
    elif not ISO_UTC_RE.match(_timestamp(generated.get("at"))):
        err(f"{rel}: `generated.at` must be an ISO 8601 UTC time like 2026-09-24T15:00:00Z")
    if data.get("status") not in STATUSES:
        err(f"{rel}: `status` must be one of {sorted(STATUSES)}")
    sources = data.get("sources")
    if not isinstance(sources, list) or not sources:
        err(f"{rel}: at least one entry in `sources` is required")
        sources = []
    ids = [str(s.get("id")) for s in sources if isinstance(s, dict) and s.get("id")]
    if len(ids) != len(sources):
        err(f"{rel}: every `sources` entry needs an `id`")
    if len(set(ids)) != len(ids):
        err(f"{rel}: duplicate `sources[].id`")
    text = _strip_code(body)
    cited = set(FOOTNOTE_REF_RE.findall(text))
    for sid in ids:
        if sid not in cited:
            err(f"{rel}: source {sid!r} is listed but never cited with [^{sid}]")
    for block in MERMAID_RE.finditer(body):
        for key in ("accTitle", "accDescr"):
            if not re.search(rf"(?m)^\s*{key}\s*:", block.group("body")):
                err(f"{rel}: a Mermaid diagram is missing `{key}`")
    if re.search(r"(?m)^# ", text):
        err(f"{rel}: the body must not contain an H1; the title lives in frontmatter")
    if data["type"] == SUMMARY_TYPE:
        return
    if "## Related" not in text:
        err(f"{rel}: missing a `## Related` section")
    definitions = {
        m.group("label"): m.group(0) for m in FOOTNOTE_DEF_LINE_RE.finditer(text)
    }
    for sid in ids:
        target = (wiki / "sources" / f"{sid}.md").resolve()
        links = LINK_RE.findall(definitions.get(sid, ""))
        if not any(_resolve(wiki, page, t) == target for t in links):
            err(f"{rel}: footnote [^{sid}] must link its summary page sources/{sid}.md")


def check_footnotes(rel: Path, data: dict[str, Any], body: str, report: Report) -> None:
    sources = data.get("sources") or []
    if not isinstance(sources, list):
        report.errors.append(f"{rel}: `sources` must be a list")
        return
    ids: set[str] = set()
    for entry in sources:
        if not isinstance(entry, dict) or not entry.get("resource"):
            report.errors.append(f"{rel}: every `sources` entry needs a `resource`")
            continue
        if entry.get("id"):
            ids.add(str(entry["id"]))
    text = _strip_code(body)
    defined = set(FOOTNOTE_DEF_RE.findall(text))
    used = set(FOOTNOTE_REF_RE.findall(text))
    for label in sorted(used | defined):
        if label not in ids:
            report.errors.append(f"{rel}: footnote [^{label}] does not match any sources[].id")
    for label in sorted(used - defined):
        report.errors.append(f"{rel}: footnote [^{label}] is used but never defined")
    for section in SECTION_SPLIT_RE.split(text):
        heading = section.splitlines()[0] if section.startswith("#") else "the opening"
        refs = FOOTNOTE_REF_RE.findall(section)
        for label in sorted({x for x in refs if refs.count(x) > 1}):
            report.errors.append(
                f"{rel}: [^{label}] is cited more than once in {heading!r}; "
                "cite each source once per section"
            )


def _resolve(wiki: Path, page: Path, target: str) -> Path | None:
    target = target.split("#", 1)[0]
    if not target or re.match(r"^[a-z][a-z0-9+.-]*:", target, re.IGNORECASE):
        return None
    base = wiki if target.startswith("/") else page.parent
    return (base / target.lstrip("/")).resolve()


def check_links(wiki: Path, page: Path, body: str, report: Report) -> None:
    for match in LINK_RE.finditer(_strip_code(body)):
        resolved = _resolve(wiki, page, match.group("target"))
        if resolved is not None and not resolved.exists():
            rel = page.relative_to(wiki)
            report.warnings.append(f"{rel}: broken link {match.group('target')}")


def check_indexes(wiki: Path, concepts: dict[Path, dict[str, Any]], report: Report) -> None:
    root = wiki / "index.md"
    if not root.exists():
        report.errors.append("index.md: the bundle root must have an index.md")
        return
    listed_by: dict[Path, set[Path]] = {}
    for index in sorted(wiki.rglob("index.md")):
        rel = index.relative_to(wiki)
        data, body, err = split_frontmatter(index.read_text(encoding="utf-8"))
        if err:
            report.errors.append(f"{rel}: {err}")
        if data is not None:
            extra = set(data) - ({"okf_version"} if index == root else set())
            if extra:
                report.errors.append(f"{rel}: index.md may not carry frontmatter {sorted(extra)}")
        listed: set[Path] = set()
        for line in body.splitlines():
            m = ENTRY_RE.match(line.strip())
            if not m:
                continue
            if m.group("target").endswith("/"):
                report.errors.append(
                    f"{rel}: entry {m.group('target')} links a directory; "
                    "link its index.md so Obsidian can resolve it"
                )
                continue
            target = _resolve(wiki, index, m.group("target"))
            if target is None:
                continue
            if target.name in RESERVED:
                continue
            page = next((p for p in concepts if p.resolve() == target), None)
            if page is None:
                report.errors.append(f"{rel}: entry {m.group('target')} is not a valid page")
                continue
            listed.add(page)
            desc = str(concepts[page].get("description", "")).strip()
            if m.group("desc").strip() != desc:
                report.errors.append(
                    f"{rel}: description for {m.group('target')} differs from its frontmatter"
                )
        listed_by[index] = listed
    for page in concepts:
        rel = page.relative_to(wiki)
        if page not in listed_by.get(root, set()):
            report.errors.append(f"index.md: {rel} is not listed in the root index")
        local = page.parent / "index.md"
        if page.parent != wiki:
            if local not in listed_by:
                report.errors.append(f"{rel}: directory has no index.md")
            elif page not in listed_by[local]:
                report.errors.append(f"{rel}: not listed in {local.relative_to(wiki)}")


def check_logs(wiki: Path, report: Report) -> None:
    for log in sorted(wiki.rglob("log.md")):
        rel = log.relative_to(wiki)
        dates: list[str] = []
        for line in log.read_text(encoding="utf-8").splitlines():
            m = DATE_HEADING_RE.match(line)
            if not m:
                continue
            if not ISO_DATE_RE.match(m.group("date")):
                report.errors.append(f"{rel}: heading '{line}' is not ## YYYY-MM-DD")
                continue
            dates.append(m.group("date"))
        if dates != sorted(dates, reverse=True) or len(dates) != len(set(dates)):
            report.errors.append(f"{rel}: date headings must be unique and newest first")


def check_frozen(repo: Path, base: str, report: Report) -> None:
    probe = subprocess.run(
        ["git", "rev-parse", "--verify", "--quiet", f"{base}^{{commit}}"],
        cwd=repo,
        capture_output=True,
        text=True,
    )
    if probe.returncode != 0:
        report.warnings.append(f"base ref {base!r} not found; frozen-source check skipped")
        return
    out = subprocess.run(
        ["git", "diff", "--name-status", "--no-renames", base, "--"],
        cwd=repo,
        capture_output=True,
        text=True,
        check=True,
    ).stdout
    for line in out.splitlines():
        status, _, name = line.partition("\t")
        top = name.split("/", 1)[0]
        if top == "raw" and status != "A":
            report.errors.append(f"{name}: raw sources are append-only ({status})")
        elif top in LEGACY_DIRS:
            report.errors.append(f"{name}: legacy articles are frozen ({status})")


REPO_BLOB = "https://github.com/kelvinlee97/engineering/blob/main/"
NUMBER_RE = re.compile(r"(?<![\w.-])\d[\d,.]*\d%?|(?<![\w.-])\d%?")


def _local_source_text(root: Path, sources: list[Any]) -> str | None:
    """Concatenated text of every source, or None if any source is not a repo file."""
    texts: list[str] = []
    for entry in sources:
        resource = str(entry.get("resource", "")) if isinstance(entry, dict) else ""
        if not resource.startswith(REPO_BLOB):
            return None
        path = root / resource[len(REPO_BLOB) :]
        if not path.is_file():
            return None
        texts.append(path.read_text(encoding="utf-8"))
    return "\n".join(texts) if texts else None


def check_faithfulness(wiki: Path, concepts: dict[Path, dict[str, Any]], report: Report) -> None:
    """Every number on a page must appear in the text of the sources it cites."""
    root = wiki.resolve().parent
    for page, data in concepts.items():
        source = _local_source_text(root, data.get("sources") or [])
        if source is None:
            continue
        _, body, _ = split_frontmatter(page.read_text(encoding="utf-8"))
        body = re.sub(r"\[\^[^\]]+\]|\([^)]*\)|`[^`]*`", "", _strip_code(body))
        for number in sorted(set(NUMBER_RE.findall(body))):
            number = number.rstrip(".,")
            if number and number not in source:
                rel = page.relative_to(wiki)
                report.errors.append(f"{rel}: number {number!r} does not appear in its sources")


def run(wiki: Path, repo: Path | None, base: str | None) -> Report:
    report = Report()
    if not wiki.is_dir():
        report.errors.append(f"{wiki}: wiki directory not found")
        return report
    concepts = check_concepts(wiki, report)
    check_indexes(wiki, concepts, report)
    check_logs(wiki, report)
    check_faithfulness(wiki, concepts, report)
    if repo is not None and base:
        check_frozen(repo, base, report)
    return report


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--wiki", type=Path, default=Path("wiki"))
    parser.add_argument("--base", default="origin/main", help="ref for the frozen-source check")
    parser.add_argument("--no-frozen", action="store_true", help="skip the frozen-source check")
    args = parser.parse_args(argv)
    repo = None if args.no_frozen else Path.cwd()
    report = run(args.wiki, repo, args.base)
    for warning in report.warnings:
        print(f"warning: {warning}")
    for error in report.errors:
        print(f"error: {error}")
    pages = sum(1 for p in args.wiki.rglob("*.md") if p.name not in RESERVED)
    print(f"{pages} pages, {len(report.errors)} errors, {len(report.warnings)} warnings")
    return 1 if report.errors else 0


if __name__ == "__main__":
    sys.exit(main())
