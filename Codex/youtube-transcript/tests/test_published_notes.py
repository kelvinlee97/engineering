from __future__ import annotations

from pathlib import Path

REPOSITORY_ROOT = Path(__file__).resolve().parents[3]
YOUTUBE_ROOT = REPOSITORY_ROOT / "YouTube"


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
