---
type: Source Summary
title: OpenResty production deployment guide (summary)
description: Summary of the legacy beginner guide for deploying OpenResty with a Lua health endpoint and reverse proxy on one Ubuntu 24.04 VM.
tags: [openresty, nginx, deployment]
sources:
  - id: openresty-production-guide
    resource: https://github.com/kelvinlee97/engineering/blob/main/Nginx/guides/openresty-production-deployment/README.md
    title: OpenResty Production Deployment and Operations for Beginners
    author: human:kelvinlee97
    last_modified: 2026-09-24T14:48:10Z
generated: { by: claude-code/wiki-v1, at: 2026-09-25T04:45:00Z }
status: draft
---
A guide in this repository, `Nginx/guides/openresty-production-deployment/README.md`, for running OpenResty (an Nginx-based platform with LuaJIT and Lua modules) alone on one Ubuntu 24.04 LTS VM, with a Lua health endpoint, a reverse proxy to `127.0.0.1:3000`, and Certbot webroot HTTPS.[^openresty-production-guide]

## Takeaways

- Choose OpenResty only when the gateway needs reviewed Lua behaviour; it replaces Nginx on the host rather than running beside it.[^openresty-production-guide] See [OpenResty production deployment](../engineering/web-serving/openresty-production-deployment.md).
- Lua runs in the event-driven request path, so blocking work does not belong there.[^openresty-production-guide]
- The change and verification procedure mirrors the Nginx guide.[^openresty-production-guide] See [Safe change procedure](../engineering/operations/safe-change-procedure.md).

[^openresty-production-guide]: OpenResty Production Deployment and Operations for Beginners
