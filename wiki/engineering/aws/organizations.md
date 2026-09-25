---
type: Service
title: AWS Organizations
description: AWS's service for managing many accounts as one tree of organizational units with shared billing and policy guardrails.
tags: [aws, governance, multi-account]
sources:
  - id: aws-organizations
    resource: https://github.com/kelvinlee97/engineering/blob/main/AWS/organizations/README.md
    title: "AWS Organizations - Runbook & Reference"
    author: human:kelvinlee97
    last_modified: 2026-09-24T14:48:10Z
generated: { by: claude-code/wiki-v1, at: 2026-09-25T06:00:00Z }
status: draft
---

AWS Organizations manages multiple AWS accounts centrally: create or invite accounts, group them into organizational units (OUs), apply governance policies, share resources, and consolidate billing. It is a global service hosted in us-east-1.[^aws-organizations]

## The tree

One root holds OUs, OUs hold accounts (nesting up to 5 levels), and policies such as SCPs attach anywhere to narrow, never grant, what accounts beneath can do. The management account is not subject to SCPs.[^aws-organizations]

| Policy type | Purpose |
| --- | --- |
| Service control policies (SCPs) | Permission boundaries for member accounts |
| Resource control policies (RCPs) | Prevent unintended external access to resources |
| Tag, backup, AI opt-out, chat applications policies | Other governance |

As listed in the note.[^aws-organizations]

## Practices

- Use many accounts as security, cost, and blast-radius boundaries; keep workloads out of the management account.[^aws-organizations]
- Group accounts into OUs by environment and write SCPs as deny lists; IAM still grants permissions.[^aws-organizations]
- Use delegated administrators (GuardDuty, Security Hub CSPM, Config, IAM Identity Center) instead of the management account, and an organization CloudTrail trail.[^aws-organizations]

## Troubleshooting and limits

| Symptom | Check |
| --- | --- |
| Account creation fails | Account quota and at most 5 creations in progress |
| SCP has no effect | SCPs grant nothing and skip the management account |
| Cannot remove an account | Created accounts must be at least 4 days old; invitations expire after 15 days |
| API errors elsewhere | Call Organizations from us-east-1 |

As tabled in the note.[^aws-organizations] Default limits include 10 accounts (adjustable up to 50,000), 2,000 OUs, SCPs up to 10,240 characters, and 10 SCPs per entity.[^aws-organizations]

## Related

- Source: [AWS Organizations - Runbook & Reference](../../sources/aws-organizations.md)

[^aws-organizations]: AWS Organizations - Runbook & Reference
