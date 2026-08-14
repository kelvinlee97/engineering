from pathlib import Path

REPOSITORY_ROOT = Path(__file__).resolve().parents[3]


def test_public_capture_examples_use_complete_second_reads() -> None:
    expected = '"second_read": [{"start_seconds": 0, "text": "First segment"}]'
    assert expected in (REPOSITORY_ROOT / "Codex/youtube-transcript/README.md").read_text(
        encoding="utf-8"
    )
    assert expected in (REPOSITORY_ROOT / "skills/youtube-transcript/SKILL.md").read_text(
        encoding="utf-8"
    )


def test_catalogue_links_to_the_tracked_skill() -> None:
    assert (REPOSITORY_ROOT / "skills/youtube-transcript/SKILL.md").is_file()
    assert "skills/youtube-transcript/SKILL.md" in (REPOSITORY_ROOT / "README.md").read_text(
        encoding="utf-8"
    )
