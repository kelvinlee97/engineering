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
  - id: claude-managed-agents
    resource: https://github.com/kelvinlee97/engineering/blob/main/Claude/managed-agents/README.md
    title: Claude Managed Agents
    author: human:kelvinlee97
    last_modified: 2026-09-24T14:48:10Z
  - id: claude-github-actions
    resource: https://github.com/kelvinlee97/engineering/blob/main/Claude/github-actions/README.md
    title: Claude Code GitHub Actions
    author: human:kelvinlee97
    last_modified: 2026-09-24T14:48:10Z
  - id: warp-self-improving-agents
    resource: https://github.com/kelvinlee97/engineering/blob/main/Claude/self-improving-agents/README.md
    title: How Warp Builds Self-Improving Agents on Claude
    author: human:kelvinlee97
    last_modified: 2026-09-24T14:48:10Z
  - id: ai-native-revenue-org
    resource: https://github.com/kelvinlee97/engineering/blob/main/Claude/ai-native-revenue-org/README.md
    title: Building an AI-Native Revenue Organization
    author: human:kelvinlee97
    last_modified: 2026-09-24T14:48:10Z
  - id: ai-native-sdlc-playbook
    resource: https://github.com/kelvinlee97/engineering/blob/main/Claude/ai-native-sdlc-playbook/README.md
    title: The AI-Native SDLC Playbook
    author: human:kelvinlee97
    last_modified: 2026-09-24T14:48:10Z
generated: { by: claude-code/wiki-v1, at: 2026-09-24T16:05:00Z }
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

Skills are not limited to Claude Code: an agent in [Claude Managed Agents](claude-managed-agents.md) bundles skills alongside its model, system prompt, tools, and MCP servers.[^claude-managed-agents]

In [Claude Code GitHub Actions](claude-code-github-actions.md), repository skills need `actions/checkout` so `.claude/skills/` exists on the runner, and plugin skills must be installed through `plugin_marketplaces` and `plugins` first.[^claude-github-actions]

## Skills are files

Because a skill is a plain file, it can be versioned, shared, and even edited by another agent: Warp's [self-improving skill loop](../ai-engineering/self-improving-skill-loop.md) has a scheduled agent propose edits to a skill through pull requests.[^warp-self-improving-agents] In a sales rollout, a top performer's routine written once as a skill can be provisioned into the team bundle, and updating the file updates it for everyone.[^ai-native-revenue-org] The AI-native SDLC playbook puts organization-wide policy in skills rather than in an ever-growing repository `CLAUDE.md`.[^ai-native-sdlc-playbook]

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

- Source: [The AI-Native SDLC Playbook](../../sources/ai-native-sdlc-playbook.md)
- Source: [Building an AI-Native Revenue Organization](../../sources/ai-native-revenue-org.md)
- Source: [How Warp Builds Self-Improving Agents on Claude](../../sources/warp-self-improving-agents.md)
- Source: [Claude Code GitHub Actions](../../sources/claude-github-actions.md)
- Source: [Claude Managed Agents](../../sources/claude-managed-agents.md)
- [Skill configuration](skill-configuration.md): frontmatter fields and directory layout.
- [Subagent](subagent.md): subagents do not inherit skills.
- Source: [Introduction to Claude Code Agent Skills](../../sources/claude-agent-skills-course.md)

[^claude-agent-skills-course]: Introduction to Claude Code Agent Skills (study guide)
[^claude-managed-agents]: Claude Managed Agents
[^claude-github-actions]: Claude Code GitHub Actions
[^warp-self-improving-agents]: How Warp Builds Self-Improving Agents on Claude
[^ai-native-revenue-org]: Building an AI-Native Revenue Organization
[^ai-native-sdlc-playbook]: The AI-Native SDLC Playbook
