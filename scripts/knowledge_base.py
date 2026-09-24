#!/usr/bin/env python3
"""Validate and stage the public Markdown knowledge base for MkDocs."""

from __future__ import annotations

import argparse
import datetime
import html
import posixpath
import re
import shutil
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path, PurePosixPath
from urllib.parse import quote, urlsplit, urlunsplit

REPOSITORY_URL = "https://github.com/kelvinlee97/engineering"
GITHUB_BLOB_URL = f"{REPOSITORY_URL}/blob/main"
PRESENTATION_CSS = Path("pages/knowledge-base.css")
STAGED_CSS = Path("stylesheets/knowledge-base.css")
PRESENTATION_ASSETS = Path("pages/assets")
STAGED_ASSETS = Path("assets")
EXCLUDED_PARTS = {
    ".agents",
    ".local",
    ".plugin-eval",
    ".pytest_cache",
    ".venv",
    "__pycache__",
}
PUBLISHABLE_NAMES = {"README.md", "summary.md"}
H1_RE = re.compile(r"(?m)^\s*#(?!#)\s+(.+?)\s*#*\s*$")
LINK_RE = re.compile(
    r"(?<!\!)\[[^\]]*\]\((?P<target><[^>]*>|[^)\s]+)(?P<tail>[^)]*)\)"
)
MERMAID_RE = re.compile(
    r"(?ms)^```mermaid[^\n]*\n(?P<body>.*?)^```\s*$"
)
YOUTUBE_RE = re.compile(
    r"https?://(?:www\.)?youtube\.com/watch\?v=([A-Za-z0-9_-]{11})"
)
YOUTUBE_SHORT_RE = re.compile(r"https?://youtu\.be/([A-Za-z0-9_-]{11})")
KIND_LABELS = {
    "guide": "Guide",
    "runbook": "Runbook",
    "reference": "Reference",
    "tooling": "Tooling",
    "video-summary": "Video summary",
    "catalog": "Catalog",
}
BLOG_KINDS = set(KIND_LABELS) - {"catalog"}
# Reading pace used for the per-article estimate.
LATIN_WORDS_PER_MINUTE = 220
EXCERPT_LENGTH = 190
RELATED_LIMIT = 4
LATIN_WORD_RE = re.compile(r"[A-Za-z0-9][A-Za-z0-9'’./_-]*")
PICTOGRAPH_RE = re.compile("[\U0001F000-\U0001FAFF←-➿⬀-⯿]")


class KnowledgeBaseError(Exception):
    """Raised when the public knowledge-base contract is invalid."""


@dataclass(frozen=True)
class Document:
    source: str
    page: str
    title: str
    area: str
    kind: str
    # Date of the commit that ADDED the file: when the note was published. The
    # timeline orders by this, so fixing a typo in an old note does not shove
    # it back to the top of the site.
    published: str
    # Full commit timestamp behind `published`, to break same-day ties.
    published_at: str
    # Date of the most recent commit that touched the file. Shown on the
    # article itself when it differs from the publication date; never used for
    # ordering.
    updated: str
    updated_at: str
    video_id: str | None


def _normalise_path(value: str | PurePosixPath) -> str:
    return PurePosixPath(str(value).replace("\\", "/")).as_posix()


def _is_publishable(path: str) -> bool:
    candidate = PurePosixPath(path)
    if any(part in EXCLUDED_PARTS for part in candidate.parts):
        return False
    if candidate.name == "AGENTS.md":
        return False
    if candidate.name not in PUBLISHABLE_NAMES:
        return False
    return not candidate.name.startswith("summary") or "YouTube" in candidate.parts


def _page_path(source: str) -> str:
    path = PurePosixPath(source)
    if path.name == "README.md":
        parent = path.parent if path.parent != PurePosixPath(".") else PurePosixPath("repository")
        return _normalise_path(parent / "index.md")
    return path.as_posix()


def _extract_title(text: str, source: str) -> str:
    match = H1_RE.search(text)
    if not match:
        raise KnowledgeBaseError(f"{source}: missing level-one heading")
    title = match.group(1).strip()
    title = re.sub(r"\[([^]]+)\]\([^)]*\)", r"\1", title)
    title = title.replace("`", "").replace("*", "").replace("_", "")
    return title.strip()


def _kind_label(kind: str) -> str:
    return KIND_LABELS.get(kind, kind.replace("-", " ").title())


def _strip_markdown(text: str) -> str:
    """Reduce Markdown to prose so word counts and excerpts ignore syntax."""

    text = re.sub(r"(?ms)^```.*?^```\s*$", " ", text)
    text = re.sub(r"(?m)^\s{0,3}(---|\*\*\*|___)\s*$", " ", text)
    text = re.sub(r"<[^>]+>", " ", text)
    text = re.sub(r"!\[[^\]]*\]\([^)]*\)", " ", text)
    text = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", text)
    # Inline emphasis and code markers hug words; dropping them keeps "**word**." intact.
    text = re.sub(r"[`*]", "", text)
    text = re.sub(r"[_#>|]", " ", text)
    return text


def _reading_minutes(text: str) -> int:
    """Estimate reading time in whole minutes, never less than one."""

    body = _strip_markdown(text)
    words = len(LATIN_WORD_RE.findall(body))
    minutes = words / LATIN_WORDS_PER_MINUTE
    return max(1, round(minutes))


def _reading_label(text: str) -> str:
    minutes = _reading_minutes(text)
    return f"{minutes} min read"


# A blockquote that opens an article (before its first section heading) is its
# plain-language framing, the best one-line description of the note. Later
# blockquotes are callouts, and a verification stamp describes nothing.
VERIFICATION_PREFIX = "facts verified"


def _excerpt(text: str) -> str:
    """One line describing a note, for the timeline.

    The first paragraph or opening framing blockquote that says something.
    """

    body = text
    if body.startswith("---\n"):
        closing = body.find("\n---\n", 4)
        if closing != -1:
            body = body[closing + 5 :]
    match = H1_RE.search(body)
    if match:
        body = body[match.end() :]
    # Fenced blocks split on blank lines like prose, so a Mermaid diagram's
    # edge list can otherwise surface as an excerpt.
    body = re.sub(r"(?ms)^```.*?^```\s*$", "\n\n", body)
    in_opening = True
    for block in re.split(r"\n\s*\n", body):
        block = block.strip()
        if not block:
            continue
        if block.startswith("#"):
            in_opening = False
            continue
        if block.startswith(">"):
            block = "\n".join(
                line.lstrip(">").strip() for line in block.splitlines()
            )
            if not in_opening or block.lower().startswith(VERIFICATION_PREFIX):
                continue
        elif block.startswith(("|", "-", "*", "<", "```", "!")):
            continue
        candidate = " ".join(_strip_markdown(block).split())
        if not candidate or len(candidate) < 40:
            continue
        # A line opening with a pictograph is a callout ("🎮 Try the
        # interactive version"), not a description of the note.
        if PICTOGRAPH_RE.match(candidate):
            continue
        # A colon-terminated line introduces the list that follows; on its own
        # it describes nothing, and many articles open with the same one.
        if candidate.endswith(":"):
            continue
        if len(candidate) <= EXCERPT_LENGTH:
            return candidate
        cut = candidate[:EXCERPT_LENGTH]
        if " " in cut:
            cut = cut[: cut.rindex(" ")]
        return cut.rstrip(" ,.;:") + "…"
    return ""


def _blog_documents(documents: list[Document]) -> list[Document]:
    return _sorted_documents(
        [document for document in documents if document.kind in BLOG_KINDS]
    )


def _sorted_documents(documents: list[Document]) -> list[Document]:
    by_source = sorted(documents, key=lambda document: document.source)
    return sorted(
        by_source,
        key=lambda document: (document.published or "", document.published_at or ""),
        reverse=True,
    )


def _site_directory(page: str) -> str:
    path = PurePosixPath(page)
    if path == PurePosixPath("index.md"):
        return "."
    if path.name == "index.md":
        return path.parent.as_posix()
    return path.with_suffix("").as_posix()


def _relative_site_url(source_page: str, target_page: str) -> str:
    source_directory = _site_directory(source_page)
    target_directory = _site_directory(target_page)
    relative = posixpath.relpath(target_directory, start=source_directory)
    return "./" if relative == "." else f"{relative.rstrip('/')}/"


def _escape(value: str) -> str:
    return html.escape(value, quote=True)


def _generated_front_matter(
    *,
    title: str | None = None,
    hide_navigation: bool = False,
    hide_toc: bool = False,
    hide_footer: bool = False,
    search_exclude: bool = False,
) -> str:
    lines = ["---"]
    if title:
        lines.append(f"title: {title}")
    hidden = []
    if hide_navigation:
        hidden.append("navigation")
    if hide_toc:
        hidden.append("toc")
    if hide_footer:
        hidden.append("footer")
    if hidden:
        lines.append("hide:")
        lines.extend(f"  - {item}" for item in hidden)
    if search_exclude:
        lines.extend(["search:", "  exclude: true"])
    lines.extend(["---", ""])
    return "\n".join(lines)


def _with_generated_metadata(text: str, document: Document) -> str:
    source = f"{GITHUB_BLOB_URL}/{quote(document.source, safe='/')}"
    metadata = f"kb_source: {source}"
    if text.startswith("---\n"):
        closing = text.find("\n---\n", 4)
        if closing != -1:
            front_matter = text[4:closing]
            front_matter = f"{front_matter.rstrip()}\n{metadata}"
            return f"---\n{front_matter}\n---\n{text[closing + 5:]}"
    return f"---\n{metadata}\n---\n\n{text}"


def _extract_video_id(text: str) -> str | None:
    ids = set(YOUTUBE_RE.findall(text)) | set(YOUTUBE_SHORT_RE.findall(text))
    if len(ids) > 1:
        raise KnowledgeBaseError("summary contains multiple YouTube video IDs")
    return next(iter(ids), None)


def _mermaid_types(text: str, source: str) -> tuple[list[str], list[str]]:
    """Return Mermaid diagram types and accessibility validation errors."""

    diagram_types: list[str] = []
    errors: list[str] = []
    for index, match in enumerate(MERMAID_RE.finditer(text), start=1):
        body = match.group("body")
        lines = [line.strip() for line in body.splitlines() if line.strip()]
        diagram_types.append(lines[0].split()[0] if lines else "empty")
        if not re.search(r"(?m)^\s*accTitle:\s*\S", body):
            errors.append(f"{source}: Mermaid diagram {index} missing accTitle")
        single_description = re.search(r"(?m)^\s*accDescr:\s*\S", body)
        multiline_description = re.search(
            r"(?ms)^\s*accDescr\s*\{\s*\n.+?^\s*\}", body
        )
        if not single_description and not multiline_description:
            errors.append(f"{source}: Mermaid diagram {index} missing accDescr")
    return diagram_types, errors


def _kind(source: str) -> str:
    path = PurePosixPath(source)
    lower_parts = {part.lower() for part in path.parts}
    if path.name.startswith("summary"):
        return "video-summary"
    if "youtube-transcript" in lower_parts:
        return "tooling"
    if "runbooks" in lower_parts:
        return "runbook"
    if "guides" in lower_parts:
        return "guide"
    if path.name.startswith("README") and (
        path.parent == PurePosixPath(".") or len(path.parts) == 2
    ):
        return "catalog"
    return "reference"


def _area(source: str) -> str:
    path = PurePosixPath(source)
    return path.parts[0] if len(path.parts) > 1 else "engineering"


def _commit_dates(root: Path, source: str) -> tuple[str, str, str, str]:
    """Publication and last-touched dates: (published, published_at, updated, updated_at).

    `git log` lists newest first, so the last line is the commit that added
    the file and the first is the most recent one to touch it.
    """

    if not (root / ".git").exists():
        return "", "", "", ""
    result = subprocess.run(
        ["git", "-C", str(root), "log", "--format=%cs%x09%cI", "--", source],
        capture_output=True,
        text=True,
        check=False,
    )
    lines = [line.strip() for line in result.stdout.strip().splitlines() if line.strip()]
    if not lines:
        return "", "", "", ""

    def split(line: str) -> tuple[str, str]:
        date, _, stamp = line.partition("\t")
        return date.strip(), stamp.strip()

    updated, updated_at = split(lines[0])
    published, published_at = split(lines[-1])
    return published, published_at, updated, updated_at


def _git_tracked_paths(root: Path) -> list[str]:
    result = subprocess.run(
        ["git", "-C", str(root), "ls-files", "-z"],
        capture_output=True,
        check=False,
    )
    if result.returncode:
        detail = result.stderr.decode(errors="replace").strip()
        raise KnowledgeBaseError(f"cannot list tracked files: {detail}")
    return [_normalise_path(item.decode()) for item in result.stdout.split(b"\0") if item]


def _split_destination(target: str) -> tuple[str, str]:
    if target.startswith("<") and target.endswith(">"):
        target = target[1:-1]
    parsed = urlsplit(target)
    path = parsed.path
    suffix = urlunsplit(("", "", "", parsed.query, parsed.fragment))
    return path, suffix


def _is_external(target: str) -> bool:
    parsed = urlsplit(target)
    return bool(parsed.scheme or parsed.netloc or target.startswith("//"))


def _resolve_local_target(source: str, target: str, tracked: set[str]) -> str | None:
    path, _ = _split_destination(target)
    if not path or path.startswith("/"):
        return None
    candidate = PurePosixPath(
        posixpath.normpath(posixpath.join(str(PurePosixPath(source).parent), path))
    )
    candidate_name = candidate.name
    candidate_path = candidate.as_posix()
    if path.endswith("/") or not candidate_name or (
        candidate_path not in tracked and "." not in candidate_name
    ):
        readme_path = _normalise_path(candidate / "README.md")
        candidate_path = readme_path if readme_path in tracked else candidate_path
    return candidate_path


def _is_tracked_directory(path: str, tracked: set[str]) -> bool:
    prefix = f"{path.rstrip('/')}/"
    return any(candidate.startswith(prefix) for candidate in tracked)


def _validate_links(
    root: Path,
    documents: list[Document],
    tracked: set[str],
    publishable: set[str],
) -> list[str]:
    errors: list[str] = []
    for document in documents:
        text = (root / document.source).read_text(encoding="utf-8")
        for match in LINK_RE.finditer(text):
            target = match.group("target")
            if _is_external(target):
                continue
            path, _ = _split_destination(target)
            if not path:
                continue
            resolved = _resolve_local_target(document.source, target, tracked)
            if resolved is None or (
                resolved not in tracked and not _is_tracked_directory(resolved, tracked)
            ):
                errors.append(f"{document.source}: missing local link target {target}")
                continue
            if resolved not in publishable and not (root / resolved).exists():
                errors.append(f"{document.source}: forbidden local link target {target}")
    return errors


def discover_documents(
    root: Path,
    paths: list[str] | None = None,
) -> list[Document]:
    """Discover and validate publishable documents from tracked paths."""

    input_paths = _git_tracked_paths(root) if paths is None else paths
    tracked_paths = {_normalise_path(path) for path in input_paths}
    candidates = sorted(path for path in tracked_paths if _is_publishable(path))
    errors: list[str] = []
    titles: dict[str, str] = {}
    video_ids: dict[str, str | None] = {}
    mermaid_types: dict[str, list[str]] = {}

    for source in candidates:
        source_path = root / source
        try:
            text = source_path.read_text(encoding="utf-8")
            titles[source] = _extract_title(text, source)
            mermaid_types[source], mermaid_errors = _mermaid_types(text, source)
            errors.extend(mermaid_errors)
            video_ids[source] = (
                _extract_video_id(text)
                if PurePosixPath(source).name.startswith("summary")
                else None
            )
        except (OSError, UnicodeError, KnowledgeBaseError) as exc:
            errors.append(str(exc))

    for source in candidates:
        if PurePosixPath(source).name.startswith("summary") and video_ids.get(source) is None:
            errors.append(f"{source}: missing YouTube source URL")

    page_paths: dict[str, str] = {}
    for source in candidates:
        page = _page_path(source)
        previous = page_paths.setdefault(page, source)
        if previous != source:
            errors.append(f"{source}: staged page path conflicts with {previous}")

    if errors:
        raise KnowledgeBaseError("\n".join(sorted(set(errors))))

    documents = []
    publishable = set(candidates)
    for source in candidates:
        dates = _commit_dates(root, source)
        documents.append(
            Document(
                source=source,
                page=_page_path(source),
                title=titles[source],
                area=_area(source),
                kind=_kind(source),
                published=dates[0],
                published_at=dates[1],
                updated=dates[2],
                updated_at=dates[3],
                video_id=video_ids[source],
            )
        )

    link_errors = _validate_links(root, documents, tracked_paths, publishable)
    if link_errors:
        raise KnowledgeBaseError("\n".join(sorted(set(link_errors))))
    return documents


def _relative_page_link(source_page: str, target_page: str) -> str:
    start = PurePosixPath(source_page).parent.as_posix()
    return posixpath.relpath(target_page, start=start)


def rewrite_links(
    text: str,
    source: str,
    page_map: dict[str, str],
    tracked: set[str],
) -> str:
    """Rewrite local Markdown links to staged pages or canonical GitHub files."""

    source_page = page_map[source]

    def replace(match: re.Match[str]) -> str:
        original = match.group("target")
        if _is_external(original):
            return match.group(0)
        path, suffix = _split_destination(original)
        if not path:
            return match.group(0)
        resolved = _resolve_local_target(source, original, tracked)
        if resolved is None or (
            resolved not in tracked and not _is_tracked_directory(resolved, tracked)
        ):
            raise KnowledgeBaseError(f"{source}: missing local link target {original}")
        if resolved in page_map:
            destination = _relative_page_link(source_page, page_map[resolved])
        elif _is_tracked_directory(resolved, tracked):
            destination = f"{REPOSITORY_URL}/tree/main/{quote(resolved, safe='/')}"
        else:
            destination = f"{GITHUB_BLOB_URL}/{quote(resolved, safe='/')}"
        target_start, target_end = match.span("target")
        full = match.group(0)
        replacement = destination + suffix
        return (
            full[: target_start - match.start()]
            + replacement
            + full[target_end - match.start() :]
        )

    return LINK_RE.sub(replace, text)


def _with_generated_context(text: str, document: Document, reading: str = "") -> str:
    """The line under an article's title: what it is, when it was written, how long."""

    match = H1_RE.search(text)
    if not match:
        return text
    kind_label = _kind_label(document.kind)
    dates = ""
    if document.published:
        dates = (
            f'  <time datetime="{_escape(document.published)}">'
            f"Published {_escape(document.published)}</time>\n"
        )
        if document.updated and document.updated != document.published:
            dates += (
                f'  <time datetime="{_escape(document.updated)}">'
                f"updated {_escape(document.updated)}</time>\n"
            )
    reading_html = ""
    if reading:
        reading_html = f'  <span class="kb-meta__reading">{_escape(reading)}</span>\n'
    context = (
        "\n\n"
        '<div class="kb-meta" role="group" aria-label="Page metadata" data-search-exclude>\n'
        f'  <span class="kb-meta__kind">{_escape(kind_label)}</span>\n'
        f"{dates}"
        f"{reading_html}"
        "</div>"
    )
    return text[: match.end()] + context + text[match.end() :]


MONTH_NAMES_EN = (
    "January", "February", "March", "April", "May", "June",
    "July", "August", "September", "October", "November", "December",
)

# Each kind gets its own filtered timeline at the site root. The slugs are the
# URLs, so they stay plural and lowercase.
KIND_SLUGS = {
    "runbook": "runbooks",
    "reference": "references",
    "guide": "guides",
    "video-summary": "video-notes",
    "tooling": "tooling",
}
KIND_TAB_LABELS = {
    "runbook": "Runbooks",
    "reference": "References",
    "guide": "Guides",
    "video-summary": "Video notes",
    "tooling": "Tooling",
}
# The home page gives this many notes the full treatment before the list
# tightens, and no topic may take more than its share of them.
HOME_RICH_LIMIT = 3
RICH_PER_AREA = 2
HOME_DENSE_LIMIT = 17


def _kind_page(kind: str) -> str:
    return f"{KIND_SLUGS[kind]}/index.md"


def _home_page() -> str:
    return "index.md"


def _month_label(month: str) -> str:
    """`2026-09` rendered as a group heading: `September 2026`."""

    if not month:
        return "Undated"
    year, _, number = month.partition("-")
    index = int(number)
    return f"{MONTH_NAMES_EN[index - 1]} {year}"


def _long_date(value: str) -> str:
    """`2026-09-18` as `Sep 18, 2026`."""

    if not value:
        return ""
    year, month, day = value.split("-")
    return f"{MONTH_NAMES_EN[int(month) - 1][:3]} {int(day)}, {year}"


def _short_date(value: str) -> str:
    """The dense list's date column: `Sep 16`."""

    if not value:
        return "--"
    _, month, day = value.split("-")
    return f"{MONTH_NAMES_EN[int(month) - 1][:3]} {int(day)}"


def _rich_html(
    document: Document,
    source_page: str,
    topic: str,
    excerpt: str,
    show_kind: bool = True,
) -> str:
    """A recent note, given room: what it is, what it is called, what it says."""

    meta = " · ".join(
        part
        for part in (
            _long_date(document.published),
            topic,
            _kind_label(document.kind) if show_kind else "",
        )
        if part
    )
    excerpt_html = (
        f'<span class="kb-lead__excerpt">{_escape(excerpt)}</span>' if excerpt else ""
    )
    return (
        f'<a class="kb-lead" href="{_escape(_relative_site_url(source_page, document.page))}">'
        f'<span class="kb-lead__meta">{_escape(meta)}</span>'
        f'<span class="kb-lead__title">{_escape(document.title)}</span>'
        f"{excerpt_html}"
        "</a>"
    )


def _dense_html(document: Document, source_page: str, topic: str) -> str:
    """An older note, one line: when, what, where it belongs."""

    return (
        '<li class="kb-row">'
        f'<a class="kb-row__link" '
        f'href="{_escape(_relative_site_url(source_page, document.page))}">'
        f'<time class="kb-row__date" datetime="{_escape(document.published)}">'
        f"{_escape(_short_date(document.published))}</time>"
        f'<span class="kb-row__title">{_escape(document.title)}</span>'
        f'<span class="kb-row__topic">{_escape(topic)}</span>'
        "</a>"
        "</li>"
    )


def _dense_feed_html(
    documents: list[Document],
    source_page: str,
    first_label: str | None = None,
) -> str:
    """Older notes, newest first, grouped by the month they were published."""

    if not documents:
        return ""
    groups: list[tuple[str, list[Document]]] = []
    for document in documents:
        month = document.published[:7] if document.published else ""
        if not groups or groups[-1][0] != month:
            groups.append((month, []))
        groups[-1][1].append(document)
    sections = []
    for index, (month, entries) in enumerate(groups):
        label = _month_label(month)
        if index == 0 and first_label:
            label = first_label
        anchor = f"feed-{month or 'undated'}"
        rows = "".join(
            _dense_html(document, source_page, _topic_name(document.area, document.area))
            for document in entries
        )
        sections.append(
            f'<section class="kb-feed__group" aria-labelledby="{_escape(anchor)}">'
            f'<h2 class="kb-feed__month" id="{_escape(anchor)}">{_escape(label)}</h2>'
            f'<ol class="kb-feed__list">{rows}</ol>'
            "</section>"
        )
    return f'<div class="kb-feed">{"".join(sections)}</div>'


def _lead_selection(notes: list[Document]) -> tuple[list[Document], list[Document]]:
    """Split the timeline into the few notes shown in full and the rest.

    Order never changes; only how much of each note is drawn. A topic may hold
    at most `RICH_PER_AREA` of the lead slots, so three notes published on the
    same day about the same thing cannot make the page look single-minded.
    """

    lead: list[Document] = []
    taken: dict[str, int] = {}
    for document in notes:
        if len(lead) == HOME_RICH_LIMIT:
            break
        if taken.get(document.area, 0) >= RICH_PER_AREA:
            continue
        taken[document.area] = taken.get(document.area, 0) + 1
        lead.append(document)
    chosen = {document.source for document in lead}
    return lead, [document for document in notes if document.source not in chosen]


def _kind_counts(documents: list[Document]) -> dict[str, int]:
    counts: dict[str, int] = {}
    for document in _blog_documents(documents):
        counts[document.kind] = counts.get(document.kind, 0) + 1
    return counts


def _kind_tabs_html(
    documents: list[Document],
    source_page: str,
    active: str | None,
) -> str:
    """Filter the timeline by kind. It never reorders: it only takes rows away."""

    counts = _kind_counts(documents)
    total = counts.get(active, 0) if active else sum(counts.values())
    tabs = [
        (
            "All",
            _relative_site_url(source_page, _home_page()),
            active is None,
        )
    ]
    for kind in KIND_SLUGS:
        if not counts.get(kind):
            continue
        tabs.append(
            (
                KIND_TAB_LABELS[kind],
                _relative_site_url(source_page, _kind_page(kind)),
                active == kind,
            )
        )
    rendered = []
    for label, url, is_active in tabs:
        classes = "kb-tab kb-tab--active" if is_active else "kb-tab"
        current = ' aria-current="page"' if is_active else ""
        rendered.append(
            f'<a class="{classes}" href="{_escape(url)}"{current}>{_escape(label)}</a>'
        )
    links = "".join(rendered)
    count = f"{total} notes · newest first"
    return (
        f'<nav class="kb-tabs" aria-label="Filter by kind">{links}'
        f'<span class="kb-tabs__count">{_escape(count)}</span></nav>'
    )


def _timeline_page(
    documents: list[Document],
    page: str,
    *,
    kind: str | None,
    excerpts: dict[str, str] | None = None,
    dense_limit: int | None = None,
) -> str:
    """The home page and every kind page: leads, then the list tightens."""

    excerpts = excerpts or {}
    notes = _blog_documents(documents)
    if kind is not None:
        notes = [document for document in notes if document.kind == kind]
    lead, rest = _lead_selection(notes)
    remaining = rest[:dense_limit] if dense_limit is not None else rest

    leads = "".join(
        _rich_html(
            document,
            page,
            _topic_name(document.area, document.area),
            excerpts.get(document.source, ""),
            show_kind=kind is None,
        )
        for document in lead
    )
    earlier_label = None
    if lead and remaining and lead[0].published[:7] == remaining[0].published[:7]:
        month = _month_label(remaining[0].published[:7])
        earlier_label = f"Earlier in {month.split(' ')[0]}"
    feed = _dense_feed_html(documents=remaining, source_page=page, first_label=earlier_label)
    empty = '<p class="kb-empty">No published notes yet.</p>'
    archive_page = "archive/index.md"
    more_label = "Full archive"

    site_name = "Kelvin’s Engineering Notes"
    heading = site_name
    if kind is not None:
        heading = f"{KIND_TAB_LABELS[kind]} — {site_name}"
    sections = [
        '<div class="kb-home">',
        # The wordmark carries the site's name visually; this is the same name
        # for a screen reader and for search engines, and it stops the theme
        # from inserting a heading of its own.
        f'<h1 class="kb-visually-hidden">{_escape(heading)}</h1>',
        _kind_tabs_html(documents, page, kind),
    ]
    if leads:
        sections.append(f'<div class="kb-leads">{leads}</div>')
    if feed:
        sections.append(feed)
    if not leads and not feed:
        sections.append(empty)
    if remaining != rest or kind is None:
        sections.append(
            f'<a class="kb-more" '
            f'href="{_escape(_relative_site_url(page, archive_page))}">'
            f"{_escape(more_label)}</a>"
        )
    sections.extend(["</div>", ""])

    title = "Home" if kind is None else KIND_TAB_LABELS[kind]
    return _generated_front_matter(
        title=title,
        # The left rail would only repeat what the tabs already say, and the
        # timeline wants the full measure.
        hide_navigation=True,
        hide_toc=True,
        search_exclude=True,
    ) + "\n".join(sections)


def _topic_catalog(documents: list[Document], area: str) -> Document | None:
    area_documents = [document for document in documents if document.area == area]
    return next(
        (document for document in area_documents if document.kind == "catalog"),
        area_documents[0] if area_documents else None,
    )


def _monogram(area: str) -> str:
    """Short badge text for a topic tile: an acronym, or the first two letters."""

    letters = [part[0] for part in re.split(r"[-_\s]+", area) if part]
    if len(letters) > 1:
        return "".join(letters[:2]).upper()
    stripped = re.sub(r"[^0-9A-Za-z]", "", area)
    if not stripped:
        return area[:1]
    if stripped.isupper():
        return stripped[:3]
    return stripped[:2].upper()


def _related_html(
    document: Document,
    documents: list[Document],
) -> str:
    """End-of-article links to nearby notes, so a reader has somewhere to go next."""

    if document.kind == "catalog":
        return ""
    pool = [
        candidate
        for candidate in _blog_documents(documents)
        if candidate.source != document.source
    ]
    same_area = [candidate for candidate in pool if candidate.area == document.area]
    related = same_area[:RELATED_LIMIT]
    if len(related) < RELATED_LIMIT:
        chosen = {candidate.source for candidate in related}
        same_kind = [
            candidate
            for candidate in pool
            if candidate.kind == document.kind and candidate.source not in chosen
        ]
        related.extend(same_kind[: RELATED_LIMIT - len(related)])
    if not related:
        return ""
    cards = []
    for candidate in related:
        date = (
            f"<span>{_escape(candidate.updated)}</span>" if candidate.updated else ""
        )
        cards.append(
            '<a class="kb-related__card" '
            f'href="{_escape(_relative_site_url(document.page, candidate.page))}">'
            f'<span class="kb-related__card-title">{_escape(candidate.title)}</span>'
            '<span class="kb-related__card-meta">'
            f'<span class="kb-chip">'
            f"{_escape(_kind_label(candidate.kind))}</span>"
            f"{date}"
            "</span>"
            "</a>"
        )
    return (
        "\n\n"
        '<section class="kb-related" aria-label="Related notes" data-search-exclude>\n'
        '<h2 class="kb-related__title">Keep reading</h2>\n'
        f'<div class="kb-related__grid">{"".join(cards)}</div>\n'
        "</section>\n"
    )


# --------------------------------------------------------------------------
# Navigation
#
# MkDocs builds its navigation from the staged tree, which is flat and
# alphabetical: AWS alone contributes 123 pages, so an auto-generated nav
# buries every other topic. The constants below group the tree into eight
# top-level sections (rendered as tabs) and split AWS into service families,
# and `_summary_markdown` emits them as the literate-nav SUMMARY.md.
# --------------------------------------------------------------------------

NAV_LABEL_SUFFIXES = (" - Runbook & Reference",)

AWS_GROUPS: tuple[tuple[str, tuple[str, ...]], ...] = (
    (
        "Foundations, cost & certification",
        (
            "aws-ecosystem",
            "foundations-cloud-computing",
            "shared-responsibility-model",
            "well-architected",
            "pricing-models",
            "billing-cost-management",
            "certifications/cloud-practitioner",
            "certifications/solutions-architect",
            "certifications/developer-associate",
            "certifications/competencies",
            "solutions-implementations",
            "solutions-consulting-offers",
        ),
    ),
    (
        "Compute & containers",
        (
            "ec2",
            "auto-scaling-groups",
            "application-auto-scaling",
            "lambda",
            "batch",
            "ecs",
            "eks",
            "ecr",
            "lightsail",
            "outposts",
            "elastic-beanstalk",
            "opsworks",
        ),
    ),
    (
        "Networking & content delivery",
        (
            "vpc",
            "route53",
            "cloudfront",
            "elb",
            "global-accelerator",
            "direct-connect",
            "api-gateway",
            "appsync",
        ),
    ),
    (
        "Storage & migration",
        (
            "s3",
            "fsx",
            "storage-gateway",
            "backup",
            "snow-family",
            "datasync",
            "transfer-family",
            "mgn",
        ),
    ),
    (
        "Databases",
        (
            "rds",
            "dynamodb",
            "elasticache",
            "documentdb",
            "neptune",
            "qldb",
            "dms",
            "managed-blockchain",
        ),
    ),
    (
        "Data & analytics",
        (
            "athena",
            "glue",
            "emr",
            "kinesis",
            "msk",
            "redshift",
            "quicksight",
            "data-pipeline",
            "opensearch",
            "cloudsearch",
            "appflow",
        ),
    ),
    (
        "Machine learning",
        (
            "sagemaker",
            "comprehend",
            "forecast",
            "kendra",
            "lex",
            "personalize",
            "polly",
            "rekognition",
            "transcribe",
            "translate",
        ),
    ),
    (
        "Application integration",
        (
            "sns",
            "sqs",
            "mq",
            "eventbridge",
            "step-functions",
            "ses",
            "connect",
        ),
    ),
    (
        "Security, identity & compliance",
        (
            "iam",
            "iam-identity-center",
            "cognito",
            "directory-service",
            "acm",
            "kms",
            "cloudhsm",
            "secrets-manager",
            "guardduty",
            "inspector",
            "detective",
            "macie",
            "security-hub",
            "shield",
            "waf",
            "artifact",
        ),
    ),
    (
        "Governance & operations",
        (
            "cloudwatch",
            "cloudtrail",
            "config",
            "systems-manager",
            "x-ray",
            "trusted-advisor",
            "health",
            "service-catalog",
            "service-quotas",
            "license-manager",
            "resource-groups-tag-editor",
            "organizations",
            "control-tower",
            "ram",
            "managed-services",
        ),
    ),
    (
        "Developer tools & IaC",
        (
            "cloudformation",
            "cdk",
            "sam",
            "solutions-constructs",
            "codebuild",
            "codecommit",
            "codedeploy",
            "codepipeline",
            "codeartifact",
            "codeguru",
            "codestar",
            "cloud9",
            "cli",
            "sdk",
            "boto3",
            "amplify",
        ),
    ),
)

# A topic directory's H1 is an article title ("Essential Git Commands for
# Operations"), which is too long to read as a sidebar group. These override it.
AREA_NAV_LABELS = {
    "Bash": "Bash",
    "Ghostty": "Ghostty",
    "Git": "Git",
    "Nginx": "Nginx & OpenResty",
    "Nodejs": "Node.js & Express BFF",
    "Python": "Python",
    "youtube-transcript": "Transcript tooling",
}

NAV_SECTIONS: tuple[tuple[str, tuple[str, ...]], ...] = (
    ("Troubleshooting", ("Git", "Kubernetes", "Nginx", "Nodejs", "ZooKeeper")),
    ("AWS", ("AWS",)),
    ("AI coding tools", ("Claude",)),
    ("Languages & practice", ("Python", "Bash")),
    ("Setup", ("Ghostty", "Ubuntu", "apple", "youtube-transcript")),
    ("Video notes", ("YouTube",)),
)


def _nav_label(title: str) -> str:
    """Trim the shared article-title suffix so sidebar entries stay scannable."""

    for suffix in NAV_LABEL_SUFFIXES:
        if title.endswith(suffix):
            return title[: -len(suffix)].strip()
    return title


def _nav_entry(document: Document, indent: str) -> str:
    return f"{indent}- [{_escape_markdown_label(_nav_label(document.title))}]({document.page})"


def _escape_markdown_label(label: str) -> str:
    return label.replace("[", r"\[").replace("]", r"\]")


def _aws_nav_lines(by_page: dict[str, Document], indent: str) -> list[str]:
    """Split AWS into service families; anything unmapped lands in `More`."""

    lines: list[str] = []
    claimed: set[str] = set()
    for group_name, slugs in AWS_GROUPS:
        entries = []
        for slug in slugs:
            page = f"AWS/{slug}/index.md"
            document = by_page.get(page)
            if document is None:
                continue
            claimed.add(page)
            entries.append(_nav_entry(document, indent + "    "))
        if entries:
            lines.append(f"{indent}- {group_name}")
            lines.extend(entries)
    leftovers = [
        document
        for page, document in sorted(by_page.items())
        if page.startswith("AWS/") and page != "AWS/index.md" and page not in claimed
    ]
    if leftovers:
        lines.append(f"{indent}- More")
        lines.extend(_nav_entry(document, indent + "    ") for document in leftovers)
    return lines


def _summary_markdown(documents: list[Document]) -> str:
    """Render the literate-nav SUMMARY.md for the site."""

    by_page = {document.page: document for document in documents}
    lines = [
        "- [Home](index.md)",
    ]
    for section_name, areas in NAV_SECTIONS:
        section_lines: list[str] = []
        for area in areas:
            root_page = f"{area}/index.md"
            root = by_page.get(root_page)
            children = sorted(
                (
                    document
                    for page, document in by_page.items()
                    if page.startswith(f"{area}/") and page != root_page
                ),
                key=lambda document: document.page,
            )
            if area == "AWS":
                if root is not None:
                    section_lines.append(_nav_entry(root, "    "))
                section_lines.extend(_aws_nav_lines(by_page, "    "))
                continue
            if root is None and not children:
                continue
            if len(areas) == 1:
                if root is not None:
                    section_lines.append(_nav_entry(root, "    "))
                section_lines.extend(_nav_entry(child, "    ") for child in children)
                continue
            if root is not None and not children:
                # A topic with no sub-articles is a link, not a one-item group.
                section_lines.append(_nav_entry(root, "    "))
                continue
            if root is None and len(children) == 1:
                # A container directory with a single article (apple/container)
                # reads better as that article than as a one-item group.
                section_lines.append(_nav_entry(children[0], "    "))
                continue
            label = AREA_NAV_LABELS.get(area) or (
                _nav_label(root.title) if root is not None else area
            )
            section_lines.append(f"    - {_escape_markdown_label(label)}")
            if root is not None:
                section_lines.append(_nav_entry(root, "        "))
            section_lines.extend(_nav_entry(child, "        ") for child in children)
        if section_lines:
            lines.append(f"- {section_name}")
            lines.extend(section_lines)
    lines.extend(
        [
            "- Browse",
            "    - [Topics](topics/index.md)",
            "    - [Repository overview](repository/index.md)",
            "    - [Archive](archive/index.md)",
        ]
    )
    return "\n".join(lines) + "\n"


# --------------------------------------------------------------------------
# Home page content
#
# The home page answers two questions before anything else: "where is my
# topic" and "what do I do when something is broken". Neither can be derived
# from the tree — a topic directory's H1 is an article title, and no metadata
# says which runbook a reader in an incident wants — so both are curated here.
# --------------------------------------------------------------------------

# area -> (name, blurb)
TOPIC_META: dict[str, tuple[str, str]] = {
    "AWS": ("AWS", "Service-by-service runbooks and references"),
    "Git": ("Git", "Sync, publish, release and recovery"),
    "Kubernetes": ("Kubernetes", "Scheduling failures and incident runbooks"),
    "Nginx": ("Nginx & OpenResty", "Deployment and reload semantics"),
    "Nodejs": ("Node.js & Express BFF", "Deployment and incident response"),
    "ZooKeeper": ("ZooKeeper", "Quorum, snapshots and recovery"),
    "Python": ("Python", "SRE exercises and language cheatsheets"),
    "Bash": ("Bash", "Log analysis on the command line"),
    "Claude": ("AI coding tools", "Claude Code, agents and skills"),
    "YouTube": ("Video notes", "Summaries of talks on startups and AI"),
    "Ghostty": ("Ghostty", "Terminal setup and a reusable config"),
    "Ubuntu": ("Ubuntu APT", "Install, upgrade and troubleshoot packages"),
    "apple": ("Apple Container", "Architecture, usage and limitations"),
}

# Repository tooling is not something a reader browses for, so it stays in the
# nav under Setup but off the home page.
HOME_TOPIC_EXCLUDE = {"youtube-transcript"}

# The home page shows this many notes before handing over to the archive.
HOME_FEED_LIMIT = 20


def _topic_name(area: str, fallback: str) -> str:
    meta = TOPIC_META.get(area)
    return meta[0] if meta else fallback


def _topic_blurb(area: str) -> str:
    meta = TOPIC_META.get(area)
    return meta[1] if meta else ""


def _area_note_count(documents: list[Document], area: str) -> int:
    return sum(
        document.area == area and document.kind in BLOG_KINDS
        for document in documents
    )


def _home_areas(documents: list[Document]) -> list[str]:
    """Topics offered on the home page, deepest first."""

    areas = {
        document.area
        for document in documents
        if document.area != "engineering" and document.area not in HOME_TOPIC_EXCLUDE
    }
    return sorted(
        areas,
        key=lambda area: (-_area_note_count(documents, area), area.lower()),
    )


def _topic_tile_html(
    documents: list[Document],
    area: str,
    source_page: str,
) -> str:
    catalog = _topic_catalog(documents, area)
    if catalog is None:
        return ""
    count = _area_note_count(documents, area)
    # A topic whose only page is its own overview still deserves a tile;
    # claiming "0 notes" would read as an empty section.
    count_label = "Overview" if count == 0 else f"{count} note" if count == 1 else f"{count} notes"
    blurb = _topic_blurb(area)
    blurb_html = (
        f'<span class="kb-topic-card__blurb">{_escape(blurb)}</span>' if blurb else ""
    )
    return (
        f'<a class="kb-topic-card" href="{_escape(_relative_site_url(source_page, catalog.page))}">'
        f'<span class="kb-topic-card__monogram" aria-hidden="true">'
        f"{_escape(_monogram(area))}</span>"
        '<span class="kb-topic-card__body">'
        f'<span class="kb-topic-card__name">'
        f"{_escape(_topic_name(area, catalog.title))}</span>"
        f"{blurb_html}"
        f'<span class="kb-topic-card__count">{_escape(count_label)}</span>'
        "</span>"
        "</a>"
    )


def _topics_page(documents: list[Document]) -> str:
    """The secondary entry point: the same notes, reachable by subject."""

    page = "topics/index.md"
    title = "Topics"
    description = (
        "The timeline is the main way in. Use this when you already know the "
        "subject you need."
    )
    cards = "\n".join(
        _topic_tile_html(documents, area, page) for area in _home_areas(documents)
    )
    return _generated_front_matter(
        title=title,
        hide_toc=True,
        hide_footer=True,
        search_exclude=True,
    ) + "\n".join(
        [
            f"# {title}",
            "",
            '<div class="kb-hub">',
            f'<p class="kb-hub__lede">{_escape(description)}</p>',
            f'<div class="kb-topic-grid">{cards}</div>',
            "</div>",
            "",
        ]
    )


def _archive_years(documents: list[Document]) -> list[tuple[str, list[Document]]]:
    """Notes grouped by publication year, newest year first."""

    grouped: dict[str, list[Document]] = {}
    for document in _blog_documents(documents):
        year = document.published[:4] if document.published else "undated"
        grouped.setdefault(year, []).append(document)
    years = sorted((year for year in grouped if year != "undated"), reverse=True)
    if "undated" in grouped:
        years.append("undated")
    return [(year, grouped[year]) for year in years]


def _archive_page_path(year: str | None) -> str:
    if year is None:
        return "archive/index.md"
    return f"archive/{year}/index.md"


def _year_nav_html(years: list[str], source_page: str, active: str) -> str:
    """One link per year, so the archive never grows into a single long page."""

    if len(years) < 2:
        return ""
    newest = years[0]
    rendered = []
    for year in years:
        label = year if year != "undated" else "Undated"
        target = _archive_page_path(None if year == newest else year)
        is_active = year == active
        classes = "kb-tab kb-tab--active" if is_active else "kb-tab"
        current = ' aria-current="page"' if is_active else ""
        rendered.append(
            f'<a class="{classes}" '
            f'href="{_escape(_relative_site_url(source_page, target))}"{current}>'
            f"{_escape(label)}</a>"
        )
    return f'<nav class="kb-tabs" aria-label="Archive by year">{"".join(rendered)}</nav>'


def _archive_page(documents: list[Document], year: str | None = None) -> str:
    """Every note of one year, one line each, newest first."""

    years = _archive_years(documents)
    labels = [label for label, _ in years]
    active = year or (labels[0] if labels else "")
    notes = next((entries for label, entries in years if label == active), [])
    page = _archive_page_path(None if year is None else year)
    title = "Archive"
    if len(labels) > 1:
        title = f"{title} · {active}" if active else title
    description = f"{len(notes)} notes published in {active}, newest first."
    if len(labels) <= 1:
        description = f"All {len(notes)} notes, newest first."
    feed = _dense_feed_html(notes, page)
    empty = '<p class="kb-empty">No published notes yet.</p>'
    return _generated_front_matter(
        title=title,
        hide_toc=True,
        hide_footer=True,
        search_exclude=True,
    ) + "\n".join(
        [
            f"# {title}",
            "",
            '<div class="kb-hub kb-archive">',
            f'<p class="kb-hub__lede">{_escape(description)}</p>',
            _year_nav_html(labels, page, active),
            feed if feed else empty,
            "</div>",
            "",
        ]
    )


# --------------------------------------------------------------------------
# Feed
#
# A timeline blog is something a reader may want to follow rather than
# revisit, so the site publishes an RSS feed of its newest notes.
# --------------------------------------------------------------------------

SITE_URL = "https://blog.kelvin.ink/"
FEED_LIMIT = 20
RFC822_DAYS = ("Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun")


def _page_url(page: str) -> str:
    """`AWS/acm/index.md` -> `https://blog.kelvin.ink/AWS/acm/`."""

    path = page[: -len("index.md")] if page.endswith("index.md") else page
    return SITE_URL + quote(path.lstrip("/"), safe="/")


def _rfc822(date: str) -> str:
    if not date:
        return ""
    stamp = datetime.date.fromisoformat(date)
    day = RFC822_DAYS[stamp.weekday()]
    month = MONTH_NAMES_EN[stamp.month - 1][:3]
    return f"{day}, {stamp.day:02d} {month} {stamp.year} 00:00:00 +0000"


def _feed_xml(documents: list[Document], excerpts: dict[str, str]) -> str:
    notes = _blog_documents(documents)[:FEED_LIMIT]
    title = "Kelvin’s Engineering Notes"
    description = "Runbooks, references and distilled study notes, newest first."
    home = _page_url("index.md")
    feed_path = "feed.xml"
    items = []
    for document in notes:
        published = _rfc822(document.published)
        date = f"    <pubDate>{published}</pubDate>\n" if published else ""
        excerpt = excerpts.get(document.source, "")
        summary = f"    <description>{_escape(excerpt)}</description>\n" if excerpt else ""
        url = _page_url(document.page)
        items.append(
            "  <item>\n"
            f"    <title>{_escape(document.title)}</title>\n"
            f"    <link>{_escape(url)}</link>\n"
            f"    <guid isPermaLink=\"true\">{_escape(url)}</guid>\n"
            f"{date}"
            f"{summary}"
            f"    <category>{_escape(_kind_label(document.kind))}</category>\n"
            "  </item>"
        )
    return (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom">\n'
        "<channel>\n"
        f"  <title>{_escape(title)}</title>\n"
        f"  <link>{_escape(home)}</link>\n"
        f"  <description>{_escape(description)}</description>\n"
        "  <language>en</language>\n"
        f'  <atom:link href="{_escape(SITE_URL + feed_path)}" rel="self" '
        'type="application/rss+xml"/>\n'
        + "\n".join(items)
        + "\n</channel>\n</rss>\n"
    )


def stage(root: Path, output: Path, paths: list[str] | None = None) -> list[Document]:
    """Create a clean MkDocs source tree without changing canonical files."""

    documents = discover_documents(root, paths)
    page_map = {document.source: document.page for document in documents}
    tracked = set(_git_tracked_paths(root) if paths is None else paths)
    if output.exists():
        if not output.is_dir() or output.resolve() == root.resolve():
            raise KnowledgeBaseError(f"refusing to replace output path {output}")
        shutil.rmtree(output)
    output.mkdir(parents=True)

    excerpts: dict[str, str] = {}
    for document in documents:
        raw = (root / document.source).read_text(encoding="utf-8")
        excerpts[document.source] = _excerpt(raw)
        reading = _reading_label(raw)
        text = rewrite_links(raw, document.source, page_map, tracked)
        text = _with_generated_metadata(text, document)
        text = _with_generated_context(text, document, reading)
        text = text.rstrip("\n") + "\n" + _related_html(document, documents)
        target = output / document.page
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(text, encoding="utf-8")

    generated_pages = {
        "topics/index.md": _topics_page(documents),
        "SUMMARY.md": _summary_markdown(documents),
        "feed.xml": _feed_xml(documents, excerpts),
    }
    years = [label for label, _ in _archive_years(documents)]
    # The newest year is the archive's front page; older years get one
    # page each, so the list never grows without bound.
    generated_pages[_archive_page_path(None)] = _archive_page(documents)
    for year in years[1:]:
        generated_pages[_archive_page_path(year)] = _archive_page(documents, year)

    home = _home_page()
    generated_pages[home] = _timeline_page(
        documents,
        home,
        kind=None,
        excerpts=excerpts,
        dense_limit=HOME_DENSE_LIMIT,
    )
    # A kind page is the same timeline with the other kinds taken out, so
    # it stays complete rather than capping like the home page.
    for kind in KIND_SLUGS:
        if not any(document.kind == kind for document in documents):
            continue
        page = _kind_page(kind)
        generated_pages[page] = _timeline_page(
            documents,
            page,
            kind=kind,
            excerpts=excerpts,
        )

    existing_pages = set(page_map.values())
    conflicts = sorted(existing_pages.intersection(generated_pages))
    if conflicts:
        raise KnowledgeBaseError(
            f"generated page paths conflict with staged documents: {', '.join(conflicts)}"
        )
    for page, text in generated_pages.items():
        target = output / page
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(text, encoding="utf-8")

    css_source = root / PRESENTATION_CSS
    if not css_source.is_file():
        raise KnowledgeBaseError(f"missing presentation stylesheet {PRESENTATION_CSS}")
    css_target = output / STAGED_CSS
    css_target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(css_source, css_target)

    assets_source = root / PRESENTATION_ASSETS
    if assets_source.is_dir():
        shutil.copytree(assets_source, output / STAGED_ASSETS, dirs_exist_ok=True)
    return documents


def _parse_args(argv: list[str] | None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    subparsers = parser.add_subparsers(dest="command", required=True)
    subparsers.add_parser("validate", help="validate the public Markdown contract")
    stage_parser = subparsers.add_parser("stage", help="stage public Markdown for MkDocs")
    stage_parser.add_argument("--output", type=Path, required=True)
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = _parse_args(argv)
    root = args.root.resolve()
    try:
        if args.command == "validate":
            documents = discover_documents(root)
            print(f"validated {len(documents)} documents")
        else:
            output = args.output if args.output.is_absolute() else root / args.output
            documents = stage(root, output)
            print(f"staged {len(documents)} documents in {output}")
    except (KnowledgeBaseError, OSError) as exc:
        print(f"knowledge-base: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
