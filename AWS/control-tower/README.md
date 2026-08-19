# AWS Control Tower - Runbook & Reference

> Facts verified against official AWS documentation: 2026-08-19

## Overview

AWS Control Tower orchestrates a multi-account AWS environment (landing zone) with governance controls and automation. It builds on AWS Organizations, AWS Service Catalog, and AWS IAM Identity Center to provision accounts, enforce guardrails, and give you a dashboard of your organization's compliance and drift.

## Key concepts

- **Landing zone**: the well-architected, multi-account baseline (management account, organizational units, guardrails, and shared accounts) that Control Tower creates and manages.
- **Organizational units (OUs)**: Control Tower manages the root OU and your custom OUs (for example, workload, sandbox) with enrolled accounts.
- **Controls (guardrails)**: governance rules applied to OUs and accounts.
  - **Preventive controls**: use service control policies (SCPs) to deny actions (for example, disallow public S3 buckets).
  - **Detective controls**: use AWS Config rules to detect and report non-compliant resources.
  - **Proactive controls**: use CloudFormation hooks to block non-compliant resources before provisioning.
- **Account Factory**: automates account creation, baselines, and account customization; accounts can be provisioned through the console, AWS Service Catalog, or APIs.
- **Drift detection**: Control Tower periodically checks for changes that violate the landing zone (for example, manual SCP changes) and reports them on the dashboard.
- **Extensions**: Control Tower integrates with AWS Service Catalog (Account Factory portfolios) and IAM Identity Center for access management.

## Common operations (AWS CLI)

```bash
# Check landing zone status and list OUs/accounts
aws controltower get-landing-zone --landing-zone-identifier <lz-id>
aws organizations list-roots
aws organizations list-accounts

# List controls on an OU
aws controltower list-enabled-controls --target-identifier <ou-arn>
aws controltower get-enabled-control --control-identifier <control-arn>
```

## Best practices

- Plan the OU structure and guardrails before creating the landing zone; changing the structure later requires drift review.
- Use Control Tower-managed accounts for workloads and keep the management account restricted to administrative tasks.
- Enforce preventive controls for high-impact actions (region restrictions, public access) and use detective controls for monitoring.
- Use Account Factory with baseline templates so every account starts compliant.
- Monitor the dashboard for drift and remediate promptly; do not manually modify resources Control Tower manages.
- Integrate with IAM Identity Center for centralized, least-privilege access to enrolled accounts.

## Troubleshooting

| Symptom | Checks and fixes |
|---|---|
| Landing zone shows drift | Review the dashboard for non-compliant resources/SCPs and remediate or re-register the affected account. |
| OU cannot be enrolled | Confirm the OU is in the organization's root hierarchy and does not conflict with Control Tower-managed structure. |
| Control status `not applicable` | Check control scope: some controls only apply to certain resource types or Regions. |
| Account Factory failure | Review AWS Service Catalog and CloudFormation stack set status for the account provisioning baseline. |
| Guardrail enforcement delayed | Detective controls rely on AWS Config; confirm Config recording is enabled in the target account/Region. |

## Limits

Control Tower supports specific OU and account structures, and some controls have Regional scope; landing zone, account, and control limits apply. See the AWS Control Tower endpoints and quotas documentation and Service Quotas console for current values.

## Official references

- [What is AWS Control Tower?](https://docs.aws.amazon.com/controltower/latest/userguide/what-is-control-tower.html)
- [AWS Control Tower controls](https://docs.aws.amazon.com/controltower/latest/userguide/controls.html)
- [AWS Control Tower endpoints and quotas](https://docs.aws.amazon.com/general/latest/gr/controltower.html)
- [AWS Control Tower pricing](https://aws.amazon.com/controltower/pricing/)
- [AWS CLI: controltower commands](https://docs.aws.amazon.com/cli/latest/reference/controltower/)
