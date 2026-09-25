---
type: Concept
title: IAM policy evaluation
description: "How AWS decides a request: every applicable policy layer is checked, an explicit deny anywhere wins, and nothing is allowed without an explicit allow."
tags: [aws, security, identity]
sources:
  - id: aws-iam
    resource: https://github.com/kelvinlee97/engineering/blob/main/AWS/iam/README.md
    title: "AWS IAM - Runbook & Reference"
    author: human:kelvinlee97
    last_modified: 2026-09-24T14:48:10Z
  - id: aws-organizations
    resource: https://github.com/kelvinlee97/engineering/blob/main/AWS/organizations/README.md
    title: "AWS Organizations - Runbook & Reference"
    author: human:kelvinlee97
    last_modified: 2026-09-24T14:48:10Z
generated: { by: claude-code/wiki-v1, at: 2026-09-25T06:00:00Z }
status: draft
---

AWS evaluates every request against several independent policy layers. An explicit deny in any layer wins, and a request is denied unless an applicable layer explicitly allows it.[^aws-iam]

```mermaid
flowchart TD
    accTitle: IAM authorization decision
    accDescr: A request is checked against identity-based policies, resource-based policies, organization SCPs and RCPs, and any permissions boundary. An explicit deny in any layer denies it; otherwise it needs an explicit allow from the applicable layers.
    R[Request] --> L[Identity policy, resource policy, SCP/RCP, permissions boundary]
    L --> D{Explicit deny anywhere?}
    D -- Yes --> X[Denied]
    D -- No --> A{Explicit allow?}
    A -- Yes --> OK[Allowed]
    A -- No --> X
```

## Layers that only narrow

Two layers can only take permissions away. A permissions boundary caps what identity-based policies can grant.[^aws-iam] Organization SCPs and RCPs set cross-account boundaries and grant nothing by themselves; SCPs also do not apply to the management account, which is why an SCP can appear to have no effect.[^aws-iam][^aws-organizations]

## Debugging `AccessDenied`

Check each layer in turn: identity policy, resource policy, SCP or RCP, permissions boundary, and session policy. IAM is eventually consistent, so a just-made change may need time to propagate.[^aws-iam]

- [Least-privilege tool access](../claude-code/least-privilege-tool-access.md): the same layered model in agent tooling.

## Related

- Source: [AWS IAM - Runbook & Reference](../../sources/aws-iam.md)
- Source: [AWS Organizations - Runbook & Reference](../../sources/aws-organizations.md)

[^aws-iam]: AWS IAM - Runbook & Reference
[^aws-organizations]: AWS Organizations - Runbook & Reference
