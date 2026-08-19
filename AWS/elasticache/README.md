# Amazon ElastiCache - Runbook & Reference

> Facts verified against official AWS documentation: 2026-08-19

## Overview

Amazon ElastiCache is a fully managed in-memory data store and cache service. It supports the Valkey, Redis OSS, and Memcached engines in either serverless or node-based deployments, and is commonly used for caching, session storage, and real-time data access.

## Deployment options

| Option | Description |
|---|---|
| ElastiCache Serverless | Create a highly available cache in under a minute; capacity scales automatically (compatible with Valkey 7.2+, Memcached 1.6.22+, Redis OSS 7.1) |
| Node-based cluster | Choose node type, node count, AZ placement, cluster mode, and patch windows for fine-grained control |

## Key concepts

- **Engine**: Valkey, Redis OSS, or Memcached; Redis-compatible engines add data structures, pub/sub, and Lua scripting.
- **Replication group / cluster**: primary node(s) with replicas for reads and failover.
- **Cluster mode**: horizontal scaling across shards (Redis Cluster API).
- **Multi-AZ**: automatic failover to a replica in another Availability Zone.
- **Durability**: Valkey nodes can persist data in a distributed Multi-AZ transactional log so replicas recover independently.
- **Use cases**: database query caching, session stores, leaderboards/rate limiting, message pub/sub.

## Common operations (AWS CLI)

```bash
# Create a serverless cache
aws elasticache create-serverless-cache --serverless-cache-name app-cache --engine valkey

# Create a node-based Redis replication group
aws elasticache create-replication-group --replication-group-id app-cache \
  --replication-group-description "App cache" --engine redis \
  --cache-node-type cache.t4g.micro --num-cache-clusters 2 \
  --multi-az-enabled --automatic-failover-enabled

# Create a Memcached cluster
aws elasticache create-cache-cluster --cache-cluster-id sessions \
  --engine memcached --cache-node-type cache.t4g.micro --num-cache-nodes 2

# Inspect
aws elasticache describe-serverless-caches
aws elasticache describe-replication-groups
aws elasticache describe-cache-clusters

# Scale a serverless cache
aws elasticache update-serverless-cache --serverless-cache-name app-cache \
  --cache-usage-limits '{"DataStorage":{"Maximum":50,"Unit":"GB"},"ECPUPerSecond":{"Maximum":10000}}'
```

## Best practices

- Choose ElastiCache Serverless for variable workloads and fast onboarding; use node-based clusters for predictable capacity and fine control.
- Set an eviction policy (for example, `maxmemory-policy allkeys-lru`) that matches your data access pattern.
- Use Multi-AZ with automatic failover for production caches; test failover regularly.
- Treat the cache as disposable: rebuild it from the database on cold start rather than relying on it as the source of truth.
- Use TLS in transit and encryption at rest; isolate in private subnets.
- Monitor CPU, memory, evictions, and connection metrics in CloudWatch; set alarms on eviction rate and swap usage.
- Patch during maintenance windows and upgrade engines in a staging cache first.

## Troubleshooting

| Symptom | Checks and fixes |
|---|---|
| High evictions | Increase memory, adjust maxmemory policy, or add nodes/shards. |
| Cache misses spike | Check expiration/eviction policy, application key design, and cold-start behavior. |
| Failover not working | Verify Multi-AZ and automatic failover are enabled and replicas are healthy. |
| Connection refused | Check security groups, TLS settings, and client configuration. |
| Slow operations | Check for hot keys, large values, and network latency; use clustering for scale. |

## Limits

Serverless caches, node-based clusters, nodes, and shards have per-account quotas; engine versions and cache node types vary by Region. See the Service Quotas console for current values.

## Official references

- [What is Amazon ElastiCache?](https://docs.aws.amazon.com/AmazonElastiCache/latest/dg/WhatIs.html)
- [Amazon ElastiCache service quotas](https://docs.aws.amazon.com/AmazonElastiCache/latest/dg/WhatIs.html#limits)
- [Amazon ElastiCache pricing](https://aws.amazon.com/elasticache/pricing/)
- [AWS CLI: elasticache commands](https://docs.aws.amazon.com/cli/latest/reference/elasticache/)
