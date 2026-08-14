# Browser-only YouTube Transcript Skill

中文版本：[README_ZH.md](README_ZH.md)

This local-first Codex Skill reads only the transcript that YouTube displays after **Show transcript** is opened. It does not download media, call `yt-dlp` or a third-party transcript API, use Whisper, or infer missing content from a title or description.

The user gives Codex a YouTube link. Codex opens the page in the in-app browser, reads the transcript DOM twice, validates both reads, saves a local `transcript.md`, and only then writes reader-facing English and Chinese summaries.

## Output contract

```text
# Ignored local evidence
.local/youtube/<title-slug>--<video-id>/
├── transcript.md
└── validation.json

# Published reading files
YouTube/<topic>/<title-slug>--<video-id>/
├── summary.md
└── summary_zh.md
```

`transcript.md` and `validation.json` are intentionally ignored by Git. Full transcripts can be copyrighted; only the reader-facing summaries are published.

## Capture contract

A browser export retains two complete ordered reads. The local validator derives their count, endpoints, and canonical SHA-256, then requires non-empty segments with strictly increasing finite timestamps, a normalized URL/video-ID match, a start close to the beginning, and an end close to the reported duration. It records gaps over 60 seconds as warnings for manual audit.

It produces deterministic chunks of roughly 1,000 words and a local `validation.json` coverage ledger. A complete capture proves structural consistency of the supplied reads; it does not prove browser-export authenticity, semantic completeness of a summary, or that YouTube's captions are word-perfect.

## Summary contract

Before publishing, the Skill must process every chunk, record every substantive item as `included`, `compressed`, or a pure `cta`, then independently audit both summaries. Publication is blocked unless:

```text
processed segments = captured segments
missing substantive items = 0
unsupported English claims = 0
unsupported Chinese claims = 0
English/Chinese timestamp mismatch = 0
```

No summary may add recommendations, plans, corrections, or outside facts. Pure subscribe, like, comment, and share calls to action may be omitted.

## Local validator

The validator uses only the Python standard library. It accepts a temporary browser export with two reads:

```json
{
  "metadata": {
    "source_url": "https://www.youtube.com/watch?v=VIDEO_ID",
    "video_id": "VIDEO_ID",
    "title": "Video title",
    "channel": "Channel name",
    "duration_seconds": 1234,
    "language": "en",
    "subtitle_type": "auto-generated"
  },
  "segments": [{"start_seconds": 0, "text": "First segment"}],
  "second_read": [{"start_seconds": 0, "text": "First segment"}]
}
```

```bash
cd Codex/youtube-transcript
uv sync --group dev
uv run yt-transcript capture browser-export.json \
  --output ../../.local/youtube/<title-slug>--<video-id>
```

This command is an internal Skill step, not a user workflow.

After the Skill marks every chunk processed and completes its manual audit, it also runs:

```bash
uv run yt-transcript validate-publication \
  ../../.local/youtube/<title-slug>--<video-id>/validation.json \
  ../../YouTube/<topic>/<title-slug>--<video-id>/summary.md \
  ../../YouTube/<topic>/<title-slug>--<video-id>/summary_zh.md
```

This gate checks ledger structure, required timestamps, timestamp parity, and reciprocal links; it does not determine whether a summary is semantically complete or source-faithful.

## Development

```bash
uv run pytest
uv run ruff check .
uv run mypy src
```
