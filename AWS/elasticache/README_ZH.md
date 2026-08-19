# Amazon ElastiCache - Runbook 与参考

> 事实核对时间（对照 AWS 官方文档）：2026-08-19

## 概述

Amazon ElastiCache 是完全托管的内存数据存储和缓存服务，支持 Valkey、Redis OSS 和 Memcached 引擎，提供 Serverless 和节点式两种部署方式，常用于缓存、会话存储和实时数据访问。

## 部署选项

| 选项 | 说明 |
|---|---|
| ElastiCache Serverless | 一分钟内创建高可用缓存，容量自动伸缩（兼容 Valkey 7.2+、Memcached 1.6.22+、Redis OSS 7.1） |
| 节点式集群 | 选择节点类型、节点数、可用区分布、集群模式和维护窗口，控制粒度更细 |

## 核心概念

- **引擎**：Valkey、Redis OSS 或 Memcached；Redis 兼容引擎支持数据结构、pub/sub 和 Lua 脚本。
- **复制组 / 集群**：主节点加副本，用于读扩展和故障转移。
- **集群模式**：跨分片水平扩展（Redis Cluster API）。
- **多 AZ**：自动故障转移到其他可用区的副本。
- **持久化**：Valkey 节点可把数据写入跨多 AZ 的分布式事务日志，副本可独立恢复。
- **典型用途**：数据库查询缓存、会话存储、排行榜/限流、消息 pub/sub。

## 常用操作（AWS CLI）

```bash
# 创建 Serverless 缓存
aws elasticache create-serverless-cache --serverless-cache-name app-cache --engine valkey

# 创建节点式 Redis 复制组
aws elasticache create-replication-group --replication-group-id app-cache \
  --replication-group-description "App cache" --engine redis \
  --cache-node-type cache.t4g.micro --num-cache-clusters 2 \
  --multi-az-enabled --automatic-failover-enabled

# 创建 Memcached 集群
aws elasticache create-cache-cluster --cache-cluster-id sessions \
  --engine memcached --cache-node-type cache.t4g.micro --num-cache-nodes 2

# 查看
aws elasticache describe-serverless-caches
aws elasticache describe-replication-groups
aws elasticache describe-cache-clusters

# 调整 Serverless 缓存限额
aws elasticache update-serverless-cache --serverless-cache-name app-cache \
  --cache-usage-limits '{"DataStorage":{"Maximum":50,"Unit":"GB"},"ECPUPerSecond":{"Maximum":10000}}'
```

## 最佳实践

- 负载波动大或想快速上手用 Serverless；容量可预测、需要精细控制用节点式集群。
- 设置与访问模式匹配的逐出策略（如 `maxmemory-policy allkeys-lru`）。
- 生产缓存启用多 AZ 和自动故障转移，并定期演练故障转移。
- 把缓存视为可重建的：冷启动时从数据库重建，而不是当作唯一数据源。
- 启用传输 TLS 和静态加密；缓存放私有子网。
- 用 CloudWatch 监控 CPU、内存、逐出数和连接数；对逐出率和 swap 用量设置告警。
- 在维护窗口打补丁，升级引擎先在预发缓存验证。

## 故障排查

| 症状 | 检查与处理 |
|---|---|
| 逐出率高 | 增加内存、调整 maxmemory 策略，或加节点/分片。 |
| 缓存未命中激增 | 检查过期/逐出策略、应用 key 设计和冷启动行为。 |
| 故障转移不生效 | 确认多 AZ 和自动故障转移已启用，副本健康。 |
| 连接被拒 | 检查安全组、TLS 设置和客户端配置。 |
| 操作慢 | 检查热 key、大 value 和网络延迟；规模化用集群模式。 |

## 配额

Serverless 缓存、节点式集群、节点和分片数量有每账号配额；引擎版本和节点类型因区域而异。以 Service Quotas 控制台当前值为准。

## 官方参考

- [什么是 Amazon ElastiCache？](https://docs.aws.amazon.com/AmazonElastiCache/latest/dg/WhatIs.html)
- [Amazon ElastiCache 服务配额](https://docs.aws.amazon.com/AmazonElastiCache/latest/dg/WhatIs.html#limits)
- [Amazon ElastiCache 定价](https://aws.amazon.com/elasticache/pricing/)
- [AWS CLI：elasticache 命令](https://docs.aws.amazon.com/cli/latest/reference/elasticache/)
