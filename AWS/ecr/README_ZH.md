# Amazon Elastic Container Registry (ECR) - Runbook 与参考

> 事实核对时间（对照 AWS 官方文档）：2026-08-19

## 概述

Amazon Elastic Container Registry（Amazon ECR）是托管的容器镜像仓库。它支持基于 IAM 访问的私有仓库和公有仓库，可存储 Docker、Open Container Initiative（OCI）镜像以及 OCI 兼容制品。

## 核心概念

- **Registry 与 Repository**：registry 按账户、按区域划分；repository 存放镜像版本。
- **镜像扫描**：识别软件漏洞；可启用推送时扫描（基础）或使用 Amazon Inspector 的增强扫描。
- **生命周期策略**：按年龄或数量自动清理未使用的镜像；应用前先测试规则。
- **复制**：跨区域和跨账户的 registry 复制。
- **Pull-through cache**：将上游 registry 的镜像缓存到你的私有 ECR。
- **托管签名**：推送时自动为镜像添加加密签名。
- **仓库策略**：基于资源的 IAM 策略，控制谁能拉取/推送。

## 常用操作（AWS CLI）

```bash
# 创建启用推送时扫描的仓库
aws ecr create-repository --repository-name app \
  --image-scanning-configuration scanOnPush=true \
  --encryption-configuration encryptionType=AES256

# 认证 Docker 到 registry
aws ecr get-login-password --region us-east-1 | \
  docker login --username AWS --password-stdin 123456789012.dkr.ecr.us-east-1.amazonaws.com

# 打标签、推送和查看
docker tag app:latest 123456789012.dkr.ecr.us-east-1.amazonaws.com/app:latest
docker push 123456789012.dkr.ecr.us-east-1.amazonaws.com/app:latest
aws ecr describe-images --repository-name app

# 生命周期策略
aws ecr put-lifecycle-policy --repository-name app \
  --lifecycle-policy-text file://lifecycle.json

# 扫描并获取结果
aws ecr start-image-scan --repository-name app --image-id imageTag=latest
aws ecr describe-image-scan-findings --repository-name app --image-id imageTag=latest

# 复制（registry 设置）
aws ecr put-replication-configuration --replication-configuration file://replication.json
```

## 最佳实践

- 使用私有仓库和 IAM/仓库策略；绝不让生产镜像公开。
- 启用推送时扫描（需要深度覆盖时用 Inspector 增强扫描），部署前修复关键/高危漏洞。
- 使用生命周期策略清理无标签和旧镜像；先测试规则。
- 使用不可变标签，防止已部署镜像被覆盖。
- 跨区域复制镜像用于容灾，并避免跨区域拉取延迟。
- 合规要求时对镜像签名，保障供应链完整性。
- 为依赖的上游 registry 配置 pull-through cache 规则。

## 故障排查

| 症状 | 检查与处理 |
|---|---|
| `denied: Your Authorization Token has expired` | 重新执行 `aws ecr get-login-password` 和 `docker login`。 |
| 推送/拉取被拒绝 | 检查仓库策略和 IAM 权限（`ecr:BatchGetImage`、`ecr:PutImage`）。 |
| 扫描无结果 | 核对扫描配置、镜像是否在启用后推送以及区域。 |
| 镜像未清理 | 检查生命周期策略规则，先用预览方式测试。 |
| 复制不工作 | 核对 registry 设置、目标账户/区域和 IAM。 |

## 配额

每 registry 的仓库数、镜像大小和 API 速率都有配额。以 Service Quotas 控制台为准。

## 官方参考

- [什么是 Amazon Elastic Container Registry？- ECR 用户指南](https://docs.aws.amazon.com/AmazonECR/latest/userguide/what-is-ecr.html)
- [Amazon ECR 服务配额](https://docs.aws.amazon.com/AmazonECR/latest/userguide/service-quotas.html)
- [Amazon ECR 定价](https://aws.amazon.com/ecr/pricing/)
- [AWS CLI：ecr 命令](https://docs.aws.amazon.com/cli/latest/reference/ecr/)
