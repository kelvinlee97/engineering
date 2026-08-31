---
name: youtube-transcript
description: Use when a user provides a YouTube URL and requests transcript-derived notes, summaries, articles, or bilingual versions. Perform one Chrome transcript read, report the first failure, and never download media or use non-transcript sources.
---

# YouTube Transcript

Read [references/operations.md](references/operations.md) before capture or publication. Use only the mounted Transcript segments exposed by the YouTube page, read together in one Chrome `evaluateAll` call. Never use timed-text URLs, page metadata, media downloads, or third-party transcript sources as transcript evidence.

## Boundaries

- Report `blocked` or `partial` immediately if Chrome, DOM parsing, or validation is unavailable or fails; do not retry or switch capture surfaces.
- `complete` proves one normalized read passed structural coverage checks, not caption accuracy, DOM-capture authenticity, or semantic completeness.
- The workflow is one-shot: never perform a second transcript read after a DOM read failure or success.
- Add no outside facts, recommendations, corrections, or opinions; preserve source numbers, names, qualifiers, modality, and uncertainty in both languages.

## Workflow

1. Normalize to `https://www.youtube.com/watch?v=<11-character-video-id>` and use one exact Chrome tab.
2. Open Transcript, wait for its segments to mount, read them in one `evaluateAll` call, and read title, channel, duration, and caption metadata from that same page.
3. Save the parsed export as temporary `browser-export.json`; do not preserve the raw text under `/tmp` as part of the normal workflow. Do not hash the raw export.
4. Run `yt-transcript capture`; continue only on `complete` and retain ignored local evidence. On any other status, stop and report the failure without retrying.
5. Process every chunk; mark substantive items `included`, `compressed`, or `cta`, with quotes and source segment IDs for non-CTA items.
6. Freshly audit both languages and resolve missing, unsupported, timestamp, and capture-warning findings.
7. Publish only the two summary files in one existing topic folder, with reciprocal links, coverage/source notes, and same-video timestamps.
8. Run `yt-transcript validate-publication`; publish only on `complete`, then update both catalogues.

## Delivery report

Report source, language/subtitle type, duration, captured range, counts, warnings, audit findings, structural status, failure reason when blocked/partial, and remaining limits.
