# AWS Managed Services（AMS）- Runbook 与参考

> 事实核对时间（对照 AWS 官方文档）：2026-08-19

## 概述

AWS Managed Services（AMS）是企业级服务，持续管理你的 AWS 基础设施：供给、运行、监控、补丁、安全和备份，遵循 AWS 最佳实践和 ITSM 流程。AMS 落实变更管理和安全策略，让你的团队专注构建应用。注意：AWS 已宣布 AMS Advanced 将于 2027 年 6 月 30 日停止支持，请提前规划。

## 核心概念

- **Landing zone**：AMS 接入环境；单账户或多账户架构，应用 AMS 基线和护栏。
- **变更请求**：AMS 通过受控的请求流程（含带审批门的自有变更）处理并实施环境变更。
- **运维**：7x24 监控、补丁管理、安全监控、备份和事件响应均包含在服务中。
- **ITSM 对齐**：AMS 遵循 IT 服务管理实践，使 IT 服务与业务需求一致。
- **服务请求**：提交新功能或改进的服务请求，由 AWS 评估。
- **停止支持（AMS Advanced）**：2027 年 6 月 30 日之后，AMS Advanced 控制台和资源将不可访问；查看 AWS 过渡指引。

## 常用操作

AMS 通过其控制台和服务请求流程运营，而不是客户直接运行 API。管理员使用：

- AMS 控制台处理变更请求、服务请求和环境状态。
- AWS Service Catalog 和 CloudFormation 产品管理已供给的基础设施。
- 自有账户进行应用开发与部署，同时受 AMS 托管护栏约束。

## 最佳实践

- 使用多账户 landing zone 隔离环境，与 AMS 托管控制对齐。
- 基础设施变更走 AMS 变更流程，保持护栏和合规完好。
- 保持 AMS 拥有的基线（监控、补丁、备份）已配置，并定期查看仪表盘。
- 应用部署接入自有 CI/CD，仅使用 AMS 支持的服务。
- 跟踪 AMS Advanced 停止支持时间线，在 2027 年 6 月 30 日前规划迁移/过渡。

## 故障排查

| 症状 | 检查与处理 |
|---|---|
| 变更请求被拒 | 对照 AMS 策略检查请求详情，修正范围/审批后重新提交。 |
| 监控告警 | 在 AMS 仪表盘查看受影响资源，并按变更门户中的 runbook 处理。 |
| 补丁未应用 | 确认 AMS 控制台中的维护窗口和补丁基线。 |
| 资源访问被拒 | AMS 使用托管角色；通过 AMS 变更流程请求变更。 |
| AMS Advanced 停止支持 | 查看 AWS 过渡指引，在 2027 年 6 月 30 日前迁移托管工作负载。 |

## 配额

AMS 是企业级产品，有接入和运营协议；支持的区域和操作系统以 AWS 文档为准。以 AMS 用户指南的当前受支持配置为准。

## 官方参考

- [什么是 AWS Managed Services？- 用户指南](https://docs.aws.amazon.com/managedservices/latest/userguide/what-is-ams.html)
- [AWS Managed Services 用户指南](https://docs.aws.amazon.com/managedservices/latest/userguide/welcome.html)
- [AWS Managed Services 定价](https://aws.amazon.com/managed-services/pricing/)
