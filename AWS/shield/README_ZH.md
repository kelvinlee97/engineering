# AWS Shield - Runbook 与参考

> 事实核对时间（对照 AWS 官方文档）：2026-08-19

## 概述

AWS Shield 是托管的分布式拒绝服务（DDoS）防护服务。**Shield Standard** 对所有 AWS 客户自动启用、无需额外费用，可防护常见的网络层容量攻击（例如 UDP 反射攻击和 TCP SYN 洪水）。**Shield Advanced** 是付费层级，提供更强的检测与缓解、防护组（protection group）、基于健康检查的检测、成本保护以及 AWS Shield Response Team（SRT）支持。

## Shield Standard 与 Shield Advanced

| 能力 | Shield Standard | Shield Advanced |
|---|---|---|
| 费用 | 包含在 AWS 中 | 付费订阅加数据传输费 |
| 自动防护 | AWS 边缘（CloudFront、Route 53 等）的常见网络层 DDoS | Standard 防护外加增强缓解 |
| 保护具体资源 | 不适用 | 按资源 ARN 添加防护 |
| 可见性与检测 | 基础 | 近实时指标与基于健康检查的检测 |
| 应急响应 | 自助 | AWS Shield Response Team（SRT）与 DDoS 成本保护 |
| Web 层攻击 | 需要 AWS WAF | 推荐配合 AWS WAF |

## 核心概念

- **网络层容量攻击**：耗尽带宽（UDP 反射、SYN 洪水），大多被 AWS 边缘吸收。
- **状态耗尽 / 应用层攻击**：针对连接状态或应用本身，用 Shield Advanced 与 AWS WAF 缓解。
- **防护（Protection）**：Shield Advanced 针对某个资源 ARN 的监控配置，例如 CloudFront 分发、Route 53 托管区、Global Accelerator、弹性 IP 和负载均衡器。
- **防护组（Protection group）**：聚合多个防护以便统一监控和响应；模式包括 `ALL`、`ARBITRARY` 和 `BY_RESOURCE_TYPE`。
- **基于健康检查的检测**：利用 Route 53 健康检查和 CloudWatch 指标识别影响可用性的攻击。
- **成本保护**：在检测到的攻击期间产生的扩容和数据传输费用可获得抵扣或退款。

## 常用操作（AWS CLI）

```bash
# 列出已有防护
aws shield list-protections

# 为资源添加防护
aws shield create-protection --name web-prod --resource-arn <resource-arn>

# 查看或更新防护
aws shield describe-protection --protection-id <protection-id>
aws shield update-protection --protection-id <protection-id> --name web-prod-new

# 防护组
aws shield create-protection-group --protection-group-id web-tier --aggregation SUM --pattern ALL
aws shield list-protection-groups

# 移除防护
aws shield delete-protection --protection-id <protection-id>
```

## 最佳实践

- 按 DDoS 韧性设计架构：流量放在 CloudFront、Global Accelerator 或负载均衡器后面，绝不公开源站 IP。
- 对业务关键、面向客户的应用启用 Shield Advanced，并为每个相关资源 ARN 添加防护。
- 配合 AWS WAF（托管规则组、速率规则）防护应用层攻击。
- 配置 Route 53 健康检查与基于健康检查的检测，并设置 CloudWatch 告警和 EventBridge 响应。
- 攻击进行中通过 AWS Support（Business 或 Enterprise）联系 Shield Response Team。
- 定期检查每个账号和区域的防护、防护组与覆盖范围。

## 故障排查

| 症状 | 检查与处理 |
|---|---|
| 攻击打到源站 | 确认源站 IP 未暴露；所有流量经过 CloudFront/ALB/Global Accelerator，并限制直连。 |
| Shield Advanced 未检测到攻击 | 确认资源 ARN 已受保护，健康检查/指标已配置且正常。 |
| 攻击期间成本飙升 | 启用成本保护和账单告警；事后核查用量。 |
| 应用层攻击仍然成功 | 添加 AWS WAF 速率规则和托管规则组；保持资源由 Shield Advanced 保护。 |
| 事件期间响应缓慢 | 通过 AWS Support 联系 SRT，并提供时间线、指标和日志。 |

## 配额

Shield Advanced：每账号每资源类型最多 1,000 个受保护资源（可调整）、最多 100 个防护组、每个防护组最多 1,000 个单独列出的成员。以 Service Quotas 控制台当前值为准。

## 官方参考

- [AWS Shield - WAF 与 Shield 开发者指南](https://docs.aws.amazon.com/waf/latest/developerguide/shield-chapter.html)
- [AWS Shield Advanced 配额](https://docs.aws.amazon.com/waf/latest/developerguide/shield-limits.html)
- [AWS Shield 定价](https://aws.amazon.com/shield/pricing/)
- [AWS CLI：shield 命令](https://docs.aws.amazon.com/cli/latest/reference/shield/)
