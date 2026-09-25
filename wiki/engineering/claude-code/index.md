# Concept

* [Agent skills](agent-skills.md) - What a Claude Code skill is, how progressive disclosure keeps it cheap, and the SKILL.md file that defines it.
* [Auto Mode and prompt injection](auto-mode.md) - A Claude Code permission mode where a classifier reviews higher-risk actions, and the prompt-injection threat it is built to contain.
* [Claude Code extension mechanisms](extension-mechanisms.md) - How CLAUDE.md, skills, subagents, hooks, and MCP servers differ, and which job each one owns.
* [Subagents](subagents.md) - What a Claude Code subagent is, when to delegate to one, how to write its task and tools, and the file that defines it.

# Pattern

* [Claude Code session cost](session-cost.md) - What sets the cost of a Claude Code task on Opus 5.5, and how effort, model choice, caching, and compaction trade tokens against a finished task.

# Tool

* [Claude Code on GitHub](github-integration.md) - The Claude GitHub App, the Claude Code GitHub Actions workflow, and PR auto-fix, and how they fit together.
* [Claude Projects](claude-projects.md) - In the September 2026 redesign, a Claude project is one long-running conversation whose coordinator splits a goal into parallel threads sharing memory and a library.

# Service

* [Claude Managed Agents](claude-managed-agents.md) - An Anthropic-hosted agent harness that runs the agent loop, sandbox, and tools for long-running tasks, driven by events instead of your own runtime.
* [Cloud sessions](cloud-sessions.md) - Running Claude Code in a cloud container: what a session is, how its environment is configured, and how work moves between terminal and cloud.
