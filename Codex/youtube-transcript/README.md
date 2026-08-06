# Verified YouTube Transcript

中文版本：[README_ZH.md](README_ZH.md)

A lightweight, local-first workflow that captures subtitle tracks already exposed by YouTube, verifies the resulting evidence, and gives Codex a strict contract for producing grounded English and Chinese one-page articles.

It uses `yt-dlp` for metadata and subtitle retrieval. It does **not** download video or audio, run FFmpeg, use Whisper, or include an AI model.

## Temporary Evidence

The CLI writes verification evidence under a caller-provided temporary directory:

```text
metadata.json              video and selected-track provenance
extraction-report.json     complete, partial, or blocked validation result
raw/*.vtt                  original subtitle file returned by yt-dlp
transcript.md              readable timestamped transcript with cue IDs
evidence.json              structured cues used for grounded writing
summary.en.md              temporary English validation draft
summary.zh.md              temporary Chinese validation draft
```

These files are working evidence, not final knowledge assets. After the reader-facing Markdown is published and checked, delete the temporary directory. Never commit raw subtitles or internal evidence. Subtitles may be copyrighted; review rights and privacy before sharing them.

## Installation

Requirements: Python 3.11+, [`uv`](https://docs.astral.sh/uv/), and [`yt-dlp`](https://github.com/yt-dlp/yt-dlp).

```bash
uv tool install yt-dlp
cd Codex/youtube-transcript
uv sync --group dev
```

No runtime Python packages are required beyond the standard library.

## Usage

Inspect available tracks and the deterministic selection:

```bash
uv run yt-transcript probe "https://www.youtube.com/watch?v=VIDEO_ID"
```

Capture and verify without media download, using a unique directory created by `mktemp -d`:

```bash
uv run yt-transcript capture "https://www.youtube.com/watch?v=VIDEO_ID" --output TEMP_DIR
uv run yt-transcript verify "TEMP_DIR/VIDEO_ID"
```

Validate a Codex-produced bilingual pair:

```bash
uv run yt-transcript validate-summaries \
  TEMP_DIR/VIDEO_ID/evidence.json \
  TEMP_DIR/VIDEO_ID/summary.en.md \
  TEMP_DIR/VIDEO_ID/summary.zh.md
```

Exit code `0` means complete. Exit code `2` means partial, blocked, or invalid. Every command also prints structured JSON.

## Track Selection

The default order is creator-provided English, creator-provided original language, YouTube automatic English, then YouTube automatic original language. The chosen reason is recorded. A video with no eligible subtitle track is `blocked`; this tool does not fall back to speech recognition.

## Completeness Contract

A capture is `complete` only when a VTT file is present, cues parse without loss, cue timing is valid, and the final cue reaches the end of the reported video within the configured tolerance. Raw and normalized files receive SHA-256 hashes.

The article validator additionally requires:

- capture status `complete`;
- known evidence cue citations;
- identical citation sets in both languages;
- required source, content, application, and limitation sections.

This prevents a visually polished but ungrounded or one-sided summary from passing.

## Codex Skill

The reusable skill lives at [`skills/youtube-transcript/`](skills/youtube-transcript/). Install or symlink it into your Codex skills directory, then requests such as “turn this YouTube link into bilingual one-page notes” can trigger the workflow.

The skill keeps the verification process temporary and publishes only reader-friendly `README.md` and `README_ZH.md` files under `YouTube/<topic>/<title>--<video-id>/`.

## Development

```bash
uv run pytest
uv run ruff check .
uv run mypy src
```

Tests use local fixtures and do not contact YouTube.
