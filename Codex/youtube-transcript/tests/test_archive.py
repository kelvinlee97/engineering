from __future__ import annotations

import json
from pathlib import Path

import pytest

from yt_transcript.archive import archive_capture, normalize_topic, slugify_title


def _complete_capture(root: Path) -> Path:
    capture = root / ".staging" / "JJyLynh5d6M"
    capture.mkdir(parents=True)
    (capture / "metadata.json").write_text(
        json.dumps(
            {
                "video_id": "JJyLynh5d6M",
                "title": "How to Actually Start Your Own Business (No-Bs Guide)",
            }
        ),
        encoding="utf-8",
    )
    (capture / "extraction-report.json").write_text(
        json.dumps({"status": "complete"}), encoding="utf-8"
    )
    (capture / "evidence.json").write_text(
        json.dumps(
            {
                "status": "complete",
                "source_url": "https://www.youtube.com/watch?v=JJyLynh5d6M",
                "title": "How to Start",
                "language": "en",
                "source_type": "automatic",
                "cues": [
                    {
                        "cue_id": "cue-0001",
                        "start_seconds": 0,
                        "end_seconds": 2,
                        "text": "Start small.",
                    }
                ],
            }
        ),
        encoding="utf-8",
    )
    (capture / "summary.en.md").write_text(
        "## Source\nS [[cue-0001]]\n## What the video says\nW\n"
        "## Practical application\nP\n## Limitations\nL\n",
        encoding="utf-8",
    )
    (capture / "summary.zh.md").write_text(
        "## 来源\n来 [[cue-0001]]\n## 视频内容\n内\n## 实际应用\n用\n## 限制\n限\n",
        encoding="utf-8",
    )
    return capture


@pytest.mark.parametrize(
    ("value", "expected"),
    [
        ("k8s", "kubernetes"),
        ("opentofu", "terraform"),
        ("ai-engineering", "claude"),
        ("LLM", "claude"),
        ("entrepreneurship", "startup"),
        ("personal-finance", "finance"),
        ("python", "python"),
    ],
)
def test_topic_aliases_are_normalized(value: str, expected: str) -> None:
    assert normalize_topic(value) == expected


@pytest.mark.parametrize("value", ["../startup", "startup/finance", "/tmp", "", "UPPER CASE"])
def test_invalid_topics_are_rejected(value: str) -> None:
    with pytest.raises(ValueError, match="topic"):
        normalize_topic(value)


def test_title_slug_is_safe_stable_and_bounded() -> None:
    slug = slugify_title(
        "How to Actually Start Your Own Business With A Very Long Practical Explanation "
        "For Complete Beginners Today (No-Bs Guide)"
    )

    assert slug.startswith("how-to-actually-start-your-own-business")
    assert "no-bs-guide" not in slug
    assert len(slug) <= 80
    assert "/" not in slug


def test_archive_moves_complete_summarized_capture_and_enriches_metadata(tmp_path: Path) -> None:
    source = _complete_capture(tmp_path)

    result = archive_capture(
        source,
        "business",
        reason="The video primarily teaches how to start and operate a business.",
        tags=["cash-flow", "marketing", "cash-flow"],
    )

    expected = tmp_path / "startup" / "how-to-actually-start-your-own-business--JJyLynh5d6M"
    assert result == expected
    assert not source.exists()
    metadata = json.loads((expected / "metadata.json").read_text(encoding="utf-8"))
    assert metadata["topic"] == "startup"
    assert metadata["tags"] == ["cash-flow", "marketing"]
    assert metadata["archive_path"] == str(expected.relative_to(tmp_path))


def test_archive_refuses_partial_capture(tmp_path: Path) -> None:
    source = _complete_capture(tmp_path)
    (source / "extraction-report.json").write_text(
        json.dumps({"status": "partial"}), encoding="utf-8"
    )

    with pytest.raises(ValueError, match="complete"):
        archive_capture(source, "startup")


def test_archive_refuses_missing_summaries(tmp_path: Path) -> None:
    source = _complete_capture(tmp_path)
    (source / "summary.zh.md").unlink()

    with pytest.raises(ValueError, match="summary"):
        archive_capture(source, "startup")


def test_archive_never_overwrites_existing_target(tmp_path: Path) -> None:
    source = _complete_capture(tmp_path)
    target = tmp_path / "startup" / "how-to-actually-start-your-own-business--JJyLynh5d6M"
    target.mkdir(parents=True)

    with pytest.raises(FileExistsError):
        archive_capture(source, "startup")
