---
type: Concept
title: Auto Mode
description: A Claude Code permission mode where low-risk actions run directly and a separate classifier reviews higher-risk ones against user intent and a configured trust boundary.
tags: [claude-code, auto-mode, security, permissions]
sources:
  - id: claude-auto-mode
    resource: https://github.com/kelvinlee97/engineering/blob/main/Claude/auto-mode/README.md
    title: How Claude Code Auto Mode Works
    author: human:kelvinlee97
    last_modified: 2026-09-24T14:48:10Z
generated: { by: claude-code/wiki-v1, at: 2026-09-24T15:50:00Z }
status: draft
---

Auto Mode lets low-risk work continue without prompts while a separate classifier checks higher-risk actions against what the user asked for, the configured rules, and the environment boundary. Claude does not approve its own actions.[^claude-auto-mode]

## Why it exists

Anthropic reports that about 97% of Claude Code permission prompts in its research were eventually approved. Approving every action gives control but causes approval fatigue and interrupts long multi-step tasks.[^claude-auto-mode]

## How an action is decided

```mermaid
flowchart TD
    accTitle: Auto Mode action review
    accDescr: Permission rules apply first, then the action's risk tier decides whether it runs directly or goes to the classifier, which approves it, rejects it so Claude seeks a safer path, or pauses for the user.
    C[Claude proposes an action] --> P[Apply deny, ask, allow rules]
    P --> R{Risk tier}
    R -->|Low risk or recoverable| E[Execute]
    R -->|Needs review| I[Classifier]
    I -->|Matches intent and boundary| E
    I -->|Safer path exists| S[Reject; Claude seeks an alternative]
    I -->|Cannot approve safely| H[Pause for the user]
```

The approximate order is: apply the `deny`, `ask`, and `allow` rules; determine the risk tier; send the action to the classifier if required; then execute, find a safer alternative, or pause.[^claude-auto-mode] Searching, reading files, and editing inside the project usually skip the classifier; shell commands, web fetches, access outside the environment, and destructive operations are more likely to reach it.[^claude-auto-mode]

The classifier sees the user's messages and Claude's proposed tool calls, but not Claude's reasoning, its replies, or tool output, which reduces the bias of one model being both executor and reviewer.[^claude-auto-mode] For example, deleting remote branches is denied when the user asked only for local cleanup; a denied force push to `main` may become a push to a new branch; repeated denials pause for the user.[^claude-auto-mode]

## Configuring the trust boundary

By default only the working directory and Git remotes count as internal. The `environment` field describes trusted resources (GitHub organizations, cloud accounts or buckets, internal services, staging) in plain English. Setting it replaces the built-in entries, so include the default string to keep them. Administrators can set organization-wide managed values that developers can add to but not remove.[^claude-auto-mode]

Classifier guidance comes as `allow`, `soft deny` (deny unless explicitly requested), and `hard deny` (deny even when requested). These guide the classifier and are not deterministic; hard enforcement stays with permission rules, covered on [Least-privilege tool access](least-privilege-tool-access.md).[^claude-auto-mode]

## What it is not

Not Claude approving itself, not removal of permission controls, not unconditional execution, not a replacement for production review, and not an absolute defense against [prompt injection](prompt-injection.md).[^claude-auto-mode]

## Rollout guidance from the source

Start narrow, define the real environment boundary, keep explicit `deny` and `ask` rules, watch what gets denied, widen gradually, keep human review for production infrastructure, and build evaluations for your own environment.[^claude-auto-mode] Actions the note says should keep explicit approval include `terraform apply`, production Kubernetes changes, cloud resource deletion, IAM changes, force-pushing protected branches, secrets, destructive SQL, and production DNS, TLS, or network-policy changes.[^claude-auto-mode]

## Related

- Source: [How Claude Code Auto Mode Works](../../sources/claude-auto-mode.md)

[^claude-auto-mode]: How Claude Code Auto Mode Works
