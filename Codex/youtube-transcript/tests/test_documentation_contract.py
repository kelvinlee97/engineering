from pathlib import Path

REPOSITORY_ROOT = Path(__file__).resolve().parents[3]


def test_public_capture_examples_use_a_single_complete_read() -> None:
    expected = '"segments": [{"start_seconds": 0, "text": "First segment"}]'
    assert expected in (REPOSITORY_ROOT / "Codex/youtube-transcript/README.md").read_text(
        encoding="utf-8"
    )
    reference = REPOSITORY_ROOT / ".agents/skills/youtube-transcript/references/operations.md"
    assert reference.is_file()
    reference_text = reference.read_text(encoding="utf-8")
    assert expected in reference_text
    assert reference_text.count("evaluateAll") == 2
    assert "do not retry" in reference_text
    assert "exportYouTubeTranscript" not in reference_text
    assert "second_read" not in reference_text


def test_capture_reads_the_mounted_transcript_once() -> None:
    reference_text = (
        REPOSITORY_ROOT / ".agents/skills/youtube-transcript/references/operations.md"
    ).read_text(encoding="utf-8")

    assert 'target-id="engagement-panel-searchable-transcript"' in reference_text
    assert 'visibility="ENGAGEMENT_PANEL_VISIBILITY_EXPANDED"' in reference_text
    assert "ytd-transcript-segment-renderer" in reference_text
    assert 'querySelector(".segment-timestamp")' in reference_text
    assert 'querySelector(".segment-text")' in reference_text
    assert 'throw new Error("Malformed transcript segment")' in reference_text
    assert 'throw new Error("Malformed transcript timestamp")' in reference_text
    assert "allTextContents" not in reference_text
    assert "evaluateAll" in reference_text


def test_catalogue_links_to_the_tracked_skill() -> None:
    assert (REPOSITORY_ROOT / ".agents/skills/youtube-transcript/SKILL.md").is_file()
    skill_link = ".agents/skills/youtube-transcript/SKILL.md"
    assert skill_link in (REPOSITORY_ROOT / "README.md").read_text(
        encoding="utf-8"
    )
