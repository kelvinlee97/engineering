---
type: Comparison
title: AWS global traffic routing
description: Route 53, CloudFront, and Global Accelerator all steer users toward healthy endpoints, but at different layers and with different failover speed.
tags: [aws, networking]
sources:
  - id: aws-route53
    resource: https://github.com/kelvinlee97/engineering/blob/main/AWS/route53/README.md
    title: "Amazon Route 53 - Runbook & Reference"
    author: human:kelvinlee97
    last_modified: 2026-09-24T14:48:10Z
  - id: aws-cloudfront
    resource: https://github.com/kelvinlee97/engineering/blob/main/AWS/cloudfront/README.md
    title: "Amazon CloudFront - Runbook & Reference"
    author: human:kelvinlee97
    last_modified: 2026-09-24T14:48:10Z
  - id: aws-global-accelerator
    resource: https://github.com/kelvinlee97/engineering/blob/main/AWS/global-accelerator/README.md
    title: "AWS Global Accelerator - Runbook & Reference"
    author: human:kelvinlee97
    last_modified: 2026-09-24T14:48:10Z
generated: { by: claude-code/wiki-v1, at: 2026-09-25T07:00:00Z }
status: draft
---

Three AWS services put traffic in front of regional endpoints. They differ in what they hand the client and how fast they react to failure.

| | Route 53 | CloudFront | Global Accelerator |
| --- | --- | --- | --- |
| What the client gets | A DNS answer chosen by routing policy[^aws-route53] | Content from the nearest edge cache[^aws-cloudfront] | Two static anycast IPs[^aws-global-accelerator] |
| Traffic | Goes direct to the chosen endpoint | HTTP(S); misses go to the origin | TCP/UDP over the AWS network |
| Failure handling | Health checks drop records; clients may cache by TTL[^aws-route53] | Origin errors surface as `502`[^aws-cloudfront] | Reacts instantly to endpoint health[^aws-global-accelerator] |
| Best fit | Name resolution and DNS failover | Cacheable web content | Latency- or availability-critical apps, non-HTTP |

The Global Accelerator note itself recommends it over DNS-based failover alone for availability-critical apps, and suggests keeping DNS TTLs short in front of it.[^aws-global-accelerator] Analysis: the DNS TTL is what limits Route 53 failover, since clients keep a cached answer until it expires; the Route 53 note's advice to lower TTLs before changes reflects the same limit.[^aws-route53]

## Related

- Source: [Amazon Route 53 - Runbook & Reference](../../sources/aws-route53.md)
- Source: [Amazon CloudFront - Runbook & Reference](../../sources/aws-cloudfront.md)
- Source: [AWS Global Accelerator - Runbook & Reference](../../sources/aws-global-accelerator.md)

[^aws-route53]: Amazon Route 53 - Runbook & Reference
[^aws-cloudfront]: Amazon CloudFront - Runbook & Reference
[^aws-global-accelerator]: AWS Global Accelerator - Runbook & Reference
