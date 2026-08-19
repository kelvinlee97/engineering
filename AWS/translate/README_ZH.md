# Amazon Translate - Runbook 与参考

> 事实核对时间（对照 AWS 官方文档）：2026-08-19

## 概述

Amazon Translate 是文本翻译服务，使用先进机器学习提供高质量按需翻译。你可以翻译非结构化文本、翻译 S3 中的文档，或将翻译集成到支持多语言的应用中。无合同或最低承诺；按翻译字符数付费。

## 核心概念

- **实时翻译**：`translate-text` API，用于小文本单元（单句、UI 字符串），低延迟。
- **批量翻译**：翻译 S3 中的文档（HTML、DOCX、XLSX、PPTX、TXT）任务；结果写入 S3。
- **语言**：支持多种语言与语言代码；详见受支持语言表。
- **定制**：自定义术语表（terminology）和平行数据，控制领域翻译。
- **主动自定义翻译（ACT）**：用平行数据训练自定义翻译模型，提升领域准确率。
- **集成**：与 Comprehend（分析翻译后文本）、Transcribe（字幕/实时字幕）、Polly（朗读翻译内容）、Lambda 和 Glue 组合。
- **用途**：多语言用户体验、知识库/支持内容翻译、跨语言 eDiscovery 搜索、社交/新闻分析。

## 常用操作（AWS CLI）

```bash
# 实时翻译
aws translate translate-text --source-language-code en \
  --target-language-code zh --text "Welcome to our platform"

# S3 文档批量翻译
aws translate start-text-translation-job --job-name docs-zh \
  --data-role-arn arn:aws:iam::123456789012:role/translate-role \
  --input-data-config '{"S3Uri":"s3://bucket/in/"}' \
  --output-data-config '{"S3Uri":"s3://bucket/out/"}' \
  --source-language-code en --target-language-codes zh
aws translate describe-text-translation-job --job-id <job-id>

# 自定义术语表
aws translate import-terminology --name product-terms \
  --merge-strategy OVERWRITE --terminology-data file://terms.json \
  --language-code en
```

## 最佳实践

- 交互式/UI 文本用实时 API；文档仓库用批量任务。
- 产品名和品牌语言导入自定义术语表；领域准确率用平行数据/ACT。
- 面向客户的内容做人工复核。
- 与 Comprehend 组合分析多语言文本情感/实体，用 Polly 生成音频。
- 用 IAM 角色和 KMS 加密保护 S3 桶；用 CloudWatch 监控任务。
- 按工作负载跟踪翻译字符量控制成本。

## 故障排查

| 症状 | 检查与处理 |
|---|---|
| 翻译失败 | 检查语言代码、文本长度限制和 API 配额。 |
| 术语表未生效 | 确认术语表已按源语言导入，且任务/API 使用它。 |
| 批量任务失败 | 核对 S3 路径、IAM 角色权限和受支持文档类型。 |
| 准确率问题 | 补充平行数据并重训 ACT 模型；常见术语用术语表。 |
| 不支持的语言对 | 查询受支持语言表确认所需语言对。 |

## 配额

每次请求文本长度、批量任务大小、每账户术语表数量和 API 请求速率有限制。以 Amazon Translate 端点和配额页面及 Service Quotas 控制台为准。

## 官方参考

- [什么是 Amazon Translate？- 开发者指南](https://docs.aws.amazon.com/translate/latest/dg/what-is.html)
- [Amazon Translate 端点和配额](https://docs.aws.amazon.com/general/latest/gr/translate.html)
- [Amazon Translate 定价](https://aws.amazon.com/translate/pricing/)
- [AWS CLI：translate 命令](https://docs.aws.amazon.com/cli/latest/reference/translate/)
