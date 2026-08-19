# AWS Trusted Advisor - Runbook 与参考

> 事实核对时间（对照 AWS 官方文档）：2026-08-19

## 概述

AWS Trusted Advisor 检查你的 AWS 环境，并推荐省钱、提升可用性与性能、以及消除安全差距的措施。它按五个类别检查账户是否符合最佳实践：成本优化、安全、容错、性能和服务配额。

## 核心概念

- **检查项（Checks）**：按类别自动执行的 Best practice 评估（例如 EC2 实例利用率低、根账户启用 MFA、RDS 备份启用、服务配额使用情况）。
- **支持计划与访问**：全部检查以及 Trusted Advisor API 需要 AWS Business Support+、Enterprise Support 或 AWS Unified Operations；Basic Support 提供服务配额检查以及部分安全/容错检查，安全类检查需手动刷新。
- **控制台**：Trusted Advisor 控制台显示检查状态（绿/红/黄）和建议操作；可手动刷新检查。
- **API 与 EventBridge**：Business Support+ 及以上可通过 Support API 读取检查结果，并用 Amazon EventBridge 监控状态变化。
- **服务配额**：服务配额类别跟踪你的用量与配额，并在接近限制前提醒。

## 常用操作（AWS CLI）

```bash
# 列出可用检查项
aws support describe-trusted-advisor-checks --language en

# 刷新检查并读取结果
aws support refresh-trusted-advisor-check --check-id <check-id>
aws support describe-trusted-advisor-check-result --check-id <check-id>

# 所有检查的摘要
aws support describe-trusted-advisor-check-summaries \
  --check-ids <check-id-1> <check-id-2>
```

## 最佳实践

- 按计划定期审查 Trusted Advisor，并为每条建议指定负责人。
- 优先处理安全和配额类检查；先处理关键问题（例如根账户 MFA、开放的安全组）。
- 用 API/EventBridge 集成跟踪状态变化并自动告警。
- 重大变更后（扩缩、新账户、安全组变更）刷新检查，确认修复生效。
- 结合 AWS Config 和 Security Hub CSPM 做持续合规，而不只依赖 Trusted Advisor 的检查。

## 故障排查

| 症状 | 检查与处理 |
|---|---|
| 无法访问全部检查 | 确认支持计划；完整检查和 API 需要 Business Support+ 及以上。 |
| 检查结果过期 | 刷新对应检查；Basic Support 的安全检查需要手动刷新。 |
| API 访问被拒 | 核对 IAM 对 `support:DescribeTrustedAdvisorChecks` 等相关操作的权限。 |
| EventBridge 未收到事件 | 启用 Trusted Advisor 集成，并检查所在区域的事件模式。 |
| 配额检查过期 | Trusted Advisor 的配额数据周期性刷新；与 Service Quotas 控制台核对。 |

## 配额

Trusted Advisor 的可用性取决于 AWS Support 计划，API 请求速率有限制。以 AWS Support API 参考和你的支持计划为准。

## 官方参考

- [AWS Trusted Advisor](https://docs.aws.amazon.com/awssupport/latest/user/trusted-advisor.html)
- [AWS Trusted Advisor API 参考](https://docs.aws.amazon.com/awssupport/latest/APIReference/API_DescribeTrustedAdvisorChecks.html)
- [AWS Support 定价与计划](https://aws.amazon.com/premiumsupport/plans/)
