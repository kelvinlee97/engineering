# Amazon MQ - Runbook 与参考

> 事实核对时间（对照 AWS 官方文档）：2026-08-19

## 概述

Amazon MQ 是 Apache ActiveMQ 和 RabbitMQ 的托管消息代理服务。它提供托管维护、版本升级、CloudWatch 监控、静态和传输加密以及 VPC 私有端点，让你迁移现有消息代理工作负载时无需重写应用。

## 核心概念

- **Broker（代理）**：托管的消息代理环境；Amazon MQ 的基本单位（ActiveMQ 或 RabbitMQ 引擎）。
- **部署模式（ActiveMQ）**：开发用单实例，高可用用 active/standby。
- **存储**：EBS 存储；创建 broker 时选择实例类型和存储大小。
- **Quorum 队列（RabbitMQ）**：跨 AZ 的主/从节点复制队列类型，用于持久化和毒消息处理。
- **跨区域数据复制（ActiveMQ）**：从主区域 broker 异步复制到副本区域 broker，可切换提升。
- **安全**：SSL/TLS、VPC 私有端点、IAM 控制 API 级操作、用户名/密码控制 broker 用户。
- **监控**：指标每分钟推送 CloudWatch；控制台、CLI、API 均可查看。

## 常用操作（AWS CLI）

```bash
# 创建 ActiveMQ broker（active/standby）
aws mq create-broker --broker-name prod-mq --engine-type ACTIVEMQ \
  --engine-version 5.18.6 --host-instance-type mq.m5.large \
  --deployment-mode ACTIVE_STANDBY_MULTI_AZ \
  --users '{"Username":"admin","ConsoleAccess":true,"Groups":["admins"]}' \
  --publicly-accessible

# 创建 RabbitMQ broker
aws mq create-broker --broker-name events-mq --engine-type RABBITMQ \
  --engine-version 3.13.12 --host-instance-type mq.m5.large \
  --users '{"Username":"admin"}'

# 列出和查看 broker
aws mq list-brokers
aws mq describe-broker --broker-id <broker-id>

# 重启和删除
aws mq reboot-broker --broker-id <broker-id>
aws mq delete-broker --broker-id <broker-id>
```

## 最佳实践

- 生产用 active/standby（ActiveMQ）或 quorum 队列（RabbitMQ）；单实例只用于开发。
- broker 放私有子网，通过 VPC 端点连接，用安全组限制。
- 启用静态加密（KMS）并要求传输 TLS；定期轮换 broker 用户凭据。
- 按峰值负载和保留需求规划实例类型与存储；监控队列深度和 broker 指标。
- 用维护窗口做版本升级，先验证客户端兼容性。
- 云原生且不依赖特定代理协议的应用，可评估 SQS/SNS 或 EventBridge 替代。

## 故障排查

| 症状 | 检查与处理 |
|---|---|
| 客户端无法连接 | 检查安全组规则（ActiveMQ 61617/61614，RabbitMQ 5671/443）、TLS 和 VPC 路由。 |
| 队列深度增长 | 检查消费者健康、消息 TTL 和 broker 容量；扩容或加存储。 |
| 故障转移不生效 | 核对 active/standby 或 quorum 队列配置及副本健康。 |
| 存储打满 | 增加 EBS 存储或缩短保留；监控 CloudWatch 的 `StorageUsed`。 |
| 维护意外 | 配置维护窗口并监控 broker 状态。 |

## 配额

每账号 broker 数、实例类型、存储和连接数有配额。以 Service Quotas 控制台当前值为准。

## 官方参考

- [什么是 Amazon MQ？](https://docs.aws.amazon.com/amazon-mq/latest/developer-guide/welcome.html)
- [Amazon MQ 服务配额](https://docs.aws.amazon.com/amazon-mq/latest/developer-guide/amazon-mq-limits.html)
- [Amazon MQ 定价](https://aws.amazon.com/amazon-mq/pricing/)
- [AWS CLI：mq 命令](https://docs.aws.amazon.com/cli/latest/reference/mq/)
