from __future__ import annotations

import re
from pathlib import Path

REPOSITORY_ROOT = Path(__file__).resolve().parents[3]
YOUTUBE_ROOT = REPOSITORY_ROOT / "YouTube"
_VIDEO_LINK = re.compile(
    r"https://www\.youtube\.com/watch\?v=([A-Za-z0-9_-]{11})(?:&t=(\d+)s)?"
)


def test_each_published_capture_has_the_two_reader_facing_summaries() -> None:
    captures = list(YOUTUBE_ROOT.glob("*/*--*"))

    assert captures, "expected at least one published YouTube capture"
    for capture in captures:
        assert (capture / "summary.md").is_file(), capture
        assert (capture / "summary_zh.md").is_file(), capture


def test_catalogues_link_to_each_published_capture() -> None:
    english_catalogue = (YOUTUBE_ROOT / "README.md").read_text(encoding="utf-8")
    chinese_catalogue = (YOUTUBE_ROOT / "README_ZH.md").read_text(encoding="utf-8")

    for capture in YOUTUBE_ROOT.glob("*/*--*"):
        relative = capture.relative_to(YOUTUBE_ROOT).as_posix()
        assert f"{relative}/summary.md" in english_catalogue
        assert f"{relative}/summary_zh.md" in chinese_catalogue


def test_published_capture_folders_contain_only_reader_facing_summaries() -> None:
    for capture in YOUTUBE_ROOT.glob("*/*--*"):
        published_files = {path.name for path in capture.iterdir() if path.is_file()}
        assert published_files == {"summary.md", "summary_zh.md"}, capture


def test_published_summaries_use_one_video_and_matching_timestamps() -> None:
    for capture in YOUTUBE_ROOT.glob("*/*--*"):
        video_id = capture.name.rsplit("--", 1)[1]
        english = (capture / "summary.md").read_text(encoding="utf-8")
        chinese = (capture / "summary_zh.md").read_text(encoding="utf-8")
        english_links = _VIDEO_LINK.findall(english)
        chinese_links = _VIDEO_LINK.findall(chinese)

        assert {video for video, _ in english_links} == {video_id}, capture
        assert {video for video, _ in chinese_links} == {video_id}, capture
        assert {time for _, time in english_links if time} == {
            time for _, time in chinese_links if time
        }, capture
