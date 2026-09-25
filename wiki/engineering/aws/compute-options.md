---
type: Comparison
title: AWS compute options
description: How EC2, Lambda, ECS, and EKS divide the work between you and AWS, and the hard limits that push a workload from one to another.
tags: [aws, compute, containers, serverless]
sources:
  - id: aws-ec2
    resource: https://github.com/kelvinlee97/engineering/blob/main/AWS/ec2/README.md
    title: "Amazon EC2 - Runbook & Reference"
    author: human:kelvinlee97
    last_modified: 2026-09-24T14:48:10Z
  - id: aws-lambda
    resource: https://github.com/kelvinlee97/engineering/blob/main/AWS/lambda/README.md
    title: "AWS Lambda - Runbook & Reference"
    author: human:kelvinlee97
    last_modified: 2026-09-24T14:48:10Z
  - id: aws-ecs
    resource: https://github.com/kelvinlee97/engineering/blob/main/AWS/ecs/README.md
    title: "Amazon ECS - Runbook & Reference"
    author: human:kelvinlee97
    last_modified: 2026-09-24T14:48:10Z
  - id: aws-eks
    resource: https://github.com/kelvinlee97/engineering/blob/main/AWS/eks/README.md
    title: "Amazon EKS - Runbook & Reference"
    author: human:kelvinlee97
    last_modified: 2026-09-24T14:48:10Z
generated: { by: claude-code/wiki-v1, at: 2026-09-25T07:00:00Z }
status: draft
---

AWS offers several places to run code. The main difference is how much of the stack you operate.

| | You manage | Notable limits |
| --- | --- | --- |
| [EC2](ec2.md) | The OS, patching, scaling | Per-Region instance quotas by type[^aws-ec2] |
| [Lambda](lambda.md) | Only the handler code | 15-minute timeout, 10,240 MB memory, 1,000 concurrent executions by default[^aws-lambda] |
| [ECS](ecs.md) | Task definitions; EC2 capacity unless on Fargate | Fargate tasks up to 16 vCPU and 120 GB[^aws-ecs] |
| [EKS](eks.md) | Kubernetes workloads; nodes unless on Auto Mode | Kubernetes version lifecycle and upgrades[^aws-eks] |

## Shared practice

All four notes give the workload an IAM role instead of long-term keys: EC2 instance roles, Lambda execution roles, ECS task and execution roles, and IRSA or Pod Identity in EKS.[^aws-ec2][^aws-lambda][^aws-ecs][^aws-eks]

Analysis: Lambda's timeout and payload limits are the usual reason to move a job to containers, and Kubernetes compatibility or ecosystem needs are the reason to pick EKS over ECS; the notes do not compare these directly.

## Related

- Source: [Amazon EC2 - Runbook & Reference](../../sources/aws-ec2.md)
- Source: [AWS Lambda - Runbook & Reference](../../sources/aws-lambda.md)
- Source: [Amazon ECS - Runbook & Reference](../../sources/aws-ecs.md)
- Source: [Amazon EKS - Runbook & Reference](../../sources/aws-eks.md)

[^aws-ec2]: Amazon EC2 - Runbook & Reference
[^aws-lambda]: AWS Lambda - Runbook & Reference
[^aws-ecs]: Amazon ECS - Runbook & Reference
[^aws-eks]: Amazon EKS - Runbook & Reference
