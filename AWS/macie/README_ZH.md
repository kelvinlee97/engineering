# Amazon Macie - Runbook 与参考

> 事实核对时间（对照 AWS 官方文档）：2026-08-19

## 概述

Amazon Macie 是一项数据安全服务，使用机器学习和模式匹配发现 Amazon S3 中的敏感数据，评估 S3 存储桶的安全与访问控制问题，并生成可供审查和修复的 finding。它提供存储桶清单、仪表盘和自动化敏感数据发现。

## 核心概念

- **存储桶清单与监控**：Macie 自动清点 S3 通用存储桶，并评估公开访问、共享访问和加密等问题，生成 policy finding。
- **敏感数据发现**：自动化发现持续对代表性对象采样；也可以运行发现任务（jobs）对指定存储桶做更深入、更针对性的分析，并定义采样深度。
- **托管数据标识符（Managed data identifiers）**：内置标准，可检测多个国家/地区的 PII、财务信息和凭证数据；自定义数据标识符使用你的正则和邻近规则；允许列表（allow lists）排除已知可接受的文本。
- **Finding**：包含严重性、受影响资源和检测详情的报告；可在控制台/API 中查看，并发布到 EventBridge 或 AWS Security Hub CSPM。
- **多账户**：通过 AWS Organizations（或邀请）指定 Macie 管理员，管理成员账户并检查其存储桶。
- **免费试用**：首次启用包含 30 天免费试用，覆盖存储桶评估和自动化发现（发现任务不包含在内）。

## 常用操作（AWS CLI）

```bash
# 启用 Macie 并查看会话状态
aws macie2 enable-macie --finding-publishing-frequency FIFTEEN_MINUTES
aws macie2 get-macie-session

# 查看存储桶清单和统计
aws macie2 list-buckets --account-ids 123456789012
aws macie2 get-bucket-statistics --account-id 123456789012

# 创建并运行敏感数据发现任务
aws macie2 create-classification-job --job-type ONE_TIME \
  --name pii-scan --s3-job-definition file://job.json \
  --sampling-percentage 100
aws macie2 list-classification-jobs

# Finding
aws macie2 list-findings --finding-criteria '{"severity":{"gte":50}}'
aws macie2 get-findings --finding-ids file://finding-ids.json
```

## 最佳实践

- 在 S3 数据增长前启用 Macie，尽早建立清单和基线。
- 自动化发现做广泛覆盖，高价值存储桶或合规期限使用针对性发现任务。
- 组合托管与自定义数据标识符；用允许列表减少已知样例数据的噪声。
- 将 finding 路由到 EventBridge 实现自动响应，并接入 Security Hub CSPM 聚合安全态势。
- 落实存储桶的公开访问/加密策略，让 policy finding 保持低位；及时修复 finding。
- 多账户环境通过 AWS Organizations 委派管理员集中管理 Macie。

## 故障排查

| 症状 | 检查与处理 |
|---|---|
| 存储桶未入库 | 确认已在存储桶所在区域启用 Macie，且账户为成员。 |
| 没有敏感数据 finding | 检查任务/自动化发现配置、采样百分比和托管标识符范围。 |
| 对象分析报错 | 核对对象权限、用于解密的 KMS 密钥访问以及受支持的对象类型。 |
| Security Hub CSPM 中没有 finding | 在同一区域启用 Security Hub CSPM 的 Macie 集成。 |
| 成本高于预期 | 审查监控的存储桶数、发现任务量和采样设置。 |

## 配额

每账户分类任务数、finding 保留期和 API 配额有限制。以 Amazon Macie 端点和配额页面及 Service Quotas 控制台为准。

## 官方参考

- [什么是 Amazon Macie？- 用户指南](https://docs.aws.amazon.com/macie/latest/user/what-is-macie.html)
- [Amazon Macie 端点和配额](https://docs.aws.amazon.com/general/latest/gr/macie.html)
- [Amazon Macie 定价](https://aws.amazon.com/macie/pricing/)
- [AWS CLI：macie2 命令](https://docs.aws.amazon.com/cli/latest/reference/macie2/)
