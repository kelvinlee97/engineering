from __future__ import annotations

import hashlib
import json
import subprocess
from dataclasses import asdict
from datetime import UTC, datetime
from pathlib import Path

from yt_transcript.models import CaptureStatus, Cue, ExtractionReport, SubtitleTrack, VideoProbe
from yt_transcript.validate import validate_cues
from yt_transcript.vtt import parse_vtt
from yt_transcript.youtube import Runner, probe_video


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _write_json(path: Path, value: object) -> None:
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def _track_dict(track: SubtitleTrack) -> dict[str, object]:
    return {
        "language": track.language,
        "source": track.source,
        "name": track.name,
        "selection_reason": track.selection_reason,
    }


def _metadata(probe: VideoProbe, raw_file: str | None) -> dict[str, object]:
    return {
        "source_url": f"https://www.youtube.com/watch?v={probe.video_id}",
        "video_id": probe.video_id,
        "title": probe.title,
        "channel": probe.channel,
        "duration_seconds": probe.duration_seconds,
        "captured_at": datetime.now(UTC).isoformat(),
        "tracks": [_track_dict(track) for track in probe.tracks],
        "selected_track": _track_dict(probe.selected_track) if probe.selected_track else None,
        "raw_file": raw_file,
    }


def _report_dict(report: ExtractionReport) -> dict[str, object]:
    value = asdict(report)
    value["status"] = report.status.value
    return value


def _write_transcript(path: Path, probe: VideoProbe, cues: list[Cue]) -> None:
    lines = [
        f"# Transcript: {probe.title}",
        "",
        f"Source: https://www.youtube.com/watch?v={probe.video_id}",
        "",
    ]
    for cue in cues:
        lines.append(
            f"- [{cue.start_seconds:.3f}–{cue.end_seconds:.3f}] {cue.text} [[{cue.cue_id}]]"
        )
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def _blocked_package(capture_dir: Path, probe: VideoProbe) -> ExtractionReport:
    report = ExtractionReport(
        status=CaptureStatus.BLOCKED,
        errors=["no eligible subtitle track is available"],
    )
    _write_json(capture_dir / "metadata.json", _metadata(probe, None))
    _write_json(capture_dir / "extraction-report.json", _report_dict(report))
    return report


def capture_video(
    url: str, output_root: Path, *, runner: Runner = subprocess.run
) -> ExtractionReport:
    probe = probe_video(url, runner=runner)
    capture_dir = output_root / probe.video_id
    raw_dir = capture_dir / "raw"
    raw_dir.mkdir(parents=True, exist_ok=True)
    if probe.selected_track is None:
        return _blocked_package(capture_dir, probe)

    track = probe.selected_track
    output_template = raw_dir / "subtitles.%(ext)s"
    write_flag = "--write-subs" if track.source == "creator" else "--write-auto-subs"
    command = [
        "yt-dlp",
        "--skip-download",
        "--no-warnings",
        write_flag,
        "--sub-langs",
        track.language,
        "--sub-format",
        "vtt",
        "--output",
        str(output_template),
        url,
    ]
    completed = runner(command, capture_output=True, text=True, check=False)
    candidates = sorted(raw_dir.glob("subtitles*.vtt"))
    if completed.returncode != 0 or not candidates:
        report = ExtractionReport(
            status=CaptureStatus.PARTIAL,
            errors=[completed.stderr.strip() or "yt-dlp did not create a VTT subtitle file"],
        )
        _write_json(capture_dir / "metadata.json", _metadata(probe, None))
        _write_json(capture_dir / "extraction-report.json", _report_dict(report))
        return report

    raw_path = candidates[0]
    parsed = parse_vtt(raw_path)
    validation = validate_cues(parsed, probe.duration_seconds)
    transcript_path = capture_dir / "transcript.md"
    _write_transcript(transcript_path, probe, parsed.cues)
    raw_relative = str(raw_path.relative_to(capture_dir))
    report = ExtractionReport(
        status=validation.status,
        errors=validation.errors,
        warnings=validation.warnings,
        coverage_ratio=validation.coverage_ratio,
        source_cue_count=parsed.source_cue_count,
        normalized_cue_count=len(parsed.cues),
        discarded_cue_count=len(parsed.discarded),
        raw_sha256=_sha256(raw_path),
        transcript_sha256=_sha256(transcript_path),
        raw_file=raw_relative,
    )
    metadata = _metadata(probe, raw_relative)
    _write_json(capture_dir / "metadata.json", metadata)
    _write_json(capture_dir / "extraction-report.json", _report_dict(report))
    _write_json(
        capture_dir / "evidence.json",
        {
            "status": report.status.value,
            "source_url": metadata["source_url"],
            "title": probe.title,
            "language": track.language,
            "source_type": track.source,
            "cues": [asdict(cue) for cue in parsed.cues],
        },
    )
    return report


def verify_capture(capture_dir: Path) -> ExtractionReport:
    metadata = json.loads((capture_dir / "metadata.json").read_text(encoding="utf-8"))
    stored = json.loads((capture_dir / "extraction-report.json").read_text(encoding="utf-8"))
    raw_file = metadata.get("raw_file")
    if not isinstance(raw_file, str):
        return ExtractionReport(CaptureStatus.BLOCKED, errors=list(stored.get("errors", [])))
    raw_path = capture_dir / raw_file
    parsed = parse_vtt(raw_path)
    duration = metadata.get("duration_seconds")
    validation = validate_cues(
        parsed, float(duration) if isinstance(duration, (int, float)) else None
    )
    errors = list(validation.errors)
    raw_hash = _sha256(raw_path)
    if stored.get("raw_sha256") != raw_hash:
        errors.append("raw subtitle hash does not match the stored report")
    status = CaptureStatus.COMPLETE if not errors else CaptureStatus.PARTIAL
    return ExtractionReport(
        status=status,
        errors=errors,
        warnings=validation.warnings,
        coverage_ratio=validation.coverage_ratio,
        source_cue_count=parsed.source_cue_count,
        normalized_cue_count=len(parsed.cues),
        discarded_cue_count=len(parsed.discarded),
        raw_sha256=raw_hash,
        transcript_sha256=stored.get("transcript_sha256"),
        raw_file=raw_file,
    )
