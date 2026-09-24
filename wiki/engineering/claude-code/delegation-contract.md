---
type: Pattern
title: Delegation contract
description: "What a subagent must be told up front: when it is used, what its output looks like, and which obstacles it must report."
tags: [claude-code, subagents, prompt-design]
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
  - id: gh-600-study-notes
    resource: https://github.com/kelvinlee97/engineering/blob/main/Claude/github-agentic-ai-developer/README.md
    title: "GitHub Certified: Agentic AI Developer (study notes)"
    author: human:kelvinlee97
    last_modified: 2026-09-24T14:48:10Z
generated: { by: claude-code/wiki-v1, at: 2026-09-24T16:05:00Z }
status: draft
---
Because the parent sees only the returned summary ([context isolation](context-isolation.md)), everything it needs back has to be agreed before the work starts. The course names four characteristics of an effective subagent: a specific description, structured output, obstacle reporting, and limited tool access.[^claude-subagents-course] The last one has its own page: [Least-privilege tool access](least-privilege-tool-access.md).

## The description does two jobs

The name and description of every available subagent are placed in the main agent's system prompt, and the parent uses them to decide which subagent to launch and when.[^claude-subagents-course] The description also shapes the task prompt the parent writes: a vague reviewer description can produce "find the current changes", while a stronger one can require the parent to name the exact files. Requiring citable sources in a research subagent's description carries that requirement into the delegated prompt.[^claude-subagents-course]

To make automatic use more likely, the course suggests including "proactively" and concrete trigger examples in the description. If delegation does not trigger as expected, improve the description rather than the system prompt.[^claude-subagents-course]

Skills are selected the same way: Claude matches the request against each skill's description, so a description needs the words users actually say.[^claude-agent-skills-course] See [Agent skill](agent-skill.md).

## A defined output is the biggest improvement

The course calls a defined output format the most important improvement: it acts as a checklist and gives a natural stopping point. Without it, a research subagent may not know when it has learned enough.[^claude-subagents-course] A code review output could be: summary, critical issues, major issues, minor issues, recommendations, approval status, obstacles encountered.[^claude-subagents-course]

## The same idea for whole tasks

The GH-600 course applies the contract to agent tasks on GitHub: each task needs inputs (issue context, repository scope, explicit constraints), outputs (a pull request with a structured plan, a bounded changeset, and evidence links), and success criteria that reflect the real intent, such as "vulnerability resolved" rather than just "tests passed". Criteria can be enforced as a required status check.[^gh-600-study-notes] See [Agents propose, people and policy accept](../ai-engineering/propose-accept-boundary.md).

## Obstacles are part of the result

If a subagent finds a workaround or quirk and leaves it out, the main thread must rediscover it. The output format should ask for:[^claude-subagents-course]

- setup issues and environment quirks;
- workarounds discovered during the task;
- commands that needed special flags or configuration;
- dependencies or imports that caused problems.

## Related

- Source: [GitHub Certified: Agentic AI Developer](../../sources/gh-600-study-notes.md)
- [Subagent configuration file](subagent-configuration.md): where the description and system prompt live.
- Source: [Introduction to Claude Code Subagents](../../sources/claude-subagents-course.md)
- Source: [Introduction to Claude Code Agent Skills](../../sources/claude-agent-skills-course.md)

[^claude-subagents-course]: Introduction to Claude Code Subagents (study guide)
[^claude-agent-skills-course]: Introduction to Claude Code Agent Skills (study guide)
[^gh-600-study-notes]: GitHub Certified: Agentic AI Developer (study notes)
