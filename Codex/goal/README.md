# Codex Goals: A Guide to the `/goal` Slash Command

Chinese version: [README_ZH.md](README_ZH.md)

`/goal` gives Codex one durable objective to keep working toward across turns, instead of stopping after a single normal turn. It is useful for work with a clear target, a validation loop, and enough room for Codex to make progress without you steering every step. When a goal is active, Codex can keep working for hours and stops when it is confident the stopping condition has been met.

This guide covers `/goal` in the Codex CLI and in the ChatGPT desktop app composer. Menus and feature availability can vary by Codex version, configuration, and account; the command list shown after typing `/` is the source of truth for your current client.

## What `/goal` does

- `/goal <objective>` sets a new goal.
- `/goal` shows the current goal.
- `/goal edit <objective>` revises it.
- `/goal pause`, `/goal resume`, and `/goal clear` control the run.

A goal attaches to the active chat. Objectives must be non-empty and at most 4,000 characters; for longer instructions, put the details in a file and point the goal at it, for example `PLAN.md`.

If `/goal` does not appear in the command list, enable the goals feature in `~/.codex/config.toml`:

```toml
[features]
goals = true
```

Alternatively run `codex features enable goals`, or simply ask Codex to enable it. On the machine where this guide was written, `codex features list` reports `goals` as stable and enabled.

## Choose work that fits a goal

A good goal is bigger than one prompt but smaller than an open-ended backlog. It states what Codex should achieve, what it must not change, how progress is validated, and when to stop.

Suitable:

- code migration with a clear target stack, parity checks, and constraints
- large refactor where tests run after each checkpoint
- deployment retry loop with a measurable health check
- experiments, prototypes, or games with a "builds and launches" definition of done
- prompt or eval optimization against a target score

Avoid loose lists of unrelated tasks, vague objectives with no verifiable end state, and work that needs frequent direction changes.

## Set up the loop

1. Name one objective and one stopping condition.
2. Point Codex at the files, docs, issue, logs, or plan it must read first.
3. Define the commands or artifacts that prove progress.
4. Ask for checkpoints with a short progress log.
5. Inspect status with `/goal`; pause, resume, or clear as needed.

Example prompts:

```text
/goal Migrate this project from [legacy stack] to [new stack]. Keep all
screens visually identical and verify the output with playwright interactive.
```

```text
/goal Implement PLAN.md. Add tests for each milestone and verify the output
with playwright interactive.
```

```text
/goal Optimize the prompts in [file or directory] until the eval suite
reaches [target score]. After each change, run [eval command], inspect the
failures, and stop when the target is met or the change would need product
or policy guidance.
```

```text
/goal Deploy the stack to staging and retry until the health check passes
and the smoke test succeeds.
```

## Daily workflow

- Keep routine bounded work in normal turns; use `/plan` first when a multi-step change needs a decided approach.
- Use `/goal` when the task will span many turns and has a clear stopping condition.
- During the run, ask for compact status updates: current checkpoint, what was verified, what remains, and whether Codex is blocked. If the status becomes vague, tighten the goal instead of adding one-off instructions.
- Treat an active goal as a background task: Codex keeps working until it believes the stopping condition is reached, then stops.
- Fork or start fresh when a chat is looping and the goal itself needs a new direction.

| Situation | Best action |
| --- | --- |
| Small bounded task | Normal turn. |
| Multi-step change needing an approach first | `/plan`, then normal turns. |
| Long-running work with a verifiable end state | `/goal <objective>`. |
| Chat looping on a failed assumption | `/fork` to a new chat. |

## Other ways to trigger a goal

The slash command is not the only entry point:

- Ask Codex directly in conversation to set a goal and start working; the official guide recommends this after a short planning conversation.
- Add a rule to the repository `AGENTS.md` (for example, "when the task matches X, set a goal and work until its stopping condition") so sessions in that repo can use goals automatically. This is a practice based on how `AGENTS.md` guides Codex, not an official goal-specific guarantee.
- Define a skill that decomposes work into goals, then invoke it via `AGENTS.md`, a scheduled-task prompt (`$skill-name`), or another agent.
- In the ChatGPT desktop app, a scheduled task can start a fresh run whose prompt asks for a goal; skills can also create scheduled tasks.

Scheduled-task and skill support are documented by OpenAI; their combination with goals follows from the same agent loop and was not separately documented at the time of writing.

## References

- [OpenAI: Follow a goal](https://developers.openai.com/codex/use-cases/follow-goals)
- [OpenAI: Developer commands](https://learn.chatgpt.com/docs/developer-commands)
- [OpenAI: Scheduled tasks](https://developers.openai.com/codex/app/automations)
