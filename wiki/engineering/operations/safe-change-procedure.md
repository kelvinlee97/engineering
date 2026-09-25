---
type: Pattern
title: Safe change procedure
description: Make one small, backed-up change at a time, validate it before applying, apply it gracefully, verify each layer, and keep a known-good rollback.
tags: [operations, change-management]
sources:
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
  - id: express-bff-deployment-guide
    resource: https://github.com/kelvinlee97/engineering/blob/main/Nodejs/guides/express-bff-production-deployment/README.md
    title: Node.js / Express BFF Production Deployment for Beginners
    author: human:kelvinlee97
    last_modified: 2026-09-24T14:48:10Z
  - id: k8s-ip-eni-runbook
    resource: https://github.com/kelvinlee97/engineering/blob/main/Kubernetes/runbooks/insufficient-ip-or-eni/README.md
    title: Kubernetes IP or ENI Exhaustion Scheduling Failure Runbook
    author: human:kelvinlee97
    last_modified: 2026-09-24T14:48:10Z
  - id: zookeeper-production-guide
    resource: https://github.com/kelvinlee97/engineering/blob/main/ZooKeeper/guides/production-deployment/README.md
    title: ZooKeeper Production Deployment Guide for DevOps Beginners
    author: human:kelvinlee97
    last_modified: 2026-09-24T14:48:10Z
  - id: ubuntu-apt-guide
    resource: https://github.com/kelvinlee97/engineering/blob/main/Ubuntu/apt/README.md
    title: Common Ubuntu APT Operations
    author: human:kelvinlee97
    last_modified: 2026-09-24T14:48:10Z
generated: { by: claude-code/wiki-v1, at: 2026-09-25T05:15:00Z }
status: draft
---
The sources in this wiki apply production changes with the same loop: record intent, back up, make one small change, validate before applying, apply gracefully, verify, and keep a way back.

## The loop

1. **Record intent and back up.** Back up the file, configuration, or release being changed.[^nginx-production-guide]
2. **Change one concern.** One small edit at a time.[^openresty-production-guide]
3. **Validate before applying.** For packages, `apt-get -s` simulates the change so the plan can be read before anything is installed or removed; the APT guide calls this simulation the step that protects you from held versions, phased rollouts, and locks.[^ubuntu-apt-guide] For servers and releases: `nginx -t` or `openresty -t` before any reload; for a release, `npm ci`, tests, and `node --check` in the new release directory before switching.[^nginx-production-guide][^express-bff-deployment-guide]
4. **Apply gracefully.** A reload validates the new configuration and then gracefully replaces workers, which is safer than a routine restart; PM2 `reload` does the same for cluster workers.[^nginx-production-guide][^express-bff-deployment-guide]
5. **Verify each layer.** Health, an approved real request, and logs, not just an open port.[^nginx-production-guide]
6. **Roll back cleanly.** Restore the backup and test it before reloading, or repoint `current` to the known-good release.[^nginx-production-guide][^express-bff-deployment-guide]

## One member at a time in a quorum system

For a replicated system the loop gains a stop rule. The ZooKeeper guide changes one member, waits for it to rejoin, checks all three members, and continues only if there is still one leader and two followers; otherwise it stops and rolls back that one member. Two members are never changed at once, because three members tolerate only one failure.[^zookeeper-production-guide]

## Restarts are a decision, not a reflex

The Kubernetes runbook says adding capacity does not justify restarting every workload: restart only the affected one, after checking replicas, update strategy, and PodDisruptionBudgets, and with the service owner's approval.[^k8s-ip-eni-runbook]

## Related

- Source: [Common Ubuntu APT operations](../../sources/ubuntu-apt-guide.md)
- Source: [ZooKeeper production deployment guide](../../sources/zookeeper-production-guide.md)
- [Layered troubleshooting](layered-troubleshooting.md)
- Source: [Nginx production deployment guide](../../sources/nginx-production-guide.md)
- Source: [OpenResty production deployment guide](../../sources/openresty-production-guide.md)
- Source: [Express BFF production deployment guide](../../sources/express-bff-deployment-guide.md)
- Source: [Kubernetes IP or ENI exhaustion runbook](../../sources/k8s-ip-eni-runbook.md)

[^nginx-production-guide]: Nginx Production Deployment and Operations for Beginners
[^openresty-production-guide]: OpenResty Production Deployment and Operations for Beginners
[^ubuntu-apt-guide]: Common Ubuntu APT Operations
[^express-bff-deployment-guide]: Node.js / Express BFF Production Deployment for Beginners
[^zookeeper-production-guide]: ZooKeeper Production Deployment Guide for DevOps Beginners
[^k8s-ip-eni-runbook]: Kubernetes IP or ENI Exhaustion Scheduling Failure Runbook
