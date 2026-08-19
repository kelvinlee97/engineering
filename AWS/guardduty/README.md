# Amazon GuardDuty - Runbook & Reference

> Facts verified against official AWS documentation: 2026-08-19

## Overview

Amazon GuardDuty is a threat detection service that continuously monitors and analyzes AWS data sources, including CloudTrail management events, VPC Flow Logs, and DNS logs. It also offers optional protection plans for EKS audit logs, RDS login activity, S3 data events, EBS malware scanning, runtime monitoring for EC2/EKS/ECS, Lambda network activity, and AI workloads. GuardDuty uses threat intelligence feeds (malicious IPs and domains, file hashes) and machine learning to produce security findings.

## Key concepts

- **Detector**: the GuardDuty configuration object; one per account per Region.
- **Findings**: structured records of detected threats with a severity level (Low/Medium/High) and resource details.
- **Foundational data sources**: CloudTrail management events, VPC Flow Logs (from EC2), and DNS logs; ingestion starts automatically when you enable GuardDuty.
- **Protection plans**: optional feature groups such as S3 Protection, EKS Audit Log Monitoring, Malware Protection for EBS/S3/backups, RDS Protection, Runtime Monitoring, Lambda Protection, and AI Protection.
- **Administrator and member accounts**: multi-account management via AWS Organizations (recommended) or invitations.
- **Filters and suppression rules**: reduce noise for known-benign activity.
- **Threat intelligence sets and trusted IP lists**: customize detection context.

## Common operations (AWS CLI)

```bash
# Enable GuardDuty (creates the detector)
aws guardduty create-detector --enable

# Get the detector ID
aws guardduty list-detectors

# List and inspect findings
aws guardduty list-findings --detector-id <detector-id>
aws guardduty get-findings --detector-id <detector-id> --finding-ids <finding-id>

# Suspend (keeps data) or delete (removes findings and configuration)
aws guardduty update-detector --detector-id <detector-id> --no-enable
aws guardduty delete-detector --detector-id <detector-id>

# Archive or unarchive findings
aws guardduty archive-findings --detector-id <detector-id> --finding-ids <finding-id>
aws guardduty unarchive-findings --detector-id <detector-id> --finding-ids <finding-id>

# Add a threat intelligence set
aws guardduty create-threat-intel-set --detector-id <detector-id> --name my-intel \
  --format TXT --location s3://bucket/threat-intel.txt --activate
```

## Best practices

- Enable GuardDuty in all Regions and accounts; manage multi-account setup through AWS Organizations with a delegated administrator.
- Enable the protection plans that match your workload (S3, EKS audit, runtime monitoring, malware protection).
- Send findings to EventBridge and AWS Security Hub CSPM; automate response with Lambda and SNS.
- Validate the detection pipeline with sample findings and the GuardDuty tester script.
- Export findings to S3 for retention beyond 90 days and for analysis.
- Use filters and suppression rules carefully: they hide findings, they don't fix root causes.
- Grant least-privilege IAM permissions; use a dedicated role for detection automation.

## Troubleshooting

| Symptom | Checks and fixes |
|---|---|
| No findings | Confirm the detector is enabled and foundational sources are ingesting; generate sample findings to test. |
| Missing S3/EKS/RDS detection | Enable the corresponding protection plan in the same Region. |
| Findings absent from Security Hub CSPM | Enable Security Hub CSPM and its GuardDuty integration in the same Region. |
| EventBridge rule not firing | Verify the event pattern source (`aws.guardduty`) and that findings are being created. |
| Malware scan not running | Check the Malware Protection plan, snapshot permissions, and scan quotas. |
| Accidental deletion | `delete-detector` removes findings and configuration; use suspend (`update-detector --no-enable`) to keep data. |

## Limits

One detector per account per Region; findings retained 90 days (fixed); up to 6 threat intelligence sets and 1 trusted IP list; up to 100 filters; up to 5,000 member accounts by invitation or 50,000 via AWS Organizations, per Region. Check the Service Quotas console for details.

## Official references

- [What is Amazon GuardDuty? - GuardDuty User Guide](https://docs.aws.amazon.com/guardduty/latest/ug/what-is-guardduty.html)
- [Amazon GuardDuty endpoints and quotas](https://docs.aws.amazon.com/general/latest/gr/guardduty.html)
- [Amazon GuardDuty pricing](https://aws.amazon.com/guardduty/pricing/)
- [AWS CLI: guardduty commands](https://docs.aws.amazon.com/cli/latest/reference/guardduty/)
