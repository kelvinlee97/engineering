# Repository Guidelines

Applies to all files in this repository; a deeper `AGENTS.md` overrides it.

## Scope

This is a public bilingual engineering knowledge base. When both exist, keep paired `README.md` and `README_ZH.md` files aligned in structure, links, and factual scope. See `README.md` for the repository catalogue. Published YouTube entries contain only `summary.md` and `summary_zh.md`; raw transcript evidence stays in ignored `.local/youtube/`.

The Python module is `Codex/youtube-transcript/`; code is under `Codex/youtube-transcript/src/yt_transcript/` and tests under `Codex/youtube-transcript/tests/test_*.py`. Use lowercase, hyphenated slugs for YouTube topics and titles.

## Checks

There is no repository-wide build. Run only checks for the changed area.

Python:

```bash
(cd Codex/youtube-transcript && \
  uv sync --frozen --group dev && \
  uv run ruff check . && \
  uv run mypy src && \
  uv run pytest)
```

Ghostty:

```bash
(cd Ghostty && ghostty +validate-config --config-file=config.ghostty)
```

For Python code changes, add or update focused regression tests. For YouTube transcript work, follow `.agents/skills/youtube-transcript/SKILL.md`; publish only when its publication gate reports `complete`.

## Style and Delivery

Use four spaces in Python, Ruff's 100-character limit, and strict mypy. Keep prose direct and based on primary or official sources; keep terminal setup platform-specific and label personal interpretation.

Use concise Conventional Commit subjects. Stage only intended paths and inspect `git diff --staged`. In pull requests, describe user-visible changes, link related issues when they exist, and include screenshots for visual changes.

Never commit credentials, private keys, confidential data, private cloud configuration, client/employer code, machine-specific data, caches, or conversation history.
