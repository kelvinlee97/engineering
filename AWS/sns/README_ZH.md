# Amazon SNS - Runbook 与参考

> 事实核对时间（对照 AWS 官方文档）：2026-08-19

## 概述

Amazon Simple Notification Service（Amazon SNS）是全托管的发布/订阅消息服务。发布者向主题（Topic）发送消息，主题把消息投递给订阅的端点。

## 核心概念

- **主题（Topic）**：逻辑接入点和通信渠道；发布者向主题发消息。
- **订阅方**：SQS 队列、Lambda 函数、HTTP(S) 端点、邮件、移动推送、短信、Amazon Data Firehose。
- **A2A 与 A2P**：应用到应用（SQS/Lambda/HTTP）和应用到人（短信/邮件/推送）。
- **扇出（Fanout）**：一次发布同时投递多个端点，做并行异步处理。
- **过滤策略（Filter policy）**：订阅级消息过滤，减少投递和成本。
- **死信队列（DLQ）**：捕获投递失败的消息（SQS/Lambda 订阅）。
- **安全**：KMS 服务端加密、IAM 策略、主题策略。

## 常用操作（AWS CLI）

```bash
# 主题
aws sns create-topic --name my-topic
aws sns list-topics

# 订阅端点（邮件/HTTP 需要确认）
aws sns subscribe --topic-arn arn:aws:sns:ap-southeast-1:123456789012:my-topic \
  --protocol sqs --notification-endpoint arn:aws:sqs:ap-southeast-1:123456789012:my-queue
aws sns subscribe --topic-arn ...:my-topic --protocol email --notification-endpoint ops@example.com

# 订阅过滤策略
aws sns set-subscription-attributes --subscription-arn <arn> \
  --attribute-name FilterPolicy --attribute-value '{"event":["order_created"]}'

# 发布
aws sns publish --topic-arn ...:my-topic --message '{"event":"order_created"}' \
  --message-attributes '{"event":{"DataType":"String","StringValue":"order_created"}}'

# 管理
aws sns get-topic-attributes --topic-arn ...:my-topic
aws sns unsubscribe --subscription-arn <arn>
aws sns delete-topic --topic-arn ...:my-topic
```

## 最佳实践

- 用 **SNS + SQS 扇出**做可靠异步处理和缓冲。
- 用**过滤策略**让订阅方只收到相关消息。
- 在订阅上配置 **DLQ** 捕获投递失败并设置告警。
- 用 message attributes 做路由/过滤；负载保持小（最大 256 KB）。
- 敏感消息用 **SSE-KMS** 加密；IAM 限定到主题 ARN。
- 短信：先在短信沙箱测试，设置消费限额。

## 故障排查

| 症状 | 检查与处理 |
|------|-----------|
| 消息未投递到 SQS | 确认订阅存在、SQS 队列策略允许 SNS；检查 DLQ。 |
| 邮件/HTTP 订阅不生效 | 订阅需要在确认消息中完成确认。 |
| 过滤后的消息没收到 | 核对过滤策略与发布时的 message attributes 是否匹配。 |
| 短信发不出 | 检查短信沙箱、消费限额、区域可用性。 |
| 扇出重复 | 至少一次投递是预期行为；让消费者幂等。 |
| 投递失败 | 查看订阅 DLQ 和 CloudWatch 投递指标。 |

## 配额

- 消息大小：最大 256 KB。
- 账户级主题配额见 Service Quotas。

## 官方参考

- [什么是 Amazon SNS？- Amazon SNS 开发者指南](https://docs.aws.amazon.com/sns/latest/dg/welcome.html)
- [AWS CLI：sns 命令](https://docs.aws.amazon.com/cli/latest/reference/sns/)
