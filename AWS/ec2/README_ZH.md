# Amazon EC2 - Runbook 与参考

> 事实核对时间（对照 AWS 官方文档）：2026-08-18

## 概述

Amazon Elastic Compute Cloud（Amazon EC2）在 AWS 云中提供按需、可扩展的计算容量。EC2 实例就是一台虚拟服务器；你选择的实例类型决定了它可用的计算、内存、网络和存储资源的配比。

## 实例生命周期与计费

| 状态 | 含义 | 实例使用计费 |
|------|------|-------------|
| `pending` | 实例正在准备进入 `running` | 不计费 |
| `running` | 实例运行中、可用 | 按秒计费，最少 1 分钟 |
| `stopping` | 实例正在停止 | 不计费（仅休眠时停止过程计费） |
| `stopped` | 实例已关机，可重新启动 | 不计费（EBS 卷和弹性 IP 仍计费） |
| `shutting-down` | 实例正在终止 | 不计费 |
| `terminated` | 实例已永久删除 | 不计费 |

- **重启（Reboot）**：实例留在同一台宿主机，保留公有 DNS 名和私有 IP，实例存储数据保留；不会开启新的计费周期。
- **停止/启动（仅 EBS 根卷实例）**：实例迁移到新宿主机，保留私有 IPv4 和弹性 IP；若没有关联弹性 IP，公有 IPv4 会变化。实例存储数据会被清除。
- **休眠（Hibernate，仅 EBS 根卷实例）**：内存内容保存到 EBS 根卷；`stopping` 过程计费，`stopped` 后不计费。
- **终止（Terminate）**：永久删除、不可恢复。根 EBS 卷默认随实例删除（`DeleteOnTermination`），其他卷保留；`InstanceInitiatedShutdownBehavior` 决定 OS 关机是停止还是终止实例（EBS 根卷默认停止）。

## 常用操作（AWS CLI）

```bash
# 启动实例
aws ec2 run-instances --image-id ami-0123456789abcdef0 \
  --instance-type t3.micro --key-name my-key \
  --security-group-ids sg-0123456789abcdef0 --subnet-id subnet-0123456789abcdef0

# 列出运行中的实例
aws ec2 describe-instances \
  --filters "Name=instance-state-name,Values=running" \
  --query 'Reservations[].Instances[].[InstanceId,InstanceType,PublicIpAddress]' \
  --output table

# 启动 / 停止 / 重启 / 终止
aws ec2 start-instances --instance-ids i-0123456789abcdef0
aws ec2 stop-instances --instance-ids i-0123456789abcdef0
aws ec2 reboot-instances --instance-ids i-0123456789abcdef0
aws ec2 terminate-instances --instance-ids i-0123456789abcdef0

# 状态检查和打标签
aws ec2 describe-instance-status --instance-ids i-0123456789abcdef0
aws ec2 create-tags --resources i-0123456789abcdef0 --tags Key=Name,Value=web-01

# 弹性 IP
aws ec2 allocate-address
aws ec2 associate-address --instance-id i-0123456789abcdef0 --allocation-id eipalloc-0123456789abcdef0
aws ec2 release-address --allocation-id eipalloc-0123456789abcdef0
```

## 计费方式

- **按需（On-Demand）**：按秒付费，最少 60 秒，无长期承诺。
- **Savings Plans / 预留实例**：承诺 1 或 3 年使用量换取更低价格。
- **竞价实例（Spot）**：使用闲置容量，价格显著更低，但可能被回收。
- **专用主机 / 按需容量预留**：满足软件许可和容量保障需求。
- 新账户有免费套餐额度。

## 安全与最佳实践

- 用安全组做虚拟防火墙，遵循最小权限（只开放必要的端口和来源网段）。
- 妥善保存私钥；AWS 只保存公钥。
- 给实例挂 IAM 角色，而不是分发长期访问密钥。
- 对关键实例开启终止保护。
- 定期做 EBS 快照、用 AMI 做恢复预案。
- 用 AWS Systems Manager 打补丁，用 CloudWatch 和实例状态检查做监控。

## 故障排查

| 症状 | 检查与处理 |
|------|-----------|
| 实例状态检查失败 | 先重启；仍失败则停止再启动。 |
| 无法 SSH/RDP 连接 | 检查安全组入站规则（22/3389 端口和来源网段）、路由表/NACL、系统服务、密钥对。 |
| 停止/启动后公有 IPv4 变化 | 未关联弹性 IP 时属预期行为；要固定地址就关联弹性 IP。 |
| 实例存储数据丢失 | 预期行为：停止/休眠/终止会清除实例存储数据；持久化数据用 EBS。 |
| 实例被误终止 | 无法恢复；依赖 AMI/快照/备份重建。 |
| t2/t3 突发 CPU 积分耗尽 | 切换到 unlimited 模式或更大实例类型。 |
| 实例状态检查通过但不可达 | 检查 CloudWatch 指标、系统内存/磁盘（CloudWatch agent）、EBS 状态。 |

## 配额

各区域按实例类型的配额不同且可调；新账户配额较低。以 Service Quotas 控制台为准，可在此申请提升。

## 官方参考

- [什么是 Amazon EC2？- Amazon EC2 用户指南](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/concepts.html)
- [Amazon EC2 实例状态变化](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ec2-instance-lifecycle.html)
- [Amazon EC2 定价](https://aws.amazon.com/ec2/pricing/)
- [AWS CLI：ec2 命令](https://docs.aws.amazon.com/cli/latest/reference/ec2/)
