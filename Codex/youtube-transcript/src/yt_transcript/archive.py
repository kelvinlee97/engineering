from __future__ import annotations

import json
import re
import unicodedata
from pathlib import Path

from yt_transcript.summary_contract import load_evidence, validate_summary_pair

TOPICS = {
    "python",
    "kubernetes",
    "terraform",
    "claude",
    "linux",
    "startup",
    "finance",
    "career",
    "productivity",
    "general",
}

TOPIC_ALIASES = {
    "k8s": "kubernetes",
    "iac": "terraform",
    "opentofu": "terraform",
    "anthropic": "claude",
    "claude-code": "claude",
    "llm": "claude",
    "ai": "claude",
    "ai-engineering": "claude",
    "agents": "claude",
    "rag": "claude",
    "entrepreneurship": "startup",
    "business": "startup",
    "investing": "finance",
    "personal-finance": "finance",
}

_TOPIC = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
_TRAILING_PARENTHETICAL = re.compile(r"\s*\([^()]+\)\s*$")


def normalize_topic(value: str) -> str:
    topic = value.strip().lower()
    if _TOPIC.fullmatch(topic) is None:
        raise ValueError("topic must be a single kebab-case directory name")
    normalized = TOPIC_ALIASES.get(topic, topic)
    if normalized not in TOPICS:
        raise ValueError(f"topic is not in the approved registry: {topic}")
    return normalized


def slugify_title(title: str, *, max_length: int = 80) -> str:
    title = _TRAILING_PARENTHETICAL.sub("", title).strip()
    ascii_title = unicodedata.normalize("NFKD", title).encode("ascii", "ignore").decode("ascii")
    slug = re.sub(r"[^a-z0-9]+", "-", ascii_title.lower()).strip("-")
    slug = slug[:max_length].rstrip("-")
    return slug or "untitled-video"


def _read_json(path: Path) -> dict[str, object]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError(f"expected a JSON object: {path}")
    return payload


def archive_capture(
    capture_dir: Path,
    topic: str,
    *,
    reason: str = "Classified by Codex after reviewing the complete summary.",
    tags: list[str] | None = None,
) -> Path:
    capture_dir = capture_dir.resolve()
    metadata_path = capture_dir / "metadata.json"
    report_path = capture_dir / "extraction-report.json"
    if not capture_dir.is_dir() or not metadata_path.is_file() or not report_path.is_file():
        raise ValueError("capture directory is missing required metadata or report files")

    report = _read_json(report_path)
    if report.get("status") != "complete":
        raise ValueError("only a complete capture can be archived")
    for filename in ("evidence.json", "summary.en.md", "summary.zh.md"):
        if not (capture_dir / filename).is_file():
            raise ValueError(f"capture is missing required summary artifact: {filename}")
    summary_errors = validate_summary_pair(
        load_evidence(capture_dir / "evidence.json"),
        (capture_dir / "summary.en.md").read_text(encoding="utf-8"),
        (capture_dir / "summary.zh.md").read_text(encoding="utf-8"),
    )
    if summary_errors:
        raise ValueError(f"summary validation failed: {'; '.join(summary_errors)}")

    metadata = _read_json(metadata_path)
    video_id = metadata.get("video_id")
    title = metadata.get("title")
    if not isinstance(video_id, str) or not isinstance(title, str):
        raise ValueError("capture metadata is missing video_id or title")

    normalized_topic = normalize_topic(topic)
    title_slug = slugify_title(title)
    capture_root = (
        capture_dir.parent.parent if capture_dir.parent.name == ".staging" else capture_dir.parent
    )
    relative_archive = Path(normalized_topic) / f"{title_slug}--{video_id}"
    target = capture_root / relative_archive
    if target.exists():
        raise FileExistsError(f"archive target already exists: {target}")

    clean_tags = list(dict.fromkeys(tag.strip() for tag in (tags or []) if tag.strip()))
    metadata.update(
        {
            "topic": normalized_topic,
            "classification_reason": reason.strip(),
            "tags": clean_tags,
            "title_slug": title_slug,
            "archive_path": str(relative_archive),
        }
    )
    metadata_path.write_text(
        json.dumps(metadata, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    target.parent.mkdir(parents=True, exist_ok=True)
    capture_dir.rename(target)
    return target
