# Concept

* [Subagent](subagent.md) - A worker agent that Claude Code hands a bounded task to, which runs in its own context and returns only a focused result.
* [Context isolation](context-isolation.md) - Keeping an agent's intermediate work out of the main context window, at the cost of losing whatever the summary leaves out.
* [Agent skill](agent-skill.md) - A folder of task-specific instructions and optional resources that Claude Code loads only when a request matches its description.
* [Claude Code extension mechanisms](extension-mechanisms.md) - How CLAUDE.md, skills, subagents, hooks, and MCP servers differ, and which job each one owns.

# Pattern

* [Delegation contract](delegation-contract.md) - What a subagent must be told up front: when it is used, what its output looks like, and which obstacles it must report.
* [When to delegate](when-to-delegate.md) - Delegate when only the result matters to the main thread; keep work in one context when its intermediate steps matter.
* [Least-privilege tool access](least-privilege-tool-access.md) - Grant an agent only the tools its job requires, starting from what it must do.
* [Progressive disclosure](progressive-disclosure.md) - Expose only a short summary up front and load detailed material into context only when the task needs it.

# Configuration

* [Subagent configuration file](subagent-configuration.md) - The Markdown file with YAML frontmatter that defines a custom Claude Code subagent, and how to create it with /agents.
* [Skill configuration](skill-configuration.md) - The SKILL.md frontmatter fields and directory layout that define a Claude Code agent skill.
