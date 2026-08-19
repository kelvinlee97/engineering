# AWS Application Migration Service（MGN）- Runbook 与参考

> 事实核对时间（对照 AWS 官方文档）：2026-08-19

## 概述

AWS Application Migration Service（MGN，官方文档现称 AWS Transform MGN）自动化将物理、虚拟和云服务器迁移到 AWS，停机时间极短，通常切换窗口只有几分钟。MGN 对源服务器执行持续块级复制，转换为可在 AWS 启动的实例，并通过模板、应用程序和 wave 支持大规模迁移。

## 核心概念

- **源服务器（Source server）**：被迁移的本地、虚拟或云服务器；安装 MGN 代理开始复制。
- **复制（Replication）**：持续块级复制到账户内的 staging 区域；无需停止源即可准备目标。
- **模板（Templates）**：复制、启动和后启动模板控制服务器如何复制、启动及迁移后配置；可针对单台服务器覆盖设置。
- **Applications 与 Waves**：将服务器分组为 application，再分组为 wave，批量执行动作（launch、cutover、archive）。
- **Cutover**：受控切换，停止复制并启动迁移实例（通常几分钟）；测试启动（蓝绿）在切换前验证。
- **操作系统与网络支持**：Windows Server 和多种 Linux 发行版；IPv4 和 IPv6；标准可用区和 Local Zones。

## 常用操作（CLI）

```bash
# 列出源服务器并启动复制
aws mgn list-source-servers --filters '{"isArchived":["false"]}'
aws mgn start-replication --source-server-id <source-server-id>

# 测试启动然后切换
aws mgn start-test --source-server-ids <source-server-id>
aws mgn describe-launch-configuration-templates
aws mgn start-cutover --source-server-ids <source-server-id>

# 收尾和管理
aws mgn finalize-cutover --source-server-id <source-server-id>
aws mgn archive-application --application-id <application-id>
```

## 最佳实践

- 批量切换前对代表性服务器做测试迁移；用测试启动验证启动、网络和应用。
- 按依赖和业务优先级规划 wave；不要乱序切换有依赖的服务器。
- 用启动模板保持实例配置一致，用后启动模板在启动后安装代理/配置。
- staging 区域网络隔离，MGN 角色遵循最小权限 IAM。
- 监控复制健康（滞后、失败），在切换窗口前修复磁盘/网络问题。
- 切换后跑完应用正常检查，再 finalize 并归档源。

## 故障排查

| 症状 | 检查与处理 |
|---|---|
| 复制滞后 | 检查源网络带宽、磁盘 I/O 和源上的代理状态。 |
| 测试启动失败 | 检查启动模板设置、AMI/目标子网和后启动脚本。 |
| 代理未安装 | 在源安装 MGN 代理，确认可连接 AWS 端点。 |
| 切换失败 | 核对 staging 区域、复制健康和源未被归档。 |
| 应用未迁移 | 检查 application/wave 成员关系及切换顺序。 |

## 配额

每账户源服务器数、并发启动数和 API 请求速率有限制。以 AWS Application Migration Service 端点和配额页面及 Service Quotas 控制台为准。

## 官方参考

- [什么是 AWS Transform MGN？- 用户指南](https://docs.aws.amazon.com/mgn/latest/ug/what-is-application-migration-service.html)
- [AWS Application Migration Service 端点和配额](https://docs.aws.amazon.com/general/latest/gr/mgn.html)
- [AWS Application Migration Service 定价](https://aws.amazon.com/application-migration-service/pricing/)
- [AWS CLI：mgn 命令](https://docs.aws.amazon.com/cli/latest/reference/mgn/)
