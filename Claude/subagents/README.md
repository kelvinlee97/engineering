# Introduction to Claude Code Subagents

Chinese version: [README_ZH.md](README_ZH.md)

This is a complete study guide to Anthropic Academy's **Introduction to subagents** course. It covers all four lessons and the accessible subtitles from their official videos. It is an original summary, not a transcript or a replacement for the course.

## Source coverage

| Lesson | Official article | Official video | Coverage status |
| --- | --- | --- | --- |
| [What are subagents?](https://anthropic.skilljar.com/introduction-to-subagents/450698) | Read in full | [Video](https://www.youtube.com/watch?v=jKErNxuxPXg), English auto-generated subtitles read in full | Complete |
| [Creating a subagent](https://anthropic.skilljar.com/introduction-to-subagents/450699) | Read in full | [Embedded video](https://www.youtube.com/watch?v=arD6qEWa2Xc) is currently unavailable because of a copyright claim | Article complete; video unavailable |
| [Designing effective subagents](https://anthropic.skilljar.com/introduction-to-subagents/450700) | Read in full | [Video](https://www.youtube.com/watch?v=WPxWKT_OaU4), English auto-generated subtitles read in full | Complete |
| [Using subagents effectively](https://anthropic.skilljar.com/introduction-to-subagents/450701) | Read in full | [Video](https://www.youtube.com/watch?v=n5LoKZ8Oa-A), English auto-generated subtitles read in full | Complete |

The second lesson's embedded player and direct YouTube URL both report that the video was blocked because of claimed content by Lynda. No transcript or timestamps have been invented for it. Its written lesson is comprehensive and is summarized below.

## The course in one mental model

> A subagent is useful when a focused worker can do substantial intermediate work in isolation and return a small, well-defined result that the main conversation can verify and use.

The four lessons form one sequence:

1. **Understand isolation:** the subagent works in a separate context and returns a summary.
2. **Create deliberately:** define its scope, description, tools, model, and system prompt.
3. **Design for completion:** specify inputs, output format, obstacle reporting, and minimum tool access.
4. **Delegate selectively:** use subagents when the result matters more than the intermediate journey.

## Lesson 1 — What are subagents?

### Definition and lifecycle

A subagent is a specialized assistant to which Claude Code delegates a task. It runs in a separate conversation context, completes the task, returns a focused summary to the parent, and then its conversation is discarded.

It receives two inputs:

1. A custom system prompt from its configuration file, defining its role and behavior.
2. A task description written by the parent agent from the user's request.

Its file reads, searches, edits, and tool results remain in the isolated context. The main conversation keeps the original request and the returned summary rather than the whole investigative trail.

Video references: [00:03–00:24](https://www.youtube.com/watch?v=jKErNxuxPXg&t=3s), [00:40–01:12](https://www.youtube.com/watch?v=jKErNxuxPXg&t=40s)

### Why isolation matters

Every exchange and tool result consumes the main context window. A large investigation can fill that finite space with material that is no longer useful. A subagent protects the main context by moving the noisy exploration elsewhere.

The tradeoff is equally important: the parent loses visibility into how the subagent reached its conclusion and what it discovered but omitted from the summary.

Video references: [00:24–00:40](https://www.youtube.com/watch?v=jKErNxuxPXg&t=24s), [01:52–02:02](https://www.youtube.com/watch?v=jKErNxuxPXg&t=112s)

### Course example

To identify which service handles refunds in an unfamiliar codebase, Claude might read around 15 files, run searches, and trace function calls. Without a subagent, all of that lands in the main context even though the desired output is one fact. With an Explore subagent, the investigation stays isolated and only the focused answer returns.

Video reference: [01:13–01:52](https://www.youtube.com/watch?v=jKErNxuxPXg&t=73s)

### Built-in subagents

| Subagent | Purpose in the course |
| --- | --- |
| General purpose | Multi-step tasks requiring both exploration and action |
| Explore | Fast searching and navigation of codebases |
| Plan | Codebase research and analysis during plan mode |

Claude Code also supports custom subagents with their own system prompts and tool access.

Video reference: [02:01–02:30](https://www.youtube.com/watch?v=jKErNxuxPXg&t=121s)

## Lesson 2 — Creating a subagent

### Creation flow

The course recommends creating a custom subagent through the `/agents` command:

1. Run `/agents` and select **Create new agent**.
2. Choose a scope:
   - **Project-level:** available only in the current project.
   - **User-level:** available across projects on the machine.
3. Choose manual configuration or describe the desired behavior and let Claude generate the initial name, description, and system prompt. The course recommends generation as the easier starting point.
4. Select the tools, model, and UI color.
5. Save the generated Markdown configuration.
6. Test the subagent against a representative task and refine its description if delegation does not trigger as expected.

Official source: [Creating a subagent](https://anthropic.skilljar.com/introduction-to-subagents/450699)

### Tool selection

The creation interface groups tools into read-only, edit, execution, MCP, and other tools. Selection should follow the task:

- A reviewer normally needs to read and analyze code, not edit it.
- Execution access can still be useful to inspect pending changes.
- Edit and write access should be reserved for subagents whose job requires modification.

This is the first appearance of the course's least-privilege principle: start from what the subagent must do, then grant only the tools required for that job.

### Model and color

The course's model picker describes four choices:

| Choice | Course guidance |
| --- | --- |
| Haiku | Fast, lightweight tasks |
| Sonnet | Middle ground between speed and depth |
| Opus | Complex analysis |
| Inherit | Use the model running in the main conversation |

The selected color is a UI cue that helps identify which subagent is active.

### Configuration file

Project-level subagents are typically stored at:

```text
.claude/agents/your-agent-name.md
```

A minimal configuration has YAML frontmatter followed by the system prompt:

```markdown
---
name: code-quality-reviewer
description: Review specified code changes for quality and risk.
tools: Bash, Glob, Grep, Read
model: sonnet
color: purple
---

Review only the files named in the delegated task. Report findings by
severity and include enough evidence for the parent agent to verify them.
```

| Field | Role |
| --- | --- |
| `name` | Unique identifier; the subagent can also be referenced with `@agent <name>` |
| `description` | Tells Claude when to delegate and helps shape the delegated input prompt |
| `tools` | Defines the tools available to the subagent |
| `model` | Selects `sonnet`, `opus`, `haiku`, or `inherit` in the course example |
| `color` | Identifies the active subagent in the UI |
| Markdown body | The system prompt defining focus, method, and reporting behavior |

The description must be one line; escaped `\n` characters can represent breaks. Concrete trigger examples help Claude recognize appropriate delegation scenarios.

### Automatic use and testing

The course suggests including **“proactively”** in the description when the subagent should be considered automatically. Examples in the description can make the trigger conditions more concrete.

After creation, test the agent on realistic changes. If Claude does not use it when expected, improve the description with more specific triggers and examples rather than assuming the system prompt alone controls selection.

## Lesson 3 — Designing effective subagents

The course identifies four characteristics of an effective subagent:

1. Specific descriptions.
2. Structured output.
3. Obstacle reporting.
4. Limited tool access.

Video overview: [00:03–00:10](https://www.youtube.com/watch?v=WPxWKT_OaU4&t=3s), [03:27–03:37](https://www.youtube.com/watch?v=WPxWKT_OaU4&t=207s)

### Descriptions have two jobs

The name and description of every available subagent are included in the main agent's system prompt. The parent uses them to decide which subagent to launch and when.

The description also guides the input prompt written by the parent. A vague reviewer description may produce a vague instruction such as “find the current changes.” A stronger description can require the parent to name the exact files. Similarly, requiring citable sources in a research subagent's description carries that requirement into the delegated prompt.

Video references: [00:17–00:49](https://www.youtube.com/watch?v=WPxWKT_OaU4&t=17s), [00:49–01:39](https://www.youtube.com/watch?v=WPxWKT_OaU4&t=49s)

### Define the output before the work starts

The course calls a defined output format the most important improvement. It gives the subagent a checklist and a natural stopping condition. Without one, a research subagent may not know when it has learned enough and can run much longer than needed.

A code review output could require:

1. Summary.
2. Critical issues.
3. Major issues.
4. Minor issues.
5. Recommendations.
6. Approval status.
7. Obstacles encountered.

The exact headings depend on the task; the invariant is that “done” is observable.

Video reference: [01:41–02:03](https://www.youtube.com/watch?v=WPxWKT_OaU4&t=101s)

### Make obstacles part of the result

If a subagent discovers a workaround, unusual setup, required flag, or problematic dependency but omits it from the summary, the main thread must rediscover that information. The output format should explicitly request obstacles such as:

- setup issues and environment quirks;
- workarounds discovered during the task;
- commands requiring special flags or configuration;
- dependencies or imports that caused problems.

Video reference: [02:04–02:42](https://www.youtube.com/watch?v=WPxWKT_OaU4&t=124s)

### Limit tools by role

| Subagent role | Course-recommended access |
| --- | --- |
| Research/read-only | `Glob`, `Grep`, `Read` |
| Code reviewer | Read tools plus `Bash` for commands such as `git diff`; no edit/write |
| Styling or code modification | Add edit/write because modification is the job |

Minimum access reduces unintended side effects and makes the responsibility of each subagent clearer.

Video reference: [02:42–03:26](https://www.youtube.com/watch?v=WPxWKT_OaU4&t=162s)

## Lesson 4 — Using subagents effectively

### The decision rule

Ask one question:

> **Does the intermediate work matter to the main thread?**

- If only the final result matters, delegation is a good candidate.
- If the main thread must see, preserve, or react to intermediate discoveries, keep the work in the main thread.

Subagents work best when exploration can be separated from execution. Dependent steps lose information when compressed through repeated handoffs.

Video references: [00:03–00:32](https://www.youtube.com/watch?v=n5LoKZ8Oa-A&t=3s), [04:33–04:41](https://www.youtube.com/watch?v=n5LoKZ8Oa-A&t=273s)

### Strong use cases

#### Research and exploration

A research subagent can search many files and code paths while returning only the location and explanation the parent needs. The course uses locating JWT validation in an unfamiliar codebase as its example.

Video reference: [00:32–01:17](https://www.youtube.com/watch?v=n5LoKZ8Oa-A&t=32s)

#### Code review with fresh context

Claude may review work less critically when the same main conversation helped create it over many turns. A reviewer subagent starts without that creation history, runs `git diff`, reads the modified files, and applies specialized review criteria. Its system prompt can also encode project-specific standards for consistent reviews.

Video reference: [01:15–02:01](https://www.youtube.com/watch?v=n5LoKZ8Oa-A&t=75s)

#### Tasks that genuinely need another system prompt

- A copywriting subagent can use instructions about audience, tone, voice, and structure rather than Claude Code's concise technical defaults.
- A styling subagent can load design-system files into its context so it knows the project's colors, spacing, and component conventions before writing CSS.

Video reference: [01:59–03:00](https://www.youtube.com/watch?v=n5LoKZ8Oa-A&t=119s)

### Anti-patterns

#### Empty expert personas

Labels such as “Python expert” or “Kubernetes specialist” do not add capability by themselves because the main Claude conversation already has that knowledge. Isolation is worthwhile only when the subagent provides a real difference, such as a custom system prompt, focused context, or controlled tools.

Video reference: [02:57–03:27](https://www.youtube.com/watch?v=n5LoKZ8Oa-A&t=177s)

#### Sequential pipelines with dependent steps

A reproduce → debug → fix pipeline loses information when each agent depends on discoveries from the previous one. Pipelines are suitable only when the tasks are genuinely independent; otherwise the work belongs in one context.

Video reference: [03:27–03:46](https://www.youtube.com/watch?v=n5LoKZ8Oa-A&t=207s)

#### Test-runner subagents

Test failures often require full output. A subagent that compresses this to “tests failed” hides the evidence needed for diagnosis and creates extra work to recover it. The course reports that the test-runner pattern performed worse among the configurations tested.

Video reference: [03:46–04:09](https://www.youtube.com/watch?v=n5LoKZ8Oa-A&t=226s)

## End-to-end design checklist

Before creating or using a subagent, answer these questions:

### Delegation

- Is the work focused enough to describe as one task?
- Does the main thread need the intermediate work or only the result?
- Are dependent steps staying in the same context?

### Configuration

- Is the scope project-level or user-level?
- Does the name and one-line description explain when to delegate?
- Does the description help the parent write a precise task prompt?
- Is the model appropriate for the task's speed and depth?

### Safety and completion

- Are tools limited to the minimum required?
- Does the output format make completion observable?
- Must the subagent report evidence, sources, files, or line numbers?
- Is there an explicit section for obstacles and workarounds?

### Verification

- Can the parent verify the returned summary?
- Has the subagent been tested with a representative task?
- If delegation did not trigger, was the description improved with concrete examples?

## Knowledge check

Answer without rereading the guide:

1. What two inputs does a subagent receive?
2. What happens to the subagent's conversation after it returns a summary?
3. What is gained and lost through context isolation?
4. What is the difference between project-level and user-level scope?
5. Which configuration field controls both selection and the parent's delegated prompt?
6. Why does a structured output make a subagent finish more reliably?
7. Which obstacles should be returned to the main thread?
8. What tools should a read-only researcher, reviewer, and modifier receive?
9. Why can a reviewer subagent give a fresher review?
10. Why is an “expert” label alone not a useful subagent?
11. Why are dependent sequential pipelines risky?
12. What single question should decide whether to delegate?

## Practice exercise

Design a **repository authentication researcher** subagent.

Produce:

1. A one-line `description` that tells the parent when to use it and requires exact target questions.
2. A minimum `tools` list.
3. A system prompt that limits the task to research.
4. An output format containing conclusion, evidence, relevant files and line numbers, uncertainty, and obstacles encountered.
5. One example that should trigger the subagent and one that should remain in the main thread.
6. A verification step the parent can perform on the returned summary.

Your final justification must apply the course's decision rule: explain whether the intermediate work matters.

## Sources

### Official course articles

- [What are subagents?](https://anthropic.skilljar.com/introduction-to-subagents/450698)
- [Creating a subagent](https://anthropic.skilljar.com/introduction-to-subagents/450699)
- [Designing effective subagents](https://anthropic.skilljar.com/introduction-to-subagents/450700)
- [Using subagents effectively](https://anthropic.skilljar.com/introduction-to-subagents/450701)

All articles were read through an enrolled Anthropic Academy session on 2026-08-05.

### Official course videos

- [What are subagents?](https://www.youtube.com/watch?v=jKErNxuxPXg) — English auto-generated subtitles read on 2026-08-05.
- [Creating a subagent](https://www.youtube.com/watch?v=arD6qEWa2Xc) — unavailable on 2026-08-05 because of a copyright claim; no transcript was used.
- [Designing effective subagents](https://www.youtube.com/watch?v=WPxWKT_OaU4) — English auto-generated subtitles read on 2026-08-05.
- [Using subagents effectively](https://www.youtube.com/watch?v=n5LoKZ8Oa-A) — English auto-generated subtitles read on 2026-08-05.

