# Architecture

```text
YouTube URL
   │
   ├─ probe ──> yt-dlp JSON metadata ──> deterministic track selection
   │                                      │
   │                              no track └─> blocked
   │
   └─ capture ─> VTT only ─> parser ─> completeness validator
                                  │              │
                                  │        partial/blocked: stop
                                  └─ complete ─> .staging/<video-id>/evidence.json
                                                    │
                                                    └─ Codex bilingual articles
                                                           │
                                                citation + topic decision
                                                           │
                                                           └─ <topic>/<title>--<id>/
```

The Python package deliberately separates provider access, subtitle parsing, completeness validation, evidence serialization, and article-contract validation. The CLI is a thin JSON interface over those layers, making it usable by people, scripts, CI, and a Codex skill.

`yt-dlp --skip-download` is used for both probing and subtitle capture. The module never requests audio extraction. Selection and validation are local and deterministic; only article writing requires an AI-capable Codex session.

Statuses are fail-closed:

- `complete`: acceptable evidence for full bilingual articles;
- `partial`: some artifact exists but the evidence contract failed;
- `blocked`: there is no eligible track or the provider cannot supply trustworthy input.

Archiving is also fail-closed. It requires complete extraction evidence, a valid bilingual summary pair, one registered flat topic, and a destination that does not already exist. Topic aliases are deterministic; secondary concepts are metadata tags.
