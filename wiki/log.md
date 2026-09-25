# Wiki Update Log

## 2026-09-25
* **Ingest**: Coding sessions are longer and use more context. Claude Opus 5.5 is built with that in mind. (https://claude.com/blog/claude-opus-5-5-built-for-coding-sessions-that-use-more-context): created 2, updated 1 pages.
* **Lint**: Readability restructure. Merged 91 single-concept pages into 30 topic pages, so `wiki/engineering/` goes from 101 pages to 40; each topic page opens with a plain-language summary and uses sections instead of separate pages. Old URLs redirect through `aliases`. Citations now appear once per source per section, and every footnote links the source summary and the original, replacing the rows of unexplained back-link buttons. Added five diagrams (Git's four places, safe change loop, propose-accept boundary, gateway request path, ZooKeeper recovery choice). Schema updated: one topic per page, section-level citations.
* **Ingest**: Batch B part 2, six YouTube summaries (`YouTube/claude/what-happens-when-ai-agents-run-the-business`, and five under `YouTube/startup/`): created 11 pages (new `startups` domain; ai-native-company, company-brain, deterministic-vs-model-work in `ai-engineering`), updated 1 page (self-improving-skill-loop). All figures in these sources are the speakers' own and unverified; the pages say so.
* **Ingest**: Batch B part 1, nine Git sources (`Git/README.md`, `Git/publish-to-github`, and the seven tutorial chapters `Git/00-init` to `Git/06-diff`): created 16 pages in a new `git` domain. The tutorial chapters were compiled into concept, command, and playbook pages rather than one page per chapter.
* **Ingest**: Batch A part 3, six legacy sources (`Ubuntu/apt`, `Bash/README.md`, `Bash/awk`, `Bash/uniq`, `Ghostty/README.md`, `apple/container`): created 12 pages in new `linux` and `dev-tools` domains, updated 1 page (safe-change-procedure).
* **Ingest**: Batch A part 2, four ZooKeeper sources (`ZooKeeper/guides/getting-started`, `ZooKeeper/guides/production-deployment`, `ZooKeeper/runbooks/disk-full-transaction-log-recovery`, `ZooKeeper/runbooks/quorum-loss-snapshot-restore`): created 8 pages in a new `zookeeper` domain, updated 3 pages (safe-change-procedure, layered-troubleshooting, incident-closure-criteria).
* **Ingest**: Batch A part 1, six legacy operations sources (`Kubernetes/runbooks/insufficient-ip-or-eni`, `Nginx/guides/nginx-production-deployment`, `Nginx/guides/openresty-production-deployment`, `Nodejs/guides/express-bff-production-deployment`, `Nodejs/runbooks/common-express-bff-incidents`, `Nodejs/guides/modern-bff-architecture-assessment`): created 16 pages in new `kubernetes`, `web-serving`, and `operations` domains.
* **Lint**: Obsidian check found five directory links (`engineering/`, `sources/`, `syntheses/`, `ai-engineering/`, `claude-code/`) that Obsidian could not resolve, leaving index pages isolated in the graph. Pointed them at each directory's `index.md`; `wiki_check.py` now rejects directory links in indexes.

## 2026-09-24
* **Ingest**: Building an AI-Native Revenue Organization (`Claude/ai-native-revenue-org/README.md`): created 3 pages, updated 1 page (agent-skill).
* **Ingest**: GitHub Certified: Agentic AI Developer (`Claude/github-agentic-ai-developer/README.md`): created 3 pages, updated 3 pages (extension-mechanisms, least-privilege-tool-access, delegation-contract). Only module 2 was read in full.
* **Ingest**: The AI-Native SDLC Playbook (`Claude/ai-native-sdlc-playbook/README.md`): created 2 pages, updated 5 pages (propose-accept-boundary, risk-based-autonomy, agent-skill, extension-mechanisms, least-privilege-tool-access).
* **Ingest**: How Warp Builds Self-Improving Agents on Claude (`Claude/self-improving-agents/README.md`): created 2 pages, updated 1 page (agent-skill).
* **Ingest**: Claude Code GitHub Actions (`Claude/github-actions/README.md`): created 2 pages, updated 4 pages (prompt-injection, least-privilege-tool-access, claude-github-app, agent-skill).
* **Ingest**: How Claude Code Auto Mode Works (`Claude/auto-mode/README.md`): created 3 pages, updated 1 page (least-privilege-tool-access).
* **Ingest**: Claude Managed Agents (`Claude/managed-agents/README.md`): created 2 pages, updated 1 page (agent-skill).
* **Ingest**: Claude Projects, Redesigned (`Claude/projects/README.md`): created 2 pages, updated 1 page (cloud-session).
* **Ingest**: Claude Code Cloud Sessions (`Claude/cloud-sessions/README.md`): created 6 pages, updated 1 page (subagent).
* **Ingest**: Introduction to Claude Code Agent Skills (`Claude/agent-skills/README.md`): created 5 pages, updated 4 pages (subagent, subagent-configuration, least-privilege-tool-access, delegation-contract). First multi-source merge; recorded a contradiction on built-in agent names in subagent.
* **Ingest**: Introduction to Claude Code Subagents (`Claude/subagents/README.md`): created 7 pages, updated 0 pages. First ingest; pilot for the migration.
* **Initialization**: Created the bundle skeleton (root, sources, engineering, syntheses).
