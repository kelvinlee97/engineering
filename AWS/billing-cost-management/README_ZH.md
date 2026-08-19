# AWS Billing and Cost Management - Runbook 与参考

> 事实核对时间（对照 AWS 官方文档）：2026-08-19

## 概述

AWS Billing and Cost Management 是一套功能集合，用于设置账单、取回和支付发票，以及分析、组织、规划和优化成本。它涵盖账单与支付、成本分析、成本组织、预算与规划、节省与承诺，并通过 AWS Organizations 合并账单实现组织级集中管理。

## 核心概念

- **账单与支付**：月度账单、发票、采购订单、支付配置、抵扣额和账单偏好（邮件投递、告警、折扣共享）。
- **合并账单**：AWS Organizations 提供跨账户统一账单，聚合用量享受阶梯折扣和预留/Savings Plans 共享；无额外费用。
- **账单转移（Billing transfer）**：用一个账户管理并支付多个 AWS Organizations 的合并账单，将账单与安全/治理管理分离。
- **成本分析**：AWS Cost Explorer（可视化分析、预测、自定义报表）、数据导出（成本/用量数据集的自定义导出）、Cost Anomaly Detection、免费套餐监控，以及共享 ECS 资源的分摊成本数据。
- **成本组织**：成本类别（将成本映射到团队/应用/环境，支持分摊规则）和成本分配标签（按标签查看成本）。
- **预算与规划**：带阈值告警的成本/用量预算；控制台内 Pricing calculator 和公共 Pricing calculator 做估算。
- **节省与承诺**：Cost Optimization Hub（建议）、Savings Plans 和预留（EC2、RDS、Redshift、DynamoDB 等）管理。
- **Billing Conductor**：为合作伙伴/转售商提供自定义 showback/chargeback 账单，不改变 AWS 对你的计费方式。
- **Price List API**：编程获取当前定价数据（批量 JSON/CSV）。
- **IAM 访问**：默认 IAM 用户/角色无法访问账单控制台；需启用 Activate IAM Access 并授予权限。

## 常用操作（AWS CLI）

```bash
# 成本与用量
aws ce get-cost-and-usage --time-period Start=2026-08-01,End=2026-08-19 \
  --granularity MONTHLY --metrics UnblendedCost --group-by file://group.json
aws ce get-cost-forecast --time-period Start=2026-08-20,End=2026-09-19 \
  --granularity MONTHLY --metric UNBLENDED_COST

# 预算
aws budgets create-budget --account-id 123456789012 --budget file://budget.json \
  --notifications-with-subscribers file://notifications.json

# 数据导出与异常检测
aws bcm-data-exports list-exports
aws ce get-anomaly-subscriptions
```

## 最佳实践

- 在 Organizations 启用合并账单，并统一使用成本分配标签/成本类别。
- 设置多阈值预算告警，并启用 Cost Anomaly Detection。
- 定期查看 Cost Explorer 和 Cost Optimization Hub 建议（rightsizing、Savings Plans、预留）。
- 将成本/用量数据导出到数据仓库，做深入分析和预测。
- 用 IAM 限制账单控制台访问；根用户只做账单专属任务。
- 启动新工作负载前用 Pricing calculator 估算；合作伙伴场景用 Billing Conductor 做 showback/chargeback。

## 故障排查

| 症状 | 检查与处理 |
|---|---|
| 无法访问账单控制台 | 启用 Activate IAM Access，并为 IAM 主体授予所需账单权限。 |
| 标签不显示成本 | 在 Billing 中激活成本分配标签；只打标签不会自动拆分成本。 |
| 预算告警不触发 | 核对预算阈值、通知/订阅者和账户范围。 |
| 成员账户成本缺失 | 确认合并账单及 Cost Management 偏好中的关联账户数据。 |
| 预测不准 | 提供更长历史数据，检查预测粒度和时间范围。 |

## 配额

预算、数据导出和 API 请求速率有限制；访问取决于 IAM 和账户设置。以 AWS Billing 端点和配额页面及 Service Quotas 控制台为准。

## 官方参考

- [什么是 AWS Billing and Cost Management？- 用户指南](https://docs.aws.amazon.com/awsaccountbilling/latest/aboutv2/billing-what-is.html)
- [AWS Billing 端点和配额](https://docs.aws.amazon.com/general/latest/gr/billing.html)
- [AWS Cost Management](https://aws.amazon.com/aws-cost-management/)
- [AWS CLI：ce 和 budgets 命令](https://docs.aws.amazon.com/cli/latest/reference/ce/)
