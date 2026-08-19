# AWS Artifact - Runbook 与参考

> 事实核对时间（对照 AWS 官方文档）：2026-08-19

## 概述

AWS Artifact 提供按需下载 AWS 安全与合规文档，包括 ISO、PCI 和 SOC 报告，以及认证机构签发的证书。你还可以审查、接受并跟踪与 AWS 的协议（针对账户和整个组织），并使用 Assurance Assistant 回答合规与尽职调查问题。AWS Artifact 的文档和协议免费提供。

## 核心概念

- **合规报告**：可下载的报告，如 ISO、PCI DSS、SOC 1/2/3 以及按区域/服务的合规文档，可提交给审计机构。
- **协议（Agreements）**：AWS 协议（例如 Business Associate Addendum），按账户或跨组织审查、接受和跟踪。
- **Marketplace Vendor Insights**：获取在 AWS Marketplace 销售产品的独立软件供应商（ISV）的安全与合规文档。
- **Assurance Assistant**：基于 AWS 合规文档，以 AI 方式回答合规与尽职调查问题。
- **共担责任背景**：Artifact 文档证明 AWS 的控制措施；你仍需负责获取并出具自己组织的合规文档。

## 常用操作（AWS CLI）

```bash
# 列出和下载报告
aws artifact list-customer-agreements
aws artifact get-report --report-id <report-id>

# 管理协议
aws artifact list-agreements
aws artifact get-customer-agreement --agreement-id <agreement-id>
aws artifact accept-agreement --agreement-id <agreement-id>
```

## 最佳实践

- 每个审计周期下载最新报告；合规报告会定期重新发布，旧版本可能不被接受。
- 在管理账户集中接受和跟踪协议，使组织级协议可见。
- 用 Assurance Assistant 做初步尽职调查问题，再对照底层报告核实答案。
- 将 Artifact 文档与自身合规证据（AWS Config 规则、备份策略、访问审查）组合成完整审计包。
- 用 IAM 限制 Artifact 访问，并用 CloudTrail 监控下载。

## 故障排查

| 症状 | 检查与处理 |
|---|---|
| 找不到报告 | 核对报告 ID，以及你的账户是否有资格获取该报告/区域。 |
| 无法接受协议 | 确认具备所需 IAM 权限，且协议未被终止。 |
| 缺少供应商文档 | 从 AWS Marketplace 控制台进入该 ISV 的 Vendor Insights。 |
| Assurance Assistant 不可用 | 检查该功能是否已为你的账户/区域启用。 |
| 组织协议不可见 | 从管理账户管理组织级协议。 |

## 配额

AWS Artifact 的文档和协议免费；访问权限和 API 配额有限制。以 AWS Artifact 用户指南和 IAM 文档为准。

## 官方参考

- [什么是 AWS Artifact？- 用户指南](https://docs.aws.amazon.com/artifact/latest/ug/what-is-aws-artifact.html)
- [AWS Artifact 协议](https://docs.aws.amazon.com/artifact/latest/ug/managing-agreements.html)
- [AWS Artifact FAQ](https://aws.amazon.com/artifact/faq/)
- [AWS CLI：artifact 命令](https://docs.aws.amazon.com/cli/latest/reference/artifact/)
