---
type: Service
title: Amazon ECS
description: "AWS's own container orchestrator: task definitions run as tasks or long-running services on Fargate, EC2, or on-premises capacity."
tags: [aws, compute, containers]
sources:
  - id: aws-ecs
    resource: https://github.com/kelvinlee97/engineering/blob/main/AWS/ecs/README.md
    title: "Amazon ECS - Runbook & Reference"
    author: human:kelvinlee97
    last_modified: 2026-09-24T14:48:10Z
generated: { by: claude-code/wiki-v1, at: 2026-09-25T07:00:00Z }
status: draft
---

Amazon Elastic Container Service (ECS) is a fully managed container orchestrator with no control plane to operate.[^aws-ecs]

## Concepts

- Three layers: capacity, controller, and provisioning tools.[^aws-ecs]
- Capacity: ECS Managed Instances, self-managed EC2, AWS Fargate (serverless), and ECS Anywhere (on-premises).[^aws-ecs]
- A task definition is the blueprint (image, CPU, memory, networking, IAM role); a task is a short-lived run; a service keeps tasks running and scales them.[^aws-ecs]
- Service auto scaling sets desired task count; cluster auto scaling manages EC2 capacity.[^aws-ecs]
- Fargate tasks go up to 16 vCPU and 120 GB memory.[^aws-ecs]

## Practices

- Separate a task role (the app's permissions) from an execution role (pulling images and secrets).[^aws-ecs]
- Secrets from Secrets Manager or Parameter Store; target tracking scaling; ELB health checks; CloudWatch Logs; ECR scanning.[^aws-ecs]

## Troubleshooting

| Symptom | Check |
| --- | --- |
| Tasks stuck `PENDING` | Capacity, subnet and ENI quotas, VPC endpoints, execution role |
| Cannot place tasks | Task CPU/memory versus cluster capacity, placement constraints |
| Image pull failure | ECR permissions and `ecr:GetAuthorizationToken`, `ecr:BatchGetImage` on the execution role |
| ELB target unhealthy | Health check path, port mapping, SGs |

As tabled in the note.[^aws-ecs] See [AWS compute options](compute-options.md).

## Related

- [Kubernetes IP or ENI exhaustion](../kubernetes/ip-eni-exhaustion.md): a related address-capacity failure in ENI-based pod networks.
- Source: [Amazon ECS - Runbook & Reference](../../sources/aws-ecs.md)

[^aws-ecs]: Amazon ECS - Runbook & Reference
