# AWS DataSync - Runbook 与参考

> 事实核对时间（对照 AWS 官方文档）：2026-08-19

## 概述

AWS DataSync 是安全、可靠、高速的数据传输服务，用于在 AWS 存储服务之间以及与其他位置移动文件/对象数据。它支持本地存储（通过代理）、AWS 存储（S3、EFS、FSx）和其他云存储，内置加密和数据完整性校验。

## 核心概念

- **任务（Task）**：在源位置和目标位置之间传输数据的作业，带可定义选项（覆盖、保留元数据、计划）。
- **位置（Location）**：源或目标端点（NFS、SMB、S3、EFS、FSx）。
- **代理（Agent）**：连接 DataSync 与本地存储的软件设备（Amazon EC2 或本地 VM）。
- **调度与监控**：任务按需或按计划运行；用 CloudWatch 指标、事件和控制台监控。
- **加速**：专用网络协议配合并行多线程架构实现快速传输。
- **安全**：端到端加密；DataSync 使用 IAM 角色并支持 VPC 端点（私有传输，不经过公共互联网）。
- **用途**：迁移活跃数据集、归档冷数据到 Glacier、复制到 S3/EFS/FSx，以及将数据移入 AWS 处理。

## 常用操作（AWS CLI）

```bash
# 创建位置和任务
aws datasync create-location-s3 --s3-bucket-arn arn:aws:s3:::my-bucket \
  --s3-config '{"BucketAccessRoleArn":"arn:aws:iam::123456789012:role/datasync-role"}' \
  --region us-east-1
aws datasync create-location-nfs --server-hostname 10.0.0.10 \
  --on-prem-config '{"AgentArns":["arn:aws:datasync:us-east-1:123456789012:agent/agent-0123456789abcdef0"]}' \
  --subdirectory /data
aws datasync create-task --source-location-arn <source-arn> \
  --destination-location-arn <dest-arn> --name migrate-data

# 启动和监控
aws datasync start-task-execution --task-arn <task-arn>
aws datasync describe-task-execution --task-execution-arn <exec-arn>
aws datasync list-tasks
aws datasync delete-task --task-arn <task-arn>
```

## 最佳实践

- 完整迁移前先对子集做发现/验证传输；可用处使用 dry-run 选项。
- 复制场景用定时任务，并对传输错误/失败设置 CloudWatch 告警。
- 代理靠近数据源部署并适当配置；超大数据集使用多任务/多代理。
- AWS 之间或混合传输不应走公共互联网时使用 VPC 端点。
- 按需保留元数据和权限；选择正确的 S3 存储类（冷归档用 Glacier）。
- 监控任务执行指标，传输后验证完整性。

## 故障排查

| 症状 | 检查与处理 |
|---|---|
| 代理离线 | 核对代理 VM 运行、网络访问，以及在正确区域完成激活。 |
| 任务失败 | 检查源/目标连通性、IAM 角色，以及任务的 CloudWatch 日志/错误信息。 |
| 传输慢 | 审查代理配置、网络带宽、小文件开销和任务调度冲突。 |
| 权限保留不正确 | 调整任务的 POSIX/SMB 元数据选项。 |
| 文件缺失 | 确认任务过滤器、验证模式和运行期间源可访问。 |

## 配额

每账户代理、位置、任务和并发任务执行数有限制。以 AWS DataSync 端点和配额页面及 Service Quotas 控制台为准。

## 官方参考

- [什么是 AWS DataSync？- 用户指南](https://docs.aws.amazon.com/datasync/latest/userguide/what-is-datasync.html)
- [AWS DataSync 端点和配额](https://docs.aws.amazon.com/general/latest/gr/datasync.html)
- [AWS DataSync 定价](https://aws.amazon.com/datasync/pricing/)
- [AWS CLI：datasync 命令](https://docs.aws.amazon.com/cli/latest/reference/datasync/)
