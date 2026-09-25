---
type: Pattern
title: AWS security findings pipeline
description: Route GuardDuty and other detector findings through Security Hub CSPM and EventBridge, and export them, because each service keeps only a short fixed history.
tags: [aws, security, monitoring]
sources:
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
  - id: aws-cloudtrail
    resource: https://github.com/kelvinlee97/engineering/blob/main/AWS/cloudtrail/README.md
    title: "AWS CloudTrail - Runbook & Reference"
    author: human:kelvinlee97
    last_modified: 2026-09-24T14:48:10Z
generated: { by: claude-code/wiki-v1, at: 2026-09-25T06:00:00Z }
status: draft
---

AWS's detective services each produce findings, but none keeps them long. The notes describe the same pipeline: detect, aggregate, route, and export.

```mermaid
flowchart LR
    accTitle: AWS security findings pipeline
    accDescr: GuardDuty and other services send findings to Security Hub CSPM for aggregation; findings go to EventBridge for automated response and are exported to S3 for long-term retention.
    G[GuardDuty, Inspector, Macie] --> H[Security Hub CSPM]
    H --> E[EventBridge: response automation]
    E --> S[S3: long-term retention]
```

## Retention is short everywhere

| Service | Built-in retention |
| --- | --- |
| GuardDuty findings | 90 days, fixed[^aws-guardduty] |
| Security Hub CSPM findings | 90 days[^aws-security-hub] |
| CloudTrail event history | 90 days, cannot be extended[^aws-cloudtrail] |

So every note recommends exporting: GuardDuty findings to S3, Security Hub findings archived through EventBridge, and CloudTrail events to a trail or Lake event data store.[^aws-guardduty][^aws-security-hub][^aws-cloudtrail]

## Wiring rules

- A service's findings reach Security Hub only if that service and its integration are enabled in the same Region.[^aws-security-hub]
- Filters and suppression rules hide findings; they do not fix causes.[^aws-guardduty]

- [AWS multi-account governance](multi-account-governance.md)

## Related

- Source: [Amazon GuardDuty - Runbook & Reference](../../sources/aws-guardduty.md)
- Source: [AWS Security Hub CSPM - Runbook & Reference](../../sources/aws-security-hub.md)
- Source: [AWS CloudTrail - Runbook & Reference](../../sources/aws-cloudtrail.md)

[^aws-guardduty]: Amazon GuardDuty - Runbook & Reference
[^aws-security-hub]: AWS Security Hub CSPM - Runbook & Reference
[^aws-cloudtrail]: AWS CloudTrail - Runbook & Reference
