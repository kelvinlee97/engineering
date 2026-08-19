# AWS Solutions Constructs - Runbook 与参考

> 事实核对时间（对照 AWS 官方文档）：2026-08-19

## 概述

AWS Solutions Constructs 是 AWS Cloud Development Kit（AWS CDK）的开源扩展。它提供预构建、良好架构的模式，将 AWS 服务组合成常见用例，让你用熟悉的编程语言和现有开发工作流定义基础设施。

## 核心概念

- **Constructs**：跨 AWS 服务执行常见操作的可复用、良好架构模式（例如 API Gateway + Lambda + DynamoDB、S3 + Lambda）。
- **语言**：目前支持 TypeScript、JavaScript、Python 和 Java。
- **基于 CDK**：construct 是 CDK 构造库；可以使用逻辑、面向对象建模和代码评审流程。
- **目录**：浏览完整 construct 目录，查找适合你用例的模式。
- **复用与共享**：将解决方案组织为逻辑模块，在团队/公司内共享为库并发布。
- **测试**：在现有 CI/CD 中用行业标准协议测试基础设施代码。

## 常用操作

```bash
# 示例：向 CDK 应用添加 constructs（Python）
mkdir constructs-app && cd constructs-app
cdk init app --language python
pip install aws-solutions-constructs.aws-lambda-s3
# 在 app.py 中导入 constructs，然后合成并部署
cdk synth
cdk deploy
```

## 最佳实践

- 常见、经过良好测试的模式优先使用 constructs，而不是手动拼接服务。
- 部署前检查 construct 的选项和默认值（加密、日志）以及成本。
- 保持 construct 库更新；跟进上游发布以获取修复和新模式。
- 将 constructs 与自有 CDK 抽象组合，满足组织特定需求。
- 生产部署前在 staging 测试合成的模板。

## 故障排查

| 症状 | 检查与处理 |
|---|---|
| 找不到 construct | 核对包名/语言以及 construct 目录中的可用性。 |
| 合成失败 | 检查 CDK 版本、construct 版本兼容性，以及 TypeScript/Python 语法。 |
| 出现意外资源 | 查看 construct 默认值和 props；用自有设置覆盖。 |
| 区域相关错误 | 确认 construct 所用的服务在目标区域可用。 |

## 配额

Constructs 是代码库；配额取决于所用 AWS 服务。以各模式的 construct 文档和本知识库中各服务 runbook 的配额为准。

## 官方参考

- [AWS Solutions Constructs](https://docs.aws.amazon.com/solutions/latest/constructs/welcome.html)
- [AWS CDK 开发者指南](../cdk/README_ZH.md)
- [AWS Solutions Constructs 目录](https://docs.aws.amazon.com/solutions/latest/constructs/construct-library.html)
