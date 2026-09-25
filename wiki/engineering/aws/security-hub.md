---
type: Service
title: AWS Security Hub CSPM
description: AWS's security posture service that gathers findings from other services and runs continuous checks against security standards.
tags: [aws, security, compliance]
sources:
  - id: aws-security-hub
    resource: https://github.com/kelvinlee97/engineering/blob/main/AWS/security-hub/README.md
    title: "AWS Security Hub CSPM - Runbook & Reference"
    author: human:kelvinlee97
    last_modified: 2026-09-24T14:48:10Z
generated: { by: claude-code/wiki-v1, at: 2026-09-25T06:00:00Z }
status: draft
---

Security Hub Cloud Security Posture Management (CSPM) gives a consolidated view of an environment's security state: it collects findings from services such as GuardDuty, Inspector, and Macie and from partners, and runs continuous checks against standards.[^aws-security-hub]

## Concepts

- Findings are normalized into the AWS Security Finding Format (ASFF).[^aws-security-hub]
- Standards include AWS Foundational Security Best Practices (FSBP), CIS, PCI DSS, and NIST; each contains controls that run configuration checks, and most controls need AWS Config recording in the account and Region.[^aws-security-hub]
- Security scores, insights, automation rules, and cross-Region aggregation.[^aws-security-hub]

## Practices

- Enable in all supported Regions with cross-Region aggregation, and enable AWS Config for the resource types standards check.[^aws-security-hub]
- Use a delegated administrator; route findings to EventBridge for remediation; disable unused standards to control cost.[^aws-security-hub]

## Troubleshooting and limits

| Symptom | Check |
| --- | --- |
| No findings after enabling | AWS Config recording, standards enabled, Region supported |
| GuardDuty or Inspector findings absent | The service and its integration in the same Region |
| Unexpected costs | Disable unused standards and controls |

As tabled in the note.[^aws-security-hub] Findings are kept 90 days; archive to S3 through EventBridge for longer.[^aws-security-hub] See [Security findings pipeline](security-findings-pipeline.md).

## Related

- Source: [AWS Security Hub CSPM - Runbook & Reference](../../sources/aws-security-hub.md)

[^aws-security-hub]: AWS Security Hub CSPM - Runbook & Reference
