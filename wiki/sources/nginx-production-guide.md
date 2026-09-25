---
type: Source Summary
title: Nginx production deployment guide (summary)
description: Summary of the legacy beginner guide for deploying Nginx as a static server and reverse proxy with HTTPS on one Ubuntu 24.04 VM.
tags: [nginx, deployment]
sources:
  - id: nginx-production-guide
    resource: https://github.com/kelvinlee97/engineering/blob/main/Nginx/guides/nginx-production-deployment/README.md
    title: Nginx Production Deployment and Operations for Beginners
    author: human:kelvinlee97
    last_modified: 2026-09-24T14:48:10Z
generated: { by: claude-code/wiki-v1, at: 2026-09-25T04:45:00Z }
status: draft
---
A guide in this repository, `Nginx/guides/nginx-production-deployment/README.md`, for running Nginx alone on one Ubuntu 24.04 LTS VM: static files, a reverse proxy to an application on `127.0.0.1:3000`, and HTTPS through Certbot webroot. It calls itself a deployable baseline, not evidence that any server was deployed.[^nginx-production-guide]

## Takeaways

- Nginx terminates HTTPS and splits requests between static files and a loopback-only application.[^nginx-production-guide] See [Reverse proxy gateway](../engineering/web-serving/reverse-proxy-gateway.md).
- Every change is backed up, tested with `nginx -t`, and applied with a graceful reload.[^nginx-production-guide] See [Safe change procedure](../engineering/operations/safe-change-procedure.md).
- Troubleshooting goes layer by layer from a symptom table.[^nginx-production-guide] See [Nginx production deployment](../engineering/web-serving/nginx-production-deployment.md).

[^nginx-production-guide]: Nginx Production Deployment and Operations for Beginners
