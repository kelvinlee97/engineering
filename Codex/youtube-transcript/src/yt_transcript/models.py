from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum


class CaptureStatus(StrEnum):
    COMPLETE = "complete"
    PARTIAL = "partial"
    BLOCKED = "blocked"


@dataclass(frozen=True)
class Segment:
    segment_id: str
    start_seconds: float
    text: str


@dataclass(frozen=True)
class VideoMetadata:
    source_url: str
    video_id: str
    title: str
    channel: str | None
    duration_seconds: float
    language: str
    subtitle_type: str


@dataclass(frozen=True)
class Chunk:
    chunk_id: str
    first_segment_id: str
    last_segment_id: str
    start_seconds: float
    end_seconds: float
    word_count: int


@dataclass(frozen=True)
class ValidationResult:
    status: CaptureStatus
    transcript_sha256: str | None
    segment_count: int
    first_start_seconds: float | None
    last_start_seconds: float | None
    chunks: list[Chunk] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)
