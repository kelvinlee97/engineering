# AWS Database Migration Service (DMS) - Runbook & Reference

> Facts verified against official AWS documentation: 2026-08-19

## Overview

AWS Database Migration Service (AWS DMS) migrates relational databases, data warehouses, NoSQL databases, and other data stores into AWS or between combinations of cloud and on-premises environments. It supports one-time migrations and ongoing replication to keep sources and targets in sync, plus Fleet Advisor (discovery) and Schema Conversion (engine conversion).

## Key concepts

- **Replication instance**: the compute resource that runs the migration tasks.
- **Endpoints**: source and target connection definitions (engine, host, credentials, VPC).
- **Replication task**: a scheduled unit of work (full load, ongoing replication/CDC, or both).
- **Schema conversion**: DMS Schema Conversion or the downloadable AWS Schema Conversion Tool (AWS SCT) converts schemas/code to the target engine.
- **Fleet Advisor**: discovers and inventories on-premises database servers to plan migrations.
- **DMS Serverless**: runs replication instances on demand without provisioning capacity.
- **Data validation**: compares source and target data to catch mismatches.
- **Heterogeneous migrations**: DMS supports migrations between different engines (for example, Oracle to Aurora PostgreSQL).

## Common operations (AWS CLI)

```bash
# Create a replication instance
aws dms create-replication-instance --replication-instance-identifier mig1 \
  --replication-instance-class dms.t3.medium --engine-version 3.5.3 \
  --allocated-storage 50 --no-publicly-accessible

# Create source and target endpoints
aws dms create-endpoint --endpoint-identifier src-oracle \
  --endpoint-type source --engine-name oracle \
  --server-name db01.example --port 1521 --username app \
  --password <password> --database-name ORCL
aws dms create-endpoint --endpoint-identifier tgt-aurora \
  --endpoint-type target --engine-name aurora-postgresql \
  --server-name cluster.cluster-xxxx.us-east-1.rds.amazonaws.com \
  --port 5432 --username app --password <password> --database-name app

# Create and start a task (full load + CDC)
aws dms create-replication-task --replication-task-identifier full-cdc \
  --source-endpoint-arn <src-arn> --target-endpoint-arn <tgt-arn> \
  --replication-instance-arn <instance-arn> \
  --migration-type full-load-and-cdc \
  --table-mappings file://table-mappings.json
aws dms start-replication-task --replication-task-arn <task-arn> \
  --start-replication-task-type start-replication

# Monitor and stop
aws dms describe-replication-tasks
aws dms stop-replication-task --replication-task-arn <task-arn>
```

## Best practices

- Use Fleet Advisor and Schema Conversion early to size the migration and convert schemas before cutover.
- Run a full-load test on a representative dataset; validate data with DMS data validation.
- Keep the replication instance in a private subnet with proper security groups for both endpoints.
- Use CDC for minimal-downtime cutover; stop application writes, verify lag, then cut over.
- Use DMS Serverless for variable or infrequent migration workloads.
- Encrypt replication instances and endpoints with KMS; use SSL/TLS where supported.
- Take a target backup immediately after cutover and retain migration logs for audit.

## Troubleshooting

| Symptom | Checks and fixes |
|---|---|
| Task stuck in failed state | Check task logs and endpoint connectivity; verify credentials and network routes. |
| CDC lag growing | Check source retention (for example, Oracle archive logs) and replication instance capacity. |
| Data mismatch | Run data validation, review transformation rules in table mappings. |
| Cannot connect to source | Verify security group/NACL rules, endpoint settings, and source-side firewall. |
| LOB/CLOB issues | Configure LOB mode appropriately for large objects. |

## Limits

Replication instances, endpoints, tasks, and concurrent connections have per-account quotas. See the Service Quotas console for current values.

## Official references

- [What is AWS Database Migration Service?](https://docs.aws.amazon.com/dms/latest/userguide/Welcome.html)
- [AWS DMS service quotas](https://docs.aws.amazon.com/dms/latest/userguide/CHAP_Limits.html)
- [AWS Database Migration Service pricing](https://aws.amazon.com/dms/pricing/)
- [AWS CLI: dms commands](https://docs.aws.amazon.com/cli/latest/reference/dms/)
