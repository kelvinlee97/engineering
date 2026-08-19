# AWS Security Hub CSPM - Runbook & Reference

> Facts verified against official AWS documentation: 2026-08-19

## Overview

AWS Security Hub Cloud Security Posture Management (AWS Security Hub CSPM) provides a comprehensive view of the security state of your AWS environment. It collects findings from AWS services (such as GuardDuty, Inspector, and Macie) and supported partner products, runs continuous checks against security standards, and gives you a consolidated, prioritized view with security scores.

## Key concepts

- **Findings**: security issues normalized into the AWS Security Finding Format (ASFF).
- **Security standards and controls**: AWS Foundational Security Best Practices (FSBP) plus external frameworks such as CIS, PCI DSS, and NIST; each standard contains controls that run configuration checks.
- **Security scores**: aggregate compliance results that identify accounts and resources needing attention.
- **Insights**: collections of related findings; you can create custom insights.
- **Automation rules**: automatically update or suppress findings based on your criteria.
- **Cross-account and cross-Region aggregation**: designate an aggregation Region and link Regions for a single view.
- **AWS Config dependency**: most controls require AWS Config recording in the account and Region.

## Common operations (AWS CLI)

```bash
# Enable in the current Region (with default standards)
aws securityhub enable-security-hub --enable-default-standards

# Disable
aws securityhub disable-security-hub

# Standards and controls
aws securityhub get-enabled-standards
aws securityhub batch-enable-standards --standards-subscription-requests file://standards.json
aws securityhub list-security-controls --standards-arn <standards-arn>

# Findings
aws securityhub get-findings
aws securityhub batch-import-findings --findings file://findings.json
aws securityhub batch-update-findings --finding-identifiers file://identifiers.json --note "reviewed"

# Insights
aws securityhub create-insight --name open-critical --filters file://filters.json --group-by-attribute Severity
aws securityhub get-insight-results --insight-arn <insight-arn>
```

## Best practices

- Enable Security Hub CSPM in all supported Regions (required for full CIS Foundations compliance) and set up cross-Region aggregation.
- Enable AWS Config and record the resource types your standards check.
- Use a delegated administrator account with AWS Organizations for multi-account management.
- Prioritize with security scores and critical/high findings; automate triage with automation rules.
- Send findings to EventBridge for remediation (ticketing, Lambda, runbooks).
- Review enabled standards and disable unused ones to control costs.
- Plan for an initial baseline: findings are only generated after enablement.

## Troubleshooting

| Symptom | Checks and fixes |
|---|---|
| No findings after enabling | Verify AWS Config is recording, standards are enabled, and the Region is supported. |
| Controls not evaluating | Enable AWS Config in the account/Region and record the required resource types. |
| Aggregated view incomplete | Configure the aggregation Region correctly and enable Security Hub CSPM in linked Regions. |
| GuardDuty/Inspector findings absent | Enable the service and its Security Hub CSPM integration in the same Region. |
| Unexpected costs | Disable unused standards/controls; check usage under Settings → Usage. |

## Limits

Up to 11,000 member accounts per administrator per Region; 1,000 outstanding invitations; 50 custom actions; 100 custom insights; 100 insight results; findings retained 90 days (archive to S3 via EventBridge for longer retention). Check the Service Quotas console for current values.

## Official references

- [Introduction to AWS Security Hub CSPM](https://docs.aws.amazon.com/securityhub/latest/userguide/what-is-securityhub.html)
- [Security Hub quotas](https://docs.aws.amazon.com/securityhub/latest/userguide/securityhub_limits.html)
- [AWS Security Hub pricing](https://aws.amazon.com/security-hub/pricing/)
- [AWS CLI: securityhub commands](https://docs.aws.amazon.com/cli/latest/reference/securityhub/)
