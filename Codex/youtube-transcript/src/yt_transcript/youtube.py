from __future__ import annotations

import json
import re
import subprocess
from collections.abc import Callable
from dataclasses import replace
from urllib.parse import parse_qs, urlparse

from yt_transcript.models import SubtitleTrack, VideoProbe

_VIDEO_ID = re.compile(r"^[A-Za-z0-9_-]{11}$")


def validate_youtube_url(url: str) -> str:
    parsed = urlparse(url)
    host = (parsed.hostname or "").lower()
    video_id: str | None = None

    if host in {"youtube.com", "www.youtube.com", "m.youtube.com"} and parsed.path == "/watch":
        video_id = parse_qs(parsed.query).get("v", [None])[0]
    elif host == "youtu.be":
        video_id = parsed.path.strip("/").split("/", 1)[0]

    if video_id is None or _VIDEO_ID.fullmatch(video_id) is None:
        raise ValueError("expected a supported YouTube video URL")
    return video_id


def _is_english(language: str) -> bool:
    normalized = language.lower().replace("_", "-")
    return normalized == "en" or normalized.startswith("en-")


def select_primary_track(tracks: list[SubtitleTrack]) -> SubtitleTrack | None:
    priorities: tuple[tuple[Callable[[SubtitleTrack], bool], str], ...] = (
        (
            lambda track: track.source == "creator" and _is_english(track.language),
            "creator-provided English subtitle",
        ),
        (lambda track: track.source == "creator", "creator-provided original-language subtitle"),
        (
            lambda track: track.source == "automatic" and _is_english(track.language),
            "YouTube automatic English subtitle",
        ),
        (lambda track: track.source == "automatic", "YouTube automatic original-language subtitle"),
    )
    for predicate, reason in priorities:
        selected = next((track for track in tracks if predicate(track)), None)
        if selected is not None:
            return replace(selected, selection_reason=reason)
    return None


Runner = Callable[..., subprocess.CompletedProcess[str]]


class ProviderError(RuntimeError):
    """Raised when yt-dlp cannot return usable structured metadata."""


def _track_list(entries: object, source: str) -> list[SubtitleTrack]:
    if not isinstance(entries, dict):
        return []
    tracks: list[SubtitleTrack] = []
    for language, formats in entries.items():
        if not isinstance(language, str) or not isinstance(formats, list):
            continue
        candidates = [item for item in formats if isinstance(item, dict)]
        chosen = next((item for item in candidates if item.get("ext") == "vtt"), None)
        if chosen is None and candidates:
            chosen = candidates[0]
        if chosen is None or not isinstance(chosen.get("url"), str):
            continue
        name = chosen.get("name") if isinstance(chosen.get("name"), str) else None
        tracks.append(SubtitleTrack(language, source, chosen["url"], name))
    return tracks


def _original_automatic_tracks(entries: object, source_language: object) -> list[SubtitleTrack]:
    tracks = _track_list(entries, "automatic")
    marked_original = [
        track for track in tracks if track.language.lower().replace("_", "-").endswith("-orig")
    ]
    if marked_original:
        return marked_original
    if not isinstance(source_language, str) or not source_language:
        return tracks
    normalized = source_language.lower().replace("_", "-")
    allowed = {normalized, normalized.split("-", 1)[0]}
    original = [track for track in tracks if track.language.lower().replace("_", "-") in allowed]
    return original or tracks


def probe_video(url: str, *, runner: Runner = subprocess.run) -> VideoProbe:
    expected_id = validate_youtube_url(url)
    command = ["yt-dlp", "--dump-single-json", "--skip-download", "--no-warnings", url]
    try:
        completed = runner(command, capture_output=True, text=True, check=False)
    except FileNotFoundError as error:
        raise ProviderError("yt-dlp is not installed or not on PATH") from error
    if completed.returncode != 0:
        message = completed.stderr.strip() or "yt-dlp metadata probe failed"
        raise ProviderError(message)
    try:
        payload = json.loads(completed.stdout)
    except json.JSONDecodeError as error:
        raise ProviderError("yt-dlp returned invalid JSON metadata") from error
    if not isinstance(payload, dict) or payload.get("id") != expected_id:
        raise ProviderError("yt-dlp metadata does not match the requested video")

    tracks = _track_list(payload.get("subtitles"), "creator")
    tracks.extend(
        _original_automatic_tracks(payload.get("automatic_captions"), payload.get("language"))
    )
    duration = payload.get("duration")
    return VideoProbe(
        video_id=expected_id,
        title=str(payload.get("title") or expected_id),
        channel=payload.get("channel") if isinstance(payload.get("channel"), str) else None,
        duration_seconds=float(duration) if isinstance(duration, (int, float)) else None,
        tracks=tracks,
        selected_track=select_primary_track(tracks),
    )
