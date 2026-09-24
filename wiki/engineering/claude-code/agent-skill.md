---
type: Concept
title: Agent skill
description: A folder of task-specific instructions and optional resources that Claude Code loads only when a request matches its description.
tags: [claude-code, skills, agents]
sources:
  - id: claude-agent-skills-course
    resource: https://github.com/kelvinlee97/engineering/blob/main/Claude/agent-skills/README.md
    title: Introduction to Claude Code Agent Skills (study guide)
    author: human:kelvinlee97
    last_modified: 2026-09-24T14:48:10Z
generated: { by: claude-code/wiki-v1, at: 2026-09-24T15:20:00Z }
status: draft
---
An agent skill is a folder of instructions, plus optional resources, that teaches Claude Code how to handle one kind of task. Its required `SKILL.md` starts with frontmatter holding a `name` and a `description`, followed by the instructions.[^claude-agent-skills-course]

## How a skill gets used

At startup Claude Code scans the skill locations but loads only names and descriptions. It compares each request with those descriptions by meaning, not by an exact command string, and loads a matching skill on demand.[^claude-agent-skills-course] The description is therefore both discovery metadata and the main trigger. How the rest of the skill stays out of context until needed is on [Progressive disclosure](progressive-disclosure.md).

After adding, editing, or removing a skill, restart Claude Code before testing, and test with several realistic phrasings rather than the words copied from the description.[^claude-agent-skills-course]

## When a skill is the right tool

Good candidates are repeated, task-specific procedures: code-review checklists, commit formats, brand guidance, documentation templates, framework-specific debugging. Having to explain the same task repeatedly is the course's signal that a skill may be worthwhile.[^claude-agent-skills-course] Rules that always apply belong in `CLAUDE.md` instead; see [Claude Code extension mechanisms](extension-mechanisms.md).

## Where skills live and who wins a name clash

| Scope | Location | Use |
| --- | --- | --- |
| Personal | `~/.claude/skills/<skill-name>/SKILL.md` | Preferences and workflows across projects |
| Project | `.claude/skills/<skill-name>/SKILL.md` | Repository standards shared through version control |

When two skills share a name, precedence is enterprise managed, then personal, then project, then plugin. Specific names such as `frontend-review` avoid clashes better than `review`.[^claude-agent-skills-course]

## Sharing

| Audience | Method |
| --- | --- |
| One repository or team | Commit `.claude/skills` to Git |
| Several repositories or the community | Package as a plugin in a marketplace |
| Whole organization | Enterprise managed settings (highest priority) |

As described in the course.[^claude-agent-skills-course]

## Troubleshooting

Run the Agent Skills validator first to rule out structural problems, then match the symptom:[^claude-agent-skills-course]

| Symptom | Likely cause | First fix |
| --- | --- | --- |
| Does not trigger | Description does not overlap real requests | Add phrases users actually say |
| Does not load | Wrong directory, filename, or YAML | Put `SKILL.md` in a named skill directory; inspect `claude --debug` |
| Wrong skill activates | Descriptions too similar | Make scope and trigger language distinct |
| Personal skill ignored | Higher-priority skill has the same name | Check precedence; rename |
| Plugin skill absent | Cache, install, or plugin structure | Validate, clear cache, restart, reinstall |
| Runtime failure | Missing dependency, permission, bad path | Install requirements, `chmod +x` scripts, use forward slashes |

## Related

- [Skill configuration](skill-configuration.md): frontmatter fields and directory layout.
- [Subagent](subagent.md): subagents do not inherit skills.
- Source: [Introduction to Claude Code Agent Skills](../../sources/claude-agent-skills-course.md)

[^claude-agent-skills-course]: Introduction to Claude Code Agent Skills (study guide)
