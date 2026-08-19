# Amazon EKS - Runbook 与参考

> 事实核对时间（对照 AWS 官方文档）：2026-08-19

## 概述

Amazon Elastic Kubernetes Service（Amazon EKS）是全托管的 Kubernetes 服务。AWS 负责运行 Kubernetes 控制平面；还可以用 **EKS Auto Mode** 让 AWS 一并管理节点、扩缩容、打补丁和安全集成。

## 核心概念

- **EKS standard**：AWS 管理控制平面；节点（托管节点组、Fargate 或自管节点）和工作负载由你管理。
- **EKS Auto Mode**：AWS 同时管理数据平面（节点）、资源预置、成本优化和补丁。
- **EKS Capabilities**：托管集群扩展，如 Argo CD（GitOps）、AWS Controllers for Kubernetes（ACK）、kro。
- **访问控制**：AWS IAM 控制 Kubernetes API 访问；工作负载用 Service Account（IRSA）获得 AWS 临时权限。
- **计算**：支持全部 EC2 实例类型，包括 Nitro 和 Graviton。
- **存储**：EBS（CSI 驱动），以及 Amazon EFS、FSx、S3、S3 Files。
- **兼容性**：Kubernetes 一致性认证；提供 standard 与 extended support 版本生命周期。

## 常用操作

```bash
# 创建集群（IAM 角色需有 EKS 权限）
aws eks create-cluster --name my-cluster --role-arn arn:aws:iam::123456789012:role/eks-cluster \
  --resources-vpc-config subnetIds=subnet-xxx,subnet-yyy
aws eks list-clusters
aws eks describe-cluster --name my-cluster

# 让 kubectl 指向集群
aws eks update-kubeconfig --name my-cluster --region ap-southeast-1
kubectl get nodes
kubectl get pods -A

# 备选：eksctl
eksctl create cluster --name my-cluster --region ap-southeast-1 --nodegroup-type managed

# 删除
aws eks delete-cluster --name my-cluster
```

## 最佳实践

- 通过 **AWS IAM** 管理集群访问；不要共享长期 kubeconfig 凭证。
- 用 **IRSA** 或 EKS Pod Identity 给 Pod 最小权限的临时凭证。
- 用**托管节点组**或 EKS Auto Mode；保持节点 AMI 更新。
- 应用 Pod Security Standards 或策略引擎；扫描镜像。
- 用 CloudWatch Container Insights、Amazon Managed Prometheus 和 CloudTrail 监控。
- 备份集群与工作负载（例如 Velero），并按 Kubernetes 版本生命周期规划升级。

## 故障排查

| 症状 | 检查与处理 |
|------|-----------|
| 节点 `NotReady` | 检查节点实例健康、kubelet 日志、AMI、安全组/网络。 |
| Pod `Pending` | 检查资源请求、节点容量、污点/容忍、存储类。 |
| API server 不可达 | 核对 VPC 网络、安全组、`update-kubeconfig` 上下文。 |
| IRSA `AccessDenied` | 检查 Pod Service Account 注解和角色信任策略（`oidc.eks.<region>.amazonaws.com/id/<cluster>`）。 |
| EBS 卷问题 | 确认已安装 EBS CSI 驱动且节点角色有权限。 |
| 升级失败 | 遵循受支持版本生命周期；先在测试集群验证。 |

## 配额

集群、节点、Fargate Profile 都有每区域配额。以 Service Quotas 控制台为准。

## 官方参考

- [什么是 Amazon EKS？- Amazon EKS 用户指南](https://docs.aws.amazon.com/eks/latest/userguide/what-is-eks.html)
- [eksctl](https://eksctl.io/)
- [AWS CLI：eks 命令](https://docs.aws.amazon.com/cli/latest/reference/eks/)
