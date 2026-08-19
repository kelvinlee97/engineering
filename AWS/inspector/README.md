# Amazon Inspector - Runbook & Reference

> Facts verified against official AWS documentation: 2026-08-19

## Overview

Amazon Inspector is a vulnerability management service that automatically discovers workloads and continuously scans them for software vulnerabilities and unintended network exposure. It scans EC2 instances, container images in Amazon ECR, and Lambda functions, and produces findings with remediation guidance and an environment-specific risk score.

## Key concepts

- **Findings**: detailed reports of detected vulnerabilities or network exposure; include severity, affected resource, and remediation recommendations; findings close automatically when remediated.
- **Continuous scanning**: Inspector discovers eligible resources and rescans automatically when packages are installed/patched or when a new CVE affecting a resource is published.
- **Risk score**: severity tailored to your environment using CVSS and your resource context (network reachability, exploitability).
- **Coverage and dashboard**: view scan coverage, most critical findings, and affected resources; generate CSV/JSON reports.
- **Delegated administrator**: with AWS Organizations, one account centrally enables and manages Inspector for member accounts.
- **Integrations**: findings publish to Amazon EventBridge and AWS Security Hub CSPM for near-real-time response.
- **Suppression rules**: filter out unwanted findings by criteria.

## Common operations (AWS CLI)

```bash
# Enable Inspector (scan types: EC2, ECR, Lambda)
aws inspector2 enable --resource-types EC2 ECR LAMBDA \
  --account-ids 123456789012

# List findings and coverage
aws inspector2 list-findings --filter-criteria '{"severity":[{"comparison":"EQUALS","value":"CRITICAL"}]}'
aws inspector2 list-coverage --account-id 123456789012

# Generate a findings report
aws inspector2 get-findings-report --report-format CSV \
  --s3-url s3://reports-bucket/inspector/ \
  --report-file-name inspector-findings

# Disable a scan type
aws inspector2 disable --resource-types EC2
```

## Best practices

- Enable Inspector across the whole organization with a delegated administrator so new accounts and resources are covered automatically.
- Scan all three resource types (EC2, ECR, Lambda) and review critical/high findings on a schedule.
- Use the risk score and dashboard to prioritize findings with real exploitability and exposure, not just raw CVSS.
- Route findings to EventBridge for automated response (quarantine, ticketing) and to Security Hub CSPM for aggregated posture.
- Use suppression rules for accepted risks and document them; keep scan coverage high.
- Fix and verify: close findings only after remediation is confirmed (Inspector closes them automatically when resolved).

## Troubleshooting

| Symptom | Checks and fixes |
|---|---|
| No resources scanned | Verify Inspector is enabled for the scan type, the account is a member, and SSM Agent is running on EC2 (agentless scanning options also apply). |
| Findings missing for Lambda | Confirm Lambda scanning is enabled and functions are in supported runtimes. |
| ECR images not scanned | Check the repository and that images were pushed after enabling scan-on-push or continuous scanning. |
| Delegated admin not working | Designate the delegated administrator in AWS Organizations and enable the service from that account. |
| Findings not in Security Hub CSPM | Enable the Inspector integration in Security Hub CSPM in the same Region. |

## Limits

Findings retention, API request rates, and per-account/resource scan quotas apply. See the Amazon Inspector endpoints and quotas page and Service Quotas console for current values.

## Official references

- [What is Amazon Inspector?](https://docs.aws.amazon.com/inspector/latest/user/what-is-inspector.html)
- [Amazon Inspector endpoints and quotas](https://docs.aws.amazon.com/general/latest/gr/inspector.html)
- [Amazon Inspector pricing](https://aws.amazon.com/inspector/pricing/)
- [AWS CLI: inspector2 commands](https://docs.aws.amazon.com/cli/latest/reference/inspector2/)
