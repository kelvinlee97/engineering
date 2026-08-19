# Amazon SageMaker AI - Runbook 与参考

> 事实核对时间（对照 AWS 官方文档）：2026-08-19

## 概述

Amazon SageMaker AI（2024 年 12 月 3 日由 Amazon SageMaker 更名）是全托管机器学习服务，用于在生产中构建、训练和部署 ML 模型。它提供托管算法、分布式训练、Notebook 与 Studio、模型部署和 MLOps 工具。下一代 Amazon SageMaker 是统一的数据、分析与 AI 平台，还包括 Lakehouse、数据与 AI 治理、SQL 分析、数据处理、Unified Studio 和 Amazon Bedrock。

## 核心概念

- **旧命名不变**：更名后 `sagemaker` API 命名空间、CLI 命令、托管策略、端点、CloudFormation 资源、服务关联角色以及控制台/文档 URL 均保持不变。
- **SageMaker AI**：用全托管基础设施、工具和工作流构建、训练和部署 ML 与基础模型。
- **Studio / Unified Studio**：用于数据准备、实验和 MLOps 的集成开发环境。
- **训练**：托管算法以及自带算法/框架，支持灵活的分部署训练选项。
- **部署**：从控制台几步即可将模型部署到安全、可扩展的托管端点；支持实时、无服务器和批处理推理。
- **下一代 SageMaker 平台**：统一数据访问（跨 S3 和 Redshift 的 Lakehouse）、数据治理（基于 DataZone 的 Catalog）、SQL 分析（Redshift）、数据处理（Athena、EMR、Glue）以及生成式 AI 的 Bedrock。

## 常用操作（AWS CLI）

```bash
# 创建并启动 Notebook 实例
aws sagemaker create-notebook-instance --notebook-instance-name ml-env \
  --instance-type ml.t3.medium --role-arn arn:aws:iam::123456789012:role/sagemaker-role
aws sagemaker start-notebook-instance --notebook-instance-name ml-env

# 训练模型
aws sagemaker create-training-job --training-job-name my-job \
  --algorithm-specification file://algo.json \
  --role-arn arn:aws:iam::123456789012:role/sagemaker-role \
  --input-data-config file://inputs.json \
  --output-data-config file://output.json \
  --resource-config '{"InstanceType":"ml.m5.large","InstanceCount":1}'

# 部署端点
aws sagemaker create-endpoint-config --endpoint-config-name my-config \
  --production-variants file://variant.json
aws sagemaker create-endpoint --endpoint-name my-endpoint \
  --endpoint-config-name my-config
aws sagemaker list-endpoints
```

## 最佳实践

- 使用 SageMaker Studio/Unified Studio 跑完整流程，保持实验可跟踪、可复现。
- 训练数据放 S3 并做版本管理；用托管 feature store 复用特征。
- 选择满足需求的最小实例，用托管 Spot 训练降低成本。
- 生产端点配置模型监控（数据质量、漂移），并通过 CI/CD 管道部署。
- 用 IAM、VPC 和 KMS 加密保护 Notebook/端点；用 SageMaker Role Manager 生成最小权限角色。
- 需要时在同一平台中用 Amazon Bedrock 评估基础模型用例。

## 故障排查

| 症状 | 检查与处理 |
|---|---|
| 训练任务失败 | 查看 CloudWatch 中的任务日志、输入数据格式和 IAM 角色权限。 |
| 端点创建失败 | 检查模型制品路径、实例类型和 production variant 配置。 |
| Notebook 无法访问 S3 | 核对 Notebook 角色和实例配置文件的权限。 |
| 推理慢 | 合理调整端点实例，突发流量用无服务器推理，非实时负载用批处理推理。 |
| 更名混淆 | 更名不改变 `sagemaker` 命名空间和现有功能。 |

## 配额

每账户 Notebook 实例、训练任务、端点和模型大小有限制。以 Amazon SageMaker 端点和配额页面及 Service Quotas 控制台为准。

## 官方参考

- [什么是 Amazon SageMaker AI？- 开发者指南](https://docs.aws.amazon.com/sagemaker/latest/dg/whatis.html)
- [Amazon SageMaker 端点和配额](https://docs.aws.amazon.com/general/latest/gr/sagemaker.html)
- [Amazon SageMaker 定价](https://aws.amazon.com/sagemaker/pricing/)
- [AWS CLI：sagemaker 命令](https://docs.aws.amazon.com/cli/latest/reference/sagemaker/)
