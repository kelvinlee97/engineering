# AWS Health - Runbook 与参考

> 事实核对时间（对照 AWS 官方文档）：2026-08-19

## 概述

AWS Health 提供 AWS 服务与账户的性能和可用性可见性。它通过事件通知服务中断、计划变更和账户通知，帮助你为计划活动做准备、排查进行中的问题并自动化响应。AWS Health Dashboard 对所有客户免费提供。

## 核心概念

- **健康事件（Health events）**：关于服务问题、计划维护和可能影响资源的账户特定事件的通知。
- **AWS Health Dashboard**：查看影响你账户事件的控制台；无需设置或编写代码。
- **EventBridge**：所有客户可免费通过 Amazon EventBridge 接收 AWS Health 事件；用规则触发自动化和告警。
- **AWS Health API**：编程访问，用于集成内部/第三方系统；需 Business Support+（部分地区 Business/Enterprise 计划）及以上。
- **事件类型**：账户通知（安全、账单）、计划变更和进行中的服务事件；每个事件可包含受影响资源和指导。

## 常用操作（AWS CLI）

```bash
# 查看健康事件（API 需要相应支持计划）
aws health describe-events --filter file://filter.json \
  --region us-east-1
aws health describe-event-details --event-arns <event-arn>
aws health describe-affected-entities --event-arns <event-arn>

# EventBridge 集成：使用默认事件总线
# 规则模式：{"source": ["aws.health"], "detail-type": ["AWS Health Event"]}
aws events put-rule --name aws-health-alerts \
  --event-pattern '{"source":["aws.health"]}'
```

## 最佳实践

- 通过 EventBridge 订阅所有账户/区域的 AWS Health 事件，并路由到 SNS/Slack/事件工具。
- 在运维工具中集成 Health API，建立统一事件视图。
- 及早监控计划变更和账户通知，避免维护窗口打乱计划。
- 组合 Health 事件、CloudWatch 告警和 Trusted Advisor，区分 AWS 侧与账户侧问题。
- 事件期间查看事件指导和受影响资源列表以界定影响范围。
- 组织场景使用组织级健康可见性，让管理账户看到成员事件。

## 故障排查

| 症状 | 检查与处理 |
|---|---|
| 看不到事件 | 确认区域和账户过滤；仪表盘按账户展示。 |
| EventBridge 规则不触发 | 检查事件模式（`aws.health` source）和规则目标权限。 |
| API 访问被拒 | 核对支持计划和 `health:DescribeEvents` 的 IAM 权限。 |
| 事件详情缺失 | 用 `describe-event-details` 并检查受影响实体界定范围。 |
| 通知延迟 | Health 事件接近实时，但部分事件类型在验证后发布；最快投递用 EventBridge。 |

## 配额

Dashboard 和 EventBridge 事件免费；Health API 有请求速率配额，并需符合条件的支持计划。以 AWS Health 端点和配额页面为准。

## 官方参考

- [什么是 AWS Health？- 用户指南](https://docs.aws.amazon.com/health/latest/ug/what-is-aws-health.html)
- [AWS Health 端点和配额](https://docs.aws.amazon.com/general/latest/gr/health.html)
- [AWS Health API 参考](https://docs.aws.amazon.com/health/latest/APIReference/Welcome.html)
- [AWS CLI：health 命令](https://docs.aws.amazon.com/cli/latest/reference/health/)
