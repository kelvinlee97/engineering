# Amazon FSx - Runbook 与参考

> 事实核对时间（对照 AWS 官方文档）：2026-08-19

## 概述

Amazon FSx 是一组完全托管的文件存储服务，用于需要共享文件系统的工作负载。它提供原生 Windows 文件服务器、高性能并行文件系统，以及兼容 NetApp 和 OpenZFS 的 POSIX 文件系统。

## 文件系统类型

| 类型 | 协议 | 适用场景 |
|---|---|---|
| FSx for Windows File Server | SMB 2.0-3.1.1 | Windows 应用上云、主目录、业务应用 |
| FSx for Lustre | POSIX（Lustre） | 高性能计算、机器学习训练、媒体处理 |
| FSx for NetApp ONTAP | NFS、SMB、iSCSI | 企业 NAS 功能：快照、克隆、数据分层 |
| FSx for OpenZFS | NFS（POSIX） | 需要 ZFS 快照、克隆、压缩的 Linux 工作负载 |

## 核心概念

- **文件系统**：主要资源；可独立配置存储容量、吞吐量（Windows 还有 SSD IOPS）。
- **文件共享**：Windows 的 SMB 共享或 Lustre/ONTAP/OpenZFS 的 NFS 导出，供计算客户端访问。
- **单 AZ / 多 AZ**：Windows 文件系统支持单可用区高可用，或跨两个可用区自动故障转移。
- **Active Directory 集成**：Windows 文件系统加入 Microsoft AD，用 ACL 做文件级权限控制。
- **备份**：文件系统一致的增量备份；默认每日自动备份，也可随时手动备份。
- **数据分层**：ONTAP 可把冷数据分层到 Amazon S3 控制成本。

## 常用操作（AWS CLI）

```bash
# 创建文件系统（Windows 示例）
aws fsx create-file-system --file-system-type WINDOWS \
  --storage-capacity 300 --storage-type SSD \
  --subnet-ids subnet-0123456789abcdef0 \
  --windows-configuration ThroughputCapacity=32,DeploymentType=MULTI_AZ_1,PreferredSubnetId=subnet-0123456789abcdef0

# 列出和查看文件系统
aws fsx describe-file-systems
aws fsx describe-file-systems --file-system-ids fs-0123456789abcdef0

# 创建备份
aws fsx create-backup --file-system-id fs-0123456789abcdef0

# 调整容量
aws fsx update-file-system --file-system-id fs-0123456789abcdef0 \
  --storage-capacity 600

# 删除（先做最终备份）
aws fsx delete-file-system --file-system-id fs-0123456789abcdef0
```

## 最佳实践

- 按协议和工作负载选择 FSx 类型：Windows/SMB、Lustre/HPC、ONTAP/OpenZFS（NAS 功能）。
- 生产环境用多 AZ Windows 文件系统；对成本敏感、可接受中断的场景用单 AZ。
- 开启每日自动备份，破坏性变更前保留手动备份。
- 文件系统放在私有子网，用 VPC 安全组控制访问。
- Windows 文件系统加入 Managed Microsoft AD，并用 Windows ACL 做文件级权限。
- 用 CloudWatch 监控，开启 CloudTrail 审计 API 调用。

## 故障排查

| 症状 | 检查与处理 |
|---|---|
| 客户端无法挂载 | 检查安全组规则（SMB 445、NFS 2049）以及 VPC 对等/Transit Gateway 连通性。 |
| Windows 认证失败 | 确认文件系统已加入 AD、DNS 能解析文件系统名、用户有 AD 账号。 |
| 性能差 | 检查吞吐量/存储/IOPS 配置是否匹配工作负载，必要时扩容。 |
| 备份失败 | 检查剩余容量和文件系统状态，重试手动备份。 |
| 多 AZ 故障转移异常 | 确认首选和备用子网位于不同可用区且路由正确。 |

## 配额

文件系统数量、总存储和吞吐量按类型和区域有每账号配额。以 Service Quotas 控制台当前值为准。

## 官方参考

- [什么是 FSx for Windows File Server？](https://docs.aws.amazon.com/fsx/latest/WindowsGuide/what-is.html)
- [Amazon FSx for Lustre](https://docs.aws.amazon.com/fsx/latest/LustreGuide/what-is.html)
- [Amazon FSx for NetApp ONTAP](https://docs.aws.amazon.com/fsx/latest/ONTAPGuide/what-is.html)
- [Amazon FSx for OpenZFS](https://docs.aws.amazon.com/fsx/latest/OpenZFSGuide/what-is.html)
- [AWS CLI：fsx 命令](https://docs.aws.amazon.com/cli/latest/reference/fsx/)
