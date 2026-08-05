# Troubleshooting

## `yt-dlp is not installed or not on PATH`

Run `uv tool install yt-dlp`, then verify with `yt-dlp --version`.

## Provider access fails

Update the isolated tool with `uv tool upgrade yt-dlp` and retry. YouTube can change its delivery behavior, require authentication, rate-limit requests, or restrict videos by region or age. Do not bypass access controls. If authorized cookies are required, this initial version intentionally does not handle them.

## Capture is `blocked`

The video exposes no supported subtitle track. This lightweight version has no Whisper or audio fallback, so a trustworthy full-video article cannot be produced.

## Capture is `partial`

Read `extraction-report.json`. Common causes include malformed cues, a truncated subtitle response, or a large gap between the final cue and video duration. Keep the raw VTT for diagnosis, but do not present a full summary as complete.

## Automatic captions contain repeated text

YouTube's rolling captions may repeat fragments. The parser normalizes each cue but preserves the provider's cue sequence for auditability. The writer may remove repetition in prose, while citations must still point to the supporting cues.
