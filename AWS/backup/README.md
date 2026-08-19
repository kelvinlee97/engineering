# AWS Backup - Runbook & Reference

> Facts verified against official AWS documentation: 2026-08-19

## Overview

AWS Backup is a fully managed backup service that centralizes backup policies, monitoring, and compliance across supported AWS services. You define backup plans once and apply them to resources; AWS Backup automates backup scheduling, retention, lifecycle transitions, and cross-Region/cross-account copies.

## Key concepts

- **Backup plan**: rules that define when to run backups, how long to keep them, and which vault receives them; a plan can include multiple rules.
- **Backup vault**: a container that stores backups and controls access with vault policies; vaults are per-Region resources.
- **Vault Lock**: enforces immutable (WORM) backup protection with governance or compliance modes, preventing backup deletion even by administrators.
- **Lifecycle**: transition backups from warm storage to cold storage after a specified period, and expire them at the retention end.
- **Cross-Region and cross-account backup**: copy backups to another Region or account for disaster recovery and isolation.
- **Incremental backups**: AWS Backup stores incremental changes after the initial full backup for supported resource types.
- **Audit Manager integration**: report and monitor backup activity for compliance.

Supported resources include EC2, EBS, S3, RDS, Aurora, DynamoDB, EFS, FSx, DocumentDB, Neptune, Redshift and Redshift Serverless, Timestream, VMware Cloud on AWS, EKS (via Backup for EKS), SAP HANA on EC2, and CloudFormation.

## Common operations (AWS CLI)

```bash
# Create a vault and a backup plan
aws backup create-backup-vault --backup-vault-name prod
aws backup create-backup-plan --backup-plan file://plan.json

# List plans, vaults, and jobs
aws backup list-backup-plans
aws backup list-backup-vaults
aws backup list-backup-jobs --by-state RUNNING

# Assign resources to a plan
aws backup create-backup-selection \
  --backup-plan-id <plan-id> \
  --backup-selection file://selection.json

# Start a backup manually and monitor it
aws backup start-backup-job --resource-arn <resource-arn> \
  --backup-vault-name prod
aws backup describe-backup-job --backup-job-id <job-id>
```

## Best practices

- Centralize plans by workload class (for example, database, application, file) and apply them with tag-based or resource-based selections.
- Use Vault Lock in compliance mode for regulated data and test governance mode before enforcing.
- Configure cross-Region copy for critical data and cross-account copy for isolation from the production account.
- Set lifecycle rules so cold backups are used only where recovery time allows cold storage retrieval.
- Monitor backup and restore jobs with CloudWatch events and alarms; test restores regularly.
- Restrict vault access with IAM and vault policies; enable AWS Backup Audit Manager for compliance reporting.

## Troubleshooting

| Symptom | Checks and fixes |
|---|---|
| Backup job failed | Check the job status message, resource permissions, and that the resource is in a supported state. |
| Restore slow | Cold storage retrievals take longer; use warm copies for time-critical restores. |
| Vault Lock cannot be removed | Compliance mode is permanent by design; create a new vault if you need different protection. |
| Cross-account copy missing | Verify the destination account vault policy grants backup access and the copy role is configured. |
| Plan not applying to resources | Confirm the backup selection tags/ARNs match the resources and the plan is assigned. |

## Limits

Backup plans, vaults, and jobs per account per Region, plus restore and copy quotas, apply. Cold storage has minimum retention periods. See the AWS Backup endpoints and quotas page and Service Quotas console for current values.

## Official references

- [What is AWS Backup?](https://docs.aws.amazon.com/aws-backup/latest/devguide/whatisbackup.html)
- [AWS Backup supported resources](https://docs.aws.amazon.com/aws-backup/latest/devguide/whatisbackup.html#supported-resources)
- [AWS Backup Vault Lock](https://docs.aws.amazon.com/aws-backup/latest/devguide/vault-lock.html)
- [AWS Backup endpoints and quotas](https://docs.aws.amazon.com/general/latest/gr/aws-backup.html)
- [AWS Backup pricing](https://aws.amazon.com/backup/pricing/)
- [AWS CLI: backup commands](https://docs.aws.amazon.com/cli/latest/reference/backup/)
