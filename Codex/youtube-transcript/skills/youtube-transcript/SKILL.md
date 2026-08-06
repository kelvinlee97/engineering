---
name: youtube-transcript
description: Capture an existing YouTube subtitle track temporarily, verify completeness, and publish reader-friendly English and Chinese Markdown summaries. Use when a user supplies a YouTube link and asks for its transcript, notes, summary, article, bilingual version, or actionable steps. Do not use for downloading media or transcribing videos with no subtitle track.
---

# YouTube Transcript to Bilingual Notes

Use the repository CLI to verify the complete subtitle, but retain only the final reader-facing Markdown. Never claim the whole video was read before verification succeeds.

## Workflow

1. Work from `Codex/youtube-transcript`. Confirm `uv` and `yt-dlp` are available.

2. Probe the URL. If the result is `blocked`, report that no eligible subtitle track exists and stop. Do not infer missing content from the title, description, thumbnail, or visible excerpt.

   ```bash
   uv run yt-transcript probe "<youtube-url>"
   ```

3. Create a unique temporary directory with `mktemp -d`. Capture into that exact directory and use the returned `capture_dir` for every later command.

   ```bash
   uv run yt-transcript capture "<youtube-url>" --output "<temporary-directory>"
   uv run yt-transcript verify "<capture-dir>"
   ```

4. Continue only when capture and verification both return `complete`. Read the full `evidence.json`, compare the outline against the cue sequence from beginning to end, and cover every major argument, warning, and action.

5. Draft temporary `summary.en.md` and `summary.zh.md` with the required headings and matching cue IDs, then run `validate-summaries`. These cue IDs are internal validation markers and must not appear in the published result.

6. Choose one flat topic: `python`, `kubernetes`, `terraform`, `claude`, `linux`, `startup`, `finance`, `career`, `productivity`, or `general`. Classify from the complete summary, not only the title. Claude, LLMs, agents, RAG, evals, and AI engineering use `claude`.

7. Publish only `README.md` and `README_ZH.md` under `YouTube/<topic>/<title-slug>--<video-id>/`. Follow the repository's `Claude/auto-mode` style:

   - direct English/Chinese navigation;
   - short source and coverage section;
   - natural headings and concise prose;
   - practical guidance and limitations;
   - clickable YouTube timestamp references.

   Never publish cue IDs, hashes, JSON, raw subtitles, transcripts, CLI instructions, or test output.

8. Update the English and Chinese `YouTube` catalogs. Confirm both Markdown files exist, links resolve, no internal markers remain, and any requested GitHub publication succeeds.

9. Only after the final reader artifacts pass, delete the exact temporary directory created in step 3. Do not delete partial evidence before reporting a failure; keep it only long enough to diagnose or obtain user direction.

10. Deliver the two direct reading links and a brief source-coverage note. Discuss implementation evidence only when the user asks.

## Stop Rules

- `blocked` or `partial`: do not publish a full-video article.
- Invalid or mismatched citations: revise and validate again.
- Missing reader files or broken links: do not clean up yet.
- Cleanup target differs from the exact temporary directory: stop rather than risk deleting unrelated data.

## Quality Bar

Completeness is coverage, not length. Remove repeated automatic-caption fragments, retain meaningful qualifications, represent late-video sections, and make recommendations specific enough to start immediately.
