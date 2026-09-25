---
type: Service
title: Amazon ElastiCache
description: AWS's managed in-memory cache running Valkey, Redis OSS, or Memcached, serverless or on chosen nodes.
tags: [aws, database, cache]
sources:
  - id: aws-elasticache
    resource: https://github.com/kelvinlee97/engineering/blob/main/AWS/elasticache/README.md
    title: "Amazon ElastiCache - Runbook & Reference"
    author: human:kelvinlee97
    last_modified: 2026-09-24T14:48:10Z
generated: { by: claude-code/wiki-v1, at: 2026-09-25T07:00:00Z }
status: draft
---

ElastiCache is a managed in-memory data store and cache, used for query caching, sessions, leaderboards, rate limiting, and pub/sub. It runs Valkey, Redis OSS, or Memcached.[^aws-elasticache]

| Option | Detail |
| --- | --- |
| Serverless | Highly available cache in under a minute, scaling automatically (Valkey 7.2+, Memcached 1.6.22+, Redis OSS 7.1) |
| Node-based | You choose node type, count, AZs, cluster mode, patch windows |

As tabled in the note.[^aws-elasticache]

## Practices

- Treat the cache as disposable and rebuildable from the database, never the source of truth.[^aws-elasticache]
- Pick an eviction policy such as `allkeys-lru`; Multi-AZ with automatic failover; TLS and encryption at rest in private subnets.[^aws-elasticache]
- Alarm on evictions and swap usage.[^aws-elasticache]

## Troubleshooting

| Symptom | Check |
| --- | --- |
| High evictions | Memory, maxmemory policy, nodes or shards |
| Miss spike | Expiry, key design, cold start |
| Failover not working | Multi-AZ and auto failover enabled, replicas healthy |
| Slow | Hot keys, large values, latency |

As tabled in the note.[^aws-elasticache] See [AWS database choices](database-choices.md).

## Related

- Source: [Amazon ElastiCache - Runbook & Reference](../../sources/aws-elasticache.md)

[^aws-elasticache]: Amazon ElastiCache - Runbook & Reference
