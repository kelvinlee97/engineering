---
type: Service
title: Amazon GuardDuty
description: AWS's threat detection service that analyzes CloudTrail, VPC Flow Logs, and DNS logs, plus optional protection plans, to produce findings.
tags: [aws, security, threat-detection]
sources:
  - id: aws-guardduty
    resource: https://github.com/kelvinlee97/engineering/blob/main/AWS/guardduty/README.md
    title: "Amazon GuardDuty - Runbook & Reference"
    author: human:kelvinlee97
    last_modified: 2026-09-24T14:48:10Z
generated: { by: claude-code/wiki-v1, at: 2026-09-25T06:00:00Z }
status: draft
---

GuardDuty continuously analyzes CloudTrail management events, VPC Flow Logs, and DNS logs, using threat intelligence and machine learning to produce security findings. Optional protection plans add EKS audit logs, RDS logins, S3 data events, malware scanning, runtime monitoring, Lambda network activity, and AI workloads.[^aws-guardduty]

## Concepts

- One **detector** per account per Region; findings have Low, Medium, or High severity.[^aws-guardduty]
- Foundational sources start ingesting as soon as it is enabled; protection plans are enabled separately.[^aws-guardduty]
- Filters and suppression rules reduce noise but hide findings rather than fix causes.[^aws-guardduty]

## Practices

- Enable in all Regions and accounts, managed through Organizations with a delegated administrator.[^aws-guardduty]
- Send findings to EventBridge and Security Hub CSPM, and export to S3 to keep them beyond 90 days.[^aws-guardduty]
- Test the pipeline with sample findings.[^aws-guardduty]

## Troubleshooting and limits

| Symptom | Check |
| --- | --- |
| No findings | Detector enabled, sources ingesting; generate samples |
| Missing S3, EKS, or RDS detection | The matching protection plan in the same Region |
| Accidental deletion | `delete-detector` removes findings; suspend with `update-detector --no-enable` instead |

As tabled in the note.[^aws-guardduty] Findings are kept 90 days (fixed); up to 6 threat intelligence sets and 100 filters per detector.[^aws-guardduty] See [Security findings pipeline](security-findings-pipeline.md).

## Related

- Source: [Amazon GuardDuty - Runbook & Reference](../../sources/aws-guardduty.md)

[^aws-guardduty]: Amazon GuardDuty - Runbook & Reference
