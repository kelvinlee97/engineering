# AWS Systems Manager - Runbook 与参考

> 事实核对时间（对照 AWS 官方文档）：2026-08-19

## 概述

AWS Systems Manager 帮助你跨 AWS、本地和多云环境集中查看、管理和操作节点。节点安装 SSM Agent 并注册为托管节点后，你可以使用 Run Command、Session Manager、Patch Manager、Parameter Store、Automation 和 OpsCenter 等工具，而无需登录服务器。

## 核心概念

- **托管节点**：安装了 SSM Agent 并能访问 Systems Manager 的 EC2 实例、本地服务器和边缘设备。
- **Run Command**：无需 SSH/RDP 即可在多个节点上批量运行脚本/命令。
- **Session Manager**：安全、可审计的交互式 Shell（无需开放入站端口，无需堡垒机）。
- **Patch Manager**：定义补丁基线并按规模应用操作系统补丁；报告合规性。
- **Automation**：运行预定义或自定义 runbook（SSM 文档）执行运维任务和修复。
- **Parameter Store**：集中、带版本管理的配置与密钥存储（明文或使用 KMS 的 SecureString）。
- **State Manager**：按计划维护一致的节点状态。
- **Inventory**：收集节点元数据（操作系统、补丁、应用程序）。
- **OpsCenter / OpsItems**：聚合运维问题并执行修复。

## 常用操作（AWS CLI）

```bash
# 列出托管节点
aws ssm describe-instance-information

# 在目标实例上运行命令
aws ssm send-command --document-name "AWS-RunShellScript" \
  --targets "Key=instanceids,Values=i-0123456789abcdef0" \
  --parameters '{"commands":["df -h","uptime"]}'
aws ssm get-command-invocation --command-id <command-id> --instance-id i-0123456789abcdef0

# 启动会话（需要 Session Manager 权限）
aws ssm start-session --target i-0123456789abcdef0

# 参数
aws ssm put-parameter --name /app/config/db-url --value "postgresql://db.internal:5432" --type String
aws ssm put-parameter --name /app/config/api-key --value "$(openssl rand -hex 32)" --type SecureString
aws ssm get-parameter --name /app/config/db-url

# Automation
aws ssm start-automation-execution --document-name "AWS-StopEC2Instance" \
  --parameters '{"InstanceId":["i-0123456789abcdef0"]}'
```

## 最佳实践

- 安装最新 SSM Agent，并为节点授予带 AmazonSSMManagedInstanceCore 策略的 IAM 角色。
- 使用 Session Manager 替代 SSH/RDP，并记录会话（S3 或 CloudWatch Logs）用于审计。
- 配置使用 Parameter Store；密钥用 SecureString（KMS），或优先使用 Secrets Manager。
- 用维护窗口应用补丁基线，并持续报告合规性。
- Automation runbook 使用 run-as 角色权限，先小范围测试再大规模执行。
- 用 IAM 和 SCP 限制控制平面操作（SendCommand、StartSession）。
- 监控托管节点健康状态，节点失管时设置告警。

## 故障排查

| 症状 | 检查与处理 |
|---|---|
| 节点未托管 | 确认 SSM Agent 已安装/运行、实例角色已附加、出站访问 SSM 端点正常。 |
| 命令超时 | 检查网络连通性、代理版本和命令输出大小。 |
| 会话无法启动 | 核对 Session Manager 配置、IAM 权限以及 SSM VPC 端点（或 NAT）。 |
| 找不到参数 | 检查路径、参数名及参数上的 IAM 权限。 |
| 补丁未应用 | 核对补丁基线、维护窗口和节点注册状态。 |

## 配额

托管节点数、并发命令数、参数吞吐量和文档大小都有配额。以 Service Quotas 控制台为准。

## 官方参考

- [什么是 AWS Systems Manager？- Systems Manager 用户指南](https://docs.aws.amazon.com/systems-manager/latest/userguide/what-is-systems-manager.html)
- [AWS Systems Manager 配额](https://docs.aws.amazon.com/general/latest/gr/ssm.html)
- [AWS Systems Manager 定价](https://aws.amazon.com/systems-manager/pricing/)
- [AWS CLI：ssm 命令](https://docs.aws.amazon.com/cli/latest/reference/ssm/)
