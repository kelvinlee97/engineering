# Claude Code GitHub Actions

> Claude Code GitHub Actions is a constrained agent inside a GitHub Actions job: an event starts it, identity checks decide whether it may run, and GitHub plus Claude tool permissions limit what it may do.

This article answers four practical questions:

1. How does a GitHub event become a Claude result?
2. When does the Action use interactive or automation mode?
3. Which permission layers determine its effective capability?
4. Where should human review and operational limits remain?

## Big picture

The complete path is event → actor verification → mode selection → constrained execution → output:

```mermaid
flowchart TD
    accTitle: Claude Code GitHub Actions execution path
    accDescr: A GitHub event starts a workflow. The Action verifies the actor, selects interactive or automation mode, runs Claude with granted tools and permissions, and produces a comment, commit, pull request, or workflow log.
    E[GitHub event] --> R[Workflow starts]
    R --> V{Actor allowed?}
    V -- No --> F[Run fails]
    V -- Yes --> M{prompt input?}
    M -- No --> I[Interactive mode<br/>look for @claude]
    M -- Yes --> A[Automation mode<br/>use predefined prompt]
    I --> C[Claude Code runs]
    A --> C
    C --> T[Use granted tools<br/>and repository permissions]
    T --> O[Comment, commit, PR,<br/>or workflow log]
```

The prompt controls the task, but it does not grant authority. The actor policy, workflow job permissions, credentials, Claude Code settings, and allowed tools remain separate controls.

## Source

- Official documentation: [Claude Code GitHub Actions](https://code.claude.com/docs/en/github-actions)
- Product: `anthropics/claude-code-action@v1`
- Reviewed: September 15, 2026
- Scope: setup, execution modes, permissions, authentication, common workflows, security, cost controls, and troubleshooting

This article is an original summary of the official documentation. The product is rolling software, so verify current inputs and examples before changing a production workflow.

## Where it fits

The Action is the workflow-file integration. It differs from automatic Claude Code Review, browser or mobile sessions, and custom automations built directly with the Claude Agent SDK.

Typical uses include turning an issue into a pull request, fixing a bug requested in a comment, answering implementation questions, reviewing code with a skill, and generating scheduled reports.

## Setup paths

Both setup paths require repository admin access.

```mermaid
flowchart TD
    accTitle: Claude Code GitHub Actions setup paths
    accDescr: Repository administrators can use quick setup on github.com through the install command, or manually install the GitHub App, authentication secret, and workflow file. Both paths end by testing an at-claude mention.
    S[Choose setup path] --> Q{Use Claude Code locally<br/>on github.com?}
    Q -- Yes --> X[Run /install-github-app]
    X --> X1[Install Claude GitHub App]
    X1 --> X2[Store API key or OAuth token<br/>as a repository secret]
    X2 --> X3[Claude creates workflow branch<br/>and prepares a pull request]
    Q -- No or need full control --> Y[Manual setup]
    Y --> Y1[Install GitHub App]
    Y1 --> Y2[Add authentication secret]
    Y2 --> Y3[Copy workflow into<br/>.github/workflows/]
    X3 --> Z[Test with @claude]
    Y3 --> Z
```

### Quick setup

Install and authenticate the GitHub CLI, start Claude Code in the target repository, then run `/install-github-app`. The command works only for repositories hosted on `github.com`. It installs the app, stores either `ANTHROPIC_API_KEY` or `CLAUDE_CODE_OAUTH_TOKEN` as a repository secret, and creates a branch containing the selected workflow files. Review and merge the prepared pull request before using `@claude`.

### Manual setup

Install the Claude GitHub App, add one authentication secret, and copy the official `examples/claude.yml` into `.github/workflows/`. Match the secret to the Action input:

| Authentication | GitHub secret | Action input | Best fit |
| --- | --- | --- | --- |
| Claude API | `ANTHROPIC_API_KEY` | `anthropic_api_key` | API billing and shared organisational automation |
| Claude subscription | `CLAUDE_CODE_OAUTH_TOKEN` | `claude_code_oauth_token` | Pro, Max, Team, or Enterprise subscription owned by the token creator |
| Workload identity federation | No long-lived API credential | Federation IDs plus `id-token: write` | Organisation deployments that can configure a Claude Console service account |
| Cloud provider | Provider-specific OIDC configuration | `use_bedrock`, `use_vertex`, or `use_foundry` | Inference routed through Amazon Bedrock, Google Cloud Agent Platform, or Microsoft Foundry |

For a multi-repository rollout, install the app at organisation level, scope it to the intended repositories, and use an organisation secret or reusable workflow. An individual's OAuth token is a poor shared credential because it remains tied to that person's subscription; use an API key or workload identity federation instead.

## Two execution modes

The presence of `prompt` selects the mode automatically; the old explicit `mode` input is not used in v1.

```mermaid
flowchart TD
    accTitle: Interactive and automation mode selection
    accDescr: When no prompt input exists, the Action waits for an at-claude trigger and replies in the issue or pull request. When a prompt exists, it runs automatically on the configured event and writes to the workflow log by default.
    W[Workflow configuration] --> P{prompt supplied?}
    P -- No --> I[Interactive mode]
    I --> I1[Wait for trigger phrase<br/>default: @claude]
    I1 --> I2[Respond in the issue or PR]
    P -- Yes --> A[Automation mode]
    A --> A1[Run prompt on configured event]
    A1 --> A2[Write to workflow log by default]
    A2 --> A3[Post a comment only when<br/>prompt and tools permit it]
```

Interactive requests can come from issue or pull-request comments, pull-request reviews, or the title or body of a newly opened issue. Automation mode supports events such as pull requests and schedules.

Before Claude starts, the Action checks the triggering actor:

1. For authored issue and pull-request events, the actor must have repository write access unless explicitly listed in `allowed_non_write_users` and a custom `github_token` is supplied.
2. Bots are rejected unless listed in `allowed_bots`, reducing the risk of automation loops. Scheduled events are also attributed to an actor, commonly the person who last edited the cron schedule.

## Permission and trust model

Three layers determine what a run can actually do:

```mermaid
flowchart TB
    accTitle: Effective permission model
    accDescr: Effective capability is the intersection of actor checks, GitHub job permissions, and the tools allowed through Claude Code arguments, settings, or skill frontmatter.
    A[Who may start the run?] --> B[Actor checks]
    B --> C[What may GitHub accept?]
    C --> D[job permissions<br/>contents, issues, pull requests]
    D --> E[What may Claude invoke?]
    E --> F[allowed tools, skill frontmatter,<br/>and Claude Code settings]
    F --> G[Effective capability<br/>intersection of all layers]
```

- GitHub workflow `permissions` constrain the job token.
- `--allowedTools` in `claude_args`, `permissions.allow` in `settings`, or a skill's `allowed-tools` frontmatter governs Claude's tool access.
- A plain-text automation prompt has no shell or GitHub API tools until the workflow grants them.
- Repository skills require `actions/checkout` so `.claude/skills/` exists on the runner. Plugin skills must be installed through `plugin_marketplaces` and `plugins` before invocation.

The official Claude GitHub App serves several Claude features, so its installation permission set is broader than this Action alone needs. The Action relies on read/write access to Contents, Issues, and Pull requests. Organisations that cannot accept the official app's full permission set can create a custom GitHub App limited to those areas, but that custom app does not replace the official app for Claude Code Review or web auto-fix.

## A minimal interactive workflow

The essential shape is:

```yaml
name: Claude Code
on:
  issue_comment:
    types: [created]
  pull_request_review_comment:
    types: [created]

jobs:
  claude:
    if: contains(github.event.comment.body, '@claude')
    runs-on: ubuntu-latest
    permissions:
      contents: write
      pull-requests: write
      issues: write
      id-token: write
      actions: read
    steps:
      - uses: actions/checkout@v6
        with:
          fetch-depth: 1
      - uses: anthropics/claude-code-action@v1
        with:
          anthropic_api_key: ${{ secrets.ANTHROPIC_API_KEY }}
```

`id-token: write` supports the Action's default GitHub App authentication. `actions: read` lets Claude inspect CI results. The job-level `if` avoids starting a runner for irrelevant comments; the Action still performs its own trigger check.

## Operational guidance

### Security

- Keep credentials in GitHub Secrets and never commit them.
- Grant only the workflow permissions and Claude tools required by the task.
- Treat issue text, comments, and changed repository content as untrusted input.
- Require human review and branch protection before merging generated changes.
- Pin third-party actions according to the organisation's supply-chain policy.
- Remember that deleting a GitHub secret does not revoke the underlying credential; revoke the API key or token at its issuer as well.

```mermaid
flowchart TD
    accTitle: Safe review boundary for generated changes
    accDescr: Untrusted repository input reaches a constrained Claude run, credentials come only from the secret store, and generated work remains on a branch or in review output until human review and required checks approve a merge.
    U[Untrusted issue, comment,<br/>or repository content] --> C[Claude run]
    S[Secret store] -->|credential reference| C
    P[Least-privilege job<br/>and tool policy] --> C
    C --> B[Feature branch or review output]
    B --> H[Human review + required checks]
    H -->|approved| M[Merge]
    H -->|rejected| R[Revise or close]
```

### Cost and reliability

Each run consumes GitHub Actions minutes and either API tokens or Claude subscription usage. Use specific requests, issue templates, a concise `CLAUDE.md`, `--max-turns`, workflow timeouts, and GitHub concurrency controls to bound work and reduce waste.

### Common failures

| Symptom | Check |
| --- | --- |
| No response to `@claude` | App installation, enabled workflows, authentication secret, exact trigger phrase, and actor write access |
| CI does not run after Claude pushes | Do not force the default `GITHUB_TOKEN` if app authentication is intended; ensure CI listens to the resulting `push` or `pull_request` event |
| Authentication fails | Validate the API key or OAuth token locally; for cloud providers, verify the provider-specific OIDC setup |
| Scheduled run fails actor checks | Ensure the user attributed to the schedule is human, or explicitly allow the bot actor |
| Fork PR cannot access a secret | GitHub withholds secrets from public-repository fork workflows; run trusted review workflows only where credentials are available safely |

## Migration notes for beta users

To migrate from `anthropics/claude-code-action@beta` to `@v1`:

1. Change the Action reference to `@v1`.
2. Remove `mode`; v1 detects the mode from `prompt`.
3. Rename `direct_prompt` to `prompt`.
4. Move options such as model and maximum turns into `claude_args`; convert `custom_instructions` to `--append-system-prompt`.

## Safety comes from the whole control chain

Claude Code GitHub Actions is best understood as a constrained agent inside an ordinary CI job. Safe adoption depends less on the prompt alone than on the complete control chain: trusted trigger, minimal GitHub permissions, explicit Claude tools, protected credentials, bounded runtime, and human review before merge.

## Further reading

- [Official Claude Code GitHub Actions documentation](https://code.claude.com/docs/en/github-actions)
- [Claude Code Action repository](https://github.com/anthropics/claude-code-action)
- [GitHub Actions secrets](https://docs.github.com/en/actions/security-for-github-actions/security-guides/using-secrets-in-github-actions)
