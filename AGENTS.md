# Repository Guidelines

## Project Structure & Module Organization

This repository is a public, bilingual engineering knowledge base. Root `README.md` is the English entry point and `README_ZH.md` is its Chinese counterpart. Keep paired documents aligned in structure, links, and factual scope. Topic material lives in `apple/`, `Claude/`, `Codex/`, `Git/`, `Ghostty/`, and `YouTube/`. Use `summary.md` and `summary_zh.md` for published video summaries. The only Python package is `Codex/youtube-transcript/`, with source in `src/yt_transcript/` and tests in `tests/`. GitHub Pages is the read-only presentation layer; the repository remains the canonical source.

## Build, Test, and Development Commands

There is no application build. Run checks for the module or site area you change:

```bash
cd Codex/youtube-transcript
uv sync --frozen --group dev  # install locked development dependencies
uv run ruff check .           # lint
uv run mypy src               # strict type-check
uv run pytest                 # test the package

cd ../../Ghostty
ghostty +validate-config --config-file=config.ghostty  # validate Ghostty configuration
```

Knowledge site:

```bash
python3 scripts/knowledge_base.py validate
python3 scripts/knowledge_base.py stage --output .pages-build
uvx --from mkdocs==1.6.1 --with mkdocs-material==9.7.7 mkdocs build --strict
```

The site stages only tracked paired Markdown documents and published YouTube summaries. It excludes `.agents/`, `AGENTS.md`, `.local/`, `.plugin-eval/`, caches, virtual environments, and raw transcript evidence.

For multiple YouTube summaries, use one pull request per batch. Do not create one branch per video or push `main` directly; the Pages deployment runs only after the validated batch is merged.

## Coding Style & Naming Conventions

Use four spaces in Python and keep lines within Ruff's 100-character limit. Maintain strict type checking and place Python tests in `tests/test_*.py`. Keep terminal setup documentation direct and platform-specific; validate Ghostty configuration with the Ghostty CLI. Use lowercase, hyphenated directory slugs for video topics and titles. Keep prose direct, reader-facing, and based on primary or official sources; label personal interpretation clearly.

## Testing & Publication

Run the relevant commands above before submitting changes. For transcript changes, update or add focused regression tests and run all lint, type, and test checks. Before publishing a video summary, run `yt-transcript validate-publication`; it must report complete. Keep capture evidence in ignored `.local/youtube/` only—never publish raw transcripts, cue IDs, hashes, or validation JSON.

## Commits, Pull Requests & Security

Use concise Conventional Commit-style subjects, such as `docs: add bilingual guide` or `fix: validate transcript coverage`. Stage only intended paths, review `git diff --staged`, and describe the user-visible change in each pull request. Link relevant issues and include screenshots only for visual changes. Never commit credentials, private keys, cloud configuration, client/employer code, machine-specific data, caches, or conversation history.
