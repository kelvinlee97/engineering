---
type: Comparison
title: AWS database choices
description: RDS for relational workloads, DynamoDB for key-value access at scale, and ElastiCache as a disposable in-memory layer in front of either.
tags: [aws, database]
sources:
  - id: aws-rds
    resource: https://github.com/kelvinlee97/engineering/blob/main/AWS/rds/README.md
    title: "Amazon RDS - Runbook & Reference"
    author: human:kelvinlee97
    last_modified: 2026-09-24T14:48:10Z
  - id: aws-dynamodb
    resource: https://github.com/kelvinlee97/engineering/blob/main/AWS/dynamodb/README.md
    title: "Amazon DynamoDB - Runbook & Reference"
    author: human:kelvinlee97
    last_modified: 2026-09-24T14:48:10Z
  - id: aws-elasticache
    resource: https://github.com/kelvinlee97/engineering/blob/main/AWS/elasticache/README.md
    title: "Amazon ElastiCache - Runbook & Reference"
    author: human:kelvinlee97
    last_modified: 2026-09-24T14:48:10Z
generated: { by: claude-code/wiki-v1, at: 2026-09-25T07:00:00Z }
status: draft
---

The three core AWS data services fill different roles.

| | [RDS](rds.md) | [DynamoDB](dynamodb.md) | [ElastiCache](elasticache.md) |
| --- | --- | --- | --- |
| Model | Relational engines[^aws-rds] | Key-value and document[^aws-dynamodb] | In-memory Valkey, Redis OSS, Memcached[^aws-elasticache] |
| Scaling | Read replicas; writes on the primary[^aws-rds] | Partition keys; on-demand or provisioned[^aws-dynamodb] | Shards in cluster mode, or serverless[^aws-elasticache] |
| Availability | Multi-AZ synchronous standby[^aws-rds] | Global tables, 99.999%[^aws-dynamodb] | Multi-AZ automatic failover[^aws-elasticache] |
| Source of truth | Yes | Yes | No: treat as disposable[^aws-elasticache] |

DynamoDB has its own in-memory cache, DAX, so it doesn't usually need ElastiCache in front of it.[^aws-dynamodb]

## Related

- Source: [Amazon RDS - Runbook & Reference](../../sources/aws-rds.md)
- Source: [Amazon DynamoDB - Runbook & Reference](../../sources/aws-dynamodb.md)
- Source: [Amazon ElastiCache - Runbook & Reference](../../sources/aws-elasticache.md)

[^aws-rds]: Amazon RDS - Runbook & Reference
[^aws-dynamodb]: Amazon DynamoDB - Runbook & Reference
[^aws-elasticache]: Amazon ElastiCache - Runbook & Reference
