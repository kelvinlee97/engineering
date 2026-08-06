from __future__ import annotations

import argparse
import json
import sys
from collections.abc import Sequence
from dataclasses import asdict
from pathlib import Path

from yt_transcript.archive import archive_capture
from yt_transcript.capture import capture_video, verify_capture
from yt_transcript.models import CaptureStatus, SubtitleTrack, VideoProbe
from yt_transcript.summary_contract import load_evidence, validate_summary_pair
from yt_transcript.youtube import ProviderError, probe_video


def _emit(payload: object) -> None:
    print(json.dumps(payload, ensure_ascii=False, indent=2))


def _public_track(track: SubtitleTrack) -> dict[str, object]:
    return {
        "language": track.language,
        "source": track.source,
        "name": track.name,
        "selection_reason": track.selection_reason,
    }


def _probe_payload(probe: VideoProbe) -> dict[str, object]:
    return {
        "status": "complete" if probe.selected_track else "blocked",
        "video_id": probe.video_id,
        "title": probe.title,
        "channel": probe.channel,
        "duration_seconds": probe.duration_seconds,
        "track_count": len(probe.tracks),
        "tracks": [_public_track(track) for track in probe.tracks],
        "selected_track": _public_track(probe.selected_track) if probe.selected_track else None,
    }


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="yt-transcript",
        description="Capture and verify existing YouTube subtitle tracks without media download.",
    )
    commands = parser.add_subparsers(dest="command", required=True)

    probe = commands.add_parser("probe", help="Inspect subtitle availability and selection")
    probe.add_argument("url")

    capture = commands.add_parser("capture", help="Create an auditable subtitle evidence package")
    capture.add_argument("url")
    capture.add_argument("--output", type=Path, default=Path("captures"))

    verify = commands.add_parser("verify", help="Revalidate an existing capture package")
    verify.add_argument("capture_dir", type=Path)

    archive = commands.add_parser(
        "archive", help="Move a complete summarized capture into its flat learning topic"
    )
    archive.add_argument("capture_dir", type=Path)
    archive.add_argument("--topic", required=True)
    archive.add_argument(
        "--reason",
        default="Classified by Codex after reviewing the complete summary.",
    )
    archive.add_argument("--tag", action="append", default=[])

    summaries = commands.add_parser(
        "validate-summaries", help="Validate a bilingual summary pair against evidence"
    )
    summaries.add_argument("evidence", type=Path)
    summaries.add_argument("english", type=Path)
    summaries.add_argument("chinese", type=Path)
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = _parser().parse_args(argv)
    try:
        if args.command == "probe":
            payload = _probe_payload(probe_video(args.url))
            _emit(payload)
            return 0 if payload["status"] == "complete" else 2
        if args.command == "capture":
            report = capture_video(args.url, args.output)
            _emit({**asdict(report), "status": report.status.value})
            return 0 if report.status is CaptureStatus.COMPLETE else 2
        if args.command == "verify":
            report = verify_capture(args.capture_dir)
            _emit({**asdict(report), "status": report.status.value})
            return 0 if report.status is CaptureStatus.COMPLETE else 2
        if args.command == "archive":
            target = archive_capture(
                args.capture_dir,
                args.topic,
                reason=args.reason,
                tags=args.tag,
            )
            _emit({"status": "complete", "capture_dir": str(target)})
            return 0
        if args.command == "validate-summaries":
            evidence = load_evidence(args.evidence)
            errors = validate_summary_pair(
                evidence,
                args.english.read_text(encoding="utf-8"),
                args.chinese.read_text(encoding="utf-8"),
            )
            _emit({"status": "complete" if not errors else "blocked", "errors": errors})
            return 0 if not errors else 2
    except (OSError, ValueError, ProviderError, json.JSONDecodeError) as error:
        _emit({"status": "blocked", "errors": [str(error)]})
        return 2
    return 2


if __name__ == "__main__":
    sys.exit(main())
