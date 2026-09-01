# Introduction to Claude Code Agent Skills

Chinese version: [README_ZH.md](README_ZH.md)

This is a complete study guide to Anthropic Academy's **Introduction to agent skills**
course. It covers all six written lessons and the accessible subtitles from the official
videos. It is an original summary, not a transcript or a replacement for the course.

## Source coverage

| Lesson | Official article | Official video | Coverage status |
| --- | --- | --- | --- |
| [What are skills?](https://anthropic.skilljar.com/introduction-to-agent-skills/434525) | Read in full | [Video](https://www.youtube.com/watch?v=bjdBVZa66oU), no captions available | Article complete; video captions unavailable |
| [Creating your first skill](https://anthropic.skilljar.com/introduction-to-agent-skills/434527) | Read in full | [Video](https://www.youtube.com/watch?v=Wx6_vjFFyHM), English auto-generated subtitles read in full | Complete |
| [Configuration and multi-file skills](https://anthropic.skilljar.com/introduction-to-agent-skills/434526) | Read in full | [Video](https://www.youtube.com/watch?v=98KaK_rn5rQ), English auto-generated subtitles read in full | Complete |
| [Skills vs. other Claude Code features](https://anthropic.skilljar.com/introduction-to-agent-skills/434528) | Read in full | [Video](https://www.youtube.com/watch?v=IgNN4v0BJdU), English auto-generated subtitles read in full | Complete |
| [Sharing skills](https://anthropic.skilljar.com/introduction-to-agent-skills/434529) | Read in full | [Video](https://www.youtube.com/watch?v=OCBi3eScNLk), English auto-generated subtitles read in full | Complete |
| [Troubleshooting skills](https://anthropic.skilljar.com/introduction-to-agent-skills/434530) | Read in full | [Video](https://www.youtube.com/watch?v=YBa1cwaG7is), English auto-generated subtitles read in full | Complete |

The first lesson's embedded video has no exportable captions. Its written lesson contains the
same stated learning goals and key takeaways, so that lesson is summarized from the article only.
No transcript or timestamps have been invented.

## The course in one mental model

> A skill is task-specific knowledge that Claude discovers from its description and loads only
> when relevant. Keep always-on rules elsewhere, isolate delegated work in subagents, and use
> hooks or MCP when the requirement is an event or an external capability.

The six lessons form one sequence:

1. **Recognize the fit:** encode repeated, task-specific instructions as a skill.
2. **Build the minimum:** create one named directory containing `SKILL.md`.
3. **Scale by disclosure:** keep the entrypoint small and load references or scripts as needed.
4. **Choose the right mechanism:** do not force project rules, delegation, events, or tools into a skill.
5. **Distribute deliberately:** use Git, plugins, or managed settings according to audience.
6. **Debug systematically:** validate structure, then check matching, priority, and runtime failures.

## Lesson 1 — What are skills?

### Definition and discovery

A skill is a folder of instructions and optional resources that teaches Claude Code how to handle
a particular kind of task. Its required `SKILL.md` starts with frontmatter containing a `name` and
`description`; the instructions follow below the frontmatter.

Claude initially sees skill names and descriptions, compares an incoming request with those
descriptions, and loads a matching skill on demand. The description is therefore both discovery
metadata and the main trigger signal.

### Where skills live

| Scope | Course location | Intended use |
| --- | --- | --- |
| Personal | `~/.claude/skills/<skill-name>/SKILL.md` | Preferences and workflows used across projects |
| Project | `.claude/skills/<skill-name>/SKILL.md` | Repository-specific standards shared through version control |

On Windows, the personal root is `C:/Users/<your-user>/.claude/skills`.

### Why skills are different

- `CLAUDE.md` is always loaded and is appropriate for rules that always apply.
- Skills load only when relevant, preserving context for unrelated work.
- Slash commands require explicit invocation; skills can activate from the intent of a normal request.

Good candidates include code-review checklists, commit formats, brand guidance, documentation
templates, and framework-specific debugging procedures. The course's rule of thumb is practical:
repeatedly explaining the same task is evidence that a skill may be worthwhile.

Official source: [What are skills?](https://anthropic.skilljar.com/introduction-to-agent-skills/434525)

## Lesson 2 — Creating your first skill

### Minimal structure

Create a directory named after the skill, then add `SKILL.md`:

```text
~/.claude/skills/pr-description/
└── SKILL.md
```

```markdown
---
name: pr-description
description: Writes pull request descriptions. Use when creating or summarizing a pull request.
---

When writing a PR description:

1. Inspect the complete branch diff.
2. Explain what changed and why.
3. List the concrete changes and any renamed or deleted files.
```

The course separates the two responsibilities clearly: `name` identifies the skill,
`description` determines when it matches, and the body defines what Claude should do after loading
it.

Video references: [00:18–00:46](https://www.youtube.com/watch?v=Wx6_vjFFyHM&t=18s)

### Loading and matching

At startup, Claude Code scans the configured skill locations but initially loads only names and
descriptions. It uses semantic overlap, rather than an exact command string, to match a request.
After editing, adding, or removing a skill, the course instructs learners to restart Claude Code
before testing the change.

Test with realistic wording, not just the exact phrases copied into the description. A successful
test verifies both discovery and whether the output follows the body instructions.

### Priority for name conflicts

The course gives this precedence order:

1. Enterprise managed skills.
2. Personal skills.
3. Project skills.
4. Plugin skills.

Descriptive names such as `frontend-review` reduce accidental conflicts better than broad names
such as `review`.

Official source: [Creating your first skill](https://anthropic.skilljar.com/introduction-to-agent-skills/434527)

## Lesson 3 — Configuration and multi-file skills

### Frontmatter fields

| Field | Requirement | Course guidance |
| --- | --- | --- |
| `name` | Required | Lowercase letters, numbers, and hyphens; at most 64 characters; match the directory name |
| `description` | Required | At most 1,024 characters; say what the skill does and when to use it |
| `allowed-tools` | Optional | Restrict tools for read-only or security-sensitive workflows |
| `model` | Optional | Select a model for the skill when needed |

The description should contain language users are likely to use. If a performance skill should
match “why is this slow?” or “help me profile this,” its description needs enough semantic overlap
with those requests.

Video references: [00:12–00:43](https://www.youtube.com/watch?v=98KaK_rn5rQ&t=12s)

### Least-privilege tool access

`allowed-tools` limits which tools are available without additional permission while a skill is
active. A read-only onboarding skill might allow `Read`, `Grep`, `Glob`, and `Bash` but omit editing
tools. Omitting the field leaves Claude's normal permission model in place.

### Progressive disclosure

Keep the essential workflow in `SKILL.md` and move conditional detail into supporting files:

```text
my-skill/
├── SKILL.md
├── references/
├── scripts/
└── assets/
```

The entrypoint should say when to read each reference or run each script. The course recommends
keeping `SKILL.md` under 500 lines and splitting supporting material when it grows beyond that.
Scripts are especially context-efficient: tell Claude to run a tested script, so only its output
rather than its source needs to enter the working context.

Official source: [Configuration and multi-file skills](https://anthropic.skilljar.com/introduction-to-agent-skills/434526)

## Lesson 4 — Skills vs. other Claude Code features

### Pick by behavior

| Mechanism | What distinguishes it | Use it for |
| --- | --- | --- |
| `CLAUDE.md` | Always loaded | Project-wide rules and constraints |
| Skill | Request-matched and loaded on demand | Task-specific knowledge and procedures |
| Subagent | Separate execution context | Isolated delegated work or different tool access |
| Hook | Triggered by an event | Repeatable checks or side effects around tool actions |
| MCP server | Supplies external capabilities | Integrations, data sources, and tools |

Video references: [00:02–00:38](https://www.youtube.com/watch?v=IgNN4v0BJdU&t=2s)

Skills extend the current conversation. Subagents leave it, do independent work, and return a
result. Hooks react to events rather than the meaning of a request. MCP is a capability boundary,
not an instruction format.

These mechanisms are complementary. A project can use `CLAUDE.md` for permanent rules, a skill for
PR-review knowledge, a hook for automatic validation, a subagent for an isolated review, and MCP
for external services without making any one mechanism carry all five responsibilities.

Official source: [Skills vs. other Claude Code features](https://anthropic.skilljar.com/introduction-to-agent-skills/434528)

## Lesson 5 — Sharing skills

### Distribution choices

| Audience | Distribution method | Best fit |
| --- | --- | --- |
| One repository or team | Commit `.claude/skills` to Git | Project-specific workflows and standards |
| Multiple repositories or the community | Package skills in a plugin and marketplace | Reusable, non-project-specific skills |
| Entire organization | Enterprise managed settings | Mandatory security, compliance, and coding standards |

Repository skills update through the team's normal pull workflow. Plugins make a reusable bundle
installable across projects. Enterprise skills have the highest priority and are appropriate when
the standard must apply organization-wide.

Video references: [00:20–00:41](https://www.youtube.com/watch?v=OCBi3eScNLk&t=20s)

### Skills and subagents

Subagents do not automatically inherit the main conversation's skills:

- Built-in agents such as Explorer, Plan, and Verify cannot access skills.
- Custom subagents can use skills only when their frontmatter explicitly lists them.
- Listed skills load when the custom subagent starts, rather than matching on demand.

```yaml
---
name: frontend-reviewer
description: Review frontend changes for accessibility and performance.
tools: Bash, Glob, Grep, Read
model: sonnet
skills: accessibility-audit, performance-check
---
```

The referenced skills must already exist in an available skills directory. This arrangement is
useful when isolated work must apply a consistent, named set of standards.

Official source: [Sharing skills](https://anthropic.skilljar.com/introduction-to-agent-skills/434529)

## Lesson 6 — Troubleshooting skills

### Diagnose in order

Start with the Agent Skills validator so structural failures are eliminated before behavioral
debugging. Then classify the symptom:

| Symptom | Likely cause | First fix |
| --- | --- | --- |
| Does not trigger | Description does not overlap real requests | Add specific phrases users actually say |
| Does not load | Wrong directory, filename, or YAML | Put exact `SKILL.md` inside a named skill directory and inspect `claude --debug` |
| Wrong skill activates | Descriptions are too similar | Make scope and trigger language distinct |
| Personal skill is ignored | Higher-priority skill has the same name | Check precedence and rename the lower-priority skill |
| Plugin skill is absent | Cache, installation, or plugin structure problem | Validate, clear the cache, restart, and reinstall |
| Runtime failure | Missing dependency, permission, or bad path | Install requirements, make scripts executable, and use forward slashes |

Video references: [00:03–00:38](https://www.youtube.com/watch?v=YBa1cwaG7is&t=3s)

For trigger testing, try several natural variants rather than one idealized prompt. For runtime
issues, keep dependency requirements in the skill documentation, apply `chmod +x` to executable
scripts, and use portable forward-slash paths even on Windows.

Official source: [Troubleshooting skills](https://anthropic.skilljar.com/introduction-to-agent-skills/434530)

## Practical checklist

Before sharing a skill:

1. Confirm that the task is repeated and task-specific.
2. Give the directory and frontmatter the same specific name.
3. Describe both what the skill does and when it should activate.
4. Keep only the essential workflow in `SKILL.md`.
5. Restrict tools only when the workflow needs that boundary.
6. Test several realistic trigger phrases and the actual result.
7. Run the validator and test from a restarted Claude Code session.
8. Choose Git, a plugin, or managed settings based on the intended audience.
