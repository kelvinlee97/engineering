---
type: Playbook
title: Express BFF incidents
description: Ten common failure modes of an Express BFF under PM2 cluster mode, each with first checks, recovery, and verification.
tags: [nodejs, bff, pm2, runbook, incident]
sources:
  - id: express-bff-incidents-runbook
    resource: https://github.com/kelvinlee97/engineering/blob/main/Nodejs/runbooks/common-express-bff-incidents/README.md
    title: "Node.js / Express BFF: Ten Common Incidents Runbook"
    author: human:kelvinlee97
    last_modified: 2026-09-24T14:48:10Z
generated: { by: claude-code/wiki-v1, at: 2026-09-25T04:45:00Z }
status: draft
---
Triage for an Express [BFF](backend-for-frontend.md) supervised by PM2 cluster mode. Collect read-only evidence first (`pm2 status`, `pm2 describe`, recent logs, the `current` release target, loopback health, the listener, disk and memory); never start with `pm2 restart`, `reload`, `delete`, or `flush`.[^express-bff-incidents-runbook]

## The ten incidents

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

As described in the runbook.[^express-bff-incidents-runbook] A PM2 memory restart is mitigation, not leak diagnosis; Node diagnostic reports should use `--report-exclude-env` and a restricted directory.[^express-bff-incidents-runbook]

## Related

- [Layered troubleshooting](../operations/layered-troubleshooting.md)
- [Incident closure criteria](../operations/incident-closure-criteria.md)
- [Express BFF deployment](express-bff-deployment.md)
- Source: [Express BFF incidents runbook](../../sources/express-bff-incidents-runbook.md)

[^express-bff-incidents-runbook]: Node.js / Express BFF: Ten Common Incidents Runbook
