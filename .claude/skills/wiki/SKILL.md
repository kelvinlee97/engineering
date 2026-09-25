---
name: wiki
description: Maintain the LLM Wiki in wiki/ (an OKF v0.2 bundle). Use when the user sends a bare link (ingest it), names a legacy article to ingest, asks a question the wiki should answer (query), or asks for a wiki health check (lint).
---

# Wiki operations

The schema and page conventions are in the root `CLAUDE.md`. This file is the
procedure. Read `wiki/index.md` before any operation.

## Ingest

Input: a URL, or a legacy article path such as `Claude/subagents/README.md`.

1. **Branch.** `git fetch origin main && git checkout -B wiki/<slug> origin/main`.
2. **De-duplicate.** `grep -rIl "<url or path>" wiki raw`. If the source is
   already ingested, say so and stop, unless the user asked for a re-ingest.
3. **Capture (links only).** Fetch the page with WebFetch. If the fetch fails
   or the page has no readable text, report it and stop; never write from
   memory. Save a snapshot to `raw/<YYYY-MM-DD>-<slug>.md`:
   ```markdown
   ---
   url: <url>
   fetched: <ISO 8601 UTC>
   title: <page title>
   ---
   <the fetched text as returned, unedited>
   ```
   A YouTube link goes through `.agents/skills/youtube-transcript/SKILL.md`
   first; save its evidence-gated summary as the snapshot. Legacy articles
   need no snapshot: the article is the raw source.
4. **Read and plan.** Read the source in full. List the concepts, patterns,
   tools, and configurations it teaches. For each, check `wiki/index.md`:
   existing page → update it; missing → create it. Tell the user the plan in
   one short list (pages to create, pages to update) and continue.
5. **Write the source summary** at `wiki/sources/<slug>.md`, `type: Source
   Summary`: what the source is, its scope and coverage gaps, the takeaways,
   and links to every concept page it feeds.
6. **Write or update concept pages** under `wiki/engineering/<domain>/`.
   - Add the source to `sources` (id, resource, title, `last_modified` from
     `git log -1 --format=%cI -- <path>` for repo files).
   - Attribute every claim with `[^<source-id>]`.
   - Merge into existing prose instead of appending a per-source section.
   - Contradiction with an existing claim → both claims under
     `## Contradictions`, each with its footnote.
   - Add relative links to related pages, both directions.
   - Refresh `generated`; keep `status: draft` unless the user promoted it.
7. **Index.** Run `python -m scripts.wiki_index` to regenerate every
   `index.md` from frontmatter; never edit index entries by hand. A new domain
   under `wiki/engineering/` needs a hand-written entry in
   `wiki/engineering/index.md` (the script reports it if missing).
8. **Log.** Under today's `## YYYY-MM-DD` heading at the top of `wiki/log.md`:
   `* **Ingest**: <source title> (<source path or URL>): created <n>, updated <m> pages.`
9. **Check.** `python scripts/wiki_check.py` and `git diff --check`. Fix and
   rerun until clean.
10. **Ship.** Commit, push `wiki/<slug>`, open a pull request listing the
    pages created and updated, and enable auto-merge (squash). GitHub merges it
    once the required checks on `main` pass; if a check fails, fix it and push.
    The user reviews the result on wiki.kelvin.ink. Report the page list to the user.

## Query

1. Read `wiki/index.md`, then the relevant pages and their linked pages.
2. Answer with links to the wiki pages used. Name any gap the wiki does not
   cover and whether a raw source covers it.
3. If the answer is a comparison, analysis, or connection worth keeping, offer
   to file it as `wiki/syntheses/<slug>.md` (`type: Comparison` or
   `Synthesis`), with `sources` pointing at the wiki pages it drew on. When
   filed, index it and log `* **Query**: ...`.

## Lint

Run `python scripts/wiki_check.py`, then review the wiki for what a script
cannot see:

- contradictions between pages, and claims a newer source superseded;
- pages past `stale_after`;
- orphan pages with no inbound links;
- concepts mentioned on several pages without a page of their own;
- missing cross-links between related pages.

Report findings as a table (page, problem, proposed fix). Apply the
mechanical fixes, ask before rewriting claims, and log `* **Lint**: ...`.

## Never

- Edit or delete anything under `raw/` or the legacy article directories.
- Add facts the source does not support.
- Add `verified` to a page: that is the user's sign-off.
- Name a wiki file `README.md` or `summary.md`.
