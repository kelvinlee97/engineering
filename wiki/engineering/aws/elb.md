---
type: Service
title: Elastic Load Balancing
description: AWS's load balancers (ALB, NLB, GWLB) that spread traffic across healthy targets in several Availability Zones.
tags: [aws, networking, load-balancing]
sources:
  - id: aws-elb
    resource: https://github.com/kelvinlee97/engineering/blob/main/AWS/elb/README.md
    title: "Elastic Load Balancing - Runbook & Reference"
    author: human:kelvinlee97
    last_modified: 2026-09-24T14:48:10Z
generated: { by: claude-code/wiki-v1, at: 2026-09-25T07:00:00Z }
status: draft
---

Elastic Load Balancing distributes incoming traffic across targets (EC2 instances, containers, IP addresses, Lambda functions) in one or more Availability Zones, sending traffic only to healthy targets and scaling automatically.[^aws-elb]

| Type | Layer | Use |
| --- | --- | --- |
| Application Load Balancer | 7 | HTTP/HTTPS, path and host routing, WAF, Lambda targets, WebSocket |
| Network Load Balancer | 4 | TCP/UDP, static IPs, TLS termination, extreme throughput |
| Gateway Load Balancer | 3 | Route traffic through third-party virtual appliances |
| Classic | | Previous generation; migrate to ALB or NLB |

As listed in the note.[^aws-elb]

## Concepts and practices

- Listeners accept connections by protocol and port; target groups route to registered targets and health-check them.[^aws-elb]
- Register targets in several AZs with cross-zone load balancing; tune health checks to reflect real application health.[^aws-elb]
- Terminate TLS with ACM certificates; send access logs to S3; attach WAF to ALBs; pair with [Auto Scaling](auto-scaling-groups.md) so new instances register automatically.[^aws-elb]

## Troubleshooting

| Symptom | Check |
| --- | --- |
| `503 Service Unavailable` | No healthy targets |
| Target unhealthy | Health check path and port, security group, the application |
| Connection timeouts | Idle timeout and application keepalive |
| NLB client IP surprises | NLB preserves client IPs, so target SGs must allow client CIDRs |
| Uneven distribution | Cross-zone setting and registration |

As tabled in the note.[^aws-elb] The default quota is 20 load balancers per Region, adjustable.[^aws-elb]

## Related

- Source: [Elastic Load Balancing - Runbook & Reference](../../sources/aws-elb.md)

[^aws-elb]: Elastic Load Balancing - Runbook & Reference
