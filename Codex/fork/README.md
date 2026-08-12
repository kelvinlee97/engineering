# Forking Codex Chats in ChatGPT Desktop

Chinese version: [README_ZH.md](README_ZH.md)

This guide explains how to fork a local Codex chat in the ChatGPT desktop app. Forking preserves the conversation as a new branch so you can test a different direction without losing the original chat.

It covers the desktop composer, not the Codex CLI. Controls can vary by app version and account access; treat the commands shown after typing `/` as the source of truth for your current client.

## What `/fork` does

In the composer, `/fork` copies a local chat into either:

- a new local chat, for an independent reasoning or investigation branch; or
- a new Git worktree, when the branch may edit files and must not share the original working tree.

The new chat receives the preceding conversation context. It is a new conversation after the fork: later messages, conclusions, and changes in either branch do not automatically appear in the other one.

Forking a chat does not prove that every earlier conclusion was correct. Treat previous output as context, then ask the new branch to distinguish verified evidence from assumptions.

## The daily workflow

Use the current chat for routine work. Fork when Codex repeats the same failed route, needs an independent review, or you want to compare approaches.

1. Stop the unproductive run rather than allowing more retries on the same assumption.
2. In the chat composer, type `/fork` and select it from the command list.
3. Choose **new local chat** for analysis-only work. Choose **new worktree** if the fork might modify files and you need isolation.
4. In the new branch, use `/model` to select a stronger model when warranted, then use `/reasoning` to select the desired effort.
5. Send a reset prompt such as:

   ```text
   Do not continue the previous assumptions. List verified facts, failed evidence,
   and unverified assumptions. Propose mutually exclusive root causes and the
   smallest check for each. Do not modify files until new evidence supports a path.
   ```

6. Use `/status` to confirm the new chat's model, reasoning effort, context usage, and limits before relying on it.
7. Keep the branch whose evidence is stronger. Bring a short evidence-backed conclusion back to the original chat if you need to continue there.

## Plan mode and reasoning effort

`/plan` switches the chat into Plan mode; it does not itself prove the effective reasoning setting. In this local setup, `config.toml` requests `low` for default mode and `high` for Plan mode, but the desktop app can retain a per-chat choice.

After entering `/plan`, run `/status`. If the displayed effort is not `high`, run `/reasoning` and choose **high** manually. Use `xhigh` only for a genuinely high-risk or high-uncertainty decision, such as a production migration, data-loss risk, or a complex security review.

## When to fork, resume, or start fresh

| Situation | Best action |
| --- | --- |
| The current approach is still sound; you only need another task | Continue the current chat. |
| The chat is looping or needs an independent diagnosis | Fork to a new local chat. |
| You need a competing implementation that must not share edits | Fork to a new worktree. |
| The old discussion is irrelevant or misleading | Start a new chat and provide only current evidence. |

## Safe branch discipline

- Name the branch purpose in the first message: for example, "independent root-cause review" or "alternative implementation review."
- Ask for new checks rather than more explanation when the chat has stalled.
- Do not merge conclusions from two branches without checking their evidence and actual file state.
- A normal local-chat fork shares the same repository files. Use a worktree fork before allowing two branches to edit the same project independently.
- Never paste credentials, tokens, private keys, production data, or employer/client-confidential material into either branch.

## References

- [OpenAI: Slash commands](https://learn.chatgpt.com/docs/reference/slash-commands) documents `/fork`, `/model`, `/reasoning`, `/plan`, and `/status` for the ChatGPT desktop app.
- [OpenAI: Config basics](https://learn.chatgpt.com/docs/config-file/config-basic) documents user-level `~/.codex/config.toml` and configuration precedence.
