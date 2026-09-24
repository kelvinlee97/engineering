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

* [Agent skill](engineering/claude-code/agent-skill.md) - A folder of task-specific instructions and optional resources that Claude Code loads only when a request matches its description.
* [AI adoption maturity](engineering/ai-engineering/ai-adoption-maturity.md) - A four-stage ladder from individual chat use to end-to-end processes, driven by growing user fluency, system access, and governance.
* [Auto Mode](engineering/claude-code/auto-mode.md) - A Claude Code permission mode where low-risk actions run directly and a separate classifier reviews higher-risk ones against user intent and a configured trust boundary.
* [Claude Code extension mechanisms](engineering/claude-code/extension-mechanisms.md) - How CLAUDE.md, skills, subagents, hooks, and MCP servers differ, and which job each one owns.
* [Context isolation](engineering/claude-code/context-isolation.md) - Keeping an agent's intermediate work out of the main context window, at the cost of losing whatever the summary leaves out.
* [Prompt injection](engineering/claude-code/prompt-injection.md) - Instructions hidden in content an agent reads, such as web pages, files, or issue comments, that try to redirect it away from the user's request.
* [Subagent](engineering/claude-code/subagent.md) - A worker agent that Claude Code hands a bounded task to, which runs in its own context and returns only a focused result.

# Pattern

* [Agents propose, people and policy accept](engineering/ai-engineering/propose-accept-boundary.md) - Route every agent change through pull requests so that required checks, code owners, and approval gates, not the agent, decide what is accepted.
* [AI-native SDLC](engineering/ai-engineering/ai-native-sdlc.md) - A software delivery loop where each stage leaves a committed artifact, agents work between human approval gates, and production evidence returns as new intent.
* [Delegation contract](engineering/claude-code/delegation-contract.md) - What a subagent must be told up front: when it is used, what its output looks like, and which obstacles it must report.
* [Least-privilege tool access](engineering/claude-code/least-privilege-tool-access.md) - Grant an agent only the tools its job requires, starting from what it must do.
* [Measuring an AI rollout](engineering/ai-engineering/ai-rollout-measurement.md) - Judge an AI tooling rollout by comparing concurrent cohorts against pre-set baselines, and lead with expansion rather than hours saved.
* [Progressive disclosure](engineering/claude-code/progressive-disclosure.md) - Expose only a short summary up front and load detailed material into context only when the task needs it.
* [Risk-based autonomy](engineering/ai-engineering/risk-based-autonomy.md) - Give agents more autonomy on low-risk, reversible work and keep human approval for high-risk and production changes, widening scope gradually.
* [Self-improving skill loop](engineering/ai-engineering/self-improving-skill-loop.md) - A scheduled agent reads human feedback on another agent's output and opens a pull request that edits that agent's skill file.
* [When to delegate](engineering/claude-code/when-to-delegate.md) - Delegate when only the result matters to the main thread; keep work in one context when its intermediate steps matter.

# Tool

* [Claude Code GitHub Actions](engineering/claude-code/claude-code-github-actions.md) - The anthropics/claude-code-action workflow step that runs Claude Code inside a GitHub Actions job, triggered by @claude mentions or a fixed prompt.
* [Claude Projects](engineering/claude-code/claude-projects.md) - In the September 2026 redesign, a Claude project is one long-running conversation whose coordinator splits a goal into parallel threads sharing memory and a library.
* [Pull request auto-fix](engineering/claude-code/pr-auto-fix.md) - A Claude Code cloud feature that watches a pull request and responds to CI failures and review comments, with known blind spots.

# Service

* [Claude GitHub App](engineering/claude-code/claude-github-app.md) - The GitHub App that gives Claude features repository access, and which features depend on it rather than on other sign-in methods.
* [Claude Managed Agents](engineering/claude-code/claude-managed-agents.md) - An Anthropic-hosted agent harness that runs the agent loop, sandbox, and tools for long-running tasks, driven by events instead of your own runtime.
* [Cloud session](engineering/claude-code/cloud-session.md) - A Claude Code session that runs on an Anthropic-managed VM instead of your machine, cloning your repository from GitHub and running after you disconnect.

# Configuration

* [Cloud environment](engineering/claude-code/cloud-environment.md) - The saved configuration that sets network access, environment variables, and setup scripts for Claude Code cloud sessions.
* [Skill configuration](engineering/claude-code/skill-configuration.md) - The SKILL.md frontmatter fields and directory layout that define a Claude Code agent skill.
* [Subagent configuration file](engineering/claude-code/subagent-configuration.md) - The Markdown file with YAML frontmatter that defines a custom Claude Code subagent, and how to create it with /agents.

# Command

* [Moving work between terminal and cloud](engineering/claude-code/terminal-cloud-handoff.md) - The CLI commands that start, message, and pull down Claude Code cloud sessions, and what each one needs.

# Source Summary

* [Building an AI-Native Revenue Organization (summary)](sources/ai-native-revenue-org.md) - Summary of Anthropic's 2026-09-15 guide and eBook on rolling Claude out across a sales organization.
* [Claude Code Cloud Sessions (summary of the official docs)](sources/claude-cloud-sessions.md) - Summary of Anthropic's Use Claude Code in the cloud documentation, reviewed on 2026-09-18.
* [Claude Code GitHub Actions (summary of the official docs)](sources/claude-github-actions.md) - Summary of Anthropic's Claude Code GitHub Actions documentation for anthropics/claude-code-action@v1, reviewed on 2026-09-15.
* [Claude Managed Agents (summary of the official overview)](sources/claude-managed-agents.md) - Summary of Anthropic's Claude Managed Agents overview documentation, reviewed on 2026-09-15 while the product was in beta.
* [Claude Projects, Redesigned (announcement summary)](sources/claude-projects.md) - Summary of Anthropic's 2026-09-17 announcement that Claude Projects became one long-running conversation coordinating parallel threads.
* [GitHub Certified: Agentic AI Developer (study notes)](sources/gh-600-study-notes.md) - Study notes for GitHub's GH-600 exam and its Microsoft Learn course, with one architecture module read in full.
* [How Claude Code Auto Mode Works (video summary)](sources/claude-auto-mode.md) - Summary of Claude's 2026-08-04 video explaining how Auto Mode reviews higher-risk actions with a separate classifier.
* [How Warp Builds Self-Improving Agents on Claude (summary)](sources/warp-self-improving-agents.md) - Summary of an Anthropic post and Warp webinar on agents that improve their own skill files through reviewed pull requests.
* [Introduction to Claude Code Agent Skills (course study guide)](sources/claude-agent-skills-course.md) - Study guide covering all six lessons of Anthropic Academy's Introduction to agent skills course.
* [Introduction to Claude Code Subagents (course study guide)](sources/claude-subagents-course.md) - Study guide covering all four lessons of Anthropic Academy's Introduction to subagents course.
* [The AI-Native SDLC Playbook (summary)](sources/ai-native-sdlc-playbook.md) - Summary of Anthropic's 2026-08-21 playbook that redesigns software delivery as a loop of versioned artifacts with human approval gates.
