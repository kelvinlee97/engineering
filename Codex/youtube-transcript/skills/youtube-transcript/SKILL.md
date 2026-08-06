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

3. Capture subtitles into the private capture root. The CLI stages the result under `.staging/<video-id>`:

   ```bash
   uv run yt-transcript capture "<youtube-url>" --output "<capture-root>"
   ```

4. Verify the staged directory returned as `capture_dir` by the CLI:

   ```bash
   uv run yt-transcript verify "<capture-root>/.staging/<video-id>"
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

9. Select exactly one flat learning topic from `python`, `kubernetes`, `terraform`, `claude`, `linux`, `startup`, `finance`, `career`, `productivity`, or `general`. Classify from the complete summary, not the title. Use `claude` for Claude, LLMs, agents, RAG, evals, and AI engineering. Use `general` when no topic clearly dominates. Keep secondary concepts as tags; never duplicate a capture.

10. Archive only after summary validation succeeds:

   ```bash
   uv run yt-transcript archive "<capture-root>/.staging/<video-id>" \
     --topic "<topic>" \
     --reason "<one-sentence classification reason>" \
     --tag "<supporting-tag>"
   ```

11. Verify the final private `capture_dir` returned by `archive`.

12. When the user wants the summary in a GitHub knowledge repository, publish only two reader-facing files under `YouTube/<topic>/<title-slug>--<video-id>/`: `README.md` and `README_ZH.md`. Match the repository's `Claude/auto-mode` style: a short source section, natural headings, concise prose, practical guidance, limitations, and clickable YouTube timestamp references. Never expose cue IDs, hashes, JSON reports, raw subtitles, CLI instructions, test output, or implementation details in this reader directory.

13. Deliver the two direct reading links. Mention technical verification only briefly unless the user asks for it.

## Stop Rules

- `blocked`: no trustworthy summary or “full video” claim.
- `partial`: preserve diagnostic files, explain the gap, and do not deliver a full article.
- Unknown or mismatched cue citations: revise the articles and validate again.
- Missing or invalid summaries: do not move the staged capture into a learning topic.
- Existing archive target: stop and preserve both directories; never overwrite.
- Provider access failure: report the exact error; do not silently switch to audio or Whisper.

## Quality Bar

Completeness is evidence coverage, not length. Before finalizing, compare the article outline against the cue sequence from beginning to end. Ensure late-video sections are represented, remove repeated auto-caption fragments, retain meaningful qualifications, and make the final action plan specific enough to start immediately.
