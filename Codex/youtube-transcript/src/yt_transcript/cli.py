from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from yt_transcript.capture import load_browser_export, validate_capture, write_local_capture
from yt_transcript.models import CaptureStatus
from yt_transcript.publication import validate_publication


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="yt-transcript",
        description="Validate browser Transcript captures and publication ledgers.",
    )
    commands = parser.add_subparsers(dest="command", required=True)
    capture = commands.add_parser(
        "capture", help="Validate a browser export and write local evidence"
    )
    capture.add_argument(
        "browser_export", type=Path, help="JSON export produced from YouTube Show transcript"
    )
    capture.add_argument(
        "--output", type=Path, required=True, help="Ignored local capture directory"
    )
    publication = commands.add_parser(
        "validate-publication", help="Validate the local coverage ledger and two summaries"
    )
    publication.add_argument("validation", type=Path)
    publication.add_argument("english", type=Path)
    publication.add_argument("chinese", type=Path)
    return parser


def main() -> int:
    args = _parser().parse_args()
    try:
        if args.command == "capture":
            metadata, segments = load_browser_export(args.browser_export)
            validation = validate_capture(metadata, segments)
            payload = {
                "status": validation.status.value,
                "segment_count": validation.segment_count,
                "first_start_seconds": validation.first_start_seconds,
                "last_start_seconds": validation.last_start_seconds,
                "transcript_sha256": validation.transcript_sha256,
                "chunk_count": len(validation.chunks),
                "warnings": validation.warnings,
                "errors": validation.errors,
            }
            if validation.status is CaptureStatus.COMPLETE:
                write_local_capture(args.output, metadata, segments, validation)
            print(json.dumps(payload, ensure_ascii=False, indent=2))
            return 0 if validation.status is CaptureStatus.COMPLETE else 2
        errors = validate_publication(args.validation, args.english, args.chinese)
        print(
            json.dumps(
                {"status": "complete" if not errors else "partial", "errors": errors},
                indent=2,
            )
        )
        return 0 if not errors else 2
    except (OSError, ValueError, json.JSONDecodeError) as error:
        print(json.dumps({"status": "blocked", "errors": [str(error)]}, ensure_ascii=False))
        return 2


if __name__ == "__main__":
    sys.exit(main())
