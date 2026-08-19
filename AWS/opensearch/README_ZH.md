# Amazon OpenSearch Service - Runbook 与参考

> 事实核对时间（对照 AWS 官方文档）：2026-08-19

## 概述

Amazon OpenSearch Service 是托管的 OpenSearch 集群服务，负责部署、运维和扩容。域（domain）等同于托管的 OpenSearch 集群。它支持 OpenSearch（当前版本含 3.x）和旧版 Elasticsearch OSS（最高 7.10），用于日志分析、应用监控、点击流分析和全文搜索。

## 核心概念

- **域（Domain）**：配置了实例类型、数量、存储和安全设置的集群。
- **数据节点**：存储和查询数据的 EC2 实例；域最多支持 1,002 个数据节点、25 PB 挂载存储。
- **专用主节点**：承担集群管理任务，提升稳定性。
- **UltraWarm 与冷存储**：面向只读数据的低成本层级（基于 S3）。
- **OpenSearch Dashboards**：内置可视化和查询工作台。
- **摄取管道（Ingestion pipelines）**：索引前转换数据（OpenSearch Ingestion）。
- **安全**：IAM、VPC、静态和节点间加密、Dashboards 的 Cognito/基础认证/SAML、细粒度访问控制。
- **自动快照**：每日快照到 S3，用于备份和恢复。
- **Serverless**：OpenSearch Serverless collection，按 OCU 伸缩。

## 常用操作（AWS CLI）

```bash
# 创建域
aws opensearch create-domain --domain-name logs-prod \
  --engine-version OpenSearch_3.1 \
  --cluster-config InstanceType=m5.large.search,InstanceCount=3,DedicatedMasterEnabled=true \
  --ebs-options EBSEnabled=true,VolumeSize=100,VolumeType=gp3 \
  --encryption-at-rest-options Enabled=true \
  --node-to-node-encryption-options Enabled=true

# 列出和查看域
aws opensearch list-domain-names
aws opensearch describe-domain --domain-name logs-prod
aws opensearch describe-domains --domain-names logs-prod

# 扩容
aws opensearch update-domain-config --domain-name logs-prod \
  --cluster-config InstanceType=m5.large.search,InstanceCount=5

# 快照仓库
aws opensearch create-package --package-name backup-repo --package-type SNAPSHOT \
  --package-source S3BucketName=snapshots-bucket,S3Key=repo

# 删除
aws opensearch delete-domain --domain-name logs-prod
```

## 最佳实践

- 旧数据或只读数据用 UltraWarm/冷存储层级控制成本；热数据留在数据节点。
- 生产环境至少 3 个数据节点加专用主节点，节点跨可用区分布。
- 启用静态加密、节点间加密，并对域强制 HTTPS。
- 生产域放 VPC；Dashboards 用 Cognito/SAML，索引用细粒度访问控制。
- 除自动快照外定期手动快照到 S3，并演练恢复。
- 用 CloudWatch 监控（集群状态、JVM 内存压力、CPU），集群 `red` 状态立即告警。
- 升级到标准支持期的 OpenSearch 版本；旧版本扩展支持会收费。
- 用 Lambda/摄取管道从 Kinesis、Firehose、CloudWatch Logs 加载流数据。

## 故障排查

| 症状 | 检查与处理 |
|---|---|
| 集群状态 `red` | 检查未分配分片；修复磁盘空间、节点数或副本设置。 |
| JVM 内存压力高 | 扩大实例、加节点，或降低索引复杂度。 |
| 写入被拒绝 | 检查集群容量和批量请求大小；扩容或限流。 |
| 无法访问 Dashboards | 检查 Cognito/基础认证/SAML 配置和 VPC 安全组。 |
| 快照恢复失败 | 确认快照仓库 IAM 角色和 S3 桶权限。 |
| 查询慢 | 检查 mapping、分片数量/大小，使用匹配查询负载的索引模式。 |

## 配额

数据节点（最多 1,002）、挂载存储（最多 25 PB）、每账号域数和 Serverless OCU 容量受配额限制。以 Service Quotas 控制台当前值为准。

## 官方参考

- [什么是 Amazon OpenSearch Service？](https://docs.aws.amazon.com/opensearch-service/latest/developerguide/what-is.html)
- [Amazon OpenSearch Service 配额](https://docs.aws.amazon.com/opensearch-service/latest/developerguide/limits.html)
- [Amazon OpenSearch Service 定价](https://aws.amazon.com/opensearch-service/pricing/)
- [AWS CLI：opensearch 命令](https://docs.aws.amazon.com/cli/latest/reference/opensearch/)
