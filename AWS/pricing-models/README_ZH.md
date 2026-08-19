# AWS 定价模式 - Runbook 与参考

> 事实核对时间（对照 AWS 官方文档）：2026-08-19

## 概述

AWS 服务按用即付（pay-as-you-go）定价：只为你使用的内容付费，无预付合同；通过承诺用量或使用闲置容量可以节省成本。理解定价模式（On-Demand、Savings Plans、预留实例、Spot 和免费套餐）有助于在满足可用性需求的同时控制成本。

## 核心概念

- **On-Demand**：按使用量付费（按秒/分钟/小时或按请求/存储单位，视服务而定），无承诺；灵活但单价最高。
- **Savings Plans**：承诺一定量的计算用量（1 或 3 年）换取低于 On-Demand 的价格，按计划类型在实例族/区域间有灵活性。
- **预留实例（Reserved Instances）**：承诺特定实例配置（1 或 3 年，Standard 或 Convertible）获得 EC2/RDS/Redshift 等折扣；有区域和可用区范围。
- **Spot 实例**：以显著折扣使用闲置 EC2 容量，适用于可容错、可中断的工作负载；容量可能被回收。
- **专用主机/实例**：满足许可和合规需要的物理隔离。
- **免费套餐**：符合条件服务在前 12 个月的有限免费额度、常青免费项和试用。
- **阶梯折扣**：组织内聚合用量（合并账单）可享受批量折扣。
- **数据传输**：出站数据传输和跨区域流量计费；入站通常免费。
- **Price List API**：编程查询当前服务定价（批量 JSON/CSV）。

## 常用操作

```bash
# Price List API 示例
aws pricing get-products --service-code AmazonEC2 \
  --filters 'Type=TERM_MATCH,Field=instanceType,Value=m5.large'

# 成本工具
aws ce get-cost-and-usage --time-period Start=2026-08-01,End=2026-08-19 \
  --granularity MONTHLY --metrics UnblendedCost
aws budgets create-budget --account-id 123456789012 --budget file://budget.json \
  --notifications-with-subscribers file://notifications.json
```

## 最佳实践

- 从 On-Demand 开始，稳定工作负载再购买 Savings Plans/预留实例。
- 无状态、可容错工作（批处理、CI、ML 训练）用 Spot，并处理中断。
- 用 Cost Explorer、预算和 Cost Anomaly Detection 跟踪用量和成本。
- 在 AWS Organizations 中合并账单，共享阶梯折扣和预留。
- 审查出站数据传输；必要时用 CloudFront/Direct Connect 降低成本。
- 构建前用 AWS Pricing Calculator 估算新工作负载。

## 故障排查

| 症状 | 检查与处理 |
|---|---|
| 账单高于预期 | 用 Cost Explorer 和数据导出找出主要服务；检查数据传输和低利用率资源。 |
| Savings Plans 未覆盖用量 | 在 Savings Plans 控制台检查覆盖/利用率，调整购买建议。 |
| Spot 实例被回收 | 确认工作负载处理中断（检查点、队列），或使用 Capacity Rebalancing。 |
| 免费套餐产生费用 | 确认服务/用量在免费额度内，且账户未超过 12 个月。 |
| API 价格看起来不对 | 按区域/条款属性过滤；Price List API 包含多个维度。 |

## 配额

定价模式和折扣因服务、区域和承诺条款而异。以 AWS 定价页面和 Price List API 文档为准。

## 官方参考

- [AWS 定价机制白皮书](https://docs.aws.amazon.com/whitepapers/latest/how-aws-pricing-works/introduction.html)
- [AWS 定价](https://aws.amazon.com/pricing/)
- [AWS Pricing Calculator](https://calculator.aws/)
- [AWS Price List API](https://docs.aws.amazon.com/awsaccountbilling/latest/aboutv2/using-pelong.html)
