# AWS Database Migration Service（DMS）- Runbook 与参考

> 事实核对时间（对照 AWS 官方文档）：2026-08-19

## 概述

AWS Database Migration Service（AWS DMS）用于把关系数据库、数据仓库、NoSQL 数据库和其他数据存储迁移到 AWS，或在云与本地之间迁移。它支持一次性迁移和持续复制（保持源与目标同步），并提供 Fleet Advisor（发现）和 Schema Conversion（引擎转换）。

## 核心概念

- **复制实例（Replication instance）**：运行迁移任务的计算资源。
- **端点（Endpoints）**：源和目标连接定义（引擎、主机、凭据、VPC）。
- **复制任务（Replication task）**：调度的工作单元（全量加载、持续复制/CDC，或两者）。
- **Schema 转换**：DMS Schema Conversion 或可下载的 AWS Schema Conversion Tool（AWS SCT）把 schema/代码转换为目标引擎。
- **Fleet Advisor**：发现并盘点本地数据库服务器，用于规划迁移。
- **DMS Serverless**：按需运行复制实例，无需预置容量。
- **数据验证（Data validation）**：比较源和目标数据，发现不一致。
- **异构迁移**：DMS 支持不同引擎之间的迁移（如 Oracle 到 Aurora PostgreSQL）。

## 常用操作（AWS CLI）

```bash
# 创建复制实例
aws dms create-replication-instance --replication-instance-identifier mig1 \
  --replication-instance-class dms.t3.medium --engine-version 3.5.3 \
  --allocated-storage 50 --no-publicly-accessible

# 创建源和目标端点
aws dms create-endpoint --endpoint-identifier src-oracle \
  --endpoint-type source --engine-name oracle \
  --server-name db01.example --port 1521 --username app \
  --password <password> --database-name ORCL
aws dms create-endpoint --endpoint-identifier tgt-aurora \
  --endpoint-type target --engine-name aurora-postgresql \
  --server-name cluster.cluster-xxxx.us-east-1.rds.amazonaws.com \
  --port 5432 --username app --password <password> --database-name app

# 创建并启动任务（全量 + CDC）
aws dms create-replication-task --replication-task-identifier full-cdc \
  --source-endpoint-arn <src-arn> --target-endpoint-arn <tgt-arn> \
  --replication-instance-arn <instance-arn> \
  --migration-type full-load-and-cdc \
  --table-mappings file://table-mappings.json
aws dms start-replication-task --replication-task-arn <task-arn> \
  --start-replication-task-type start-replication

# 监控和停止
aws dms describe-replication-tasks
aws dms stop-replication-task --replication-task-arn <task-arn>
```

## 最佳实践

- 尽早用 Fleet Advisor 和 Schema Conversion 评估迁移规模，并在割接前完成 schema 转换。
- 用有代表性的数据集先做全量测试；用 DMS 数据验证核对数据。
- 复制实例放私有子网，安全组只放行两个端点所需流量。
- 用 CDC 实现最小停机割接：停止应用写入、确认延迟归零后再切换。
- 负载波动大或低频迁移用 DMS Serverless。
- 复制实例和端点用 KMS 加密，支持处启用 SSL/TLS。
- 割接后立即对目标做备份，并保留迁移日志用于审计。

## 故障排查

| 症状 | 检查与处理 |
|---|---|
| 任务卡在 failed | 查看任务日志、端点连通性和凭据/网络路由。 |
| CDC 延迟增长 | 检查源端保留日志（如 Oracle archive log）和复制实例容量。 |
| 数据不一致 | 运行数据验证，检查表映射中的转换规则。 |
| 无法连接源端 | 检查安全组/NACL、端点设置和源端防火墙。 |
| LOB/CLOB 问题 | 按大对象情况配置合适的 LOB 模式。 |

## 配额

复制实例、端点、任务和并发连接数有每账号配额。以 Service Quotas 控制台当前值为准。

## 官方参考

- [什么是 AWS Database Migration Service？](https://docs.aws.amazon.com/dms/latest/userguide/Welcome.html)
- [AWS DMS 服务配额](https://docs.aws.amazon.com/dms/latest/userguide/CHAP_Limits.html)
- [AWS Database Migration Service 定价](https://aws.amazon.com/dms/pricing/)
- [AWS CLI：dms 命令](https://docs.aws.amazon.com/cli/latest/reference/dms/)
