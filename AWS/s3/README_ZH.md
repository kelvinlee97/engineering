# Amazon S3 - Runbook 与参考

> 事实核对时间（对照 AWS 官方文档）：2026-08-18

## 概述

Amazon S3 是对象存储服务，用于存储和保护任意规模的数据：数据湖、网站、移动应用、备份与恢复、归档、企业应用和分析。S3 在所有区域对 PUT 和 DELETE 请求提供强一致（read-after-write）。

## 存储桶与对象

- **存储桶**是对象的容器；**对象**是文件加元数据，在桶内以唯一的 key 标识。
- **通用桶**（默认推荐）：默认在全局命名空间（名称在所有 AWS 账户间唯一），默认私有。
- **目录桶**：层级结构，面向低延迟和数据驻留场景；所有公网访问都被禁用且无法开启。
- **表桶**：以 Apache Iceberg 格式存储表格数据，用于分析和机器学习。
- **向量桶**：专为向量数据设计。

## 存储类

- **频繁访问**：S3 Standard、S3 Express One Zone（毫秒级延迟）。
- **低频访问**：S3 Standard-IA、S3 One Zone-IA。
- **归档**：S3 Glacier Instant Retrieval、Glacier Flexible Retrieval、Glacier Deep Archive。
- **自动分层**：S3 Intelligent-Tiering 根据访问模式在四层之间自动移动数据。
- 用**生命周期规则**在不同存储类间转换对象或到期删除。

## 常用操作（AWS CLI）

```bash
# 创建桶、列出对象
aws s3 mb s3://my-bucket --region ap-southeast-1
aws s3 ls s3://my-bucket/

# 复制 / 同步 / 移动 / 删除
aws s3 cp ./file.txt s3://my-bucket/path/
aws s3 cp s3://my-bucket/path/file.txt ./
aws s3 sync ./logs/ s3://my-bucket/logs/ --exclude "*.tmp"
aws s3 mv s3://my-bucket/old.txt s3://my-bucket/new.txt
aws s3 rm s3://my-bucket/path/ --recursive
aws s3 rb s3://my-bucket --force

# 过滤语义：顺序重要；先排除全部，再重新包含
aws s3 cp ./src/ s3://my-bucket/src/ --recursive --exclude "*" --include "*.jpg"

# 生成预签名 URL
aws s3 presign s3://my-bucket/path/file.txt --expires-in 3600
```

底层 `aws s3api` 命令覆盖版本控制、生命周期、加密和桶策略。大文件上传会自动使用分片上传（multipart）。

## 访问控制

- 桶和对象**默认私有**；桶级 Block Public Access 默认开启。
- 使用 **IAM 策略**、**桶策略**和**接入点（access points）**；AWS 建议用策略而非 ACL（ACL 通过 S3 Object Ownership 默认关闭）。
- 用 **IAM Access Analyzer for S3**、CloudTrail 和服务器访问日志审计访问。

## 数据保护

- **版本控制**：保留对象的多个版本，可恢复误覆盖/误删除。
- **S3 Object Lock**：WORM 写入一次多次读取，满足合规要求。
- **复制（Replication）**：在相同或跨区域桶间复制对象。
- **服务端加密**：SSE-S3 或 SSE-KMS。

## 监控

- CloudWatch 指标（含账单告警）、CloudTrail API 日志、服务器访问日志、S3 Storage Lens（60+ 使用与活动指标）、S3 Inventory。

## 故障排查

| 症状 | 检查与处理 |
|------|-----------|
| `AccessDenied` | 检查 IAM 身份策略、桶策略、接入点策略、Block Public Access、组织的 SCP/RCP。 |
| `404 NoSuchKey` | 确认 key/前缀路径、桶所在区域；开启版本控制后可能需要指定 version ID。 |
| 上传/下载慢 | 使用分片上传、Transfer Acceleration 或 CloudFront，并检查网络路径。 |
| 成本异常增长 | 用 Storage Lens 定位；添加生命周期规则；清理未完成的分片上传。 |
| 桶名被占用 | 通用桶名全局唯一；加唯一后缀或使用账户区域命名空间。 |

## 配额

- 通用桶：每账户默认 100 个（可调）。
- 目录桶：每账户默认 100 个。
- 表桶：每区域每账户 10 个；每个表桶最多 10,000 张表。
- 单次 PUT 对象最大 5 TB。
- 以 Service Quotas 控制台为准。

## 官方参考

- [什么是 Amazon S3？- Amazon S3 用户指南](https://docs.aws.amazon.com/AmazonS3/latest/userguide/Welcome.html)
- [AWS CLI：s3 命令](https://docs.aws.amazon.com/cli/latest/reference/s3/)
- [Amazon S3 端点和配额](https://docs.aws.amazon.com/general/latest/gr/s3.html)
