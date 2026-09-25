---
type: Service
title: Amazon Route 53
description: "AWS's DNS service: domain registration, hosted zones with routing policies, and health checks that drop unhealthy targets from answers."
tags: [aws, networking, dns]
sources:
  - id: aws-route53
    resource: https://github.com/kelvinlee97/engineering/blob/main/AWS/route53/README.md
    title: "Amazon Route 53 - Runbook & Reference"
    author: human:kelvinlee97
    last_modified: 2026-09-24T14:48:10Z
generated: { by: claude-code/wiki-v1, at: 2026-09-25T07:00:00Z }
status: draft
---

Route 53 is AWS's DNS service with three functions: domain registration, DNS routing, and health checking. A query lands in a hosted zone, a routing policy picks which records to answer with, and health checks can remove unhealthy targets before a client sees them.[^aws-route53]

## Concepts

- Public and private (VPC-internal) hosted zones.[^aws-route53]
- Alias records map a name to an AWS resource such as ELB, CloudFront, or S3, with no charge and no TTL issues; prefer them to CNAME or A records for AWS targets.[^aws-route53]
- Routing policies: simple, weighted, latency, failover, geolocation, geoproximity, and multivalue.[^aws-route53]
- DNSSEC signs zones against spoofing; VPC Resolver and DNS Firewall handle private resolution and outbound filtering.[^aws-route53]

## Practices

- Combine health checks with failover routing across Regions, and alarm on health check status in CloudWatch.[^aws-route53]
- Lower TTLs before planned changes.[^aws-route53]

## Troubleshooting

| Symptom | Check |
| --- | --- |
| Not resolving | NS delegation at the registrar, records exist, TTL caching |
| Failover not working | Health check status, evaluation windows, failover records |
| Alias errors | Correct hosted zone ID of the target, fully qualified name |
| Private DNS fails in VPC | VPC DNS attributes, Resolver rules, VPC association |
| DNSSEC issues | Key signing and DS record at the registrar |

As tabled in the note.[^aws-route53] Default quotas are 500 hosted zones and 10,000 records per zone, adjustable.[^aws-route53] See [AWS global traffic routing](global-traffic-routing.md).

## Related

- Source: [Amazon Route 53 - Runbook & Reference](../../sources/aws-route53.md)

[^aws-route53]: Amazon Route 53 - Runbook & Reference
