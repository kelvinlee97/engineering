---
type: Service
title: Amazon EC2 Auto Scaling
description: Groups of EC2 instances held between a minimum and maximum size, scaled by policies and self-healed by health checks.
tags: [aws, compute, scaling]
sources:
  - id: aws-auto-scaling-groups
    resource: https://github.com/kelvinlee97/engineering/blob/main/AWS/auto-scaling-groups/README.md
    title: "Amazon EC2 Auto Scaling - Runbook & Reference"
    author: human:kelvinlee97
    last_modified: 2026-09-24T14:48:10Z
generated: { by: claude-code/wiki-v1, at: 2026-09-25T07:00:00Z }
status: draft
---

An Auto Scaling group (ASG) keeps the right number of EC2 instances running. It never goes below its minimum or above its maximum; scaling policies move desired capacity within that range, and health checks replace any instance that fails. The two loops, health-driven replacement and policy-driven scaling, both launch instances from the same launch template.[^aws-auto-scaling-groups]

## Concepts

- Launch templates (AMI, instance type, key pair, security groups, user data); launch configurations are legacy.[^aws-auto-scaling-groups]
- EC2 status checks plus optional custom or ELB health checks; unhealthy instances are terminated and replaced.[^aws-auto-scaling-groups]
- Even spread across the chosen AZs; mixed instance types and On-Demand with Spot, with Capacity Rebalancing for Spot at risk.[^aws-auto-scaling-groups]
- Instance refresh for rolling or canary updates; lifecycle hooks and scale-in protection for stateful work.[^aws-auto-scaling-groups]
- No additional charge beyond the underlying resources.[^aws-auto-scaling-groups]

## Practices

- Versioned launch templates; target tracking on CPU, requests per target, or queue depth.[^aws-auto-scaling-groups]
- ELB health checks for application-aware replacement across several AZs.[^aws-auto-scaling-groups]

## Troubleshooting

| Symptom | Check |
| --- | --- |
| Not launching | Template validity, AZ capacity, instance type availability, IAM |
| Desired not maintained | Scaling activities, health, unexpected scale-in protection |
| Policy never triggers | Metric name and namespace, alarm thresholds |
| Instance refresh fails | `MinHealthyPercentage` and readiness |

As tabled in the note.[^aws-auto-scaling-groups]

## Related

- [Elastic Load Balancing](elb.md)
- Source: [Amazon EC2 Auto Scaling - Runbook & Reference](../../sources/aws-auto-scaling-groups.md)

[^aws-auto-scaling-groups]: Amazon EC2 Auto Scaling - Runbook & Reference
