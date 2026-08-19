# AWS Consulting Offers - Runbook 与参考

> 事实核对时间（对照 AWS 官方文档）：2026-08-19

## 概述

AWS Consulting Offers 是 AWS 合作伙伴提供的打包咨询项目，针对特定业务结果（例如迁移、现代化、安全评估和数据分析）。它们是 AWS Partner Network（APN）和 AWS Marketplace 生态的一部分，让客户以有界、可重复的方式采购合作伙伴专业服务。

## 核心概念

- **咨询项目（Consulting offers）**：来自 AWS 合作伙伴、范围固定并带明确交付物和结果的咨询项目，可被发现和采购。
- **合作伙伴生态**：项目来自经验证的 AWS 合作伙伴；能力项目（competencies）验证合作伙伴在解决方案领域的专业能力。
- **发现**：在 AWS Marketplace 和 AWS Partner 资源中浏览项目；可按用例、行业和合作伙伴过滤。
- **采购与执行**：购买项目、与合作伙伴接洽，并按约定范围跟踪交付物。
- **与 AWS 资产的关系**：Consulting Offers 与 AWS Solutions Library（可自助部署的代码）和 Solutions Constructs（CDK 模式）互补；合作伙伴提供咨询层。

## 常用操作

咨询项目通过合作伙伴/Marketplace 流程采购，而非 AWS CLI：

```bash
# 用 AWS Marketplace 目录 API 发现项目和卖家
aws marketplace-catalog list-entities --catalog AWSMarketplace --entity-type DataProduct
aws marketplace-catalog describe-entity --catalog AWSMarketplace --entity-id <entity-id>
```

## 最佳实践

- 采购前明确预期结果和交付物；让项目匹配具体业务需求。
- 接洽前验证合作伙伴资质（能力、客户案例）。
- 就项目中的访问、安全和数据处理要求达成一致。
- 自助实现先使用 AWS Solutions Library；有界的咨询工作再找合作伙伴。

## 故障排查

| 症状 | 检查与处理 |
|---|---|
| 找不到项目 | 放宽 AWS Marketplace 过滤条件；检查合作伙伴官网是否有直接项目。 |
| 项目范围不匹配 | 采购前与合作伙伴确认交付物和排除项。 |
| 交付物不明确 | 参考项目描述和约定的工作说明书（SOW）。 |

## 配额

咨询项目受合作伙伴协议和 Marketplace 条款约束；技术配额取决于涉及的 AWS 服务。以 AWS Partner Network 和 Marketplace 文档为准。

## 官方参考

- [AWS Partner Network](https://aws.amazon.com/partners/)
- [AWS Marketplace](https://aws.amazon.com/marketplace)
- [AWS Partner competencies](../certifications/competencies/README_ZH.md)
- [AWS Solutions Library](../solutions-implementations/README_ZH.md)
