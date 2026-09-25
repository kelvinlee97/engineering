---
type: Service
title: AWS Global Accelerator
description: Static anycast IP addresses that carry user traffic over the AWS network to the healthiest, nearest regional endpoint.
tags: [aws, networking]
sources:
  - id: aws-global-accelerator
    resource: https://github.com/kelvinlee97/engineering/blob/main/AWS/global-accelerator/README.md
    title: "AWS Global Accelerator - Runbook & Reference"
    author: human:kelvinlee97
    last_modified: 2026-09-24T14:48:10Z
generated: { by: claude-code/wiki-v1, at: 2026-09-25T07:00:00Z }
status: draft
---

Global Accelerator gives an application static anycast IP addresses and routes traffic over the AWS global network to the best regional endpoint by health, client location, and your weights.[^aws-global-accelerator]

## Concepts

- An accelerator has two static IPv4 addresses (four for dual-stack) for its whole lifetime; deleting it releases them.[^aws-global-accelerator]
- Listeners (TCP/UDP ports) route to regional endpoint groups of NLBs, ALBs, EC2 instances, or Elastic IPs, weighted and health-checked.[^aws-global-accelerator]
- Custom routing accelerators map users to specific VPC subnet private IPs, for gaming and real-time apps.[^aws-global-accelerator]
- It reacts instantly to endpoint health changes.[^aws-global-accelerator]

## Practices

- Use it for global, latency-sensitive, or availability-critical apps instead of DNS failover alone.[^aws-global-accelerator]
- Endpoint groups in several Regions with weights for active/passive or active/active.[^aws-global-accelerator]
- Protect production accelerators from deletion with IAM or tag policies.[^aws-global-accelerator]

## Troubleshooting

| Symptom | Check |
| --- | --- |
| Clients cannot connect | Listener ports, endpoint group health |
| Traffic to an unhealthy Region | Endpoint health and weights |
| Endpoint unreachable | SGs and NACLs allow Global Accelerator's published ranges |
| No performance gain | DNS points at the static IPs |

As tabled in the note.[^aws-global-accelerator] See [AWS global traffic routing](global-traffic-routing.md).

## Related

- Source: [AWS Global Accelerator - Runbook & Reference](../../sources/aws-global-accelerator.md)

[^aws-global-accelerator]: AWS Global Accelerator - Runbook & Reference
