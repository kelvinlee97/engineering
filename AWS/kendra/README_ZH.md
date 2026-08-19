# Amazon Kendra - Runbook 与参考

> 事实核对时间（对照 AWS 官方文档）：2026-08-19

## 概述

Amazon Kendra 是托管智能搜索服务，使用自然语言处理和语义排序从文档中检索答案，超越传统关键词搜索。注意：Amazon Kendra 已不再对新客户开放；类似能力 AWS 推荐使用 Amazon Bedrock Knowledge Bases。

## 核心概念

- **索引（Index）**：可搜索的文档存储；Kendra 提供 GenAI Enterprise、Basic Enterprise 和 Basic Developer 三个版本。
- **数据源**：连接 SharePoint、S3、数据库等仓库的连接器，用于爬取和同步文档。
- **语义搜索**：理解问题上下文，返回最相关的答案、片段或文档。
- **查询类型**：事实类问题（从 FAQ/文档返回单词或短语答案）、描述类问题，以及关键词/自然语言问题。
- **智能排序（Intelligent ranking）**：用 Kendra 语义能力对另一搜索服务的结果重新排序。
- **GenAI 集成**：Kendra GenAI 索引可支撑 Amazon Q Business 和 Amazon Bedrock knowledge bases，用于检索增强生成（RAG）。
- **安全**：结果反映组织的访问模型，支持用户/组过滤；认证和授权由你负责。

## 常用操作（AWS CLI）

```bash
# 创建索引和数据源
aws kendra create-index --name corp-search --edition ENTERPRISE_EDITOR \
  --role-arn arn:aws:iam::123456789012:role/kendra-role
aws kendra create-data-source --index-id <index-id> --name s3-docs \
  --type S3 --configuration file://ds-config.json
aws kendra start-data-source-sync-job --id <data-source-id> --index-id <index-id>

# 查询索引
aws kendra query --index-id <index-id> --query-text "How do I reset my password?"
aws kendra list-indices
```

## 最佳实践

- 生产 RAG 和企业搜索使用 GenAI Enterprise 索引。
- 整理元数据和 FAQ 提升答案质量；用访问控制列表保证文档安全。
- 按计划同步数据源并监控同步任务状态。
- 用智能排序提升现有搜索引擎，无需迁移。
- 新的生成式搜索用例优先评估 Amazon Bedrock Knowledge Bases（当前推荐服务）。
- 为已供给索引做好预算：即使空闲，也会为已供给索引付费。

## 故障排查

| 症状 | 检查与处理 |
|---|---|
| 无结果 | 检查索引状态、数据源同步和查询/访问过滤配置。 |
| 同步任务失败 | 查看数据源配置、凭证和文档格式支持。 |
| 答案不准确 | 改进元数据、FAQ 和文档质量；变更后重新索引。 |
| 搜索返回受限文档 | 确认索引已配置 ACL/用户组过滤。 |
| 无法创建索引 | Kendra 已对新客户关闭；使用 Amazon Bedrock Knowledge Bases。 |

## 配额

每账户索引数、文档与元数据限制以及数据源同步配额有限制。以 Amazon Kendra 端点和配额页面及 Service Quotas 控制台为准。

## 官方参考

- [什么是 Amazon Kendra？- 开发者指南](https://docs.aws.amazon.com/kendra/latest/dg/what-is-kendra.html)
- [Amazon Kendra 端点和配额](https://docs.aws.amazon.com/general/latest/gr/kendra.html)
- [Amazon Kendra 定价](https://aws.amazon.com/kendra/pricing/)
- [AWS CLI：kendra 命令](https://docs.aws.amazon.com/cli/latest/reference/kendra/)
