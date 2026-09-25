---
type: Service
title: Amazon EC2
description: "AWS's virtual servers: the instance type sets compute, memory, network, and storage, and the lifecycle state decides what you pay and what data survives."
tags: [aws, compute]
sources:
  - id: aws-ec2
    resource: https://github.com/kelvinlee97/engineering/blob/main/AWS/ec2/README.md
    title: "Amazon EC2 - Runbook & Reference"
    author: human:kelvinlee97
    last_modified: 2026-09-24T14:48:10Z
generated: { by: claude-code/wiki-v1, at: 2026-09-25T07:00:00Z }
status: draft
---

Amazon Elastic Compute Cloud (EC2) provides on-demand virtual servers called instances; the instance type sets the balance of compute, memory, network, and storage.[^aws-ec2]

## Lifecycle and billing

| State | Instance usage billing |
| --- | --- |
| `pending` | Not billed |
| `running` | Per second, 1-minute minimum |
| `stopping` | Not billed, except when hibernating |
| `stopped` | Not billed; EBS volumes and Elastic IPs still cost |
| `shutting-down`, `terminated` | Not billed |

As tabled in the note.[^aws-ec2]

| Action | Effect |
| --- | --- |
| Reboot | Same host; keeps public DNS, private IP, and instance-store data |
| Stop/start (EBS-backed) | New host; keeps private IPv4 and Elastic IP; new public IPv4; instance store erased |
| Hibernate (EBS-backed) | RAM saved to the EBS root volume |
| Terminate | Permanent; root volume deleted by default via `DeleteOnTermination` |

As described in the note.[^aws-ec2]

## Pricing options

On-Demand (per second, 60-second minimum), Savings Plans or Reserved Instances (1 or 3 year commitments), Spot (cheap, reclaimable), and Dedicated Hosts or Capacity Reservations.[^aws-ec2]

## Practices

- Least-privilege security groups; IAM roles instead of long-term keys; termination protection on critical instances.[^aws-ec2]
- Regular EBS snapshots and AMIs; patch through Systems Manager.[^aws-ec2]

## Troubleshooting

| Symptom | Check |
| --- | --- |
| Status check fails | Reboot; if it persists, stop and start |
| No SSH/RDP | SG port 22/3389 and source, routes and NACL, OS service, key pair |
| Public IP changed | Expected after stop/start without an Elastic IP |
| Instance-store data gone | Expected on stop, hibernate, terminate |
| Burstable credits exhausted (t2/t3) | Unlimited mode or a bigger type |

As tabled in the note.[^aws-ec2]

## Related

- Source: [Amazon EC2 - Runbook & Reference](../../sources/aws-ec2.md)

[^aws-ec2]: Amazon EC2 - Runbook & Reference
