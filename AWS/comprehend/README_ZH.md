# Amazon Comprehend - Runbook 与参考

> 事实核对时间（对照 AWS 官方文档）：2026-08-19

## 概述

Amazon Comprehend 使用自然语言处理（NLP）从文档中提取洞察：实体、关键短语、语言、情感、语法和 PII。小型工作负载可实时分析，大型文档集可用异步任务；你还可以训练自定义分类和实体识别模型。

## 核心概念

- **洞察（Insights）**：预训练模型输出——实体（人、地点、组织）、关键短语、PII、主语言、情感（积极/中性/消极/混合）、定向情感（按实体的情感）和语法（词性）。
- **实时与异步**：小负载用 `Detect*` API；大型文档集用分析任务。
- **自定义分类**：使用 AutoML 构建的分类器，将文档组织到你的自定义类别。
- **自定义实体识别**：训练识别你特定术语和短语的识别器。
- **Flywheels**：随时间编排自定义模型新版本的训练与评估。
- **主题建模（文档聚类）**：按词频将语料组织为主题/聚类。
- **输入**：UTF-8 文本；自定义分类/实体识别还接受图片、PDF 和 Word 文件。
- **安全与成本**：输出和卷数据可用你的 KMS 密钥加密；按分析文档数及自定义模型训练/端点用量付费。

## 常用操作（AWS CLI）

```bash
# 实时分析
aws comprehend detect-sentiment --text "The service is excellent" \
  --language-code en
aws comprehend detect-entities --text "AWS announced new services in Singapore" \
  --language-code en
aws comprehend detect-pii-entities --text "Contact alice at 123-456-7890" \
  --language-code en

# 异步分析任务
aws comprehend start-dominant-language-detection-job \
  --job-name docs-lang --input-data-config S3Uri=s3://bucket/docs \
  --output-data-config S3Uri=s3://bucket/out
aws comprehend list-dominant-language-detection-jobs
```

## 最佳实践

- 文档存 S3 并用 KMS 加密任务与卷；IAM 角色限定所用桶。
- 实时 API 只用于交互式负载；批量分析用任务控制成本。
- 领域文本用有代表性的标注数据训练自定义分类器/识别器。
- 用 flywheels 管理模型版本与评估，而不是临时重训。
- 存储/发布文本前用 Comprehend PII 检测做脱敏或掩码。
- 与 Firehose、Lambda 和 EventBridge 组合实现实时文本管道。

## 故障排查

| 症状 | 检查与处理 |
|---|---|
| 任务失败 | 检查 S3 输入路径、IAM 角色权限和文档格式（UTF-8）。 |
| 语言未识别 | 确认功能支持该语言；主语言检测覆盖的语言多于其他功能。 |
| 自定义模型准确率低 | 增加有代表性的标注数据，用 flywheel 重训并评估。 |
| 端点成本高 | 删除空闲的自定义模型端点；批量工作负载用任务。 |
| 未检测到 PII | 确认文本语言受支持，并用正确的语言代码调用 `detect-pii-entities`。 |

## 配额

文档大小、批大小、自定义模型训练配额和 API 请求速率有限制。以 Amazon Comprehend 端点和配额页面及 Service Quotas 控制台为准。

## 官方参考

- [什么是 Amazon Comprehend？- 开发者指南](https://docs.aws.amazon.com/comprehend/latest/dg/what-is.html)
- [Amazon Comprehend 端点和配额](https://docs.aws.amazon.com/general/latest/gr/comprehend.html)
- [Amazon Comprehend 定价](https://aws.amazon.com/comprehend/pricing/)
- [AWS CLI：comprehend 命令](https://docs.aws.amazon.com/cli/latest/reference/comprehend/)
