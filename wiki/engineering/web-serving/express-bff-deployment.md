---
type: Playbook
title: Express BFF deployment
description: Deploy an Express backend-for-frontend under PM2 cluster mode as an unprivileged user, with immutable releases and symlink rollback.
tags: [nodejs, bff, pm2, deployment, runbook]
sources:
  - id: express-bff-deployment-guide
    resource: https://github.com/kelvinlee97/engineering/blob/main/Nodejs/guides/express-bff-production-deployment/README.md
    title: Node.js / Express BFF Production Deployment for Beginners
    author: human:kelvinlee97
    last_modified: 2026-09-24T14:48:10Z
generated: { by: claude-code/wiki-v1, at: 2026-09-25T04:45:00Z }
status: draft
---
A baseline for deploying an Express [BFF](backend-for-frontend.md) on a Linux VM, with PM2 running several workers as an unprivileged account behind a separately operated gateway.[^express-bff-deployment-guide]

## Host and account

- Use a supported Node.js LTS exact patch version recorded in the change; never an EOL or Current-only line.[^express-bff-deployment-guide]
- Create a system account and group, a release layout under `/srv/<app-name>` (`releases`, `shared`, `shared/logs`), and an environment file `/etc/<app-name>/production.env` owned `root:<app-group>` with mode `0640`. The account gets no root access and no SSH login.[^express-bff-deployment-guide]

## Application contract

A private `GET /healthz` and a graceful exit on `SIGINT` or `SIGTERM` that closes the server and exits within a timeout. Install dependencies with `npm ci`, which needs `package.json` and `package-lock.json` to agree; never run `npm install` on the server to fix a release.[^express-bff-deployment-guide]

The example ecosystem file runs `instances: 2` in `exec_mode: 'cluster'` with `max_memory_restart: '512M'`, `kill_timeout: 30000`, and `watch: false`, loading secrets with `--env-file`. The guide says these are safe examples, not capacity recommendations.[^express-bff-deployment-guide]

## Release and rollback

1. Unpack the approved artifact into a new directory under `releases/`, then run `npm ci --omit=dev`, tests, and `node --check` there.[^express-bff-deployment-guide]
2. Take a baseline (`pm2 status`, `pm2 describe`, `readlink -f current`, health).[^express-bff-deployment-guide]
3. Atomically repoint `current` with `ln -sfn`, then `pm2 start` (first time) or `pm2 reload` (cluster), `pm2 save`, and check status, logs, and health. PM2 can fall back to a restart if workers never become ready.[^express-bff-deployment-guide]
4. Continue only after health, a gateway request, a representative user flow, error rate, and release identity pass. Otherwise repoint `current` to the known-good release and reload; never delete the known-good release during observation.[^express-bff-deployment-guide]

Set up boot recovery once with `pm2 startup` (run only the command it prints, after review) and `pm2 save`; repeat when the Node binary location changes.[^express-bff-deployment-guide]

## Related

- [Express BFF incidents](express-bff-incidents.md)
- [Safe change procedure](../operations/safe-change-procedure.md)
- Source: [Express BFF production deployment guide](../../sources/express-bff-deployment-guide.md)

[^express-bff-deployment-guide]: Node.js / Express BFF Production Deployment for Beginners
