# YouTube Transcript Operations

## Capture

Use exactly `https://www.youtube.com/watch?v=<11-character-video-id>`. Import the repository's tested reader from an absolute path, then use it on that tab. The reader reacquires controls across YouTube SPA rerenders, opens Transcript, and reads the expanded panel in one `evaluateAll` call. If no eligible segments mount within 10 seconds, it calls `exportYouTubeTranscript` once instead. This leaves execution time for the helper before the browser's 30-second command deadline. These paths are mutually exclusive. If Chrome, both transcript paths, parsing, or structural validation fails, return `blocked` or `partial` immediately; do not retry or switch sources.

### Chrome transcript read

From the repository root, use the reader on the exact YouTube tab:

```js
const readerPath = `${nodeRepl.cwd}/.agents/skills/youtube-transcript/scripts/read-transcript.mjs`;
const { readYouTubeTranscript } = await import(readerPath);
const segments = await readYouTubeTranscript(tab);
```

The 10-second DOM deadline is condition-based rather than a fixed sleep: the reader polls fresh locators every 250 ms and never keeps a detached element handle. Only the expanded searchable Transcript panel is eligible, so hidden duplicate panels cannot enter the read. If segments mount, the helper is never called; if they do not, the helper is called exactly once and its saved export is parsed locally. Do not retry either path.

Read title, channel, duration, caption metadata, and the normalized source URL from the same page, then put `segments` into the temporary JSON shape accepted by `yt-transcript capture`:

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

Do not fetch timed-text URLs or call another transcript source to fill gaps. If the read is empty, malformed, or rejected by `yt-transcript capture`, return the failure immediately. Do not preserve raw transcript text under `/tmp` as part of the normal workflow.

## Export and capture

The temporary JSON export contains `metadata` (`source_url`, `video_id`, `title`, `channel`, `duration_seconds`, `language`, `subtitle_type`) and `segments`, a non-empty ordered list of `{start_seconds, text}`. Do not add hashes to the temporary export.

Example: `"segments": [{"start_seconds": 0, "text": "First segment"}]`

From the engineering repository root:

```bash
(cd Codex/youtube-transcript && uv run yt-transcript capture browser-export.json --output ../../.local/youtube/<title-slug>--<video-id>)
```

Continue only on `complete`; delete `browser-export.json` on success and failure. Only complete captures write ignored `transcript.md` and `validation.json`.

## Ledger and publication

The ledger has positive `segment_count`. Chunks use `chunk-001` numbering, start at `segment-0001`, continue without gaps, and end at `segment_count`. Each chunk has `first_segment_id`, `last_segment_id`, times, `word_count`, `text`, `status`, and `content_items`; each non-CTA item has `disposition`, `timestamp_seconds`, `source_segment_ids`, and a verbatim `quote`. Set `audit.status` to `complete` only after the bilingual audit and keep `audit.unresolved_capture_warnings` empty.

Run `uv run yt-transcript validate-publication <validation.json> <summary.md> <summary_zh.md>` from `Codex/youtube-transcript`. Publish only on `complete`; the gate checks source video ID, ranges, chunk coverage, quote binding, timestamp parity, and reciprocal links, not semantic completeness.
