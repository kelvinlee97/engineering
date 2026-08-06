# Verified YouTube Transcript

中文版本：[README_ZH.md](README_ZH.md)

A lightweight, local-first workflow that captures subtitle tracks already exposed by YouTube, verifies the resulting evidence, and gives Codex a strict contract for producing grounded English and Chinese one-page articles.

It uses `yt-dlp` for metadata and subtitle retrieval. It does **not** download video or audio, run FFmpeg, use Whisper, or include an AI model.

## What It Produces

Captures are staged under `<output>/.staging/<video-id>/`, then archived after summarization under `<output>/<topic>/<title-slug>--<video-id>/`:

```text
metadata.json              video and selected-track provenance
extraction-report.json     complete, partial, or blocked validation result
raw/*.vtt                  original subtitle file returned by yt-dlp
transcript.md              readable timestamped transcript with cue IDs
evidence.json              structured cues used for grounded writing
summary.en.md              optional English article created by Codex
summary.zh.md              optional Chinese article created by Codex
```

Generated captures are ignored by Git by default. Subtitles may be copyrighted; review rights and privacy before sharing them.

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

Capture and verify without media download:

```bash
uv run yt-transcript capture "https://www.youtube.com/watch?v=VIDEO_ID" --output captures
uv run yt-transcript verify "captures/.staging/VIDEO_ID"
```

Validate a Codex-produced bilingual pair:

```bash
uv run yt-transcript validate-summaries \
  captures/.staging/VIDEO_ID/evidence.json \
  captures/.staging/VIDEO_ID/summary.en.md \
  captures/.staging/VIDEO_ID/summary.zh.md
```

Archive after Codex reviews the complete summary and selects its primary topic:

```bash
uv run yt-transcript archive captures/.staging/VIDEO_ID \
  --topic startup \
  --reason "The video primarily teaches startup validation and operation." \
  --tag product-market-fit
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

## Flat Learning Topics

The registry is `python`, `kubernetes`, `terraform`, `claude`, `linux`, `startup`, `finance`, `career`, `productivity`, and `general`. Codex chooses one from the complete summary. Claude, LLMs, agents, RAG, evals, and AI engineering share `claude`. Related concepts remain metadata tags rather than nested folders or duplicate captures. Common aliases such as `k8s`, `opentofu`, `business`, and `investing` are normalized automatically.

## Codex Skill

The reusable skill lives at [`skills/youtube-transcript/`](skills/youtube-transcript/). Install or symlink it into your Codex skills directory, then requests such as “turn this YouTube link into bilingual one-page notes” can trigger the workflow.

See [Architecture](docs/architecture.md), [Privacy and provenance](docs/privacy-and-provenance.md), and [Troubleshooting](docs/troubleshooting.md).

## Development

```bash
uv run pytest
uv run ruff check .
uv run mypy src
```

Tests use local fixtures and do not contact YouTube.
