from __future__ import annotations

import json
from pathlib import Path

from yt_transcript.capture import load_browser_export, validate_reads, write_local_capture
from yt_transcript.models import CaptureStatus
from yt_transcript.publication import validate_publication


def export(*, second_read: dict[str, object] | None = None) -> dict[str, object]:
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
        "second_read": second_read
        if second_read is not None
        else {
            "segment_count": 3,
            "first_start_seconds": 0,
            "last_start_seconds": 9,
            "transcript_sha256": "fb10a576884310c830f02097d135b29d455e389ee6960f4f402d99fea5bce3f5",
        },
    }


def load(tmp_path: Path, payload: dict[str, object]):
    source = tmp_path / "browser-export.json"
    source.write_text(json.dumps(payload), encoding="utf-8")
    return load_browser_export(source)


def test_matching_reads_produce_a_complete_capture_and_local_files(tmp_path: Path) -> None:
    metadata, segments, second_read = load(tmp_path, export())

    validation = validate_reads(metadata, segments, second_read)
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


def test_changed_second_read_fails_closed(tmp_path: Path) -> None:
    changed = {
        "segment_count": 3,
        "first_start_seconds": 0,
        "last_start_seconds": 9,
        "transcript_sha256": "incorrect",
    }
    metadata, segments, second_read = load(tmp_path, export(second_read=changed))

    validation = validate_reads(metadata, segments, second_read)

    assert validation.status is CaptureStatus.PARTIAL
    assert validation.errors == ["the two browser reads do not match"]


def test_late_start_fails_even_when_final_segment_reaches_the_end(tmp_path: Path) -> None:
    late = [
        {"start_seconds": 20, "text": "Late opening."},
        {"start_seconds": 99, "text": "Conclusion."},
    ]
    payload = export()
    payload["segments"] = late
    payload["metadata"] = {**payload["metadata"], "duration_seconds": 100}
    payload["second_read"] = {
        "segment_count": 2,
        "first_start_seconds": 20,
        "last_start_seconds": 99,
        "transcript_sha256": "578a2a3a279be8d362821039126a8847b9d71043326cbbce5c67cda186ecd6db",
    }
    metadata, segments, second_read = load(tmp_path, payload)

    validation = validate_reads(metadata, segments, second_read)

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
    payload["second_read"] = {
        "segment_count": 4,
        "first_start_seconds": 0,
        "last_start_seconds": 10,
        "transcript_sha256": "b23060694b7f95a8b3a70dff5881c98557e874b5c8a94c23a72414930999652d",
    }
    metadata, segments, second_read = load(tmp_path, payload)

    validation = validate_reads(metadata, segments, second_read)

    assert validation.status is CaptureStatus.PARTIAL
    assert "timestamps are not strictly increasing at segment-0003" in validation.errors


def test_large_gap_is_recorded_for_auditing(tmp_path: Path) -> None:
    gapped = [
        {"start_seconds": 0, "text": "Opening."},
        {"start_seconds": 70, "text": "Later."},
        {"start_seconds": 100, "text": "Conclusion."},
    ]
    payload = export()
    payload["segments"] = gapped
    payload["metadata"] = {**payload["metadata"], "duration_seconds": 100}
    payload["second_read"] = {
        "segment_count": 3,
        "first_start_seconds": 0,
        "last_start_seconds": 100,
        "transcript_sha256": "32d0d9f0f5fc20644e7b073e9cdbf0841caea0fafea829da9cb8755da6b94920",
    }
    metadata, segments, second_read = load(tmp_path, payload)

    validation = validate_reads(metadata, segments, second_read)

    assert validation.status is CaptureStatus.COMPLETE
    assert validation.warnings == ["gap of 70.000 seconds between segment-0001 and segment-0002"]


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


def test_publication_requires_processed_chunks_a_clean_audit_and_matching_times(
    tmp_path: Path,
) -> None:
    ledger = {
        "status": "complete",
        "chunks": [
            {
                "status": "processed",
                "content_items": [
                    {"disposition": "included", "timestamp_seconds": 60},
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
        },
    }
    validation = tmp_path / "validation.json"
    english = tmp_path / "summary.md"
    chinese = tmp_path / "summary_zh.md"
    validation.write_text(json.dumps(ledger), encoding="utf-8")
    english.write_text("[source](https://www.youtube.com/watch?v=x&t=60s)", encoding="utf-8")
    chinese.write_text("[来源](https://www.youtube.com/watch?v=x&t=60s)", encoding="utf-8")

    assert validate_publication(validation, english, chinese) == []

    ledger["chunks"][0]["status"] = "pending"
    validation.write_text(json.dumps(ledger), encoding="utf-8")
    assert validate_publication(validation, english, chinese) == ["chunk 1 is not processed"]
