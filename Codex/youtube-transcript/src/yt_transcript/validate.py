from __future__ import annotations

from yt_transcript.models import CaptureStatus, ParseResult, ValidationResult


def validate_cues(
    parsed: ParseResult,
    video_duration_seconds: float | None,
    *,
    gap_warning_seconds: float = 30,
) -> ValidationResult:
    errors: list[str] = []
    warnings: list[str] = []

    if not parsed.cues:
        errors.append("transcript contains no valid cues")
    if parsed.discarded:
        errors.append("one or more cues were discarded")
    if video_duration_seconds is None or video_duration_seconds <= 0:
        errors.append("video duration is unavailable")

    previous = None
    for cue in parsed.cues:
        if previous is not None:
            if cue.start_seconds < previous.start_seconds:
                errors.append(f"timestamps are not monotonic at {cue.cue_id}")
            gap = cue.start_seconds - previous.end_seconds
            if gap > gap_warning_seconds:
                warnings.append(f"gap of {gap:.3f} seconds before {cue.cue_id}")
        previous = cue

    coverage_ratio: float | None = None
    if video_duration_seconds is not None and video_duration_seconds > 0 and parsed.cues:
        final_end = parsed.cues[-1].end_seconds
        coverage_ratio = min(final_end / video_duration_seconds, 1.0)
        tolerance = max(15.0, video_duration_seconds * 0.03)
        if final_end < video_duration_seconds - tolerance:
            errors.append("final cue ends too early")

    status = CaptureStatus.COMPLETE if not errors else CaptureStatus.PARTIAL
    return ValidationResult(status, coverage_ratio, warnings, errors)
