from __future__ import annotations

import json
import math
import re
from pathlib import Path
from typing import Any

from yt_transcript.models import CaptureStatus, normalize_text

_TIMESTAMP = re.compile(
    r"https://www\.youtube\.com/watch\?v=([A-Za-z0-9_-]{11})&t=(\d+)s(?=[)\s])"
)
_SEGMENT = re.compile(r"segment-(\d+)")
_RECIPROCAL_ENGLISH = re.compile(r"\]\(summary_zh\.md\)")
_RECIPROCAL_CHINESE = re.compile(r"\]\(summary\.md\)")
_DISPOSITIONS = {"included", "compressed", "cta"}
_AUDIT_KEYS = (
    "missing_from_english",
    "missing_from_chinese",
    "unsupported_english_claims",
    "unsupported_chinese_claims",
    "timestamp_mismatches",
)


def _timestamp_links(markdown: str) -> list[tuple[str, int]]:
    return [(video_id, int(value)) for video_id, value in _TIMESTAMP.findall(markdown)]


def _segment_number(value: object) -> int | None:
    if not isinstance(value, str):
        return None
    match = _SEGMENT.fullmatch(value)
    return int(match.group(1)) if match else None


def validate_publication(
    validation_path: Path, english_path: Path, chinese_path: Path
) -> list[str]:
    payload: Any = json.loads(validation_path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        return ["validation ledger is not an object"]
    errors: list[str] = []
    if payload.get("status") != CaptureStatus.COMPLETE.value:
        errors.append("local capture is not complete")

    metadata = payload.get("metadata")
    video_id: str | None = None
    duration: float | None = None
    if not isinstance(metadata, dict):
        errors.append("validation ledger has no metadata")
    else:
        candidate_id = metadata.get("video_id")
        candidate_duration = metadata.get("duration_seconds")
        if isinstance(candidate_id, str) and re.fullmatch(r"[A-Za-z0-9_-]{11}", candidate_id):
            video_id = candidate_id
        else:
            errors.append("validation ledger has an invalid video ID")
        if (
            isinstance(candidate_duration, (int, float))
            and not isinstance(candidate_duration, bool)
            and math.isfinite(candidate_duration)
            and candidate_duration > 0
        ):
            duration = float(candidate_duration)
        else:
            errors.append("validation ledger has an invalid video duration")
        candidate_source_url = metadata.get("source_url")
        if video_id is not None and candidate_source_url != (
            f"https://www.youtube.com/watch?v={video_id}"
        ):
            errors.append("validation ledger source URL does not match video ID")

    candidate_segment_count = payload.get("segment_count")
    segment_count: int | None = None
    if (
        isinstance(candidate_segment_count, int)
        and not isinstance(candidate_segment_count, bool)
        and candidate_segment_count > 0
    ):
        segment_count = candidate_segment_count
    else:
        errors.append("validation ledger has an invalid segment count")

    chunks = payload.get("chunks")
    if not isinstance(chunks, list) or not chunks:
        errors.append("validation ledger has no chunks")
        chunks = []

    required_timestamps: set[int] = set()
    previous_last_segment: int | None = None
    for index, chunk in enumerate(chunks, start=1):
        if not isinstance(chunk, dict):
            errors.append(f"chunk {index} is invalid")
            continue
        if chunk.get("status") != "processed":
            errors.append(f"chunk {index} is not processed")
        if chunk.get("chunk_id") != f"chunk-{index:03d}":
            errors.append(f"chunk {index} has an invalid chunk ID")

        first_segment = _segment_number(chunk.get("first_segment_id"))
        last_segment = _segment_number(chunk.get("last_segment_id"))
        if first_segment is None or last_segment is None or first_segment > last_segment:
            errors.append(f"chunk {index} has an invalid segment range")
        else:
            if index == 1 and first_segment != 1:
                errors.append("chunks do not start at segment 1")
            if previous_last_segment is not None and first_segment != previous_last_segment + 1:
                errors.append(f"chunks are not contiguous at chunk {index}")
            previous_last_segment = last_segment

        chunk_start = chunk.get("start_seconds")
        chunk_end = chunk.get("end_seconds")
        valid_range = (
            isinstance(chunk_start, (int, float))
            and not isinstance(chunk_start, bool)
            and isinstance(chunk_end, (int, float))
            and not isinstance(chunk_end, bool)
            and chunk_start <= chunk_end
        )
        if not valid_range:
            errors.append(f"chunk {index} has an invalid time range")

        items = chunk.get("content_items")
        if not isinstance(items, list) or not items:
            errors.append(f"chunk {index} has no content items")
            continue
        for item_index, item in enumerate(items, start=1):
            if not isinstance(item, dict):
                errors.append(f"chunk {index} item {item_index} is invalid")
                continue
            disposition = item.get("disposition")
            if disposition not in _DISPOSITIONS:
                errors.append(f"chunk {index} item {item_index} has invalid disposition")
                continue
            if disposition == "cta":
                continue

            timestamp = item.get("timestamp_seconds")
            if not isinstance(timestamp, int) or isinstance(timestamp, bool) or timestamp < 0:
                errors.append(f"chunk {index} item {item_index} has no timestamp")
            else:
                required_timestamps.add(timestamp)
                if (
                    valid_range
                    and isinstance(chunk_start, (int, float))
                    and isinstance(chunk_end, (int, float))
                    and not chunk_start <= timestamp <= chunk_end
                ):
                    errors.append(f"chunk {index} item {item_index} timestamp is outside the chunk")

            source_segment_ids = item.get("source_segment_ids")
            if not isinstance(source_segment_ids, list) or not source_segment_ids:
                errors.append(f"chunk {index} item {item_index} has no source segments")
            elif first_segment is not None and last_segment is not None:
                for source_segment_id in source_segment_ids:
                    source_segment = _segment_number(source_segment_id)
                    if (
                        source_segment is None
                        or not first_segment <= source_segment <= last_segment
                    ):
                        errors.append(
                            f"chunk {index} item {item_index} source segment is outside the chunk"
                        )
                        break

            quote = item.get("quote")
            chunk_text = chunk.get("text")
            if not isinstance(quote, str) or not quote.strip():
                errors.append(f"chunk {index} item {item_index} has no quote")
            elif not isinstance(chunk_text, str) or normalize_text(quote) not in normalize_text(
                chunk_text
            ):
                errors.append(f"chunk {index} item {item_index} quote is not from this chunk")
    if segment_count is not None and previous_last_segment != segment_count:
        errors.append(f"chunks do not cover all {segment_count} segments")

    audit = payload.get("audit")
    if not isinstance(audit, dict) or audit.get("status") != "complete":
        errors.append("independent audit is not complete")
    elif any(audit.get(key) for key in _AUDIT_KEYS):
        errors.append("independent audit contains unresolved findings")
    if isinstance(audit, dict) and audit.get("unresolved_capture_warnings"):
        errors.append("capture warnings remain unresolved")

    english = english_path.read_text(encoding="utf-8")
    chinese = chinese_path.read_text(encoding="utf-8")
    english_links = _timestamp_links(english)
    chinese_links = _timestamp_links(chinese)
    english_timestamps = {timestamp for _, timestamp in english_links}
    chinese_timestamps = {timestamp for _, timestamp in chinese_links}
    if not _RECIPROCAL_ENGLISH.search(english):
        errors.append("English summary does not link to Chinese summary")
    if not _RECIPROCAL_CHINESE.search(chinese):
        errors.append("Chinese summary does not link to English summary")
    if english_timestamps != chinese_timestamps:
        errors.append("English and Chinese summaries use different timestamps")
    if video_id is not None:
        if any(link_video_id != video_id for link_video_id, _ in english_links):
            errors.append("English summary uses a different video ID")
        if any(link_video_id != video_id for link_video_id, _ in chinese_links):
            errors.append("Chinese summary uses a different video ID")
    if duration is not None:
        outside = sorted(
            timestamp
            for timestamp in english_timestamps | chinese_timestamps
            if timestamp > duration
        )
        if outside:
            errors.append(f"summaries use timestamps outside video duration: {outside}")
    missing = required_timestamps - english_timestamps
    if missing:
        errors.append(f"summaries omit required timestamps: {sorted(missing)}")
    return errors
