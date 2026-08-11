---
name: youtube-transcript
description: Read a YouTube page's visible Show transcript panel twice, prove the two reads match, retain the full transcript locally, and publish audited English and Chinese summaries. Use when a user provides a YouTube link and asks for a transcript, notes, summary, article, or bilingual version. Do not use for media downloads, speech recognition, or videos without a visible YouTube Transcript.
---

# Browser-only YouTube Transcript

Use the in-app Browser. The transcript text must come only from the YouTube **Show transcript** panel. Do not call `yt-dlp`, `youtube-transcript-api`, Whisper, a third-party transcript service, or infer content from the title, description, chapters, thumbnail, or model memory.

## Non-negotiable stop rules

- No `Show transcript`, empty transcript, unstable DOM reads, or failed validation: report `blocked` or `partial`; do not publish a full-video summary.
- Never use a whole-page DOM snapshot, screenshots/OCR, or one browser call per segment. Query only transcript segment elements.
- Never claim the full video was read until the local validator reports `complete`.
- Do not add recommendations, action plans, opinions, corrections, numbers, or factual context that the transcript did not state.

## Capture workflow

1. Normalize the supplied URL to `https://www.youtube.com/watch?v=<video-id>`. Claim the already-open in-app browser tab when it exactly matches; otherwise open the normalized URL.

2. Open **Show transcript**. If the panel is already open, reuse it. Wait for transcript segment elements, not for video playback.

3. Read only transcript rows. Use a locator that requires both an interactive transcript row and a descendant `transcript-segment-view-model`. Extract the timestamp element and attributed text element into `{start_seconds, text}` rows. Also read title, channel, video duration, language, and subtitle type from the current player response.

4. Repeat the exact targeted transcript query after a short wait. If the count or last timestamp changes, scroll only the transcript panel, then repeat until two reads match. Use a bounded number of attempts. If it never stabilizes, stop as `partial`.

5. Keep the first full, ordered browser result. For the second read, calculate the canonical SHA-256 using one line per segment, exactly `start_seconds.toFixed(3) + "\\t" + text + "\\n"`, then retain its count, first timestamp, last timestamp, and hash. This proves the two reads matched without storing the same full transcript twice.

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
  "second_read": {
    "segment_count": 1,
    "first_start_seconds": 0,
    "last_start_seconds": 0,
    "transcript_sha256": "<canonical SHA-256>"
  }
}
   ```

6. Create a local capture directory under the repository root:

   ```bash
   uv run yt-transcript capture browser-export.json \
     --output ".local/youtube/<title-slug>--<video-id>"
   ```

   Continue only if the command returns `complete`. It writes the local-only `transcript.md` and `validation.json`. Delete the temporary `browser-export.json` after the command succeeds.

## Completeness and coverage workflow

7. Read the complete local transcript from first segment to last segment, in the deterministic chunks listed in `validation.json`. Do not skip a chunk because the title or an earlier section seems sufficient.

8. For every chunk, record each substantive claim, definition, number, example, comparison, step, qualification, limitation, conclusion, and meaningful resource in the local coverage ledger. Mark each item only as:

   ```text
   included
   compressed
   cta
   ```

   `cta` is only for pure subscribe, like, comment, share, or watch-next promotion. A substantive item cannot be omitted.

9. Create an English `summary.md` and Chinese `summary_zh.md` under one topic directory:

   ```text
   YouTube/<topic>/<title-slug>--<video-id>/
   ```

   Select exactly one topic from `python`, `kubernetes`, `terraform`, `claude`, `linux`, `startup`, `finance`, `career`, `productivity`, or `general`, based on the complete transcript rather than the title. Use `claude` for Claude, LLMs, AI agents, RAG, evals, AI engineering, Anthropic, and `claude-code`; use `kubernetes` for `k8s`; `terraform` for IaC or OpenTofu; `startup` for entrepreneurship or business; and `finance` for investing or personal finance. Keep one primary topic; record secondary themes only in prose or tags, never by creating an ad-hoc folder.

10. Both summaries must use the same source-time coverage and link to each other. Include a concise source and coverage note plus clickable YouTube timestamp links. Follow the video’s natural structure; never force an application section that the video did not provide.

11. Run a fresh audit pass that compares the full transcript and coverage ledger against both summaries. It must report all of these as zero before publication:

   ```text
   unprocessed segments
   missing substantive items
   unsupported English claims
   unsupported Chinese claims
   English/Chinese coverage mismatch
   timestamp mismatch
   ```

12. Run `yt-transcript validate-publication` against the local `validation.json`, `summary.md`, and `summary_zh.md`. It must report `complete` before publication.

13. Update `YouTube/README.md` and `YouTube/README_ZH.md`. Confirm the two summary files exist, their reciprocal links work, the local evidence remains ignored by Git, and the published files contain no cue IDs, hashes, raw transcript, validation JSON, or tooling instructions.

## Delivery report

When finished, report the exact capture evidence:

```text
Transcript source
Language and subtitle type
Video duration
Captured time range
Captured / processed segment counts
Chunk or chapter coverage
Missing items
Unsupported claims
Final status
```

Do not say only “summary complete.”
