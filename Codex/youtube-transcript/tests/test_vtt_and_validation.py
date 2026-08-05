from __future__ import annotations

from pathlib import Path

from yt_transcript.models import CaptureStatus
from yt_transcript.validate import validate_cues
from yt_transcript.vtt import parse_vtt

FIXTURES = Path(__file__).parent / "fixtures"


def test_parse_vtt_preserves_text_timestamps_and_stable_ids() -> None:
    result = parse_vtt(FIXTURES / "complete.vtt")

    assert [cue.cue_id for cue in result.cues] == ["cue-0001", "cue-0002", "cue-0003"]
    assert result.cues[0].start_seconds == 0
    assert result.cues[-1].end_seconds == 10
    assert result.cues[1].text == "Test the smallest useful offer."
    assert result.source_cue_count == 3
    assert result.discarded == []


def test_complete_track_passes_timeline_validation() -> None:
    parsed = parse_vtt(FIXTURES / "complete.vtt")

    report = validate_cues(parsed, video_duration_seconds=10)

    assert report.status is CaptureStatus.COMPLETE
    assert report.coverage_ratio == 1.0
    assert report.errors == []


def test_vtt_header_metadata_is_not_counted_as_a_cue(tmp_path: Path) -> None:
    path = tmp_path / "metadata-header.vtt"
    path.write_text(
        "WEBVTT\nKind: captions\nLanguage: en\n\n00:00:00.000 --> 00:00:02.000\nHello\n",
        encoding="utf-8",
    )

    parsed = parse_vtt(path)

    assert parsed.source_cue_count == 1
    assert len(parsed.cues) == 1
    assert parsed.discarded == []


def test_early_ending_track_is_partial() -> None:
    parsed = parse_vtt(FIXTURES / "partial.vtt")

    report = validate_cues(parsed, video_duration_seconds=100)

    assert report.status is CaptureStatus.PARTIAL
    assert "final cue ends too early" in report.errors


def test_missing_duration_is_partial() -> None:
    parsed = parse_vtt(FIXTURES / "complete.vtt")

    report = validate_cues(parsed, video_duration_seconds=None)

    assert report.status is CaptureStatus.PARTIAL
    assert "video duration is unavailable" in report.errors


def test_malformed_cue_is_accounted_for_and_partial() -> None:
    parsed = parse_vtt(FIXTURES / "malformed.vtt")

    report = validate_cues(parsed, video_duration_seconds=2)

    assert parsed.source_cue_count == 1
    assert len(parsed.discarded) == 1
    assert report.status is CaptureStatus.PARTIAL
    assert "one or more cues were discarded" in report.errors


def test_long_silence_is_a_warning_when_ending_coverage_passes(tmp_path: Path) -> None:
    vtt = tmp_path / "silence.vtt"
    vtt.write_text(
        "WEBVTT\n\n00:00:00.000 --> 00:00:02.000\nIntro.\n\n"
        "00:00:45.000 --> 00:00:50.000\nConclusion.\n",
        encoding="utf-8",
    )

    report = validate_cues(parse_vtt(vtt), video_duration_seconds=50)

    assert report.status is CaptureStatus.COMPLETE
    assert report.warnings == ["gap of 43.000 seconds before cue-0002"]
