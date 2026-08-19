# Amazon RDS - Runbook & Reference

> Facts verified against official AWS documentation: 2026-08-19

## Overview

Amazon Relational Database Service (Amazon RDS) makes it easier to set up, operate, and scale a relational database in the cloud. AWS manages backups, software patching, automatic failure detection, and recovery.

## Key concepts

- **DB instance**: the basic building block; an isolated database environment in the cloud.
- **Engines**: IBM Db2, MariaDB, Microsoft SQL Server, MySQL, Oracle, and PostgreSQL (Aurora is documented separately).
- **Instance classes**: general purpose (`db.m*`), memory optimized (`db.z*`, `db.x*`, `db.r*`), compute optimized (`db.c*`), burstable (`db.t*`).
- **Storage**: General Purpose SSD and Provisioned IOPS SSD; magnetic is deprecated (no restore to magnetic after July 1, 2026).
- **Multi-AZ**: synchronous standby in another AZ for failover; Multi-AZ DB clusters add reader nodes.
- **Read replicas**: scale read traffic asynchronously.
- **Backups**: automated backups with point-in-time recovery, plus manual snapshots.
- **Security**: VPC + security groups, IAM authentication, encryption at rest (KMS), TLS in transit.

## Common operations (AWS CLI)

```bash
# Create a DB instance
aws rds create-db-instance --db-instance-identifier mydb \
  --db-instance-class db.m7g.large --engine postgres \
  --master-username admin --master-user-password 'ChangeMe123!' \
  --allocated-storage 100 --db-subnet-group-name my-db-subnet-group

# Inspect
aws rds describe-db-instances --db-instance-identifier mydb
aws rds describe-db-engine-versions --engine postgres

# Modify / reboot
aws rds modify-db-instance --db-instance-identifier mydb --allocated-storage 200 --apply-immediately
aws rds reboot-db-instance --db-instance-identifier mydb

# Backups
aws rds create-db-snapshot --db-instance-identifier mydb --db-snapshot-identifier mydb-snapshot
aws rds restore-db-instance-from-db-snapshot --db-instance-identifier mydb-restored --db-snapshot-identifier mydb-snapshot

# Read replica
aws rds create-db-instance-read-replica --db-instance-identifier mydb-ro --source-db-instance-identifier mydb

# Delete (skip final snapshot only for disposable environments)
aws rds delete-db-instance --db-instance-identifier mydb --skip-final-snapshot
```

## Best practices

- Use **Multi-AZ** for production and **read replicas** for read scaling.
- Enable **automated backups with point-in-time recovery**; keep manual snapshots for long-term retention.
- Restrict network access with **security groups**; never enable public accessibility without strong justification.
- Enable **encryption at rest (KMS)** and require TLS for connections.
- Grant database users least privilege; use IAM authentication where supported.
- Monitor with CloudWatch metrics, Enhanced Monitoring, and Performance Insights; tune with parameter groups.

## Troubleshooting

| Symptom | Checks and fixes |
|---------|------------------|
| Connection refused/timeout | Check security group source rules, VPC/subnet routing, and public accessibility. |
| Storage full | Modify the DB instance to add storage; check slow-growth tables and logs. |
| Failover occurred | Review RDS events and notifications; check replica lag and primary load. |
| Slow queries | Use Performance Insights to find load; tune queries, indexes, and parameter groups. |
| Replica lag growing | Check replica instance class, primary write load, and long transactions. |
| Restore fails to magnetic | Magnetic storage is deprecated; restore to General Purpose or Provisioned IOPS SSD. |

## Limits

Per-Region quotas apply to DB instances (default 40), storage, and read replicas; storage minimums/maximums vary by engine. See the Service Quotas console for current values.

## Official references

- [What is Amazon RDS? - Amazon RDS User Guide](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/Welcome.html)
- [AWS CLI: rds commands](https://docs.aws.amazon.com/cli/latest/reference/rds/)
