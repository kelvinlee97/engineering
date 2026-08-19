# Amazon Redshift - Runbook & Reference

> Facts verified against official AWS documentation: 2026-08-19

## Overview

Amazon Redshift is a fully managed, petabyte-scale data warehouse. It uses columnar storage and massively parallel processing (MPP) for fast SQL analytics, and it integrates with the BI and SQL tools you already use. Redshift Serverless removes cluster administration, automatically provisions capacity, scales for demand, and stops charging when idle.

## Key concepts

- **Cluster (provisioned)**: a set of compute nodes with a leader node; you manage node types, counts, and maintenance windows.
- **Redshift Serverless**: namespaces (databases) and workgroups; capacity scales automatically in RPUs (Redshift Processing Units).
- **Node types**: RA3 nodes separate compute from managed storage, letting you scale compute independently; DC2 is for fixed local storage.
- **Columnar storage and compression**: analytics-optimized layout; choose sort and distribution keys to reduce I/O.
- **Redshift Spectrum**: query data directly in S3 without loading it into the warehouse.
- **Concurrency scaling**: adds transient capacity to serve concurrent queries.
- **Snapshots**: automatic snapshots (retention up to 35 days) and manual snapshots, restorable to another Region.
- **Python UDFs**: support ends June 30, 2026; plan migrations to SQL UDFs or Lambda UDFs.

## Common operations (AWS CLI)

```bash
# Create a provisioned cluster
aws redshift create-cluster --cluster-identifier dw-prod \
  --node-type ra3.xlplus --number-of-nodes 2 \
  --master-username adminuser --master-user-password <password> \
  --publicly-accessible

# List and describe clusters
aws redshift describe-clusters
aws redshift describe-clusters --cluster-identifier dw-prod

# Pause/resume to save cost
aws redshift pause-cluster --cluster-identifier dw-prod
aws redshift resume-cluster --cluster-identifier dw-prod

# Snapshots
aws redshift create-cluster-snapshot --cluster-identifier dw-prod --snapshot-identifier dw-prod-backup
aws redshift restore-from-cluster-snapshot --cluster-identifier dw-restored \
  --snapshot-identifier dw-prod-backup

# Serverless: create namespace and workgroup
aws redshift-serverless create-namespace --namespace-name analytics
aws redshift-serverless create-workgroup --workgroup-name analytics-wg \
  --namespace-name analytics --base-capacity 8
```

## Best practices

- Choose RA3 for most workloads so storage scales separately from compute; use Serverless for variable/unpredictable demand.
- Design tables with appropriate distribution and sort keys; vacuum and analyze regularly (or use automatic maintenance).
- Load in bulk (COPY from S3 with columnar formats) instead of row-by-row inserts.
- Use Redshift Spectrum for cold data in S3 and reserve warehouse capacity for hot data.
- Use workload management (WLM), concurrency scaling, and query monitoring rules to protect SLAs.
- Encrypt with KMS, keep clusters in private subnets, and rotate credentials (or use IAM/Secrets Manager integration).
- Automate snapshots and test cross-Region restore as part of DR.

## Troubleshooting

| Symptom | Checks and fixes |
|---|---|
| Slow queries | Check distribution/sort keys, table statistics, WLM queues, and whether Spectrum would be cheaper for cold data. |
| Disk full (DC2) | Resize, offload cold data, or move to RA3 managed storage. |
| COPY failures | Validate source file format, IAM role permissions on S3, and column mapping. |
| Connection limits | Increase cluster size, use connection pooling, or add concurrency scaling. |
| Snapshot restore slow | Verify snapshot availability and choose sufficient cluster size for restore. |
| Python UDF errors | Migrate Python UDFs before June 30, 2026 support end. |

## Limits

Cluster counts, node counts, snapshots, and Serverless capacity have per-account quotas. See the Service Quotas console for current values.

## Official references

- [What is Amazon Redshift? - Management Guide](https://docs.aws.amazon.com/redshift/latest/mgmt/welcome.html)
- [Amazon Redshift Database Developer Guide](https://docs.aws.amazon.com/redshift/latest/dg/welcome.html)
- [Amazon Redshift pricing](https://aws.amazon.com/redshift/pricing/)
- [AWS CLI: redshift commands](https://docs.aws.amazon.com/cli/latest/reference/redshift/)
