---
type: Playbook
title: Express backend for frontend
description: The backend-for-frontend pattern, deploying an Express BFF to production, and handling its common incidents.
tags:
- web-serving
- nodejs
- bff
aliases:
- engineering/web-serving/backend-for-frontend
- engineering/web-serving/express-bff-deployment
- engineering/web-serving/express-bff-incidents
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
- id: express-bff-incidents-runbook
  resource: https://github.com/kelvinlee97/engineering/blob/main/Nodejs/runbooks/common-express-bff-incidents/README.md
  title: 'Node.js / Express BFF: Ten Common Incidents Runbook'
  author: human:kelvinlee97
  last_modified: 2026-09-24T14:48:10Z
generated: { by: claude-code/wiki-v1, at: 2026-09-25T12:00:00Z }
status: draft
---
A backend for frontend (BFF) is a backend that serves one browser-facing application. This page covers the pattern and whether it is still current, then the runbooks for deploying an Express BFF behind a gateway and for handling its common production incidents.

## Backend for frontend

A backend for frontend (BFF) is a backend used by a browser-facing application. It can enforce session and authorization rules, adapt requests, and call downstream services; it is neither the gateway in front of it nor the downstream API behind it.[^express-bff-deployment-guide]

### Is the pattern still current?

The assessment guide argues that it is not obsolete: a BFF still provides browser-specific authorization, request adaptation, and aggregation. What ages is the operating model around it: manually managed hosts, mutable releases, process-local state, shared long-lived credentials, and no usable evidence during an incident. It should stay browser-focused and not become a catch-all for unrelated domain logic.[^modern-bff-assessment]

### Minimum operating contract

| Contract | Minimum behaviour |
| --- | --- |
| Health | Liveness separate from readiness; readiness fails before a terminating instance gets new work |
| Shutdown | On `SIGTERM`/`SIGINT`, stop accepting requests, finish bounded in-flight work, exit non-zero past the deadline |
| State | No session, upload, job, or authoritative state held only in worker memory |
| Dependencies | Explicit timeouts; retries only for safe, bounded, idempotent operations |
| Observability | One correlation ID across gateway, BFF, and downstream; structured, redacted logs; RED metrics and release version |
| Delivery | One immutable artifact, progressive exposure, a rollback owner, and a tested rollback |

The guide asks for this contract on the current platform before any move.[^modern-bff-assessment] Stateless workers are also what PM2 cluster mode requires.[^express-bff-deployment-guide]

### Choosing a platform

| Option | Choose it when | Not merely because |
| --- | --- | --- |
| VM with systemd or PM2 | One or few stable services, predictable traffic, a clear host owner, automated release and rollback | Containers or Kubernetes are fashionable |
| Managed container service | A stateless BFF needing repeatable images and simple autoscaling, without operating Kubernetes | It is assumed to provide SLOs or security automatically |
| Kubernetes | Many independently released services and a staffed platform owner | There are only a few services and nobody can run the cluster |

As described in the assessment. It lists five gates before any migration, ending with approved network, identity, secret rotation, logging, on-call, and escalation for the target; if they are not met, improving the current platform is itself the modernization outcome.[^modern-bff-assessment]

## Deploying an Express BFF

A baseline for deploying an Express [BFF](#backend-for-frontend) on a Linux VM, with PM2 running several workers as an unprivileged account behind a separately operated gateway.[^express-bff-deployment-guide]

### Host and account

- Use a supported Node.js LTS exact patch version recorded in the change; never an EOL or Current-only line.
- Create a system account and group, a release layout under `/srv/<app-name>` (`releases`, `shared`, `shared/logs`), and an environment file `/etc/<app-name>/production.env` owned `root:<app-group>` with mode `0640`. The account gets no root access and no SSH login.[^express-bff-deployment-guide]

### Application contract

A private `GET /healthz` and a graceful exit on `SIGINT` or `SIGTERM` that closes the server and exits within a timeout. Install dependencies with `npm ci`, which needs `package.json` and `package-lock.json` to agree; never run `npm install` on the server to fix a release.

The example ecosystem file runs `instances: 2` in `exec_mode: 'cluster'` with `max_memory_restart: '512M'`, `kill_timeout: 30000`, and `watch: false`, loading secrets with `--env-file`. The guide says these are safe examples, not capacity recommendations.[^express-bff-deployment-guide]

### Release and rollback

1. Unpack the approved artifact into a new directory under `releases/`, then run `npm ci --omit=dev`, tests, and `node --check` there.
2. Take a baseline (`pm2 status`, `pm2 describe`, `readlink -f current`, health).
3. Atomically repoint `current` with `ln -sfn`, then `pm2 start` (first time) or `pm2 reload` (cluster), `pm2 save`, and check status, logs, and health. PM2 can fall back to a restart if workers never become ready.
4. Continue only after health, a gateway request, a representative user flow, error rate, and release identity pass. Otherwise repoint `current` to the known-good release and reload; never delete the known-good release during observation.

Set up boot recovery once with `pm2 startup` (run only the command it prints, after review) and `pm2 save`; repeat when the Node binary location changes.[^express-bff-deployment-guide]

## Common incidents

Triage for an Express [BFF](#backend-for-frontend) supervised by PM2 cluster mode. Collect read-only evidence first (`pm2 status`, `pm2 describe`, recent logs, the `current` release target, loopback health, the listener, disk and memory); never start with `pm2 restart`, `reload`, `delete`, or `flush`.[^express-bff-incidents-runbook]

### The ten incidents

| # | Incident | First checks | Recovery |
| --- | --- | --- | --- |
| 1 | Request never reaches the BFF | Gateway logs, DNS/LB/TLS, gateway upstream, BFF health | Gateway or DNS owner's path; do not restart the BFF |
| 2 | PM2 daemon or boot restore missing | `pm2 ping`, startup unit, Node path after upgrades | Rebuild startup via the reviewed command, then `pm2 save` |
| 3 | Crash or restart loop | Restart count, logs against release ID, journal | Roll back a failing release, or escalate the error signature |
| 4 | Port conflict or wrong bind | `PORT` versus `ss -lntp`, loopback health, gateway upstream | Restore the approved private listener |
| 5 | Node, artifact, or lockfile mismatch | Versions, release ID, `npm ci` output | Redeploy the tested artifact, or return to known-good |
| 6 | Env, secret, or permission failure | Key names, env file owner and mode, redacted errors | Fix only the reference or permission; rotate if exposed |
| 7 | Gateway `502` / `504` | BFF health, gateway reachability, logs, latency | Fix the first failed layer; do not raise all timeouts |
| 8 | Downstream failure | DNS, TCP/TLS, HTTP status, response parsing | Downstream owner's fix, or roll back BFF adaptation |
| 9 | Memory growth or OOM | PM2 memory and restarts, host OOM, release correlation | Remove unhealthy capacity or roll back; do not raise heap limits blindly |
| 10 | CPU, event-loop, disk, or log pressure | CPU vs I/O wait, `df -h`, `df -i`, log growth | Approved capacity, rate limit, rollback, or retention |

As described in the runbook. A PM2 memory restart is mitigation, not leak diagnosis; Node diagnostic reports should use `--report-exclude-env` and a restricted directory.[^express-bff-incidents-runbook]

## Related

- [Reverse proxy gateway](reverse-proxy-gateway.md)
- [Safe change procedure](../operations/incident-operations.md#safe-change-procedure)
- [Layered troubleshooting](../operations/incident-operations.md#layered-troubleshooting)
- [Incident closure criteria](../operations/incident-operations.md#incident-closure-criteria)

[^express-bff-deployment-guide]: [Node.js / Express BFF Production Deployment for Beginners](../../sources/express-bff-deployment-guide.md), [original](https://github.com/kelvinlee97/engineering/blob/main/Nodejs/guides/express-bff-production-deployment/README.md)
[^modern-bff-assessment]: [Modern BFF Architecture Assessment for Beginners](../../sources/modern-bff-assessment.md), [original](https://github.com/kelvinlee97/engineering/blob/main/Nodejs/guides/modern-bff-architecture-assessment/README.md)
[^express-bff-incidents-runbook]: [Node.js / Express BFF: Ten Common Incidents Runbook](../../sources/express-bff-incidents-runbook.md), [original](https://github.com/kelvinlee97/engineering/blob/main/Nodejs/runbooks/common-express-bff-incidents/README.md)
