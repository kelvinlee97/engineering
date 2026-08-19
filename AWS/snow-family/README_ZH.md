# AWS Snow Family - Runbook 与参考

> 事实核对时间（对照 AWS 官方文档）：2026-08-19

## 概述

AWS Snow Family 提供物理设备，用于缺乏可靠网络环境下的离线数据传输和边缘计算。**请注意当前生命周期：** Snowcone（HDD/SSD）已于 2024 年 11 月 12 日停售，AWS Snowball Edge 已不再对新客户开放。新的在线数据传输请使用 AWS DataSync；离线传输选项请参考最新的 Snowball Edge 文档。

## 设备与当前状态

| 设备 | 用途 | 状态 |
|---|---|---|
| Snowball Edge Storage Optimized（210 TB） | 大规模离线数据迁移，S3/EC2 兼容端点 | 不再对新客户开放 |
| Snowball Edge Compute Optimized | 带本地处理的边缘计算 | 不再对新客户开放 |
| Snowcone（HDD/SSD） | 小型边缘计算与数据传输 | 2024 年 11 月 12 日停售 |
| Snowmobile | EB 级数据中心传输 | 2024 年 3 月退役 |

## 核心概念

- **任务（Job）**：在站点与 S3 之间移动数据的导入/导出任务；通过控制台或 Snowball API 创建管理。
- **设备配置**：Storage Optimized（210 TB，最多 40 vCPU）vs Compute Optimized（最多 104 vCPU，可选 GPU）。
- **端点**：Snowball Edge 提供 S3 和 EC2 兼容端点及 NFS，供本地工作负载使用。
- **集群**：3-16 台设备组成集群，提供更高持久性的本地存储和计算。
- **OpsHub / Snowball Edge 客户端**：解锁设备、配置网络和传输数据的工具。

## 常用操作（AWS CLI）

```bash
# 创建导入任务（目标 S3 桶）
aws snowball create-job --job-type IMPORT --resources '{"S3":{"S3ResourceArns":["arn:aws:s3:::bucket-name"]}}' \
  --address-id <address-id> --role-arn arn:aws:iam::123456789012:role/snowball-role \
  --snowball-capacity-preference T210 --shipping-option SECOND_DAY

# 列出和查看任务
aws snowball list-jobs
aws snowball describe-job --job-id <job-id>

# 更新寄送地址
aws snowball update-job --job-id <job-id> --address-id <new-address-id>

# 设备寄出前取消任务
aws snowball cancel-job --job-id <job-id>
```

## 最佳实践

- 能在线迁移就优先用 AWS DataSync，减少物理设备的周转。
- 下单前估算数据量和传输时间，选择合适设备减少寄送趟数。
- 先准备好 S3 桶、IAM 角色和寄送地址，再创建任务。
- 用 AWS OpsHub 解锁和监控设备；妥善保管解锁码和清单。
- 启用加密：Snow 设备数据默认在静态和传输中加密。
- 用 E Ink 标签跟踪设备，按导入/导出流程归还。
- 边缘计算场景：为 AMI 做快照并规划设备更换；AWS 会监控已连接设备并寄送替换设备。

## 故障排查

| 症状 | 检查与处理 |
|---|---|
| 设备无法解锁 | 核对任务状态，使用控制台提供的正确清单/解锁码。 |
| 本地传输慢 | 检查客户端与设备之间的网络（10/25/40/100 GbE），按场景用 S3 适配器或 NFS。 |
| S3 中没有数据 | 确认任务已完成且设备归还后 AWS 已处理。 |
| 寄出后任务被取消 | 联系 AWS Support；已寄出的任务一般无法取消。 |
| 边缘计算实例失败 | 确认 AMI 与 Snowball Edge 兼容（sbe1/sbe-c/sbe-g 实例类型）。 |

## 配额

每账号任务数、同时在途设备数和集群大小（3-16 台）受 AWS 配额和区域可用性限制。以 Service Quotas 控制台和最新 Snowball Edge 文档为准。

## 官方参考

- [什么是 Snowball Edge？](https://docs.aws.amazon.com/snowball/latest/developer-guide/whatisedge.html)
- [AWS DataSync（推荐用于新的在线传输）](https://docs.aws.amazon.com/datasync/latest/userguide/what-is-datasync.html)
- [AWS Snowball Edge 定价](https://aws.amazon.com/snowball/pricing/)
- [AWS CLI：snowball 命令](https://docs.aws.amazon.com/cli/latest/reference/snowball/)
