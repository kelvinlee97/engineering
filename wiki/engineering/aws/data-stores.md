---
type: Comparison
title: AWS data stores
description: 'Choosing an AWS data store, and the main options: RDS, DynamoDB, ElastiCache, and S3.'
tags:
- aws
- databases
- storage
aliases:
- engineering/aws/database-choices
- engineering/aws/rds
- engineering/aws/dynamodb
- engineering/aws/elasticache
- engineering/aws/s3
sources:
- id: aws-rds
  resource: https://github.com/kelvinlee97/engineering/blob/main/AWS/rds/README.md
  title: Amazon RDS - Runbook & Reference
  author: human:kelvinlee97
  last_modified: 2026-09-24T14:48:10Z
- id: aws-dynamodb
  resource: https://github.com/kelvinlee97/engineering/blob/main/AWS/dynamodb/README.md
  title: Amazon DynamoDB - Runbook & Reference
  author: human:kelvinlee97
  last_modified: 2026-09-24T14:48:10Z
- id: aws-elasticache
  resource: https://github.com/kelvinlee97/engineering/blob/main/AWS/elasticache/README.md
  title: Amazon ElastiCache - Runbook & Reference
  author: human:kelvinlee97
  last_modified: 2026-09-24T14:48:10Z
- id: aws-s3
  resource: https://github.com/kelvinlee97/engineering/blob/main/AWS/s3/README.md
  title: Amazon S3 - Runbook & Reference
  author: human:kelvinlee97
  last_modified: 2026-09-24T14:48:10Z
generated: { by: claude-code/wiki-v1, at: 2026-09-25T12:00:00Z }
status: draft
---
AWS has a managed store for most data shapes. This page starts with how to choose, then covers Amazon RDS for relational data, DynamoDB for NoSQL access by partition key, ElastiCache for in-memory caching, and S3 for objects.

## Choosing a data store

The three core AWS data services fill different roles.

| | [RDS](#amazon-rds) | [DynamoDB](#amazon-dynamodb) | [ElastiCache](#amazon-elasticache) |
| --- | --- | --- | --- |
| Model | Relational engines | Key-value and document | In-memory Valkey, Redis OSS, Memcached |
| Scaling | Read replicas; writes on the primary | Partition keys; on-demand or provisioned | Shards in cluster mode, or serverless |
| Availability | Multi-AZ synchronous standby[^aws-rds] | Global tables, 99.999% | Multi-AZ automatic failover |
| Source of truth | Yes | Yes | No: treat as disposable[^aws-elasticache] |

DynamoDB has its own in-memory cache, DAX, so it doesn't usually need ElastiCache in front of it.[^aws-dynamodb]

## Amazon RDS

Amazon Relational Database Service (RDS) runs Db2, MariaDB, SQL Server, MySQL, Oracle, and PostgreSQL with AWS handling backups, patching, and failure recovery. It has two independent scaling axes: Multi-AZ adds a synchronous standby for failover, read replicas add asynchronous copies for reads, and writes always go to the primary.[^aws-rds]

### Concepts

- Instance classes: general purpose `db.m*`, memory optimized `db.r*`/`db.x*`/`db.z*`, compute `db.c*`, burstable `db.t*`.
- Storage: General Purpose and Provisioned IOPS SSD; magnetic is deprecated, with no restore to magnetic after July 1, 2026.
- Automated backups with point-in-time recovery, plus manual snapshots.
- VPC and security groups, IAM authentication, KMS encryption at rest, TLS in transit.[^aws-rds]

### Troubleshooting

| Symptom | Check |
| --- | --- |
| Connection refused | SG source rules, routing, public accessibility |
| Storage full | Add storage; find growth |
| Failover occurred | RDS events, replica lag, primary load |
| Slow queries | Performance Insights, indexes, parameter groups |
| Replica lag | Replica class, write load, long transactions |

As tabled in the note. Default quota: 40 DB instances per Region.[^aws-rds] See [AWS database choices](#choosing-a-data-store).

## Amazon DynamoDB

DynamoDB is a serverless NoSQL database with single-digit millisecond performance at any scale and nothing to patch. Items are distributed by partition key (plus an optional sort key), so tables are designed around access patterns.[^aws-dynamodb]

### Concepts

- On-demand capacity (per request, scales to zero) or provisioned RCU/WCU with auto scaling.
- Global and local secondary indexes; Streams for change data capture; ACID transactions.
- Global tables: multi-active replication across Regions with 99.999% availability.
- DAX in-memory cache for up to 10x read performance.
- Point-in-time recovery up to 35 days; IAM-only access with encryption at rest by default.[^aws-dynamodb]

### Practices

- `query` rather than `scan`; spread partition keys to avoid hot partitions; TTL to expire data.[^aws-dynamodb]

### Troubleshooting and limits

| Symptom | Check |
| --- | --- |
| `ProvisionedThroughputExceededException` | On-demand or more capacity, backoff, hot keys |
| Slow `scan` | A GSI and `query` |
| Item too large | Limit is 400 KB; store the payload in S3 |

As tabled in the note. Per-partition throughput is 3,000 RCU and 1,000 WCU.[^aws-dynamodb] See [AWS database choices](#choosing-a-data-store).

## Amazon ElastiCache

ElastiCache is a managed in-memory data store and cache, used for query caching, sessions, leaderboards, rate limiting, and pub/sub. It runs Valkey, Redis OSS, or Memcached.

| Option | Detail |
| --- | --- |
| Serverless | Highly available cache in under a minute, scaling automatically (Valkey 7.2+, Memcached 1.6.22+, Redis OSS 7.1) |
| Node-based | You choose node type, count, AZs, cluster mode, patch windows |

As tabled in the note.[^aws-elasticache]

### Practices

- Treat the cache as disposable and rebuildable from the database, never the source of truth.
- Pick an eviction policy such as `allkeys-lru`; Multi-AZ with automatic failover; TLS and encryption at rest in private subnets.
- Alarm on evictions and swap usage.[^aws-elasticache]

### Troubleshooting

| Symptom | Check |
| --- | --- |
| High evictions | Memory, maxmemory policy, nodes or shards |
| Miss spike | Expiry, key design, cold start |
| Failover not working | Multi-AZ and auto failover enabled, replicas healthy |
| Slow | Hot keys, large values, latency |

As tabled in the note.[^aws-elasticache] See [AWS database choices](#choosing-a-data-store).

## Amazon S3

Amazon S3 stores any amount of data as objects in buckets, with strong read-after-write consistency for PUT and DELETE in all Regions. Lifecycle rules move objects from frequent-access storage toward archive tiers, or expire them.[^aws-s3]

### Buckets and storage classes

| Bucket type | Note |
| --- | --- |
| General purpose | Recommended default; globally unique names; private by default |
| Directory | Low latency and data residency; public access cannot be enabled |
| Table | Apache Iceberg tabular data |
| Vector | Vector data |

| Access pattern | Classes |
| --- | --- |
| Frequent | Standard, Express One Zone |
| Infrequent | Standard-IA, One Zone-IA |
| Archive | Glacier Instant Retrieval, Flexible Retrieval, Deep Archive |
| Unknown | Intelligent-Tiering across four tiers |

As listed in the note.[^aws-s3]

### Access and protection

- Private by default with Block Public Access on; prefer IAM policies, bucket policies, and access points over ACLs, which are disabled by default.
- Versioning, Object Lock (WORM), replication, and SSE-S3 or SSE-KMS encryption.
- Storage Lens (60+ metrics), Inventory, CloudTrail, and server access logs.[^aws-s3]

### Troubleshooting and quotas

| Symptom | Check |
| --- | --- |
| `AccessDenied` | Identity, bucket, and access point policies, Block Public Access, SCP/RCP |
| `404 NoSuchKey` | Key path, bucket Region, version ID |
| Cost growth | Storage Lens, lifecycle rules, incomplete multipart uploads |
| Name taken | General purpose names are global |

As tabled in the note. Defaults: 100 general purpose buckets per account (adjustable), 100 directory buckets, 10 table buckets per Region with up to 10,000 tables each, and objects up to 5 TB in a single PUT.[^aws-s3]

## Related
- [Specialized databases](specialized-databases.md): DocumentDB, Neptune, QLDB, and Managed Blockchain.
- [Analytics](analytics.md): querying and warehousing data.
- [Storage and migration](storage-and-migration.md): backup, file systems, and moving data into AWS.
- [Domain index](index.md): other pages in this domain.

[^aws-rds]: [Amazon RDS - Runbook & Reference](../../sources/aws-rds.md), [original](https://github.com/kelvinlee97/engineering/blob/main/AWS/rds/README.md)
[^aws-dynamodb]: [Amazon DynamoDB - Runbook & Reference](../../sources/aws-dynamodb.md), [original](https://github.com/kelvinlee97/engineering/blob/main/AWS/dynamodb/README.md)
[^aws-elasticache]: [Amazon ElastiCache - Runbook & Reference](../../sources/aws-elasticache.md), [original](https://github.com/kelvinlee97/engineering/blob/main/AWS/elasticache/README.md)
[^aws-s3]: [Amazon S3 - Runbook & Reference](../../sources/aws-s3.md), [original](https://github.com/kelvinlee97/engineering/blob/main/AWS/s3/README.md)
