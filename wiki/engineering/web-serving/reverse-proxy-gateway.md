---
type: Concept
title: Reverse proxy gateway
description: A server such as Nginx or OpenResty that terminates HTTPS at the edge and forwards requests to an application listening only on a private address.
tags: [nginx, openresty, networking]
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
  - id: modern-bff-assessment
    resource: https://github.com/kelvinlee97/engineering/blob/main/Nodejs/guides/modern-bff-architecture-assessment/README.md
    title: Modern BFF Architecture Assessment for Beginners
    author: human:kelvinlee97
    last_modified: 2026-09-24T14:48:10Z
generated: { by: claude-code/wiki-v1, at: 2026-09-25T04:45:00Z }
status: draft
---
A reverse proxy gateway sits in front of an application: it accepts public traffic, terminates HTTPS, and forwards requests to the application over a private address, so the application port is never exposed directly.[^nginx-production-guide] In this wiki's sources the gateway is Nginx or OpenResty and the upstream is an application on `127.0.0.1:3000`.[^nginx-production-guide][^openresty-production-guide]

## How the pieces are named

Nginx's master process reads and validates configuration and worker processes serve requests. A `server` block is a virtual host, a `location` matches a request path, and `proxy_pass` forwards a request to the upstream application.[^nginx-production-guide]

## Nginx or OpenResty

| | Nginx | OpenResty |
| --- | --- | --- |
| What it is | The web server | An Nginx-based platform with LuaJIT and Lua modules |
| Choose it for | Static serving and reverse proxying | Gateway behaviour that needs reviewed Lua |
| On one host | Not together with OpenResty: both bind ports 80 and 443 | Replaces Nginx; not an add-on |

As described in the two deployment guides.[^nginx-production-guide][^openresty-production-guide]

## Rules that carry across

- Preserve `Host`, `X-Forwarded-For`, and `X-Forwarded-Proto`, and trust them only when traffic is constrained to an approved gateway.[^express-bff-deployment-guide]
- Never expose an unauthenticated development listener directly to the Internet.[^express-bff-deployment-guide]
- At the edge, Nginx and OpenResty remain useful for TLS, routing, rate limiting, and carefully bounded Lua extensions.[^modern-bff-assessment]

## Related

- [Nginx production deployment](nginx-production-deployment.md)
- [OpenResty production deployment](openresty-production-deployment.md)
- [Backend for frontend](backend-for-frontend.md)
- Source: [Nginx production deployment guide](../../sources/nginx-production-guide.md)
- Source: [OpenResty production deployment guide](../../sources/openresty-production-guide.md)
- Source: [Express BFF production deployment guide](../../sources/express-bff-deployment-guide.md)
- Source: [Modern BFF architecture assessment](../../sources/modern-bff-assessment.md)

[^nginx-production-guide]: Nginx Production Deployment and Operations for Beginners
[^openresty-production-guide]: OpenResty Production Deployment and Operations for Beginners
[^express-bff-deployment-guide]: Node.js / Express BFF Production Deployment for Beginners
[^modern-bff-assessment]: Modern BFF Architecture Assessment for Beginners
