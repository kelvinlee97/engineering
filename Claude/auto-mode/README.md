# How Claude Code Auto Mode Works

English | [简体中文](README_ZH.md)

## Source

- Video: [How auto mode works with Claude Code](https://www.youtube.com/watch?v=b8SV4U6fEIc)
- Publisher: Claude
- Published: August 4, 2026
- Duration: 5:41
- Source coverage: Complete YouTube auto-generated English transcript

This guide is an original summary of the video, not a transcript or a replacement for the official documentation.

## Summary

Claude Code Auto Mode does not allow Claude to approve its own actions. It uses a separate classifier to check whether higher-risk actions match the user's intent, reducing repetitive permission prompts while preserving safety controls.

## Why Auto Mode exists

Anthropic reports that approximately 97% of Claude Code permission prompts in its research were eventually approved by users. Approving every action provides control, but it can also cause approval fatigue and interrupt long-running, multi-step tasks.

Auto Mode is designed to:

- Continue low-risk and recoverable work
- Review potentially destructive or out-of-scope actions
- Reduce unnecessary manual approvals
- Return control to the user when an action cannot be approved safely

Video reference: [00:00–00:43](https://www.youtube.com/watch?v=b8SV4U6fEIc&t=0s)

## How actions are reviewed

### Claude does not review itself

When Claude proposes a tool call, the action is reviewed by a separate classifier instead of Claude approving its own work.

The classifier can see:

- The user's messages
- Claude's proposed tool calls

It cannot see:

- Claude's internal reasoning
- Claude's responses to the user
- Tool output

This separation reduces the bias that would result from Claude acting as both the executor and reviewer.

Video reference: [00:49–01:31](https://www.youtube.com/watch?v=b8SV4U6fEIc&t=49s)

### Actions are compared with user intent

The classifier checks whether Claude is going beyond the requested scope, attempting an irreversible or destructive operation, or reaching outside the configured trust boundary.

For example, deleting remote Git branches should be denied when the user requested only local cleanup. After a denial, Claude will usually look for a safer alternative. If a force push to `main` is denied, it might push to a new branch instead. If actions continue to be denied, Auto Mode pauses and asks the user to decide.

Video reference: [01:31–02:03](https://www.youtube.com/watch?v=b8SV4U6fEIc&t=91s)

### Prompt-injection protection

Web pages, source files, and other tool results may contain hidden instructions intended to redirect Claude away from the user's original request. The video describes two layers of protection:

1. A server-side probe scans tool results and flags suspicious instructions.
2. The classifier checks whether Claude's next action still matches the user's intent.

An attack must pass both layers before it can influence subsequent actions. Anthropic reports that prompt-injection attack success fell to zero in its evaluations when both the probe and Auto Mode were enabled.

This is an Anthropic-reported internal evaluation result, not a guarantee for every real-world environment.

Video reference: [02:03–02:46](https://www.youtube.com/watch?v=b8SV4U6fEIc&t=123s)

## Which actions reach the classifier

The approximate evaluation order is:

1. Apply `deny`, `ask`, and `allow` permission rules.
2. Determine the action's risk tier.
3. Send the action to the classifier when required.
4. Execute it, find a safer alternative, or pause for the user.

Actions that can usually skip the classifier include:

- Searching a codebase
- Reading files
- Editing files inside the project
- Other read-only or recoverable actions

Actions more likely to require classifier review include:

- Shell commands
- Web fetches
- Access to resources outside the current environment
- Destructive or difficult-to-reverse operations

Video reference: [02:46–03:20](https://www.youtube.com/watch?v=b8SV4U6fEIc&t=166s)

## Configuring the trust boundary

By default, Auto Mode considers only the current working directory and Git remotes internal. Company-owned cloud buckets, internal services, and other infrastructure may still be treated as external.

Use the `environment` field to describe trusted resources in plain English, such as:

- GitHub organizations
- AWS accounts or cloud buckets
- Internal services
- Development and staging infrastructure

Administrators can define organization-wide managed settings. Developers may add user-level entries but cannot remove administrator-defined settings.

Setting `environment` replaces Claude's built-in entries. Include the default environment string if those entries should remain available.

Video reference: [03:20–04:10](https://www.youtube.com/watch?v=b8SV4U6fEIc&t=200s)

## Guidance and enforced rules

Classifier guidance includes:

- `allow`: actions that are generally acceptable
- `soft deny`: actions that should be denied unless explicitly requested
- `hard deny`: actions that should be denied even when requested

These fields guide the classifier; they are not deterministic enforcement rules.

For hard enforcement, use Claude Code permission rules:

- `deny`: block matching tool calls
- `ask`: require user confirmation even in Auto Mode
- `allow`: permit matching actions

Broad rules that enable arbitrary code execution may still be reviewed by the classifier.

Video reference: [04:10–04:48](https://www.youtube.com/watch?v=b8SV4U6fEIc&t=250s)

## What Auto Mode is not

Auto Mode is not:

- Claude approving its own actions
- A complete removal of permission controls
- Unconditional execution of every action
- A replacement for production review
- An absolute defense against prompt injection

## Practical DevOps guidance

Reasonable initial Auto Mode use cases:

- Editing Terraform on a feature branch
- Reading Kubernetes manifests
- Analyzing CI logs
- Updating project documentation
- Running local tests and linters
- Creating a remediation branch

Actions that should normally retain explicit approval:

- `terraform apply`
- Production Kubernetes mutations
- Cloud resource deletion
- IAM permission changes
- Force-pushing protected branches
- Operations involving secrets
- Database migrations or destructive SQL
- Production DNS, TLS, or network-policy changes

## Recommended rollout

1. Start with a narrow scope.
2. Define the real environment boundary.
3. Keep explicit `deny` and `ask` rules.
4. Observe which actions are denied.
5. Expand the scope gradually.
6. Retain human review for production infrastructure.
7. Build evaluations for your own environment.

Video reference: [05:13–05:32](https://www.youtube.com/watch?v=b8SV4U6fEIc&t=313s)

## Key takeaway

Auto Mode does not remove safety review. It moves review from every individual tool call to the level of user intent and operational risk.

Its main mechanisms are:

1. A separate classifier
2. Action risk tiers
3. A prompt-injection probe
4. A configurable environment trust boundary

## Further reading

- [Anthropic engineering announcement](https://www.anthropic.com/engineering/claude-code-auto-mode)
- [Claude Code Auto Mode configuration](https://code.claude.com/docs/en/auto-mode-config)
