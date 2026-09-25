---
type: Concept
title: Backend for frontend
description: "A backend that serves one browser-facing application: it enforces session and authorization rules, adapts requests, and calls downstream services."
tags: [bff, architecture, nodejs]
sources:
  - id: express-bff-deployment-guide
    resource: https://github.com/kelvinlee97/engineering/blob/main/Nodejs/guides/express-bff-production-deployment/README.md
    title: Node.js / Express BFF Production Deployment for Beginners
    author: human:kelvinlee97
    last_modified: 2026-09-24T14:48:10Z
  - id: modern-bff-assessment
    resource: https://github.com/kelvinlee97/engineering/blob/main/Nodejs/guides/modern-bff-architecture-assessment/README.md
    title: Modern BFF Architecture Assessment for Beginners
    author: human:kelvinlee97
    last_modified: 2026-09-24T14:48:10Z
generated: { by: claude-code/wiki-v1, at: 2026-09-25T04:45:00Z }
status: draft
---
A backend for frontend (BFF) is a backend used by a browser-facing application. It can enforce session and authorization rules, adapt requests, and call downstream services; it is neither the gateway in front of it nor the downstream API behind it.[^express-bff-deployment-guide]

## Is the pattern still current?

The assessment guide argues that it is not obsolete: a BFF still provides browser-specific authorization, request adaptation, and aggregation. What ages is the operating model around it: manually managed hosts, mutable releases, process-local state, shared long-lived credentials, and no usable evidence during an incident.[^modern-bff-assessment] It should stay browser-focused and not become a catch-all for unrelated domain logic.[^modern-bff-assessment]

## Minimum operating contract

| Contract | Minimum behaviour |
| --- | --- |
| Health | Liveness separate from readiness; readiness fails before a terminating instance gets new work |
| Shutdown | On `SIGTERM`/`SIGINT`, stop accepting requests, finish bounded in-flight work, exit non-zero past the deadline |
| State | No session, upload, job, or authoritative state held only in worker memory |
| Dependencies | Explicit timeouts; retries only for safe, bounded, idempotent operations |
| Observability | One correlation ID across gateway, BFF, and downstream; structured, redacted logs; RED metrics and release version |
| Delivery | One immutable artifact, progressive exposure, a rollback owner, and a tested rollback |

The guide asks for this contract on the current platform before any move.[^modern-bff-assessment] Stateless workers are also what PM2 cluster mode requires.[^express-bff-deployment-guide]

## Choosing a platform

| Option | Choose it when | Not merely because |
| --- | --- | --- |
| VM with systemd or PM2 | One or few stable services, predictable traffic, a clear host owner, automated release and rollback | Containers or Kubernetes are fashionable |
| Managed container service | A stateless BFF needing repeatable images and simple autoscaling, without operating Kubernetes | It is assumed to provide SLOs or security automatically |
| Kubernetes | Many independently released services and a staffed platform owner | There are only a few services and nobody can run the cluster |

As described in the assessment.[^modern-bff-assessment] It lists five gates before any migration, ending with approved network, identity, secret rotation, logging, on-call, and escalation for the target; if they are not met, improving the current platform is itself the modernization outcome.[^modern-bff-assessment]

## Related

- [Express BFF deployment](express-bff-deployment.md)
- [Reverse proxy gateway](reverse-proxy-gateway.md)
- Source: [Express BFF production deployment guide](../../sources/express-bff-deployment-guide.md)
- Source: [Modern BFF architecture assessment](../../sources/modern-bff-assessment.md)

[^express-bff-deployment-guide]: Node.js / Express BFF Production Deployment for Beginners
[^modern-bff-assessment]: Modern BFF Architecture Assessment for Beginners
