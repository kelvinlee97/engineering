---
type: Comparison
title: AWS global traffic routing
description: 'Getting users to the right AWS endpoint: Route 53 DNS, CloudFront caching, and Global Accelerator, and how to choose between them.'
tags:
- aws
- networking
- cdn
aliases:
- engineering/aws/global-traffic-routing
- engineering/aws/route53
- engineering/aws/cloudfront
- engineering/aws/global-accelerator
sources:
- id: aws-route53
  resource: https://github.com/kelvinlee97/engineering/blob/main/AWS/route53/README.md
  title: Amazon Route 53 - Runbook & Reference
  author: human:kelvinlee97
  last_modified: 2026-09-24T14:48:10Z
- id: aws-cloudfront
  resource: https://github.com/kelvinlee97/engineering/blob/main/AWS/cloudfront/README.md
  title: Amazon CloudFront - Runbook & Reference
  author: human:kelvinlee97
  last_modified: 2026-09-24T14:48:10Z
- id: aws-global-accelerator
  resource: https://github.com/kelvinlee97/engineering/blob/main/AWS/global-accelerator/README.md
  title: AWS Global Accelerator - Runbook & Reference
  author: human:kelvinlee97
  last_modified: 2026-09-24T14:48:10Z
generated: { by: claude-code/wiki-v1, at: 2026-09-25T12:00:00Z }
status: draft
---
Route 53, CloudFront, and Global Accelerator all sit in front of regional AWS endpoints and steer users to them. This page compares them first, then covers each service.

## Choosing a service

Three AWS services put traffic in front of regional endpoints. They differ in what they hand the client and how fast they react to failure.

| | Route 53 | CloudFront | Global Accelerator |
| --- | --- | --- | --- |
| What the client gets | A DNS answer chosen by routing policy | Content from the nearest edge cache | Two static anycast IPs |
| Traffic | Goes direct to the chosen endpoint | HTTP(S); misses go to the origin | TCP/UDP over the AWS network |
| Failure handling | Health checks drop records; clients may cache by TTL | Origin errors surface as `502`[^aws-cloudfront] | Reacts instantly to endpoint health |
| Best fit | Name resolution and DNS failover | Cacheable web content | Latency- or availability-critical apps, non-HTTP |

The Global Accelerator note itself recommends it over DNS-based failover alone for availability-critical apps, and suggests keeping DNS TTLs short in front of it.[^aws-global-accelerator] Analysis: the DNS TTL is what limits Route 53 failover, since clients keep a cached answer until it expires; the Route 53 note's advice to lower TTLs before changes reflects the same limit.[^aws-route53]

## Amazon Route 53

Route 53 is AWS's DNS service with three functions: domain registration, DNS routing, and health checking. A query lands in a hosted zone, a routing policy picks which records to answer with, and health checks can remove unhealthy targets before a client sees them.[^aws-route53]

### Concepts

- Public and private (VPC-internal) hosted zones.
- Alias records map a name to an AWS resource such as ELB, CloudFront, or S3, with no charge and no TTL issues; prefer them to CNAME or A records for AWS targets.
- Routing policies: simple, weighted, latency, failover, geolocation, geoproximity, and multivalue.
- DNSSEC signs zones against spoofing; VPC Resolver and DNS Firewall handle private resolution and outbound filtering.[^aws-route53]

### Practices

- Combine health checks with failover routing across Regions, and alarm on health check status in CloudWatch.
- Lower TTLs before planned changes.[^aws-route53]

### Troubleshooting

| Symptom | Check |
| --- | --- |
| Not resolving | NS delegation at the registrar, records exist, TTL caching |
| Failover not working | Health check status, evaluation windows, failover records |
| Alias errors | Correct hosted zone ID of the target, fully qualified name |
| Private DNS fails in VPC | VPC DNS attributes, Resolver rules, VPC association |
| DNSSEC issues | Key signing and DS record at the registrar |

As tabled in the note. Default quotas are 500 hosted zones and 10,000 records per zone, adjustable.[^aws-route53] See [AWS global traffic routing](#choosing-a-service).

## Amazon CloudFront

CloudFront is a content delivery network (CDN). Each request is routed to the lowest-latency edge location; a cache hit never touches the origin, and a miss is fetched from the origin. That makes cache configuration the main lever over cost and freshness.[^aws-cloudfront]

### Concepts

- A distribution maps a domain to origins (S3, ELB or API Gateway, custom HTTP servers) and cache behaviors.
- A cache behavior sets path patterns, TTL (default 24 hours, minimum 0), and which headers and cookies are forwarded.
- Invalidations remove cached objects before their TTL expires.
- Two independent gates for private content: Origin Access Control (OAC) stops direct access to the origin, and signed URLs or cookies stop CloudFront serving to unauthorized viewers.[^aws-cloudfront]

### Practices

- S3 origin with OAC; signed URLs or cookies rather than public buckets.
- Set `Cache-Control` and avoid forwarding headers or cookies you don't need; a higher hit ratio means fewer origin fetches.
- ACM certificate with HTTPS enforced; access logs; WAF.[^aws-cloudfront]

### Troubleshooting

| Symptom | Check |
| --- | --- |
| Content not updating | TTL and cache behavior; invalidate changed paths |
| `403` from S3 origin | OAC or OAI and the bucket policy |
| `502` from origin | Origin health, custom origin settings, security groups |
| Slow first byte | Origin latency and hit ratio |

As tabled in the note.[^aws-cloudfront] See [AWS global traffic routing](#choosing-a-service).

## AWS Global Accelerator

Global Accelerator gives an application static anycast IP addresses and routes traffic over the AWS global network to the best regional endpoint by health, client location, and your weights.[^aws-global-accelerator]

### Concepts

- An accelerator has two static IPv4 addresses (four for dual-stack) for its whole lifetime; deleting it releases them.
- Listeners (TCP/UDP ports) route to regional endpoint groups of NLBs, ALBs, EC2 instances, or Elastic IPs, weighted and health-checked.
- Custom routing accelerators map users to specific VPC subnet private IPs, for gaming and real-time apps.
- It reacts instantly to endpoint health changes.[^aws-global-accelerator]

### Practices

- Use it for global, latency-sensitive, or availability-critical apps instead of DNS failover alone.
- Endpoint groups in several Regions with weights for active/passive or active/active.
- Protect production accelerators from deletion with IAM or tag policies.[^aws-global-accelerator]

### Troubleshooting

| Symptom | Check |
| --- | --- |
| Clients cannot connect | Listener ports, endpoint group health |
| Traffic to an unhealthy Region | Endpoint health and weights |
| Endpoint unreachable | SGs and NACLs allow Global Accelerator's published ranges |
| No performance gain | DNS points at the static IPs |

As tabled in the note.[^aws-global-accelerator] See [AWS global traffic routing](#choosing-a-service).

## Related
- [Application security](application-security.md): WAF and Shield at the edge.
- [Domain index](index.md): other pages in this domain.

[^aws-route53]: [Amazon Route 53 - Runbook & Reference](../../sources/aws-route53.md), [original](https://github.com/kelvinlee97/engineering/blob/main/AWS/route53/README.md)
[^aws-cloudfront]: [Amazon CloudFront - Runbook & Reference](../../sources/aws-cloudfront.md), [original](https://github.com/kelvinlee97/engineering/blob/main/AWS/cloudfront/README.md)
[^aws-global-accelerator]: [AWS Global Accelerator - Runbook & Reference](../../sources/aws-global-accelerator.md), [original](https://github.com/kelvinlee97/engineering/blob/main/AWS/global-accelerator/README.md)
