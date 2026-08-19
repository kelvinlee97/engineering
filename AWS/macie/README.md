# Amazon Macie - Runbook & Reference

> Facts verified against official AWS documentation: 2026-08-19

## Overview

Amazon Macie is a data security service that discovers sensitive data in Amazon S3 using machine learning and pattern matching, evaluates S3 buckets for security and access-control issues, and generates findings you can review and remediate. It provides a bucket inventory, a dashboard, and automated sensitive data discovery.

## Key concepts

- **Bucket inventory and monitoring**: Macie automatically inventories S3 general purpose buckets and evaluates them for public access, shared access, and encryption issues, producing policy findings.
- **Sensitive data discovery**: automated discovery samples representative objects continuously, or you run discovery jobs for deeper, targeted analysis of specific buckets with defined sampling depth.
- **Managed data identifiers**: built-in criteria detecting PII, financial information, and credentials for many countries/regions; custom data identifiers use your regex and proximity rules; allow lists exclude known acceptable text.
- **Findings**: detailed reports with severity, affected resource, and detection details; can be reviewed in the console/API and exported to EventBridge or AWS Security Hub CSPM.
- **Multi-account**: designate a Macie administrator via AWS Organizations (or invitations) to manage member accounts and inspect their buckets.
- **Free trial**: first enablement includes a 30-day free trial for bucket evaluation and automated discovery (jobs are not included).

## Common operations (AWS CLI)

```bash
# Enable Macie and check session state
aws macie2 enable-macie --finding-publishing-frequency FIFTEEN_MINUTES
aws macie2 get-macie-session

# Review bucket inventory and statistics
aws macie2 list-buckets --account-ids 123456789012
aws macie2 get-bucket-statistics --account-id 123456789012

# Create and run a sensitive data discovery job
aws macie2 create-classification-job --job-type ONE_TIME \
  --name pii-scan --s3-job-definition file://job.json \
  --sampling-percentage 100
aws macie2 list-classification-jobs

# Findings
aws macie2 list-findings --finding-criteria '{"severity":{"gte":50}}'
aws macie2 get-findings --finding-ids file://finding-ids.json
```

## Best practices

- Enable Macie before S3 data grows, so the inventory and baseline are established early.
- Use automated discovery for broad coverage and targeted jobs for high-value buckets or compliance deadlines.
- Combine managed and custom data identifiers; use allow lists to reduce noise from known sample data.
- Route findings to EventBridge for automated response and to Security Hub CSPM for aggregated security posture.
- Enforce bucket policies for public/encrypted access so policy findings stay low; remediate findings promptly.
- In multi-account environments, manage Macie centrally with a delegated administrator via AWS Organizations.

## Troubleshooting

| Symptom | Checks and fixes |
|---|---|
| Buckets not inventoried | Confirm Macie is enabled in the bucket's Region and the account is a member. |
| No sensitive data findings | Check job/automated discovery configuration, sampling percentage, and managed identifier scope. |
| Object analysis errors | Verify object permissions, KMS key access for decryption, and supported object types. |
| Findings not in Security Hub CSPM | Enable the Macie integration in Security Hub CSPM in the same Region. |
| Cost higher than expected | Review the number of buckets monitored, discovery job volume, and sampling settings. |

## Limits

Classification jobs per account, findings retention, and API quotas apply. See the Amazon Macie endpoints and quotas page and Service Quotas console for current values.

## Official references

- [What is Amazon Macie?](https://docs.aws.amazon.com/macie/latest/user/what-is-macie.html)
- [Amazon Macie endpoints and quotas](https://docs.aws.amazon.com/general/latest/gr/macie.html)
- [Amazon Macie pricing](https://aws.amazon.com/macie/pricing/)
- [AWS CLI: macie2 commands](https://docs.aws.amazon.com/cli/latest/reference/macie2/)
