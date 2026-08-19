# AWS Solutions Library（Solutions Implementations）- Runbook 与参考

> 事实核对时间（对照 AWS 官方文档）：2026-08-19

## 概述

AWS Solutions Library（原 AWS Solutions Implementations）为常见业务和技术用例提供经过验证的解决方案与指引。每个方案都由 AWS 架构师按可靠性、安全和成本效率审查，并附带可在你账户中部署的指引和代码。

## 核心概念

- **解决方案**：覆盖行业和技术用例（例如数据湖、安全、DevOps、分析）的打包参考实现。
- **部署资产**：方案包含 CloudFormation 模板和/或 CDK 代码，以及包含架构和运维细节的实施指南。
- **审查**：发布前由 AWS 架构师按可靠性、安全和成本最佳实践审查方案。
- **定制**：你可以 fork 并定制开源代码以适应环境。
- **与 AWS 其他资产的关系**：Solutions Library 与 AWS Solutions Constructs（预构建 CDK 模式）和 AWS Partner Consulting Offers（合作伙伴交付的咨询项目）互补。

## 常用操作

```bash
# 多数方案从方案库页面或通过 CloudFormation 部署
aws cloudformation describe-stacks --stack-name <solution-stack-name>
aws cloudformation list-stack-resources --stack-name <solution-stack-name>
```

## 最佳实践

- 部署前阅读实施指南；注意前提条件、区域和成本估算。
- 先在测试账户部署，再为生产定制代码（VPC、加密、日志）。
- 跟踪方案版本和 AWS 服务更新；库发布更新时重新部署或升级。
- 生产工作负载结合 Well-Architected Framework 评审。

## 故障排查

| 症状 | 检查与处理 |
|---|---|
| 部署失败 | 检查 CloudFormation 栈事件和实施指南中的前提条件。 |
| 区域限制 | 确认方案支持你的区域；部分方案使用可用性有限的服务。 |
| 升级后定制丢失 | 将自定义改动放在 fork 中，跟踪上游更新。 |

## 配额

方案是指导性资产；配额取决于其部署的底层 AWS 服务。以 AWS Solutions Library 页面的最新方案列表和本知识库中各服务 runbook 的配额为准。

## 官方参考

- [AWS Solutions Library](https://aws.amazon.com/solutions/)
- [AWS Solutions Constructs](../solutions-constructs/README_ZH.md)
- [AWS Well-Architected Framework](../well-architected/README_ZH.md)
