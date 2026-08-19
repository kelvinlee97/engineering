# Amazon ECS - Runbook 与参考

> 事实核对时间（对照 AWS 官方文档）：2026-08-19

## 概述

Amazon Elastic Container Service（Amazon ECS）是托管容器编排服务，用于部署、管理和扩展容器化应用。它可以在多个 AWS 区域和本地环境运行工作负载，无需管理控制平面。

## 核心概念

- **三层结构**：容量（容器运行的基础设施）、控制器（部署/管理应用）、预置（与调度器交互的工具）。
- **容量选项**：ECS Managed Instances（EC2 但基础设施由 AWS 管理）、EC2 实例（自行管理）、AWS Fargate（无服务器、按量付费）、ECS Anywhere（本地服务器/虚拟机）。
- **任务定义（Task definition）**：应用的蓝图（镜像、CPU、内存、网络、IAM 角色）。
- **集群（Cluster）**：任务和服务运行的基础设施。
- **任务（Task）**：一次性工作负载，例如批处理任务。
- **服务（Service）**：长期运行的应用，由 ECS 维持期望数量并扩缩容。
- **自动扩缩**：服务自动扩缩调整任务数；集群自动扩缩管理 EC2 实例。

## 常用操作（AWS CLI）

```bash
# 集群
aws ecs create-cluster --cluster-name my-cluster
aws ecs list-clusters

# 任务定义（JSON/YAML）
aws ecs register-task-definition --cli-input-json file://task-definition.json

# 运行一次性任务
aws ecs run-task --cluster my-cluster --task-definition my-task --launch-type FARGATE

# 服务（长期运行）
aws ecs create-service --cluster my-cluster --service-name web \
  --task-definition my-task --desired-count 2 --launch-type FARGATE \
  --network-configuration "awsvpcConfiguration={subnets=[subnet-xxx],securityGroups=[sg-xxx]}"
aws ecs update-service --cluster my-cluster --service-name web --desired-count 5
aws ecs describe-services --cluster my-cluster --services web

# 进入运行中的任务
aws ecs execute-command --cluster my-cluster --task <task-id> --container app --command "/bin/sh" --interactive

# 删除
aws ecs delete-service --cluster my-cluster --service-name web --force
```

## 最佳实践

- 无服务器场景优先用 **Fargate**；需要专用 EC2 能力（GPU、架构、网络）时用 ECS Managed Instances。
- 给任务**最小权限 IAM 角色**（task role 给应用、execution role 用于拉镜像/取密钥）。
- 密钥放 **AWS Secrets Manager / Parameter Store**，不要明文写进环境变量。
- 用**服务自动扩缩**（target tracking：CPU/内存/请求数）。
- 用 **Elastic Load Balancing** 做流量分发并配置容器健康检查。
- 容器日志发到 **CloudWatch Logs**，开启 ECR 镜像扫描。

## 故障排查

| 症状 | 检查与处理 |
|------|-----------|
| 任务卡在 `PENDING` | 检查容量（Fargate/EC2）、子网/ENI 配额、VPC 端点、任务 execution role。 |
| 服务无法放置任务 | 核对任务定义 CPU/内存与集群容量；检查放置约束。 |
| 任务启动后立刻停止 | 看容器日志；检查任务 IAM 角色和镜像配置。 |
| ELB 目标不健康 | 核对健康检查路径/端口、容器端口映射、安全组规则。 |
| 拉取镜像失败 | 确认 ECR 仓库权限和 execution role（`ecr:GetAuthorizationToken`、`ecr:BatchGetImage`）。 |
| 内存不足 | 调大任务内存/CPU 或修复泄漏；检查任务定义的 memory 限制。 |

## 配额

集群、服务、任务都有每区域配额；Fargate 任务规格最大 16 vCPU / 120 GB 内存。以 Service Quotas 控制台为准。

## 官方参考

- [什么是 Amazon ECS？- Amazon ECS 开发者指南](https://docs.aws.amazon.com/AmazonECS/latest/developerguide/Welcome.html)
- [AWS Fargate](https://docs.aws.amazon.com/AmazonECS/latest/developerguide/AWS_Fargate.html)
- [AWS CLI：ecs 命令](https://docs.aws.amazon.com/cli/latest/reference/ecs/)
