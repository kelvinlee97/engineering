# Amazon DynamoDB - Runbook 与参考

> 事实核对时间（对照 AWS 官方文档）：2026-08-19

## 概述

Amazon DynamoDB 是服务化、全托管的 NoSQL 数据库，任意规模下都有个位数毫秒级性能。支持键值（key-value）和文档两种数据模型，无需预置服务器、打补丁或维护。

## 核心概念

- **表、项、属性**：表存储项；每项有若干属性。**分区键**（可加排序键）决定数据分布。
- **容量模式**：按需（按请求付费，可缩到零）或预置（RCU/WCU + 自动扩缩）。
- **二级索引**：全局（GSI）和本地（LSI）二级索引，支持用其他键查询。
- **流（Streams）**：DynamoDB Streams 和 Kinesis Data Streams for DynamoDB 记录项级变更（CDC）。
- **全局表**：跨区域多活复制，可用性 99.999%。
- **事务**：单表或多表 ACID。
- **DAX**：内存缓存，读性能最高提升 10 倍。
- **备份**：时间点恢复（最长 35 天）和按需备份；支持 AWS Backup。
- **安全**：只用 IAM（无用户名密码），默认静态加密（KMS），支持细粒度访问控制。

## 常用操作（AWS CLI）

```bash
# 创建表（按需模式）
aws dynamodb create-table --table-name orders \
  --attribute-definitions AttributeName=id,AttributeType=S \
  --key-schema AttributeName=id,KeyType=HASH \
  --billing-mode PAY_PER_REQUEST

# CRUD
aws dynamodb put-item --table-name orders --item '{"id":{"S":"1001"},"amount":{"N":"250"}}'
aws dynamodb get-item --table-name orders --key '{"id":{"S":"1001"}}'
aws dynamodb query --table-name orders --key-condition-expression "id = :id" \
  --expression-attribute-values '{":id":{"S":"1001"}}'
aws dynamodb update-item --table-name orders --key '{"id":{"S":"1001"}}' \
  --update-expression "SET #a = :a" --expression-attribute-names '{"#a":"amount"}' \
  --expression-attribute-values '{":a":{"N":"300"}}'
aws dynamodb delete-item --table-name orders --key '{"id":{"S":"1001"}}'

# 管理
aws dynamodb list-tables
aws dynamodb describe-table --table-name orders
aws dynamodb update-table --table-name orders --billing-mode PROVISIONED \
  --provisioned-throughput ReadCapacityUnits=5,WriteCapacityUnits=5

# 备份
aws dynamodb create-backup --table-name orders --backup-name orders-backup
aws dynamodb restore-table-to-point-in-time --source-table-name orders \
  --target-table-name orders-restored --use-latest-restorable-time
```

## 最佳实践

- 围绕**访问模式**设计表（合适时用单表设计）；用 `query` 而不是 `scan`。
- 分散分区键避免热点分区；用排序键实现排序。
- 负载波动用**按需模式**；稳定负载用预置 + 自动扩缩。
- 开启**时间点恢复**；用 **TTL** 自动过期数据。
- 读密集、延迟敏感场景用 **DAX**。
- 用**细粒度 IAM**（属性级条件）和资源策略控制访问。

## 故障排查

| 症状 | 检查与处理 |
|------|-----------|
| 限流（`ProvisionedThroughputExceededException`） | 切换到按需或提高容量；指数退避重试；检查热点键。 |
| 热点分区 | 重新设计键（加熵、用排序键或分片）；复查访问模式。 |
| `scan` 太慢 | 用针对访问模式设计的 GSI 做 `query`。 |
| 项太大 | 项上限 400 KB；大负载存 S3，DynamoDB 存指针。 |
| 流积压 | 检查 Lambda 消费并发和错误处理；使用事件过滤。 |
| DAX 没效果 | 确认 DAX 集群在同一个 VPC 且客户端使用 DAX 端点。 |

## 配额

- 单项最大 400 KB。
- 单分区吞吐：3,000 RCU / 1,000 WCU。
- 表大小几乎无上限；账户级配额见 Service Quotas。

## 官方参考

- [什么是 Amazon DynamoDB？- DynamoDB 开发者指南](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/Introduction.html)
- [AWS CLI：dynamodb 命令](https://docs.aws.amazon.com/cli/latest/reference/dynamodb/)
