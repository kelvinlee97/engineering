#!/usr/bin/env python3
"""Validate and stage the public Markdown knowledge base for MkDocs."""

from __future__ import annotations

import argparse
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
    pair_link = _relative_page_link(document.page, document.pair_page)
    source_link = f"{GITHUB_BLOB_URL}/{quote(document.source, safe='/')}"
    context = f"\n\n> [{pair_label}]({pair_link}) · [GitHub source]({source_link})"
    return text[: match.end()] + context + text[match.end() :]


def _dashboard(documents: list[Document]) -> str:
    lines = [
        "# Engineering Knowledge Base",
        "",
        "A searchable, bilingual engineering knowledge base.",
        "",
        "[Repository guide](repository/index.md) · [中文入口](repository/index_zh.md)",
        "",
        "## Areas",
        "",
    ]
    areas: dict[str, list[Document]] = {}
    for document in documents:
        if document.language == "en" and document.area != "engineering":
            areas.setdefault(document.area, []).append(document)
    for area in sorted(areas):
        area_documents = areas[area]
        document = next(
            (item for item in area_documents if item.kind == "catalog"),
            area_documents[0],
        )
        lines.append(
            f"- [{document.title}]({document.page}) · "
            f"[{document.pair_title}]({_relative_page_link('index.md', document.pair_page)})"
        )

    recent = sorted(
        (document for document in documents if document.language == "en"),
        key=lambda document: (document.updated, document.source),
        reverse=True,
    )[:12]
    lines.extend(["", "## Recently updated", ""])
    for document in recent:
        date = f" — {document.updated}" if document.updated else ""
        lines.append(f"- [{document.title}]({document.page}){date}")

    videos = sorted(
        (
            document
            for document in documents
            if document.kind == "video-summary" and document.language == "en"
        ),
        key=lambda document: (document.updated, document.source),
        reverse=True,
    )
    lines.extend(["", "## YouTube summaries", ""])
    for document in videos:
        lines.append(
            f"- [{document.title}]({document.page}) · "
            f"[{document.pair_title}]({_relative_page_link('index.md', document.pair_page)})"
        )
    return "\n".join(lines) + "\n"


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
        text = _with_generated_context(text, document)
        target = output / document.page
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(text, encoding="utf-8")

    (output / "index.md").write_text(_dashboard(documents), encoding="utf-8")
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
