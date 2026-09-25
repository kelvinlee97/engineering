---
type: Pattern
title: AWS multi-account governance
description: Run AWS as many accounts under Organizations, with central sign-in, an organization audit trail, and security services run from delegated administrator accounts.
tags: [aws, governance, multi-account, security]
sources:
  - id: aws-organizations
    resource: https://github.com/kelvinlee97/engineering/blob/main/AWS/organizations/README.md
    title: "AWS Organizations - Runbook & Reference"
    author: human:kelvinlee97
    last_modified: 2026-09-24T14:48:10Z
  - id: aws-iam-identity-center
    resource: https://github.com/kelvinlee97/engineering/blob/main/AWS/iam-identity-center/README.md
    title: "AWS IAM Identity Center - Runbook & Reference"
    author: human:kelvinlee97
    last_modified: 2026-09-24T14:48:10Z
  - id: aws-cloudtrail
    resource: https://github.com/kelvinlee97/engineering/blob/main/AWS/cloudtrail/README.md
    title: "AWS CloudTrail - Runbook & Reference"
    author: human:kelvinlee97
    last_modified: 2026-09-24T14:48:10Z
  - id: aws-guardduty
    resource: https://github.com/kelvinlee97/engineering/blob/main/AWS/guardduty/README.md
    title: "Amazon GuardDuty - Runbook & Reference"
    author: human:kelvinlee97
    last_modified: 2026-09-24T14:48:10Z
  - id: aws-security-hub
    resource: https://github.com/kelvinlee97/engineering/blob/main/AWS/security-hub/README.md
    title: "AWS Security Hub CSPM - Runbook & Reference"
    author: human:kelvinlee97
    last_modified: 2026-09-24T14:48:10Z
generated: { by: claude-code/wiki-v1, at: 2026-09-25T06:00:00Z }
status: draft
---

AWS recommends running workloads across many accounts: accounts are natural boundaries for security, cost, and blast radius.[^aws-organizations] The legacy notes describe a consistent setup across five services.

| Concern | Setup |
| --- | --- |
| Structure | [Organizations](organizations.md) with OUs by environment; SCPs as deny lists; no workloads in the management account[^aws-organizations] |
| Sign-in | [IAM Identity Center](iam-identity-center.md) in the management account, group-based assignments, external IdP with SCIM[^aws-iam-identity-center] |
| Audit | An organization [CloudTrail](cloudtrail.md) trail that member accounts cannot disable[^aws-cloudtrail] |
| Threat detection | [GuardDuty](guardduty.md) in all accounts and Regions through a delegated administrator[^aws-guardduty] |
| Posture | [Security Hub CSPM](security-hub.md) through a delegated administrator with cross-Region aggregation[^aws-security-hub] |

The common thread is that security services are operated from a delegated administrator account rather than the management account.[^aws-organizations]

- [Security findings pipeline](security-findings-pipeline.md)

## Related

- Source: [AWS Organizations - Runbook & Reference](../../sources/aws-organizations.md)
- Source: [AWS IAM Identity Center - Runbook & Reference](../../sources/aws-iam-identity-center.md)
- Source: [AWS CloudTrail - Runbook & Reference](../../sources/aws-cloudtrail.md)
- Source: [Amazon GuardDuty - Runbook & Reference](../../sources/aws-guardduty.md)
- Source: [AWS Security Hub CSPM - Runbook & Reference](../../sources/aws-security-hub.md)

[^aws-organizations]: AWS Organizations - Runbook & Reference
[^aws-iam-identity-center]: AWS IAM Identity Center - Runbook & Reference
[^aws-cloudtrail]: AWS CloudTrail - Runbook & Reference
[^aws-guardduty]: Amazon GuardDuty - Runbook & Reference
[^aws-security-hub]: AWS Security Hub CSPM - Runbook & Reference
