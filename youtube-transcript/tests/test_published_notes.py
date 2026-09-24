from __future__ import annotations

import re
from pathlib import Path

REPOSITORY_ROOT = Path(__file__).resolve().parents[2]
YOUTUBE_ROOT = REPOSITORY_ROOT / "YouTube"
_VIDEO_LINK = re.compile(
    r"https://www\.youtube\.com/watch\?v=([A-Za-z0-9_-]{11})(?:&t=(\d+)s)?"
)


def test_each_published_capture_has_a_reader_facing_summary() -> None:
    captures = list(YOUTUBE_ROOT.glob("*/*--*"))

    assert captures, "expected at least one published YouTube capture"
    for capture in captures:
        assert (capture / "summary.md").is_file(), capture


def test_catalogue_links_to_each_published_capture() -> None:
    catalogue = (YOUTUBE_ROOT / "README.md").read_text(encoding="utf-8")

    for capture in YOUTUBE_ROOT.glob("*/*--*"):
        relative = capture.relative_to(YOUTUBE_ROOT).as_posix()
        assert f"{relative}/summary.md" in catalogue


def test_published_capture_folders_contain_only_the_reader_facing_summary() -> None:
    for capture in YOUTUBE_ROOT.glob("*/*--*"):
        published_files = {path.name for path in capture.iterdir() if path.is_file()}
        assert published_files == {"summary.md"}, capture


def test_published_summaries_use_one_video() -> None:
    for capture in YOUTUBE_ROOT.glob("*/*--*"):
        video_id = capture.name.rsplit("--", 1)[1]
        summary = (capture / "summary.md").read_text(encoding="utf-8")
        links = _VIDEO_LINK.findall(summary)

        assert {video for video, _ in links} == {video_id}, capture
