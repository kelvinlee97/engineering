# Amazon EMR - Runbook 与参考

> 事实核对时间（对照 AWS 官方文档）：2026-08-19

## 概述

Amazon EMR（原 Amazon Elastic MapReduce）是托管集群平台，用于运行 Apache Spark、Hive、HBase、Flink、Trino、Presto 等大数据框架。支持传统 EC2 集群、EMR Serverless 和 EMR on EKS。

## 部署模式

| 模式 | 说明 |
|---|---|
| EMR on EC2 | 按选择的发布版本和应用，在 EC2 实例上预置集群 |
| EMR Serverless | 无需管理集群即可运行 Spark/Hive 作业，按作业付费 |
| EMR on EKS | 用 EMR Spark 运行时在 Amazon EKS 上运行 Spark 工作负载 |

## 核心概念

- **集群**：主节点加核心节点和任务节点；核心节点运行 HDFS，任务节点增加计算能力。
- **发布标签（Release label）**：版本化捆绑包（如 emr-7.5.0），固定应用及其版本。
- **步骤（Steps）**：提交给集群的有序工作单元（Spark/Hive 作业）。
- **应用**：Spark、Hive、HBase、Flink、Trino/Presto、Hue、Zeppelin 及生态工具（Hudi、Iceberg、Delta Lake）。
- **自动伸缩**：按指标或计划伸缩核心/任务节点。
- **Spot 实例**：任务节点用 Spot 省钱；核心节点保持 On-Demand。
- **集成**：S3（S3A）、Glue Data Catalog、DynamoDB、Kinesis，以及 EMRFS 访问 S3。

## 常用操作（AWS CLI）

```bash
# 创建 Spark 集群（使用默认 EMR 角色）
aws emr create-cluster --name analytics --release-label emr-7.5.0 \
  --applications Name=Spark \
  --ec2-attributes KeyName=my-key,InstanceProfile=EMR_EC2_DefaultRole \
  --instance-groups InstanceGroupType=MASTER,InstanceType=m5.xlarge,InstanceCount=1 \
    InstanceGroupType=CORE,InstanceType=m5.xlarge,InstanceCount=2 \
  --service-role EMR_DefaultRole \
  --auto-terminate

# 列出和查看集群
aws emr list-clusters --cluster-states RUNNING WAITING
aws emr describe-cluster --cluster-id j-XXXXXXXXXXXXX

# 添加步骤（Spark 作业）
aws emr add-steps --cluster-id j-XXXXXXXXXXXXX \
  --steps Type=Spark,Name=ETL,ActionOnFailure=CONTINUE,Args=[--class,com.example.ETL,s3://bucket/job.jar]

# 终止集群
aws emr terminate-clusters --cluster-ids j-XXXXXXXXXXXXX
```

## 最佳实践

- 间歇性负载用 EMR Serverless；长期、低延迟场景用 EMR on EC2。
- 数据放 S3（用 EMRFS）而不是 HDFS，集群可以随时销毁且数据保留。
- 任务节点用 Spot，配合自动伸缩匹配需求；启用 Cluster Auto Scaling。
- 用 Glue Data Catalog 与 Athena、Redshift Spectrum 共享表元数据。
- 用步骤或 Step Functions 编排作业；用 CloudWatch 和托管伸缩指标监控。
- 配置加密（S3 SSE、传输 TLS），集群放私有子网。
- 固定发布标签，先在预发集群验证应用升级。

## 故障排查

| 症状 | 检查与处理 |
|---|---|
| 集群启动失败 | 检查 IAM 角色（EMR_DefaultRole/EMR_EC2_DefaultRole）、子网、密钥对和服务配额。 |
| 步骤失败 | 查看 CloudWatch/S3 中的步骤日志、驱动日志和应用 stderr。 |
| 内存不足 | 调大 executor 内存/核数、启用动态分配，或扩展任务节点。 |
| S3 访问拒绝 | 确认实例配置文件角色有相应 S3 权限，桶策略放行。 |
| Spark 作业慢 | 调优分区、用列式格式，必要时启用 EMRFS 一致性视图。 |

## 配额

集群数、每账号实例数和 EMR Serverless 容量受服务配额限制。以 Service Quotas 控制台当前值为准。

## 官方参考

- [什么是 Amazon EMR？](https://docs.aws.amazon.com/emr/latest/ManagementGuide/emr-what-is-emr.html)
- [EMR Serverless 用户指南](https://docs.aws.amazon.com/emr/latest/EMR-Serverless-UserGuide/emr-serverless.html)
- [Amazon EMR 定价](https://aws.amazon.com/emr/pricing/)
- [AWS CLI：emr 命令](https://docs.aws.amazon.com/cli/latest/reference/emr/)
