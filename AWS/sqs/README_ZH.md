# Amazon SQS - Runbook 与参考

> 事实核对时间（对照 AWS 官方文档）：2026-08-19

## 概述

Amazon Simple Queue Service（Amazon SQS）是托管消息队列服务，用于解耦分布式系统。消息冗余存储在多台服务器上；支持死信队列（DLQ）和成本分配标签。

## 核心概念

- **队列类型**：标准队列（至少一次投递、高吞吐）和 FIFO 队列（精确一次处理、有序、支持高吞吐模式）。
- **可见性超时（Visibility timeout）**：消息被消费者接收后对其他消费者隐藏的时长（处理期间）。
- **消息保留期**：默认 4 天，可配置 60 秒到 14 天。
- **死信队列（DLQ）**：接收源队列处理失败消息的队列。
- **长轮询（Long polling）**：降低成本与延迟，推荐（`ReceiveMessageWaitTimeSeconds=20`）。
- **安全**：服务端加密（SQS 托管或 KMS）、IAM 策略、队列策略。

## 常用操作（AWS CLI）

```bash
# 创建队列（标准 + FIFO + DLQ）
aws sqs create-queue --queue-name my-queue \
  --attributes VisibilityTimeout=60,ReceiveMessageWaitTimeSeconds=20,MessageRetentionPeriod=345600
aws sqs create-queue --queue-name my-queue.fifo --attributes FifoQueue=true
aws sqs create-queue --queue-name my-queue-dlq

# 发送
aws sqs send-message --queue-url https://sqs.ap-southeast-1.amazonaws.com/123456789012/my-queue \
  --message-body '{"order": "1001"}'

# 接收并删除
aws sqs receive-message --queue-url .../my-queue --max-number-of-messages 10 --wait-time-seconds 20
aws sqs delete-message --queue-url .../my-queue --receipt-handle <receipt-handle>

# 配置 DLQ（源队列的 RedrivePolicy）
aws sqs set-queue-attributes --queue-url .../my-queue \
  --attributes '{"RedrivePolicy":"{\"deadLetterTargetArn\":\"arn:aws:sqs:...:my-queue-dlq\",\"maxReceiveCount\":5}"}'

# 查看
aws sqs list-queues
aws sqs get-queue-attributes --queue-url .../my-queue --attribute-names All
```

## 最佳实践

- 配置 **DLQ** 和合理的 `maxReceiveCount`，对 DLQ 深度设置告警。
- **可见性超时**大于最大处理时间；使用长轮询。
- 用**批量 API**（最多 10 条）降低成本。
- 消费者要**幂等**（标准队列是至少一次投递）。
- 需要有序或精确一次时用 **FIFO**；同一工作流用同一个 message group ID。
- 敏感消息加密（SSE-KMS），IAM 策略限定到队列 ARN。

## 故障排查

| 症状 | 检查与处理 |
|------|-----------|
| 消息卡住/不被消费 | 检查可见性超时与消费者处理时长；检查消费者报错。 |
| 重复处理 | 标准队列预期行为；让消费者幂等。 |
| DLQ 不断堆积 | 检查消息内容和消费者错误；修复消费者后 redrive。 |
| 限流 | 用批量发送/接收和指数退避。 |
| FIFO 乱序 | 确认同一工作流的所有消息使用同一个 message group ID。 |
| 消息超过 1 MiB | 大负载存 S3，消息里放指针。 |

## 配额

- 消息大小：1 KB - 1 MiB。
- 保留期：60 秒 - 14 天。
- 在途消息（标准队列）：每队列 120,000 条。
- 账户级配额见 Service Quotas。

## 官方参考

- [什么是 Amazon SQS？- Amazon SQS 开发者指南](https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/welcome.html)
- [AWS CLI：sqs 命令](https://docs.aws.amazon.com/cli/latest/reference/sqs/)
