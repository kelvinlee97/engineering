# Amazon Kinesis - Runbook 与参考

> 事实核对时间（对照 AWS 官方文档）：2026-08-19

## 概述

Amazon Kinesis 是 AWS 流式数据平台，用于大规模收集、处理和分析实时数据。平台包括 Kinesis Data Streams、Amazon Data Firehose、Managed Service for Apache Flink 和 Kinesis Video Streams。

## 服务组件

| 服务 | 用途 |
|---|---|
| Kinesis Data Streams | 持久、可扩展的流式摄取；每个 shard 内记录有序，生产者推送、消费者拉取 |
| Amazon Data Firehose | 完全托管的流式投递到 S3、Redshift、OpenSearch、Splunk 等；无需运行消费者 |
| Managed Service for Apache Flink | 用 Apache Flink（SQL 和 DataStream API）做流处理 |
| Kinesis Video Streams | 视频流的摄取和回放，用于机器学习和分析 |

## 核心概念

- **流与分片（Shard）**：分片是容量单位；同一分片内数据有序，吞吐量随分片数扩展。
- **记录（Record）**：数据单元（分区键 + 数据块），按可配置周期保留（默认 24 小时，最长 365 天）。
- **生产者和消费者**：生产者用 `PutRecord`/`PutRecords`；消费者用 Kinesis Client Library（KCL）`GetRecords` 容错消费。
- **按需 vs 预置模式**：按需自动伸缩分片；预置模式由你管理固定分片数。
- **增强型扇出**：通过 `SubscribeToShard` 给每个消费者 2 MB/s 专用读吞吐。
- **Firehose 缓冲**：按大小（最大 128 MB）或时间（最长 900 秒）累积记录后再投递。

## 常用操作（AWS CLI）

```bash
# 创建流（预置模式，2 个分片）
aws kinesis create-stream --stream-name events --shard-count 2

# 列出流并写入记录
aws kinesis list-streams
aws kinesis put-record --stream-name events \
  --partition-key order-123 --data "$(printf '{"event":"created"}' | base64)"

# 获取分片迭代器并读取
aws kinesis get-shard-iterator --stream-name events \
  --shard-id shardId-000000000000 --shard-iterator-type TRIM_HORIZON
aws kinesis get-records --shard-iterator <shard-iterator>

# 扩容
aws kinesis update-shard-count --stream-name events --target-shard-count 4 --scaling-type UNIFORM_SCALING

# Data Firehose
aws firehose create-delivery-stream --delivery-stream-name app-logs \
  --extended-s3-destination-configuration RoleARN=arn:aws:iam::123456789012:role/firehose-role,BucketARN=arn:aws:s3:::logs-bucket
aws firehose put-record --delivery-stream-name app-logs \
  --record "Data=$(printf '{"level":"info"}' | base64)"
```

## 最佳实践

- 只需要可靠投递到存储/分析时用 Data Firehose；需要自定义消费者或回放时用 Data Streams。
- 设计分区键避免热点键倾斜到单个分片；监控 `WriteProvisionedThroughputExceeded`。
- 用 Kinesis Client Library（KCL）做容错、近乎精确一次的消费和动态分片处理。
- 保留期匹配回放窗口；保留越久成本越高。
- 消费者多且都要全吞吐时用增强型扇出。
- `PutRecords` 前做缓冲和压缩；用批量写入而不是单条。
- 用 KMS 加密流（SSE），IAM 控制访问；用 CloudWatch 指标监控。

## 故障排查

| 症状 | 检查与处理 |
|---|---|
| `ProvisionedThroughputExceededException` | 增加分片、改善分区键分布，或改用按需模式。 |
| 记录丢失 | 检查保留期和消费者 checkpoint；消费者慢会导致 KCL checkpoint 落后。 |
| 消费者延迟高 | 加分片/消费者、用增强型扇出，或把重处理移到下游。 |
| Firehose 投递失败 | 检查目标权限、缓冲设置，以及投递流的 CloudWatch 指标。 |
| 数据乱序 | 只有同一分片内保证顺序；按此设计分区键。 |

## 配额

每个分片支持 1 MB/s（或 1,000 条/秒）写入、2 MB/s 读取；默认保留 24 小时，可延长至最长 365 天。流、分片和 Firehose 数量有每账号配额。以 Service Quotas 控制台当前值为准。

## 官方参考

- [什么是 Amazon Kinesis Data Streams？](https://docs.aws.amazon.com/streams/latest/dev/introduction.html)
- [什么是 Amazon Data Firehose？](https://docs.aws.amazon.com/firehose/latest/dev/what-is-this-service.html)
- [Amazon Kinesis 定价](https://aws.amazon.com/kinesis/pricing/)
- [AWS CLI：kinesis 与 firehose 命令](https://docs.aws.amazon.com/cli/latest/reference/kinesis/)
