# Amazon DocumentDB - Runbook 与参考

> 事实核对时间（对照 AWS 官方文档）：2026-08-19

## 概述

Amazon DocumentDB（兼容 MongoDB）是快速、可靠、完全托管的文档数据库。你可以继续使用 MongoDB 的应用代码、驱动和工具。它把存储与计算分离：集群卷在三个可用区间复制 6 份，并随数据增长自动扩容。

## 核心概念

- **集群**：一个主实例加最多 15 个副本，共享集群卷；所有实例都能读。
- **弹性集群（Elastic clusters）**：支持每秒数百万次读写和 PB 级存储的部署类型。
- **存储增长**：存储自动按 10 GB 增量增长；引擎 8.0+ 最大 256 TiB（更早引擎 128 TiB）。
- **读取端点（Reader endpoint）**：跨副本负载均衡读请求的稳定端点。
- **备份**：自动、连续、增量备份到 S3，支持时间点恢复（最近 5 分钟内）；保留期最长 35 天。
- **加密**：KMS 加密存储、备份、快照和副本。
- **MongoDB 兼容性**：使用 MongoDB 驱动和 MongoDB shell 连接。

## 常用操作（AWS CLI）

```bash
# 创建集群
aws docdb create-db-cluster --db-cluster-identifier app-docdb \
  --engine docdb --engine-version 5.0.0 \
  --master-username adminuser --master-user-password <password> \
  --backup-retention-period 7 --storage-encrypted

# 创建实例（主实例）
aws docdb create-db-instance --db-instance-identifier app-docdb-1 \
  --db-cluster-identifier app-docdb --db-instance-class db.r6g.large --engine docdb

# 添加副本做读扩展
aws docdb create-db-instance --db-instance-identifier app-docdb-2 \
  --db-cluster-identifier app-docdb --db-instance-class db.r6g.large --engine docdb

# 查看
aws docdb describe-db-clusters
aws docdb describe-db-instances

# 备份和恢复
aws docdb create-db-cluster-snapshot --db-cluster-identifier app-docdb \
  --db-cluster-snapshot-identifier app-docdb-backup
aws docdb restore-db-cluster-from-snapshot \
  --db-cluster-identifier app-docdb-restored --snapshot-identifier app-docdb-backup \
  --engine docdb
```

## 最佳实践

- 合理配置主实例，副本放在不同可用区做读扩展和故障转移；应用使用读取端点。
- 启用自动备份并按 RPO 设置保留期；演练 PITR 恢复。
- 索引匹配 MongoDB 查询模式，用 `explain` 验证。
- 集群放 VPC，安全组只放行应用子网；启用 TLS。
- 用 CloudWatch（CPU、连接数、存储、副本延迟）和 DocumentDB 事件监控。
- 写入/读取规模极大时评估弹性集群，而不是实例型集群。
- 引擎升级和实例规格变更先在预发集群验证。

## 故障排查

| 症状 | 检查与处理 |
|---|---|
| 连接失败 | 检查安全组、TLS 设置，以及客户端是否使用集群端点（端口 27017）。 |
| 读延迟 | 加副本并使用读取端点；检查副本延迟。 |
| 存储打满 | DocumentDB 自动扩容；若到引擎上限，评估弹性集群或归档数据。 |
| 查询慢 | 用 `explain` 检查索引和查询模式；CPU 瓶颈时调整实例规格。 |
| PITR 恢复失败 | 确认保留期已配置且集群启用了自动备份。 |

## 配额

每集群最多 15 个副本；存储最高 256 TiB（引擎 8.0+）或 128 TiB（更早引擎）；备份保留最长 35 天。集群和实例数有每账号配额。以 Service Quotas 控制台当前值为准。

## 官方参考

- [什么是 Amazon DocumentDB（兼容 MongoDB）？](https://docs.aws.amazon.com/documentdb/latest/developerguide/what-is.html)
- [Amazon DocumentDB 配额](https://docs.aws.amazon.com/documentdb/latest/developerguide/limits.html)
- [Amazon DocumentDB 定价](https://aws.amazon.com/documentdb/pricing/)
- [AWS CLI：docdb 命令](https://docs.aws.amazon.com/cli/latest/reference/docdb/)
