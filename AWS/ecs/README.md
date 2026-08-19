# Amazon ECS - Runbook & Reference

> Facts verified against official AWS documentation: 2026-08-19

## Overview

Amazon Elastic Container Service (Amazon ECS) is a fully managed container orchestration service for deploying, managing, and scaling containerized applications. It runs workloads across AWS Regions and on-premises without the complexity of managing a control plane.

## Key concepts

- **Three layers**: capacity (where containers run), controller (deploy/manage applications), and provisioning (tools to interact with the scheduler).
- **Capacity options**: ECS Managed Instances (EC2 with AWS-managed infrastructure), EC2 instances (you manage), AWS Fargate (serverless, pay-as-you-go), and ECS Anywhere (on-premises servers/VMs).
- **Task definition**: the blueprint for an application (image, CPU, memory, networking, IAM role).
- **Cluster**: the infrastructure your tasks and services run on.
- **Task**: a short-lived workload such as a batch job.
- **Service**: a long-running application that ECS keeps running and scales.
- **Auto scaling**: service auto scaling adjusts desired task count; cluster auto scaling manages EC2 instances.

## Common operations (AWS CLI)

```bash
# Cluster
aws ecs create-cluster --cluster-name my-cluster
aws ecs list-clusters

# Task definition (JSON/YAML)
aws ecs register-task-definition --cli-input-json file://task-definition.json

# Run a one-off task
aws ecs run-task --cluster my-cluster --task-definition my-task --launch-type FARGATE

# Service (long-running)
aws ecs create-service --cluster my-cluster --service-name web \
  --task-definition my-task --desired-count 2 --launch-type FARGATE \
  --network-configuration "awsvpcConfiguration={subnets=[subnet-xxx],securityGroups=[sg-xxx]}"
aws ecs update-service --cluster my-cluster --service-name web --desired-count 5
aws ecs describe-services --cluster my-cluster --services web

# Exec into a running task
aws ecs execute-command --cluster my-cluster --task <task-id> --container app --command "/bin/sh" --interactive

# Delete
aws ecs delete-service --cluster my-cluster --service-name web --force
```

## Best practices

- Prefer **Fargate** for serverless operations or ECS Managed Instances when you need specialized EC2 capacity (GPU, architecture, networking).
- Give tasks a **least-privilege IAM role** (task role for application, execution role for pulling images/secrets).
- Store secrets in **AWS Secrets Manager / Parameter Store**; never in environment variables in plain text.
- Use **service auto scaling** with target tracking on CPU/memory or request counts.
- Route traffic through **Elastic Load Balancing** with container health checks.
- Send container logs to **CloudWatch Logs** and enable ECR image scanning.

## Troubleshooting

| Symptom | Checks and fixes |
|---------|------------------|
| Tasks stuck in `PENDING` | Check capacity (Fargate/EC2), subnet/ENI quotas, VPC endpoints, and the task IAM execution role. |
| Service cannot place tasks | Verify CPU/memory in the task definition vs. cluster capacity; check placement constraints. |
| Task starts then stops | Read the container logs; check task IAM role and image configuration. |
| ELB target unhealthy | Verify health check path/port, container port mapping, and security group rules. |
| Image pull failure | Confirm ECR repository permissions and task execution role (`ecr:GetAuthorizationToken`, `ecr:BatchGetImage`). |
| Out of memory | Increase task memory/CPU or fix the leak; check `memory` limits in the task definition. |

## Limits

Per-Region quotas apply to clusters, services, and tasks; Fargate task sizes range up to 16 vCPU / 120 GB memory. See the Service Quotas console for current values.

## Official references

- [What is Amazon ECS? - Amazon ECS Developer Guide](https://docs.aws.amazon.com/AmazonECS/latest/developerguide/Welcome.html)
- [AWS Fargate](https://docs.aws.amazon.com/AmazonECS/latest/developerguide/AWS_Fargate.html)
- [AWS CLI: ecs commands](https://docs.aws.amazon.com/cli/latest/reference/ecs/)
