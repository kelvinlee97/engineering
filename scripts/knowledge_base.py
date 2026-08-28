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
    return sorted(by_source, key=lambda document: document.updated or "", reverse=True)


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


def _language(source: str) -> str:
    name = PurePosixPath(source).name
    return "zh" if name.endswith("_ZH.md") or name == "summary_zh.md" else "en"


def _kind(source: str) -> str:
    path = PurePosixPath(source)
    lower_parts = {part.lower() for part in path.parts}
    if path.name.startswith("summary"):
        return "video-summary"
    if {"codex", "youtube-transcript"}.issubset(lower_parts):
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


def _last_modified(root: Path, source: str) -> str:
    if not (root / ".git").exists():
        return ""
    result = subprocess.run(
        ["git", "-C", str(root), "log", "-1", "--format=%cs", "--", source],
        capture_output=True,
        text=True,
        check=False,
    )
    return result.stdout.strip()


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

    for source in candidates:
        source_path = root / source
        try:
            text = source_path.read_text(encoding="utf-8")
            titles[source] = _extract_title(text, source)
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
                updated=_last_modified(root, source),
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


def _with_generated_context(text: str, document: Document) -> str:
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
    context = (
        "\n\n"
        f'<div class="kb-meta" role="group" aria-label="{metadata_aria}">\n'
        f'  <span class="kb-meta__kind">{_escape(kind_label)}</span>\n'
        f"{updated}"
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
        f'<span class="kb-entry__meta">{_escape(_kind_label(document.kind, document.language))}'
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
    return (
        f'<a class="kb-topic-card" href="{_escape(_relative_site_url(source_page, catalog.page))}">'
        f'<span class="kb-topic-card__name">{_escape(catalog.title)}</span>'
        f'<span class="kb-topic-card__count">{count_label}</span>'
        "</a>"
    )


def _dashboard(documents: list[Document], language: str) -> str:
    page = "index.md" if language == "en" else "index_zh.md"
    repository_page = "repository/index.md" if language == "en" else "repository/index_zh.md"
    topics_page = "topics/index.md" if language == "en" else "topics/index_zh.md"
    archive_page = "archive/index.md" if language == "en" else "archive/index_zh.md"
    is_english = language == "en"
    title = "Engineering Knowledge Base" if is_english else "工程知识库"
    description = (
        "Practical notes on cloud, infrastructure, developer tooling, and operations."
        if is_english
        else "记录云、基础设施、开发者工具与运维实践。"
    )
    search_label = "Search the knowledge base" if is_english else "搜索工程知识库"
    latest_title = "Latest notes" if is_english else "最新笔记"
    topics_title = "Topics" if is_english else "主题"
    video_title = "Video learning" if is_english else "视频学习"
    archive_label = "View full archive" if is_english else "查看完整归档"
    repository_label = "Repository guide" if is_english else "仓库指南"
    language_target = "index_zh.md" if is_english else "index.md"
    language_label = "中文" if is_english else "English"
    site_links_label = "Site links" if is_english else "站点链接"
    notes = _blog_documents(documents, language)[:6]
    videos = [document for document in notes if document.kind == "video-summary"]
    if len(videos) < 3:
        videos = [
            document
            for document in _blog_documents(documents, language)
            if document.kind == "video-summary"
        ][:3]
    areas = sorted(
        {
            document.area
            for document in documents
            if document.language == language and document.area != "engineering"
        }
    )
    topic_cards = "\n".join(
        _topic_card_html(documents, area, language, page) for area in areas
    )
    note_entries = "\n".join(_entry_html(document, page) for document in notes)
    video_entries = "\n".join(_entry_html(document, page) for document in videos)
    empty_notes = (
        "<p class=\"kb-empty\">No published notes yet.</p>"
        if is_english and not note_entries
        else "<p class=\"kb-empty\">暂时没有已发布笔记。</p>"
        if not is_english and not note_entries
        else ""
    )
    empty_videos = (
        "<p class=\"kb-empty\">No video summaries yet.</p>"
        if is_english and not video_entries
        else "<p class=\"kb-empty\">暂时没有视频摘要。</p>"
        if not is_english and not video_entries
        else ""
    )
    return _generated_front_matter(
        language,
        title="Home" if is_english else "中文首页",
        hide_navigation=True,
        hide_toc=True,
        hide_footer=True,
        search_exclude=True,
    ) + "\n".join(
        [
            '<p class="kb-home__eyebrow">ENGINEERING NOTES</p>',
            f"# {title}",
            "",
            '<div class="kb-home">',
            f'<p class="kb-home__lede">{description}</p>',
            (
                f'<button class="kb-search-trigger" type="button" '
                f'onclick="document.getElementById(\'__search\').click(); '
                f'document.querySelector(\'.md-search__input\').focus()">{search_label}</button>'
            ),
            f'<nav class="kb-home__links" aria-label="{site_links_label}">',
            (
                f'<a href="{_escape(_relative_site_url(page, repository_page))}">'
                f'{repository_label}</a>'
            ),
            f'<a href="{_escape(_relative_site_url(page, topics_page))}">{topics_title}</a>',
            f'<a href="{_escape(_relative_site_url(page, archive_page))}">{archive_label}</a>',
            f'<a href="{_escape(_relative_site_url(page, language_target))}">{language_label}</a>',
            "</nav>",
            '<section class="kb-home__section" aria-labelledby="kb-latest-title">',
            (
                f'<div class="kb-section-heading"><h2 id="kb-latest-title">{latest_title}</h2>'
                f'<a href="{_escape(_relative_site_url(page, archive_page))}">'
                f'{archive_label}</a></div>'
            ),
            f'<ul class="kb-entry-list">{note_entries}</ul>',
            empty_notes,
            "</section>",
            '<section class="kb-home__section" aria-labelledby="kb-topics-title">',
            f'<h2 id="kb-topics-title">{topics_title}</h2>',
            f'<div class="kb-topic-grid">{topic_cards}</div>',
            "</section>",
            '<section class="kb-home__section" aria-labelledby="kb-video-title">',
            (
                f'<div class="kb-section-heading"><h2 id="kb-video-title">{video_title}</h2>'
                f'<a href="{_escape(_relative_site_url(page, archive_page))}">'
                f'{archive_label}</a></div>'
            ),
            f'<ul class="kb-entry-list">{video_entries}</ul>',
            empty_videos,
            "</section>",
            "</div>",
            "",
        ]
    )


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
        hide_navigation=True,
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
        hide_navigation=True,
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

    for document in documents:
        text = (root / document.source).read_text(encoding="utf-8")
        text = rewrite_links(text, document.source, page_map, tracked)
        text = _with_generated_metadata(text, document)
        text = _with_generated_context(text, document)
        target = output / document.page
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(text, encoding="utf-8")

    generated_pages = {
        "index.md": _dashboard(documents, "en"),
        "index_zh.md": _dashboard(documents, "zh"),
        "topics/index.md": _topics_page(documents, "en"),
        "topics/index_zh.md": _topics_page(documents, "zh"),
        "archive/index.md": _archive_page(documents, "en"),
        "archive/index_zh.md": _archive_page(documents, "zh"),
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
