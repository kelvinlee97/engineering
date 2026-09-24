# Concept

* [Agent skill](agent-skill.md) - A folder of task-specific instructions and optional resources that Claude Code loads only when a request matches its description.
* [Auto Mode](auto-mode.md) - A Claude Code permission mode where low-risk actions run directly and a separate classifier reviews higher-risk ones against user intent and a configured trust boundary.
* [Claude Code extension mechanisms](extension-mechanisms.md) - How CLAUDE.md, skills, subagents, hooks, and MCP servers differ, and which job each one owns.
* [Context isolation](context-isolation.md) - Keeping an agent's intermediate work out of the main context window, at the cost of losing whatever the summary leaves out.
* [Prompt injection](prompt-injection.md) - Instructions hidden in content an agent reads, such as web pages, files, or issue comments, that try to redirect it away from the user's request.
* [Subagent](subagent.md) - A worker agent that Claude Code hands a bounded task to, which runs in its own context and returns only a focused result.

# Pattern

* [Delegation contract](delegation-contract.md) - What a subagent must be told up front: when it is used, what its output looks like, and which obstacles it must report.
* [Least-privilege tool access](least-privilege-tool-access.md) - Grant an agent only the tools its job requires, starting from what it must do.
* [Progressive disclosure](progressive-disclosure.md) - Expose only a short summary up front and load detailed material into context only when the task needs it.
* [When to delegate](when-to-delegate.md) - Delegate when only the result matters to the main thread; keep work in one context when its intermediate steps matter.

# Tool

* [Claude Code GitHub Actions](claude-code-github-actions.md) - The anthropics/claude-code-action workflow step that runs Claude Code inside a GitHub Actions job, triggered by @claude mentions or a fixed prompt.
* [Claude Projects](claude-projects.md) - In the September 2026 redesign, a Claude project is one long-running conversation whose coordinator splits a goal into parallel threads sharing memory and a library.
* [Pull request auto-fix](pr-auto-fix.md) - A Claude Code cloud feature that watches a pull request and responds to CI failures and review comments, with known blind spots.

# Service

* [Claude GitHub App](claude-github-app.md) - The GitHub App that gives Claude features repository access, and which features depend on it rather than on other sign-in methods.
* [Claude Managed Agents](claude-managed-agents.md) - An Anthropic-hosted agent harness that runs the agent loop, sandbox, and tools for long-running tasks, driven by events instead of your own runtime.
* [Cloud session](cloud-session.md) - A Claude Code session that runs on an Anthropic-managed VM instead of your machine, cloning your repository from GitHub and running after you disconnect.

# Configuration

* [Cloud environment](cloud-environment.md) - The saved configuration that sets network access, environment variables, and setup scripts for Claude Code cloud sessions.
* [Skill configuration](skill-configuration.md) - The SKILL.md frontmatter fields and directory layout that define a Claude Code agent skill.
* [Subagent configuration file](subagent-configuration.md) - The Markdown file with YAML frontmatter that defines a custom Claude Code subagent, and how to create it with /agents.

# Command

* [Moving work between terminal and cloud](terminal-cloud-handoff.md) - The CLI commands that start, message, and pull down Claude Code cloud sessions, and what each one needs.
