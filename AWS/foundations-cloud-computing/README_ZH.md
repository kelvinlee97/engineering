# 云计算基础 - Runbook 与参考

> 事实核对时间（对照 AWS 官方文档）：2026-08-19

## 概述

云计算通过互联网按需交付 IT 资源，并按用即付定价。AWS 在全球基础设施上提供计算、存储、数据库、网络、分析等众多服务，将大额预付资本支出转化为随用量变化的可变成本。

## 核心概念

- **按需自助服务**：无需人工交互即可按需供给资源，用完释放。
- **按用即付**：只为你使用的内容付费，将资本支出转化为可变运营支出。
- **规模经济**：AWS 聚合大量客户需求，降低单位成本。
- **弹性与可扩展性**：按需上下/内外扩展容量；包括纵向（更大实例）和横向（更多实例）扩展。
- **高可用与容错**：跨可用区和区域设计，抵御故障。
- **全球基础设施**：区域（地理区域）、可用区（区域内隔离的数据中心）和边缘节点（内容分发）。
- **服务模型**：IaaS（EC2：基础设施）、PaaS（Elastic Beanstalk、RDS：托管平台）、SaaS（全托管应用）。
- **敏捷性**：借助自助基础设施和托管服务，更快开发、测试和部署。
- **共担责任**：AWS 负责云的安全；客户负责云中的安全（见共担责任模型 runbook）。

## 常用操作

基础是概念而非单一 API；这样落地：

```bash
# 示例：弹性与托管服务实践
aws ec2 describe-regions                          # 全球基础设施
aws autoscaling describe-auto-scaling-groups      # 弹性
aws elasticbeanstalk describe-applications        # PaaS 模型
aws lambda list-functions                         # 无服务器计算
```

## 最佳实践

- 为故障设计：多可用区/区域架构、健康检查和自动恢复。
- 使用弹性：用 Auto Scaling 和无服务器选项让容量匹配需求。
- 按工作负载选择正确的服务模型（IaaS/PaaS/SaaS），降低运维负担。
- 从第一天就用预算、标签和 Cost Explorer 跟踪成本。
- 设计新工作负载时遵循 Well-Architected Framework 支柱。

## 故障排查

| 症状 | 检查与处理 |
|---|---|
| 启动时容量意外 | 使用 Elastic Beanstalk/Auto Scaling，并在 staging 测试扩缩行为。 |
| 闲置资源推高成本 | 释放或缩容未使用资源；尽量使用托管/无服务器。 |
| 单点故障 | 跨可用区分布工作负载，并添加带健康检查的冗余。 |

## 配额

概念是通用性的；实际行为取决于服务配额和架构选择。以 AWS Cloud 概览和本知识库中各服务 runbook 为准。

## 官方参考

- [AWS Cloud 概览](https://docs.aws.amazon.com/whitepapers/latest/aws-overview/introduction.html)
- [AWS 全球基础设施](https://aws.amazon.com/about-aws/global-infrastructure/)
- [云计算类型](https://aws.amazon.com/types-of-cloud-computing/)
