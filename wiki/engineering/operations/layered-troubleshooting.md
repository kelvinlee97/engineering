---
type: Pattern
title: Layered troubleshooting
description: Treat a failure as one broken link in a known chain of layers, and find the first broken link with read-only evidence before changing anything.
tags: [operations, incident, troubleshooting]
sources:
  - id: k8s-ip-eni-runbook
    resource: https://github.com/kelvinlee97/engineering/blob/main/Kubernetes/runbooks/insufficient-ip-or-eni/README.md
    title: Kubernetes IP or ENI Exhaustion Scheduling Failure Runbook
    author: human:kelvinlee97
    last_modified: 2026-09-24T14:48:10Z
  - id: express-bff-incidents-runbook
    resource: https://github.com/kelvinlee97/engineering/blob/main/Nodejs/runbooks/common-express-bff-incidents/README.md
    title: "Node.js / Express BFF: Ten Common Incidents Runbook"
    author: human:kelvinlee97
    last_modified: 2026-09-24T14:48:10Z
  - id: nginx-production-guide
    resource: https://github.com/kelvinlee97/engineering/blob/main/Nginx/guides/nginx-production-deployment/README.md
    title: Nginx Production Deployment and Operations for Beginners
    author: human:kelvinlee97
    last_modified: 2026-09-24T14:48:10Z
  - id: openresty-production-guide
    resource: https://github.com/kelvinlee97/engineering/blob/main/Nginx/guides/openresty-production-deployment/README.md
    title: OpenResty Production Deployment and Operations for Beginners
    author: human:kelvinlee97
    last_modified: 2026-09-24T14:48:10Z
generated: { by: claude-code/wiki-v1, at: 2026-09-25T04:45:00Z }
status: draft
---
Layered troubleshooting treats a failure as one broken link in a chain the request or workload depends on. You collect read-only evidence, walk the chain in order, and act only on the first broken link. All four operational sources in this wiki follow it.

| Source | The chain it walks |
| --- | --- |
| Kubernetes IP or ENI exhaustion | Node health, Pod subnet presence, subnet free IPs, node ENI/IP allocatable, IPAM and admission components[^k8s-ip-eni-runbook] |
| Express BFF incidents | Gateway, PM2 and BFF process, route and app logic, downstream dependency, host resources[^express-bff-incidents-runbook] |
| Nginx and OpenResty deployments | Configuration test, port ownership, upstream, file permissions, request mapping, ACME[^nginx-production-guide][^openresty-production-guide] |

## Rules the sources share

- **Evidence before action.** Start with read-only commands and preserve evidence before changing processes, releases, routes, credentials, or downstream targets.[^express-bff-incidents-runbook]
- **One symptom is not a cause.** A `Pending` Pod does not establish IP exhaustion, and one event string is not enough; correlate several signals.[^k8s-ip-eni-runbook] A downstream `4xx/5xx` is not proof the BFF is broken.[^express-bff-incidents-runbook]
- **A restart is not a diagnosis.** A restart can restore service temporarily without proving the root cause.[^express-bff-incidents-runbook]
- **Do not widen the blast radius.** Raising timeouts before finding the failing layer, `chmod -R 777`, or restarting everything are listed as things not to do.[^nginx-production-guide]

## Related

- [Incident closure criteria](incident-closure-criteria.md)
- [Safe change procedure](safe-change-procedure.md)
- Source: [Kubernetes IP or ENI exhaustion runbook](../../sources/k8s-ip-eni-runbook.md)
- Source: [Express BFF incidents runbook](../../sources/express-bff-incidents-runbook.md)
- Source: [Nginx production deployment guide](../../sources/nginx-production-guide.md)
- Source: [OpenResty production deployment guide](../../sources/openresty-production-guide.md)

[^k8s-ip-eni-runbook]: Kubernetes IP or ENI Exhaustion Scheduling Failure Runbook
[^express-bff-incidents-runbook]: Node.js / Express BFF: Ten Common Incidents Runbook
[^nginx-production-guide]: Nginx Production Deployment and Operations for Beginners
[^openresty-production-guide]: OpenResty Production Deployment and Operations for Beginners
