---
type: Service
title: Amazon CloudFront
description: "AWS's CDN: requests are answered from the nearest edge cache, and only misses reach the origin, so cache settings control both cost and freshness."
tags: [aws, networking, cdn]
sources:
  - id: aws-cloudfront
    resource: https://github.com/kelvinlee97/engineering/blob/main/AWS/cloudfront/README.md
    title: "Amazon CloudFront - Runbook & Reference"
    author: human:kelvinlee97
    last_modified: 2026-09-24T14:48:10Z
generated: { by: claude-code/wiki-v1, at: 2026-09-25T07:00:00Z }
status: draft
---

CloudFront is a content delivery network (CDN). Each request is routed to the lowest-latency edge location; a cache hit never touches the origin, and a miss is fetched from the origin. That makes cache configuration the main lever over cost and freshness.[^aws-cloudfront]

## Concepts

- A distribution maps a domain to origins (S3, ELB or API Gateway, custom HTTP servers) and cache behaviors.[^aws-cloudfront]
- A cache behavior sets path patterns, TTL (default 24 hours, minimum 0), and which headers and cookies are forwarded.[^aws-cloudfront]
- Invalidations remove cached objects before their TTL expires.[^aws-cloudfront]
- Two independent gates for private content: Origin Access Control (OAC) stops direct access to the origin, and signed URLs or cookies stop CloudFront serving to unauthorized viewers.[^aws-cloudfront]

## Practices

- S3 origin with OAC; signed URLs or cookies rather than public buckets.[^aws-cloudfront]
- Set `Cache-Control` and avoid forwarding headers or cookies you don't need; a higher hit ratio means fewer origin fetches.[^aws-cloudfront]
- ACM certificate with HTTPS enforced; access logs; WAF.[^aws-cloudfront]

## Troubleshooting

| Symptom | Check |
| --- | --- |
| Content not updating | TTL and cache behavior; invalidate changed paths |
| `403` from S3 origin | OAC or OAI and the bucket policy |
| `502` from origin | Origin health, custom origin settings, security groups |
| Slow first byte | Origin latency and hit ratio |

As tabled in the note.[^aws-cloudfront] See [AWS global traffic routing](global-traffic-routing.md).

## Related

- Source: [Amazon CloudFront - Runbook & Reference](../../sources/aws-cloudfront.md)

[^aws-cloudfront]: Amazon CloudFront - Runbook & Reference
