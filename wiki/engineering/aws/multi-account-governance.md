---
type: Pattern
title: AWS multi-account governance
description: Running many AWS accounts under AWS Organizations, with guardrails applied from the organization rather than per account.
tags:
- aws
- governance
aliases:
- engineering/aws/organizations
sources:
- id: aws-organizations
  resource: https://github.com/kelvinlee97/engineering/blob/main/AWS/organizations/README.md
  title: AWS Organizations - Runbook & Reference
  author: human:kelvinlee97
  last_modified: 2026-09-24T14:48:10Z
- id: aws-iam-identity-center
  resource: https://github.com/kelvinlee97/engineering/blob/main/AWS/iam-identity-center/README.md
  title: AWS IAM Identity Center - Runbook & Reference
  author: human:kelvinlee97
  last_modified: 2026-09-24T14:48:10Z
- id: aws-cloudtrail
  resource: https://github.com/kelvinlee97/engineering/blob/main/AWS/cloudtrail/README.md
  title: AWS CloudTrail - Runbook & Reference
  author: human:kelvinlee97
  last_modified: 2026-09-24T14:48:10Z
- id: aws-guardduty
  resource: https://github.com/kelvinlee97/engineering/blob/main/AWS/guardduty/README.md
  title: Amazon GuardDuty - Runbook & Reference
  author: human:kelvinlee97
  last_modified: 2026-09-24T14:48:10Z
- id: aws-security-hub
  resource: https://github.com/kelvinlee97/engineering/blob/main/AWS/security-hub/README.md
  title: AWS Security Hub CSPM - Runbook & Reference
  author: human:kelvinlee97
  last_modified: 2026-09-24T14:48:10Z
generated: { by: claude-code/wiki-v1, at: 2026-09-25T12:00:00Z }
status: draft
---
AWS recommends spreading workloads across many accounts, because an account is a natural boundary for security, cost, and blast radius. This page covers why and how to split accounts, and AWS Organizations, which groups them and applies guardrails from one place.

## Why many accounts

AWS recommends running workloads across many accounts: accounts are natural boundaries for security, cost, and blast radius. The legacy notes describe a consistent setup across five services.

| Concern | Setup |
| --- | --- |
| Structure | [Organizations](#aws-organizations) with OUs by environment; SCPs as deny lists; no workloads in the management account |
| Sign-in | [IAM Identity Center](iam.md#aws-iam-identity-center) in the management account, group-based assignments, external IdP with SCIM[^aws-iam-identity-center] |
| Audit | An organization [CloudTrail](security-monitoring.md#aws-cloudtrail) trail that member accounts cannot disable[^aws-cloudtrail] |
| Threat detection | [GuardDuty](security-monitoring.md#amazon-guardduty) in all accounts and Regions through a delegated administrator[^aws-guardduty] |
| Posture | [Security Hub CSPM](security-monitoring.md#aws-security-hub-cspm) through a delegated administrator with cross-Region aggregation[^aws-security-hub] |

The common thread is that security services are operated from a delegated administrator account rather than the management account.[^aws-organizations]

How those findings flow onward is covered under [the findings pipeline](security-monitoring.md#the-findings-pipeline).

## AWS Organizations

AWS Organizations manages multiple AWS accounts centrally: create or invite accounts, group them into organizational units (OUs), apply governance policies, share resources, and consolidate billing. It is a global service hosted in us-east-1.[^aws-organizations]

### The tree

One root holds OUs, OUs hold accounts (nesting up to 5 levels), and policies such as SCPs attach anywhere to narrow, never grant, what accounts beneath can do. The management account is not subject to SCPs.

| Policy type | Purpose |
| --- | --- |
| Service control policies (SCPs) | Permission boundaries for member accounts |
| Resource control policies (RCPs) | Prevent unintended external access to resources |
| Tag, backup, AI opt-out, chat applications policies | Other governance |

As listed in the note.[^aws-organizations]

### Practices

- Use many accounts as security, cost, and blast-radius boundaries; keep workloads out of the management account.
- Group accounts into OUs by environment and write SCPs as deny lists; IAM still grants permissions.
- Use delegated administrators (GuardDuty, Security Hub CSPM, Config, IAM Identity Center) instead of the management account, and an organization CloudTrail trail.[^aws-organizations]

### Troubleshooting and limits

| Symptom | Check |
| --- | --- |
| Account creation fails | Account quota and at most 5 creations in progress |
| SCP has no effect | SCPs grant nothing and skip the management account |
| Cannot remove an account | Created accounts must be at least 4 days old; invitations expire after 15 days |
| API errors elsewhere | Call Organizations from us-east-1 |

As tabled in the note. Default limits include 10 accounts (adjustable up to 50,000), 2,000 OUs, SCPs up to 10,240 characters, and 10 SCPs per entity.[^aws-organizations]

## Related
- [Management and governance](management-and-governance.md): Control Tower, Service Catalog, quotas, and resource sharing.
- [Compliance and posture](compliance-and-posture.md): Config, Inspector, Macie, Detective, and Artifact.
- [Domain index](index.md): other pages in this domain.

[^aws-organizations]: [AWS Organizations - Runbook & Reference](../../sources/aws-organizations.md), [original](https://github.com/kelvinlee97/engineering/blob/main/AWS/organizations/README.md)
[^aws-iam-identity-center]: [AWS IAM Identity Center - Runbook & Reference](../../sources/aws-iam-identity-center.md), [original](https://github.com/kelvinlee97/engineering/blob/main/AWS/iam-identity-center/README.md)
[^aws-cloudtrail]: [AWS CloudTrail - Runbook & Reference](../../sources/aws-cloudtrail.md), [original](https://github.com/kelvinlee97/engineering/blob/main/AWS/cloudtrail/README.md)
[^aws-guardduty]: [Amazon GuardDuty - Runbook & Reference](../../sources/aws-guardduty.md), [original](https://github.com/kelvinlee97/engineering/blob/main/AWS/guardduty/README.md)
[^aws-security-hub]: [AWS Security Hub CSPM - Runbook & Reference](../../sources/aws-security-hub.md), [original](https://github.com/kelvinlee97/engineering/blob/main/AWS/security-hub/README.md)
