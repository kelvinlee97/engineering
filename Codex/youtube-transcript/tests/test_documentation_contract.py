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
    assert reference_text.count("evaluateAll") == 1
    assert "do not retry" in reference_text
    assert reference_text.count("exportYouTubeTranscript") == 1
    assert "mutually exclusive" in reference_text
    assert "second_read" not in reference_text


def test_capture_reads_the_mounted_transcript_once() -> None:
    reference_text = (
        REPOSITORY_ROOT / ".agents/skills/youtube-transcript/references/operations.md"
    ).read_text(encoding="utf-8")

    reader = REPOSITORY_ROOT / ".agents/skills/youtube-transcript/scripts/read-transcript.mjs"
    reader_test = (
        REPOSITORY_ROOT / ".agents/skills/youtube-transcript/tests/read-transcript.test.mjs"
    )
    assert reader.is_file()
    assert reader_test.is_file()
    assert "readYouTubeTranscript(tab)" in reference_text
    assert "read-transcript.mjs" in reference_text
    assert "allTextContents" not in reference_text


def test_catalogue_links_to_the_tracked_skill() -> None:
    assert (REPOSITORY_ROOT / ".agents/skills/youtube-transcript/SKILL.md").is_file()
    skill_link = ".agents/skills/youtube-transcript/SKILL.md"
    assert skill_link in (REPOSITORY_ROOT / "README.md").read_text(
        encoding="utf-8"
    )
