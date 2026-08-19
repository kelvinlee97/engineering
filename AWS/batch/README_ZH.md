# AWS Batch - Runbook 与参考

> 事实核对时间（对照 AWS 官方文档）：2026-08-19

## 概述

AWS Batch 是完全托管的批处理计算服务。它按需供给计算资源、优化工作负载分布，并在 Amazon ECS、Amazon EKS、EC2 和 AWS Fargate 上运行容器化批处理作业。还支持 SageMaker Training 作业排队。

## 核心概念

- **计算环境（Compute environment）**：作业运行的计算资源池（EC2 On-Demand/Spot、Fargate 或 EKS）。
- **作业队列（Job queue）**：有序提交队列，按优先级映射到一个或多个计算环境。
- **作业定义（Job definition）**：容器镜像、资源（vCPU/内存）、IAM 角色和参数。
- **作业（Job）**：提交到队列的单个工作单元；可以是单个容器或数组作业。
- **数组作业（Array jobs）**：用不同索引值运行同一作业的多个副本。
- **多节点并行作业**：跨多实例协调多个容器，用于 MPI 风格工作负载。
- **调度策略**：跨队列的公平调度和作业优先级。
- **SageMaker 排队**：用可配置队列和优先级提交 ML 训练作业。

## 常用操作（AWS CLI）

```bash
# 创建 Fargate 计算环境和作业队列
aws batch create-compute-environment --compute-environment-name fargate-env \
  --type MANAGED --compute-resources '{
    "Type": "FARGATE",
    "Subnets": ["subnet-1","subnet-2"],
    "SecurityGroupIds": ["sg-12345"],
    "AssignPublicIp": "DISABLED"
  }'
aws batch create-job-queue --job-queue-name main --state ENABLED \
  --priority 1 --compute-environment-order '{"Order":1,"ComputeEnvironment":"fargate-env"}'

# 注册作业定义
aws batch register-job-definition --job-definition-name etl \
  --type container --container-properties '{
    "Image": "123456789012.dkr.ecr.us-east-1.amazonaws.com/etl:latest",
    "ResourceRequirements": [{"Type":"VCPU","Value":"2"},{"Type":"MEMORY","Value":"4096"}],
    "ExecutionRoleArn": "arn:aws:iam::123456789012:role/ecsTaskExecutionRole"
  }'

# 提交和监控作业
aws batch submit-job --job-name etl-2026-08-19 --job-queue main \
  --job-definition etl --parameters '{"date":"2026-08-19"}'
aws batch describe-jobs --jobs <job-id>
aws batch list-jobs --job-queue main --job-status RUNNABLE

# 取消/终止
aws batch cancel-job --job-id <job-id> --reason "schedule change"
aws batch terminate-job --job-id <job-id> --reason "maintenance"
```

## 最佳实践

- 简单容器作业用 Fargate；大计算量或 GPU 负载用 EC2（配 Spot）。
- 按优先级/团队拆分作业队列，用调度策略保证公平。
- 作业要幂等、可容错；重试逻辑放应用内。
- 作业脚本/配置存 S3，容器镜像存 ECR；两者都做版本管理。
- 监控队列深度、作业状态和计算环境利用率；设置告警。
- 空闲时清理计算环境；Spot 用多样化的分配策略节省成本。

## 故障排查

| 症状 | 检查与处理 |
|---|---|
| 作业卡在 RUNNABLE | 检查队列/计算环境容量、子网/IP 可用性和作业定义。 |
| 容器失败 | 查看 CloudWatch 日志和退出码；本地先测试镜像。 |
| 计算环境容量不足 | 提高 max vCPU 或加 Spot 容量；检查服务配额。 |
| IAM 报错 | 核对作业角色和执行角色权限。 |
| 数组作业部分失败 | 检查各索引退出码，相应设计重试。 |

## 配额

计算环境、作业队列、在途作业数和每账号最大 vCPU 有配额。以 Service Quotas 控制台当前值为准。

## 官方参考

- [什么是 AWS Batch？](https://docs.aws.amazon.com/batch/latest/userguide/what-is-batch.html)
- [AWS Batch 服务配额](https://docs.aws.amazon.com/batch/latest/userguide/service_limits.html)
- [AWS Batch 定价](https://aws.amazon.com/batch/pricing/)
- [AWS CLI：batch 命令](https://docs.aws.amazon.com/cli/latest/reference/batch/)
