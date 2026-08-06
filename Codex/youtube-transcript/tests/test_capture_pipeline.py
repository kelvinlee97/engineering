from __future__ import annotations

import json
import shutil
import subprocess
from pathlib import Path

from yt_transcript.capture import capture_video, verify_capture
from yt_transcript.models import CaptureStatus
from yt_transcript.youtube import probe_video

FIXTURES = Path(__file__).parent / "fixtures"
URL = "https://www.youtube.com/watch?v=JJyLynh5d6M"


def probe_payload(*, subtitles: bool = True) -> dict[str, object]:
    return {
        "id": "JJyLynh5d6M",
        "title": "How to Start",
        "channel": "Example Channel",
        "language": "en",
        "duration": 10,
        "subtitles": {
            "en": [{"ext": "vtt", "url": "https://example.test/manual.vtt", "name": "English"}]
        }
        if subtitles
        else {},
        "automatic_captions": {
            "en": [{"ext": "vtt", "url": "https://example.test/auto.vtt", "name": "English"}]
        },
    }


def test_probe_video_builds_typed_tracks_from_structured_metadata() -> None:
    commands: list[list[str]] = []

    def runner(command: list[str], **_: object) -> subprocess.CompletedProcess[str]:
        commands.append(command)
        return subprocess.CompletedProcess(command, 0, json.dumps(probe_payload()), "")

    result = probe_video(URL, runner=runner)

    assert result.video_id == "JJyLynh5d6M"
    assert result.selected_track is not None
    assert result.selected_track.source == "creator"
    assert [track.source for track in result.tracks] == ["creator", "automatic"]
    assert commands[0][:4] == ["yt-dlp", "--dump-single-json", "--skip-download", "--no-warnings"]


def test_probe_ignores_automatic_translation_catalog() -> None:
    payload = probe_payload(subtitles=False)
    payload["automatic_captions"] = {
        "zh-Hans": [{"ext": "vtt", "url": "https://example.test/translated.vtt"}],
        "en-orig": [{"ext": "vtt", "url": "https://example.test/original.vtt"}],
    }

    def runner(command: list[str], **_: object) -> subprocess.CompletedProcess[str]:
        return subprocess.CompletedProcess(command, 0, json.dumps(payload), "")

    result = probe_video(URL, runner=runner)

    assert [track.language for track in result.tracks] == ["en-orig"]


def test_capture_video_writes_auditable_package_without_media(tmp_path: Path) -> None:
    commands: list[list[str]] = []

    def runner(command: list[str], **_: object) -> subprocess.CompletedProcess[str]:
        commands.append(command)
        if "--dump-single-json" in command:
            return subprocess.CompletedProcess(command, 0, json.dumps(probe_payload()), "")
        output_template = Path(command[command.index("--output") + 1])
        target = output_template.parent / "subtitles.en.vtt"
        shutil.copyfile(FIXTURES / "complete.vtt", target)
        return subprocess.CompletedProcess(command, 0, "", "")

    result = capture_video(URL, tmp_path, runner=runner)
    capture_dir = tmp_path / "JJyLynh5d6M"

    assert result.status is CaptureStatus.COMPLETE
    assert (capture_dir / "metadata.json").exists()
    assert (capture_dir / "extraction-report.json").exists()
    assert (capture_dir / "evidence.json").exists()
    assert (capture_dir / "transcript.md").exists()
    download_command = commands[1]
    assert "--skip-download" in download_command
    assert "--write-subs" in download_command
    assert "--extract-audio" not in download_command
    assert "--write-auto-subs" not in download_command

    evidence = json.loads((capture_dir / "evidence.json").read_text(encoding="utf-8"))
    assert evidence["status"] == "complete"
    assert evidence["cues"][0]["cue_id"] == "cue-0001"


def test_capture_without_subtitles_is_blocked_and_does_not_download(tmp_path: Path) -> None:
    commands: list[list[str]] = []

    def runner(command: list[str], **_: object) -> subprocess.CompletedProcess[str]:
        commands.append(command)
        payload = probe_payload(subtitles=False)
        payload["automatic_captions"] = {}
        return subprocess.CompletedProcess(command, 0, json.dumps(payload), "")

    result = capture_video(URL, tmp_path, runner=runner)

    assert result.status is CaptureStatus.BLOCKED
    assert len(commands) == 1
    report = json.loads(
        (tmp_path / "JJyLynh5d6M" / "extraction-report.json").read_text(encoding="utf-8")
    )
    assert report["errors"] == ["no eligible subtitle track is available"]


def test_verify_capture_recomputes_hashes_and_status(tmp_path: Path) -> None:
    def runner(command: list[str], **_: object) -> subprocess.CompletedProcess[str]:
        if "--dump-single-json" in command:
            return subprocess.CompletedProcess(command, 0, json.dumps(probe_payload()), "")
        output_template = Path(command[command.index("--output") + 1])
        shutil.copyfile(FIXTURES / "complete.vtt", output_template.parent / "subtitles.en.vtt")
        return subprocess.CompletedProcess(command, 0, "", "")

    capture_video(URL, tmp_path, runner=runner)

    verified = verify_capture(tmp_path / "JJyLynh5d6M")

    assert verified.status is CaptureStatus.COMPLETE
    assert verified.raw_sha256 is not None
    assert len(verified.raw_sha256) == 64
