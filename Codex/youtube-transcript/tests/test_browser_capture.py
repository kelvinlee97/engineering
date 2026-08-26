from __future__ import annotations

import json
import sys
from pathlib import Path

from yt_transcript.capture import (
    _chunks,
    _segments,
    load_browser_export,
    validate_capture,
    write_local_capture,
)
from yt_transcript.cli import main
from yt_transcript.models import CaptureStatus
from yt_transcript.publication import validate_publication


def export() -> dict[str, object]:
    segments = [
        {"start_seconds": 0, "text": "Opening claim."},
        {"start_seconds": 4, "text": "Middle evidence."},
        {"start_seconds": 9, "text": "Conclusion."},
    ]
    return {
        "metadata": {
            "source_url": "https://www.youtube.com/watch?v=abcdefghijk",
            "video_id": "abcdefghijk",
            "title": "Example video",
            "channel": "Example channel",
            "duration_seconds": 10,
            "language": "en",
            "subtitle_type": "auto-generated",
        },
        "segments": segments,
    }


def load(tmp_path: Path, payload: dict[str, object]):
    source = tmp_path / "browser-export.json"
    source.write_text(json.dumps(payload), encoding="utf-8")
    return load_browser_export(source)


def test_single_complete_read_produces_a_complete_capture_and_local_files(tmp_path: Path) -> None:
    metadata, segments = load(tmp_path, export())

    validation = validate_capture(metadata, segments)
    write_local_capture(tmp_path / "capture", metadata, segments, validation)

    assert validation.status is CaptureStatus.COMPLETE
    assert validation.segment_count == 3
    assert len(validation.chunks) == 1
    transcript = (tmp_path / "capture" / "transcript.md").read_text(encoding="utf-8")
    report = json.loads((tmp_path / "capture" / "validation.json").read_text(encoding="utf-8"))
    assert "[00:00] Opening claim." in transcript
    assert "[00:09] Conclusion." in transcript
    assert report["chunks"][0]["status"] == "pending"
    assert report["audit"]["status"] == "pending"
    assert report["audit"]["unresolved_capture_warnings"] == []


def test_cli_accepts_a_single_complete_read(
    tmp_path: Path, monkeypatch, capsys
) -> None:
    source = tmp_path / "browser-export.json"
    source.write_text(json.dumps(export()), encoding="utf-8")
    output = tmp_path / "capture"
    monkeypatch.setattr(
        sys,
        "argv",
        ["yt-transcript", "capture", str(source), "--output", str(output)],
    )

    assert main() == 0
    assert json.loads(capsys.readouterr().out)["status"] == "complete"


def test_local_capture_copies_capture_warnings_to_the_audit(tmp_path: Path) -> None:
    gapped = [
        {"start_seconds": 0, "text": "Opening."},
        {"start_seconds": 70, "text": "Later."},
        {"start_seconds": 100, "text": "Conclusion."},
    ]
    payload = export()
    payload["segments"] = gapped
    payload["metadata"] = {**payload["metadata"], "duration_seconds": 100}
    metadata, segments = load(tmp_path, payload)

    validation = validate_capture(metadata, segments)
    write_local_capture(tmp_path / "capture", metadata, segments, validation)
    report = json.loads((tmp_path / "capture" / "validation.json").read_text(encoding="utf-8"))

    assert report["audit"]["unresolved_capture_warnings"] == validation.warnings


def test_late_start_fails_even_when_final_segment_reaches_the_end(tmp_path: Path) -> None:
    late = [
        {"start_seconds": 20, "text": "Late opening."},
        {"start_seconds": 99, "text": "Conclusion."},
    ]
    payload = export()
    payload["segments"] = late
    payload["metadata"] = {**payload["metadata"], "duration_seconds": 100}
    metadata, segments = load(tmp_path, payload)

    validation = validate_capture(metadata, segments)

    assert validation.status is CaptureStatus.PARTIAL
    assert "first segment starts too late" in validation.errors


def test_non_monotonic_timestamps_fail_closed(tmp_path: Path) -> None:
    unordered = [
        {"start_seconds": 0, "text": "Opening."},
        {"start_seconds": 7, "text": "Later."},
        {"start_seconds": 6, "text": "Out of order."},
        {"start_seconds": 10, "text": "Conclusion."},
    ]
    payload = export()
    payload["segments"] = unordered
    metadata, segments = load(tmp_path, payload)

    validation = validate_capture(metadata, segments)

    assert validation.status is CaptureStatus.PARTIAL
    assert "timestamps move backwards at segment-0003" in validation.errors


def test_equal_timestamps_are_valid_for_adjacent_caption_cues(tmp_path: Path) -> None:
    payload = export()
    payload["segments"] = [
        {"start_seconds": 0, "text": "Opening."},
        {"start_seconds": 7, "text": "First cue."},
        {"start_seconds": 7, "text": "Second cue."},
        {"start_seconds": 10, "text": "Conclusion."},
    ]
    metadata, segments = load(tmp_path, payload)

    validation = validate_capture(metadata, segments)

    assert validation.status is CaptureStatus.COMPLETE


def test_large_gap_is_recorded_for_manual_audit(tmp_path: Path) -> None:
    gapped = [
        {"start_seconds": 0, "text": "Opening."},
        {"start_seconds": 70, "text": "Later."},
        {"start_seconds": 100, "text": "Conclusion."},
    ]
    payload = export()
    payload["segments"] = gapped
    payload["metadata"] = {**payload["metadata"], "duration_seconds": 100}
    metadata, segments = load(tmp_path, payload)

    validation = validate_capture(metadata, segments)

    assert validation.status is CaptureStatus.COMPLETE
    assert validation.errors == []
    assert validation.warnings == [
        "gap of 70.000 seconds between segment-0001 and segment-0002"
    ]


def test_empty_segment_is_rejected_before_validation(tmp_path: Path) -> None:
    bad = export()
    bad["segments"] = [{"start_seconds": 0, "text": ""}]
    source = tmp_path / "bad.json"
    source.write_text(json.dumps(bad), encoding="utf-8")

    try:
        load_browser_export(source)
    except ValueError as error:
        assert str(error) == "segment 1 has empty text"
    else:
        raise AssertionError("empty segment should be rejected")


def test_non_finite_timestamp_is_rejected_before_validation(tmp_path: Path) -> None:
    bad = export()
    bad["segments"] = [{"start_seconds": float("inf"), "text": "Impossible."}]

    try:
        load(tmp_path, bad)
    except ValueError as error:
        assert str(error) == "segment start_seconds must be finite"
    else:
        raise AssertionError("non-finite timestamp should be rejected")


def test_source_url_must_match_video_id(tmp_path: Path) -> None:
    bad = export()
    bad["metadata"] = {**bad["metadata"], "video_id": "differentid0"}

    try:
        load(tmp_path, bad)
    except ValueError as error:
        assert str(error) == "source_url video ID does not match video_id"
    else:
        raise AssertionError("mismatched video ID should be rejected")


def test_source_url_must_use_the_youtube_watch_path(tmp_path: Path) -> None:
    bad = export()
    bad["metadata"] = {
        **bad["metadata"],
        "source_url": "https://www.youtube.com/playlist?v=abcdefghijk",
    }

    try:
        load(tmp_path, bad)
    except ValueError as error:
        assert str(error) == "source_url must be a normalized YouTube watch URL"
    else:
        raise AssertionError("non-watch YouTube URL should be rejected")


def test_source_url_must_not_have_extra_query_parameters(tmp_path: Path) -> None:
    bad = export()
    bad["metadata"] = {
        **bad["metadata"],
        "source_url": "https://www.youtube.com/watch?v=abcdefghijk&list=playlist",
    }

    try:
        load(tmp_path, bad)
    except ValueError as error:
        assert str(error) == "source_url must be a normalized YouTube watch URL"
    else:
        raise AssertionError("extra YouTube URL query parameters should be rejected")


def test_video_id_must_have_the_youtube_length(tmp_path: Path) -> None:
    bad = export()
    bad["metadata"] = {
        **bad["metadata"],
        "source_url": "https://www.youtube.com/watch?v=short",
        "video_id": "short",
    }

    try:
        load(tmp_path, bad)
    except ValueError as error:
        assert str(error) == "video_id must be 11 characters"
    else:
        raise AssertionError("short YouTube video IDs should be rejected")


def test_interior_timestamp_is_validated_from_the_single_read(tmp_path: Path) -> None:
    payload = export()
    payload["segments"] = [
        {"start_seconds": 0, "text": "Opening claim."},
        {"start_seconds": 4.0004, "text": "Middle evidence."},
        {"start_seconds": 9, "text": "Conclusion."},
    ]
    metadata, segments = load(tmp_path, payload)

    validation = validate_capture(metadata, segments)

    assert validation.status is CaptureStatus.COMPLETE


def test_late_end_fails_even_when_the_read_starts_at_zero(tmp_path: Path) -> None:
    payload = export()
    payload["segments"] = [
        {"start_seconds": 0, "text": "Opening claim."},
        {"start_seconds": 4, "text": "Only the beginning."},
    ]
    payload["metadata"] = {**payload["metadata"], "duration_seconds": 100}
    metadata, segments = load(tmp_path, payload)

    validation = validate_capture(metadata, segments)

    assert validation.status is CaptureStatus.PARTIAL
    assert "last segment ends too early" in validation.errors


def _publication_ledger(
    *,
    timestamp: int = 60,
    unresolved_capture_warnings: list[str] | None = None,
    source_segment_ids: list[str] | None = None,
    chunks: list[dict[str, object]] | None = None,
) -> dict[str, object]:
    return {
        "status": "complete",
        "metadata": {
            "source_url": "https://www.youtube.com/watch?v=abcdefghijk",
            "video_id": "abcdefghijk",
            "duration_seconds": 120,
        },
        "segment_count": 3,
        "chunks": chunks
        if chunks is not None
        else [
            {
                "chunk_id": "chunk-001",
                "first_segment_id": "segment-0001",
                "last_segment_id": "segment-0003",
                "start_seconds": 0,
                "end_seconds": 90,
                "word_count": 3,
                "status": "processed",
                "text": "First segment second segment",
                "content_items": [
                    {
                        "disposition": "included",
                        "timestamp_seconds": timestamp,
                        "source_segment_ids": source_segment_ids or ["segment-0001"],
                        "quote": "First segment",
                    }
                ],
            }
        ],
        "audit": {
            "missing_from_english": [],
            "missing_from_chinese": [],
            "unsupported_english_claims": [],
            "unsupported_chinese_claims": [],
            "timestamp_mismatches": [],
            "unresolved_capture_warnings": unresolved_capture_warnings or [],
            "status": "complete",
        },
    }


def _write_publication_fixture(
    tmp_path: Path,
    ledger: dict[str, object],
    *,
    english_video_id: str = "abcdefghijk",
    chinese_video_id: str = "abcdefghijk",
    timestamp: int = 60,
) -> None:
    (tmp_path / "validation.json").write_text(json.dumps(ledger), encoding="utf-8")
    (tmp_path / "summary.md").write_text(
        "[中文](summary_zh.md) "
        f"[source](https://www.youtube.com/watch?v={english_video_id}&t={timestamp}s)",
        encoding="utf-8",
    )
    (tmp_path / "summary_zh.md").write_text(
        "[English](summary.md) "
        f"[来源](https://www.youtube.com/watch?v={chinese_video_id}&t={timestamp}s)",
        encoding="utf-8",
    )


def test_publication_rejects_timestamps_from_another_video(tmp_path: Path) -> None:
    ledger = _publication_ledger()
    _write_publication_fixture(tmp_path, ledger, english_video_id="wrongvideo1")

    errors = validate_publication(
        tmp_path / "validation.json",
        tmp_path / "summary.md",
        tmp_path / "summary_zh.md",
    )

    assert "English summary uses a different video ID" in errors


def test_publication_rejects_metadata_source_url_mismatch(tmp_path: Path) -> None:
    ledger = _publication_ledger()
    ledger["metadata"]["source_url"] = "https://www.youtube.com/watch?v=wrongvideo1"
    _write_publication_fixture(tmp_path, ledger)

    errors = validate_publication(
        tmp_path / "validation.json",
        tmp_path / "summary.md",
        tmp_path / "summary_zh.md",
    )

    assert "validation ledger source URL does not match video ID" in errors


def test_publication_rejects_timestamps_outside_video_duration(tmp_path: Path) -> None:
    ledger = _publication_ledger(timestamp=121)
    _write_publication_fixture(tmp_path, ledger, timestamp=121)

    errors = validate_publication(
        tmp_path / "validation.json",
        tmp_path / "summary.md",
        tmp_path / "summary_zh.md",
    )

    assert "summaries use timestamps outside video duration: [121]" in errors


def test_publication_rejects_timestamp_links_with_extra_query_parameters(tmp_path: Path) -> None:
    ledger = _publication_ledger()
    _write_publication_fixture(tmp_path, ledger)
    (tmp_path / "summary.md").write_text(
        "[中文](summary_zh.md) "
        "[source](https://www.youtube.com/watch?v=abcdefghijk&t=60s&list=playlist)",
        encoding="utf-8",
    )

    errors = validate_publication(
        tmp_path / "validation.json",
        tmp_path / "summary.md",
        tmp_path / "summary_zh.md",
    )

    assert "summaries omit required timestamps: [60]" in errors


def test_publication_rejects_unresolved_capture_warnings(tmp_path: Path) -> None:
    ledger = _publication_ledger(unresolved_capture_warnings=["gap of 70 seconds"])
    _write_publication_fixture(tmp_path, ledger)

    errors = validate_publication(
        tmp_path / "validation.json",
        tmp_path / "summary.md",
        tmp_path / "summary_zh.md",
    )

    assert "capture warnings remain unresolved" in errors


def test_publication_rejects_source_segments_outside_the_chunk(tmp_path: Path) -> None:
    ledger = _publication_ledger(source_segment_ids=["segment-0099"])
    _write_publication_fixture(tmp_path, ledger)

    errors = validate_publication(
        tmp_path / "validation.json",
        tmp_path / "summary.md",
        tmp_path / "summary_zh.md",
    )

    assert "chunk 1 item 1 source segment is outside the chunk" in errors


def test_publication_rejects_non_contiguous_chunks(tmp_path: Path) -> None:
    chunks = [
        {
            "chunk_id": "chunk-001",
            "first_segment_id": "segment-0001",
            "last_segment_id": "segment-0002",
            "start_seconds": 0,
            "end_seconds": 30,
            "word_count": 2,
            "status": "processed",
            "text": "First segment",
            "content_items": [
                {
                    "disposition": "included",
                    "timestamp_seconds": 10,
                    "source_segment_ids": ["segment-0001"],
                    "quote": "First segment",
                }
            ],
        },
        {
            "chunk_id": "chunk-002",
            "first_segment_id": "segment-0004",
            "last_segment_id": "segment-0005",
            "start_seconds": 40,
            "end_seconds": 50,
            "word_count": 2,
            "status": "processed",
            "text": "Second segment",
            "content_items": [
                {
                    "disposition": "included",
                    "timestamp_seconds": 45,
                    "source_segment_ids": ["segment-0004"],
                    "quote": "Second segment",
                }
            ],
        },
    ]
    ledger = _publication_ledger(chunks=chunks)
    ledger["segment_count"] = 5
    _write_publication_fixture(tmp_path, ledger, timestamp=10)

    errors = validate_publication(
        tmp_path / "validation.json",
        tmp_path / "summary.md",
        tmp_path / "summary_zh.md",
    )

    assert "chunks are not contiguous at chunk 2" in errors


def test_publication_rejects_invalid_chunk_ids_and_incomplete_segment_coverage(
    tmp_path: Path,
) -> None:
    ledger = _publication_ledger()
    ledger["segment_count"] = 3
    ledger["chunks"][0]["chunk_id"] = "chunk-009"
    ledger["chunks"][0]["first_segment_id"] = "segment-0002"
    _write_publication_fixture(tmp_path, ledger)

    errors = validate_publication(
        tmp_path / "validation.json",
        tmp_path / "summary.md",
        tmp_path / "summary_zh.md",
    )

    assert "chunk 1 has an invalid chunk ID" in errors
    assert "chunks do not start at segment 1" in errors


def test_chunks_count_cjk_characters_as_text_units() -> None:
    segments = _segments(
        [{"start_seconds": index, "text": "字" * 1000} for index in range(5)]
    )

    chunks = _chunks(segments)

    assert len(chunks) == 5
    assert [chunk.word_count for chunk in chunks] == [1000] * 5


def test_publication_requires_processed_chunks_a_clean_audit_and_matching_times(
    tmp_path: Path,
) -> None:
    ledger = {
        "status": "complete",
        "metadata": {
            "source_url": "https://www.youtube.com/watch?v=abcdefghijk",
            "video_id": "abcdefghijk",
            "duration_seconds": 120,
        },
        "segment_count": 3,
        "chunks": [
            {
                "chunk_id": "chunk-001",
                "first_segment_id": "segment-0001",
                "last_segment_id": "segment-0003",
                "start_seconds": 0,
                "end_seconds": 90,
                "word_count": 3,
                "status": "processed",
                "text": "First segment second segment",
                "content_items": [
                    {
                        "disposition": "included",
                        "timestamp_seconds": 60,
                        "source_segment_ids": ["segment-0001"],
                        "quote": "First segment",
                    },
                    {"disposition": "cta"},
                ],
            }
        ],
        "audit": {
            "status": "complete",
            "missing_from_english": [],
            "missing_from_chinese": [],
            "unsupported_english_claims": [],
            "unsupported_chinese_claims": [],
            "timestamp_mismatches": [],
            "unresolved_capture_warnings": [],
        },
    }
    validation = tmp_path / "validation.json"
    english = tmp_path / "summary.md"
    chinese = tmp_path / "summary_zh.md"
    validation.write_text(json.dumps(ledger), encoding="utf-8")
    english.write_text(
        "[中文](summary_zh.md) "
        "[source](https://www.youtube.com/watch?v=abcdefghijk&t=60s)",
        encoding="utf-8",
    )
    chinese.write_text(
        "[English](summary.md) "
        "[来源](https://www.youtube.com/watch?v=abcdefghijk&t=60s)",
        encoding="utf-8",
    )

    assert validate_publication(validation, english, chinese) == []

    ledger["chunks"][0]["status"] = "pending"
    validation.write_text(json.dumps(ledger), encoding="utf-8")
    assert validate_publication(validation, english, chinese) == ["chunk 1 is not processed"]


def test_publication_requires_verbatim_quotes_from_the_chunk(tmp_path: Path) -> None:
    ledger = {
        "status": "complete",
        "metadata": {
            "source_url": "https://www.youtube.com/watch?v=abcdefghijk",
            "video_id": "abcdefghijk",
            "duration_seconds": 120,
        },
        "segment_count": 3,
        "chunks": [
            {
                "chunk_id": "chunk-001",
                "first_segment_id": "segment-0001",
                "last_segment_id": "segment-0003",
                "start_seconds": 0,
                "end_seconds": 90,
                "word_count": 3,
                "status": "processed",
                "text": "First segment second segment",
                "content_items": [
                    {
                        "disposition": "included",
                        "timestamp_seconds": 60,
                        "source_segment_ids": ["segment-0001"],
                        "quote": "First segment",
                    },
                ],
            }
        ],
        "audit": {
            "status": "complete",
            "missing_from_english": [],
            "missing_from_chinese": [],
            "unsupported_english_claims": [],
            "unsupported_chinese_claims": [],
            "timestamp_mismatches": [],
            "unresolved_capture_warnings": [],
        },
    }
    validation = tmp_path / "validation.json"
    english = tmp_path / "summary.md"
    chinese = tmp_path / "summary_zh.md"
    validation.write_text(json.dumps(ledger), encoding="utf-8")
    english.write_text(
        "[中文](summary_zh.md) "
        "[source](https://www.youtube.com/watch?v=abcdefghijk&t=60s)",
        encoding="utf-8",
    )
    chinese.write_text(
        "[English](summary.md) "
        "[来源](https://www.youtube.com/watch?v=abcdefghijk&t=60s)",
        encoding="utf-8",
    )

    assert validate_publication(validation, english, chinese) == []

    del ledger["chunks"][0]["content_items"][0]["quote"]
    validation.write_text(json.dumps(ledger), encoding="utf-8")
    assert validate_publication(validation, english, chinese) == [
        "chunk 1 item 1 has no quote"
    ]

    ledger["chunks"][0]["content_items"][0]["quote"] = "not from this chunk"
    validation.write_text(json.dumps(ledger), encoding="utf-8")
    assert validate_publication(validation, english, chinese) == [
        "chunk 1 item 1 quote is not from this chunk"
    ]
