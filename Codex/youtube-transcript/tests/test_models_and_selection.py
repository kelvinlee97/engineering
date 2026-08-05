from __future__ import annotations

import pytest

from yt_transcript.models import CaptureStatus, SubtitleTrack
from yt_transcript.youtube import select_primary_track, validate_youtube_url


@pytest.mark.parametrize(
    "url",
    [
        "https://www.youtube.com/watch?v=JJyLynh5d6M",
        "https://youtu.be/JJyLynh5d6M",
    ],
)
def test_validate_youtube_url_accepts_supported_watch_urls(url: str) -> None:
    assert validate_youtube_url(url) == "JJyLynh5d6M"


@pytest.mark.parametrize(
    "url",
    [
        "https://example.com/watch?v=JJyLynh5d6M",
        "https://www.youtube.com/results?search_query=business",
        "not-a-url",
    ],
)
def test_validate_youtube_url_rejects_non_video_urls(url: str) -> None:
    with pytest.raises(ValueError, match="YouTube video URL"):
        validate_youtube_url(url)


def test_track_selection_prefers_creator_english_then_creator_original() -> None:
    tracks = [
        SubtitleTrack(language="en", source="automatic", url="auto-en"),
        SubtitleTrack(language="ja", source="creator", url="creator-ja"),
        SubtitleTrack(language="en-US", source="creator", url="creator-en"),
    ]

    selected = select_primary_track(tracks)

    assert selected is not None
    assert selected.url == "creator-en"
    assert selected.selection_reason == "creator-provided English subtitle"


def test_track_selection_uses_creator_original_before_automatic_english() -> None:
    tracks = [
        SubtitleTrack(language="en", source="automatic", url="auto-en"),
        SubtitleTrack(language="ja", source="creator", url="creator-ja"),
    ]

    selected = select_primary_track(tracks)

    assert selected is not None
    assert selected.url == "creator-ja"


def test_track_selection_returns_none_without_tracks() -> None:
    assert select_primary_track([]) is None
    assert CaptureStatus.BLOCKED.value == "blocked"
