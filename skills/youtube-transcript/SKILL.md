---
name: youtube-transcript
description: Read a YouTube page's visible Show transcript panel twice, retain validated local evidence, and create source-grounded English and Chinese summaries. Use when a user provides a YouTube link and requests a transcript, notes, summary, article, or bilingual version. Do not use for media downloads, speech recognition, third-party transcript services, or videos without a visible YouTube Transcript.
---

# Browser-only YouTube Transcript

Use the in-app Browser. Take transcript text only from YouTube's visible **Show transcript** panel. Do not call `yt-dlp`, `youtube-transcript-api`, Whisper, a third-party transcript service, OCR, or infer content from the title, description, chapters, thumbnail, comments, or model memory.

## Boundaries

- If the panel is unavailable, empty, unstable, or validation fails, report `blocked` or `partial`; do not publish a full-video summary.
- Query transcript segment elements only. Do not use a whole-page DOM snapshot, screenshots, or one browser call per segment.
- A `complete` capture proves only that two supplied browser reads have identical normalized rows and pass structural/timestamp checks. It does not prove caption accuracy, browser-export authenticity, or semantic completeness of a summary.
- Do not add recommendations, action plans, opinions, corrections, numbers, or external facts not stated in the transcript.

## Capture

1. Normalize the URL to `https://www.youtube.com/watch?v=<video-id>`. Reuse an exactly matching in-app tab or open it.
2. Open **Show transcript** and wait for transcript segment rows, not for playback.
3. Read only rows that contain an interactive transcript row and descendant `transcript-segment-view-model`. Extract timestamp and attributed text into ordered `{start_seconds, text}` rows. Read title, channel, duration, language, and subtitle type from the current player response.
4. After a short wait, repeat the exact targeted query. If either read changes, scroll only the transcript panel and retry a bounded number of times. Stop as `partial` if it cannot stabilize.
5. Save a temporary `browser-export.json` containing both complete reads. Do not calculate or supply hash fields yourself:

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

6. From the engineering repository root, run the validator through the tool module:

   ```bash
   (
     cd Codex/youtube-transcript &&
     uv run yt-transcript capture browser-export.json \
       --output ../../.local/youtube/<title-slug>--<video-id>
   )
   ```

   Continue only on `complete`; then delete the temporary export. The validator writes ignored local-only `transcript.md` and `validation.json`.

## Summarize and audit

7. Read every deterministic chunk listed in local `validation.json`, from first through last. Record each substantive claim, definition, number, example, comparison, step, qualification, limitation, conclusion, and meaningful resource as `included`, `compressed`, or pure `cta`.
8. Publish only `summary.md` and `summary_zh.md` in `YouTube/<topic>/<title-slug>--<video-id>/`. Select one existing primary topic based on the complete transcript. Add reciprocal links, a source/coverage note, and matching clickable YouTube timestamps.
9. Perform a fresh manual audit against the transcript and ledger. Record unresolved missing or unsupported claims and timestamp mismatches in `validation.json`; do not mark the audit complete while any remain.
10. Run the structural publication gate:

   ```bash
   (
     cd Codex/youtube-transcript &&
     uv run yt-transcript validate-publication \
       ../../.local/youtube/<title-slug>--<video-id>/validation.json \
       ../../YouTube/<topic>/<title-slug>--<video-id>/summary.md \
       ../../YouTube/<topic>/<title-slug>--<video-id>/summary_zh.md
   )
   ```

   It checks the ledger structure, required timestamps, timestamp parity, and reciprocal links; it does not perform semantic verification. Publish only on `complete`.

11. Update both `YouTube` catalogues. Keep raw transcripts, hashes, cue IDs, validation JSON, and tooling instructions out of published summary folders.

## Delivery report

Report source, language/subtitle type, duration, captured time range, captured/processed segment counts, audit findings, structural validation status, and any remaining manual-verification limitation.
