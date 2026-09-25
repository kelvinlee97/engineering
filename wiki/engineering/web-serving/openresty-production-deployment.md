---
type: Playbook
title: OpenResty production deployment
description: Deploy OpenResty on one Ubuntu 24.04 VM with a Lua health endpoint, a loopback reverse proxy, and Certbot HTTPS.
tags: [openresty, nginx, deployment, runbook]
sources:
  - id: openresty-production-guide
    resource: https://github.com/kelvinlee97/engineering/blob/main/Nginx/guides/openresty-production-deployment/README.md
    title: OpenResty Production Deployment and Operations for Beginners
    author: human:kelvinlee97
    last_modified: 2026-09-24T14:48:10Z
generated: { by: claude-code/wiki-v1, at: 2026-09-25T04:45:00Z }
status: draft
---
A baseline for running OpenResty alone on one Ubuntu 24.04 LTS VM. It differs from the [Nginx deployment](nginx-production-deployment.md) mainly in two ways: it installs from OpenResty's package repository, and `/healthz` is served by a Lua script.[^openresty-production-guide]

## When to choose it

Only when the gateway needs reviewed Lua behaviour; ordinary Nginx covers static serving and reverse proxying. OpenResty replaces the Nginx web-server process on the host, so disable Ubuntu's `nginx` (after confirming it serves nothing required) rather than running both.[^openresty-production-guide]

`content_by_lua_file` runs in OpenResty's event-driven request path: no blocking shell commands, blocking file I/O, unbounded loops, secrets, or ad-hoc network calls without a reviewed design.[^openresty-production-guide]

## Steps

1. **Prepare.** Check DNS, ports 80/443, time, CPU architecture (`dpkg --print-architecture`; official x86_64 packages require SSE 4.2), and port ownership.[^openresty-production-guide]
2. **Install.** Add OpenResty's signed apt repository (arm64 uses a different repository URL), install `openresty`, and create `/etc/openresty/conf.d` and `/etc/openresty/lua`. Use the `openresty` command, not a bare `nginx` that may be another binary.[^openresty-production-guide]
3. **Configure.** Write `health.lua` (owned by `root:root`, mode `0644`), a site file whose `/healthz` uses `content_by_lua_file`, and include `conf.d` inside `http {}` of the vendor `nginx.conf` only if no equivalent include exists. Run `openresty -t`, enable, and reload.[^openresty-production-guide]
4. **HTTPS.** As for Nginx: prove HTTP health, issue with Certbot webroot, add the redirect and TLS servers, and dry-run renewal.[^openresty-production-guide]
5. **Verify.** Service, Lua health, upstream health, and TLS separately; then the journal.[^openresty-production-guide]

## Troubleshooting additions

| Symptom | First checks |
| --- | --- |
| `500` on `/healthz` | Error log, Lua path and ownership, config test; never make a broken script return success |
| `502` / `504` | The loopback upstream before blaming Lua |

As described in the guide.[^openresty-production-guide]

## Related

- [Reverse proxy gateway](reverse-proxy-gateway.md)
- [Safe change procedure](../operations/safe-change-procedure.md)
- Source: [OpenResty production deployment guide](../../sources/openresty-production-guide.md)

[^openresty-production-guide]: OpenResty Production Deployment and Operations for Beginners
