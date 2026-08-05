---
name: youtube-transcript
description: Capture an existing YouTube subtitle track, verify its completeness, and turn it into evidence-linked English and Chinese one-page Markdown articles. Use when a user supplies a YouTube video link and asks for its transcript, notes, summary, article, bilingual version, or actionable steps. Do not use for downloading media or transcribing videos that have no subtitle track.
---

# Verified YouTube Transcript

Turn a YouTube link into an auditable subtitle package and grounded bilingual articles. Use the repository CLI as the source of truth; never claim the whole video was read before verification succeeds.

## Prerequisites

Work from the `Codex/youtube-transcript` module. Confirm `uv` and `yt-dlp` are available. If dependencies are missing, follow the module README. Store captures outside a public repository unless the user explicitly approves publishing that transcript.

## Workflow

1. Probe the URL before writing anything:

   ```bash
   uv run yt-transcript probe "<youtube-url>"
   ```

2. If the result is `blocked`, report that YouTube exposes no eligible subtitle track and stop. Do not infer the video from its title, description, thumbnail, or partial visible transcript.

3. Capture subtitles into a private or temporary directory:

   ```bash
   uv run yt-transcript capture "<youtube-url>" --output "<capture-root>"
   ```

4. Verify the generated video directory:

   ```bash
   uv run yt-transcript verify "<capture-root>/<video-id>"
   ```

5. Continue only when both capture and verification return `complete`. Read `metadata.json`, `extraction-report.json`, and the complete `evidence.json`. Do not summarize from `transcript.md` alone.

6. Create `summary.en.md` and `summary.zh.md`. Keep both concise enough to be useful as one-page articles, but cover every major argument, sequence, warning, and concrete action found in the evidence. Use these exact level-two headings:

   English: `Source`, `What the video says`, `Practical application`, `Limitations`.

   Chinese: `来源`, `视频内容`, `实际应用`, `限制`.

7. Cite claims with stable cue IDs such as `[[cue-0042]]`. The English and Chinese versions must cite the same set of cue IDs. Clearly distinguish the speaker's claims from your practical recommendations.

8. Validate before delivery:

   ```bash
   uv run yt-transcript validate-summaries \
     "<capture-dir>/evidence.json" \
     "<capture-dir>/summary.en.md" \
     "<capture-dir>/summary.zh.md"
   ```

9. Deliver only after validation returns `complete`. State whether the selected source was creator-provided or YouTube automatic captions, its language, and any warnings from the extraction report.

## Stop Rules

- `blocked`: no trustworthy summary or “full video” claim.
- `partial`: preserve diagnostic files, explain the gap, and do not deliver a full article.
- Unknown or mismatched cue citations: revise the articles and validate again.
- Provider access failure: report the exact error; do not silently switch to audio or Whisper.

## Quality Bar

Completeness is evidence coverage, not length. Before finalizing, compare the article outline against the cue sequence from beginning to end. Ensure late-video sections are represented, remove repeated auto-caption fragments, retain meaningful qualifications, and make the final action plan specific enough to start immediately.
