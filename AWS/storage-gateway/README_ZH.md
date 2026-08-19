# AWS Storage Gateway - Runbook 与参考

> 事实核对时间（对照 AWS 官方文档）：2026-08-19

## 概述

AWS Storage Gateway 把本地软件设备（或 Storage Gateway 硬件设备）与云存储连接起来，让本地环境可以使用 AWS 托管的文件、卷和磁带存储，是混合存储架构的桥梁。

## 网关类型

| 网关 | 接口 | 提供的内容 |
|---|---|---|
| S3 File Gateway | SMB / NFS | 把 S3 对象暴露为文件共享，带本地缓存 |
| FSx File Gateway | SMB | 带本地缓存的 FSx for Windows File Server 共享 |
| Volume Gateway | iSCSI | 由 EBS 快照支撑的块存储卷（缓存型或存储型） |
| Tape Gateway | iSCSI VTL | 存储在 S3 并可归档到 S3 Glacier 的虚拟磁带 |

## 核心概念

- **网关**：部署在数据中心的虚拟机或硬件设备，激活后关联到你的 AWS 账号。
- **文件共享**：由 S3 桶或 FSx 文件系统支撑的 SMB/NFS 导出，带本地热数据缓存。
- **缓存型 vs 存储型卷**：缓存型主数据在 S3、本地保留热数据；存储型主数据在本地、用 EBS 快照备份。
- **虚拟磁带库（VTL）**：通过 iSCSI 呈现的磁带机和磁带库；磁带存 S3，可归档到 Glacier。
- **AWS OpsHub**：用于部署、激活和监控网关的桌面应用。

## 常用操作（AWS CLI）

```bash
# 创建并激活网关（返回 GatewayARN）
aws storagegateway create-gateway --gateway-name site-a-file --gateway-timezone GMT \
  --gateway-type FILE_FSX_SMB --gateway-platform "VMWARE" \
  --gateway-capacity Medium

# 列出网关
aws storagegateway list-gateways

# 创建 SMB 文件共享
aws storagegateway create-smb-file-share --gateway-arn <gateway-arn> \
  --role arn:aws:iam::123456789012:role/StorageGatewayRole \
  --location-arn arn:aws:s3:::bucket-name

# 创建磁带（1 TiB）
aws storagegateway create-tapes --gateway-arn <gateway-arn> \
  --tape-size-in-bytes 1099511627776 --num-tapes-to-create 1 \
  --client-token tape-001

# 查看资源
aws storagegateway list-file-shares
aws storagegateway list-volumes
aws storagegateway list-tapes
```

## 最佳实践

- 网关部署在离工作负载近的位置，并按工作集大小规划本地缓存/磁盘。
- 本地文件访问 S3 用 S3 File Gateway；需要 iSCSI 的块工作负载用 Volume Gateway。
- 开启网关带宽限速，保护广域网链路。
- 备份网关虚拟机；不适合自建虚拟机时用硬件设备。
- 用 CloudWatch 监控缓存命中率、上传吞吐量等指标并设置告警。
- IAM 最小权限：文件共享只需要用到的 S3/FSx 权限。
- 用 AWS Backup 集中管理快照和磁带生命周期。

## 故障排查

| 症状 | 检查与处理 |
|---|---|
| 文件共享挂载失败 | 确认共享可用、DNS/SMB 设置正确、客户端路径正确。 |
| 上传慢 | 检查带宽限速、本地缓存大小和网络连通性。 |
| 缓存打满 | 增大缓存盘或缩小共享的工作集。 |
| VTL 中看不到磁带 | 检查 iSCSI 发起端配置，确认磁带库/驱动器已配置。 |
| 网关离线 | 在 OpsHub 检查网关健康、虚拟机资源和到 AWS 端点的网络。 |

## 配额

网关数量、缓存大小、文件共享数量和磁带数量有每账号配额。以 Service Quotas 控制台当前值为准。

## 官方参考

- [什么是 AWS Storage Gateway？](https://docs.aws.amazon.com/storagegateway/latest/userguide/WhatIsStorageGateway.html)
- [Amazon S3 File Gateway 用户指南](https://docs.aws.amazon.com/storagegateway/latest/s3fgw/WhatIsS3FileGateway.html)
- [AWS Storage Gateway 定价](https://aws.amazon.com/storagegateway/pricing/)
- [AWS CLI：storagegateway 命令](https://docs.aws.amazon.com/cli/latest/reference/storagegateway/)
