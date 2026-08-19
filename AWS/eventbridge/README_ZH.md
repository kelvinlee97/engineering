# Amazon EventBridge - Runbook 与参考

> 事实核对时间（对照 AWS 官方文档）：2026-08-19

## 概述

Amazon EventBridge 是无服务器事件路由服务，用于构建事件驱动应用。它负责事件的摄取、过滤、转换和投递，连接 AWS 服务、你的应用和第三方 SaaS。包含事件总线与规则、EventBridge Pipes（带富化的一对一集成）和 EventBridge Scheduler（cron/rate/一次性调度）。

## 核心概念

- **事件（Event）**：表示状态变化的 JSON 结构；AWS 服务会自动发出事件。
- **事件总线（Event bus）**：接收事件并投递给零个或多个目标的路由器；每个账号有默认总线，另有自定义总线和来自其他账号的总线。
- **规则（Rule）**：按事件模式匹配事件并路由到目标（Lambda、SQS、SNS、Step Functions、API 目标等）。
- **事件模式**：JSON 匹配（source、detail-type、detail 字段），决定规则接收哪些事件。
- **目标与转换**：目标服务加可选的事件载荷输入转换。
- **归档与重放（Archives and replay）**：归档保存事件最多 14 天，可重放用于测试或恢复。
- **Pipes**：从单一来源（含 DynamoDB 流、Kinesis 等非 EventBridge 来源）到单一目标的一对一集成，支持过滤和富化。
- **Scheduler**：无服务器调度，支持 cron/rate 表达式、一次性调用、灵活时间窗口和重试限制。
- **Schemas**：发现和管理事件 schema，生成代码绑定。

## 常用操作（AWS CLI）

```bash
# 在默认总线上创建规则并添加目标
aws events put-rule --name order-created \
  --event-pattern '{"source":["app.orders"],"detail-type":["OrderCreated"]}'
aws events put-targets --rule order-created \
  --targets 'Id=1,Arn=arn:aws:lambda:us-east-1:123456789012:function:on-order'

# 发送自定义事件
aws events put-events \
  --entries 'Source=app.orders,DetailType=OrderCreated,Detail="{\"orderId\":\"123\"}",EventBusName=default'

# 列出和删除规则
aws events list-rules
aws events delete-rule --name order-created

# 归档和重放
aws events create-archive --archive-name orders-archive --event-source-arn arn:aws:events:us-east-1:123456789012:event-bus/default
aws events start-replay --replay-name replay-1 --destination '{"Arn":"arn:aws:events:us-east-1:123456789012:event-bus/default"}' \
  --event-start-time 2026-08-18T00:00:00Z --event-end-time 2026-08-19T00:00:00Z \
  --source-arn arn:aws:events:us-east-1:123456789012:event-bus/default

# Scheduler
aws scheduler create-schedule --name nightly-cleanup --schedule-expression "cron(0 2 * * ? *)" \
  --flexible-time-window Mode=OFF \
  --target '{"Arn":"arn:aws:lambda:us-east-1:123456789012:function:cleanup","RoleArn":"arn:aws:iam::123456789012:role/scheduler-role"}'
```

## 最佳实践

- 显式建模事件：使用带版本的 `detail-type` 和稳定的 `source`，让消费者独立演进。
- 按领域使用自定义事件总线，规则只关注单一职责。
- 简单源到目标的管道用 Pipes，而不是 Lambda 胶水。
- 归档关键事件，并先测试重放再依赖它做恢复。
- 先在预发总线验证事件模式和转换。
- 目标用资源策略和 IAM 最小权限；用 CloudTrail 审计。
- 用 CloudWatch 监控（调用数、失败、限流），对目标投递失败设置告警。

## 故障排查

| 症状 | 检查与处理 |
|---|---|
| 规则不触发 | 核对事件模式是否匹配（source/detail-type），以及总线和规则所在区域。 |
| 目标未调用 | 检查目标 ARN、IAM/资源策略和输入转换语法。 |
| 事件丢失 | 确认规则启用、目标存在，并配置投递重试策略。 |
| 重放未投递 | 确认归档包含事件，目标总线/规则处于启用状态。 |
| Scheduler 调用失败 | 检查调度表达式、灵活时间窗口和目标角色权限。 |

## 配额

每总线规则数、每规则目标数、事件大小（256 KB）、归档保留（最多 14 天）和 Scheduler 配额有每账号限制。以 Service Quotas 控制台当前值为准。

## 官方参考

- [什么是 Amazon EventBridge？](https://docs.aws.amazon.com/eventbridge/latest/userguide/eb-what-is.html)
- [Amazon EventBridge 配额](https://docs.aws.amazon.com/eventbridge/latest/userguide/eb-quota.html)
- [Amazon EventBridge 定价](https://aws.amazon.com/eventbridge/pricing/)
- [AWS CLI：events 与 scheduler 命令](https://docs.aws.amazon.com/cli/latest/reference/events/)
