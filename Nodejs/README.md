# Node.js / Express BFF Operations

Chinese version: [README_ZH.md](README_ZH.md)

This module contains beginner-friendly guides for operating a Node.js Express backend-for-frontend (BFF) with PM2 cluster mode. It uses a generalized production model: an external Nginx or OpenResty gateway sends traffic to a private Node.js BFF, which calls approved downstream HTTP services.

The model is deliberately generic. It does not describe any employer's ports, worker count, downstream services, release tooling, or ingress topology.

## Guides

| Guide | Description |
| --- | --- |
| [Production deployment for beginners](guides/express-bff-production-deployment/README.md) | Deploy a non-root Express BFF with PM2, release rollback, health checks, and optional gateway integration. |
| [Modern BFF architecture assessment](guides/modern-bff-architecture-assessment/README.md) | Decide whether a VM/PM2 BFF needs modernization, and select a proportionate platform without treating Kubernetes as mandatory. |

## Runbooks

| Runbook | Description |
| --- | --- |
| [Ten common Node.js / Express BFF incidents](runbooks/common-express-bff-incidents/README.md) | Evidence-first diagnosis and safe recovery for gateway, PM2, runtime, dependency, resource, and release failures. |
