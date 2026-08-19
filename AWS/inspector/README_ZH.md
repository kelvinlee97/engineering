# Amazon Inspector - Runbook 与参考

> 事实核对时间（对照 AWS 官方文档）：2026-08-19

## 概述

Amazon Inspector 是一项漏洞管理服务，自动发现工作负载并持续扫描软件漏洞和意外网络暴露。它扫描 EC2 实例、Amazon ECR 中的容器镜像和 Lambda 函数，并生成带有修复建议和环境特定风险评分的 finding。

## 核心概念

- **Finding**：检测到的漏洞或网络暴露的详细报告，包含严重性、受影响资源和修复建议；修复完成后 Inspector 会自动关闭 finding。
- **持续扫描**：Inspector 自动发现符合条件的资源，并在安装/修补软件包或发布影响资源的新 CVE 时自动重新扫描。
- **风险评分**：使用 CVSS 并结合你的环境上下文（网络可达性、可利用性）定制的严重性评分。
- **覆盖范围与仪表盘**：查看扫描覆盖、最关键 finding 和受影响资源；可生成 CSV/JSON 报告。
- **委派管理员**：通过 AWS Organizations，由一个账户集中启用和管理成员账户的 Inspector。
- **集成**：finding 发布到 Amazon EventBridge 和 AWS Security Hub CSPM，支持近实时响应。
- **抑制规则**：按条件过滤不想要的 finding。

## 常用操作（AWS CLI）

```bash
# 启用 Inspector（扫描类型：EC2、ECR、Lambda）
aws inspector2 enable --resource-types EC2 ECR LAMBDA \
  --account-ids 123456789012

# 列出 finding 和覆盖范围
aws inspector2 list-findings --filter-criteria '{"severity":[{"comparison":"EQUALS","value":"CRITICAL"}]}'
aws inspector2 list-coverage --account-id 123456789012

# 生成 finding 报告
aws inspector2 get-findings-report --report-format CSV \
  --s3-url s3://reports-bucket/inspector/ \
  --report-file-name inspector-findings

# 禁用扫描类型
aws inspector2 disable --resource-types EC2
```

## 最佳实践

- 通过委派管理员在整个组织启用 Inspector，新账户和新资源自动纳入覆盖。
- 扫描全部三种资源类型（EC2、ECR、Lambda），并按计划审查关键/高危 finding。
- 使用风险评分和仪表盘优先处理真正可利用且有暴露的 finding，而不只是原始 CVSS。
- 将 finding 路由到 EventBridge 实现自动响应（隔离、工单），并接入 Security Hub CSPM 聚合安全态势。
- 对已接受的风险使用抑制规则并记录；保持扫描覆盖率高。
- 修复并验证：只有确认修复后才关闭 finding（Inspector 在解决后会自动关闭）。

## 故障排查

| 症状 | 检查与处理 |
|---|---|
| 没有资源被扫描 | 确认已为对应扫描类型启用 Inspector、账户为成员，且 EC2 上运行 SSM Agent（无代理扫描选项同样适用）。 |
| Lambda 缺少 finding | 确认已启用 Lambda 扫描，且函数使用受支持的运行时。 |
| ECR 镜像未扫描 | 检查仓库，确认镜像是启用扫描后推送的（扫描时或持续扫描）。 |
| 委派管理员不工作 | 在 AWS Organizations 中指定委派管理员，并从该账户启用服务。 |
| Security Hub CSPM 中没有 finding | 在同一区域启用 Security Hub CSPM 的 Inspector 集成。 |

## 配额

Finding 保留期、API 请求速率以及每账户/资源扫描配额有限制。以 Amazon Inspector 端点和配额页面及 Service Quotas 控制台为准。

## 官方参考

- [什么是 Amazon Inspector？- 用户指南](https://docs.aws.amazon.com/inspector/latest/user/what-is-inspector.html)
- [Amazon Inspector 端点和配额](https://docs.aws.amazon.com/general/latest/gr/inspector.html)
- [Amazon Inspector 定价](https://aws.amazon.com/inspector/pricing/)
- [AWS CLI：inspector2 命令](https://docs.aws.amazon.com/cli/latest/reference/inspector2/)
