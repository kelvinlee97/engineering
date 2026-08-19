# Amazon CloudSearch - Runbook 与参考

> 事实核对时间（对照 AWS 官方文档）：2026-08-19

## 概述

Amazon CloudSearch 是全托管搜索服务，用于为网页、文档、论坛帖子、商品信息等大规模数据集合构建搜索方案。你创建搜索域（domain）、上传数据，并通过 HTTP 搜索端点查询。注意：Amazon CloudSearch 已不再向新客户开放；现有客户可以继续使用。

## 核心概念

- **搜索域（Search domain）**：一个域包含你的可搜索数据和提供搜索请求的搜索实例；不同数据集合可创建多个域。
- **索引（Indexing）**：CloudSearch 为结构化数据和纯文本建立索引，并将索引部署到一个或多个搜索实例。
- **搜索功能**：带语言特定文本处理的全文本搜索、布尔搜索、前缀与范围搜索、词项加权（term boosting）、分面（facet）、高亮和自动补全建议。
- **端点**：配置端点（按区域）管理域；每个域有文档端点（`doc-<domain>-<id>...`，用于上传）和搜索端点（`search-<domain>-<id>...`，用于查询）；结果格式为 JSON 或 XML。
- **扩展**：随数据量和流量变化添加/移除搜索实例。

## 常用操作（AWS CLI）

```bash
# 创建和管理域
aws cloudsearch create-domain --domain-name products
aws cloudsearch describe-domains --domain-names products

# 上传文档（通过文档端点提交 JSON/XML 批次）
aws cloudsearchdomain upload-documents --endpoint-url https://doc-products-xxxxxxxxx.us-east-1.cloudsearch.amazonaws.com \
  --documents file://batch.json --content-type application/json

# 建立索引并搜索
aws cloudsearch index-documents --domain-name products
aws cloudsearchdomain search --endpoint-url https://search-products-xxxxxxxxx.us-east-1.cloudsearch.amazonaws.com \
  --query "laptop" --query-parser simple --size 10

# 删除域
aws cloudsearch delete-domain --domain-name products
```

## 最佳实践

- 上传大批量数据前先定义清晰的索引 schema（字段、分面、suggester）。
- 批量上传文档，每批完成后统一建立索引，减少索引开销。
- 按数据量和查询流量选择搜索实例；监控延迟并提前扩容。
- 使用 facet 和 suggester 提升结果体验；搜索端点不应公开时用 SigV4 或访问策略保护。
- 现有客户：新项目请规划迁移到当前搜索服务，因为新客户无法再开通。

## 故障排查

| 症状 | 检查与处理 |
|---|---|
| 文档搜不到 | 确认文档已上传到文档端点，且 `index-documents` 执行成功。 |
| 搜索无结果 | 检查查询解析器、字段名，以及索引是否处于 ACTIVE 状态。 |
| 不知道域端点 | 用 `describe-domains` 获取端点；其中包含账户/域标识。 |
| 搜索慢 | 增加搜索实例或减少结果集；检查 facet/聚合使用情况。 |
| 访问被拒 | 用 SigV4 签名请求，或为匿名查询端点配置访问策略。 |

## 配额

每账户域数、每域搜索实例数、文档大小和 API 速率有限制；服务仅限现有客户开通。以 Amazon CloudSearch 端点和配额页面为准。

## 官方参考

- [什么是 Amazon CloudSearch？- 开发者指南](https://docs.aws.amazon.com/cloudsearch/latest/developerguide/what-is-cloudsearch.html)
- [Amazon CloudSearch 端点和配额](https://docs.aws.amazon.com/general/latest/gr/cloudsearch.html)
- [Amazon CloudSearch 定价](https://aws.amazon.com/cloudsearch/pricing/)
- [AWS CLI：cloudsearch 和 cloudsearchdomain 命令](https://docs.aws.amazon.com/cli/latest/reference/cloudsearch/)
