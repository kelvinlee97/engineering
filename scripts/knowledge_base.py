#!/usr/bin/env python3
"""Validate and stage the public Markdown knowledge base for MkDocs."""

from __future__ import annotations

import argparse
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
PUBLISHABLE_NAMES = {"README.md", "README_ZH.md", "summary.md", "summary_zh.md"}
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
    "en": {
        "guide": "Guide",
        "runbook": "Runbook",
        "reference": "Reference",
        "tooling": "Tooling",
        "video-summary": "Video summary",
        "catalog": "Catalog",
    },
    "zh": {
        "guide": "指南",
        "runbook": "运维手册",
        "reference": "参考",
        "tooling": "工具",
        "video-summary": "视频摘要",
        "catalog": "目录",
    },
}
BLOG_KINDS = set(KIND_LABELS["en"]) - {"catalog"}
# Reading pace used for the per-article estimate: Latin words and CJK characters are
# consumed at different rates, so each is counted against its own budget.
LATIN_WORDS_PER_MINUTE = 220
CJK_CHARS_PER_MINUTE = 400
EXCERPT_LENGTH = 150
# CJK packs far more meaning per character, so its cards get a shorter budget.
CJK_EXCERPT_LENGTH = 72
RELATED_LIMIT = 4
LANGUAGE_LINE_MARKERS = (
    "Chinese version",
    "English version",
    "中文版本",
    "简体中文",
)
CJK_RE = re.compile(r"[\u3400-\u9fff\u3040-\u30ff]")
LATIN_WORD_RE = re.compile(r"[A-Za-z0-9][A-Za-z0-9'\u2019./_-]*")


class KnowledgeBaseError(Exception):
    """Raised when the public knowledge-base contract is invalid."""


@dataclass(frozen=True)
class Document:
    source: str
    page: str
    pair_source: str
    pair_page: str
    title: str
    pair_title: str
    language: str
    area: str
    kind: str
    updated: str
    # Full commit timestamp behind `updated`. `updated` is a date, so two notes
    # touched on the same day tie; ordering by the timestamp keeps the most
    # recent edit first.
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


def _pair_path(source: str) -> str:
    path = PurePosixPath(source)
    pair_name = {
        "README.md": "README_ZH.md",
        "README_ZH.md": "README.md",
        "summary.md": "summary_zh.md",
        "summary_zh.md": "summary.md",
    }[path.name]
    return _normalise_path(path.parent / pair_name)


def _page_path(source: str) -> str:
    path = PurePosixPath(source)
    if path.name == "README.md":
        parent = path.parent if path.parent != PurePosixPath(".") else PurePosixPath("repository")
        return _normalise_path(parent / "index.md")
    if path.name == "README_ZH.md":
        parent = path.parent if path.parent != PurePosixPath(".") else PurePosixPath("repository")
        return _normalise_path(parent / "index_zh.md")
    return path.as_posix()


def _extract_title(text: str, source: str) -> str:
    match = H1_RE.search(text)
    if not match:
        raise KnowledgeBaseError(f"{source}: missing level-one heading")
    title = match.group(1).strip()
    title = re.sub(r"\[([^]]+)\]\([^)]*\)", r"\1", title)
    title = title.replace("`", "").replace("*", "").replace("_", "")
    return title.strip()


def _kind_label(kind: str, language: str) -> str:
    return KIND_LABELS[language].get(kind, kind.replace("-", " ").title())


def _strip_markdown(text: str) -> str:
    """Reduce Markdown to prose so word counts and excerpts ignore syntax."""

    text = re.sub(r"(?ms)^```.*?^```\s*$", " ", text)
    text = re.sub(r"(?m)^\s{0,3}(---|\*\*\*|___)\s*$", " ", text)
    text = re.sub(r"<[^>]+>", " ", text)
    text = re.sub(r"!\[[^\]]*\]\([^)]*\)", " ", text)
    text = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", text)
    text = re.sub(r"[`*_#>|]", " ", text)
    return text


def _reading_minutes(text: str) -> int:
    """Estimate reading time in whole minutes, never less than one."""

    body = _strip_markdown(text)
    cjk = len(CJK_RE.findall(body))
    latin = len(LATIN_WORD_RE.findall(CJK_RE.sub(" ", body)))
    minutes = latin / LATIN_WORDS_PER_MINUTE + cjk / CJK_CHARS_PER_MINUTE
    return max(1, round(minutes))


def _reading_label(text: str, language: str) -> str:
    minutes = _reading_minutes(text)
    if language == "en":
        return f"{minutes} min read"
    return f"约 {minutes} 分钟"


def _excerpt(text: str, language: str) -> str:
    """First real paragraph of a document, trimmed for use on a card."""

    body = text
    if body.startswith("---\n"):
        closing = body.find("\n---\n", 4)
        if closing != -1:
            body = body[closing + 5 :]
    match = H1_RE.search(body)
    if match:
        body = body[match.end() :]
    for block in re.split(r"\n\s*\n", body):
        block = block.strip()
        if not block or block.startswith((">", "#", "|", "-", "*", "<", "```", "!")):
            continue
        candidate = " ".join(_strip_markdown(block).split())
        # Skip the reciprocal language-switch line that opens most documents, plus
        # any other one-liner too short to describe the note.
        if not candidate or len(candidate) < 40:
            continue
        if any(marker in candidate for marker in LANGUAGE_LINE_MARKERS):
            continue
        # A colon-terminated line introduces the list that follows; on its own
        # it describes nothing, and many articles open with the same one.
        if candidate.endswith((":", "\uff1a")):
            continue
        limit = EXCERPT_LENGTH if language == "en" else CJK_EXCERPT_LENGTH
        if len(candidate) <= limit:
            return candidate
        cut = candidate[:limit]
        if language == "en" and " " in cut:
            cut = cut[: cut.rindex(" ")]
        return cut.rstrip(" ,.;:、，。") + "…"
    return ""


def _blog_documents(documents: list[Document], language: str) -> list[Document]:
    return _sorted_documents(
        [
            document
            for document in documents
            if document.language == language and document.kind in BLOG_KINDS
        ]
    )


def _sorted_documents(documents: list[Document]) -> list[Document]:
    by_source = sorted(documents, key=lambda document: document.source)
    return sorted(
        by_source,
        key=lambda document: (document.updated or "", document.updated_at or ""),
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
    language: str,
    *,
    title: str | None = None,
    hide_navigation: bool = False,
    hide_toc: bool = False,
    hide_footer: bool = False,
    search_exclude: bool = False,
) -> str:
    lines = ["---", f"kb_language: {language}"]
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
    metadata = f"kb_language: {document.language}"
    if text.startswith("---\n"):
        closing = text.find("\n---\n", 4)
        if closing != -1:
            front_matter = text[4:closing]
            if re.search(r"(?m)^kb_language:", front_matter):
                front_matter = re.sub(
                    r"(?m)^kb_language:.*$",
                    metadata,
                    front_matter,
                    count=1,
                )
            else:
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


def _language(source: str) -> str:
    name = PurePosixPath(source).name
    return "zh" if name.endswith("_ZH.md") or name == "summary_zh.md" else "en"


def _kind(source: str) -> str:
    path = PurePosixPath(source)
    lower_parts = {part.lower() for part in path.parts}
    if path.name.startswith("summary"):
        return "video-summary"
    if "youtube-transcript" in lower_parts or "rss-digest" in lower_parts:
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


def _last_modified(root: Path, source: str) -> tuple[str, str]:
    """Commit date (for display) and full commit timestamp (for ordering)."""

    if not (root / ".git").exists():
        return "", ""
    result = subprocess.run(
        ["git", "-C", str(root), "log", "-1", "--format=%cs%n%cI", "--", source],
        capture_output=True,
        text=True,
        check=False,
    )
    lines = result.stdout.strip().splitlines()
    if len(lines) < 2:
        return (lines[0].strip() if lines else ""), ""
    return lines[0].strip(), lines[1].strip()


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
        pair = _pair_path(source)
        if pair not in candidates:
            errors.append(f"{source}: missing paired document {pair}")
            continue
        if PurePosixPath(source).name.startswith("summary") and video_ids.get(source) is None:
            errors.append(f"{source}: missing YouTube source URL")
        if source < pair and video_ids.get(source) != video_ids.get(pair):
            errors.append(f"{source}: paired summaries use different YouTube video IDs")
        if source < pair and mermaid_types.get(source) != mermaid_types.get(pair):
            errors.append(
                f"{source}: paired documents use different Mermaid diagram types or order"
            )

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
        pair = _pair_path(source)
        modified = _last_modified(root, source)
        documents.append(
            Document(
                source=source,
                page=_page_path(source),
                pair_source=pair,
                pair_page=_page_path(pair),
                title=titles[source],
                pair_title=titles[pair],
                language=_language(source),
                area=_area(source),
                kind=_kind(source),
                updated=modified[0],
                updated_at=modified[1],
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


def _with_generated_context(text: str, document: Document, reading: str = '') -> str:
    match = H1_RE.search(text)
    if not match:
        return text
    pair_label = "中文" if document.language == "en" else "English"
    pair_link = _relative_site_url(document.page, document.pair_page)
    source_link = f"{GITHUB_BLOB_URL}/{quote(document.source, safe='/')}"
    language_aria = "Switch to Chinese" if document.language == "en" else "切换到 English"
    metadata_aria = "Page metadata" if document.language == "en" else "页面信息"
    kind_label = _kind_label(document.kind, document.language)
    updated = ""
    if document.updated:
        updated_label = "Updated" if document.language == "en" else "更新于"
        updated = (
            f'  <time datetime="{_escape(document.updated)}">'
            f"{updated_label} {_escape(document.updated)}</time>\n"
        )
    reading_html = ""
    if reading:
        reading_html = f'  <span class="kb-meta__reading">{_escape(reading)}</span>\n'
    context = (
        "\n\n"
        f'<div class="kb-meta" role="group" aria-label="{metadata_aria}">\n'
        f'  <span class="kb-meta__kind">{_escape(kind_label)}</span>\n'
        f"{updated}"
        f"{reading_html}"
        f'  <a class="kb-meta__language" href="{_escape(pair_link)}" '
        f'aria-label="{language_aria}">{pair_label}</a>\n'
        f'  <a class="kb-meta__source" href="{_escape(source_link)}">GitHub source</a>\n'
        "</div>"
    )
    return text[: match.end()] + context + text[match.end() :]


def _entry_html(document: Document, source_page: str) -> str:
    date = ""
    if document.updated:
        date = (
            f' <time datetime="{_escape(document.updated)}">'
            f"{_escape(document.updated)}</time>"
    )
    return (
        '<li class="kb-entry">'
        f'<a class="kb-entry__link" '
        f'href="{_escape(_relative_site_url(source_page, document.page))}">'
        f'<span class="kb-entry__title">{_escape(document.title)}</span>'
        f'<span class="kb-entry__meta">'
        f'<span class="kb-chip">{_escape(_kind_label(document.kind, document.language))}</span>'
        f"{date}</span>"
        "</a>"
        "</li>"
    )


def _topic_catalog(documents: list[Document], area: str, language: str) -> Document | None:
    area_documents = [
        document
        for document in documents
        if document.area == area and document.language == language
    ]
    return next(
        (document for document in area_documents if document.kind == "catalog"),
        area_documents[0] if area_documents else None,
    )


def _topic_card_html(documents: list[Document], area: str, language: str, source_page: str) -> str:
    catalog = _topic_catalog(documents, area, language)
    if catalog is None:
        return ""
    count = sum(
        document.language == language
        and document.area == area
        and document.kind in BLOG_KINDS
        for document in documents
    )
    if language == "en":
        count_label = f"{count} note" if count == 1 else f"{count} notes"
    else:
        count_label = f"{count} 篇笔记"
    monogram = _monogram(area)
    return (
        f'<a class="kb-topic-card" href="{_escape(_relative_site_url(source_page, catalog.page))}">'
        f'<span class="kb-topic-card__monogram" aria-hidden="true">{_escape(monogram)}</span>'
        '<span class="kb-topic-card__body">'
        f'<span class="kb-topic-card__name">{_escape(catalog.title)}</span>'
        f'<span class="kb-topic-card__count">{count_label}</span>'
        "</span>"
        "</a>"
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
    excerpts: dict[str, str] | None = None,
) -> str:
    """End-of-article links to nearby notes, so a reader has somewhere to go next."""

    if document.kind == "catalog":
        return ""
    pool = [
        candidate
        for candidate in _blog_documents(documents, document.language)
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
    is_english = document.language == "en"
    heading = "Keep reading" if is_english else "继续阅读"
    aria = "Related notes" if is_english else "相关笔记"
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
            f"{_escape(_kind_label(candidate.kind, candidate.language))}</span>"
            f"{date}"
            "</span>"
            "</a>"
        )
    return (
        "\n\n"
        f'<section class="kb-related" aria-label="{aria}">\n'
        f'<h2 class="kb-related__title">{heading}</h2>\n'
        f'<div class="kb-related__grid">{"".join(cards)}</div>\n'
        "</section>\n"
    )


def _stats_html(documents: list[Document], language: str) -> str:
    notes = _blog_documents(documents, language)
    # Count the topics the home page actually offers, so the stat and the
    # tile grid can never disagree.
    areas = _home_areas(documents, language)
    updated = next((document.updated for document in notes if document.updated), "")
    is_english = language == "en"
    items = [
        (str(len(notes)), "notes" if is_english else "篇笔记"),
        (str(len(areas)), "topics" if is_english else "个主题"),
    ]
    if updated:
        items.append((updated, "last updated" if is_english else "最近更新"))
    cells = "".join(
        f'<li class="kb-stat"><span class="kb-stat__value">{_escape(value)}</span>'
        f'<span class="kb-stat__label">{_escape(label)}</span></li>'
        for value, label in items
    )
    aria = "Knowledge base statistics" if is_english else "知识库统计"
    return f'<ul class="kb-stats" aria-label="{aria}">{cells}</ul>'



# --------------------------------------------------------------------------
# Navigation
#
# MkDocs builds its navigation from the staged tree, which is flat and
# alphabetical: AWS alone contributes 123 pages, so an auto-generated nav
# buries every other topic. The constants below group the tree into eight
# top-level sections (rendered as tabs) and split AWS into service families,
# and `_summary_markdown` emits them as the literate-nav SUMMARY.md.
#
# Chinese pages are deliberately left out of the nav: they double every entry
# and are reached through the language link each article carries.
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
    "rss-digest": "RSS digest tooling",
    "youtube-transcript": "Transcript tooling",
}

NAV_SECTIONS: tuple[tuple[str, tuple[str, ...]], ...] = (
    ("Troubleshooting", ("Git", "Kubernetes", "Nginx", "Nodejs", "ZooKeeper")),
    ("AWS", ("AWS",)),
    ("AI coding tools", ("Claude",)),
    ("Languages & practice", ("Python", "Bash")),
    ("Setup", ("Ghostty", "Ubuntu", "apple", "rss-digest", "youtube-transcript")),
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
    """Render the literate-nav SUMMARY.md for the English tree."""

    by_page = {
        document.page: document
        for document in documents
        if document.language == "en"
    }
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
            # A top-level entry, so the Chinese home page gets its own tab
            # rather than sitting under Browse — which made every Chinese
            # page render the breadcrumb "Home > Browse".
            "- [中文](index_zh.md)",
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

# area -> (English name, Chinese name, English blurb, Chinese blurb)
TOPIC_META: dict[str, tuple[str, str, str, str]] = {
    "AWS": (
        "AWS",
        "AWS",
        "Service-by-service runbooks and references",
        "按服务整理的运维手册与参考",
    ),
    "Git": (
        "Git",
        "Git",
        "Sync, publish, release and recovery",
        "同步、发布、回滚与恢复",
    ),
    "Kubernetes": (
        "Kubernetes",
        "Kubernetes",
        "Scheduling failures and incident runbooks",
        "调度失败与故障处理手册",
    ),
    "Nginx": (
        "Nginx & OpenResty",
        "Nginx 与 OpenResty",
        "Deployment and reload semantics",
        "部署与 reload 行为",
    ),
    "Nodejs": (
        "Node.js & Express BFF",
        "Node.js 与 Express BFF",
        "Deployment and incident response",
        "部署与故障响应",
    ),
    "ZooKeeper": (
        "ZooKeeper",
        "ZooKeeper",
        "Quorum, snapshots and recovery",
        "quorum、快照与恢复",
    ),
    "Python": (
        "Python",
        "Python",
        "SRE exercises and language cheatsheets",
        "SRE 练习与语言速查",
    ),
    "Bash": (
        "Bash",
        "Bash",
        "Log analysis on the command line",
        "命令行日志分析",
    ),
    "Claude": (
        "AI coding tools",
        "AI 编程工具",
        "Claude Code, agents and skills",
        "Claude Code、agent 与 skills",
    ),
    "YouTube": (
        "Video notes",
        "视频笔记",
        "Summaries of talks on startups and AI",
        "创业与 AI 演讲摘要",
    ),
    "Ghostty": (
        "Ghostty",
        "Ghostty",
        "Terminal setup and a reusable config",
        "终端配置与可复用配置文件",
    ),
    "Ubuntu": (
        "Ubuntu APT",
        "Ubuntu APT",
        "Install, upgrade and troubleshoot packages",
        "安装、升级与排查软件包",
    ),
    "apple": (
        "Apple Container",
        "Apple Container",
        "Architecture, usage and limitations",
        "架构、用法与限制",
    ),
}

# Repository tooling is not something a reader browses for, so it stays in the
# nav under Setup but off the home page.
HOME_TOPIC_EXCLUDE = {"rss-digest", "youtube-transcript"}

# (page, English question, Chinese question, English answer, Chinese answer)
SYMPTOM_ENTRIES: tuple[tuple[str, str, str, str, str], ...] = (
    (
        "Kubernetes/runbooks/insufficient-ip-or-eni/index.md",
        "A Pod is stuck Pending",
        "Pod 一直是 Pending",
        "Is it IP capacity, or something else?",
        "是 IP 容量不够，还是别的原因？",
    ),
    (
        "Git/index.md",
        "Branches have diverged",
        "分支分叉了",
        "Read the state before picking a sync strategy.",
        "先看清状态，再选同步策略。",
    ),
    (
        "Nodejs/runbooks/common-express-bff-incidents/index.md",
        "The BFF started timing out",
        "BFF 开始超时",
        "Ten common Express incidents and their checks.",
        "十种常见 Express 故障及排查步骤。",
    ),
)

# At most two notes per topic, so a topic with 123 pages cannot fill the list.
LATEST_PER_AREA = 2
LATEST_LIMIT = 8


def _topic_name(area: str, language: str, fallback: str) -> str:
    meta = TOPIC_META.get(area)
    if meta is None:
        return fallback
    return meta[0] if language == "en" else meta[1]


def _topic_blurb(area: str, language: str) -> str:
    meta = TOPIC_META.get(area)
    if meta is None:
        return ""
    return meta[2] if language == "en" else meta[3]


def _area_note_count(documents: list[Document], area: str, language: str) -> int:
    return sum(
        document.language == language
        and document.area == area
        and document.kind in BLOG_KINDS
        for document in documents
    )


def _home_areas(documents: list[Document], language: str) -> list[str]:
    """Topics offered on the home page, deepest first."""

    areas = {
        document.area
        for document in documents
        if document.language == language
        and document.area != "engineering"
        and document.area not in HOME_TOPIC_EXCLUDE
    }
    return sorted(
        areas,
        key=lambda area: (-_area_note_count(documents, area, language), area.lower()),
    )


def _topic_tile_html(
    documents: list[Document],
    area: str,
    language: str,
    source_page: str,
) -> str:
    catalog = _topic_catalog(documents, area, language)
    if catalog is None:
        return ""
    count = _area_note_count(documents, area, language)
    if count == 0:
        # A topic whose only page is its own overview still deserves a tile;
        # claiming "0 notes" would read as an empty section.
        count_label = "Overview" if language == "en" else "概览"
    elif language == "en":
        count_label = f"{count} note" if count == 1 else f"{count} notes"
    else:
        count_label = f"{count} 篇笔记"
    blurb = _topic_blurb(area, language)
    blurb_html = (
        f'<span class="kb-topic-card__blurb">{_escape(blurb)}</span>' if blurb else ""
    )
    return (
        f'<a class="kb-topic-card" href="{_escape(_relative_site_url(source_page, catalog.page))}">'
        f'<span class="kb-topic-card__monogram" aria-hidden="true">'
        f"{_escape(_monogram(area))}</span>"
        '<span class="kb-topic-card__body">'
        f'<span class="kb-topic-card__name">'
        f"{_escape(_topic_name(area, language, catalog.title))}</span>"
        f"{blurb_html}"
        f'<span class="kb-topic-card__count">{_escape(count_label)}</span>'
        "</span>"
        "</a>"
    )


def _symptoms_html(documents: list[Document], language: str, source_page: str) -> str:
    pages = {
        document.page for document in documents if document.language == language
    }
    is_english = language == "en"
    cards = []
    for page, question_en, question_zh, answer_en, answer_zh in SYMPTOM_ENTRIES:
        target = page if is_english else page.replace("index.md", "index_zh.md")
        if target not in pages:
            continue
        question = question_en if is_english else question_zh
        answer = answer_en if is_english else answer_zh
        cards.append(
            f'<a class="kb-symptom" href="{_escape(_relative_site_url(source_page, target))}">'
            f'<span class="kb-symptom__question">{_escape(question)}</span>'
            f'<span class="kb-symptom__answer">{_escape(answer)}</span>'
            "</a>"
        )
    return "".join(cards)


def _latest_documents(documents: list[Document], language: str) -> list[Document]:
    """Most recent notes, capped per topic so one large area cannot fill the list."""

    seen: dict[str, int] = {}
    latest: list[Document] = []
    for document in _blog_documents(documents, language):
        if seen.get(document.area, 0) >= LATEST_PER_AREA:
            continue
        seen[document.area] = seen.get(document.area, 0) + 1
        latest.append(document)
        if len(latest) == LATEST_LIMIT:
            break
    return latest


def _coverage_html(documents: list[Document], language: str, source_page: str) -> str:
    """Notes per topic as a bar chart, so relative depth is visible at a glance."""

    rows = [
        (area, _area_note_count(documents, area, language))
        for area in _home_areas(documents, language)
    ]
    rows = [(area, count) for area, count in rows if count]
    if not rows:
        return ""
    largest = max(count for _, count in rows)
    cells = []
    for area, count in rows:
        catalog = _topic_catalog(documents, area, language)
        if catalog is None:
            continue
        name = _topic_name(area, language, catalog.title)
        share = max(3, round(count / largest * 100))
        unit = ("note" if count == 1 else "notes") if language == "en" else "篇笔记"
        cells.append(
            f'<a class="kb-coverage__row" '
            f'href="{_escape(_relative_site_url(source_page, catalog.page))}">'
            f'<span class="kb-coverage__name">{_escape(name)}</span>'
            f'<span class="kb-coverage__track" aria-hidden="true">'
            f'<span class="kb-coverage__fill" style="width:{share}%"></span></span>'
            f'<span class="kb-coverage__count">{count}'
            f'<span class="kb-visually-hidden"> {_escape(unit)}</span></span>'
            "</a>"
        )
    return "".join(cells)


def _latest_entry_html(document: Document, source_page: str, excerpt: str) -> str:
    excerpt_html = (
        f'<span class="kb-entry__excerpt">{_escape(excerpt)}</span>' if excerpt else ""
    )
    date = ""
    if document.updated:
        date = (
            f' <time datetime="{_escape(document.updated)}">'
            f"{_escape(document.updated)}</time>"
        )
    return (
        '<li class="kb-entry">'
        f'<a class="kb-entry__link kb-entry__link--rich" '
        f'href="{_escape(_relative_site_url(source_page, document.page))}">'
        f'<span class="kb-entry__title">{_escape(document.title)}</span>'
        f'<span class="kb-entry__meta">'
        f'<span class="kb-chip">{_escape(_kind_label(document.kind, document.language))}</span>'
        f"{date}</span>"
        f"{excerpt_html}"
        "</a>"
        "</li>"
    )


def _dashboard(
    documents: list[Document],
    language: str,
    excerpts: dict[str, str] | None = None,
) -> str:
    excerpts = excerpts or {}
    page = "index.md" if language == "en" else "index_zh.md"
    archive_page = "archive/index.md" if language == "en" else "archive/index_zh.md"
    is_english = language == "en"

    # The eyebrow carries the site's identity: the headline is a call to
    # action, so without this the home page never names whose notes these are.
    eyebrow = "Kelvin’s Engineering Notes" if is_english else "Kelvin 的工程笔记"
    heading = (
        "Start from a symptom, or pick a topic."
        if is_english
        else "从一个故障现象开始，或者直接挑一个主题。"
    )
    lede = (
        "Runbooks, references and study notes from real incidents and real "
        "setups. Every article ships in English and 简体中文."
        if is_english
        else "来自真实故障和真实配置的运维手册、参考与学习笔记。每篇文章都有中英文两个版本。"
    )
    search_label = "Search the knowledge base" if is_english else "搜索工程知识库"
    topics_title = "Pick a topic" if is_english else "挑一个主题"
    symptom_title = "Or start from a symptom" if is_english else "或者从一个故障现象开始"
    latest_title = "Recently updated" if is_english else "最近更新"
    depth_title = "Depth per topic" if is_english else "各主题的篇数"
    archive_label = "Full archive" if is_english else "完整归档"
    language_target = "index_zh.md" if is_english else "index.md"
    language_label = "中文" if is_english else "English"
    site_links_label = "Site links" if is_english else "站点链接"
    latest_note = (
        f"At most {LATEST_PER_AREA} notes per topic, so one large topic "
        "cannot fill the list."
        if is_english
        else f"每个主题最多取 {LATEST_PER_AREA} 篇，避免某个大主题占满整个列表。"
    )
    depth_note = (
        "AWS is written as a service-by-service reference, so it leads by "
        "count. The other topics are narrower and go deeper."
        if is_english
        else "AWS 是按服务逐个整理的参考，所以篇数最多；其它主题更窄也更深。"
    )

    topic_tiles = "\n".join(
        _topic_tile_html(documents, area, language, page)
        for area in _home_areas(documents, language)
    )
    symptoms = _symptoms_html(documents, language, page)
    latest_entries = "\n".join(
        _latest_entry_html(document, page, excerpts.get(document.source, ""))
        for document in _latest_documents(documents, language)
    )
    coverage = _coverage_html(documents, language, page)
    empty_latest = (
        ""
        if latest_entries
        else (
            '<p class="kb-empty">No published notes yet.</p>'
            if is_english
            else '<p class="kb-empty">暂时没有已发布笔记。</p>'
        )
    )

    sections = [
        '<div class="kb-home">',
        '<header class="kb-hero">',
        f'<p class="kb-home__eyebrow">{eyebrow}</p>',
        f'<h1 id="{"home" if is_english else "home-zh"}">{_escape(heading)}</h1>',
        f'<p class="kb-home__lede">{_escape(lede)}</p>',
        (
            f'<button class="kb-search-trigger" type="button" '
            f'aria-label="{search_label}" '
            f"onclick=\"document.getElementById('__search').click(); "
            f"document.querySelector('.md-search__input').focus()\">"
            f"<span>{search_label}</span>"
            f'<kbd class="kb-search-trigger__hint">/</kbd></button>'
        ),
        f'<nav class="kb-home__links" aria-label="{site_links_label}">',
        f'<a href="{_escape(_relative_site_url(page, archive_page))}">{archive_label}</a>',
        f'<a href="{_escape(_relative_site_url(page, language_target))}">{language_label}</a>',
        "</nav>",
        _stats_html(documents, language),
        "</header>",
    ]

    if topic_tiles:
        sections.extend(
            [
                '<section class="kb-home__section" aria-labelledby="kb-topics-title">',
                f'<h2 class="kb-home__block-title" id="kb-topics-title">{topics_title}</h2>',
                f'<div class="kb-topic-grid">{topic_tiles}</div>',
                "</section>",
            ]
        )
    if symptoms:
        sections.extend(
            [
                '<section class="kb-home__section" aria-labelledby="kb-symptom-title">',
                f'<h2 class="kb-home__block-title" id="kb-symptom-title">{symptom_title}</h2>',
                f'<div class="kb-symptoms">{symptoms}</div>',
                "</section>",
            ]
        )

    sections.extend(
        [
            '<div class="kb-home__split">',
            '<section class="kb-home__section" aria-labelledby="kb-latest-title">',
            (
                f'<div class="kb-section-heading">'
                f'<h2 class="kb-home__block-title" id="kb-latest-title">{latest_title}</h2>'
                f'<a href="{_escape(_relative_site_url(page, archive_page))}">'
                f"{archive_label}</a></div>"
            ),
            f'<ul class="kb-entry-list">{latest_entries}</ul>',
            empty_latest,
            f'<p class="kb-home__note">{_escape(latest_note)}</p>',
            "</section>",
        ]
    )
    if coverage:
        sections.extend(
            [
                '<section class="kb-home__section" aria-labelledby="kb-depth-title">',
                f'<h2 class="kb-home__block-title" id="kb-depth-title">{depth_title}</h2>',
                f'<div class="kb-coverage">{coverage}</div>',
                f'<p class="kb-home__note">{_escape(depth_note)}</p>',
                "</section>",
            ]
        )
    sections.extend(["</div>", "</div>", ""])

    return _generated_front_matter(
        language,
        title="Home" if is_english else "中文首页",
        # The topic tabs live in the header, so they survive this; the left
        # rail would only repeat "Home" and cost the page a column of width.
        hide_navigation=True,
        hide_toc=True,
        search_exclude=True,
    ) + "\n".join(sections)


def _topics_page(documents: list[Document], language: str) -> str:
    page = "topics/index.md" if language == "en" else "topics/index_zh.md"
    title = "Topics" if language == "en" else "主题"
    description = (
        "Browse the knowledge base by engineering area."
        if language == "en"
        else "按工程领域浏览知识库。"
    )
    areas = sorted(
        {
            document.area
            for document in documents
            if document.language == language and document.area != "engineering"
        }
    )
    cards = "\n".join(
        _topic_card_html(documents, area, language, page) for area in areas
    )
    return _generated_front_matter(
        language,
        title=title,
        hide_toc=True,
        hide_footer=True,
        search_exclude=True,
    ) + "\n".join(
        [
            f"# {title}",
            "",
            '<div class="kb-hub">',
            f'<p class="kb-hub__lede">{description}</p>',
            f'<div class="kb-topic-grid">{cards}</div>',
            "</div>",
            "",
        ]
    )


def _archive_page(documents: list[Document], language: str) -> str:
    page = "archive/index.md" if language == "en" else "archive/index_zh.md"
    title = "Archive" if language == "en" else "归档"
    description = (
        "All guides, runbooks, references, tooling notes, and video summaries."
        if language == "en"
        else "全部指南、运维手册、参考资料、工具笔记和视频摘要。"
    )
    grouped: dict[str, list[Document]] = {}
    for document in _blog_documents(documents, language):
        year = document.updated[:4] if document.updated else "Undated"
        grouped.setdefault(year, []).append(document)
    years = sorted((year for year in grouped if year != "Undated"), reverse=True)
    if "Undated" in grouped:
        years.append("Undated")
    year_sections = []
    for year in years:
        entries = "\n".join(_entry_html(document, page) for document in grouped[year])
        year_sections.append(
            f'<section class="kb-archive__year" aria-labelledby="archive-{_escape(year)}">'
            f'<h2 id="archive-{_escape(year)}">{_escape(year)}</h2>'
            f'<ul class="kb-entry-list">{entries}</ul>'
            "</section>"
        )
    empty = (
        "<p class=\"kb-empty\">No published notes yet.</p>"
        if language == "en"
        else "<p class=\"kb-empty\">暂时没有已发布笔记。</p>"
    )
    return _generated_front_matter(
        language,
        title=title,
        hide_toc=True,
        hide_footer=True,
        search_exclude=True,
    ) + "\n".join(
        [
            f"# {title}",
            "",
            '<div class="kb-hub kb-archive">',
            f'<p class="kb-hub__lede">{description}</p>',
            "".join(year_sections) if year_sections else empty,
            "</div>",
            "",
        ]
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
        excerpts[document.source] = _excerpt(raw, document.language)
        reading = _reading_label(raw, document.language)
        text = rewrite_links(raw, document.source, page_map, tracked)
        text = _with_generated_metadata(text, document)
        text = _with_generated_context(text, document, reading)
        text = text.rstrip("\n") + "\n" + _related_html(document, documents)
        target = output / document.page
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(text, encoding="utf-8")

    generated_pages = {
        "index.md": _dashboard(documents, "en", excerpts),
        "index_zh.md": _dashboard(documents, "zh", excerpts),
        "topics/index.md": _topics_page(documents, "en"),
        "topics/index_zh.md": _topics_page(documents, "zh"),
        "archive/index.md": _archive_page(documents, "en"),
        "archive/index_zh.md": _archive_page(documents, "zh"),
        "SUMMARY.md": _summary_markdown(documents),
    }
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
            print(f"validated {len(documents)} documents in {len(documents) // 2} bilingual pairs")
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
