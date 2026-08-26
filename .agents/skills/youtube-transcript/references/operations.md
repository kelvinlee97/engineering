# YouTube Transcript Operations

## Capture

Use exactly `https://www.youtube.com/watch?v=<11-character-video-id>`. Use the Chrome extension's page-content export once because it returns the complete transcript in one read. If Chrome is unavailable or the export fails structural validation, return `blocked` or `partial` immediately; do not retry or switch to the visible panel or another browser.

### Preferred Chrome export

On the exact YouTube tab, call the helper once:

```js
const rawExport = await tab.content.exportYouTubeTranscript();
```

The result is temporary plain text, typically with headers such as `Video ID`, `Language`, and `Captions`, followed by lines like `[14:24] The caption text`. Read title, channel, duration, and the normalized source URL from the same page, then convert each timestamp line into the temporary JSON shape accepted by `yt-transcript capture`:

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
  "segments": [{"start_seconds": 0, "text": "First segment"}]
}
```

Do not fetch timed-text URLs or call another transcript source to fill gaps. If the export is empty, malformed, or rejected by `yt-transcript capture`, return the failure immediately. Do not preserve the raw text under `/tmp` as part of the normal workflow.

## Export and capture

The temporary JSON export contains `metadata` (`source_url`, `video_id`, `title`, `channel`, `duration_seconds`, `language`, `subtitle_type`) and `segments`, a non-empty ordered list of `{start_seconds, text}`. The Chrome helper's raw text is evidence to parse, not the final JSON input. Do not add hashes to the temporary export.

Example: `"segments": [{"start_seconds": 0, "text": "First segment"}]`

From the engineering repository root:

```bash
(cd Codex/youtube-transcript && uv run yt-transcript capture browser-export.json --output ../../.local/youtube/<title-slug>--<video-id>)
```

Continue only on `complete`; delete `browser-export.json` on success and failure. Only complete captures write ignored `transcript.md` and `validation.json`.

## Ledger and publication

The ledger has positive `segment_count`. Chunks use `chunk-001` numbering, start at `segment-0001`, continue without gaps, and end at `segment_count`. Each chunk has `first_segment_id`, `last_segment_id`, times, `word_count`, `text`, `status`, and `content_items`; each non-CTA item has `disposition`, `timestamp_seconds`, `source_segment_ids`, and a verbatim `quote`. Set `audit.status` to `complete` only after the bilingual audit and keep `audit.unresolved_capture_warnings` empty.

Run `uv run yt-transcript validate-publication <validation.json> <summary.md> <summary_zh.md>` from `Codex/youtube-transcript`. Publish only on `complete`; the gate checks source video ID, ranges, chunk coverage, quote binding, timestamp parity, and reciprocal links, not semantic completeness.
