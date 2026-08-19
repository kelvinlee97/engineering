# Amazon MSK - Runbook 与参考

> 事实核对时间（对照 AWS 官方文档）：2026-08-19

## 概述

Amazon Managed Streaming for Apache Kafka（Amazon MSK）是运行 Apache Kafka 应用的完全托管服务。AWS 管理控制面（集群创建/更新/删除）；你用标准 Kafka 数据面 API 生产/消费，现有应用和工具无需修改即可使用。

## 核心概念

- **集群**：一组 broker 节点；每个可用区至少一个 broker。
- **MSK Provisioned**：你选择 broker 数量和类型（Standard 或 Express）；AWS 管理 ZooKeeper 节点或 KRaft 控制器。
- **MSK Serverless**：AWS 管理 broker 容量，你在集群层面预置，自动伸缩。
- **主题、生产者、消费者**：标准 Kafka API 和工具（kafka-clients、kcat 等）。
- **MSK Connect**：托管连接器，向/从 Kafka 集群流式传输数据。
- **MSK Replicator**：在同一或不同区域间的 MSK 集群之间复制数据。
- **认证**：IAM 访问控制、SASL/SCRAM、TLS 或双向 TLS。
- **监控**：CloudWatch 指标和 Prometheus/Grafana 开放监控。
- **KRaft vs ZooKeeper**：新版 Kafka 用 KRaft 替代 ZooKeeper 管理元数据。

## 常用操作（AWS CLI）

```bash
# 创建预置集群（KRaft 模式，IAM 认证）
aws kafka create-cluster-v2 --cluster-name events-prod \
  --provisioned '{
    "BrokerNodeGroupInfo": {
      "InstanceType": "kafka.m5.large",
      "ClientSubnets": ["subnet-1","subnet-2","subnet-3"]
    },
    "KafkaVersion": "3.7.0",
    "NumberOfBrokerNodes": 3
  }'

# 创建 Serverless 集群
aws kafka create-cluster-v2 --cluster-name events-serverless --serverless '{
  "VpcConfigs": [{"SubnetIds": ["subnet-1","subnet-2"]}],
  "ClientAuthentication": {"Sasl": {"Iam": {"Enabled": true}}}
}'

# 查看集群
aws kafka describe-cluster-v2 --cluster-arn <cluster-arn>
aws kafka list-clusters-v2

# 获取 bootstrap brokers
aws kafka get-bootstrap-brokers --cluster-arn <cluster-arn>

# 删除
aws kafka delete-cluster --cluster-arn <cluster-arn>
```

## 最佳实践

- 流量波动大用 MSK Serverless；可预测容量用 MSK Provisioned 以精细控制。
- broker 至少跨三个可用区，按峰值吞吐选择 broker 类型。
- 用 IAM 访问控制或 SASL/SCRAM（密钥存 Secrets Manager）；启用 TLS。
- 主题副本因子至少 3，保留期匹配消费者回放窗口。
- 用 CloudWatch 和 Prometheus 监控；对 broker CPU、磁盘、请求处理器利用率告警。
- 扩分区前用 `kafka-consumer-groups` 验证消费者行为。
- 跨区域灾备用 MSK Replicator，托管连接器用 MSK Connect。

## 故障排查

| 症状 | 检查与处理 |
|---|---|
| 生产者/消费者无法连接 | 核对 bootstrap brokers、安全组规则和认证配置。 |
| `NotEnoughReplicasException` / 分区副本不足 | 检查 broker 健康和磁盘、副本因子。 |
| 磁盘打满 | 增加存储或缩短保留期；监控 `KafkaDataLogsDiskUsed`。 |
| 限流 | 增加 broker 数量/规格，或改用 Serverless 容量。 |
| 认证失败 | 检查 SASL/IAM 配置、SCRAM 密钥和客户端属性。 |

## 配额

每账号集群数、每集群 broker 数、存储和 Serverless 容量有配额。以 Service Quotas 控制台当前值为准。

## 官方参考

- [欢迎使用 Amazon MSK 开发者指南](https://docs.aws.amazon.com/msk/latest/developerguide/what-is-msk.html)
- [Amazon MSK 服务配额](https://docs.aws.amazon.com/msk/latest/developerguide/limits.html)
- [Amazon MSK 定价](https://aws.amazon.com/msk/pricing/)
- [AWS CLI：kafka 命令](https://docs.aws.amazon.com/cli/latest/reference/kafka/)
