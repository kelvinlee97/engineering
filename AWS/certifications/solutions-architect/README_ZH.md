# AWS Certified Solutions Architect - Associate（SAA-C03）- 学习大纲

> 事实核对时间（对照 AWS 官方文档）：2026-08-19

## 考试概览

SAA-C03 面向解决方案架构师角色，验证基于 AWS Well-Architected Framework 设计方案的能力：满足当前和未来的业务需求，同时保证架构安全、弹性、高性能和成本优化，并能评审现有方案提出改进。

- **题型**：65 题（50 计分 + 15 不计分），单选和多选。
- **时长**：130 分钟。
- **评分**：换算分 100-1,000；及格线 720；补偿计分（无需每节都过线）。
- **建议经验**：至少一年使用 AWS 服务设计解决方案的实操经验。

## 官方资源

- [SAA-C03 考试指南](https://docs.aws.amazon.com/aws-certification/latest/solutions-architect-associate-03/solutions-architect-associate-03.html)
- [AWS 认证总览](https://aws.amazon.com/certification/)
- [AWS Skill Builder](https://skillbuilder.aws/)

## 内容领域

官方考试指南定义了四个内容领域及其权重：

1. 设计安全架构。
2. 设计弹性架构。
3. 设计高性能架构。
4. 设计成本优化架构。

详细任务说明以考试指南为准；本大纲沿用原知识库的结构。

## Cloud Practitioner 基础（CLF-C02）

原知识库从 Cloud Practitioner 内容起步，这些内容仍是很好的基础：

- 云计算优势：按需、按量付费、弹性、全球覆盖。
- AWS 云的设计原则。
- 安全与合规概念、IAM 和访问管理。
- 核心技术和服务：计算、存储、数据库、网络、AI/ML、分析。
- 账单、定价与支持。

官方指南：[CLF-C02 考试指南](https://docs.aws.amazon.com/aws-certification/latest/cloud-practitioner-02/cloud-practitioner-02.html)

## 云计算基础

- 按需自助服务和按量付费。
- 规模经济与可变成本 vs 资本支出。
- 服务模型：IaaS、PaaS、SaaS。
- 与传统数据中心相比的弹性、可扩展性和敏捷性。

## 云技术与服务

- 全球基础设施：区域、可用区、边缘站点。
- 核心服务分类：计算、存储、数据库、网络、安全、分析、集成。
- 本知识库中每个服务都有深入 runbook（见索引）。

## AWS 生态与共享责任模型

- 共享责任：AWS 负责云的安全；客户负责云内的安全。
- AWS Partner Network、AWS Marketplace 和支持计划。
- 用 AWS Artifact 获取合规报告与协议。

## AWS Well-Architected Framework

六大支柱：

1. 卓越运营
2. 安全
3. 可靠性
4. 性能效率
5. 成本优化
6. 可持续性

官方白皮书：[AWS Well-Architected Framework](https://docs.aws.amazon.com/wellarchitected/latest/framework/welcome.html)

## 云计算的特性与优势

- 弹性与可扩展性（纵向和横向）。
- 跨可用区和区域的高可用与容错。
- 解耦、松散耦合架构与无服务器选项。
- 减轻运维负担的托管服务。

## AWS 定价模型

- 按需：按用量付费，无承诺。
- Savings Plans 和预留实例：承诺用量换折扣。
- Spot 实例：用闲置容量降低成本，适合可中断负载。
- 专用主机/实例：满足物理隔离需求。
- 免费套餐、合并账单和 Cost Explorer 成本追踪。

## 学习计划

1. 通读官方 SAA-C03 考试指南，标注任务说明。
2. 阅读 Well-Architected Framework 白皮书。
3. 在自己的账号里按本知识库 runbook 动手实践。
4. 在 AWS Skill Builder 做官方练习题，针对薄弱领域复习。
5. 报名前再次核对考试指南；AWS 会随时间更新考试范围。

## 练习资源

官方练习题和课程在 AWS Skill Builder 提供。题库内容有意不在此发布。

## 本知识库相关 Runbook

- 计算：[EC2](../../ec2/README.md)、[ECS](../../ecs/README.md)、[EKS](../../eks/README.md)、[Lambda](../../lambda/README.md)
- 存储：[S3](../../s3/README.md)、[FSx](../../fsx/README.md)、[Storage Gateway](../../storage-gateway/README.md)
- 数据库：[RDS](../../rds/README.md)、[DynamoDB](../../dynamodb/README.md)、[ElastiCache](../../elasticache/README.md)
- 网络：[VPC](../../vpc/README.md)、[Route 53](../../route53/README.md)、[ELB](../../elb/README.md)、[CloudFront](../../cloudfront/README.md)
- 安全：[IAM](../../iam/README.md)、[KMS](../../kms/README.md)、[Secrets Manager](../../secrets-manager/README.md)、[WAF](../../waf/README.md)、[Shield](../../shield/README.md)、[GuardDuty](../../guardduty/README.md)、[Security Hub CSPM](../../security-hub/README.md)
- 集成：[SQS](../../sqs/README.md)、[SNS](../../sns/README.md)、[Step Functions](../../step-functions/README.md)、[EventBridge](../../eventbridge/README.md)
