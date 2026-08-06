# Privacy and Provenance

- The URL and subtitle request are sent to YouTube through `yt-dlp`; validation runs locally.
- No video or audio is downloaded by this module.
- Captures may contain copyrighted speech, personal data, or sensitive information. They are ignored by Git and should remain private unless publication is authorized.
- `metadata.json` records the video ID, canonical source URL, capture time, available tracks, subtitle selection, final topic, classification reason, tags, title slug, and archive path.
- `extraction-report.json` records validation findings and SHA-256 hashes.
- `evidence.json` preserves cue IDs used by both language versions, allowing claims to be traced back to exact subtitle intervals.
- Creator subtitles and YouTube automatic captions are identified separately. Automatic captions may contain recognition errors and should be disclosed as such.

This tool proves what subtitle evidence was processed; it does not prove that the speaker's claims are factually correct.

Captures remain in `.staging` until both articles pass their evidence contract. Archiving moves—not copies—the package into one flat topic, so secondary tags do not create duplicate copyrighted artifacts.
