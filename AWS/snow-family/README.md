# AWS Snow Family - Runbook & Reference

> Facts verified against official AWS documentation: 2026-08-19

## Overview

The AWS Snow Family provides physical devices for offline data transfer and edge computing in environments without reliable connectivity. **Note the current lifecycle:** Snowcone (HDD/SSD) was discontinued on November 12, 2024, and AWS Snowball Edge is no longer available to new customers. For new online data transfers, use AWS DataSync; for offline transfer options, review the current Snowball Edge documentation.

## Devices and current status

| Device | Purpose | Status |
|---|---|---|
| Snowball Edge Storage Optimized (210 TB) | Large-scale offline data migration, S3/EC2-compatible endpoints | No longer available to new customers |
| Snowball Edge Compute Optimized | Edge compute with local processing | No longer available to new customers |
| Snowcone (HDD/SSD) | Small edge compute/data transfer | Discontinued November 12, 2024 |
| Snowmobile | Exabyte-scale data center transfer | Retired March 2024 |

## Key concepts

- **Job**: an import/export job for moving data between your site and Amazon S3; create and manage jobs in the console or with the Snowball API.
- **Device configuration**: Storage Optimized (210 TB, up to 40 vCPUs) vs. Compute Optimized (up to 104 vCPUs with GPU options).
- **Endpoints**: Snowball Edge exposes S3- and EC2-compatible endpoints plus NFS, for local workloads.
- **Clusters**: group 3-16 devices for local storage and compute with higher durability.
- **OpsHub / Snowball Edge client**: tools for unlocking the device, configuring the network, and transferring data.

## Common operations (AWS CLI)

```bash
# Create an import job (S3 destination)
aws snowball create-job --job-type IMPORT --resources '{"S3":{"S3ResourceArns":["arn:aws:s3:::bucket-name"]}}' \
  --address-id <address-id> --role-arn arn:aws:iam::123456789012:role/snowball-role \
  --snowball-capacity-preference T210 --shipping-option SECOND_DAY

# List and inspect jobs
aws snowball list-jobs
aws snowball describe-job --job-id <job-id>

# Update the shipping address or state
aws snowball update-job --job-id <job-id> --address-id <new-address-id>

# Cancel a job before the device ships
aws snowball cancel-job --job-id <job-id>
```

## Best practices

- For ongoing or online migrations, use AWS DataSync instead of physical devices where possible.
- Estimate data volume and transfer time before ordering; choose the right device size to minimize shipping legs.
- Set up the S3 bucket, IAM role, and shipping address before creating the job.
- Use AWS OpsHub to unlock and monitor the device; keep the unlock code and manifest secure.
- Enable encryption: data on Snow devices is encrypted at rest and in transit by default.
- Track the device with the E Ink shipping label and follow import/export return procedures.
- For edge compute, snapshot AMIs and plan for device replacement; AWS monitors connected devices and can ship replacements.

## Troubleshooting

| Symptom | Checks and fixes |
|---|---|
| Device won't unlock | Verify the job state and use the correct manifest/unlock code from the console. |
| Slow local transfer | Check the local network between clients and device (10/25/40/100 GbE), and use the S3 adapter or NFS as appropriate. |
| Data not appearing in S3 | Confirm the job completed and was processed by AWS after the device was returned. |
| Job cancelled after shipping | Contact AWS Support; shipped jobs generally cannot be cancelled. |
| Edge compute instances fail | Verify AMI compatibility with Snowball Edge (sbe1/sbe-c/sbe-g instance types). |

## Limits

Job counts per account, device counts in flight, and cluster sizes (3-16 devices) are constrained by AWS quotas and regional availability. Check the Service Quotas console and Snowball Edge documentation for current values.

## Official references

- [What is Snowball Edge?](https://docs.aws.amazon.com/snowball/latest/developer-guide/whatisedge.html)
- [AWS DataSync (recommended for new online transfers)](https://docs.aws.amazon.com/datasync/latest/userguide/what-is-datasync.html)
- [AWS Snowball Edge pricing](https://aws.amazon.com/snowball/pricing/)
- [AWS CLI: snowball commands](https://docs.aws.amazon.com/cli/latest/reference/snowball/)
