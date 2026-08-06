from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum


class CaptureStatus(StrEnum):
    COMPLETE = "complete"
    PARTIAL = "partial"
    BLOCKED = "blocked"


@dataclass(frozen=True)
class SubtitleTrack:
    language: str
    source: str
    url: str
    name: str | None = None
    selection_reason: str | None = None


@dataclass(frozen=True)
class Cue:
    cue_id: str
    start_seconds: float
    end_seconds: float
    text: str


@dataclass(frozen=True)
class DiscardedCue:
    source_index: int
    reason: str
    raw: str


@dataclass(frozen=True)
class ParseResult:
    cues: list[Cue]
    source_cue_count: int
    discarded: list[DiscardedCue] = field(default_factory=list)


@dataclass(frozen=True)
class ValidationResult:
    status: CaptureStatus
    coverage_ratio: float | None
    warnings: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)


@dataclass(frozen=True)
class EvidenceBundle:
    status: CaptureStatus
    source_url: str
    title: str
    language: str
    source_type: str
    cues: list[Cue]


@dataclass(frozen=True)
class VideoProbe:
    video_id: str
    title: str
    channel: str | None
    duration_seconds: float | None
    tracks: list[SubtitleTrack]
    selected_track: SubtitleTrack | None


@dataclass(frozen=True)
class ExtractionReport:
    status: CaptureStatus
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    coverage_ratio: float | None = None
    source_cue_count: int = 0
    normalized_cue_count: int = 0
    discarded_cue_count: int = 0
    raw_sha256: str | None = None
    transcript_sha256: str | None = None
    raw_file: str | None = None
    capture_dir: str | None = None
