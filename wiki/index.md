---
okf_version: "0.2"
---
# Engineering Wiki

A wiki the LLM compiles from the sources in `raw/` and the legacy articles, following the conventions in the repository's `CLAUDE.md`. Every page lists its sources; pages marked `status: draft` have not been reviewed yet.

* [Domains](engineering/) - Concept pages grouped by domain.
* [Sources](sources/) - One summary page per ingested source.
* [Syntheses](syntheses/) - Answers filed back from queries.
* [Log](log.md) - What changed and when, newest first.

# Concept

* [Subagent](engineering/claude-code/subagent.md) - A worker agent that Claude Code hands a bounded task to, which runs in its own context and returns only a focused result.
* [Context isolation](engineering/claude-code/context-isolation.md) - Keeping an agent's intermediate work out of the main context window, at the cost of losing whatever the summary leaves out.

# Pattern

* [Delegation contract](engineering/claude-code/delegation-contract.md) - What a subagent must be told up front: when it is used, what its output looks like, and which obstacles it must report.
* [When to delegate](engineering/claude-code/when-to-delegate.md) - Delegate when only the result matters to the main thread; keep work in one context when its intermediate steps matter.
* [Least-privilege tool access](engineering/claude-code/least-privilege-tool-access.md) - Grant an agent only the tools its job requires, starting from what it must do.

# Configuration

* [Subagent configuration file](engineering/claude-code/subagent-configuration.md) - The Markdown file with YAML frontmatter that defines a custom Claude Code subagent, and how to create it with /agents.

# Source Summary

* [Introduction to Claude Code Subagents (course study guide)](sources/claude-subagents-course.md) - Study guide covering all four lessons of Anthropic Academy's Introduction to subagents course.
