# YouTube Transcript Operations

## Capture

Use exactly `https://www.youtube.com/watch?v=<11-character-video-id>`. Open YouTube's Transcript panel on that tab, wait for its segments to mount, and read all mounted segments in one `evaluateAll` call. If Chrome, the transcript panel, DOM parsing, or structural validation fails, return `blocked` or `partial` immediately; do not retry or switch sources.

### Chrome transcript read

On the exact YouTube tab, expand the description if needed, open Transcript, and wait for the first segment. Then perform the only transcript read:

```js
const expand = tab.playwright.locator("#description-inline-expander #expand");
if (await expand.isVisible()) await expand.click();

const transcriptSegments = tab.playwright.locator(
  'ytd-engagement-panel-section-list-renderer[target-id="engagement-panel-searchable-transcript"]' +
    '[visibility="ENGAGEMENT_PANEL_VISIBILITY_EXPANDED"] ytd-transcript-segment-renderer',
);
if ((await transcriptSegments.count()) === 0) {
  const showTranscript = tab.playwright
    .locator("ytd-video-description-transcript-section-renderer button")
    .filter({ visible: true })
    .first();
  await showTranscript.waitFor({ state: "visible", timeoutMs: 15000 });
  await showTranscript.click();
  await transcriptSegments.first().waitFor({ state: "attached", timeoutMs: 15000 });
}

const segments = await transcriptSegments.evaluateAll((elements) =>
  elements.map((element) => {
    const timestamp = element.querySelector(".segment-timestamp")?.textContent?.trim();
    const text = element.querySelector(".segment-text")?.textContent?.replace(/\s+/g, " ").trim();
    if (!timestamp || !text) throw new Error("Malformed transcript segment");
    const parts = timestamp.split(":").map(Number);
    if (parts.length < 2 || parts.length > 3 || parts.some((part) => !Number.isFinite(part))) {
      throw new Error("Malformed transcript timestamp");
    }
    const start_seconds =
      parts.length === 3 ? parts[0] * 3600 + parts[1] * 60 + parts[2] : parts[0] * 60 + parts[1];
    return { start_seconds, text };
  }),
);
```

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
