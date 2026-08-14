# Codex CLI Slash Commands: A Quick Guide

Chinese version: [README_ZH.md](README_ZH.md)

Codex CLI is an interactive coding assistant in your terminal. Slash commands
control the current chat: they help you inspect its state, plan work, review
changes, and manage saved sessions. They are not shell commands and do not
replace normal Git review or repository instructions.

Your installed `/` menu is the source of truth. Available commands can vary by
Codex version, configuration, operating system, and account.

## Start here

Run `codex` from the repository you want to work on, then use a short,
bounded prompt. A practical first loop is:

```text
/status
/mention AGENTS.md
/plan Update the documentation only. Preserve unrelated changes and run the
relevant checks before reporting the result.
```

- `/status` shows the active model, approval policy, writable roots, and context use.
- `/mention path/to/file` adds an important file to the current chat for later requests to reference.
- `/plan` helps decide a multi-step task before editing. It is unavailable while Codex is working.

## Commands you will use most

| Command | What it does |
| --- | --- |
| `/permissions` | Choose what Codex may do without asking first. Select the least authority needed, then use `/status` to confirm it. |
| `/diff` | Show staged, unstaged, and untracked changes before a checkpoint or commit. |
| `/review` | Review the working tree for issues and missing tests. Treat it as an extra check, not proof of correctness. |
| `/compact` | Summarize a long chat to free context while retaining key decisions. |
| `/side` | Open a temporary focused investigation without leaving the parent chat. Use it for read-only questions. |
| `/fork` | Create a new chat from the current one to explore a durable alternative approach. |
| `/resume` | Reopen a saved active chat from the session picker. |
| `/rename` | Give the current chat a recognizable name. |
| `/archive` | Archive the current chat and exit Codex. Restore it later with `codex unarchive <SESSION>`. |
| `/exit` | Leave the CLI without archiving the current chat. |

## A safe everyday workflow

1. Run `/status`, then attach relevant instructions with `/mention`.
2. For a non-trivial change, use `/plan` and state the scope, checks, and what must not change.
3. Ask Codex to make the bounded change.
4. Inspect `/diff`, run the repository's relevant checks, then use `/review`.
5. Save or commit only the intended files through normal Git commands.

For read-only review, select `Read Only` in `/permissions`. For any edit,
preserve unrelated working-tree changes and check the target paths before
approving an action. Do not put `/delete`, `/logout`, or other state-changing
commands in unattended workflows.

## References

- [OpenAI: Developer commands](https://learn.chatgpt.com/docs/developer-commands?surface=cli)
- [OpenAI: Codex CLI overview](https://developers.openai.com/codex/cli)
- [Forking Codex chats in ChatGPT Desktop](../fork/README.md)
