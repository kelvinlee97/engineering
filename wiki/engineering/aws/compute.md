---
type: Service
title: AWS compute
description: Choosing AWS compute, and running EC2 instances behind load balancers in Auto Scaling groups.
tags:
- aws
- compute
aliases:
- engineering/aws/compute-options
- engineering/aws/ec2
- engineering/aws/auto-scaling-groups
- engineering/aws/elb
sources:
- id: aws-ec2
  resource: https://github.com/kelvinlee97/engineering/blob/main/AWS/ec2/README.md
  title: Amazon EC2 - Runbook & Reference
  author: human:kelvinlee97
  last_modified: 2026-09-24T14:48:10Z
- id: aws-lambda
  resource: https://github.com/kelvinlee97/engineering/blob/main/AWS/lambda/README.md
  title: AWS Lambda - Runbook & Reference
  author: human:kelvinlee97
  last_modified: 2026-09-24T14:48:10Z
- id: aws-ecs
  resource: https://github.com/kelvinlee97/engineering/blob/main/AWS/ecs/README.md
  title: Amazon ECS - Runbook & Reference
  author: human:kelvinlee97
  last_modified: 2026-09-24T14:48:10Z
- id: aws-eks
  resource: https://github.com/kelvinlee97/engineering/blob/main/AWS/eks/README.md
  title: Amazon EKS - Runbook & Reference
  author: human:kelvinlee97
  last_modified: 2026-09-24T14:48:10Z
- id: aws-auto-scaling-groups
  resource: https://github.com/kelvinlee97/engineering/blob/main/AWS/auto-scaling-groups/README.md
  title: Amazon EC2 Auto Scaling - Runbook & Reference
  author: human:kelvinlee97
  last_modified: 2026-09-24T14:48:10Z
- id: aws-elb
  resource: https://github.com/kelvinlee97/engineering/blob/main/AWS/elb/README.md
  title: Elastic Load Balancing - Runbook & Reference
  author: human:kelvinlee97
  last_modified: 2026-09-24T14:48:10Z
generated: { by: claude-code/wiki-v1, at: 2026-09-25T12:00:00Z }
status: draft
---
AWS offers several places to run code, differing in how much of the stack you operate. This page compares the options, then covers the classic building blocks: EC2 instances, Auto Scaling groups that add and remove them, and Elastic Load Balancing in front.

## Choosing compute

AWS offers several places to run code. The main difference is how much of the stack you operate.

| | You manage | Notable limits |
| --- | --- | --- |
| [EC2](#amazon-ec2) | The OS, patching, scaling | Per-Region instance quotas by type[^aws-ec2] |
| [Lambda](containers-and-serverless.md#aws-lambda) | Only the handler code | 15-minute timeout, 10,240 MB memory, 1,000 concurrent executions by default[^aws-lambda] |
| [ECS](containers-and-serverless.md#amazon-ecs) | Task definitions; EC2 capacity unless on Fargate | Fargate tasks up to 16 vCPU and 120 GB[^aws-ecs] |
| [EKS](containers-and-serverless.md#amazon-eks) | Kubernetes workloads; nodes unless on Auto Mode | Kubernetes version lifecycle and upgrades[^aws-eks] |

### Shared practice

All four notes give the workload an IAM role instead of long-term keys: EC2 instance roles, Lambda execution roles, ECS task and execution roles, and IRSA or Pod Identity in EKS.[^aws-ec2][^aws-lambda][^aws-ecs][^aws-eks]

Analysis: Lambda's timeout and payload limits are the usual reason to move a job to containers, and Kubernetes compatibility or ecosystem needs are the reason to pick EKS over ECS; the notes do not compare these directly.

## Amazon EC2

Amazon Elastic Compute Cloud (EC2) provides on-demand virtual servers called instances; the instance type sets the balance of compute, memory, network, and storage.[^aws-ec2]

### Lifecycle and billing

| State | Instance usage billing |
| --- | --- |
| `pending` | Not billed |
| `running` | Per second, 1-minute minimum |
| `stopping` | Not billed, except when hibernating |
| `stopped` | Not billed; EBS volumes and Elastic IPs still cost |
| `shutting-down`, `terminated` | Not billed |

As tabled in the note.

| Action | Effect |
| --- | --- |
| Reboot | Same host; keeps public DNS, private IP, and instance-store data |
| Stop/start (EBS-backed) | New host; keeps private IPv4 and Elastic IP; new public IPv4; instance store erased |
| Hibernate (EBS-backed) | RAM saved to the EBS root volume |
| Terminate | Permanent; root volume deleted by default via `DeleteOnTermination` |

As described in the note.[^aws-ec2]

### Pricing options

On-Demand (per second, 60-second minimum), Savings Plans or Reserved Instances (1 or 3 year commitments), Spot (cheap, reclaimable), and Dedicated Hosts or Capacity Reservations.[^aws-ec2]

### Practices

- Least-privilege security groups; IAM roles instead of long-term keys; termination protection on critical instances.
- Regular EBS snapshots and AMIs; patch through Systems Manager.[^aws-ec2]

### Troubleshooting

| Symptom | Check |
| --- | --- |
| Status check fails | Reboot; if it persists, stop and start |
| No SSH/RDP | SG port 22/3389 and source, routes and NACL, OS service, key pair |
| Public IP changed | Expected after stop/start without an Elastic IP |
| Instance-store data gone | Expected on stop, hibernate, terminate |
| Burstable credits exhausted (t2/t3) | Unlimited mode or a bigger type |

As tabled in the note.[^aws-ec2]

## Amazon EC2 Auto Scaling

An Auto Scaling group (ASG) keeps the right number of EC2 instances running. It never goes below its minimum or above its maximum; scaling policies move desired capacity within that range, and health checks replace any instance that fails. The two loops, health-driven replacement and policy-driven scaling, both launch instances from the same launch template.[^aws-auto-scaling-groups]

### Concepts

- Launch templates (AMI, instance type, key pair, security groups, user data); launch configurations are legacy.
- EC2 status checks plus optional custom or ELB health checks; unhealthy instances are terminated and replaced.
- Even spread across the chosen AZs; mixed instance types and On-Demand with Spot, with Capacity Rebalancing for Spot at risk.
- Instance refresh for rolling or canary updates; lifecycle hooks and scale-in protection for stateful work.
- No additional charge beyond the underlying resources.[^aws-auto-scaling-groups]

### Practices

- Versioned launch templates; target tracking on CPU, requests per target, or queue depth.
- ELB health checks for application-aware replacement across several AZs.[^aws-auto-scaling-groups]

### Troubleshooting

| Symptom | Check |
| --- | --- |
| Not launching | Template validity, AZ capacity, instance type availability, IAM |
| Desired not maintained | Scaling activities, health, unexpected scale-in protection |
| Policy never triggers | Metric name and namespace, alarm thresholds |
| Instance refresh fails | `MinHealthyPercentage` and readiness |

As tabled in the note.[^aws-auto-scaling-groups]

## Elastic Load Balancing

Elastic Load Balancing distributes incoming traffic across targets (EC2 instances, containers, IP addresses, Lambda functions) in one or more Availability Zones, sending traffic only to healthy targets and scaling automatically.

| Type | Layer | Use |
| --- | --- | --- |
| Application Load Balancer | 7 | HTTP/HTTPS, path and host routing, WAF, Lambda targets, WebSocket |
| Network Load Balancer | 4 | TCP/UDP, static IPs, TLS termination, extreme throughput |
| Gateway Load Balancer | 3 | Route traffic through third-party virtual appliances |
| Classic | | Previous generation; migrate to ALB or NLB |

As listed in the note.[^aws-elb]

### Concepts and practices

- Listeners accept connections by protocol and port; target groups route to registered targets and health-check them.
- Register targets in several AZs with cross-zone load balancing; tune health checks to reflect real application health.
- Terminate TLS with ACM certificates; send access logs to S3; attach WAF to ALBs; pair with [Auto Scaling](#amazon-ec2-auto-scaling) so new instances register automatically.[^aws-elb]

### Troubleshooting

| Symptom | Check |
| --- | --- |
| `503 Service Unavailable` | No healthy targets |
| Target unhealthy | Health check path and port, security group, the application |
| Connection timeouts | Idle timeout and application keepalive |
| NLB client IP surprises | NLB preserves client IPs, so target SGs must allow client CIDRs |
| Uneven distribution | Cross-zone setting and registration |

As tabled in the note. The default quota is 20 load balancers per Region, adjustable.[^aws-elb]

## Related
- [Compute platforms](compute-platforms.md): Batch, Lightsail, Elastic Beanstalk, Outposts, and scaling beyond EC2.
- [Containers and serverless](containers-and-serverless.md): ECS, EKS, and Lambda.
- [Domain index](index.md): other pages in this domain.

[^aws-ec2]: [Amazon EC2 - Runbook & Reference](../../sources/aws-ec2.md), [original](https://github.com/kelvinlee97/engineering/blob/main/AWS/ec2/README.md)
[^aws-lambda]: [AWS Lambda - Runbook & Reference](../../sources/aws-lambda.md), [original](https://github.com/kelvinlee97/engineering/blob/main/AWS/lambda/README.md)
[^aws-ecs]: [Amazon ECS - Runbook & Reference](../../sources/aws-ecs.md), [original](https://github.com/kelvinlee97/engineering/blob/main/AWS/ecs/README.md)
[^aws-eks]: [Amazon EKS - Runbook & Reference](../../sources/aws-eks.md), [original](https://github.com/kelvinlee97/engineering/blob/main/AWS/eks/README.md)
[^aws-auto-scaling-groups]: [Amazon EC2 Auto Scaling - Runbook & Reference](../../sources/aws-auto-scaling-groups.md), [original](https://github.com/kelvinlee97/engineering/blob/main/AWS/auto-scaling-groups/README.md)
[^aws-elb]: [Elastic Load Balancing - Runbook & Reference](../../sources/aws-elb.md), [original](https://github.com/kelvinlee97/engineering/blob/main/AWS/elb/README.md)
