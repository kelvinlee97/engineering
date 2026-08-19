# AWS Trusted Advisor - Runbook & Reference

> Facts verified against official AWS documentation: 2026-08-19

## Overview

AWS Trusted Advisor inspects your AWS environment and recommends actions to save money, improve system availability and performance, and close security gaps. It checks your account against best practices across five categories: cost optimization, security, fault tolerance, performance, and service limits.

## Key concepts

- **Checks**: automated best-practice evaluations per category (for example, underutilized EC2 instances, MFA on root account, RDS backup enabled, service limit usage).
- **Support plans and access**: all checks plus the Trusted Advisor API are available with AWS Business Support+, Enterprise Support, or AWS Unified Operations; Basic Support provides Service Limits checks and selected Security/Fault tolerance checks, with manual refresh for Security.
- **Console**: the Trusted Advisor console shows check status (green/red/yellow) and recommended actions; you can refresh checks manually.
- **API and EventBridge**: Business Support+ and above can read check results via the Support API and monitor check status changes with Amazon EventBridge.
- **Service limits**: the service limits category tracks your usage against quotas and notifies you before you hit limits.

## Common operations (AWS CLI)

```bash
# List available checks
aws support describe-trusted-advisor-checks --language en

# Refresh a check and read its result
aws support refresh-trusted-advisor-check --check-id <check-id>
aws support describe-trusted-advisor-check-result --check-id <check-id>

# Summaries for all checks
aws support describe-trusted-advisor-check-summaries \
  --check-ids <check-id-1> <check-id-2>
```

## Best practices

- Review Trusted Advisor on a regular schedule and assign owners to each recommendation.
- Prioritize security and service-limits checks; act on critical findings (for example, MFA on the root account, open security groups) first.
- Use the API/EventBridge integration to track check status changes and alert your team automatically.
- Refresh checks after major changes (resizing, new accounts, security group changes) to confirm remediation.
- Combine with AWS Config and Security Hub CSPM for continuous compliance beyond Trusted Advisor's checks.

## Troubleshooting

| Symptom | Checks and fixes |
|---|---|
| Cannot access all checks | Confirm your support plan; full checks and API require Business Support+ or above. |
| Check result stale | Refresh the specific check; Basic Support requires manual refresh for Security checks. |
| API access denied | Verify IAM permissions for `support:DescribeTrustedAdvisorChecks` and related actions. |
| EventBridge not receiving events | Enable the Trusted Advisor integration and check the event pattern in the region. |
| Limits check outdated | Trusted Advisor service-limit data refreshes periodically; verify against the Service Quotas console. |

## Limits

Trusted Advisor availability depends on your AWS Support plan, and API request rates have quotas. See the AWS Support API reference and your support plan details for current values.

## Official references

- [AWS Trusted Advisor](https://docs.aws.amazon.com/awssupport/latest/user/trusted-advisor.html)
- [AWS Trusted Advisor API Reference](https://docs.aws.amazon.com/awssupport/latest/APIReference/API_DescribeTrustedAdvisorChecks.html)
- [AWS Support pricing and plans](https://aws.amazon.com/premiumsupport/plans/)
