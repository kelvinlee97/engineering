---
type: Service
title: Amazon RDS
description: AWS's managed relational databases, where Multi-AZ standbys give failover and read replicas give read scaling.
tags: [aws, database]
sources:
  - id: aws-rds
    resource: https://github.com/kelvinlee97/engineering/blob/main/AWS/rds/README.md
    title: "Amazon RDS - Runbook & Reference"
    author: human:kelvinlee97
    last_modified: 2026-09-24T14:48:10Z
generated: { by: claude-code/wiki-v1, at: 2026-09-25T07:00:00Z }
status: draft
---

Amazon Relational Database Service (RDS) runs Db2, MariaDB, SQL Server, MySQL, Oracle, and PostgreSQL with AWS handling backups, patching, and failure recovery. It has two independent scaling axes: Multi-AZ adds a synchronous standby for failover, read replicas add asynchronous copies for reads, and writes always go to the primary.[^aws-rds]

## Concepts

- Instance classes: general purpose `db.m*`, memory optimized `db.r*`/`db.x*`/`db.z*`, compute `db.c*`, burstable `db.t*`.[^aws-rds]
- Storage: General Purpose and Provisioned IOPS SSD; magnetic is deprecated, with no restore to magnetic after July 1, 2026.[^aws-rds]
- Automated backups with point-in-time recovery, plus manual snapshots.[^aws-rds]
- VPC and security groups, IAM authentication, KMS encryption at rest, TLS in transit.[^aws-rds]

## Troubleshooting

| Symptom | Check |
| --- | --- |
| Connection refused | SG source rules, routing, public accessibility |
| Storage full | Add storage; find growth |
| Failover occurred | RDS events, replica lag, primary load |
| Slow queries | Performance Insights, indexes, parameter groups |
| Replica lag | Replica class, write load, long transactions |

As tabled in the note.[^aws-rds] Default quota: 40 DB instances per Region.[^aws-rds] See [AWS database choices](database-choices.md).

## Related

- Source: [Amazon RDS - Runbook & Reference](../../sources/aws-rds.md)

[^aws-rds]: Amazon RDS - Runbook & Reference
