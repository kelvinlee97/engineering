# Amazon Neptune - Runbook & Reference

> Facts verified against official AWS documentation: 2026-08-19

## Overview

Amazon Neptune is a fast, reliable, fully managed graph database for highly connected datasets. It supports property graphs (Apache TinkerPop Gremlin and openCypher) and RDF graphs (SPARQL), and is used for fraud detection, recommendation engines, knowledge graphs, drug discovery, and network security.

## Key concepts

- **DB cluster**: a primary instance plus up to 15 read replicas sharing a cluster volume.
- **Cluster volume**: SSD-backed storage replicated across three Availability Zones; durable, self-healing, and grows automatically.
- **Property graph vs. RDF**: choose Gremlin/openCypher for property graphs or SPARQL for RDF data.
- **Neptune Analytics**: an analytics engine that loads large graph datasets (from Neptune or a data lake) into memory for fast analysis.
- **Backups**: continuous backups to S3 and point-in-time recovery (PITR).
- **Security**: VPC isolation, IAM, encryption at rest and in transit.
- **Graph notebooks**: Neptune Workbench/Jupyter notebooks for development and visualization.

## Common operations (AWS CLI)

```bash
# Create a cluster and instance
aws neptune create-db-cluster --db-cluster-identifier graph-prod \
  --engine neptune \
  --db-cluster-instance-class db.r6g.large \
  --master-username adminuser --master-user-password <password> \
  --backup-retention-period 7

aws neptune create-db-instance --db-instance-identifier graph-prod-1 \
  --db-cluster-identifier graph-prod --db-instance-class db.r6g.large --engine neptune

# Add read replicas
aws neptune create-db-instance --db-instance-identifier graph-prod-2 \
  --db-cluster-identifier graph-prod --db-instance-class db.r6g.large --engine neptune

# Inspect
aws neptune describe-db-clusters
aws neptune describe-db-instances

# Backup and restore
aws neptune create-db-cluster-snapshot --db-cluster-identifier graph-prod \
  --db-cluster-snapshot-identifier graph-prod-backup
aws neptune restore-db-cluster-from-snapshot \
  --db-cluster-identifier graph-restored --snapshot-identifier graph-prod-backup \
  --engine neptune
```

## Best practices

- Model data as a graph deliberately: high-fanout nodes and deep traversals are where graph databases win over relational joins.
- Use replicas for reads and automatic failover; keep the primary for writes.
- Design IDs and indexes (for Gremlin/SPARQL) to match query patterns; avoid full-graph scans.
- Use PITR retention that matches your RPO; test snapshot restore.
- Put clusters in private subnets and use IAM database auth plus TLS.
- Monitor with CloudWatch (CPU, memory, replica lag) and Neptune's own metrics (queries, Gremlin/SPARQL request latency).
- For heavy analytics over graph data, use Neptune Analytics rather than OLTP queries.

## Troubleshooting

| Symptom | Checks and fixes |
|---|---|
| Slow traversals | Review query plans, add indexes, and reduce super-node traversal. |
| Write throughput low | Scale the primary instance class; Neptune is read-scalable, writes go through the primary. |
| Failover issues | Confirm replicas are in different AZs and check replica lag. |
| PITR unavailable | Ensure backup retention is configured (PITR requires automated backups). |
| Connection refused | Check security group rules for the Neptune port (8182) and TLS settings. |

## Limits

Up to 15 replicas per cluster; instance classes, clusters per account, and storage growth are subject to quotas. See the Service Quotas console for current values.

## Official references

- [What Is Amazon Neptune?](https://docs.aws.amazon.com/neptune/latest/userguide/intro.html)
- [Amazon Neptune quotas](https://docs.aws.amazon.com/neptune/latest/userguide/limits.html)
- [Amazon Neptune pricing](https://aws.amazon.com/neptune/pricing/)
- [AWS CLI: neptune commands](https://docs.aws.amazon.com/cli/latest/reference/neptune/)
