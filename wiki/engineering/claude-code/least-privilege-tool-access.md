---
type: Pattern
title: Least-privilege tool access
description: Grant an agent only the tools its job requires, starting from what it must do.
tags: [claude-code, agents, security]
sources:
  - id: claude-subagents-course
    resource: https://github.com/kelvinlee97/engineering/blob/main/Claude/subagents/README.md
    title: Introduction to Claude Code Subagents (study guide)
    author: human:kelvinlee97
    last_modified: 2026-09-24T14:48:10Z
  - id: claude-agent-skills-course
    resource: https://github.com/kelvinlee97/engineering/blob/main/Claude/agent-skills/README.md
    title: Introduction to Claude Code Agent Skills (study guide)
    author: human:kelvinlee97
    last_modified: 2026-09-24T14:48:10Z
  - id: claude-auto-mode
    resource: https://github.com/kelvinlee97/engineering/blob/main/Claude/auto-mode/README.md
    title: How Claude Code Auto Mode Works
    author: human:kelvinlee97
    last_modified: 2026-09-24T14:48:10Z
  - id: claude-github-actions
    resource: https://github.com/kelvinlee97/engineering/blob/main/Claude/github-actions/README.md
    title: Claude Code GitHub Actions
    author: human:kelvinlee97
    last_modified: 2026-09-24T14:48:10Z
  - id: gh-600-study-notes
    resource: https://github.com/kelvinlee97/engineering/blob/main/Claude/github-agentic-ai-developer/README.md
    title: "GitHub Certified: Agentic AI Developer (study notes)"
    author: human:kelvinlee97
    last_modified: 2026-09-24T14:48:10Z
  - id: ai-native-sdlc-playbook
    resource: https://github.com/kelvinlee97/engineering/blob/main/Claude/ai-native-sdlc-playbook/README.md
    title: The AI-Native SDLC Playbook
    author: human:kelvinlee97
    last_modified: 2026-09-24T14:48:10Z
  - id: aws-iam
    resource: https://github.com/kelvinlee97/engineering/blob/main/AWS/iam/README.md
    title: "AWS IAM - Runbook & Reference"
    author: human:kelvinlee97
    last_modified: 2026-09-24T14:48:10Z
generated: { by: claude-code/wiki-v1, at: 2026-09-25T06:00:00Z }
status: draft
---
Least privilege means starting from what an agent must do and granting only the tools that job requires. Both Claude Code courses apply it: subagents through their `tools` list, skills through `allowed-tools`.[^claude-subagents-course][^claude-agent-skills-course] For subagents, the course gives two reasons: fewer unintended side effects, and a clearer responsibility for each subagent.[^claude-subagents-course]

## Tools by role

| Subagent role | Course-recommended access |
| --- | --- |
| Research, read-only | `Glob`, `Grep`, `Read` |
| Code reviewer | Read tools plus `Bash` for commands such as `git diff`; no edit or write |
| Styling or code modification | Add edit and write, because modification is the job |

As described in the course.[^claude-subagents-course]

The `/agents` creation screen groups tools as read-only, edit, execution, MCP, and other. A reviewer normally needs to read, may still use execution to inspect pending changes, and should not get edit or write access.[^claude-subagents-course] The chosen list is stored in the `tools` field of the [subagent configuration file](subagent-configuration.md).

## Rules versus guidance

Claude Code permission rules are the deterministic layer: `deny` blocks matching tool calls, `ask` requires confirmation even in [Auto Mode](auto-mode.md), and `allow` permits them. Auto Mode's classifier guidance (`allow`, `soft deny`, `hard deny`) only steers the classifier and is not enforcement.[^claude-auto-mode] Broad rules that allow arbitrary code execution may still be reviewed by the classifier.[^claude-auto-mode]

The AI-native SDLC playbook states the same split as a principle: use deterministic checks for enforcement and agents for judgment or diagnosis.[^ai-native-sdlc-playbook]

## Beyond a single agent

- Prefer tool allowlists over wildcards; give planning and review agents read-only tools and reserve write and execution tools for implementation agents.[^gh-600-study-notes]
- Treat adding or widening an MCP server as a reviewable, high-risk change, because it directly widens what an agent can reach.[^gh-600-study-notes]
- Inject secrets at runtime only into the components that need them; an agent's runtime does not automatically inherit repository CI secrets.[^gh-600-study-notes]
- Give workflows minimal permissions by default, such as `contents: read` and `pull-requests: write`.[^gh-600-study-notes]
- Give automated jobs their own identity, narrow permissions, short-lived credentials, and no standing production access.[^ai-native-sdlc-playbook]

## In cloud identity

AWS IAM applies the same idea: temporary credentials through roles and federation instead of long-term keys, starting from AWS managed policies and narrowing, and IAM Access Analyzer to generate least-privilege policies from actual CloudTrail activity.[^aws-iam] See [IAM policy evaluation](../aws/iam-policy-evaluation.md).

## Layers multiply

In [Claude Code GitHub Actions](claude-code-github-actions.md), effective capability is the intersection of actor checks, the job's GitHub `permissions`, and the tools Claude may invoke; granting a tool in one layer does nothing if another withholds it.[^claude-github-actions]

## Skills: `allowed-tools`

While a [skill](agent-skill.md) is active, `allowed-tools` limits which tools are available without asking for extra permission. A read-only onboarding skill might allow `Read`, `Grep`, `Glob`, and `Bash` and leave out editing tools. Leaving the field out keeps Claude's normal permission model.[^claude-agent-skills-course] Restrict tools only when the workflow needs that boundary.[^claude-agent-skills-course]

## Related

- Source: [AWS IAM - Runbook & Reference](../../sources/aws-iam.md)
- Source: [The AI-Native SDLC Playbook](../../sources/ai-native-sdlc-playbook.md)
- Source: [GitHub Certified: Agentic AI Developer](../../sources/gh-600-study-notes.md)
- Source: [Claude Code GitHub Actions](../../sources/claude-github-actions.md)
- Source: [How Claude Code Auto Mode Works](../../sources/claude-auto-mode.md)
- [Skill configuration](skill-configuration.md): where `allowed-tools` is set.
- Source: [Introduction to Claude Code Agent Skills](../../sources/claude-agent-skills-course.md)
- [Delegation contract](delegation-contract.md): tool limits are one of the course's four characteristics of an effective subagent.
- Source: [Introduction to Claude Code Subagents](../../sources/claude-subagents-course.md)

[^claude-subagents-course]: Introduction to Claude Code Subagents (study guide)
[^claude-agent-skills-course]: Introduction to Claude Code Agent Skills (study guide)
[^claude-auto-mode]: How Claude Code Auto Mode Works
[^ai-native-sdlc-playbook]: The AI-Native SDLC Playbook
[^gh-600-study-notes]: GitHub Certified: Agentic AI Developer (study notes)
[^aws-iam]: AWS IAM - Runbook & Reference
[^claude-github-actions]: Claude Code GitHub Actions
