# AWS 生态 - Runbook 与参考

> 事实核对时间（对照 AWS 官方文档）：2026-08-19

## 概述

AWS 生态包括 AWS 云平台本身（在全球基础设施上提供计算、存储、数据库、网络、分析、安全和 AI/ML 服务），以及 AWS Partner Network（APN）、AWS Marketplace、支持计划、合规资源（AWS Artifact），以及指导使用的 Well-Architected 与共担责任框架。

## 核心概念

- **全球基础设施**：区域、可用区和边缘节点；除特别说明外服务按区域作用域。
- **服务类别**：计算（EC2、Lambda、ECS、EKS）、存储（S3、EBS、EFS、FSx）、数据库（RDS、DynamoDB、Aurora）、网络（VPC、Route 53、ELB、CloudFront）、分析（Athena、Redshift、EMR）、安全（IAM、KMS、GuardDuty、Security Hub CSPM）、集成（SQS、SNS、EventBridge）和 AI/ML（SageMaker、Lex、Rekognition 等）。
- **AWS Partner Network（APN）**：提供解决方案、服务和经 AWS 验证能力的咨询与技术合作伙伴。
- **AWS Marketplace**：可在 AWS 中采购和部署的第三方软件与服务数字目录。
- **支持计划**：Basic、Developer、Business、Enterprise（当前计划过渡中的 Business Support+、Enterprise Support、AWS Unified Operations）；计划决定支持访问和 Trusted Advisor 等工具。
- **合规资源**：AWS Artifact 提供报告与协议；共担责任模型帮助理解义务。
- **框架**：Well-Architected Framework 指导架构评审；AWS Cloud Adoption Framework 指导组织上云。

## 常用操作

生态通过控制台和编程服务访问：

```bash
# 示例：查看运行位置与可用内容
aws ec2 describe-regions
aws organizations list-accounts
aws service-quotas list-services
aws marketplace-catalog list-entities --catalog AWSMarketplace --entity-type Products
```

## 最佳实践

- 按工作负载需求和 Well-Architected 支柱选服务，而不是按功能清单。
- 用合并账单和标签获得整个生态的成本可见性。
- 评估 Marketplace/合作伙伴方案时，对照支持、安全和合规要求。
- 支持计划匹配生产需求；启用 Trusted Advisor 和 Health 监控。
- 让认证和合作伙伴能力与团队实际角色对齐。

## 故障排查

| 症状 | 检查与处理 |
|---|---|
| 区域中服务不可用 | 查看服务的区域可用性页面；部分服务并非全球可用。 |
| 合作伙伴方案出问题 | 部署前核对方案的支持路径、IAM 和网络要求。 |
| 需要合规证据 | 用 AWS Artifact；AWS 侧控制由 AWS 覆盖，客户侧由你的团队覆盖。 |

## 配额

生态受各服务配额和协议约束；详见本知识库的 AWS 索引和各服务 runbook。

## 官方参考

- [AWS Cloud 概览](https://docs.aws.amazon.com/whitepapers/latest/aws-overview/introduction.html)
- [AWS Partner Network](https://aws.amazon.com/partners/)
- [AWS Marketplace](https://aws.amazon.com/marketplace)
- [AWS 支持计划](https://aws.amazon.com/premiumsupport/plans/)
- [AWS Artifact](https://aws.amazon.com/artifact/)
- [本知识库的 AWS 索引](../README_ZH.md)
