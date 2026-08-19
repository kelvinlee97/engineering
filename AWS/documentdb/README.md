# Amazon DocumentDB - Runbook & Reference

> Facts verified against official AWS documentation: 2026-08-19

## Overview

Amazon DocumentDB (with MongoDB compatibility) is a fast, reliable, fully managed document database. You can run the same application code, drivers, and tools you use with MongoDB. It separates storage from compute: a cluster volume is replicated six ways across three Availability Zones and grows automatically as data grows.

## Key concepts

- **Cluster**: one primary instance plus up to 15 replicas sharing a cluster volume; all instances can serve reads.
- **Elastic clusters**: a deployment type for millions of reads/writes per second and petabyte-scale storage.
- **Storage growth**: storage grows automatically in 10 GB increments, up to 256 TiB for engine version 8.0+ (128 TiB for earlier versions).
- **Reader endpoint**: a stable endpoint that load-balances reads across replicas.
- **Backups**: automatic, continuous, incremental backups to S3 with point-in-time recovery (up to the last 5 minutes); retention up to 35 days.
- **Encryption**: KMS encryption at rest for storage, backups, snapshots, and replicas.
- **MongoDB compatibility**: use MongoDB drivers and the MongoDB shell to connect.

## Common operations (AWS CLI)

```bash
# Create a cluster
aws docdb create-db-cluster --db-cluster-identifier app-docdb \
  --engine docdb --engine-version 5.0.0 \
  --master-username adminuser --master-user-password <password> \
  --backup-retention-period 7 --storage-encrypted

# Create an instance (primary)
aws docdb create-db-instance --db-instance-identifier app-docdb-1 \
  --db-cluster-identifier app-docdb --db-instance-class db.r6g.large --engine docdb

# Add replicas for read scaling
aws docdb create-db-instance --db-instance-identifier app-docdb-2 \
  --db-cluster-identifier app-docdb --db-instance-class db.r6g.large --engine docdb

# Inspect
aws docdb describe-db-clusters
aws docdb describe-db-instances

# Backup and restore
aws docdb create-db-cluster-snapshot --db-cluster-identifier app-docdb \
  --db-cluster-snapshot-identifier app-docdb-backup
aws docdb restore-db-cluster-from-snapshot \
  --db-cluster-identifier app-docdb-restored --snapshot-identifier app-docdb-backup \
  --engine docdb
```

## Best practices

- Right-size the primary and add replicas in different AZs for reads and failover; use the reader endpoint in applications.
- Enable automated backups and set retention per your RPO; test PITR restores.
- Use indexes that match your MongoDB query patterns; use `explain` to validate.
- Keep clusters in a VPC with security groups scoped to application subnets; enable TLS.
- Monitor with CloudWatch (CPU, connections, storage, replica lag) and DocumentDB events.
- For massive write/read scale, evaluate elastic clusters instead of instance-based clusters.
- Plan engine upgrades and instance class changes in a staging cluster first.

## Troubleshooting

| Symptom | Checks and fixes |
|---|---|
| Connection failures | Check security groups, TLS settings, and that the client uses the cluster endpoint (port 27017). |
| Read latency | Add replicas and use the reader endpoint; check replica lag. |
| Storage full | DocumentDB grows automatically; if at the engine limit, evaluate elastic clusters or archive data. |
| Slow queries | Review indexes and query patterns with `explain`; adjust instance class if CPU-bound. |
| PITR restore fails | Verify retention period and that the cluster has automated backups enabled. |

## Limits

Up to 15 replicas per cluster; storage up to 256 TiB (engine 8.0+) or 128 TiB (earlier engines); backup retention up to 35 days. Cluster and instance counts have per-account quotas. See the Service Quotas console for current values.

## Official references

- [What is Amazon DocumentDB (with MongoDB compatibility)?](https://docs.aws.amazon.com/documentdb/latest/developerguide/what-is.html)
- [Amazon DocumentDB quotas](https://docs.aws.amazon.com/documentdb/latest/developerguide/limits.html)
- [Amazon DocumentDB pricing](https://aws.amazon.com/documentdb/pricing/)
- [AWS CLI: docdb commands](https://docs.aws.amazon.com/cli/latest/reference/docdb/)
