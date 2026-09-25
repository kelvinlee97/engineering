---
type: Source Summary
title: Express BFF production deployment guide (summary)
description: Summary of the legacy beginner guide for deploying a Node.js Express backend-for-frontend under PM2 cluster mode on a Linux VM.
tags: [nodejs, bff, deployment]
sources:
  - id: express-bff-deployment-guide
    resource: https://github.com/kelvinlee97/engineering/blob/main/Nodejs/guides/express-bff-production-deployment/README.md
    title: Node.js / Express BFF Production Deployment for Beginners
    author: human:kelvinlee97
    last_modified: 2026-09-24T14:48:10Z
generated: { by: claude-code/wiki-v1, at: 2026-09-25T04:45:00Z }
status: draft
---
A guide in this repository, `Nodejs/guides/express-bff-production-deployment/README.md`, for deploying a generic Express backend-for-frontend (BFF) on a Linux VM, with PM2 running several workers as an unprivileged account behind an optional Nginx or OpenResty gateway. It is a repeatable baseline, not evidence about any production service.[^express-bff-deployment-guide]

## Takeaways

- Cluster mode requires stateless workers. See [Backend for frontend](../engineering/web-serving/express-bff.md#backend-for-frontend).
- Releases go into immutable directories, switch with a symlink, and roll back by repointing it.[^express-bff-deployment-guide] See [Express BFF deployment](../engineering/web-serving/express-bff.md#deploying-an-express-bff).

[^express-bff-deployment-guide]: Node.js / Express BFF Production Deployment for Beginners, [original on GitHub](https://github.com/kelvinlee97/engineering/blob/main/Nodejs/guides/express-bff-production-deployment/README.md)
