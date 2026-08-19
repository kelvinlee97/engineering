# Amazon EC2 Auto Scaling（Auto Scaling Group）- Runbook 与参考

> 事实核对时间（对照 AWS 官方文档）：2026-08-19

## 概述

Amazon EC2 Auto Scaling 帮助你的应用程序保持正确数量的 EC2 实例以应对负载。实例组织为 Auto Scaling Group（自动扩缩组），你设置最小、期望和最大容量；当需求变化时，扩缩策略在这些边界内启动或终止实例，服务也会自动替换不健康的实例。

## 核心概念

- **Auto Scaling Group（ASG）**：作为单一单元管理的一组 EC2 实例；实例数不会低于最小值，也不会超过最大值。
- **启动模板（Launch template）**：实例的配置模板（AMI、实例类型、密钥对、安全组、用户数据）；启动配置是旧版替代方案。
- **健康检查**：EC2 状态检查以及可选的自定义健康检查（例如应用级检查）；不健康的实例会被终止并替换以维持期望容量。
- **AZ 均衡**：实例均匀分布在你指定的可用区中，实现高可用。
- **多种实例类型与购买选项**：可在同一组内使用多种实例类型并混合按需与 Spot；Capacity Rebalancing 会在 Spot 实例中断风险升高时主动替换。
- **负载均衡集成**：组扩缩时，Elastic Load Balancing 自动注册/注销实例。
- **实例刷新（Instance refresh）**：更新 AMI 或启动模板时执行滚动或 canary（分阶段）部署。
- **生命周期钩子（Lifecycle hooks）**：实例启动或终止前运行自定义操作；可与 scale-in 保护配合支持有状态工作负载。

## 常用操作（AWS CLI）

```bash
# 创建 Auto Scaling Group
aws autoscaling create-auto-scaling-group \
  --auto-scaling-group-name web-asg \
  --launch-template LaunchTemplateName=web-lt,Version=1 \
  --min-size 2 --max-size 10 --desired-capacity 4 \
  --vpc-zone-identifier subnet-0123456789abcdef0,subnet-1234567890abcdef0

# 更新容量或配置
aws autoscaling update-auto-scaling-group --auto-scaling-group-name web-asg \
  --min-size 3 --max-size 12 --desired-capacity 6
aws autoscaling set-desired-capacity --auto-scaling-group-name web-asg \
  --desired-capacity 8

# 查看与终止实例
aws autoscaling describe-auto-scaling-groups --auto-scaling-group-names web-asg
aws autoscaling describe-scaling-activities --auto-scaling-group-name web-asg
aws autoscaling terminate-instance-in-auto-scaling-group \
  --instance-id i-0123456789abcdef0 --should-decrement-desired-capacity

# 实例刷新（滚动更新）
aws autoscaling start-instance-refresh --auto-scaling-group-name web-asg \
  --preferences '{"MinHealthyPercentage": 90}'
```

## 最佳实践

- 使用启动模板（而不是启动配置）并做版本管理，便于受控变更。
- 根据实测容量设置 min/max/desired；对合适的指标（CPU、每目标请求数、队列深度）使用目标跟踪策略。
- 跨多个可用区分布实例，并启用 ELB 健康检查实现应用级替换。
- 容错工作负载混合按需与 Spot 并启用 Capacity Rebalancing 降低成本。
- 使用生命周期钩子做排空/注册，对有状态实例启用 scale-in 保护。
- 预热 AMI，并用实例刷新安全地做滚动/canary 部署。
- 监控扩缩活动，对 MinSize/MaxSize/InService 数量设置告警。

## 故障排查

| 症状 | 检查与处理 |
|---|---|
| 实例不启动 | 检查启动模板有效性、子网/可用区容量、实例类型可用性以及 IAM 权限。 |
| 期望容量未维持 | 查看扩缩活动、健康检查状态，以及实例是否被意外保护不缩容。 |
| 各 AZ 不均衡 | 确认组覆盖了你预期的可用区，且每个可用区都有容量。 |
| 扩缩策略从不触发 | 核对 CloudWatch 指标名称/命名空间及策略对应的告警阈值。 |
| 实例刷新失败 | 检查 MinHealthyPercentage 和实例就绪情况，调整参数后重试。 |

## 配额

每账户 Auto Scaling Group、启动模板和扩缩策略有配额；组大小受 EC2 实例配额约束。以 Service Quotas 控制台为准。EC2 Auto Scaling 本身无额外费用，你只为底层资源付费。

## 官方参考

- [什么是 Amazon EC2 Auto Scaling？- 用户指南](https://docs.aws.amazon.com/autoscaling/ec2/userguide/what-is-amazon-ec2-auto-scaling.html)
- [Amazon EC2 Auto Scaling 配额](https://docs.aws.amazon.com/autoscaling/ec2/userguide/ec2-auto-scaling-quotas.html)
- [Amazon EC2 Auto Scaling 定价](https://aws.amazon.com/ec2/autoscaling/pricing/)
- [AWS CLI：autoscaling 命令](https://docs.aws.amazon.com/cli/latest/reference/autoscaling/)
