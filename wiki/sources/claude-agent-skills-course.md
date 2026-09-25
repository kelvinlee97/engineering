---
type: Source Summary
title: Introduction to Claude Code Agent Skills (course study guide)
description: Study guide covering all six lessons of Anthropic Academy's Introduction to agent skills course.
tags: [claude-code, skills, course]
sources:
  - id: claude-agent-skills-course
    resource: https://github.com/kelvinlee97/engineering/blob/main/Claude/agent-skills/README.md
    title: Introduction to Claude Code Agent Skills (study guide)
    author: human:kelvinlee97
    last_modified: 2026-09-24T14:48:10Z
generated: { by: claude-code/wiki-v1, at: 2026-09-24T15:20:00Z }
status: draft
---
A study guide to Anthropic Academy's six-lesson *Introduction to agent skills* course, written in this repository as `Claude/agent-skills/README.md`. It is an original summary, not a transcript.[^claude-agent-skills-course]

## Scope and coverage

| Lesson | Coverage in the guide |
| --- | --- |
| What are skills? | Article read in full; the video had no captions, so it is summarized from the article only |
| Creating your first skill | Article and video subtitles read in full |
| Configuration and multi-file skills | Article and video subtitles read in full |
| Skills vs. other Claude Code features | Article and video subtitles read in full |
| Sharing skills | Article and video subtitles read in full |
| Troubleshooting skills | Article and video subtitles read in full |

[^claude-agent-skills-course] Upstream sources are the six course articles on anthropic.skilljar.com and their YouTube videos; this wiki cites the study guide, not the course directly.

## Takeaways

- A skill is task-specific knowledge Claude discovers from its description and loads only when relevant. See [Agent skill](../engineering/claude-code/agent-skills.md#what-a-skill-is).
- Only names and descriptions are loaded up front; detail enters context when the task needs it. See [Progressive disclosure](../engineering/claude-code/agent-skills.md#progressive-disclosure).
- `CLAUDE.md`, skills, subagents, hooks, and MCP servers each own a different job. See [Claude Code extension mechanisms](../engineering/claude-code/extension-mechanisms.md).
- `allowed-tools` applies least privilege to skills. See [Least-privilege tool access](../engineering/claude-code/subagents.md#least-privilege-tool-access).
- Subagents do not inherit skills; a custom subagent lists them in its frontmatter.[^claude-agent-skills-course] See [Subagent](../engineering/claude-code/subagents.md#what-a-subagent-is) and [Subagent configuration file](../engineering/claude-code/subagents.md#subagent-configuration-file).

## What this source changed in the wiki

It is the second Claude Code course ingested and overlaps the [subagents course](claude-subagents-course.md) on tool limits, subagent configuration, and built-in agents. The two guides name the built-in agents differently; the difference is recorded on [Subagent](../engineering/claude-code/subagents.md#contradictions).

[^claude-agent-skills-course]: Introduction to Claude Code Agent Skills (study guide), [original on GitHub](https://github.com/kelvinlee97/engineering/blob/main/Claude/agent-skills/README.md)
