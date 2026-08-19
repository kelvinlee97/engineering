# Amazon S3 - Runbook & Reference

> Facts verified against official AWS documentation: 2026-08-18

## Overview

Amazon S3 is an object storage service for storing and protecting any amount of data: data lakes, websites, mobile apps, backup and restore, archives, enterprise applications, and analytics. S3 provides strong read-after-write consistency for PUT and DELETE requests in all AWS Regions.

## Buckets and objects

- A **bucket** is a container for objects; an **object** is a file plus its metadata, identified by a unique key within the bucket.
- **General purpose buckets** (recommended for most workloads): by default in the global namespace (unique names across all AWS accounts), private by default.
- **Directory buckets**: hierarchical layout, built for low-latency and data-residency use cases; all public access is disabled and cannot be enabled.
- **Table buckets**: store tabular data in Apache Iceberg format for analytics and machine learning.
- **Vector buckets**: purpose-built for vector data.

## Storage classes

- **Frequent access**: S3 Standard, S3 Express One Zone (single-digit millisecond latency).
- **Infrequent access**: S3 Standard-IA, S3 One Zone-IA.
- **Archive**: S3 Glacier Instant Retrieval, Glacier Flexible Retrieval, Glacier Deep Archive.
- **Automatic**: S3 Intelligent-Tiering moves data across four tiers based on access patterns.
- Use **lifecycle rules** to transition objects between classes or expire them.

## Common operations (AWS CLI)

```bash
# Create a bucket and list objects
aws s3 mb s3://my-bucket --region ap-southeast-1
aws s3 ls s3://my-bucket/

# Copy / sync / move / delete
aws s3 cp ./file.txt s3://my-bucket/path/
aws s3 cp s3://my-bucket/path/file.txt ./
aws s3 sync ./logs/ s3://my-bucket/logs/ --exclude "*.tmp"
aws s3 mv s3://my-bucket/old.txt s3://my-bucket/new.txt
aws s3 rm s3://my-bucket/path/ --recursive
aws s3 rb s3://my-bucket --force

# Filter semantics: order matters; exclude everything first, then re-include
aws s3 cp ./src/ s3://my-bucket/src/ --recursive --exclude "*" --include "*.jpg"

# Generate a presigned URL
aws s3 presign s3://my-bucket/path/file.txt --expires-in 3600
```

Low-level `aws s3api` commands cover versioning, lifecycle, encryption, and bucket policies. Large uploads use multipart upload automatically.

## Access control

- Buckets and objects are **private by default**; Block Public Access is on by default at the bucket level.
- Use **IAM policies**, **bucket policies**, and **access points**; AWS recommends policies over ACLs (ACLs are disabled by default via S3 Object Ownership).
- Audit access with **IAM Access Analyzer for S3**, CloudTrail, and server access logging.

## Data protection

- **Versioning**: keep multiple versions of an object and restore accidental overwrites/deletes.
- **S3 Object Lock**: write-once-read-many (WORM) protection for compliance.
- **Replication**: copy objects to same- or cross-Region buckets.
- **Server-side encryption**: SSE-S3 or SSE-KMS.

## Monitoring

- CloudWatch metrics (including billing alerts), CloudTrail API logging, server access logs, S3 Storage Lens (60+ usage/activity metrics), and S3 Inventory.

## Troubleshooting

| Symptom | Checks and fixes |
|---------|------------------|
| `AccessDenied` | Check IAM identity policy, bucket policy, access point policy, Block Public Access, and organization SCP/RCP. |
| `404 NoSuchKey` | Verify the key/prefix path, bucket Region, and whether versioning requires a version ID. |
| Slow uploads/downloads | Use multipart upload, Transfer Acceleration or CloudFront, and check the network path. |
| Unexpected cost growth | Use Storage Lens; add lifecycle rules; clean up incomplete multipart uploads. |
| Bucket name already taken | General purpose bucket names are globally unique; use a unique suffix or the account regional namespace. |

## Quotas

- General purpose buckets: 100 per account by default (adjustable).
- Directory buckets: 100 per account by default.
- Table buckets: 10 per account per Region; up to 10,000 tables per table bucket.
- Single PUT object size: up to 5 TB.
- See the Service Quotas console for current values.

## Official references

- [What is Amazon S3? - Amazon S3 User Guide](https://docs.aws.amazon.com/AmazonS3/latest/userguide/Welcome.html)
- [AWS CLI: s3 commands](https://docs.aws.amazon.com/cli/latest/reference/s3/)
- [Amazon S3 endpoints and quotas](https://docs.aws.amazon.com/general/latest/gr/s3.html)
