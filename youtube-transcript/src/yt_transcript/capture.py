from __future__ import annotations

import hashlib
import json
import math
import re
from dataclasses import asdict
from pathlib import Path
from typing import Any

from yt_transcript.models import CaptureStatus, Chunk, Segment, ValidationResult, VideoMetadata

_WORD = re.compile(r"[\w’'-]+")
_CJK = re.compile(r"[\u3040-\u30ff\u3400-\u4dbf\u4e00-\u9fff\uf900-\ufaff\uac00-\ud7af]")


def _seconds(value: object) -> float:
    if not isinstance(value, (int, float)) or isinstance(value, bool):
        raise ValueError("segment start_seconds must be a number")
    result = float(value)
    if not math.isfinite(result):
        raise ValueError("segment start_seconds must be finite")
    if result < 0:
        raise ValueError("segment start_seconds cannot be negative")
    return result


def _segments(value: object) -> list[Segment]:
    if not isinstance(value, list) or not value:
        raise ValueError("browser transcript must contain one or more segments")
    segments: list[Segment] = []
    for index, item in enumerate(value, start=1):
        if not isinstance(item, dict):
            raise ValueError("each segment must be an object")
        text = item.get("text")
        if not isinstance(text, str) or not text.strip():
            raise ValueError(f"segment {index} has empty text")
        segments.append(
            Segment(
                segment_id=f"segment-{index:04d}",
                start_seconds=_seconds(item.get("start_seconds")),
                text=" ".join(text.split()),
            )
        )
    return segments


def _metadata(value: object) -> VideoMetadata:
    if not isinstance(value, dict):
        raise ValueError("browser export metadata must be an object")
    required_text = ("source_url", "video_id", "title", "language", "subtitle_type")
    for key in required_text:
        if not isinstance(value.get(key), str) or not value[key].strip():
            raise ValueError(f"browser export metadata is missing {key}")
    duration = _seconds(value.get("duration_seconds"))
    if duration <= 0:
        raise ValueError("duration_seconds must be positive")
    channel = value.get("channel")
    if channel is not None and not isinstance(channel, str):
        raise ValueError("channel must be a string or null")
    source_url = value["source_url"].strip()
    video_id = value["video_id"].strip()
    source_match = re.fullmatch(
        r"https://www\.youtube\.com/watch\?v=([A-Za-z0-9_-]+)", source_url
    )
    if source_match is None:
        raise ValueError("source_url must be a normalized YouTube watch URL")
    source_id = source_match.group(1)
    if source_id != video_id:
        raise ValueError("source_url video ID does not match video_id")
    if not re.fullmatch(r"[A-Za-z0-9_-]{11}", video_id):
        raise ValueError("video_id must be 11 characters")
    return VideoMetadata(
        source_url=source_url,
        video_id=video_id,
        title=value["title"].strip(),
        channel=channel.strip() if isinstance(channel, str) else None,
        duration_seconds=duration,
        language=value["language"].strip(),
        subtitle_type=value["subtitle_type"].strip(),
    )


def load_browser_export(path: Path) -> tuple[VideoMetadata, list[Segment]]:
    payload: Any = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError("browser export must be a JSON object")
    metadata = _metadata(payload.get("metadata"))
    segments = _segments(payload.get("segments"))
    return metadata, segments


def _canonical(segments: list[Segment]) -> str:
    return json.dumps(
        [(segment.start_seconds, segment.text) for segment in segments],
        ensure_ascii=False,
        separators=(",", ":"),
    )


def _text_units(text: str) -> int:
    cjk_units = len(_CJK.findall(text))
    non_cjk_text = _CJK.sub(" ", text)
    return cjk_units + len(_WORD.findall(non_cjk_text))


def _chunks(segments: list[Segment], *, target_words: int = 1000) -> list[Chunk]:
    chunks: list[Chunk] = []
    start_index = 0
    words = 0
    for index, segment in enumerate(segments, start=1):
        words += _text_units(segment.text)
        if words >= target_words and index < len(segments):
            first = segments[start_index]
            last = segments[index - 1]
            chunks.append(
                Chunk(
                    chunk_id=f"chunk-{len(chunks) + 1:03d}",
                    first_segment_id=first.segment_id,
                    last_segment_id=last.segment_id,
                    start_seconds=first.start_seconds,
                    end_seconds=last.start_seconds,
                    word_count=words,
                    text=" ".join(item.text for item in segments[start_index:index]),
                )
            )
            start_index = index
            words = 0
    first = segments[start_index]
    last = segments[-1]
    chunks.append(
        Chunk(
            chunk_id=f"chunk-{len(chunks) + 1:03d}",
            first_segment_id=first.segment_id,
            last_segment_id=last.segment_id,
            start_seconds=first.start_seconds,
            end_seconds=last.start_seconds,
            word_count=words,
            text=" ".join(item.text for item in segments[start_index:]),
        )
    )
    return chunks


def validate_capture(metadata: VideoMetadata, segments: list[Segment]) -> ValidationResult:
    errors: list[str] = []
    warnings: list[str] = []
    transcript_hash = hashlib.sha256(_canonical(segments).encode()).hexdigest()

    previous_start = -1.0
    for segment in segments:
        if segment.start_seconds < previous_start:
            errors.append(f"timestamps move backwards at {segment.segment_id}")
            break
        previous_start = segment.start_seconds

    start_tolerance = min(15.0, metadata.duration_seconds * 0.03)
    if segments[0].start_seconds > start_tolerance:
        errors.append("first segment starts too late")
    end_tolerance = max(15.0, metadata.duration_seconds * 0.03)
    if metadata.duration_seconds - segments[-1].start_seconds > end_tolerance:
        errors.append("last segment ends too early")

    for previous, current in zip(segments, segments[1:], strict=False):
        gap = current.start_seconds - previous.start_seconds
        if gap > 60:
            warnings.append(
                f"gap of {gap:.3f} seconds between {previous.segment_id} and {current.segment_id}"
            )

    status = CaptureStatus.COMPLETE if not errors else CaptureStatus.PARTIAL
    return ValidationResult(
        status=status,
        transcript_sha256=transcript_hash,
        segment_count=len(segments),
        first_start_seconds=segments[0].start_seconds,
        last_start_seconds=segments[-1].start_seconds,
        chunks=_chunks(segments),
        warnings=warnings,
        errors=errors,
    )


def _timestamp(seconds: float) -> str:
    whole = round(seconds)
    hours, remainder = divmod(whole, 3600)
    minutes, seconds = divmod(remainder, 60)
    if hours:
        return f"{hours:02d}:{minutes:02d}:{seconds:02d}"
    return f"{minutes:02d}:{seconds:02d}"


def write_local_capture(
    output_dir: Path,
    metadata: VideoMetadata,
    segments: list[Segment],
    validation: ValidationResult,
) -> None:
    if validation.status is not CaptureStatus.COMPLETE:
        raise ValueError("cannot write a complete local capture from an invalid transcript")
    output_dir.mkdir(parents=True, exist_ok=True)
    transcript = [
        f"# Transcript: {metadata.title}",
        "",
        f"- Source: {metadata.source_url}",
        f"- Channel: {metadata.channel or 'Unknown'}",
        f"- Language: {metadata.language}",
        f"- Subtitle type: {metadata.subtitle_type}",
        f"- Video duration: {_timestamp(metadata.duration_seconds)}",
        (
            "- Transcript coverage: "
            f"{_timestamp(validation.first_start_seconds or 0)}–"
            f"{_timestamp(validation.last_start_seconds or 0)}"
        ),
        f"- Segments: {validation.segment_count}",
        "",
        "## Transcript",
        "",
    ]
    transcript.extend(
        f"[{_timestamp(segment.start_seconds)}] {segment.text}" for segment in segments
    )
    (output_dir / "transcript.md").write_text("\n".join(transcript) + "\n", encoding="utf-8")

    report = {
        "status": validation.status.value,
        "metadata": asdict(metadata),
        "transcript_sha256": validation.transcript_sha256,
        "segment_count": validation.segment_count,
        "first_start_seconds": validation.first_start_seconds,
        "last_start_seconds": validation.last_start_seconds,
        "warnings": validation.warnings,
        "errors": validation.errors,
        "chunks": [
            {**asdict(chunk), "status": "pending", "content_items": []}
            for chunk in validation.chunks
        ],
        "audit": {
            "missing_from_english": [],
            "missing_from_chinese": [],
            "unsupported_english_claims": [],
            "unsupported_chinese_claims": [],
            "timestamp_mismatches": [],
            "unresolved_capture_warnings": list(validation.warnings),
            "status": "pending",
        },
    }
    (output_dir / "validation.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
